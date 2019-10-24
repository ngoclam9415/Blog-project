from __future__ import print_function
from flask import request,render_template, Flask, send_from_directory, jsonify, Response, redirect
import os
import time
from utils.random_generator import generate_random_hexcode
from database import BlogDatabase
from datetime import date
import json
import logging


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'back_end', 'static')
hex_code = generate_random_hexcode()
# app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')
app = Flask(__name__)
db = BlogDatabase()

@app.route('/')
def index():
    return render_template('blog/index.html')

data_user = None
@app.route('/secret_ingredient/',methods=['GET','POST'])
def login_page():
    if request.method == 'GET':
        return render_template("login/html/index.html",data=hex_code)
    elif request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        print(username,password)
        cursor = db.user_login(username, password)
        #print(cursor)
        global user_login
        user_login = cursor
        #print(user_login)
        if user_login == None:
            return render_template("login/html/index.html")
        else:
            return show_blog()
            #return render_template("index.html",data=cursor)
        #return render_template('login/html/index.html')

@app.route("/secret_ingredient/blog/", methods=['GET','POST'])
def show_blog():
    if user_login == None:
        return login_page()
    blogs = db.post_get_all_all()
    i = blogs.count() 
    return render_template("login/html/admin.html", data=user_login,blog=blogs,ln=i)
    #return render_template("login/html/admin.html", data=user_login,blog=blogs[0] ,ln=i)

@app.route("/secret_ingredient/add-new-post/",methods=['GET','POST'])
def show_add():
    if user_login == None:
        return login_page()

    return render_template("login/html/add-new-post.html",data = user_login)


@app.route("/post/test",methods=['POST'])
def post_test():
    data_body = request.json
    '''db.uploadpost(postTitle=data_body["title"],email=data_body["username"], 
    thumbnail_IMG_URL=data_body["thumbnail"],slug=data_body["slug"],
    postContent=data_body["postContent"],ispublished=data_body["isPublished"],
    tags=data_body["tags"])'''
    #db.uploadpost("day la bai post 1","admin","thumbnail","day-la-bai-post-1","khong co gi ngoai test","True","AI")
    db.uploadpost(data_body['title'],data_body["username"],data_body["thumbnail"],data_body["slug"],data_body["postContent"],data_body["isPublished"],data_body["tags"])
    return jsonify({"success":True})



@app.route('/uploadpost', methods=["POST"]) #{postTitle,email,thumbnail_IMG_URL,slug,postContent,ispublish}
def uploadpost():
    data= request.get_json()
    result = db.uploadpost(data.get("postTitle"),data.get("email"),data.get("thumbnail_IMG_URL"),data.get('slug'),data.get("postContent"),data.get("ispublish"),data.get("tags"))
    print(data)
    return jsonify({"success": True})





@app.route('/save_images', methods=["POST"])
def save_images():
    images = request.files.getlist("images")
    logging.warning(images)
    hex_code = request.form.get("hex_code")
    return_paths = []
    for image in images:
        print(image.filename)
        filename = '{}.jpg'.format(int(round(time.time() * 1000)))
        relative_path = os.path.join('static', filename)
        path = os.path.join(STATIC_FOLDER, filename)
        print(path)
        image.save(path)
        return_paths.append('http://localhost:5000/' + relative_path)

    print('aaaaaaaaaa : ',images)
    
    return jsonify({'baseurl' : 'http://localhost:5000', "messages" : "success", "error" : 0, "paths": return_paths})

@app.route('/secret_ingredient/edit/<slug>')
def edit_post(slug):
    if ".html" not in slug:
        data = db.findpost(slug)
        print("slug la :",slug)
        print(data)
        comments = db.getcommentofpost(slug, 0, time.time(), 0)
        comments = json.loads(comments)
        cover_image=data['thumbnail_IMG_URL'].split('/')[-1]

        for comment in comments:
            print(comment)
            print(type(comment))
            comment["commentDate"] = date.fromtimestamp(comment["commentDate"]).strftime("%B %d, %Y AT %I:%M%p")
            # print(comm)
        return render_template("login/html/edit-post.html", data = user_login,text_title=data["postTitle"], content=data['postContent'], cover_image=cover_image, comments_len=len(comments), comments=comments)
    else:
        return render_template("/blog/contact.html")

@app.route('/blog/<slug>')
def show_post(slug):
    print(slug)
    if ".html" not in slug:
        data = db.findpost(slug)
        print(data)
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







@app.route("/register",methods=['POST'])
def api_regis():
    data_body = request.json
    #print(data_body["username"])
    cursor = db.insert_user(data_body['username'],data_body['password'])    
    return jsonify({"success":True})
    

@app.route("/deletepost", methods=['POST'])
def api_delete():
    data_body = request.json
    cursor = db.delete_post()
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
