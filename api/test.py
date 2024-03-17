from flask import Flask

app = Flask(__name__)

def get_from_model(date: str) -> str:
    return date

@app.route('/<date>')
def hello(date: str):
    return f'Hello, {get_from_model(date)}!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
