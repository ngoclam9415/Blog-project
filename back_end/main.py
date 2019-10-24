from __future__ import print_function
from flask import request,render_template, Flask, send_from_directory, jsonify, Response, redirect
import os
import time
from utils.random_generator import generate_random_hexcode
from utils.bucket_uploader import BucketStorageClient, LocalStorageClient
from database import BlogDatabase
from datetime import datetime
import json
import logging


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'back_end', 'static')
hex_code = generate_random_hexcode()
# app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')
app = Flask(__name__)
db = BlogDatabase()
BSC = BucketStorageClient()
# BSC = LocalStorageClient(STATIC_FOLDER)

category_collection = {"ai-ml" : "AI/ML",
                        "front-end" : "Front-end",
                        "back-end" : "Back-end",
                        "system" : "System",
                        "data" : "Data"}

@app.route('/')
def index():
    page_number = int(request.args.get("page", 1))
    latest_posts = db.findlimit_post(0, time.time(), 10, page_number)
    latest_posts = json.loads(latest_posts)
    nof_document = db.post_collection.count_documents({})
    latest_posts.reverse()
    for latest_post in latest_posts:
        latest_post["postDate"] = datetime.fromtimestamp(latest_post["postDate"]).strftime("%B %d, %Y")
        latest_post["nof_comments"] = db.comment_collection.count_documents({"slug" : latest_post["slug"]})
    pages, current_page_index = caculate_page_number(nof_document, page_number, 10, 5)
    disable_next = ""
    disable_previous = ""
    if len(pages):
        if current_page_index == len(pages) - 1:
            disable_next = "disabled"
        if current_page_index == 0:
            disable_previous = "disabled"
    else:
        disable_next = "disabled"
        disable_previous = "disabled"

    category_post_number = {}
    for key, value in category_collection.items():
        category_post_number[key] = (value, db.db[value].estimated_document_count())

    # recently_commented_post 
    recent_post_info, recent_comment_info = db.comment_collection_find_recent_post(limit=3)
    print('recent_post_info : ',recent_post_info )

    # format [{'_id': {'slug': 'this-is-event-driven-system', 'name': 'Dat', 'email': 'datnn@athena.studio', 'text': 'Hello this is good'}, 'last_date': 1571825624.113014}, {'_id': {'slug': 'meo-uong-sua', 'name': 'Dat', 'email': 'datnn@athena.studio', 'text': 'Whattttt'}, 'last_date': 1571824885.201149}, {'_id': {'slug': 'meo-uong-sua', 'name': 'Dat', 'email': 'datnn@athena.studio', 'text': 'Hehe'}, 'last_date': 1571824876.3144479}]

    for recent_comment in recent_comment_info:
        recent_comment['last_date'] = datetime.fromtimestamp(recent_comment['last_date']).strftime("%B %d, %Y AT %I:%M%p")

    
    return render_template('blog/index.html', 
                                latest_posts=latest_posts,
                                pages=enumerate(pages),
                                current_index=current_page_index,
                                current_page=pages[current_page_index], 
                                disable_next=disable_next,
                                disable_previous=disable_previous,
                                category_post_number=category_post_number.items(),
                                recent_post_info=recent_post_info,
                                recent_comment_info=recent_comment_info,
                                nof_info = len(recent_post_info))

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
    result = db.uploadpost(data.get("postTitle"),data.get("email"),data.get("thumbnail_IMG_URL"),data.get('slug'),data.get("postContent"),data.get("ispublish"), data.get("tags"))
    print(data)
    print(result)
    return jsonify({"success": True})

@app.route('/save_images', methods=["POST"])
def save_images():
    images = request.files.getlist("images")
    logging.warning(images)
    hex_code = request.form.get("hex_code")
    return_paths = []
    for image in images:
        url = BSC.upload_file(image)
        return_paths.append(url)

    print('aaaaaaaaaa : ',images)
    
    return jsonify({'baseurl' : 'http://localhost:5000', "messages" : "success", "error" : 0, "paths": return_paths})

@app.route('/blog/<slug>')
def show_post(slug):
    print(slug)
    if ".html" not in slug:
        data = db.findpost(slug)
        if data is None:
            return "Page is not avaiable"
        comments = db.getcommentofpost(slug, 0, time.time(), 0)
        comments = json.loads(comments)
        for comment in comments:
            print(comment)
            print(type(comment))
            comment["commentDate"] = datetime.fromtimestamp(comment["commentDate"]).strftime("%B %d, %Y AT %I:%M%p")
            # print(comm)


        latest_posts = db.findlimit_post(0, time.time(), 3, 1)
        latest_posts = json.loads(latest_posts)
        latest_posts.reverse()
        for latest_post in latest_posts:
            latest_post["postDate"] = datetime.fromtimestamp(latest_post["postDate"]).strftime("%B %d, %Y")

        category_post_number = {}
        for key, value in category_collection.items():
            category_post_number[key] = (value, db.db[value].estimated_document_count())

        recent_post_info, recent_comment_info = db.comment_collection_find_recent_post(limit=3)
        for recent_comment in recent_comment_info:
            recent_comment['last_date'] = datetime.fromtimestamp(recent_comment['last_date']).strftime("%B %d, %Y AT %I:%M%p")

        return render_template("blog/blog-slug.html", text_title=data["postTitle"], content=data['postContent'], cover_image=data['thumbnail_IMG_URL'], comments_len=len(comments), comments=comments, tags=data["tags"], postDate = datetime.fromtimestamp(data["postDate"]).strftime("%B %d, %Y AT %I:%M%p"),
                    category_post_number=category_post_number.items(),
                    latest_posts=latest_posts,
                    recent_post_info=recent_post_info,
                    recent_comment_info=recent_comment_info,
                    nof_info = len(recent_post_info))
    else:
        return render_template("blog/contact.html")

@app.route('/get_latest_posts', methods=["POST"])
def get_some_posts():
    cursors = db.findlimit_post(0, time.time(), 10, 1)
    # print(cursors)
    return jsonify(cursors)

@app.route('/editor')
def show_editor():
    return render_template("blog/editor.html")

@app.route('/uploadcomment', methods=["POST"]) #{slug,commenterName,commenterEmail,CommentText}
def uploadcomment():
    data = request.get_json()
    curtime = time.time()
    result, comment = db.insert_comment(data.get("slug"),data.get("commenterName"),data.get("commenterEmail"),data.get('CommentText'), curtime)
    print(comment)
    comment = dict(comment)
    comment.setdefault("sucess", True)
    del comment["_id"]
    print(type(comment))
    print(comment)
    return jsonify(comment)

@app.route('/getlimitcomment', methods=["POST"]) #{postid,timestart, endtime, commentnumber}
def getlimitcomment():
    data= request.get_json()
    posts = db.getcommentofpost(data.get("slug"),data.get("starttime"),data.get("endtime"),data.get("commentnumber"))
    print(posts)
    return jsonify(posts)

@app.route('/category/<category_name>')
def show_category_page(category_name):
    page_number = int(request.args.get("page", 1))
    if category_name not in category_collection.keys():
        return "INVALID URL"
    category_posts, nof_document = db.query_posts_by_tag(category_collection[category_name], 0, time.time(), 10, page_number)
    category_posts = json.loads(category_posts)
    for category_post in category_posts:
        category_post["postDate"] = datetime.fromtimestamp(category_post["postDate"]).strftime("%B %d, %Y")
        category_post["nof_comments"] = db.comment_collection.count_documents({"slug" : category_post["slug"]})
    pages, current_page_index = caculate_page_number(nof_document, page_number, 10, 5)
    disable_next = ""
    disable_previous = ""
    if len(pages):
        if current_page_index == len(pages) - 1:
            disable_next = "disabled"
        if current_page_index == 0:
            disable_previous = "disabled"
    else:
        disable_next = "disabled"
        disable_previous = "disabled"

    latest_posts = db.findlimit_post(0, time.time(), 3, 1)
    latest_posts = json.loads(latest_posts)
    latest_posts.reverse()
    for latest_post in latest_posts:
        latest_post["postDate"] = datetime.fromtimestamp(latest_post["postDate"]).strftime("%B %d, %Y")
    
    category_post_number = {}
    for key, value in category_collection.items():
        category_post_number[key] = (value, db.db[value].estimated_document_count())
    print(latest_posts)
    
    recent_post_info, recent_comment_info = db.comment_collection_find_recent_post(limit=3)
    for recent_comment in recent_comment_info:
        recent_comment['last_date'] = datetime.fromtimestamp(recent_comment['last_date']).strftime("%B %d, %Y AT %I:%M%p")
    print('recent_post_info : ',recent_post_info )
    return render_template("/blog/category.html",
                     category_name=category_collection[category_name], 
                     category_posts=category_posts,
                    pages=enumerate(pages),
                     current_index=current_page_index,
                     current_page=pages[current_page_index],
                     disable_next=disable_next,
                     disable_previous=disable_previous,
                     latest_posts=latest_posts,
                     category_post_number=category_post_number.items(),
                     category_subfix=category_name,
                     recent_post_info=recent_post_info,
                    recent_comment_info=recent_comment_info,
                    nof_info = len(recent_post_info))

def caculate_page_number(total_posts, request_page, nof_post_per_page, nof_displayed_page):
    if total_posts == 0:
        return [], 0
    page_indexes = []
    if total_posts > request_page*nof_post_per_page :
        if (total_posts - request_page*nof_post_per_page)//nof_post_per_page + (total_posts%nof_post_per_page > 0) > nof_displayed_page - 1:
            page_indexes = [i + request_page for i in range(nof_displayed_page)]
        else: 
            nof_next_pages = (total_posts - request_page*nof_post_per_page)//nof_post_per_page + (total_posts%nof_post_per_page > 0)
            # print('nof_next_pages : ',nof_next_pages)
            # print(" Loop range : {} - {}".format(0, nof_displayed_page - nof_next_pages - 1))
            for index in reversed(range(nof_displayed_page - nof_next_pages)):
                print(index)
                if request_page - index >= 1:
                    page_indexes.append(request_page - index)
            for next_page in range(nof_next_pages):
                # print("next page index : ",next_page + request_page + 1)
                page_indexes.append(next_page + request_page + 1)
    else:
        for index in range(request_page - nof_displayed_page, request_page + 1):
            if index > 0 :
                page_indexes.append(index)
    return page_indexes, page_indexes.index(request_page)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
