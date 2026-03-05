import json
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="API de Chistes Temáticos")

# Modelos de Datos
class Chiste(BaseModel):
    categoria: str
    texto: str

# Lee json de bromas
def cargar_datos() -> Dict[str, List[str]]:
    try:
        with open("./src/jokes/chistes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_datos(datos: Dict[str, List[str]]):
    with open("./src/jokes/chistes.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# Endpoints
@app.get("/chiste/{categoria}")
async def obtener_chiste(categoria: str):
    datos = cargar_datos()
    if categoria not in datos or not datos[categoria]:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada o vacía"
            )
    
    chiste_aleatorio = random.choice(datos[categoria])
    return {"categoria": categoria, "chiste": chiste_aleatorio}

@app.post("/chiste/")
async def añadir_chiste(nuevo_chiste: Chiste):
    datos = cargar_datos()
    cat = nuevo_chiste.categoria.lower()
    
    if cat not in datos:
        datos[cat] = []
    
    datos[cat].append(nuevo_chiste.texto)
    guardar_datos(datos)
    return {"message": "Chiste añadido con éxito", "data": nuevo_chiste}

@app.put("/chiste/{categoria}")
async def reemplazar_categoria(categoria: str, chistes: List[str]):
    """Reemplaza toda la lista de chistes de una categoría"""
    datos = cargar_datos()
    datos[categoria.lower()] = chistes
    guardar_datos(datos)
    return {"message": f"Categoría {categoria} actualizada"}

@app.patch("/chiste/{categoria}/{index}")
async def editar_chiste_especifico(categoria: str, index: int, nuevo_texto: str):
    """Edita un chiste específico por su índice en la lista"""
    datos = cargar_datos()
    if categoria in datos and 0 <= index < len(datos[categoria]):
        datos[categoria][index] = nuevo_texto
        guardar_datos(datos)
        return {"message": "Chiste modificado"}
    raise HTTPException(status_code=404, detail="No se encontró el chiste")

@app.delete("/chiste/{categoria}")
async def eliminar_categoria(categoria: str):
    datos = cargar_datos()
    if categoria in datos:
        del datos[categoria]
        guardar_datos(datos)
        return {"message": f"Categoría {categoria} eliminada"}
    raise HTTPException(status_code=404, detail="Categoría no encontrada")