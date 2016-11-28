/**
 * Exposes the option to fetch data from a defined endpoint
 * @param {string} data_endpoint - URL for where the data is fetched from
 * @param {string} image_root - the root that images will reference
 */
var getData = function(data_endpoint, image_root){
  console.log("getData() is being called");
  $.ajax({
    url: data_endpoint, // TODO: This needs to be passed in as an attribute
    type: 'GET',
    success: function(data){
      if(data["message"]){
        console.log(data["message"]);
      }
      else{
        console.log("populating");
        populateForm(data, image_root);
      }
    },
    error: function(data){
      alert("Fetching data from the server went wrong!")
      // TODO: handle this by preventing editing
    },
  });
}

/**
 * Adds data to the page from a JSON object of structured data
 * @param {object} data - JavaScript object containing the data to populate the fields
 * @param {string} image_root - the root that images will reference
 */
var populateForm = function(data, image_root){
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
      if(block["text"]){
        addTextField(section_name, block["text"], is_inline);
      }
      else if(block["latex"]){
        addEquationField(section_name, block["latex"], is_inline);
      }
      else if(block["image"]){
        addExistingImageField(section_name, block["image"], is_inline, image_root)
      }
      else{
        throw "Block is not defined as text, latex or image";
      }
    });
  });
  // check the correct answer
  $("#" + data["correct"]).prop("checked", true);
}
