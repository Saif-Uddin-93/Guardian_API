let searchButton = $("#search-button");
let ratingCheckbox = $("#rating-check");

const apiURI = () => ($("#search-term").val() && $("#aws-api").val()) ? $("#aws-api").val() : "";

searchButton.on("click", function(){
    console.log($("#search-term").val());
    console.log($("#date-from").val());
    console.log($("#date-to").val());
    console.log($("#page-size").val());
    console.log($("#rating").val());
    console.log(apiURI())
});


ratingCheckbox.on("click", function(){
    if(ratingCheckbox.prop("checked")){
        $("#rating").prop("disabled", false);
    }else{
        $("#rating").prop("disabled", true);
    }
})

let apiID = "l3sxz02jal"
let region = "eu-west-2"
let stage = "dev"
apiTemplate = `https://${apiID}.execute-api.${region}.amazonaws.com/${stage}`

