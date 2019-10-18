from __future__ import print_function
from flask import request,render_template, Flask, send_from_directory, jsonify, Response, redirect
from flask_cors import CORS, cross_origin
import os
from back_end.utils.random_generator import 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'front_end')
print(STATIC_FOLDER)

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('login/html/index.html')
    # return app.send_static_file('test/test.html')

@app.route('/main', methods=["GET"])
def show_main():
    return redirect('/main_index', code=302)

@app.route('/main_index')
def drive():
    return app.send_static_file('blog/index.html')

@app.route('/<path:path>')
def serve_page(path):
    return send_from_directory(path)

@app.route('/login', methods=["GET"])
def login():
    data = request.values
    user_id = data.get("email")
    print(dict(data))
    # return jsonify({"message" : "Hello {}".format(user_id)})
    # return app.send_static_file("blog/index.html")
    return redirect("/main", code=302)

@app.route('/save_images', methods=["POST"])
def save_images():
    data = request.files
    data["files[0]"].save(os.path.join(STATIC_FOLDER, 'static', 'kitty.jpg'))
    print('aaaaaaaaaa : ',dict(data))
    
    return jsonify({"success" : True, "data" : dict(Response({"Hello" : "Lam"}).headers)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)



