from base import Base
from producto import Producto


class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        self.__cantidad: int = cantidad
        self.__producto: Producto = producto
        self.__precio_unitario: float = producto.precio
        self.__subtotal: float = cantidad * self.__precio_unitario

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        self.__cantidad = valor
        self.__subtotal = self.__cantidad * self.__precio_unitario

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    def __str__(self) -> str:
        return f"{self.producto.nombre} x {self.cantidad} = ${self.subtotal:.2f}"
