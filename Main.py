import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from enums import *
from exepciones import FoodStoreError


class FoodStoreApp(tk.Tk):
    def __init__(self, categoria_servicio, producto_servicio, usuario_servicio, pedido_servicio):
        super().__init__()
        self.title("Food Store - Gestion de pedidos")
        self.geometry("950x620")
        self.minsize(800, 520)
        self.configure(bg="#f2f2f2")
        self.categorias = categoria_servicio
        self.productos = producto_servicio
        self.usuarios = usuario_servicio
        self.pedidos = pedido_servicio
        self.sesion = None
        self.contenedor = ttk.Frame(self, padding=18)
        self.contenedor.pack(fill="both", expand=True)
        self.mostrar_login()

    def limpiar(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def titulo(self, texto):
        ttk.Label(self.contenedor, text=texto, font=("Arial", 19, "bold")).pack(pady=(0, 15))

    def mostrar_login(self):
        self.limpiar()
        marco = ttk.Frame(self.contenedor, padding=35)
        marco.place(relx=0.5, rely=0.45, anchor="center")
        ttk.Label(marco, text="FOOD STORE", font=("Arial", 25, "bold")).grid(row=0, column=0, columnspan=2, pady=15)
        ttk.Label(marco, text="Mail").grid(row=1, column=0, sticky="w", pady=6)
        mail = ttk.Entry(marco, width=32)
        mail.grid(row=1, column=1, pady=6)
        ttk.Label(marco, text="Contraseña").grid(row=2, column=0, sticky="w", pady=6)
        clave = ttk.Entry(marco, width=32, show="*")
        clave.grid(row=2, column=1, pady=6)
        intentos = {"cantidad": 0}

        def ingresar():
            try:
                self.sesion = self.usuarios.autenticar(mail.get(), clave.get())
                self.mostrar_menu()
            except FoodStoreError:
                intentos["cantidad"] += 1
                messagebox.showerror("Acceso", "Mail o contraseña incorrectos")
                clave.delete(0, tk.END)
                if intentos["cantidad"] >= 3:
                    messagebox.showerror("Acceso", "Se agotaron los 3 intentos")
                    self.destroy()

        ttk.Button(marco, text="Ingresar", command=ingresar).grid(row=3, column=0, columnspan=2, pady=15)
        ttk.Label(marco, text="Administrador inicial: admin@foodstore.com / admin123",
                  foreground="gray").grid(row=4, column=0, columnspan=2)

    def mostrar_menu(self):
        self.limpiar()
        rol = "ADMINISTRADOR" if self.sesion.rol == Rol.ADMIN else "CLIENTE"
        self.titulo(f"FOOD STORE - {rol}: {self.sesion.nombre} {self.sesion.apellido}")
        botones = ttk.Frame(self.contenedor)
        botones.pack(pady=10)
        if self.sesion.rol == Rol.ADMIN:
            opciones = [
                ("Categorias", self.ventana_categorias),
                ("Productos", self.ventana_productos),
                ("Usuarios", self.ventana_usuarios),
                ("Pedidos", self.ventana_pedidos),
            ]
        else:
            opciones = [
                ("Ver categorias", self.ventana_categorias),
                ("Ver productos", self.ventana_productos),
                ("Mis pedidos", self.ventana_pedidos),
                ("Mis datos", self.mis_datos),
            ]
        for i, (texto, accion) in enumerate(opciones):
            ttk.Button(botones, text=texto, width=22, command=accion).grid(row=i // 2, column=i % 2, padx=10, pady=10, ipady=12)
        ttk.Button(self.contenedor, text="Cerrar sesion", command=self.mostrar_login).pack(side="left", pady=20)
        ttk.Button(self.contenedor, text="Salir", command=self.destroy).pack(side="right", pady=20)

    def tabla(self, columnas, filas):
        ventana = tk.Toplevel(self)
        ventana.geometry("850x430")
        ventana.title("Listado")
        marco = ttk.Frame(ventana, padding=12)
        marco.pack(fill="both", expand=True)
        tree = ttk.Treeview(marco, columns=columnas, show="headings")
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=max(100, int(760 / len(columnas))))
        for fila in filas:
            tree.insert("", tk.END, values=fila)
        tree.pack(fill="both", expand=True)
        return ventana

    def ventana_categorias(self):
        admin = self.sesion.rol == Rol.ADMIN
        filas = [(c.id, c.nombre, c.descripcion) for c in self.categorias.listar()]
        ventana = self.tabla(("ID", "Nombre", "Descripcion"), filas)
        if admin:
            barra = ttk.Frame(ventana, padding=10)
            barra.pack()
            ttk.Button(barra, text="Crear", command=self.crear_categoria).pack(side="left", padx=5)
            ttk.Button(barra, text="Editar por ID", command=self.editar_categoria).pack(side="left", padx=5)
            ttk.Button(barra, text="Eliminar por ID", command=self.eliminar_categoria).pack(side="left", padx=5)

    def crear_categoria(self):
        nombre = simpledialog.askstring("Categoria", "Nombre:")
        if nombre is None: return
        descripcion = simpledialog.askstring("Categoria", "Descripcion:")
        if descripcion is None: return
        try:
            categoria = self.categorias.crear(nombre, descripcion)
            messagebox.showinfo("Correcto", f"Categoria creada. ID: {categoria.id}")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def editar_categoria(self):
        try:
            id_cat = simpledialog.askinteger("Editar", "ID de categoria:")
            if id_cat is None: return
            categoria = self.categorias.buscar(id_cat)
            nombre = simpledialog.askstring("Editar", "Nombre:", initialvalue=categoria.nombre)
            descripcion = simpledialog.askstring("Editar", "Descripcion:", initialvalue=categoria.descripcion)
            if nombre is not None and descripcion is not None:
                self.categorias.editar(id_cat, nombre, descripcion)
                messagebox.showinfo("Correcto", "Categoria modificada")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def eliminar_categoria(self):
        try:
            id_cat = simpledialog.askinteger("Eliminar", "ID de categoria:")
            if id_cat is None: return
            if messagebox.askyesno("Confirmar", "¿Eliminar categoria?"):
                self.categorias.eliminar(id_cat, self.productos.listar())
                messagebox.showinfo("Correcto", "Categoria eliminada")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def ventana_productos(self):
        admin = self.sesion.rol == Rol.ADMIN
        productos = self.productos.listar(solo_disponibles=not admin)
        filas = [(p.id, p.nombre, f"${p.precio:.2f}", p.stock, p.categoria.nombre,
                  "Sí" if p.disponible else "No") for p in productos]
        ventana = self.tabla(("ID", "Nombre", "Precio", "Stock", "Categoria", "Disponible"), filas)
        if admin:
            ttk.Button(ventana, text="Crear producto", command=self.crear_producto).pack(pady=8)
            ttk.Button(ventana, text="Eliminar por ID", command=self.eliminar_producto).pack(pady=5)

    def crear_producto(self):
        try:
            nombre = simpledialog.askstring("Producto", "Nombre:")
            if nombre is None: return
            descripcion = simpledialog.askstring("Producto", "Descripcion:")
            if descripcion is None: return
            precio = simpledialog.askfloat("Producto", "Precio:")
            if precio is None: return
            stock = simpledialog.askinteger("Producto", "Stock:")
            if stock is None: return
            imagen = simpledialog.askstring("Producto", "Imagen (ruta o descripcion):") or ""
            disponible = messagebox.askyesno("Producto", "¿Esta disponible?")
            categorias = self.categorias.listar()
            if not categorias:
                messagebox.showwarning("Producto", "Primero debe crear una categoria")
                return
            opciones = "\n".join(f"{c.id} - {c.nombre}" for c in categorias)
            id_cat = simpledialog.askinteger("Producto", f"ID de categoria:\n{opciones}")
            if id_cat is None: return
            categoria = self.categorias.buscar(id_cat)
            producto = self.productos.crear(nombre, precio, descripcion, stock, imagen, disponible, categoria)
            messagebox.showinfo("Correcto", f"Producto creado. ID: {producto.id}")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def editar_producto(self):
        try:
            id_prod = simpledialog.askinteger("Editar", "ID de producto:")
            if id_prod is None: return
            producto = self.productos.buscar(id_prod)
            nombre = simpledialog.askstring("Editar", "Nombre:", initialvalue=producto.nombre)
            if nombre is None: return
            descripcion = simpledialog.askstring("Editar", "Descripcion:", initialvalue=producto.descripcion)
            if descripcion is None: return
            precio = simpledialog.askfloat("Editar", "Precio:", initialvalue=producto.precio)
            if precio is None: return
            stock = simpledialog.askinteger("Editar", "Stock:", initialvalue=producto.stock)
            if stock is None: return
            imagen = simpledialog.askstring("Editar", "Imagen:", initialvalue=producto.imagen)
            if imagen is None: return
            disponible = messagebox.askyesno("Editar", "¿Esta disponible?")
            categorias = self.categorias.listar()
            opciones = "\n".join(f"{c.id} - {c.nombre}" for c in categorias)
            id_cat = simpledialog.askinteger("Editar", f"ID de categoria:\n{opciones}", initialvalue=producto.categoria.id)
            if id_cat is None: return
            categoria = self.categorias.buscar(id_cat)
            self.productos.editar(id_prod, nombre, precio, descripcion, stock, imagen, disponible, categoria)
            messagebox.showinfo("Correcto", "Producto modificado")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def eliminar_producto(self):
        try:
            id_prod = simpledialog.askinteger("Eliminar", "ID de producto:")
            if id_prod is None: return
            if messagebox.askyesno("Confirmar", "¿Eliminar producto?"):
                self.productos.eliminar(id_prod)
                messagebox.showinfo("Correcto", "Producto eliminado")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def ventana_usuarios(self):
        if self.sesion.rol != Rol.ADMIN:
            return self.mis_datos()
        filas = [(u.id, u.nombre, u.apellido, u.mail, u.celular, u.rol.value)
                 for u in self.usuarios.listar()]
        ventana = self.tabla(("ID", "Nombre", "Apellido", "Mail", "Celular", "Rol"), filas)
        ttk.Button(ventana, text="Crear usuario", command=self.crear_usuario).pack(pady=8)
        ttk.Button(ventana, text="Editar por ID", command=self.editar_usuario).pack(pady=5)
        ttk.Button(ventana, text="Eliminar por ID", command=self.eliminar_usuario).pack(pady=5)

    def crear_usuario(self):
        try:
            nombre = simpledialog.askstring("Usuario", "Nombre:")
            if nombre is None: return
            apellido = simpledialog.askstring("Usuario", "Apellido:")
            if apellido is None: return
            mail = simpledialog.askstring("Usuario", "Mail:")
            if mail is None: return
            celular = simpledialog.askstring("Usuario", "Celular:")
            if celular is None: return
            clave = simpledialog.askstring("Usuario", "Contraseña:", show="*")
            if clave is None: return
            rol = Rol.ADMIN if messagebox.askyesno("Rol", "¿Es administrador? (No = cliente)") else Rol.USUARIO
            usuario = self.usuarios.crear(nombre, apellido, mail, celular, clave, rol)
            messagebox.showinfo("Correcto", f"Usuario creado. ID: {usuario.id}")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def editar_usuario(self):
        try:
            id_usr = simpledialog.askinteger("Editar", "ID de usuario:")
            if id_usr is None: return
            usuario = self.usuarios.buscar(id_usr)
            nombre = simpledialog.askstring("Editar", "Nombre:", initialvalue=usuario.nombre)
            if nombre is None: return
            apellido = simpledialog.askstring("Editar", "Apellido:", initialvalue=usuario.apellido)
            if apellido is None: return
            mail = simpledialog.askstring("Editar", "Mail:", initialvalue=usuario.mail)
            if mail is None: return
            celular = simpledialog.askstring("Editar", "Celular:", initialvalue=usuario.celular)
            if celular is None: return
            clave = simpledialog.askstring("Editar", "Nueva contraseña (vacío = conservar):", show="*")
            if clave is None: return
            self.usuarios.editar(id_usr, nombre, apellido, mail, celular, clave)
            messagebox.showinfo("Correcto", "Usuario modificado")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def eliminar_usuario(self):
        try:
            id_usr = simpledialog.askinteger("Eliminar", "ID de usuario:")
            if id_usr is None: return
            if messagebox.askyesno("Confirmar", "¿Eliminar usuario?"):
                self.usuarios.eliminar(id_usr, self.sesion)
                messagebox.showinfo("Correcto", "Usuario eliminado")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def mis_datos(self):
        u = self.sesion
        messagebox.showinfo("Mis datos", f"Nombre: {u.nombre} {u.apellido}\nMail: {u.mail}\nCelular: {u.celular}\nRol: {u.rol.value}")

    def ventana_pedidos(self):
        if self.sesion.rol == Rol.ADMIN:
            pedidos = self.pedidos.listar()
        else:
            pedidos = self.pedidos.listar_usuario(self.sesion)
        filas = [(p.id, f"{p.usuario.nombre} {p.usuario.apellido}", p.estado.value,
                  p.forma_pago.value, f"${p.total:.2f}", p.fecha) for p in pedidos]
        ventana = self.tabla(("ID", "Usuario", "Estado", "Pago", "Total", "Fecha"), filas)
        if self.sesion.rol == Rol.ADMIN:
            ttk.Button(ventana, text="Crear pedido", command=self.crear_pedido).pack(pady=8)
            ttk.Button(ventana, text="Cambiar estado", command=self.cambiar_estado_pedido).pack(pady=5)
            ttk.Button(ventana, text="Eliminar pedido", command=self.eliminar_pedido).pack(pady=5)
        else:
            ttk.Button(ventana, text="Ver detalles por ID", command=self.ver_detalles).pack(pady=8)

    def crear_pedido(self):
        try:
            usuarios = self.usuarios.listar()
            productos = self.productos.listar(solo_disponibles=True)
            if not usuarios or not productos:
                messagebox.showwarning("Pedido", "Se necesitan usuarios y productos disponibles")
                return
            lista_usuarios = "\n".join(f"{u.id} - {u.nombre} {u.apellido}" for u in usuarios)
            id_usr = simpledialog.askinteger("Pedido", f"ID de usuario:\n{lista_usuarios}")
            if id_usr is None: return
            usuario = self.usuarios.buscar(id_usr)
            forma = simpledialog.askinteger("Pedido", "Forma de pago:\n1 Tarjeta\n2 Transferencia\n3 Efectivo")
            if forma not in (1, 2, 3): return
            forma_pago = list(FormaPago)[forma - 1]
            items = []
            while True:
                lista_productos = "\n".join(f"{p.id} - {p.nombre} | Stock {p.stock} | ${p.precio:.2f}" for p in productos)
                id_prod = simpledialog.askinteger("Detalle", f"ID de producto (Cancelar para terminar):\n{lista_productos}")
                if id_prod is None:
                    break
                producto = self.productos.buscar(id_prod)
                cantidad = simpledialog.askinteger("Detalle", f"Cantidad de {producto.nombre}:")
                if cantidad is None: continue
                items.append((producto, cantidad))
                if not messagebox.askyesno("Detalle", "¿Agregar otro producto?"):
                    break
            if not items:
                return
            pedido = self.pedidos.crear(usuario, forma_pago, items)
            messagebox.showinfo("Correcto", f"Pedido {pedido.id} creado. Total: ${pedido.total:.2f}")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def cambiar_estado_pedido(self):
        try:
            id_ped = simpledialog.askinteger("Pedido", "ID de pedido:")
            if id_ped is None: return
            pedido = self.pedidos.buscar(id_ped)
            opciones = "\n".join(f"{i + 1} - {estado.value}" for i, estado in enumerate(Estado))
            numero = simpledialog.askinteger("Estado", f"Nuevo estado:\n{opciones}")
            if numero is None or numero not in range(1, 5): return
            self.pedidos.cambiar_estado(id_ped, list(Estado)[numero - 1])
            messagebox.showinfo("Correcto", "Estado actualizado")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def eliminar_pedido(self):
        try:
            id_ped = simpledialog.askinteger("Pedido", "ID de pedido:")
            if id_ped is None: return
            if messagebox.askyesno("Confirmar", "¿Eliminar pedido?"):
                self.pedidos.eliminar(id_ped)
                messagebox.showinfo("Correcto", "Pedido eliminado")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def ver_detalles(self):
        try:
            id_ped = simpledialog.askinteger("Pedido", "ID de pedido:")
            if id_ped is None: return
            pedido = self.pedidos.buscar(id_ped)
            if pedido.usuario != self.sesion:
                messagebox.showerror("Pedido", "Pedido inexistente")
                return
            texto = "\n".join(str(d) for d in pedido.detalles)
            messagebox.showinfo("Detalles del pedido", f"{texto}\n\nTotal: ${pedido.total:.2f}")
        except Exception as error:
            messagebox.showerror("Error", str(error))


from funciones import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio


def main() -> None:
    categoria_servicio = CategoriaServicio()
    producto_servicio = ProductoServicio()
    usuario_servicio = UsuarioServicio()
    pedido_servicio = PedidoServicio()

    usuario_servicio.crear(
        "Admin", "Food Store", "admin@foodstore.com",
        "2610000000", "admin123", Rol.ADMIN
    )

    categoria = categoria_servicio.crear("Comidas", "Platos y comidas")
    producto_servicio.crear(
        "Hamburguesa", 4500, "Hamburguesa completa",
        20, "", True, categoria
    )
    usuario_servicio.crear(
        "Juan", "Gómez", "juan@gmail.com",
        "2611111111", "1234", Rol.USUARIO
    )

    app = FoodStoreApp(
        categoria_servicio,
        producto_servicio,
        usuario_servicio,
        pedido_servicio
    )
    app.mainloop()


if __name__ == "__main__":
    main()