from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

# Crear la app
models.Base.metadata.create_all(bind=engine)  # crea la tabla si no existe

app = FastAPI(title="API CRUD de Productos")



# Endpoint de prueba
# @app.get("/")
# def read_root():
#     return {"mensaje": "Hola, esta es mi primera API con FastAPI"}

# # Endpoint con parámetro
# @app.get("/saludo/{nombre}")
# def saludar(nombre: str):
#     return {"mensaje": f"Hola {nombre}, bienvenido a la API"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/productos/", response_model=schemas.ProductoResponse)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    nuevo = models.Producto(**producto.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# 📌 Listar productos
@app.get("/productos/", response_model=list[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()

# 📌 Obtener producto por ID
@app.get("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# 📌 Actualizar producto
@app.put("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def actualizar_producto(producto_id: int, datos: schemas.ProductoUpdate, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(producto, key, value)
    db.commit()
    db.refresh(producto)
    return producto

# 📌 Eliminar producto
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {
    "mensaje": "Producto eliminado con éxito",
    "id_eliminado": producto_id
}