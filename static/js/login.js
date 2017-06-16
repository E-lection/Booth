window.onload = function() {
  document.getElementById('loginform').onkeypress = function(e) {
    var key = e.charCode || e.keyCode || 0;
    var target = e.target;
    // If they are in the username box we dont submit the form
    if (key === 13 && target.id === 'username-input') {
      e.preventDefault();
      document.getElementById('password-input').focus();
    }
  }
}
