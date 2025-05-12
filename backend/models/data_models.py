from dataclasses import dataclass

@dataclass
class PredictionInput:
    empleados: int
    dispositivos: int
    hora: int
    dia: int
    temperatura: float
