#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
from game.game import Game

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

game = Game()

@app.route('/')
def index():
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
    return jsonify(messages=messages, game_over=game.state.game_over)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
