#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ���E��\�� Created by nanamie
#================================================


@world_summaries = (
	# ���a
	'���a', '�ɉh','�v��','���D','�\�N','����','����','�S��','�s��','��]','�[��','�ċ�','��N','�I��','��E�E','����','����','����','�E��','��','�ԉ�','�ّ�','�p�Y','�O���u','�s��ՓV','����',   '�Í�');

#================================================
&decode;
&header;
&run;
&footer;
exit;

#================================================
sub run {
	$in{world} ||= 0;
	$in{world} = 0 if $in{world} >= @world_states;

	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index">|;
		print qq|<input type="submit" value="�s�n�o" class="button1"></form>|;
	}

	print qq|<h1>$world_states[$in{world}]</h1><hr>|;
	print "���݂̐��E��� $world_states[$in{world}] �ł��B<br>";
	print "$world_summaries[$in{world}]";
}