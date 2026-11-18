from funciones import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio
from enums import *
from exepciones import StockInsuficienteError


def main() -> None:
    categorias = CategoriaServicio()
    productos = ProductoServicio()
    usuarios = UsuarioServicio()
    pedidos = PedidoServicio()

    categoria = categorias.crear("Bebidas", "Bebidas frías")
    producto = productos.crear("Agua", 1000, "Botella 500 ml", 3, "", True, categoria)
    usuario = usuarios.crear("Ana", "Pérez", "ana@gmail.com", "261123", "1234", Rol.USUARIO)

    pedido = pedidos.crear(usuario, FormaPago.EFECTIVO, [(producto, 2)])
    print("Caso válido:", pedido)
    print("Stock restante:", producto.stock)
    print("Total calculado:", pedido.total)

    try:
        pedidos.crear(usuario, FormaPago.EFECTIVO, [(producto, 5)])
    except StockInsuficienteError as error:
        print("Error esperado:", error)

    pedidos.cambiar_estado(pedido.id, Estado.CANCELADO)
    print("Pedido cancelado:", pedido.estado.value)
    print("Stock devuelto:", producto.stock)


if __name__ == "__main__":
    main()