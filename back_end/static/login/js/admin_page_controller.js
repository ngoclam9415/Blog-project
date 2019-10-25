var edit_post_stage_url = window.location.origin + "/update_post_stage"
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