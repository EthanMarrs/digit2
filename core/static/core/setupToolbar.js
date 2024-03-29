/**
 * Called when a toolbar button is pressed
 * Calls the MathQuill API
 * The correct MathQuill object is kept in the selectedSection var
 */
var addMathContent = function(command_type, command){
  // get the MathField object in question

  if(command_type === "keystroke"){
    selectedSection.typedText(command)
    selectedSection.keystroke('Enter')
    selectedSection.focus()
  }
  else if(command_type === "cmd"){
    selectedSection.cmd(command)
    selectedSection.focus()
  }
}

// The structure of the toolbar
// as well as the commands
buttons_info = [
  {name:"Frequently Used",
   content:[
    {button_content:"x^{\\square}", command_type:"keystroke", command:"^"},
    {button_content:"\\sqrt{ x }", command_type:"cmd", command:"\\sqrt"},
    {button_content:"\\sqrt[y]{ x }", command_type:"keystroke", command:"\\\\nthroot"},
    {button_content:"\\times", command_type:"cmd", command:"\\times"},
    {button_content:"x^{\\circ}", command_type:"keystroke", command:"^\\\\circ"},
   ],
  },
  {name:"Algebra",
   content:[
      {button_content:"\\frac{\\square}{\\square}", command_type:"cmd", command:"\\\\frac"},
    ],
  }
]

/**
 * Iterates through buttons_info
 * Creates the buttons and tabs that they exist in
 */
var addToolbarButtons = function(){
  console.log("boop!");
  var tab_count = 1
  buttons_info.map(function(tab){
    var tab_div = $("<section></section>").attr("id", "content" + tab_count).addClass("tab-content");
    ++tab_count;
    // tab_content = tab.content;
    tab.content.map(function(button_info){
      var button = $("<div onClick=\"addMathContent('" + button_info.command_type + "', '" + button_info.command + "')\"></div>")
        // .click(addMathContent(button_info.command_type, button_info.command))
        .append(katex.renderToString(button_info.button_content))
        .addClass("toolbar-button");
      tab_div.append(button);
    })
    $("#toolbar_container").append(tab_div);
  })
  var toolbar_quit_section = $("<button>X</button>")
    .attr("id", "toolbar_quit")
    .on("click", function(){
      $("#toolbar_container").css("display", "none")
    });

  $("#toolbar_container").append(toolbar_quit_section);
}
