from flask import Blueprint, request, jsonify
from backend.models.data_models import PredictionInput
from backend.services.octave_runner import run_poli_lagrange, verify_octave_installation
from pydantic import ValidationError
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear el blueprint para las rutas de predicción
predict_bp = Blueprint("predict", __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para realizar predicciones de consumo energético.
    """
    try:
        # Obtener los datos enviados en la solicitud
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400
        
        # Validar los datos usando Pydantic
        try:
            prediction_input = PredictionInput.model_validate(data)
        except ValidationError as ve:
            return jsonify({
                "error": "Datos inválidos", 
                "detalles": ve.errors()
            }), 422
            
        # Verificar que Octave esté instalado antes de ejecutar
        octave_available, octave_cmd = verify_octave_installation()
        if not octave_available:
            return jsonify({
                "error": "Octave no está disponible",
                "detalle": "Asegúrate de que Octave esté instalado y disponible en el PATH"
            }), 500
        
        logger.info(f"Ejecutando predicción con Octave usando comando: {octave_cmd}")
        
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
            ciudad=prediction_input.ciudad,
            precio_kw=prediction_input.precio_kw,
            dia=prediction_input.dia,
            hora=prediction_input.hora,
            temperatura=prediction_input.temperatura,
            llueve=prediction_input.llueve,
            prob_lluvia=prediction_input.prob_lluvia
        )
        
        logger.info("Predicción ejecutada exitosamente")
        
        # Devolver los resultados al frontend
        return jsonify({
            "success": True,
            "prediccion": resultado
        }), 200
    
    except ValidationError as ve:
        logger.error(f"Error de validación: {ve}")
        return jsonify({
            "error": "Datos de entrada inválidos",
            "detalles": ve.errors()
        }), 422
        
    except RuntimeError as re:
        logger.error(f"Error de runtime: {re}")
        return jsonify({
            "error": "Error en la ejecución",
            "detalle": str(re)
        }), 500
    
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return jsonify({
            "error": "Ocurrió un error inesperado",
            "detalle": str(e)
        }), 500
        

@predict_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar el estado del servicio.
    """
    octave_available, octave_cmd = verify_octave_installation()
    
    return jsonify({
        "status": "ok",
        "octave_available": octave_available,
        "octave_command": octave_cmd
    }), 200