from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.database import Base, engine
from app.routes import users, doctors, patients, schedule, appointments

app = FastAPI(title="ASSCORP")


app.mount("/static", StaticFiles(directory="app/static"), name="static")


templates = Jinja2Templates(directory="app/templates")


Base.metadata.create_all(bind=engine)


app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(schedule.router, prefix="/schedule", tags=["Schedule"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):

    return templates.TemplateResponse("login.html", {"request": request})
