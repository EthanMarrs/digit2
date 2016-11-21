var getUUID = function(){
  return uuid()
}

var dict_of_questions = {};
var MQ = MathQuill.getInterface(2);
var mathField;
var selectedSection = "";

var count = 0;
// create a function that creates a span, textfield and mathfield
// then add them to the array
// then add them to the document

// appends buttons that control the handling of the blocks
var addControlButtons = function(object, uuid, checked){
  var buttonContainer = $("<div></div>")
    .addClass("button-container");

  var checked_value = checked ? "checked" : "";

  buttonContainer
    .append("<div class='control-button' ><input type='checkbox' class='control-checkbox' " + checked_value + ">Make inline</input></div>")
    .append("<button type='button' class='control-button' onClick='moveUp(\"" + uuid + "\")'><i class='fa fa-chevron-up' aria-hidden='true'>Move up</i></button>")
    .append("<button type='button' class='control-button' onClick='moveDown(\"" + uuid + "\")'><i class='fa fa-chevron-down' aria-hidden='true'>Move Down</i></button>")
    .append("<button type='button' class='control-button' onClick='deleteBlock(\"" + uuid + "\")'><i class='fa fa-trash' aria-hidden='true'>Delete</i></button>");

  return(object.append(buttonContainer));
}

var attachToolbar = function(id_value){
    selectedSection = dict_of_questions[id_value]
  }

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

    // This allows added functionality
    // They will be added later
    // .append("<button type='button' class='equation-button' onClick='copyEquationField(\"" + mathquill_block_id + "\")'>Add a copy</button>");

  // add the elements to the page

  var content_field = $("<div></div>")
    .attr("id", uuid)
    .addClass("content_field")
    .addClass("math_field")
    .append(contentDiv)
    .append(textSpan);

  var content_field = addControlButtons(content_field, uuid, is_inline);

  $("." + div_name).append(content_field);

  var math_field = document.getElementById(mathquill_block_id);
  var text_field = document.getElementById(mathquill_text_block_id);
  // var otherThing = document.getElementById("other_thing_id");

  mathField = MQ.MathField(math_field, {spaceBehavesLikeTab: true,
    handlers: {
      edit: function() {
        // set the text of the textfield to the plain LaTeX
        text_field.textContent = mathField.latex();
      }
    }
  });

  // TODO Change this to mathquill block id
  dict_of_questions[mathquill_text_block_id] = mathField;

  ++count;
}

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
    .addClass("text_field")
    .append(contentDiv);

  content_field = addControlButtons(content_field, uuid, is_inline);

  // add it to the field
  $("."+div_name)
    .append(content_field);

  // end
  ++count;
}

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
    .css("display", "none")
    .append(input_field);

  content_field = addControlButtons(content_field, uuid, is_inline);

  $("." + div_name)
    .append(content_field);

  // get the file from the div that has been created
  var fileInput = $("." + div_name).children().last().find(".fileInput");
  // this will trigger the file upload option.
  fileInput.click()
  // once a file has been selected, the onChange will be handled.

  // if they hit cancel, then it will need to trigger a delete of the div/ or create a placeholder? Which you can then delete?
}

var handleFiles = function(div_name, files){
  // add the image before uploading

  // get the last file that has been added within the block.
  var file = files[files.length - 1];
  var imageType = /^image\//;

  // check that file is of type image
  if (!imageType.test(file.type)) {
    // TODO give a warning if is not an image!
    return false;
  }

  var img = $("<img></img>")
    .addClass("uploaded-image")
    .attr("file", file);

  var contentDiv = $("<div></div>")
    .addClass("content-container")
    .append(img);


  // add to the last div, which has been created already and added to the bottom
  // assumes that div is always the last one - no deletes or changes :/
  // TODO
  // Make changes so that UUID is used to append the image
  $("."+div_name).children().last()
    .prepend(contentDiv)
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
    .addClass("existing-image")
    .append(contentDiv);

  content_field = addControlButtons(content_field, uuid, is_inline);

  $("." + div_name)
    .append(content_field);

}

var toggleTextField = function(textfield_id){

  if($("#" + textfield_id).css("display")=="none"){
    $("#" + textfield_id).css("display", "inline-block");
  }
  else{
    $("#" + textfield_id).css("display", "none");
  }
}

var deleteBlock = function(uuid){
  // remove the mathquill objects if nec
  if($("#" + uuid).hasClass("math_field")){
    delete dict_of_questions["mathquill_block_" + uuid];
  }
  // remove the html
  $("#" + uuid).remove()
}

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
            console.log("AAAAAAA");
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

/*
The way this function currently works is to find all of blocks of content
For each block of content, find all of the textfields
If the textfield is linked to an eqation field,
  use the id to find the mathField object which has been stored in the dict_of_questions
Pull the content and add it to an array of strings.
*/
var postInfo = function(){
  fetched_data = getContent();

  data=fetched_data.data;
  image_data=fetched_data.image_data;

  var data_invalid = false;
  // validate the data
  /*
  if(data.name===""){
    console.log("WARNING: There is no name for the question");
    data_invalid = true;
  }
  */
  data.name=global_question_id

  /*
  if(data.question_content==""){
    console.log("NO CONTENT: question_content");
    data_invalid = true;
  }
  if(data.answer_explanation_content==""){
    console.log("NO CONTENT: answer_explanation_content");
    data_invalid = true;
  }
  if(data.option_content_1==""){
    console.log("NO CONTENT: option_content_1");
    data_invalid = true;
  }
  if(data.option_content_2==""){
    console.log("NO CONTENT: option_content_2");
    data_invalid = true;
  }
  if(data.option_content_3==""){
    console.log("NO CONTENT: option_content_3");
    data_invalid = true;
  }
  */

  // Send the data and clean it up
  if(!data_invalid){
    //  CLEAN UP
    // clear the blocks so that more content can be created
    // TODO: create a global reference for the sections - this violates DRY
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
    // END OF CLEAN UP

    // post the data to the server
    json_data = data
    // TODO - make the code optional
    // add the CSRF token to the headers
    $.ajaxSetup({
      headers: {"X-CSRFToken": $.cookie("csrftoken")}
    });

    // Check if there are images


    $.ajax({
      url: '../../../question_content/file_upload/', // TODO: This needs to be passed in as an attribute
      data: image_data,
      cache: false,
      contentType: false,
      processData: false,
      type: 'POST',
      success: function(data){
        console.log("Images posted to server")
        // post the data to the server
        $.ajax({
          url: '../../../question_content/', // TODO: This needs to be passed in as an attribute
          type: 'POST',
          contentType:'application/json',
          data: JSON.stringify(json_data),
          dataType:'json',
          success: function(data){
            console.log("succes posting data")
            // TODO: change this code
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

// wraps input in 'p' tags
var renderText = function(text){
  return $("<p></p>")
    .addClass("preview-text")
    .text(text);
}

var renderLatex = function(latex){
  var katex_span = $("<span></span>")
    .addClass("katex-span")[0];
  katex.render(latex, katex_span);

  // TODO
  // handle case where there is text as well as
  // TODO
  // handle case where the latex is nt valid
  return katex_span;
}

var renderImage = function(){
  return $("<div></div>")
    .addClass("image-placeholder")
}

// items is an array of objects that either have a key of
// "text", "latex", "image"
var renderBlock = function(items, block_name){
  // create a root jquery div
  var block = $("<div></div>")
    .addClass(block_name);

  // iterate through the items and append them
  for (var i = 0; i < items.length; ++i) {
    key = Object.keys(items[i])[0]
    switch(key){
      case "text":
        block.append(renderText(items[i][key]));
        break;
      case "latex":
        block.append(renderLatex(items[i][key]));
        break;
      case "image":
        block.append(renderImage(items[i][key]));
        break;
      default:
        console.log();
    }
    block.append($("<br />"))
  }
  return block;
}

var createPreview = function(data){
  var root_div = $("#preview-panel");

  // pull the data from the edit-panel
  fetched_data = getContent();

  data=fetched_data.data;
  image_data=fetched_data.image_data;

  console.dir(data);

  root_div.append("<h3>Question</h3>");
  // State the question
  root_div.append(renderBlock(data.question_content, "question_block"));
  // State the possible answers
  root_div.append("<h3>Options</h3>");
  root_div.append(renderBlock(data.option_content_1, "option block_1"));
  root_div.append(renderBlock(data.option_content_1, "option block_2"));
  root_div.append(renderBlock(data.option_content_1, "option block_3"));

  // add a 'submit' button that will change question section to hidden

  // add the correct answer

  //
}

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
