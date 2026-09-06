from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

## Creo el motor base:

engine = create_engine('sqlite:///database.db', echo=True)

# Declaro la base

Base = declarative_base()

# Creo las clases que representan las tablas // serian productos - ventas
class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    nombre = Column(String, nullable = False)
    precio = Column(Float, nullable = False)

class Venta(Base):
    __tablename__ = 'ventas'
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    fecha = Column(Date, nullable = False)
    hora = Column(Time, nullable = False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable = False)
    cantidad = Column(Integer, nullable = False)
    precio_total = Column(Float, nullable = False)


# Crear las tablas en el archivo si no existen
Base.metadata.create_all(engine)

#Crear una sesion para interactuar con la base
Session = sessionmaker(bind=engine)
session = Session()

#agregar y consultar???