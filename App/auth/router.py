from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from ..database import get_db
from . import models, schemas

router = APIRouter()

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
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")
    
    # Check username
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
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
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    return user
