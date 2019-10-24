var upload_file = [];
var upload_images_url = window.location.origin +  "/save_images";
var upload_post_url = window.location.origin + "/uploadpost";

class FileUploader{
    constructor(){
        this.title_img = undefined;
        this.content_img = undefined;
    }

    upload_tiltle_images(url, files){
        this.request_upload_images(url, files).then(response => {
            console.log(response)
            var title_url =  response.paths[0]
            if (this.title_img === undefined){
                $(".site-section.py-lg").prepend('<div class="container>"><img src="'+ window.location.origin + '/' + title_url +'" class="img-thumbnail rounded mx-auto d-block" style="width: 50%; height: 50%;" alt="Responsive image"></div>')
            } else{
                $(".img-thumbnail").attr('src', title_url)
            }
            this.title_img = title_url;
        })
    }

    upload_content_images(url, files){
        this.request_upload_images(url, files).then(response => {
            console.log(response);
            var title_url =  response.paths[0];
            $(".jodit_wysiwyg").append('<img src="'+ title_url +'" class="img-thumbnail" style="width: 25%; height: auto;" alt="Responsive image">')
        })
    }

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

}


var fileUploader = new FileUploader();

$('textarea#editor').each(function () {
    var editor = new Jodit(this, {
        height : '800px', 
    });
    editor.value = '<p>start</p>';
});

insert_file_button()

$(document).ready(function(){
    $('input[type="file"]').change(function(e){
        var fileName = e.target.files[0];
        if ($(this).attr("id") === "title_file"){
            fileUploader.upload_tiltle_images(upload_images_url, [fileName])
        } else {
            fileUploader.upload_content_images(upload_images_url, [fileName])
        }
        upload_file.push(fileName)
        alert('The file "' + fileName.name +  '" has been selected.');
    });
    $("#post-btn").on("click", post_blog);
});
// add_input_file_button()

function add_input_file_button(){
    $(".jodit_draganddrop_file_box").find("input").replaceWith('<input type="file" class="form-control-file" id="file_input">');
}

function insert_file_button(){
    // $('<li class="jodit_toolbar_btn jodit_toolbar_btn-separator"></li>').insertAfter('.jodit_toolbar_btn-redo');
    $('<li class="jodit_toolbar_btn"><a id="upload" style="background-color: rgba(255,0,0,0.2);;" onclick="document.getElementById(\'file_input\').click();"><i class="fa fa-upload"></i><input type="file" id="file_input" class="form-control-file" accept="image/*" hidden=""></a></li>').insertAfter('.jodit_toolbar_btn-redo');

}

function get_html_output(){
    return $(".jodit_wysiwyg").html()
}

function post_blog(){
    var title = $('#title_text').val();
    var tags = [];
    var choices = $(".select2-selection__rendered").find(".select2-selection__choice") 
    if (choices.length > 0){
        for (i = 0; i < choices.length; i++){
            tags.push(choices.eq(i).attr("title"))
        }
    }
    var data = {
        postTitle : title, 
        email : window.localStorage.getItem("email"),
        thumbnail_IMG_URL : fileUploader.title_img,
        slug : slugify(title),
        postContent : get_html_output(),
        tags : tags,
    }
    send_blog_request(upload_post_url, data, ispublish=true).then(response => {
        console.log(response);
        window.location.href = window.location.origin + "/blog/" + data.slug;
        // console.log(window.location.origin + "/blog/" + data.slug);
    })
}

function draft_blog(){
    var title = $('#title_text').val();
    var data = {
        postTitle : title, 
        email : window.localStorage.getItem("email"),
        thumbnail_IMG_URL : fileUploader.title_img,
        slug : slugify(title),
        postContent : get_html_output(),
    }
    send_blog_request(upload_post_url, data, ispublish=false).then(response => {
        console.log(response);
        window.location.href = window.location.origin + "/blog/" + data.slug;
    })
}



async function send_blog_request(url, data, ispublish){
    data.ispublish = ispublish;
    const response = await fetch(url, {
        method : 'POST',
        headers : {
            'Content-Type' : 'application/json'
        },
        body : JSON.stringify(data)
    });
    return await response.json();
}

function slugify(string) {
  const a = 'àáâäæãåāăąçćčđďèéêëēėęěğǵḧîïíīįìłḿñńǹňôöòóœøōõṕŕřßśšşșťțûüùúūǘůűųẃẍÿýžźż·/_,:;'
  const b = 'aaaaaaaaaacccddeeeeeeeegghiiiiiilmnnnnooooooooprrsssssttuuuuuuuuuwxyyzzz------'
  const p = new RegExp(a.split('').join('|'), 'g')

  return string.toString().toLowerCase()
    .replace(/\s+/g, '-') // Replace spaces with -
    .replace(p, c => b.charAt(a.indexOf(c))) // Replace special characters
    .replace(/&/g, '-and-') // Replace & with 'and'
    .replace(/[^\w\-]+/g, '') // Remove all non-word characters
    .replace(/\-\-+/g, '-') // Replace multiple - with single -
    .replace(/^-+/, '') // Trim - from start of text
    .replace(/-+$/, '') // Trim - from end of text
}




