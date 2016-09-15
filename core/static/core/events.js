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
});
