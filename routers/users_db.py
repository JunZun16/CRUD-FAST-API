#USER DB API 

from fastapi import APIRouter,HTTPException,status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema,users_schema
from bson import ObjectId


router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})
# Inicia el server: uvicorn users:router --reload

users_list=[]

#busqueda de todos los usuarios
@router.get("/",response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())

#Busqueda por path
@router.get("/{id}")
async def user(id:str):
    return search_user("_id",ObjectId(id))

#Busqueda por query
@router.get("/")  
async def user(id: str):
    return search_user("_id",ObjectId(id))

#funcion pa buscar
##################################################### GET
def search_user(field: str, key):
    
    try:
        user=db_client.local.users.find_one({field:key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}


##añadir usuarios o insertar valores
##################################################### POST
@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED)
async def user(user:User):
    if type(search_user("email",user.email))==User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="El usuario ya Existe")
        
    user_dict=dict(user)
    #eliminar el id para que la bd lo genera automaticamente
    del user_dict["id"]
    
    id=db_client.local.users.insert_one(user_dict).inserted_id
    
    new_user= user_schema(db_client.local.users.find_one({"_id":id}))
    
    return User(**new_user)
#actualizar
###################################################### PUT
@router.put("/",response_model=User)
async def user(user:User):
    user_dict=dict(user)
    del user_dict["id"]
    try:
        db_client.local.users.find_one_and_replace({"_id":ObjectId(user.id)},user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return search_user({"_id":ObjectId(user.id)})
    
#Eliminar
##################################################### DELETE
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = db_client.local.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    
    