var edit_post_stage_url = window.location.origin + "/update_post_stage"
var delete_post_url = window.location.origin + "/delete_post"
var stage_controller = {};

$(document).ready(function(){
    var rows = $("tbody").find("tr");
    for (var i =0; i<rows.length; i++){
        var row = rows.eq(i)
        stage_controller[row.find("td").eq(3).text()] = row.find("td").eq(4).find("select").find("option:selected").text();
    }
})

$(".btn-primary").on("click", function(){
    var modify_value = $(this).closest("tr").find("td").eq(4).find("select").find("option:selected").text();
    var slug = $(this).closest("tr").find("td").eq(3).text();
    if (stage_controller[slug] === modify_value){
        alert("This post wasn't changed");
    } else {
        if (confirm("Modify "+slug+ " stage from "+ stage_controller[slug] + " to "+ modify_value)){
            edit_post_stage(edit_post_stage_url, slug, modify_value).then(response => {
                console.log("EDIT POST STAGE RESPONSE");
                console.log(response)
            });
        } else {}
    }
})



async function edit_post_stage(url, slug, ispublished){
    if (ispublished === "True"){
        ispublished = true;
    } else {
        ispublished = false;
    }
    var data = {slug : slug, 
                ispublished : ispublished};
    const reponse = await fetch(url, {
        method : 'POST',
        headers : {
            'Content-Type' : 'application/json'
        },
        body : JSON.stringify(data)
    });
    return await reponse.json();
}

$(".btn.btn-danger").on("click", function(){
    const this_row = $(this).closest("tr")
    var modify_value = this_row.find("td").eq(4).find("select").find("option:selected").text();
    var slug = this_row.find("td").eq(3).text();
    var data = {slug : slug};
    if (confirm("Do you want to delete post : "+slug)){
        delete_blog_request(delete_post_url, data).then(response => {
            console.log(response);
            window.location.href = window.location.href;
        });
    }
})

async function delete_blog_request(url, data){
    const response = await fetch(url,{
        method : "POST",
        headers :{
            "Content-Type" : "application/json"
        },
        body : JSON.stringify(data)
    });
    return await response.json();
}