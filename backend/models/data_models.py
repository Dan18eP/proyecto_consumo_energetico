from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class PredictionInput(BaseModel):
    empleados: int = Field(..., gt=0, description="Número de empleados")
    
    # Dispositivos por separado
    computadora: int = Field(..., ge=0)
    monitor: int = Field(..., ge=0)
    impresora: int = Field(..., ge=0)
    aire_acondicionado: int = Field(..., ge=0)
    iluminacion: int = Field(..., ge=0)
    router: int = Field(..., ge=0)
    cafetera: int = Field(..., ge=0)
    proyector: int = Field(..., ge=0)

    modo: Literal["hora", "dia_entero"] = Field(..., description="Cálculo por hora o todo el día")

    # Solo si el modo es 'hora'
    hora: Optional[int] = Field(None, ge=7, le=19)
    temperatura: Optional[float] = None
    llueve: Optional[bool] = None

    # Solo si el modo es 'dia'
    prob_lluvia: Optional[float] = Field(None, ge=0, le=1)

    ciudad: str = Field(..., description="Ciudad seleccionada")
    precio_kw: float = Field(..., gt=0)
    dia: str = Field(...)

    @model_validator(mode="before")
    def validar_datos_dependientes(cls, data):
        modo = data.get("modo")

        if modo == "hora":
            if data.get("hora") is None:
                raise ValueError("Debes indicar la hora si el cálculo es por hora.")
            if data.get("temperatura") is None:
                raise ValueError("Debes indicar la temperatura si el cálculo es por hora.")
            if data.get("llueve") is None:
                raise ValueError("Debes indicar si está lloviendo si el cálculo es por hora.")
        elif modo == "dia_entero":
            if data.get("prob_lluvia") is None:
                raise ValueError("Debes indicar la probabilidad de lluvia si el cálculo es por día.")

        return data
