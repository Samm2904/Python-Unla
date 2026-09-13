from fastapi import FastAPI, HTTPException, status
from database import Product, Sale, session #Esta bien la declaracion de session como == de db??? Consultar 
from schema import ProductResponse, ProductCreate, SaleCreate, SaleResponse
#Instacio fastApi
app = FastAPI() 

#Listar cada producto
@app.get("/products")
async def get_products(): #consultar si etsa bien no pasar parametros
    try:
        products = session.query(Product).all() #Consultar por la estructura del query
        response = {"products": products} #Creo el diccionario para hcaerlo tipo JSON
        return response   #Devuelve la respuesta

    except Exception as e:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Hubo un error al tratar de obtener productos: {e}")
        

#Obtener un solo producto por su id
@app.get("/products/{id}")
async def get_product(id:int):
    try:
        product = session.query(Product).get(id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado") 
        
        response = {"product": product}
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error ocurrido al intentar encontrar el producto con id {id}: {e}")


#Modificar un producto segun su id
@app.put("/products/{id}", status_code=status.HTTP_200_OK)
async def modify_product(id:int, product_data: ProductCreate): 
    try:
        products = session.query(Product).get(id)

        if products is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        products.name = product_data.name  #Consultar si esta bien acceder como un struct
        products.price = product_data.price 

        response = {"product": products}
        session.commit()

        return response
    except HTTPException:
        session.rollback()
        raise    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error ocurrido al tratar de crear el producto: {e}")

#Agregar producto nuevo
@app.post("/products", status_code=status.HTTP_201_CREATED)
async def create_products(product_data: ProductCreate):
    try:

        new_product = session.query(Product).filter_by(name=product_data.name).first()

        if new_product:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Producto ya existente")

        new_product = Product(
            # id = lo dejo vacio porque es autoincremental
            name = product_data.name,
            price = product_data.price 
        )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        response = {"product": new_product}

        return response
    except HTTPException:
        session.rollback()
        raise   
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error al crear productos, datos invalidos o nulos")

#Eliminar producto
@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int):
    try:
        products = session.query(Product).get(id)
        if products is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto de {id} no encontrado")
        session.delete(products)
        session.commit()
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error inesperado al borrar producto")