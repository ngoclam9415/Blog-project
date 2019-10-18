$('textarea#editor').each(function () {
    var editor = new Jodit(this, {
        uploader:{
            url: 'http://localhost:5000/save_images',
            headers:{
                'Access-Control-Allow-Origin': true,
            },
            format: 'json',
            filesVariableName(i){
                return 'images'
            }
        }
    });
    editor.value = '<p>start</p>';
});

$(document).ready(function(){
    $('input[type="file"]').change(function(e){
        var fileName = e.target.files[0].name;
        alert('The file "' + fileName +  '" has been selected.');
    });
});