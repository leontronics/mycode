#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
from game.game import Game

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

game = Game()

@app.route('/')
def index():
    game_instructions = game.show_instructions()
    return render_template('index.html', instructions=game_instructions)


@app.route('/command', methods=['POST'])
def execute_command():
    data = request.json
    command = data['command'].split() 
    game.command_processor.process(command)
    messages = game.get_messages()
    game.clear_messages()
    return jsonify(messages=messages)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
