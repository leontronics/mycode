#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify, redirect, url_for
from extensions import socketio
from game.game import Game

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
socketio.init_app(app)

game = Game()
game.state.game_interface = 'web'

@app.route('/')
def index():
    socketio.emit('game_message', {'message': 'Welcome to the game!'})
    game.show_instructions()
    instructions = "<br>".join(game.get_messages())
    game.clear_messages()
    return render_template('index.html', instructions=instructions)

@app.route('/status', methods=['GET'])
def game_status():
    game.show_status()
    status = "<br>".join(game.get_messages())
    game.clear_messages()
    return jsonify(status=status)

@app.route('/command', methods=['POST'])
def execute_command():
    data = request.json
    command = data['command'].split()
    game.command_processor.process(command)
    messages = game.get_messages()
    game_over = game.check_game_over()  
    game.clear_messages()

    for message in messages:
        socketio.emit('game_message', {'message': message})

    return jsonify(game_over=game.state.game_over)


@app.route('/messages', methods=['GET'])
def get_messages():
    messages = game.get_messages()
    game.clear_messages()
    return jsonify(messages=messages)

@app.route('/restart', methods=['GET'])
def restart_game():
    global game  
    game = Game()
    game.state.game_interface = 'web'
    return redirect(url_for('index'))


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=3000, debug=True)
