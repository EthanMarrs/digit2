/**
 * Created by ethan on 2016/09/14.
 */

$(function() {
    $(".up-link").on('click', function () {
        console.log("yay");
        $.ajax({
            url: "/admin/core/block/6/move-up/?",
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
