from flask import Flask, request
import json
import random

app = Flask(__name__)

@app.route('/start')
def start():
    key = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    return key

@app.route('/move/<int:move>')
def move(move):
    return str(move)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7500,debug=True)
