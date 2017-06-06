var keycode_to_number = { 49:1, 50:2, 51:3, 52:4, 53:5, 54:6, 55:7, 56:8, 57:9 }
var keycode_to_numpad = { 97:1, 98:2, 99:3, 100:4, 101:5, 102:6, 103:7, 104:8, 105:9 }

var keycode_enter = 13;

function code(e) {
  e = e || window.event;
  return(e.keyCode || e.which);
}

window.onload = function(){

  // ID of what is currently selected
  var current_selected = "";

  // If the user presses a button
  document.onkeypress = function(e){
      var keycode = code(e);

      // If they press a number that we know
      if (keycode_to_number[keycode]) {
        num_selected = keycode_to_number[keycode].toString();
        // Check if this is an option to vote for
        if (document.getElementById(num_selected)) {

          document.getElementById("cast-vote").style.display = 'block';

          // Uncheck the thing that is currently selected
          if (document.getElementById(current_selected)) {
            document.getElementById(current_selected).style.backgroundColor = "#dee0e2";
            document.getElementById(current_selected).style.color = "#0b0c0c";
          }

          // Colour in the newly selected thing
          document.getElementById(num_selected).style.backgroundColor = "#005ea5";
          document.getElementById(num_selected).style.color = "#fff";
          current_selected = num_selected;
        }
      }

      // If they press the enter keyCode
      if (keycode === keycode_enter && current_selected != "") {
        alert("You are going to vote for " + document.getElementById(current_selected).textContent);
      }
  };
};
