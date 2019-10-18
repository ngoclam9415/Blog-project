var upload_file = [];

class FileUploader{
    constructor(){
        this.title_img = undefined;
        this.content_img = undefined;
    }

    upload_tiltle_images(url, files){
        this.request_upload_images(url, files).then(response => {
            this.title_img = response.paths[0];
        })
    }

    async request_upload_images(url, files){
        const formData = new FormData();
        console.log(files.length)
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
        height : '500px', 
        // uploader:{
        //     url: 'http://localhost:5000/save_images',
        //     headers:{
        //         'Access-Control-Allow-Origin': true,
        //     },
        //     format: 'json',
        //     filesVariableName(i){
        //         return 'images'
        //     }
        // }
    });
    editor.value = '<p>start</p>';
});

insert_file_button()

$(document).ready(function(){
    $('input[type="file"]').change(function(e){
        var fileName = e.target.files[0];
        upload_file.push(fileName)
        alert('The file "' + fileName.name +  '" has been selected.');
    });
});
// add_input_file_button()

function add_input_file_button(){
    $(".jodit_draganddrop_file_box").find("input").replaceWith('<input type="file" class="form-control-file" id="file_input">');
}

function insert_file_button(){
    // $('<li class="jodit_toolbar_btn jodit_toolbar_btn-separator"></li>').insertAfter('.jodit_toolbar_btn-redo');
    $('<li class="jodit_toolbar_btn"><a id="upload" style="background-color: rgba(255,0,0,0.2);;" onclick="document.getElementById(\'file_input\').click();"><i class="fa fa-upload"></i><input type="file" id="file_input" class="form-control-file" accept="image/png, image/jpeg" hidden=""></a></li>').insertAfter('.jodit_toolbar_btn-redo');

}

function get_html_input(){
    return $(".jodit_wysiwyg").html()
}
// $(".jodit_toolbar_btn-image").on("click", function(){
//     add_input_file_button()
//     $("#file_input").change(function(event){
//         var file = event.target.files[0];
//         console.log(file.name);
//     })
// })
