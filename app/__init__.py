from flask import Flask, jsonify

def create_app(config_name='development'):
    app = Flask(__name__)
    
    from .config import config_map
    app.config.from_object(config_map[config_name])
    
    # INIT
    @app.route('/')
    def health_check():
        return jsonify({'status': 'healthy'})
    

    # BLUEPRINTS
    # line webhook
    from .blueprints import line_webhook_bp
    app.register_blueprint(line_webhook_bp, url_prefix='/webhook')

    # whatsapp webhook (later)
    # 


    # SERVICES
    from .services import line_service, room_service
    line_service.initialize(app)
    room_service.initialize(app)
    
    return app
