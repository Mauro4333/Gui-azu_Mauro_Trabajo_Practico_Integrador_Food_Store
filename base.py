from abc import ABC
from datetime import datetime


class Base(ABC):
    _ultimos_ids: dict = {}

    def __init__(self) -> None:
        clase = type(self)
        Base._ultimos_ids[clase] = Base._ultimos_ids.get(clase, 0) + 1
        self.__id: int = Base._ultimos_ids[clase]
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise ValueError("Eliminado debe ser verdadero o falso")
        self.__eliminado = valor

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    def __eq__(self, otro: object) -> bool:
        return type(self) is type(otro) and self.id == otro.id

    def __hash__(self) -> int:
        return hash((type(self), self.id))