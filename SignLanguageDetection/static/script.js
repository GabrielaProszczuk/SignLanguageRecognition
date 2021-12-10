var container = document.querySelector('.container');
var start_button = document.querySelector('.dis_start');
var stop_button = document.querySelector('.dis_stop');

var container_displayed;

if(container.style.display == "none"){
  container_displayed = false;
}else{
  container_displayed = true;
}


start_button.onclick = function() {
  if (container_displayed == false) {
    container.style.display = "block";
    start_button.className = 'btn btn-secondary'
    stop_button.className = 'btn btn-danger'
    container_displayed = true;
  }
}

stop_button.onclick = function() {
  if (container_displayed == true) {
    container.style.display = "none";
    stop_button.className = 'btn btn-secondary'
    start_button.className = 'btn btn-danger'
    container_displayed = false;
  }
}