enchant();

$(function() {
	var game = new Core(NobOGame.sizeX, NobOGame.sizeY);
	NobOGame.setGame(game);
	var nobo = NobOGame.Game();
	nobo.start();
	
	$("#new_game").click(function() {
		if (confirm('今までの領地がすべて放棄されます。')) {
			if (confirm('よろしいですか?')) {
				location.href = '?id=' + $("#id").val() + '&pass=' + $("#pass").val() + '&mode=new_game';
			}
		}
	});
	
	$.PeriodicalUpdater('./cgi-bin/bjtest', {
		url: 'nobo_ajax.cgi',
		minTimeout: 6000,
		sendData: {
			id: $("#id").val(),
			pass: $("#pass").val(),
			log: '1'
		}
	},
	function(data) {
		$("#logDiv").html(data);
	});
});