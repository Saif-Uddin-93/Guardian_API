/* eslint-disable prettier/prettier */
$(document).ready(function () {

    var key = ""
    var articleNumber = 0;
    var filterBtn = $("#filter-btn")
    var ratingCheckbox = $("#rating-check")
    var ratingThumb = $(".range-thumb")

    filterBtn.on("click", function () {
        filtersVisible = $("#filters").prop("hidden")
        $("#filters").prop("hidden", !filtersVisible)
    })

    ratingCheckbox.on("click", function(){
        ratingEnabled = $("#rating-check").prop("checked")
        $("#rating").prop("disabled", !ratingEnabled);
        if (ratingEnabled){
            $("#rating-output").val($("#rating").val())
            $(".rating-span-text").css("background-color", "rgb(247, 198, 51)")
        }else {
            $("#rating-output").val("")
            $(".rating-span-text").css("background-color", "rgb(170, 176, 188)")
        }
    })

    ratingThumb.on("mouseup", function(){
        rating = $("#rating").val()
        roundedRating = Math.round(rating)
        $("#rating-output").val(roundedRating)
        $("#rating").val(roundedRating)
    })

    function build_guardian_api_url (term="", opts=[]) {
        searchTerm = $("#search-string").val() ? $("#search-string").val() : term
        filters = ""
        console.log(opts)
        opts.forEach(keyVal => {
            console.log(keyVal)
            filters += `${keyVal[0]}=${keyVal[1]}&`
        });
        console.log(filters)
        return searchTerm ? `https://content.guardianapis.com/search?q=${searchTerm}&show-blocks=body&${filters}api-key=${key || 'test'}` : null
    }

    $(".clear").click(function () {
        articleNumber = 0;
        $("#search-string").val("");
        $("#article-results").empty();
    });

    $("#sqs").on("click", function () {
        console.log("sending to SQS")
        apiID = $("#aws-api").val()
        console.log(apiID)
        // const re = new RegExp("\\.execute-api\\.eu-west-2\\.amazonaws\\.com/dev$"); 
        const re = /^[a-z0-9]{10,12}$/;
        validApi = re.test(apiID)
        console.log(validApi)
        if (validApi){
            api = `https://${apiID}.execute-api.eu-west-2.amazonaws.com/dev`
            fetch(api)
                .then(function (response) {
                    return response.json()
                }).then(function(data){
                    console.log(data)
                })
            }
        })

    $(".search").on("click", function () {
        $("#article-results").empty();
        articleNumber = 0;
        api = build_guardian_api_url()
        fetch(api)
            .then(function (response) {
                return response.json();
            }).then(function (data) {
                console.log(api)
                console.log(data);
                console.log(data.response.results);
                for (i = 0; i < data.response.results.length; i++) {
                    articleNumber++;
                    var article = $("<div>");
                    article.addClass("well well-lg row");
                    var title = $("<h3>");
                    title.addClass("title");
                    title.text(data.response.results[i].webTitle);
                    var description = $("<div>");
                    description.addClass("description");
                    var iframeFix = data.response.results[i].blocks.body[0].bodyHtml.replace('<iframe height="480" width="854"', "<iframe")
                    description.html(iframeFix);
                    console.log(description)
                    var number = $("<div class='articleNumber'>").text(`${articleNumber}.`);
                    $(article).append(number, title, description);
                    $("#article-results").append(article);
                }
            });
    });
});