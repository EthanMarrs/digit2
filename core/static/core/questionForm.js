var array_of_questions = {};
var MQ = MathQuill.getInterface(2);
var mathField;

var count = 0;
// create a function that creates a span, textfield and mathfield
// then add them to the array
// then add them to the document
var addEquationField = function(div_name, math_content){

  var mathquill_block_id = "mathquill_block_" + count;
  var mathquill_text_block_id = "mathquill_text_block_" + count;

  var mathFieldSpan = $("<span>" + math_content + "</span>")
    .addClass("mathquill-field mq-editable-field mq-math-mode mq-editable-field")
    .attr("id", mathquill_block_id);

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
    .append(mathFieldSpan)
    .append("<button type='button' onClick='toggleTextField(\"" + mathquill_text_block_id + "\")'>Toggle TextField</button>")
    .append("<button type='button' onClick='copyEquationField(\"" + mathquill_block_id + "\")'>Add a copy</button>");

  // add the elements to the page

  var content_field = $("<div></div>")
    .addClass("content_field")
    .addClass("math_field")
    .append(outer_math_span)
    .append("<br />")
    .append(textSpan);

  $(div_name).append(content_field);

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

  array_of_questions[mathquill_text_block_id] = mathField;

  ++count;
}

// add a copy of the existing equation and add it beneath the existing equation
var copyEquationField = function(div_name){
  // create a new equation by getting the content of the
}

var addTextField = function(div_name){
  var text_block_id = "text_block_" + count;
  // create the textfield
  var textField = $("<textarea></textarea>")
    .attr("wrap","physical")
    .attr("cols","40")
    .attr("rows","5")
    .addClass("question_content_textfield")
    .attr("id", text_block_id);

  var content_field = $("<div></div>")
    .addClass("content_field")
    .addClass("text_field")
    .append(textField);

  // add it to the field
  $("."+div_name)
    .append(content_field);

  // end
  ++count;
}

var addImageField = function(div_name){
  var input_field = $("<input />")
    .attr("type","file")
    .addClass("fileInput")
    .attr("accept","image/*")
    .css("display","none")
    .attr("onchange","handleFiles('" + div_name + "', this.files)");

  var content_field = $("<div></div>")
    .addClass("content_field")
    .addClass("image_field")
    .css("display", "none")
    .append(input_field);

  $("." + div_name)
    .append(content_field);

  // get the file from the div that has been created
  var fileInput = $("." + div_name).children().last().find(".fileInput");
  // this will trigger the file upload option.
  fileInput.click()
  // once a file has been selected, the onChange will be handled.

  // if they hit cancel, then it will need to trigger a delete of the div/ or create a placeholder? Which you can then delete?
}

handleFiles = function(div_name, files){
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

  // add to the last div, which has been created already and added to the bottom
  // assumes that div is always the last one - no deletes or changes :/
  $("."+div_name).children().last()
    .append(img)
    .css("display","inline");

  var reader = new FileReader();
  reader.onload = (function(aImg){
    return function(e) { aImg.attr("src", e.target.result); };
  })(img);
  reader.readAsDataURL(file);
}

var toggleTextField = function(textfield_id){

  if($("#" + textfield_id).css("display")=="none"){
    $("#" + textfield_id).css("display", "inline-block");
  }
  else{
    $("#" + textfield_id).css("display", "none");
  }
}

/*
The way this function currently works is to find all of blocks of content
For each block of content, find all of the textfields
If the textfield is linked to an eqation field,
  use the id to find the mathField object which has been stored in the array_of_questions
Pull the content and add it to an array of strings.
*/
var postInfo = function(){
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
        values.push(
          {"text": text}
        );
      }
      else if($(this).hasClass("math_field")){
        // fetch the math content
        var mathquill_field = $(this).find(".question_content_textfield");
        // console.log(array_of_questions[mathquill_field.attr("id")].latex());
        values.push(
          { "latex": array_of_questions[mathquill_field.attr("id")].latex() }
        );
      }
      else if($(this).hasClass("image_field")){
        // check whether the img exists, otherwise cancel was called and the image was not put in the block
        if ($(this).has("img")){
          // generate a uuid for the image
          var pic_uuid = uuid.v4()
          //  get the file type
          var files = $(this).find(".fileInput")[0].files;
          var file = files[files.length - 1];
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
      else{
        alert("Content Field Div does not have a type of text_field, math_field or image_field")
      }
    });

    // add the elements to data
    data[class_name] = values;
  });

  var data_invalid = false;
  // validate the data
  /*
  if(data.name===""){
    console.log("WARNING: There is no name for the question");
    data_invalid = true;
  }
  */
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

  // Send the data and clean it up
  if(!data_invalid){
    //  CLEAN UP
    // clear the blocks so that more content can be created
    sections.map(function(class_name){
      $("."+class_name).empty();
    });
    $("#question_name_textfield").val("");
    // reset count value
    count = 0;
    // clear the array that stores mathFields
    array_of_questions = {};

    // post the data to the server

    // add the CSRF token to the headers
    $.ajaxSetup({
      headers: {"X-CSRFToken": $.cookie("csrftoken")}
    });

    $.ajax({
      url: "../../../question_content/",
      type: 'POST',
      contentType:'application/json',
      data: JSON.stringify(data),
      dataType:'json',
      success: function(data){
        $.ajax({
          url: '../../../question_content/file_upload/',
          data: image_data,
          cache: false,
          contentType: false,
          processData: false,
          type: 'POST',
          success: function(data){
            // alert("Images posted to server")
          },
          error: function(data){
            alert("Posting images posting went wrong");
          },
        });
      },
      error: function(data){
        alert("Posting data to server went wrong!")
      },
    });
    console.dir(image_data);
  }
}
