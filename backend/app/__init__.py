from flask import Flask

def create_app():
    app = Flask(__name__)

    # Registrar las rutas
    from backend.routes.predict import predict_bp
    app.register_blueprint(predict_bp, url_prefix="/api")
    
    return app