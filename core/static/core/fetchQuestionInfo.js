
var fetchQuestionInfo = function(){
  // fetch the content
  getData()

}

var getData = function(){
  console.log("getData() is being called");
  $.ajax({
    url: '../../../question_content/' + '?question_id=' + global_question_id, // TODO: This needs to be passed in as an attribute
    type: 'GET',
    success: function(data){
      console.dir(data);
      if(data["message"]){
        console.log(data["message"]);
      }
      else{
        console.log("populating");
        populateForm(data);
      }
    },
    error: function(data){
      alert("Fetching data from the server went wrong!")
      // TODO: handle this by preventing editing
    },
  });
}

/*
Accepts Javascript object of data for form
Returns: Nothing
*/
var populateForm = function(data){
  var sections = [
    "question_content",
    "answer_explanation_content",
    "additional_information",
    "option_content_1",
    "option_content_2",
    "option_content_3",
  ]
  sections.map(function(section_name){
    data[section_name].map(function(block){
      is_inline = block["inline"]; // evals to true or false
      console.log(block);
      if(block["text"]){
        addTextField(section_name, block["text"], is_inline);
      }
      else if(block["latex"]){
        addEquationField(section_name, block["latex"], is_inline);
      }
      else if(block["image"]){
        console.log("There's an existing image!");
        addExistingImageField(section_name, block["image"], is_inline, "/media/optimised_media/")
      }
      else{
        throw "Block is not defined as text, latex or image";
      }
    });
  });
  // check the correct answer
  $("#" + data["correct"]).prop("checked", true);
}
// populate the question content

// populate the answer content

// populate the additional info block

// for each quesiton, populate the block

// iterate function
// if it's text or latex, create the latex
// handle it differently if it's an image
