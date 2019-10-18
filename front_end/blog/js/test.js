$('textarea#editor').each(function () {
    var editor = new Jodit(this, {
        height : '500px', 
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