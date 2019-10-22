# How to make http repquest
## POST request with JSON data
### Client side
```
var upload_comment_url = window.location.origin + "/uploadcomment";

function post_comment(event){
  event.preventDefault()
  var url_list = window.location.href.split("/");
  var slug = url_list[url_list.length - 1];
  var data = {
    slug : slug,
    commenterName : $("#name").val(),
    commenterEmail : $("#email").val(),
    CommentText : $("#message").val(),
  };
  console.log(data)
  send_post_comment(upload_comment_url, data).then(response => {
    console.log(response)
    render_comment(response)
  })
}

async function send_post_comment(url, data){
  const response = await fetch(url, {
    method : "POST",
    headers : {
      'Content-Type' : 'application/json'
    },
    body : JSON.stringify(data),
  }); 
  return await response.json();
}
```
### Server side
```
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
```

## POST Request with Form Data
### Client side
#### Add Event for Input File type
```
$(document).ready(function(){
    $('input[type="file"]').change(function(e){
        var fileName = e.target.files[0];
        request_upload_images(upload_images_url, [fileName]).then(response => {
            console.log(response)
        })
        alert('The file "' + fileName.name +  '" has been selected.');
    });
});
```
#### HTTP request for form
```
async request_upload_images(url, files){
        const formData = new FormData();
        console.log(files.length)
        formData.append("hex_code", window.localStorage.getItem("hex_code"))
        for (let i = 0; i < files.length; i++){
            formData.append("images", files[i]);
        }
        for (var key of formData.entries()) {
            console.log(key[0] + ', ' + key[1]);
        }
        const response = await fetch(url, {
            method : 'POST',
            body : formData 
        });
        return await response.json();
    }
```