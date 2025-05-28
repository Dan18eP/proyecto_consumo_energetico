from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal

class PredictionInput(BaseModel):
    empleados: int = Field(..., gt=0, description="Número de empleados")
    
    # Dispositivos por separado
    computadora: int = Field(..., ge=0, description="Cantidad de computadoras")
    monitor: int = Field(..., ge=0, description="Cantidad de monitores")
    impresora: int = Field(..., ge=0, description="Cantidad de impresoras")
    aire_acondicionado: int = Field(..., ge=0, description="Cantidad de aires acondicionados")
    iluminacion: int = Field(..., ge=0, description="Cantidad de luces")
    router: int = Field(..., ge=0, description="Cantidad de routers")
    cafetera: int = Field(..., ge=0, description="Cantidad de cafeteras")
    proyector: int = Field(..., ge=0, description="Cantidad de proyectores")

    modo: Literal["hora", "dia"] = Field(..., description="Cálculo por hora o todo el día")
    ciudad: str = Field(..., description="Ciudad seleccionada")
    precio_kw: float = Field(..., gt=0, description="Precio del kW en la ciudad")
    dia: Literal["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"] = Field(
        ..., description="Día de la semana")
    # Solo si el modo es 'hora'
    hora: Optional[int] = Field(None, ge=7, le=19, description="Hora del día (7 a 19)")
    temperatura: Optional[float] = Field(None, description="Temperatura en grados Celsius")
    llueve: Optional[bool] = Field(None, description="Indica si está lloviendo")

    # Solo si el modo es 'dia_entero'
    prob_lluvia: Optional[float] = Field(None, ge=0, le=1, description="Probabilidad de lluvia (0 a 1)")
    

    @model_validator(mode="before")
    def validar_datos_dependientes(cls, data):
        """
        Valida que los datos dependientes sean correctos según el modo seleccionado.
        """
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
