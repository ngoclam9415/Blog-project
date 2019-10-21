var upload_comment_url = window.location.origin + "/uploadcomment";
const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

$(".p-5.bg-light").submit(function(event){
  event.preventDefault()
  var url_list = window.location.href.split("/");
  var slug = url_list[url_list.length - 1];
  var data = {
    slug : slug,
    commenterName : $("#name").val(),
    commenterEmail : $("#email").val(),
    CommentText : $("#message").val(),
  };
  send_post_comment(upload_comment_url, data).then(response => {
    console.log(response);
    render_comment(response);
  })
})


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

function render_comment(data){
  var render_item = '<li class="comment">  <div class="vcard">    <img src="https://fresherseason2-teamtwo.appspot.com/static/blog/images/person_1.jpg" alt="Image placeholder">  </div>  <div class="comment-body">    <h3>{{comments[i]["commenterName"]}}</h3>    <div class="meta">{{comments[i]["commentDate"]}}</div>    <p>{{comments[i]["CommentText"]}}</p>  </div></li>';
  var time = new Date(data.commentDate*1000);
  var hours = time.getHours();
  var ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12;
  var time_string = monthNames[time.getMonth()] + " " + time.getDate() + ", " + time.getFullYear() + " AT " + hours + ':' + ((time.getMinutes()<10?'0':'') + time.getMinutes())+ampm 
  render_item = render_item.replace('{{comments[i]["commenterName"]}}', data.commenterName);
  console.log(render_item, data.commenterName)
  render_item = render_item.replace('{{comments[i]["commentDate"]}}', time_string);
  console.log(render_item, time_string)
  render_item = render_item.replace('{{comments[i]["CommentText"]}}', data.CommentText);
  console.log(render_item, data.CommentText)
  
  var number_of_comments = $("#nof_comments").val();
  $("#nof_comments").val(parseInt(number_of_comments) + 1);
  $(".comment-list").prepend(render_item);
}
