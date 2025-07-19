# Структура файлов
```
├── .env     # Переменные окружения
├── README.md
├── backend
│   ├── Dockerfile
│   ├── app
│   │   ├── __init__.py        
│   │   ├── __pycache__        
│   │   ├── auth.py
│   │   ├── database.py        
│   │   ├── dependencies.py    
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routes
│   │   │   ├── __init__.py    
│   │   │   ├── __pycache__    
│   │   │   ├── appointments.py
│   │   │   ├── assistant.py   
│   │   │   ├── doctors.py     
│   │   │   ├── patients.py    
│   │   │   ├── schedule.py    
│   │   │   └── users.py
│   │   ├── schemas.py
│   │   ├── static
│   │   │   ├── Background.webp
│   │   │   ├── account.css
│   │   │   ├── appointment.css
│   │   │   ├── contacts.css
│   │   │   ├── login.css
│   │   │   ├── main.css
│   │   │   └── style.css
│   │   └── templates
│   │       ├── account.html
│   │       ├── appointment.html
│   │       ├── contacts.html
│   │       ├── index.html
│   │       ├── login.html
│   │       ├── patient_appointments.html
│   │       └── register.html
│   ├── requirements.txt
│   └── venv
└── docker-compose.yml
```
---

## Комментарии по файлам и папкам

### Корень проекта

- **README.md**  
  Документация.

- **docker-compose.yml**  
  Конфигурация для запуска контейнеров Docker (backend, БД и др.).

---

### Папка `backend`

- **Dockerfile**  
  Описание образа Docker для backend-приложения.

- **requirements.txt**  
  Список Python-зависимостей проекта.

---

### Папка `app`

- **`__init__.py`**  
  Позволяет Python трактовать папку как пакет. (Для других файлов)

- **auth.py**  
  Логика аутентификации, генерация и проверка токенов.

- **database.py**  
  Настройка подключения к базе данных.

- **dependencies.py**  
  Общие зависимости и вспомогательные функции для FastAPI.

- **main.py**  
  Точка входа приложения — создание и запуск FastAPI.

- **models.py**  
  Описания моделей базы данных (ORM).

- **schemas.py**  
  Pydantic-схемы для валидации и сериализации данных.


---

### Папка `routes`

- **appointments.py**  
  Маршруты для работы с приёмами пациентов.

- **doctors.py**  
  Маршруты для работы с данными врачей.

- **patients.py**  
  Маршруты для работы с пациентами.

- **schedule.py**  
  Маршруты для расписаний приёмов.

- **users.py**  
  Маршруты для работы с пользователями (регистрация, профиль).

---

### Папка `static`

  Стили для фронтенд-страниц.

---

### Папка `templates`
  Совместно с папкой `static` - фронтенд.

---
