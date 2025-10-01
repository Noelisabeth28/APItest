from fastapi import FastAPI

# Crear la app
app = FastAPI()

# Endpoint de prueba
@app.get("/")
def read_root():
    return {"mensaje": "Hola, esta es mi primera API con FastAPI"}

# Endpoint con parámetro
@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"Hola {nombre}, bienvenido a la API"}
