var upload_comment_url = window.location.origin + "/uploadcomment"

$("#postcomment").on("click",post_comment)


function post_comment(){
  var url_list = window.location.href.split("/");
  var slug = url_list[url_list.length - 1];
  var data = {
    slug : slug,
    commenterName : $("#name").val(),
    commenterEmail : $("#email").val(),
    CommentText : $("#message").val(),
  };
  post_comment(upload_comment_url, data).then(response => {
    render_comment(response)
  })
}

async function post_comment(url, data){
  var response = fetch(url, {
    method : "POST",
    headers : {
      'Content-Type' : 'application/json'
    },
    body : data,
  })
  return await response.json();
}

function render_comment(data){
  var render_item = '<li class="comment">  <div class="vcard">    <img src="https://fresherseason2-teamtwo.appspot.com/static/blog/images/person_1.jpg" alt="Image placeholder">  </div>  <div class="comment-body">    <h3>{{comments[i]["commenterName"]}}</h3>    <div class="meta">{{comments[i]["commentDate"]}}</div>    <p>{{comments[i]["CommentText"]}}</p>  </div></li>'
  render_item = render_item.replace('{{comments[i]["commenterName"]}}', data.commenterName);
  render_item = render_item.replace('{{comments[i]["commenterEmail"]}}', data.commenterEmail);
  render_item = render_item.replace('{{comments[i]["commenterText"]}}', data.commenterText);
  
  var number_of_comments = $("#nof_comments").val();
  $("#nof_comments").val(parseInt(number_of_comments) + 1);
  $(".comment-list").prepend(render_item);
}
