from datetime import date
from base import Base
from calculable import Calculable
from usuario import Usuario
from producto import Producto
from detalle_pedido import DetallePedido
from enums import Estado, FormaPago
from exepciones import StockInsuficienteError, OperacionNoPermitidaError


class Pedido(Base, Calculable):
    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        if not isinstance(usuario, Usuario) or usuario.eliminado:
            raise ValueError("El pedido requiere un usuario activo")
        self.__usuario: Usuario = usuario
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__forma_pago: FormaPago = forma_pago
        self.__total: float = 0.0
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @estado.setter
    def estado(self, valor: Estado) -> None:
        transiciones = {
            Estado.PENDIENTE: [Estado.CONFIRMADO, Estado.CANCELADO],
            Estado.CONFIRMADO: [Estado.TERMINADO, Estado.CANCELADO],
            Estado.TERMINADO: [],
            Estado.CANCELADO: []
        }
        if valor != self.__estado and valor not in transiciones[self.__estado]:
            raise OperacionNoPermitidaError("Transicion de estado no permitida")
        self.__estado = valor

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise ValueError("Forma de pago invalida")
        self.__forma_pago = valor

    @property
    def total(self) -> float:
        return self.__total

    @property
    def detalles(self) -> tuple:
        return tuple(self.__detalles)

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        if producto.eliminado or not producto.disponible:
            raise OperacionNoPermitidaError("El producto no esta disponible")
        detalle = self.buscar_detalle_por_producto(producto)
        cantidad_actual = detalle.cantidad if detalle else 0
        if cantidad_actual + cantidad > producto.stock:
            raise StockInsuficienteError(f"Stock insuficiente para {producto.nombre}")
        if detalle:
            detalle.cantidad = cantidad_actual + cantidad
        else:
            self.__detalles.append(DetallePedido(cantidad, producto))
        self.calcular_total()

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle:
            self.__detalles.remove(detalle)
            self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = sum(detalle.subtotal for detalle in self.__detalles)

    def __str__(self) -> str:
        return (f"Pedido {self.id} | {self.usuario.nombre} | {self.estado.value} | "
                f"${self.total:.2f}")
