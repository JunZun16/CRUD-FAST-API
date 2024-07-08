
from fastapi import FastAPI
from routers import products,users,jwt_auth_users,basic_auth_auth,users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

##ROUTERS
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_auth.router)
app.include_router(users_db.router)

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/")
async def root():
    return "Hola FastAPI!"

@app.get("/url")
async def url():
    return {"url_curso":"https://juancarlos.com.com/python"}

# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc