(function(){
  console.log("Running");

  var root_div = $("#edit-panel");

  /*
    for each item passed into the array,
    a div is created with that string used as the class of that div
    the resulting html is returned
  */
  var createContentSections = function(array){
    var parentDiv = $("<div></div>")
      .addClass("boop");

    array.forEach(function(value, index){
      var class_name = value[0];
      var heading_name = value[1]

      var heading = $("<h4>" + heading_name + "</h4>")

      var content_block = $("<div></div>")
        .addClass(value[0])

      var add_equation_button = $("<button></button>")
        .attr("type", "button")
        .html("Add Equation")
        .attr("onClick",
              "addEquationField('." + class_name + "', '')")
      var add_text_button = $("<button></button>")
        .attr("type", "button")
        .html("Add Text")
        .attr("onClick",
              "addTextField('" + class_name + "')")
      var add_image_button = $("<button></button>")
        .attr("type", "button")
        .html("Add Image")
        .attr("onClick",
              "addImageField('" + class_name + "')")
      var button_console = $("<span></span>")

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
  root_div.append("<h3>Question</h3>")
  // append the 3 sections of the question
  root_div.append(createContentSections(question_sections));
  // add "options" h3
  root_div.append("<h3>Options</h3>")
  // add the 3 option sections
  root_div.append(createContentSections(option_sections));

})();
