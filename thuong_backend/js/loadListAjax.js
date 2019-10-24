jQuery("#list2").jqGrid({
    url:'server.php?q=2',
 datatype: "json",
    colNames:['ID','Title', 'Slug', 'Published','Edit','Delete'],
    colModel:[
        {name:'id',index:'id', width:55},
        {name:'Title',index:'Title asc', width:90},
        {name:'Slug',index:'Slug', width:100},
        {name:'Published',index:'Published', width:80, align:"right"},
        {name:'Edit',index:'Edit', width:80, align:"right"},		
        {name:'Delete',index:'Delete', width:80,align:"right"}	
    ],
    rowNum:10,
    rowList:[10,20,30],
    pager: '#pager2',
    sortname: 'id',
 viewrecords: true,
 sortorder: "desc",
 caption:"List Blog"
});
jQuery("#list2").jqGrid('navGrid','#pager2',{edit:false,add:false,del:false});