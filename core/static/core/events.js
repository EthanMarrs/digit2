/**
 * Created by ethan on 2016/09/14.
 */

$(function () {
    $(".move-link").on('click', function () {
        $.ajaxSetup({
            headers: {"X-CSRFToken": $.cookie("csrftoken")}
        });

        var url = $(this).attr("url");

        $.ajax({
            url: url,
            type: "POST",
            success: function () {
                location.reload();
            },
            error: function () {
                console.log("Error: Can't update question position.")
            }
        })
    });

    $(".state-select").on("change", function () {
        var code = $(this).find(":selected").attr("value");
        var src = $(this).attr("about");

        $.ajaxSetup({
            headers: {"X-CSRFToken": $.cookie("csrftoken")}
        });

        $.ajax({
            url: "/questions/" + src + "/state/",
            type: "POST",
            data: {
                "value": code
            },
            success: function () {
                location.reload();
            },
            error: function () {
                console.log("Error: Can't update question state.")
            }
        })

    });

    $(".edit-description").on("click", function () {
        var text = $(this).siblings(".description").text();
        $(this).siblings("form").children("textarea").text(text);
        $(this).siblings("form.hidden").removeClass("hidden");
    });

    $(".update-button").on("click", function () {
        var text = $(this).siblings("textarea").val();
        var id = $(this).attr("datasrc");

        $.ajaxSetup({
            headers: {"X-CSRFToken": $.cookie("csrftoken")}
        });

        $.ajax({
            url: "/blocks/" + id + "/",
            type: "POST",
            data: {
                "text": text
            },
            success: function () {
                location.reload();
            },
            error: function () {
                console.log("Error: Can't update block.")
            }
        })
    });

    $(".comment-button").on("click", function () {
        var text = $(this).siblings("textarea").val();
        var id = $(this).attr("datasrc");

        $.ajaxSetup({
            headers: {"X-CSRFToken": $.cookie("csrftoken")}
        });

        $.ajax({
            url: "/comments/" + id + "/",
            type: "POST",
            data: {
                "text": text
            },
            success: function () {
                location.reload();
            },
            error: function () {
                console.log("Error: Can't add comment.")
            }
        })
    })

    $(".")
});
