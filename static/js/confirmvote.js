var keycode_enter = 13;

function code(e) {
  e = e || window.event;
  return(e.keyCode || e.which);
}

window.onload = function(){

  // If the user presses a button
  document.onkeypress = function(e){
      var keycode = code(e);

      // If this is the enter key we say they've voted
      if (keycode === keycode_enter) {
        $.ajax({
          type: "POST",
          url: "/confirm-vote",
          contentType: 'application/json;charset=UTF-8',
          data: JSON.stringify({
            "confirm": 1
          }),
          success: function(data) {
            window.location.replace('/youve-voted');
          },
          error: function(e) {
            alert("Error Occurred")
          },
        });
      } else {
        $.ajax({
          type: "POST",
          url: "/confirm-vote",
          contentType: 'application/json;charset=UTF-8',
          data: JSON.stringify({
            "confirm": 0
          }),
          success: function(data) {
            // The voter gets to re choose candidate therefore redirecting to cast-vote page
            window.location.replace('/cast-vote');
          },
          error: function(e) {
            alert("Error Occurred")
          },
        });
      }
  };
};
