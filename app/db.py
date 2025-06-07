# DB connection setup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def connect_to_postgresql(host, database, user, password, port=5432):
    """
    Kết nối đến cơ sở dữ liệu PostgreSQL.
    :param host: Địa chỉ máy chủ PostgreSQL
    :param database: Tên cơ sở dữ liệu
    :param user: Tên người dùng
    :param password: Mật khẩu
    :return: Đối tượng kết nối
    """
    try:
        # Tạo kết nối đến cơ sở dữ liệu
        # Replace with your PostgreSQL connection string
        DATABASE_URL = "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

        # Set up the database engine and session
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)

        print("Kết nối thành công đến PostgreSQL://{user}:{password}@{host}:{port}/{database}".format(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        ))
        
        return {
            'engine': engine,
            'SessionLocal': SessionLocal
        }
    except Exception as e:
        print(f"Lỗi khi kết nối đến PostgreSQL: {e}")
        return None