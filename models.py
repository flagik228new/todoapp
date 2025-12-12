from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo = True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    idUser: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    userRole: Mapped[str] = mapped_column(String(128))
    
class Task(Base):
    __tablename__ = 'tasks'
    idTask: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    completed: Mapped[bool] = mapped_column(default=False)
    idUser: Mapped[int] = mapped_column(ForeignKey('users.idUser', ondelete='CASCADE'))
    
class TypesVPN(Base):
    __tablename__ = 'TypesVPN'
    idTypeVPN: Mapped[int] = mapped_column(primary_key=True)
    nameType: Mapped[str] = mapped_column(String(128))
    descriptionType: Mapped[str] = mapped_column(String(128))
    
class CountriesOpen(Base):
    __tablename__ = 'CountriesOpen'
    idCountry: Mapped[int] = mapped_column(primary_key=True)
    nameType: Mapped[str] = mapped_column(String(128))
    
class ServersVPN(Base):
    __tablename__ = 'ServersVPN'
    idVPN: Mapped[int] = mapped_column(primary_key=True)
    idTypeVPN: Mapped[int] = mapped_column(ForeignKey('TypesVPN.idTypeVPN', ondelete='CASCADE'))
    idCountry: Mapped[int] = mapped_column(ForeignKey('CountriesOpen.idCountry', ondelete='CASCADE'))
    
    
    
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
"""
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    
class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    completed: Mapped[bool] = mapped_column(default=False)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    
    
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
"""