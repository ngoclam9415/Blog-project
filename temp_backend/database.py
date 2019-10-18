import pymongo
from pymongo import MongoClient
import time
from bson.objectid import ObjectId


cluster = MongoClient("mongodb+srv://dat:mothai34@cluster0-4qfvw.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["blogDb"]
user_collection = db["usertb"]
post_collection = db["posttb"]
comment_collection = db["commenttb"]


#Usercollection
def insert_user(username,userpassword):
	curtime = time.time()
	user = {"username": username, "userpassword":userpassword, "createdate" : curtime, "role": 1, "active": True}
	result = user_collection.insert_one(user)
	print(result)
	return result

def find_user(username):
	cursors = user_collection.find({"username": username})
	for cursor in cursors:
		print(cursor)
	return cursors

def delete_user(username):
	result = user_collection.delete_one({"username": username})
	print(result)
	return result

#PostCollection
def insert_post(postTitle,username,thumbnailIMG,slug,postContent):
	curtime = time.time()
	post = {"postTitle":postTitle, "postDate": curtime, "username":username, "thumbnailIMG" : thumbnailIMG, "slug": slug, "postContent": postContent, "ispublished": True,"isDeleted": False}
	result = post_collection.insert_one(post)
	print(result)
	return result

def findall_post():
	cursors = post_collection.find({"ispublished": True, "isDeleted": False})
	for cursor in cursors:
		print(cursor)
	return cursors

def findlimit_post(startTime,endTime,limit):
	cursors = post_collection.find({"ispublished":True, "isDeleted": False, "postDate": {"$gte" : startTime, "$lte" : endTime}}).sort('postDate', -1).limit(limit)
	for cursor in cursors:
		print(cursor)
	return cursors

def findpostbyId(postId):
	cursors = post_collection.find_one({"_id":ObjectId(postid)})
	print(cursors)
	return cursors

def delete_post(postid):
	result = post_collection.update_one({"_id": ObjectId(postid)},{"$set":{"isDeleted": False}})
	print(result)
	return result

def unpublish_post(postid):
	result = post_collection.update_one({"_id": ObjectId(postid)},{"$set":{"ispublished": False}})
	print(result)
	return result


#CommentColection
def insert_comment(commentName,commentEmail,CommentText):
	curtime = time.time()
	comment = {"commentName":commentName, "commentEmail": commentEmail, "commentDate":curtime, "CommentText" : CommentText}
	result = comment_collection.insert_one(comment)
	print(result)
	return result
def delete_comment(comentid):
    result = comment_collection.remove({"_id": ObjectId(comentid)})
    print(result)
    return result


if __name__ == '__main__':
	delete_comment("5da9138603caeb6825af77b4")


