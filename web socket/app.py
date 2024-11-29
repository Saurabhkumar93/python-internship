from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# Handle messages from the client
@socketio.on('message')
def handle_message(message):
    print(f'Received message: {message}')
    
    # Respond based on message content
    if 'details' in message.lower():
        # Respond with some detailed information
        response = 'Here are the details: [Insert specific details here]'
    else:
        # Default response
        response = 'Hello from server!'
    
    send(response, broadcast=True)  # Broadcast the response to all clients

# Main entry point to run the server
if __name__ == '__main__':
    socketio.run(app, debug=True)
