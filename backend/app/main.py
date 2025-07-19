from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.routes import assistant, users, doctors, patients, schedule, appointments
from app.database import Base, engine
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="ASSCORP")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await create_tables()


app.include_router(assistant.router, prefix="/api")
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(patients.router, prefix="/patient", tags=["Patients"])
app.include_router(schedule.router, prefix="/schedule", tags=["Schedule"])
app.include_router(
    appointments.router, prefix="/api/appointments", tags=["appointments"]
)


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/contacts", response_class=HTMLResponse)
async def contacts_page(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request})


@app.get("/account", response_class=HTMLResponse)
async def account_page(request: Request):
    return templates.TemplateResponse("account.html", {"request": request})


@app.get("/appointment", response_class=HTMLResponse)
async def appointment_page(request: Request):
    return templates.TemplateResponse("appointment.html", {"request": request})
