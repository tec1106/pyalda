from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Yay!"

if __name__ == '__main__':
    app.run(
        port=80,
        debug=True,
    )