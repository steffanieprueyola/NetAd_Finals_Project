from flask import Flask
from flask_socketio import SocketIO

# Import modules
from auth.routes import auth_bp
from dashboard.routes import dashboard_bp

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-change-this'

# SocketIO setup (IMPORTANT for live logs)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Register Blueprints (connect group work)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# Optional: test route
@app.route("/ping")
def ping():
    return "Server is running"

# MAIN RUN (Railway compatible)
if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        allow_unsafe_werkzeug=True  # fixes Railway error
    )
