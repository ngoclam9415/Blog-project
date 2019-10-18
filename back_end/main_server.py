from __future__ import print_function
from flask import request,render_template, Flask, send_from_directory, jsonify, Response, redirect
import os
from back_end.utils.random_generator import generate_random_hexcode

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'front_end')
hex_code = generate_random_hexcode()
app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('blog/index.html')

@app.route('/secret_ingredient')
def login_page():
    return app.send_static_file('login/html/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect('/', code=302)
    elif request.method == 'POST':
        data = request.get_json()
        print(data)
        if data["email"] == "lamnn@athena.studio" and data["pass"] == "1":
            return jsonify({"hex_code" : hex_code, "message" : "Hello superuser"})
        else:
            return jsonify({"hex_code" : "0", "message" : "Hello"})
        
@app.route('/save_images', methods=["POST"])
def save_images():
    data = request.files
    data["files[0]"].save(os.path.join(STATIC_FOLDER, 'static', 'kitty.jpg'))
    print('aaaaaaaaaa : ',dict(data))
    
    return jsonify({'baseurl' : 'http://localhost:5000', "messages" : "success", "error" : 0, "files": ['static/kitty.jpg'], 'isImages' : [True]})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
