function update_game_odds(){
    var games = document.getElementById("game_table").getElementsByTagName("tbody")[0].getElementsByClassName('clickable');
    for (index = 0; index < games.length; index++) {
        var game_data = $(games[index]).attr('data-game')
        $.ajax({
            type: "POST",
            url: "/odds_update",
            data: { game: game_data},
            ajaxI: index, // Capture the correct value of index.
            success: function(result){
                var info_to_update = JSON.parse(result)
                var tds = games[this.ajaxI].getElementsByTagName("td")
                 $(tds[1])[0].innerHTML = info_to_update.home_spread[0] + ', ' + info_to_update.home_spread[1] + "<br>"
                 $(tds[1])[0].innerHTML += info_to_update.away_spread[0] + ', ' + info_to_update.away_spread[1]
                 $(tds[2])[0].innerHTML = info_to_update.ml[0] + "<br>" + info_to_update.ml[1]
                 $(tds[3])[0].innerHTML = info_to_update.over[0] + ', ' + info_to_update.over[1] + "<br>"
                 $(tds[3])[0].innerHTML += info_to_update.under[0] + ', ' + info_to_update.under[1]
            }
        })
    }
    setTimeout(update_game_odds, 150000); //150000
};

$(document).ready(update_game_odds);
