from flask import Blueprint, request, jsonify
from backend.models.data_models import PredictionInput
from backend.services.octave_runner import run_poli_lagrange

predict_bp= Blueprint("predict", __name__)

@predict_bp.route('/predict', methods=['POST'])

def predict():
    try:
        data=request.json
         # Validar que todos los datos estén presentes
        if not all(key in data for key in ["empleados", "dispositivos", "hora", "dia", "temperatura"]):
            return jsonify({"error": "Faltan datos en la solicitud"}), 400

        prediction_input = PredictionInput(
            empleados=data["empleados"],
            dispositivos=data["dispositivos"],
            hora=data["hora"],
            dia=data["dia"],
            temperatura=data["temperatura"]
        )
        
        resultado= run_poli_lagrange(
            empleados=prediction_input.empleados,
            dispositivos=prediction_input.dispositivos,
            hora=prediction_input.hora,
            dia=prediction_input.dia,
            temperatura=prediction_input.temperatura
        )
        
        return jsonify({"prediccion": resultado}), 200
    except Exception as e:
         return jsonify({"error": "Ocurrió un error", "detalle": str(e)}), 500