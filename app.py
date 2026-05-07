from flask import Flask, render_template, request, Response

app = Flask(__name__)

# Basic Security: Define authorized credentials
USER_DATA = {
    "admin": "SecurePass123"
}

@app.route('/')
def index():
    # Check for basic authentication headers
    auth = request.authorization
    if not auth or not (auth.username in USER_DATA and USER_DATA[auth.username] == auth.password):
        return Response(
            'Unauthorized Access: Please login.', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        )
    return render_template('camera.html')

if __name__ == '__main__':
    # Binding to 0.0.0.0 allows network-wide access as per Phase 5 [cite: 373, 425]
    app.run(host='0.0.0.0', port=5000, debug=False)