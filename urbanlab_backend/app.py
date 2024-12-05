from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)  # Enable CORS for cross-origin requests

    # Configure app
    app.config['DATABASE_CONFIG'] = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',  # Replace with your MySQL password
        'database': 'urbanlab_db'    # Your database name
    }
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key

    # Initialize JWT
    jwt = JWTManager(app)

    # Test route
    @app.route('/')
    def home():
        return jsonify({'message': 'Welcome to the Urban Lab API'})

    # Register blueprints
    register_blueprints(app)

    return app


def register_blueprints(app):
    """
    Register all route blueprints.
    """
    from routes.students import students_bp
    from routes.contacts import contacts_bp
    from routes.events import events_bp
    from routes.interactions import interactions_bp
    from routes.grants import grants_bp
    from routes.auth import auth_bp
    from routes.roles import roles_bp

    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(contacts_bp, url_prefix='/contacts')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(interactions_bp, url_prefix='/interactions')
    app.register_blueprint(grants_bp, url_prefix='/grants')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(roles_bp, url_prefix='/roles')


if __name__ == '__main__':
    # Run the app
    app = create_app()
    app.run(debug=True)
