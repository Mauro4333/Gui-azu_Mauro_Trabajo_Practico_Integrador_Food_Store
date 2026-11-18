from base import Base
from enums import Rol


class Usuario(Base):
    def __init__(self, nombre: str, apellido: str, mail: str,
                 celular: str, contraseña: str, rol: Rol) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.__contraseña: str = contraseña
        self.rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El apellido no puede estar vacío")
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise ValueError("Ingrese un mail válido")
        self.__mail = valor.strip().lower()

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        if not str(valor).strip():
            raise ValueError("El celular no puede estar vacío")
        self.__celular = str(valor).strip()

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise ValueError("Rol inválido")
        self.__rol = valor

    def verificar_contraseña(self, contraseña: str) -> bool:
        return self.__contraseña == contraseña

    def cambiar_contraseña(self, contraseña: str) -> None:
        if not contraseña:
            raise ValueError("La contraseña no puede estar vacía")
        self.__contraseña = contraseña

    def __str__(self) -> str:
        return f"{self.id} - {self.nombre} {self.apellido} | {self.mail} | {self.rol.value}"
