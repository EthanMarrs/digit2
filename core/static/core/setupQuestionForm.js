/**
 * Returns a jQuery object - a button that fires the addEquationField function when clicked
 * @param {string} class_name - the class of the object associated with addEquationField button
 */
var create_add_equation_button = function(class_name){
  return $("<button></button>")
    .attr("type", "button")
    .addClass("create-block-buttons")
    .html("Add Equation")
    .attr("onClick",
          "addEquationField('" + class_name + "', '')");
}

/**
 * Returns a jQuery object - a button that fires the addTextField function when clicked
 * @param {string} class_name - the class of the object associated with addTextField button
 */
var create_add_text_button = function(class_name){
  return $("<button></button>")
    .attr("type", "button")
    .addClass("create-block-buttons")
    .html("Add Text")
    .attr("onClick",
          "addTextField('" + class_name + "','',false)");
}

/**
 * Returns a jQuery object - a button that fires the addImageField function when clicked
 * @param {string} class_name - the class of the object associated with addImageField button
 */
var create_add_image_button = function(class_name){
  return $("<button></button>")
    .attr("type", "button")
    .addClass("create-block-buttons")
    .html("Add Image")
    .attr("onClick",
          "addImageField('" + class_name + "')");
}

/**
 * for each item passed into the array,
 * a div is created with that string used as the class of that div
 * the resulting html is returned
 */
var setupToolbar = function(){
  console.log("Running Setup");

  var root_div = $("#edit-panel").addClass("panel");
  // TODO: need to make this optional
  $("#preview-panel").addClass("panel");

  /** This function iterates through the array */
  var createContentSections = function(array, is_option){
    var parentDiv = $("<div></div>");

    array.forEach(function(value, index){
      var class_name = value[0];
      var heading_name = value[1]

      var heading = $("<h4>" + heading_name + "</h4>")

      var content_block = $("<div></div>")
        .addClass(value[0])
      if(is_option){
        content_block.addClass("is_option")
          .append("<div class='option-Dive' >Correct<input type = 'radio' name = 'correct_option' id = '" + class_name + "' value = '" + class_name + "' /></div>")
      }

      var add_equation_button = create_add_equation_button(class_name);

      var add_text_button = create_add_text_button(class_name);

      var add_image_button = create_add_image_button(class_name);

      var button_console = $("<div></div>")
        .addClass("create-block-buttons-container");

      button_console
        .append(add_equation_button)
        .append(add_text_button)
        .append(add_image_button);

      parentDiv
        .append(heading)
        .append(content_block)
        .append(button_console);

    })

    return parentDiv.children();
  };

  var question_sections = [
    ["question_content", "Question Content"],
    ["answer_explanation_content", "Answer Explanation"],
    ["additional_information", "Additional Information"],
  ]
  var option_sections = [
    ["option_content_1", "Option 1"],
    ["option_content_2", "Option 2"],
    ["option_content_3", "Option 3"],
  ]

  // add "question" h3
  root_div.append("<h2>Question</h2>"); //.append('Question Name:<input id="question_name_textfield" type="text" name="name" size="40"/><br/>')
  // append the 3 sections of the question
  root_div.append(createContentSections(question_sections, false));
  // add "options" h3
  root_div.append("<h2 id='edit_panel_option_heading'>Options</h2>")
  // add the 3 option sections
  root_div.append(createContentSections(option_sections, true));

  root_div.append("<br />")
  root_div.append("<br />")

  // TODO: make the submit button optional
  // add the submit button
  // root_div.append("<button type='button' class='create-block-buttons' onClick=>Submit</button>")

  // add the preview button
  // hide the preview pane
  var togglePreviewButton = $("<button>SEE PREVIEW</button>")
    .attr("type","button")
    .addClass("toggle-preview-button")
    .attr("onClick", "togglePreview()");
  // type='button' class='create-block-buttons' onClick='togglePreview()'
  $(".submit-row").prepend(togglePreviewButton);
}
