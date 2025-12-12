from sqlalchemy import select, update, delete, func
from models import async_session, User, Task
from pydantic import BaseModel, ConfigDict
from typing import List


class TaskView(BaseModel):
    idTask: int
    title: str
    completed: bool
    idUser: int
    
    model_config = ConfigDict(from_attributes=True)


async def add_user(tg_id, user_role):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user
        
        new_user = User(tg_id=tg_id, userRole="Пользователь")
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def get_tasks(user_id):
    async with async_session() as session:
        tasks = await session.scalars(
            select(Task).where(Task.idUser == user_id, Task.completed == False)
        )
        
        serialized_tasks = [
            TaskView.model_validate(t).model_dump() for t in tasks
        ]
        
        return serialized_tasks


async def get_completed_tasks_count(user_id):
    async with async_session() as session:
        return await session.scalar(select(func.count(Task.idTask)).where(Task.completed == True, Task.idUser == user_id))


async def add_task(user_id, title):
    async with async_session() as session:
        new_task = Task(
            title=title,
            idUser=user_id
        )
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return new_task


async def update_task(task_id):
    async with async_session() as session:
        await session.execute(update(Task).where(Task.idTask == task_id).values(completed=True))
        await session.commit()
        
        
class TaskAdminView(BaseModel):
    idTask: int
    title: str
    completed: bool
    idUser: int

    model_config = ConfigDict(from_attributes=True)
    
async def admin_get_tasks():
    async with async_session() as session:
        tasks = await session.scalars(select(Task))
        return [TaskAdminView.model_validate(t).model_dump() for t in tasks]
    
async def admin_add_task(title: str, completed: bool, idUser: int):
    async with async_session() as session:
        new_task = Task(title=title, completed=completed, idUser=idUser)
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return TaskAdminView.model_validate(new_task).model_dump()
    
async def admin_update_task(task_id: int, title: str, completed: bool, idUser: int):
    async with async_session() as session:
        await session.execute(update(Task)
                              .where(Task.idTask == task_id)
                              .values(title=title,completed=completed, idUser=idUser)
        )
        await session.commit()
        return {'status': 'ok'}
    
async def admin_delete_task(task_id: int):
    async with async_session() as session:
        await session.execute(delete(Task).where(Task.idTask == task_id))
        await session.commit()
        return {'status': 'ok'}
    
async def admin_get_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return [{"idUser": u.idUser, "tg_id": u.tg_id, "userRole": u.userRole} for u in users]