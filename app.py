from fastapi import FastAPI, HTTPException, status
from database import Producto, Venta, session #Esta bien la declaracion de session como == de db??? Consultar 

#Instacio fastApi
app = FastAPI() 

#Listar cada producto
@app.get("/productos")
def listar_productos(): #consultar si etsa bien no pasar parametros
 
    producto = session.query(Producto).all() #Consultar por la estructura del query
    if producto is not None:
         return [vars(p) for p in producto]  
    else:
        raise HTTPException(status_code=204, detail="No hay productos")
   

#Obtener un solo producto por su id
@app.get("/productos/{id}")
def obtener_productos(id:int):
    producto = session.query(Producto).get(id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado") 
    else:
        return vars(producto)

#Modificar un producto segun su id
@app.put("/productos/{id}")
def modificar_producto(id:int, datos_producto): 
    producto = session.query(Producto).get(id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    try: 
        producto.nombre = datos_producto.nombre  #Consultar si esta bien acceder como un struct
        producto.precio = datos_producto.precio 
        session.commit()
        return vars(producto)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error inesperado en el servidor")
        #Esta bien asi o si o si necesito un return??

#Agregar producto nuevo
@app.post("/productos", status_code=status.HTTP_201_CREATED)
def agregar_producto(datos_producto):
    try:
        producto_nuevo = Producto(
            # id = lo dejo vacio porque es autoincremental
            nombre = datos_producto.nombre,
            precio = datos_producto.precio 
        )
        session.add(producto_nuevo)
        session.commit()
        session.refresh(producto_nuevo)
        return vars(producto_nuevo)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error al crear productos, datos invalidos o nulos")

#Eliminar producto
@app.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_producto(id: int):
    try:
        producto = session.query(Producto).get(id)
        if producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        session.delete(producto)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error inesperado al borrar producto")