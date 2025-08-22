# My Project
## commands
- python -m app.main
- uvicorn app.main:app --reload
- fastapi dev .\main.py
- python -m uvicorn App.main:app --reload


##Các việc cần làm:
- Cấu trúc dự án chuẩn có thể tham khảo: https://github.com/zhanymkanov/fastapi-best-practices
- đọc lại về chuẩn pep8
- đọc về quy chuẩn thiết kế API: https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design

## Alchemy
### Tạo migration đầu tiên
alembic revision --autogenerate -m "Initial migration"

### Chạy migration
alembic upgrade head

### chạy server 
python run.py


# Từ thư mục gốc
uvicorn App.main:app --reload --host 0.0.0.0 --port 8000

# Từ thư mục App
uvicorn main:app --reload --host 0.0.0.0 --port 8000