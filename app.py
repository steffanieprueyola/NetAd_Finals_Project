from flask import Flask
from flask_socketio import SocketIO

# Core modules
from auth.routes import auth_bp
from dashboard.routes import dashboard_bp

# Optional modules (based on your structure)
from camera.stream import camera_bp
from security.limiter import security_bp

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-change-this'

# SocketIO setup (for real-time features like logs, dashboard updates, etc.)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

# Register all blueprints (system modules)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(camera_bp)
app.register_blueprint(security_bp)

# Health check route
@app.route("/ping")
def ping():
    return "Server is running"

# Main execution
if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )
