from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from fastapi import HTTPException, status


SECRET_KEY = "chuoimabimatdetaojwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict, expire_time: Optional[timedelta] = None):
    #Nếu không nhập vào thời gian hết hạn sẽ dùng mặc định là 30 phút
    to_encode = data.copy() #copy tránh làm thay đổi dữ liệu gốc
    if expire_time:
        expire = datetime.now(timezone.utc) + expire_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    #thêm expire time vào to_encode để đưa vào payload
    to_encode.update({"exp": int(expire.timestamp())})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_token(token:str):
    try:
        payload =jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn"
        )
