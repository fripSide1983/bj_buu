enchant();

$(function() {
	var game = new Core(NobOGame.sizeX, NobOGame.sizeY);
	NobOGame.setGame(game);
	var nobo = NobOGame.Game();
	nobo.start();
	
	$("#new_game").click(function() {
		if (confirm('���܂ł̗̒n�����ׂĕ�������܂��B')) {
			if (confirm('��낵���ł���?')) {
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