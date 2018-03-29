# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class CityList(Base):
    # 表的名字:
    __tablename__ = 'city_list'


# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:mysql@localhost:3306/ganji')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

session = DBSession()

session.close()