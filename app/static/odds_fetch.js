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
                for (td_i = 1; td_i < tds.length; td_i++) {
                    $(tds[td_i])[0].innerHTML = ////// HELP ////////
                   {{ make_odds_pretty(game.home_spread_cur[0]) }}, {{ make_odds_pretty(game.home_spread_cur[1]) }} <br>  {{ make_odds_pretty(game.away_spread_cur[0]) }}, {{ make_odds_pretty(game.away_spread_cur[1]) }}
                }
            }
        })
    }
    setTimeout(update_game_odds, 150000); //150000
};

$(document).ready(update_game_odds);
