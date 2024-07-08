from fastapi import FastAPI,Depends, HTTPException,status,APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta

algoritmo= "HS256"
ACCESS_TOKEN_DURATION=1
SECRET="ASDFGHJKL1234567890"

router = APIRouter()

oauth2=OAuth2PasswordBearer(tokenUrl="login")

crypt=CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username:str
    full_name:str
    email:str
    disabled:bool
    
    
class UserDB(User):
    password:str    


users_db={
    "juanca":{
        "username":"juanca",
        "full_name":"Juan Carlos",
        "email":"zunigaperez@gmail.com",
        "disabled":False,
        "password":"$2a$12$v57fQzFAAgiXeZxQSeXEt.RbeyinuizdctMdv6W9.seYgVJQQZiVO"
    },
    "iltse":{
        "username":"iltse",
        "full_name":"Iltse Raquel",
        "email":"maruchon@gmail.com",
        "disabled":True,
        "password":"$2a$12$V6jJ5CNc5SV9PiwEv2BTk.HjNZYwySOUzuj8EkJremum7VxHYqtim"
    }
}

########BUSQUEDA DE USUARIOS
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

########BUSQUEDA DE USUARIO
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token:str=Depends(oauth2)):

    
    try:
        username=jwt.decode(token,SECRET,algorithms=[algoritmo]).get("sub")
        if username is None:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})
        
    except JWTError: 
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})
        
    return search_user(username)
    
########
#NOS DECIA CUAL ERA EL USAURIO DE LA SESION
async def current_user(user:User=Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user

#######
#AUTENTICACION
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm=Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    
    
    
    if not crypt.verify(form.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
        
    access_token_duration=timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    access_token={"sub":user.username,
                  "exp":expire}
        
    return {"access_token":jwt.encode(access_token,SECRET,algorithm=algoritmo) ,"token_type":"bearer"}


########
#PARA OBTENER DATOS DEL USUARIO
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

