#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ��ڲ԰ؾ�ď��� Created by Merino
#================================================

&decode;
&header;
&run;
&footer;
exit;


#================================================
sub run {
	&refresh_player if defined $in{login_name} && defined $in{pass};

	print <<"EOM";
<form action="$script_index">
	<input type="submit" value="�s�n�o" class="button1">
</form>

<h2>��ڲ԰ؾ�ď���</h2>

<div class="mes">
	<ul>
		<li>��ʂɉ����\\������Ȃ��Ȃ��Ă��܂���
		<li>�ςȖ���ٰ�߂Ɋׂ��Ă��܂����Ȃǂً̋}����
		<li>���̏����͖{���ɂǂ����悤���Ȃ��Ȃ������ȊO�g�p���Ȃ��悤��!
		<li>�܂��́A�񎟔�Q�O����Q�ɂȂ�Ȃ��悤�Ɍf���Ȃǂɕ񍐂��邱��
		<li>�������Ă��āA�ǂ����ݸނł����Ȃ��Ă��܂����̂��o�O�������e���ڂ����񍐂��邱��
		<li><font color="#FF0000">�g�p����è�F�ð���޳݁A$shogos[1][0]�̏̍��A$GWT���S��</font>
		<li>�S���ł̋~����S����Ԃ�����������̂ł͂Ȃ��̂Œ���!
	</ul>
</div>
<br>
<form method="$method" action="reset_player.cgi">
<table class="table1">
	<tr><th><tt>��ڲ԰��:</tt></th><td><input type="text" name="login_name" class="text_box1"></td></tr>
	<tr><th><tt> �߽ܰ��:</tt></th><td><input type="password" name="pass" class="text_box1"></td></tr>
</table>
<p><input type="submit" value="ؾ��" class="button_s"></p>
</form>
EOM
}

# =========================================================
# ��ʂ��\������Ȃ��A�n�}�����ꍇ�Ɏg�p(��������ُ̈�װ�̎�)
# �Ǘ���ʂ�ؾ�Ă�����è����������
sub refresh_player {
	&read_user;
	
	if ($m{lib}) {
		$m{lib} = $m{tp} = '';
		for my $k (qw/max_hp max_mp at df mat mdf ag lea cha/) {
			$m{$k} = int($m{$k} * 0.9) if $m{$k} > 5;
		}
		&wait;
		$m{shogo} = $shogos[1][0];
		
		&write_user;
		
		&error("$m{name}��ؾ�ď��������܂���<br>");
	}
	else {
		&error('���ł�ؾ�ď���������Ă��܂�');
	}
}

