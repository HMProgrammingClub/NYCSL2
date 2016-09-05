from flask import Flask, request
import json
import random

games = {}

app = Flask(__name__)

@app.route('/start')
def start():
    key = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    games[key] = Map(21, 21, random.randint(0, 4294967295))
    return key

@app.route('/move/<str:key, int:move>')
def move(key, move):
    result = games[key].make_move(move)
    if result != 0:
        del games[key]
        return result
    games[key].update_visibility()
    games[key].delay()
    send_string(games[key].serialize()) # Josh, I'm assuming that 'send_string' exists, because I have no idea how you want it to be written.

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7500,debug=True)
