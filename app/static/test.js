
$(document).ready(function(){
$('button[id^="game"]').unbind("click").bind('click', function(event) {
  if(!$('tr[id^="collapse"]').hasClass('collapse in')){
    console.log($(this).attr('id'));
  }

//  return false;
});
});

