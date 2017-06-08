window.onload = function(){
  var counter = document.getElementById('count-down');
  setInterval(function() {
    counter--;
    if(counter < 0) {
      window.location.replace('/');
    } else {
      document.getElementById('count-down').innerHTML = counter;
    }
  }, 5000);
}
