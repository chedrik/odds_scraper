function update_game_styling() {
    for (var table = 1; table <= 2; table++) { // update for changed & steam tables
        var table_string = "game_table" + table;
        if (document.getElementById(table_string)) { // both tables may not be there
            var games = document.getElementById(table_string).getElementsByTagName("tbody")[0].getElementsByClassName('clickable');
            for (index = 0; index < games.length; index++) {
                var game_data = $(games[index]).attr('data-game')
                $.ajax({
                    type: "POST",
                    url: "/steam_update",
                    data: { game: game_data},
                    ajaxI: index, // Capture the correct value of index.
                    success: function(result){
                        var info_to_update = JSON.parse(result)
                        var tds = games[this.ajaxI].getElementsByTagName("td")
                        if (info_to_update.change_vector[0] || info_to_update.change_vector[1] || info_to_update.steam_vector[0]) {
                            $(tds[1])[0].style.backgroundColor = "lime";
                        }
                        if (info_to_update.change_vector[2] || info_to_update.change_vector[3] || info_to_update.steam_vector[1]) {
                            $(tds[2])[0].style.backgroundColor = "lime";
                        }
                        if (info_to_update.change_vector[4] || info_to_update.change_vector[5] || info_to_update.steam_vector[2]) {
                            $(tds[3])[0].style.backgroundColor = "lime";
                        }
                    }
                })
            }
        }
    }
    setTimeout(update_game_styling, 150000); //150000
};

$(document).ready(update_game_styling);