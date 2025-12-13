from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from models import init_db
import requestsfile as rq
    

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print('Bot is ready!')
    yield

app = FastAPI(title='To Do App', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://*.github.dev",
        "https://todoapp-10f89.web.app",
        "https://todoapp-10f89.firebaseapp.com",
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class AddTask(BaseModel):
    tg_id: int
    title: str
    
class CompleteTask(BaseModel):
    id: int
    
# --- CRUD для задач (админка) ---
class AdminTaskCreate(BaseModel):
    title: str
    completed: bool
    idUser: int

class AdminTaskUpdate(BaseModel):
    title: str
    completed: bool
    idUser: int
    
    
@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id: int):
    user = await rq.add_user(tg_id, "Пользователь")
    return await rq.get_tasks(user.idUser)

@app.get("/api/main/{tg_id}")
async def profile(tg_id: int):
    user = await rq.add_user(tg_id, "Пользователь")
    completed_tasks_count = await rq.get_completed_tasks_count(user.idUser)
    return {'completedTasks': completed_tasks_count, 'userRole':user.userRole}

@app.post("/api/add")
async def add_task(task: AddTask):
    user = await rq.add_user(task.tg_id, "Пользователь")
    await rq.add_task(user.idUser, task.title)
    return {'status': 'ok'}

@app.patch("/api/completed")
async def complete_task(task: CompleteTask):
    await rq.update_task(task.id)
    return {'status': 'ok'}

# для админки
@app.get("/api/admin/tasks")
async def admin_get_tasks():
    return await rq.admin_get_tasks()

@app.post("/api/admin/tasks")
async def admin_add_task(task: AdminTaskCreate):
    return await rq.admin_add_task(task.title, task.completed, task.idUser)

@app.patch("/api/admin/tasks/{task_id}")
async def admin_update_task(task_id: int, task: AdminTaskUpdate):
    return await rq.admin_update_task(task_id, task.title, task.completed, task.idUser)

@app.delete("/api/admin/tasks/{task_id}")
async def admin_delete_task(task_id: int):
    return await rq.admin_delete_task(task_id)

# --- Получение пользователей (для select) ---
@app.get("/api/admin/users")
async def admin_get_users():
    return await rq.admin_get_users()