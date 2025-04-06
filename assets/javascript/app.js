$(document).ready(function () {

    var key = ""
    var articleNumber = 0;
    var filterBtn = $("#filter-btn")
    var ratingCheckbox = $("#rating-check")
    var ratingThumb = $(".range-thumb")
    var guardianData = {}

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
        filters = ""
        console.log(opts)
        opts.forEach(keyVal => {
            console.log(keyVal)
            filters += `${keyVal[0]}=${keyVal[1]}&`
        });
        console.log(filters)
        return `https://content.guardianapis.com/search?q=${term}&show-blocks=body&${filters}api-key=${key || 'test'}`
    }

    function build_aws_api_url (apiID, queueName="guardian-queue", opts=[]) {
        filters = ""
        opts.forEach(keyVal => {
            console.log(keyVal)
            filters += `${keyVal[0]}=${keyVal[1]}&`
        });
        console.log(filters)
        return `https://${apiID}.execute-api.eu-west-2.amazonaws.com/dev?queue-name=${queueName}${filters ? '&'+filters : ''}`
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
        console.log(guardianData)
        if (validApi && guardianData) {
            api = build_aws_api_url(apiID = apiID)
            fetch(api, {
                method: "POST",  // Specify the HTTP method
                mode: 'no-cors',
                headers: {
                    "Content-Type": "application/json"  // Set the request headers
                },
                body: JSON.stringify(guardianData)  // Convert data to JSON string
            })
                .then(response => response.json())  // Convert response to JSON
                .then(data => console.log("Success:", data))  // Handle success
                .catch(error => console.error("Error:", error));  // Handle errors
            $("#sqs-confirm").prop("hidden", false)
        }
    })

    $("#sqs-confirm .btn-close").on("click", ()=>{
        $("#sqs-confirm").prop("hidden", true)
    })

    $(".search").on("click", function () {
        if(!$("#search-string").val()){
            return
        }
        $("#article-results").empty();
        articleNumber = 0;
        searchTerm = $("#search-string").val() ? $("#search-string").val() : ""
        filters = [
            ["from-date", `${$('#date-from').val()}`],
            ["to-date", `${$('#date-to').val()}`],
            ["page-size", `${$('#page-size').val()}`],
            ["star-rating", `${$('#rating-output').val()}`],
        ]
        validFilters = filters.filter(function (element) {
            if (element[1]) return element
        })
        console.log("filters: \n",filters)
        console.log("valid filters: \n",validFilters)
        api = build_guardian_api_url(searchTerm, validFilters)
        fetch(api)
            .then(function (response) {
                return response.json();
            }).then(function (data) {
                guardianData = data.response
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