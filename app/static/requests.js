$(document).ready(function(){  // waits for document to be loaded before binding
    $('button[id^="game"]').unbind("click").bind('click', function(event) {  // unbind/bind ensures only 1 click handler
      if ($(this).attr('clicked') != 'true') { // set click state attribute, enables multiple plots to be done at once
          $(this).attr('clicked', true)
      } else {
          $(this).attr('clicked', "")
      }
      if($(this).attr('clicked') == 'true') { // only build plot on click -> expand
        var words = $(this).attr('id').split(' ');
        $.ajax({
            type: "POST",
            url: "/plot",
            data: { game: $(this).attr('data-game')},
            success: function(result){
                // embed_item appends plots rather than replacing, so we need to delete the older plot
                var plots = document.getElementById('span ' + words[1]).getElementsByClassName("bk-widget bk-layout-fixed");
                if (plots.length > 0){
                    plots[0].remove()
                }
                Bokeh.embed.embed_item(JSON.parse(result), 'span ' + words[1]);
             }
        });
      }
    });
});
