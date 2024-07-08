
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

router = APIRouter()

# Inicia el server: uvicorn users:router --reload

#Entidad user
class User(BaseModel):
    id:int
    nombre:str
    apellido:str
    url:str
    edad:int
    

users_list=[User(id=1,nombre="Juan",apellido="zuniga",url="https://juan.com",edad=24),
            User(id=2,nombre="daniel",apellido="Gomez",url="https://dani.com",edad=33),
            User(id=3,nombre="Iltse",apellido="Gonzalez",url="https://iltse.com",edad=22),
            User(id=4,nombre="Venegas",apellido="Fernandiño",url="https://venedick.com",edad=29),]

@router.get("/usersjson")
async def usersjson():
    return [{"nombre":"juan","apellido":"Zuñiga","url":"https://juan.com","edad":"19"},
            {"nombre":"daniel","apellido":"Gomez","url":"https://dani.com","edad":"19"},
            {"nombre":"Iltse","apellido":"Gonzalez","url":"https://iltse.com","edad":"19"}]


@router.get("/users")
async def users():
    return users_list

#path
@router.get("/user/{id}")
async def user(id:int):
    return search_user(id)

#query
@router.get("/user/")  
async def user(id: int):
    return search_user(id)

#funcion pa buscar
#####################################################GET
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}


##añadir usuarios o insertar valores
#####################################################POST
@router.post("/user/",status_code=201)
async def user(user:User):
    if type(search_user(user.id))==User:
        raise HTTPException(status_code=204,detail="El usuario ya Existe")
        
    else:
        users_list.append(user)
        return user

        
#actualizar
#####################################################PUT
@router.put("/user/")
async def user(user:User):
    found=False
    for index,save_user in enumerate(users_list):
        if save_user.id==user.id:
            users_list[index]=user
            found=True
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user
    
    
#Eliminar
#####################################################DELETE
@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "No se ha eliminado el usuario"}