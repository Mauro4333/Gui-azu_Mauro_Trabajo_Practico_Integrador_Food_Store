from base import Base
from categoria import Categoria
from exepciones import PrecioInvalidoError


class Producto(Base):
    def __init__(self, nombre: str, precio: float, descripcion: str,
                 stock: int, imagen: str, disponible: bool,
                 categoria: Categoria) -> None:
        super().__init__()
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.categoria = categoria

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacio")
        self.__nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor < 0:
            raise PrecioInvalidoError("El precio no puede ser negativo")
        self.__precio = float(valor)

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La descripcion no puede estar vacia")
        self.__descripcion = valor.strip()

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("El stock debe ser un entero mayor o igual a cero")
        self.__stock = valor

    @property
    def imagen(self) -> str:
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        self.__imagen = str(valor).strip()

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise ValueError("La disponibilidad debe ser verdadera o falsa")
        self.__disponible = valor

    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        if not isinstance(valor, Categoria) or valor.eliminado:
            raise ValueError("Debe seleccionar una categoria activa")
        self.__categoria = valor

    def __str__(self) -> str:
        return (f"{self.id} - {self.nombre} | ${self.precio:.2f} | "
                f"Stock: {self.stock} | {self.categoria.nombre}")