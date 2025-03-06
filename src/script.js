var searchButton = $("#search-button");
var ratingCheckbox = $("#rating-check");


searchButton.on("click", function(){
    console.log($("#search-term").val());
    console.log($("#date-from").val());
    console.log($("#date-to").val());
    console.log($("#page-size").val());
    console.log($("#rating").val());
});


ratingCheckbox.on("click", function(){
    if(ratingCheckbox.prop("checked")){
        $("#rating").prop("disabled", false);
    }else{
        $("#rating").prop("disabled", true);
    }
})