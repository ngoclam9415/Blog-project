import pymongo
from pymongo import MongoClient
import time
from bson.objectid import ObjectId
from bson.json_util import dumps

class BlogDatabase:
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://dat:mothai34@cluster0-4qfvw.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.cluster["blogDb"]
        self.user_collection = self.db["usertb"]
        self.post_collection = self.db["posttb"]
        self.comment_collection = self.db["commenttb"]
    #Usercollection
    def insert_user(self, username,userpassword):
	    curtime = time.time()
	    user = {"username": username, "userpassword":userpassword, "createdate" : curtime, "role": 1, "active": True}
	    result = self.user_collection.insert_one(user)
	    print(result)
	    return result

    def find_user(self, username):
        cursors = selfuser_collection.find({"username": username})
        for cursor in cursors:
            print(cursor)
        return dumps(cursors)

    def delete_user(self, username):
        result = user_collection.delete_one({"username": username})
        print(result)
        return result

    #PostCollection
    def uploadpost(self, postTitle,email,thumbnail_IMG_URL,slug,postContent,ispublished):
        curtime = time.time()
        post = {"postTitle":postTitle, "postDate": curtime, "email":email, "thumbnail_IMG_URL" : thumbnail_IMG_URL, "slug": slug, "postContent": postContent, "ispublished": ispublished,"isDeleted": False}
        result = self.post_collection.insert_one(post)
        print(result)
        return result

    def update_post(self,postid, postTitle,email,thumbnail_IMG_URL,slug,postContent):
        curtime = time.time()
        querry= {"_id": ObjectId(postid)}
        post = {"$set":{"postTitle":postTitle, "postDate": curtime, "email":email, "thumbnail_IMG_URL" : thumbnail_IMG_URL, "slug": slug, "postContent": postContent, "ispublished": True,"isDeleted": False}}
        result = self.post_collection.update_one(querry,post)
        return result

    def findall_post(self):
        cursors = self.post_collection.find({"ispublished": True, "isDeleted": False})
        return dumps(cursors)

    def findlimit_post(self,startTime,endTime,limit):
        cursors = self.post_collection.find({"ispublished": True, "isDeleted": False, "postDate": {"$gte" : startTime, "$lte" : endTime}}).sort('time', -1).limit(limit)
        return dumps(cursors)

    def findpostbyId(self,postId):
        cursors = self.post_collection.find_one({"_id":ObjectId(postid)})
        print(cursors)
        return dumps(cursors)

    def delete_post(self,postid):
        result = self.post_collection.update_one({"_id": ObjectId(postid)},{"$set":{"isDeleted": False}})
        print(result)
        return result

    def unpublish_post(self,postid):
        result = self.post_collection.update_one({"_id": ObjectId(postid)},{"$set":{"ispublished": False}})
        print(result)
        return result
    
    def publish_post(self,postid):
        result = self.post_collection.update_one({"_id": ObjectId(postid)},{"$set":{"ispublished": True}})
        print(result)
        return result


    #CommentColection
    def insert_comment(self,postid,commenterName,commenterEmail,CommentText):
        curtime = time.time()
        comment = {"postid":postid,"commenterName":commenterName, "commenterEmail": commenterEmail, "commentDate":curtime, "CommentText" : CommentText}
        result = self.comment_collection.insert_one(comment)
        print(result)
        return result

    def delete_comment(self,comentid):
        result = self.comment_collection.delete_one({"_id": ObjectId(comentid)})
        print(result)
        return result

    def getcommentofpost(self,postid,timestart,endtime,commentnumber):
        data=[]
        cursors = self.comment_collection.find({"postid": postid, "commentDate": {"$gte" : timestart, "$lte" : endtime}}).sort('commentDate', -1).limit(commentnumber)
        return dumps(cursors)

# if __name__ == '__main__':
#     BDB = BlogDatabase()
#     BDB.findall_post()