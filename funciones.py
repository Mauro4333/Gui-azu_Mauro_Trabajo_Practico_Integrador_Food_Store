from categoria import *
from exepciones import *
from producto import *
from usuario import *
from enums import *
from pedido import *


class CategoriaServicio:
    def __init__(self) -> None:
        self._categorias: list[Categoria] = []

    def listar(self) -> list[Categoria]:
        return [c for c in self._categorias if not c.eliminado]

    def buscar(self, id_categoria: int) -> Categoria:
        for categoria in self._categorias:
            if categoria.id == id_categoria and not categoria.eliminado:
                return categoria
        raise EntidadNoEncontradaError("Categoria inexistente")

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        if any(c.nombre.lower() == nombre.strip().lower() and not c.eliminado for c in self._categorias):
            raise DuplicadoError("Ya existe una categoria con ese nombre")
        categoria = Categoria(nombre, descripcion)
        self._categorias.append(categoria)
        return categoria

    def editar(self, id_categoria: int, nombre: str, descripcion: str) -> None:
        categoria = self.buscar(id_categoria)
        if any(c.id != id_categoria and c.nombre.lower() == nombre.strip().lower()
               and not c.eliminado for c in self._categorias):
            raise DuplicadoError("Ya existe una categoria con ese nombre")
        categoria.nombre = nombre
        categoria.descripcion = descripcion

    def eliminar(self, id_categoria: int, productos: list) -> None:
        categoria = self.buscar(id_categoria)
        cantidad = sum(1 for p in productos if p.categoria == categoria and not p.eliminado)
        if cantidad:
            raise OperacionNoPermitidaError(f"No se puede eliminar: tiene {cantidad} producto(s) activo(s)")
        categoria.eliminado = True

class ProductoServicio:
    def __init__(self) -> None:
        self._productos: list[Producto] = []

    def listar(self, solo_disponibles: bool = False) -> list[Producto]:
        return [p for p in self._productos if not p.eliminado
                and (not solo_disponibles or (p.disponible and p.stock > 0))]

    def buscar(self, id_producto: int) -> Producto:
        for producto in self._productos:
            if producto.id == id_producto and not producto.eliminado:
                return producto
        raise EntidadNoEncontradaError("Producto inexistente")

    def crear(self, nombre: str, precio: float, descripcion: str, stock: int,
              imagen: str, disponible: bool, categoria) -> Producto:
        producto = Producto(nombre, precio, descripcion, stock, imagen, disponible, categoria)
        self._productos.append(producto)
        return producto

    def editar(self, id_producto: int, nombre: str, precio: float, descripcion: str,
               stock: int, imagen: str, disponible: bool, categoria) -> None:
        producto = self.buscar(id_producto)
        producto.nombre = nombre
        producto.precio = precio
        producto.descripcion = descripcion
        producto.stock = stock
        producto.imagen = imagen
        producto.disponible = disponible
        producto.categoria = categoria

    def eliminar(self, id_producto: int) -> None:
        self.buscar(id_producto).eliminado = True

class UsuarioServicio:
    def __init__(self) -> None:
        self._usuarios: list[Usuario] = []

    def listar(self) -> list[Usuario]:
        return [u for u in self._usuarios if not u.eliminado]

    def buscar(self, id_usuario: int) -> Usuario:
        for usuario in self._usuarios:
            if usuario.id == id_usuario and not usuario.eliminado:
                return usuario
        raise EntidadNoEncontradaError("Usuario inexistente")

    def crear(self, nombre: str, apellido: str, mail: str, celular: str,
              contraseña: str, rol: Rol) -> Usuario:
        if any(u.mail == mail.strip().lower() for u in self._usuarios):
            raise DuplicadoError("El mail ya esta registrado")
        usuario = Usuario(nombre, apellido, mail, celular, contraseña, rol)
        self._usuarios.append(usuario)
        return usuario

    def autenticar(self, mail: str, contraseña: str) -> Usuario:
        for usuario in self._usuarios:
            if (usuario.mail == mail.strip().lower() and not usuario.eliminado
                    and usuario.verificar_contraseña(contraseña)):
                return usuario
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")

    def editar(self, id_usuario: int, nombre: str, apellido: str, mail: str,
               celular: str, contraseña: str = "") -> None:
        usuario = self.buscar(id_usuario)
        if any(u.id != id_usuario and u.mail == mail.strip().lower() and not u.eliminado
               for u in self._usuarios):
            raise DuplicadoError("El mail ya esta registrado")
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.mail = mail
        usuario.celular = celular
        if contraseña:
            usuario.cambiar_contraseña(contraseña)

    def eliminar(self, id_usuario: int, sesion: Usuario) -> None:
        usuario = self.buscar(id_usuario)
        if usuario == sesion:
            raise ValueError("No puede eliminarse a si mismo")
        usuario.eliminado = True

class PedidoServicio:
    def __init__(self) -> None:
        self._pedidos: list[Pedido] = []

    def listar(self) -> list[Pedido]:
        return [p for p in self._pedidos if not p.eliminado]

    def listar_usuario(self, usuario) -> list[Pedido]:
        return [p for p in self.listar() if p.usuario == usuario]

    def buscar(self, id_pedido: int) -> Pedido:
        for pedido in self._pedidos:
            if pedido.id == id_pedido and not pedido.eliminado:
                return pedido
        raise EntidadNoEncontradaError("Pedido inexistente")

    def crear(self, usuario, forma_pago, items: list) -> Pedido:
        pedido = Pedido(usuario, forma_pago)
        for producto, cantidad in items:
            pedido.agregar_detalle(cantidad, producto)
        for detalle in pedido.detalles:
            detalle.producto.stock -= detalle.cantidad
        pedido.calcular_total()
        self._pedidos.append(pedido)
        return pedido

    def cambiar_estado(self, id_pedido: int, nuevo_estado: Estado) -> None:
        pedido = self.buscar(id_pedido)
        estado_anterior = pedido.estado
        pedido.estado = nuevo_estado
        if nuevo_estado == Estado.CANCELADO and estado_anterior != Estado.CANCELADO:
            for detalle in pedido.detalles:
                detalle.producto.stock += detalle.cantidad

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.buscar(id_pedido)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            for detalle in pedido.detalles:
                detalle.producto.stock += detalle.cantidad
        pedido.eliminado = True
        for detalle in pedido.detalles:
            detalle.eliminado = True