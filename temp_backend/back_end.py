from __future__ import print_function
from flask import request,render_template, Flask, send_from_directory, jsonify, Response
from flask_cors import CORS, cross_origin
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'front-end')
print(STATIC_FOLDER)

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('login/html/index.html')
    # return app.send_static_file('test/test.html')

@app.route('/main')
def show_main():
    data = request.get_json()
    if data['email'] == "lamnn@athena.studio" and data['pass'] == '1':
        return app.send_static_file('blog/index.html')
    else:
        return Response("VALIDATE ERROR, INCORRECT PASSWORD OR EMAIL")

@app.route('/<path:path>')
def serve_page(path):
    return send_from_directory(path)

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    user_id = data.get("email")
    print(dict(data))
    return jsonify({"message" : "Hello {}".format(user_id)})

@app.route('/save_images', methods=["POST"])
def save_images():
    data = request.files
    data["files[0]"].save(os.path.join(STATIC_FOLDER, 'static', 'kitty.jpg'))
    print('aaaaaaaaaa : ',dict(data))
    
    return jsonify({"success" : True, "data" : dict(Response({"Hello" : "Lam"}).headers)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)



