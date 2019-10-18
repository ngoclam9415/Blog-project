from __future__ import print_function
from flask import request,render_template, Flask, send_from_directory, jsonify, Response, redirect, url_for
from flask_cors import CORS, cross_origin
import os
from database import BlogDatabase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'front_end')
print(STATIC_FOLDER)

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')
db = BlogDatabase()

@app.route('/')
def index():
        return app.send_static_file('blog/about.html')
    
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
    data = request.get_json()
    data = {'email' : asas, 'pass' : 1}
    user_id = data.get("email")
    print(dict(data))
    return jsonify({"message" : "Hello {}".format(user_id)})
    return app.send_static_file("blog/index.html")


@app.route('/save_images', methods=["POST"])
def save_images():
    data = request.files
    data["files[0]"].save(os.path.join(STATIC_FOLDER, 'static', 'kitty.jpg'))
    print('aaaaaaaaaa : ',dict(data))
    return jsonify({"success" : True, "data" : dict(Response({"Hello" : "Lam"}).headers)})

@app.route('/goto')
def gotoso():
    return redirect(url_for('main'))

#PostAPI
@app.route('/uploadpost', methods=["POST"]) #{postTitle,email,thumbnail_IMG_URL,slug,postContent,ispublish}
def uploadpost():
    data= request.get_json()
    result = db.insert_post(data.get("postTitle"),data.get("email"),data.get("thumbnail_IMG_URL"),data.get('slug'),data.get("postContent"),data.get("ispublish"))
    return jsonify({"success": True})

@app.route('/updatepost', methods=["POST"]) #{postid,postTitle,email,thumbnail_IMG_URL,slug,postContent}
def updatepost():
    data= request.get_json()
    db.update_post(data.get("postid"),data.get("postTitle"),data.get("email"),data.get("thumbnail_IMG_URL"),data.get('slug'),data.get("postContent"))
    return jsonify({"success": True})


@app.route('/delepost', methods=["POST"]) #{postid}
def delepost():
    data= request.get_json()
    result = db.delete_post(data.get("postid"))
    return jsonify({"success": True})

@app.route('/unpublishedpost', methods=["POST"]) #{postid}
def unpublishedpost():
    data= request.get_json()
    result = db.unpublish_post(data.get("postid"))
    return jsonify({"success": True})

@app.route('/publishpost', methods=["POST"]) #{postid}
def publishpost():
    data= request.get_json()
    result = db.publish_post(data.get("postid"))
    return jsonify({"success": True})

@app.route('/getallpost', methods=["GET"]) #{}
def getallpost():
    posts = db.findall_post()
    return posts

@app.route('/getlimitpost', methods=["POST"]) #{timestart, endtime, postnumber}
def getlimitpost():
    data= request.get_json()
    posts = db.findlimit_post(data.get("timestart"),data.get("endtime"),data.get("postnumber"))
    return posts

#commentAPI
@app.route('/getlimitcomment', methods=["POST"]) #{postid,timestart, endtime, commentnumber}
def getlimitcomment():
    data= request.get_json()
    posts = db.getcommentofpost(data.get("postid"),data.get("timestart"),data.get("endtime"),data.get("commentnumber"))
    return posts

@app.route('/uploadcomment', methods=["POST"]) #{postid,commenterName,commenterEmail,CommentText}
def uploadcomment():
    data= request.get_json()
    result = db.insert_comment(data.get("postid"),data.get("commenterName"),data.get("commenterEmail"),data.get('CommentText'))
    return jsonify({"success": True})

@app.route('/deletecomment', methods=["POST"]) #{commentid}
def deletecomment():
    data= request.get_json()
    result = db.delete_comment(data.get("commentid"))
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)



