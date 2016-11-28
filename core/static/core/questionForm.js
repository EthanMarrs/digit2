/**
 * Get a UUID
 * A wrapper for the uuid function
 */
var getUUID = function(){
  return uuid()
}

var dict_of_questions = {};
var MQ = MathQuill.getInterface(2);
var mathField;
var selectedSection = "";

var count = 0;

/**
 * Adds buttons to jQuery object
 * @param {object} object - the object that div will be appended to
 * @param {string} uuid - refernce to div that buttons will act upon
 * @param {boolean} checked - whether the inline checkbox is true
 */
var addControlButtons = function(object, uuid, checked){
  var buttonContainer = $("<div></div>")
    .addClass("button-container");

  var checked_value = checked ? "checked" : "";

  buttonContainer
    .append("<div class='control-button' ><input type='checkbox' class='control-checkbox' " + checked_value + ">inline</input></div>")
    .append("<button type='button' class='control-button move-up' onClick='moveUp(\"" + uuid + "\")'><i class='fa fa-chevron-up' aria-hidden='true'></i></button>")
    .append("<button type='button' class='control-button move-down' onClick='moveDown(\"" + uuid + "\")'><i class='fa fa-chevron-down' aria-hidden='true'></i></button>")
    .append("<button type='button' class='control-button delete' onClick='deleteBlock(\"" + uuid + "\")'><i class='fa fa-trash' aria-hidden='true'></i></button>");

  return(object.append(buttonContainer));
}

/**
 * Changes the selectedSection to is of last clicked on MathQuill equation
 * Allows toolbar actions to reference the correct equation field.
 */
var attachToolbar = function(id_value){
    selectedSection = dict_of_questions[id_value]
  }

/**
 * Adds a Mathquill equation field and block to selected div
 * @param {string} div_name - div that block will be appended to
 * @param {string} math_content - latex string is it exists
 * @param {string} is_inline - boolean for if the equation is inline
 */
var addEquationField = function(div_name, math_content, is_inline){

  var uuid = getUUID();
  var mathquill_block_id = "mathquill_block_" + uuid;
  var mathquill_text_block_id = "mathquill_text_block_" + uuid;

  var mathFieldSpan = $("<span>" + math_content + "</span>")
    .addClass("mathquill-field mq-editable-field mq-math-mode mq-editable-field")
    .attr("id", mathquill_block_id)
    .on("click",function(){
      attachToolbar(mathquill_text_block_id);
      $("#toolbar_container").css("display", "block")
    });

  var textField = $("<textarea></textarea>")
    .attr("wrap","physical")
    .attr("cols","40")
    .attr("rows","5")
    .attr("id", mathquill_text_block_id)
    .addClass("question_content_textfield")
    .addClass("mathquill_textfield")
    .css("display", "none");

  // wrap the textfield in a span
  var textSpan = $("<span></span>").append(textField);
  var outer_math_span = $("<span></span>")
    .addClass("outer_math_span")
    .append(mathFieldSpan);

  var contentDiv = $("<div></div>")
    .addClass("content-container")
    .append(outer_math_span)
    .append("<button type='button' class='equation-button' onClick='toggleTextField(\"" + mathquill_text_block_id + "\")'>Toggle TextField</button>");

  var content_field = $("<div></div>")
    .attr("id", uuid)
    .addClass("content_field")
    .addClass("math_field");

  var content_field = addControlButtons(content_field, uuid, is_inline);

  content_field.append(contentDiv)
    .append(textSpan);


  $("." + div_name).append(content_field);

  var math_field = document.getElementById(mathquill_block_id);
  var text_field = document.getElementById(mathquill_text_block_id);

  mathField = MQ.MathField(math_field, {spaceBehavesLikeTab: true,
    handlers: {
      edit: function() {
        // set the text of the textfield to the plain LaTeX
        text_field.textContent = mathField.latex();
      }
    }
  });

  dict_of_questions[mathquill_text_block_id] = mathField;

  ++count;
}

/**
 * Adds a textarea field and block to selected div
 * @param {string} div_name - div that block will be appended to
 * @param {string} content - string of content to populate textarea is it exists
 * @param {string} is_inline - boolean for if the equation is inline
 */
var addTextField = function(div_name, content, is_inline){
  var uuid = getUUID();

  var text_block_id = "text_block_" + count;
  // create the textfield
  var textField = $("<textarea>" + content + "</textarea>")
    .attr("wrap","physical")
    .attr("cols","40")
    .attr("rows","5")
    .addClass("question_content_textfield")
    .attr("id", text_block_id);

  var contentDiv = $("<div></div>")
    .addClass("content-container")
    .append(textField);

  var content_field = $("<div></div>")
    .attr("id", uuid)
    .addClass("content_field")
    .addClass("text_field");

  content_field = addControlButtons(content_field, uuid, is_inline);

  content_field.append(contentDiv);


  // add it to the field
  $("."+div_name)
    .append(content_field);

  // end
  ++count;
}

/**
 * Adds a file field and block to selected div
 * @param {string} div_name - div that block will be appended to
 */
var addImageField = function(div_name){
  var uuid = getUUID();

  var input_field = $("<input />")
    .attr("type","file")
    .addClass("fileInput")
    .attr("accept","image/*")
    .css("display","none")
    .attr("onchange","handleFiles('" + div_name + "', this.files)");

  var content_field = $("<div></div>")
    .attr("id", uuid)
    .addClass("content_field")
    .addClass("image_field")
    .css("display", "none");

  content_field = addControlButtons(content_field, uuid, false);
  content_field.append(input_field);


  $("." + div_name)
    .append(content_field);

  // get the file from the div that has been created
  var fileInput = $("." + div_name).children().last().find(".fileInput");
  // this will trigger the file upload option.
  fileInput.click()
  // once a file has been selected, the onChange will be handled.
}

/**
 * Handles the uploaded file, checks that it is an image and appends it to the respective div
 * @param {string} div_name - name of div to append to
 * @param {object} files - reference to the file objects
 */
var handleFiles = function(div_name, files){
  // add the image before uploading

  // get the last file that has been added within the block.
  var file = files[files.length - 1];
  var imageType = /^image\//;

  // check that file is of type image
  if (!imageType.test(file.type)) {
    return false;
  }

  var img = $("<img></img>")
    .addClass("uploaded-image")
    .attr("file", file);

  var contentDiv = $("<div></div>")
    .addClass("content-container")
    .append(img);

  $("."+div_name).children().last()
    .append(contentDiv)
    .css("display","flex");

  var reader = new FileReader();
  reader.onload = (function(aImg){
    return function(e) { aImg.attr("src", e.target.result); };
  })(img);
  reader.readAsDataURL(file);
}

var addExistingImageField = function(div_name, image_name, is_inline, src_path){
  var img = $("<img src=" + src_path + image_name + "></img>");

  console.log(img[0]);

  var contentDiv = $("<div></div>")
    .addClass("content-container")
    .append(img);

  var content_field = $("<div></div>")
    .attr("id", uuid)
    .addClass("content_field")
    .addClass("image_field")
    .addClass("existing-image");

  content_field = addControlButtons(content_field, uuid, is_inline);

  content_field.append(contentDiv);


  $("." + div_name)
    .append(content_field);

}

/**
 * Display or hide the textfield associated with a MathQuill field
 * @param {string} textfield_id - id of textfield
 */
var toggleTextField = function(textfield_id){
  if($("#" + textfield_id).css("display")=="none"){
    $("#" + textfield_id).css("display", "inline-block");
  }
  else{
    $("#" + textfield_id).css("display", "none");
  }
}

/**
 * Deletes a block
 */
var deleteBlock = function(uuid){
  // remove the mathquill objects if nec
  if($("#" + uuid).hasClass("math_field")){
    delete dict_of_questions["mathquill_block_" + uuid];
  }
  // remove the html
  $("#" + uuid).remove()
}

/**
 * Moves a block up in the order
 * If it is at the top, nothing will happen
 */
var moveUp = function(uuid){
  // check if there is a previous element
  var blockToMove = $("#"+uuid);
  var previousElement = blockToMove.prev();
  // JQuesy selector will never return false
  // if length === 0 then nothing has been found
  if(previousElement.length){
    previousElement.before(blockToMove);
  }
  else{
    // do nothing
  }
}

/**
 * Moves a block down in the order
 * If it is at the bottom, nothing will happen
 */
var moveDown = function(uuid){
  // check if there is a previous element
  var blockToMove = $("#"+uuid);
  var previousElement = blockToMove.next();
  // JQuesy selector will never return false
  // if length === 0 then nothing has been found
  if(previousElement.length){
    previousElement.after(blockToMove);
  }
  else{
    // do nothing
    console.log("do nothing");
  }
}

/**
 * Fetch the content from each of the blocks and images from files fields
 * Wraps data into JavaScript objects that can convert to a dict and stores the
 * images as FormData.
 */
var getContent = function(){
  data = {}
  data["name"] = $("#question_name_textfield").val()

  // used to post images to static consumption point
  var image_data = new FormData();

  // iterate through the sections
  var sections = [
    "question_content",
    "answer_explanation_content",
    "additional_information",
    "option_content_1",
    "option_content_2",
    "option_content_3",
  ]

  sections.map(function(class_name){

    var values = [];

    // get all of the content divs
    var content_fields = $("." + class_name + " > .content_field");

    $(content_fields).each(function( index ) {
      if($(this).hasClass("text_field")){
        var text = $(this).find(".question_content_textfield").val();
        var inline_boolean = $($(this) )
        // check if its checked
        var inline_boolean = $(this).find(".control-checkbox").first().is(":checked");
        values.push(
          {"text": text,
           "inline": inline_boolean,
          }
        );
      }
      else if($(this).hasClass("math_field")){
        // fetch the math content
        var mathquill_field = $(this).find(".question_content_textfield");
        // console.log(dict_of_questions[mathquill_field.attr("id")].latex());
        // check if block is inline
        var inline_boolean = $(this).find(".control-checkbox").first().is(":checked");
        values.push(
          {"latex": dict_of_questions[mathquill_field.attr("id")].latex(),
           "inline": inline_boolean,
          }
        );
      }
      else if($(this).hasClass("image_field")){
        // check whether the img exists, otherwise cancel was called
        // and the image was not put in the block
        if ($(this).has("img")){
          // check if the image already exists
          if ($(this).hasClass("existing-image")){
            console.log("It's an existing image!");
            // extract the uuid
            console.log($(this).find("img").attr("src") );
            values.push(
              { "image": $(this).find("img").attr("src").split("/").pop() }
            );
          }
          // image has just been uploaded
          else{
            // generate a uuid for the image
            var pic_uuid = getUUID();
            //  get the file type
            var files = $(this).find(".fileInput")[0].files;
            var file = files[files.length - 1]; // get the last file
            var file_suffix = file.name.split('.').pop();
            var new_file_name = pic_uuid + "." + file_suffix;
            // console.log(new_file_name);
            // add the uuid to the values array
            values.push(
              { "image": new_file_name }
            );
            // add the image to the image_data object
            image_data.append(new_file_name, file)
            // post the image to the '/file' URL
          }
        }
      }
      else{
        alert("Content Field Div does not have a type of text_field, math_field or image_field")
      }
    });

    // add the elements to data
    data[class_name] = values;
  });

  // get the correct option
  options = [
    "option_content_1",
    "option_content_2",
    "option_content_3",
  ]

  // check for a correct answer
  data["correct"] = $("input[name='correct_option']:checked").val()

  return({
    "data": data,
    "image_data": image_data,
  });
}

/**
 * Posts the images to a defined endpoint and json data to another
 * @param {string} image_endpoint - relative URL for the FormData
 * @param {string} data_endpoint - relative URL for the JSON data
 * @param {boolean} cookie_flag - whether a cookie should included in the data post
 */
var postInfo = function(image_endpoint, data_endpoint, cookie_flag){
  fetched_data = getContent();

  data=fetched_data.data;
  image_data=fetched_data.image_data;

  var data_invalid = false;

  data.name=global_question_id

  // Send the data and clean it up
  if(!data_invalid){
    var sections = [
      "question_content",
      "answer_explanation_content",
      "additional_information",
      "option_content_1",
      "option_content_2",
      "option_content_3",
    ]

    sections.map(function(class_name){
      $("."+class_name).empty();
    });
    $("#question_name_textfield").val("");
    // reset count value
    count = 0;
    // clear the array that stores mathFields
    dict_of_questions = {};

    // post the data to the server
    json_data = data

    if(cookie_flag){
    // add the CSRF token to the headers
      $.ajaxSetup({
        headers: {"X-CSRFToken": $.cookie("csrftoken")}
      });
    }

    if((image_endpoint)&&(data_endpoint)){
      $.ajax({
        url: image_endpoint,
        data: image_data,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        success: function(data){
          console.log("Images posted to server")
          // post the data to the server
          $.ajax({
            url: data_endpoint,
            type: 'POST',
            contentType:'application/json',
            data: JSON.stringify(json_data),
            dataType:'json',
            success: function(data){
              console.log("succes posting data")
              $("#subject_form_button").click();
            },
            error: function(data){
              console.log("Posting data to server went wrong!")
            },
          });
        },
        error: function(data){
          console.log("Posting images posting went wrong");
        },
      });
    }
  }
}

/**
 * Display or hide the preview bar
 */
var togglePreview = function(){
  var preview_panel = $("#preview-panel");
  var display_value = preview_panel.css("display");
  if(display_value === "block"){
    preview_panel.css("display", "none");
  }
  else{
    preview_panel.css("display", "block");
  }
}
