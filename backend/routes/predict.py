from flask import Blueprint, request, jsonify
from backend.models.data_models import PredictionInput
from backend.services.octave_runner import run_poli_lagrange
from pydantic import ValidationError

predict_bp= Blueprint("predict", __name__)

@predict_bp.route('/predict', methods=['POST'])

def predict():
    try:
        data=request.get_json()
        
         # Validar que todos los datos estén presentes
        try:
            prediction_input= PredictionInput.model_validate(data)
        except ValidationError as ve:
            return jsonify({"error": "Datos inválidos", "detalles": ve.errors()}), 422
        
        # Ejecutar el modelo Octave
        resultado = run_poli_lagrange(
            empleados=prediction_input.empleados,
            computadora=prediction_input.computadora,
            monitor=prediction_input.monitor,
            impresora=prediction_input.impresora,
            aire_acondicionado=prediction_input.aire_acondicionado,
            iluminacion=prediction_input.iluminacion,
            router=prediction_input.router,
            cafetera=prediction_input.cafetera,
            proyector=prediction_input.proyector,
            modo=prediction_input.modo,
            hora=prediction_input.hora,
            temperatura=prediction_input.temperatura,
            llueve=prediction_input.llueve,
            prob_lluvia=prediction_input.prob_lluvia,
            ciudad=prediction_input.ciudad,
            precio_kw=prediction_input.precio_kw,
            dia=prediction_input.dia
        )
        
        return jsonify({"prediccion": resultado}), 200
    
    except Exception as e:
         return jsonify({"error": "Ocurrió un error", "detalle": str(e)}), 500