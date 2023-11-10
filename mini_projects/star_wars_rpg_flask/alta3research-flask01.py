#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
from game.game import Game

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

game = Game()

@app.route('/')
def index():
    game.show_instructions()
    game.show_status()
    all_messages = game.get_messages()
    full_message = "<br>".join(all_messages)
    game.clear_messages()
    return render_template('index.html', full_message=full_message)


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
