/**
 * Created by ethan on 2016/09/14.
 */

$(function () {
    var fields = 0;

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
    });

    $("#live-button").on("click", function () {
        var flag = true;
        var id = $(this).attr("datasrc");

        $(".state-select :selected").each(function (index, value) {
            if (value.text != "Complete") {
                flag = false;
            }
        });

        if (flag) {
            $.ajaxSetup({
                headers: {"X-CSRFToken": $.cookie("csrftoken")}
            });

            $.ajax({
                url: "/tasks/" + id + "/live/",
                type: "POST",
                success: function () {
                    location.reload();
                },
                error: function () {
                    console.log("Error: Can't update question liveness.")
                }
            })
        }
        else {
            alert("Cannot make questions live. There are questions with a state that is not 'Complete'.")
        }
    });

    $("#id_open").on("change", function () {
        var state = $(this).is(":checked");
        var id = $(this).attr("datasrc");

        $.ajaxSetup({
            headers: {"X-CSRFToken": $.cookie("csrftoken")}
        });

        $.ajax({
            url: "/tasks/" + id + "/open/",
            type: "POST",
            data: {
                "state": state
            },
            success: function () {
                location.reload();
            },
            error: function () {
                console.log("Error: Can't update question order state.")
            }
        })
    });

    $(".box").on("click", function () {
        var id = $(this).attr("question");
        var block = $(this).attr("block");

        $.ajaxSetup({
            headers: {"X-CSRFToken": $.cookie("csrftoken")}
        });

        $.ajax({
            url: "/questions/" + id + "/move/",
            type: "POST",
            data: {
                "block": block
            },
            success: function () {
                location.reload();
            },
            error: function () {
                console.log("Error: Can't update task state.")
            }
        })
    });

    $("#add-field").off().on("click", function () {
        $(".field-classes").append(
            '<div id="class-field-div"><label class="required"></label>' +
            '<textarea class="pad-text" cols="40" id="id_class_' + fields + '" name="class" rows="1" style="resize:none;" required="">' +
            '</textarea><img class="del-field" src="/static/admin/img/icon-deletelink.svg" alt="delete"></div>'
        );
        fields++;

        $(document).on("click", ".del-field", function () {
            $(this).parent().remove();

        })
    });
});
