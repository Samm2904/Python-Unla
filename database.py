from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship #Agregue relationshop para poder hacer relaciones entre tablas
from sqlalchemy.ext.declarative import declarative_base #Lo agregue porque asi lo tenia Gonzalo

## Creo el motor base

engine = create_engine('sqlite:///database.db', echo=True)

#Crear una sesion para interactuar con la base
session = scoped_session(sessionmaker(bind=engine)) #scoped session la aisla y evita problemas de hilos
# Declaro la base

Base = declarative_base()
Base.query = session.query_property() #Agregue esto para poder hacer consultas a la base de datos

# Creo las clases que representan las tablas // serian productos - ventas
#Modifico todo en ingles xq asi lo piden
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    name = Column(String(100), nullable = False) #El string(100) es para limitar la cantidad de caracteres que puede tener el nombre del producto
    price = Column(Float, nullable = False)

    sales = relationship('Sale', back_populates='product') #Agregue esto para poder hacer la relacion entre las tablas, que sepa que puede tener mas de uno



class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    date = Column(Date, nullable = False)
    time = Column(Time, nullable = False)
    id_product = Column(Integer, ForeignKey('products.id'), nullable = False)
    quantity = Column(Integer, nullable = False)
    total_price = Column(Float, nullable = False)

    product = relationship('Product', back_populates='sales')


# Crear las tablas en el archivo si no existen
Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)