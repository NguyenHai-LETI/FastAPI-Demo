from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..database import get_db
from . import models, schemas
from .services import create_access_token, verify_token

router = APIRouter()
# Khởi tạo một đối tượng CryptContext khai báo thuật toán hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", 
    response_model=schemas.UserResponse,
    status_code=201,
    summary="Tạo user mới",
    description="Tạo một user mới với username và email. Hệ thống sẽ kiểm tra trùng lặp trước khi tạo."
)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    # Check email - Query lấy bản ghi đầu tiên thỏa mãn filter
    db_user = db.query(models.User).filter_by(email = user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")
    
    # Check username
    db_user = db.query(models.User).filter_by(username = user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username đã tồn tại")
    
    # Tạo user mới
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password="default_password",
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", 
    response_model=list[schemas.UserResponse],
    summary="Lấy danh sách user",
    description="Lấy danh sách tất cả user"
)
def get_users(
    skip: int = Query(0, ge=0, description="Số user bỏ qua"),
    limit: int = Query(100, ge=1, le=1000, description="Số user tối đa trả về"),
    db: Session = Depends(get_db)
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", 
    response_model=schemas.UserResponse,
    summary="Lấy thông tin user",
    description="Lấy thông tin chi tiết của user theo ID"
)

def get_user(
    user_id: int = Path(..., gt=0, description="ID của user"),
    db: Session = Depends(get_db)
):
    """... - chỉ định đây là giá trị bắt buoc;
    gt=0 - greater than 0 """
    user = db.query(models.User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    return user


@router.post('/register',
    response_model=schemas.UserResponse,
    status_code=201,
    summary='Đăng Ký',
    description='Đăng ký ứng dụng'
)
def register_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    #sanitize data
    email = user.email
    username = user.username.strip()
    hash_password = pwd_context.hash(user.password)

    # check email or username are exist in db
    db_user = db.query(models.User).filter(or_(models.User.email == email
                                           ,models.User.username == username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email hoặc username đã tồn tại")

    # Tạo user mới
    db_user = models.User(
        username=username,
        email=email,
        hashed_password=hash_password,
    )
    print("tạo user mới với mật khẩu: " + hash_password)
    #xử lí ngoại lệ khi commit db
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        #db.rollback() #Cần rollback db trong dự án thực tế
        raise HTTPException(status_code=400, detail=str(e))
    return db_user

@router.post('/login',
    response_model=schemas.TokenResponse,
    summary='Đăng nhập',
    description='Đăng nhập ứng dụng'
)
def login_user(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    user_db = db.query(models.User).filter_by(email=user.email).first()
    #Check user_db is not None
    if not user_db or not pwd_context.verify(user.password, user_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    #Check password
    if not pwd_context.verify(user.password, user_db.hashed_password):
        raise  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    #Tạo access token
    token_data = {
        "sub": user_db.username,
    }
    access_token = create_access_token(
        token_data,
        expire_time = timedelta(minutes = 10)
    )

    return schemas.TokenResponse.model_validate(
        {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_db
        },
        from_attributes=True
    )