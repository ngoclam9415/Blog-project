from __future__ import print_function
from flask import request,render_template, Flask, send_from_directory, jsonify, Response, redirect
import os
import time
from utils.random_generator import generate_random_hexcode
from database import BlogDatabase
from datetime import date
import json


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'back_end', 'static')
hex_code = generate_random_hexcode()
app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/static')
# app = Flask(__name__)
db = BlogDatabase()

@app.route('/')
def index():
    return render_template('blog/index.html')

@app.route('/secret_ingredient')
def login_page():
    return render_template('login/html/index.html')

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
        
@app.route('/uploadpost', methods=["POST"]) #{postTitle,email,thumbnail_IMG_URL,slug,postContent,ispublish}
def uploadpost():
    data= request.get_json()
    result = db.uploadpost(data.get("postTitle"),data.get("email"),data.get("thumbnail_IMG_URL"),data.get('slug'),data.get("postContent"),data.get("ispublish"))
    print(data)
    return jsonify({"success": True})

@app.route('/save_images', methods=["POST"])
def save_images():
    images = request.files.getlist("images")
    hex_code = request.form.get("hex_code")
    return_paths = []
    for image in images:
        print(image.filename)
        relative_path = os.path.join('static', '{}.jpg'.format(int(round(time.time() * 1000))))
        path = os.path.join(STATIC_FOLDER, relative_path)
        image.save(path)
        return_paths.append(relative_path)

    print('aaaaaaaaaa : ',images)
    
    return jsonify({'baseurl' : 'http://localhost:5000', "messages" : "success", "error" : 0, "paths": return_paths})

@app.route('/blog/<slug>')
def show_post(slug):
    print(slug)
    if ".html" not in slug:
        data = db.findpost(slug)
        comments = db.getcommentofpost(slug, 0, time.time(), 0)
        comments = json.loads(comments)
        for comment in comments:
            print(comment)
            print(type(comment))
            comment["commentDate"] = date.fromtimestamp(comment["commentDate"]).strftime("%B %d, %Y AT %I:%M%p")
            # print(comm)
        return render_template("blog/blog-slug.html", text_title=data["postTitle"], content=data['postContent'], cover_image=data['thumbnail_IMG_URL'], comments_len=len(comments), comments=comments)
    else:
        return render_template("blog/contact.html")

@app.route('/get_latest_posts', methods=["POST"])
def get_some_posts():
    cursors = db.findlimit_post(0, time.time(), 20)
    print(cursors)
    return jsonify(cursors)

@app.route('/editor')
def show_editor():
    return render_template("blog/editor.html")

@app.route('/uploadcomment', methods=["POST"]) #{slug,commenterName,commenterEmail,CommentText}
def uploadcomment():
    data= request.get_json()
    result = db.insert_comment(data.get("slug"),data.get("commenterName"),data.get("commenterEmail"),data.get('CommentText'))
    return jsonify({"success": True})

@app.route('/getlimitcomment', methods=["POST"]) #{postid,timestart, endtime, commentnumber}
def getlimitcomment():
    data= request.get_json()
    posts = db.getcommentofpost(data.get("slug"),data.get("starttime"),data.get("endtime"),data.get("commentnumber"))
    print(posts)
    return jsonify(posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
