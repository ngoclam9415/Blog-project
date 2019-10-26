import pymongo
from pymongo import MongoClient
import time
from bson.objectid import ObjectId
from bson.json_util import dumps

class BlogDatabase:
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://dat:mothai34@cluster0-4qfvw.mongodb.net/test?retryWrites=true&w=majority")
        # self.cluster = MongoClient("localhost", 27017)
        self.db = self.cluster["blogDb"]
        self.user_collection = self.db["usertb"]
        self.post_collection = self.db["posttb"]
        self.comment_collection = self.db["commenttb"]
    
    def insert_user(self, username,userpassword):
	    curtime = time.time()
	    user = {"username": username, "userpassword":userpassword, "createdate" : curtime, "role": 1, "active": True}
	    result = self.user_collection.insert_one(user)
	    print(result)
	    return result

    def find_user(self, username):
        cursors = self.user_collection.find({"username": username})
        for cursor in cursors:
            print(cursor)
        return dumps(cursors)

    def delete_user(self, username):
        result = self.user_collection.delete_one({"username": username})
        print(result)
        return result

    #PostCollection
    def uploadpost(self, postTitle,email,thumbnail_IMG_URL,slug,postContent,ispublished, tags):
        curtime = time.time()
        post = {"postTitle":postTitle, "postDate": curtime, "email":email, "thumbnail_IMG_URL" : thumbnail_IMG_URL, "slug": slug, "postContent": postContent, "ispublished": ispublished,"isDeleted": False, "tags" : tags}
        result = self.post_collection.insert_one(post)
        for tag in tags:
            self.insert_to_tag_collection(tag, str(result.inserted_id), post["slug"], curtime, thumbnail_IMG_URL, postTitle, email, ispublished)
        return result

    #Find post by slug
    def findpost(self, slug_url):
        print(slug_url)
        cursor = self.post_collection.find_one({"slug" : slug_url})
        print(cursor)
        if cursor is None:
            return None
        return dict(cursor)


    # def find_latest_comment_post(self, nof_post):
        # self.comment_collection.distinct("")

    def update_post(self,postid, postTitle,email,thumbnail_IMG_URL,slug,postContent, ispublished, tags):
        curtime = time.time()
        querry= {"_id": ObjectId(postid)}
        post = {"$set":{"postTitle":postTitle, "postDate": curtime, "email":email, "thumbnail_IMG_URL" : thumbnail_IMG_URL, "slug": slug, "postContent": postContent, "ispublished": ispublished,"isDeleted": False, "tags" : tags}}
        result = self.post_collection.update_one(querry,post)
        for tag in tags:
            self.update_to_tag_collection(tag, postid, slug, curtime, thumbnail_IMG_URL, postTitle, email, ispublished)
        return result

    def findall_post(self):
        cursors = self.post_collection.find({"isDeleted": False})
        return dumps(cursors)

    def findlimit_post(self,startTime,endTime,limit, skipped_item=1):
        # Find post tu lau nhat den gan nhat
        print(self.post_collection.estimated_document_count() - skipped_item*limit)
        nof_documents = self.post_collection.estimated_document_count()
        if nof_documents < skipped_item*limit:
            skip = (skipped_item-1)*limit
        else:
            skip = nof_documents - skipped_item*limit
        print(skip)
        cursors = self.post_collection.find({"ispublished": True, "isDeleted": False, "postDate": {"$gte" : startTime, "$lte" : endTime}}).sort('time', -1).skip(skip).limit(limit)
        return dumps(cursors)

    def findpostbyId(self,postid):
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
    def insert_comment(self,slug,commenterName,commenterEmail,CommentText, curtime):
        comment = {"slug":slug,"commenterName":commenterName, "commenterEmail": commenterEmail, "commentDate":curtime, "CommentText" : CommentText}
        result = self.comment_collection.insert_one(comment)
        return result, comment

    def delete_comment(self,comentid):
        result = self.comment_collection.delete_one({"_id": ObjectId(comentid)})
        # print(result)
        # return result

    def getcommentofpost(self,slug,timestart,endtime,commentnumber):
        data = []
        cursors = self.comment_collection.find({"slug": slug, "commentDate": {"$gte" : timestart, "$lte" : endtime}}).sort('commentDate', -1).limit(commentnumber)
        return dumps(cursors)

    def insert_to_tag_collection(self, tag, id, slug, curtime,thumbnail_IMG_URL, postTitle, email, ispublished):
        object_id = ObjectId(id)
        self.db[tag].insert_one({"_id" : object_id, 
                    "slug" : slug, "postDate" : curtime, 
                    "thumbnail_IMG_URL" : thumbnail_IMG_URL, 
                    "postTitle" : postTitle,
                    "email" : email,
                    "ispublished" : ispublished,
                    "isDeleted" : False})

    def query_posts_by_tag(self, tag, startTime, endTime, limit= 10, skipped_item=1):
        nof_documents = self.db[tag].estimated_document_count()
        print(tag)
        if nof_documents < skipped_item*limit:
            skip = (skipped_item-1)*limit
        else:
            skip = nof_documents - skipped_item*limit
        cursors = self.db[tag].find({"ispublished": True, "isDeleted": False, "postDate": {"$gte" : startTime, "$lte" : endTime}}).sort('time', -1).skip(skip).limit(limit)
        return dumps(cursors), nof_documents

    def comment_collection_find_recent_post(self, limit=3):
        cursors = self.comment_collection.aggregate([
            {"$group" : {
                "_id" : "$slug",
                "name" : {"$last" : "$commenterName"},
                "email" : {"$last" : "$commenterEmail"},
                "text" : {"$last" : "$CommentText"},
                "last_date" : {"$last" : "$commentDate"}
            }},
            {"$sort" : {"last_date" : -1}},
            # {"$limit" : limit},
        ])
        # cursors = dumps(cursors)
        cursors = list(cursors)
        print('cursor : ', cursors)
        print("limit = ", limit)
        print("len of cursors : ",len(cursors))
        field_query_values = [cursor["_id"] for cursor in cursors]
        new_cursors = self.post_collection.find({"slug" : {"$in" : field_query_values}, "ispublished": True, "isDeleted": False}).limit(limit)
        # return_post_info = []
        sort_key = {}
        for cursor in cursors:
            sort_key[cursor["_id"]] = cursor["last_date"]
        new_cursors = sorted(new_cursors, key = lambda k : sort_key[k['slug']], reverse=True)
        
        return list(new_cursors), cursors
        # return dumps(cursors)

    def post_collection_modify_post_stage(self, slug, ispublished):
        self.post_collection.update({"slug" : slug}, {"$set" : {"ispublished" : ispublished}})
        

    def update_to_tag_collection(self, tag, id, slug, curtime,thumbnail_IMG_URL, postTitle, email, ispublished):
        object_id = ObjectId(id)

        self.db[tag].update_one({"_id" : object_id},{ "$set" :  
                    {"slug" : slug, "postDate" : curtime, 
                    "thumbnail_IMG_URL" : thumbnail_IMG_URL, 
                    "postTitle" : postTitle,
                    "email" : email,
                    "ispublished" : ispublished,
                    "isDeleted" : False}}, upsert=True)

    def delete_to_tag_collection(self, tag, id):
        self.db[tag].remove({"_id" : ObjectId(id)})   

    def delete_post_by_slug(self, slug):
    #    result = self.post_collection.update_one({"slug": slug},{"$set":{"isDeleted": True}})
        self.post_collection.remove({"slug": slug})
        self.comment_collection.remove({"slug" : slug})
        for tag in ["AI/ML", "Front-end", "Back-end", "System","Data"]:
            # self.db[tag].update_one({"slug": slug},{"$set":{"isDeleted": True}})
            self.db[tag].remove({"slug" : slug})
        
    def query_commentId_as_string(self, slug):
        cursors = self.comment_collection.find({"slug" : slug})
        cursors = list(cursors)
        for cursor in cursors:
            cursor["_id"] = str(cursor["_id"])
        return cursors

if __name__ == '__main__':
    import time
    BDB = BlogDatabase()
    # data = BDB.query_posts_by_tag("AI/ML", 0, time.time(), 6, 1)
    # data = BDB.comment_collection_find_recent_post()
    data = db.query_commentId_as_string("asdasd-testing-some-thing")
    print(data)
    print(type(data))
