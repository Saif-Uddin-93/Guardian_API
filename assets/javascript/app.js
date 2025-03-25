/* eslint-disable prettier/prettier */
$(document).ready(function () {

    var key = ""
    var searchString = "";
    var articleNumber = 0;

    const build_api_url = (term="tech", opts=[]) => {
        searchTerm = $("#search-string").val() ? $("#search-string").val() : term
        filters = ""
        opts.forEach(keyVal => {
            filters += `${keyVal[0]}=${keyVal[1]}&`
        });
        return `https://content.guardianapis.com/search?q=${searchTerm}&show-blocks=body&${filters}api-key=${key || 'test'}`
    }

    $(".clear").click(function () {
        articleNumber = 0;
        $("#search-string").val("");
        $("#article-results").empty();
    });

    $(".search").on("click", function () {
        $("#article-results").empty();
        articleNumber = 0;
        searchString = $("#search-string").val();

        fetch(build_api_url(opts = [["from-date", "2020-01-01"], ["page-size", "1"]]))
            .then(function (response) {
                return response.json();
            }).then(function (data) {
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
                    description.html(data.response.results[i].blocks.body[0].bodyHtml);
                    console.log(description)
                    var number = $("<div class='articleNumber'>").text(articleNumber);
                    $(article).append(number, title, description);
                    $("#article-results").append(article);
                }
            });
    });
});