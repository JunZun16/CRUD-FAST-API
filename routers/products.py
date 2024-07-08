from fastapi import APIRouter
from pydantic import BaseModel

router=APIRouter(prefix="/productos",
                 tags=["productos"],
                 responses={404:{"meensaje":"No encontrado"}})

productos_list=["Producto 1","Producto 2","Producto 3","Producto 4","Producto 5","Producto 6"]

@router.get("/")
async def productos():
    return productos_list

@router.get("/{id}")
async def productos(id:int):
    return productos_list[id]
    