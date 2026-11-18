class FoodStoreError(Exception):
    """Error base del sistema."""

class EntidadNoEncontradaError(FoodStoreError):
    pass

class DatoInvalidoError(FoodStoreError):
    pass

class PrecioInvalidoError(DatoInvalidoError):
    pass

class StockInsuficienteError(FoodStoreError):
    pass

class DuplicadoError(FoodStoreError):
    pass

class OperacionNoPermitidaError(FoodStoreError):
    pass

class CredencialesInvalidasError(FoodStoreError):
    pass