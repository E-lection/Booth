window.onload = function(){
  var counter = document.getElementById('count-down').innerHTML;
  setInterval(function() {
    counter--;
    if(counter < 0) {
      window.location = '/';
    } else {
      document.getElementById('count-down').innerHTML = counter;
    }
  });
}
