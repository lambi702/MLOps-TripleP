from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def upload_file():
    to_return = '''
    <html>
        <body>
            <form action = "/uploader" method = "POST" 
                enctype = "multipart/form-data">
                <input type = "file" name = "file" />
                <input type = "submit"/>
            </form>         
        </body>
    </html>
    '''
    return to_return

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_post():
    if request.method == 'POST':
        f = request.files['file']
        data = json.load(f)
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')