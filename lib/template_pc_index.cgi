#================================================
# index.cgi����ڰ�(PC) Created by Merino
#================================================

#================================================
sub index {
	my($login_list, %cs_c) = @_;
	my($cook_name, $cook_pass, $cook_is_cookie) = &get_cookie;
	my $checked = $cook_is_cookie ? 'checked' : '';

	$cs_c{all} ||= 0;
	$cs_c{0}   ||= 0;
	
	my @lines = &get_countries_mes();

	my $country_html;
	$country_html .= qq|۸޲ݒ� $cs_c{all}�l [<font color="$cs{color}[0]">$cs{name}[0]</font> $cs_c{0}�l]<br>|;
	$country_html .= qq|<table cellpadding="4" class="table2">|;
	for my $i (1 .. $w{country}) {
		my $c_count = defined $cs_c{$i} ? $cs_c{$i} : 0;
		
		my($country_mes, $country_mark) = split /<>/, $lines[$i];
		$country_mark = 'non_mark.gif' if $country_mark eq '';
		$country_html .= qq|<tr><td><img src="$icondir/$country_mark"></td></td><td style="color: #333; background-color: $cs{color}[$i]; text-align: right;" nowrap><b>$cs{name}[$i]</b><br>$c_count�l<br>$cs{ceo}[$i]<br></td><td style="width:100%;">$country_mes<br></td></tr>\n|;
	}
	$country_html .= qq|</table>|;
	my $title_html = $title_img ? qq|<img src="$title_img">| : qq|<h1>$title</h1>|;

	my $login_html = '';
	if ($cs_c{all} >= $max_login) {
		$login_box_html .= qq|<br><p style="font-size: 16px; color: #FF0; font-weight: bold;">۸޲݋K����</p><p>۸޲ݐl��������܂ł��΂炭���҂����������B�g�т����۸޲݂͉\\�ł��B</p><br>|;
	}
	else {
		$login_box_html .= qq|<form method="$method" action="login.cgi" style="margin: 0; padding: 0;"><table class="table1">|;
		$login_box_html .= qq|<tr><th><tt>��ڲ԰��:</tt></th><td><input type="text" name="login_name" value="$cook_name" class="text_box1"></td></tr>|;
		$login_box_html .= qq|<tr><th><tt>�߽ܰ��:</tt></th><td><input type="password" name="pass" value="$cook_pass" class="text_box1"></td></tr>|;
		$login_box_html .= qq|<tr><td colspan="2"><input type="checkbox" name="is_cookie" value="1" $checked> <tt>���񂩂���͏ȗ�</tt></th></tr>|;
		$login_box_html .= qq|</table><p><input type="submit" value="[> ���O�C��" class="button_login"></p></form>|;
	}
	
	print <<"EOM";
<style type="text/css">
<!--
body { margin: 0; padding: 0; }
form { margin: 0; padding: 7px; }
-->
</style>
<div align="center">
<table width="840" border="0" cellpading="0" cellspacing="0" class="top_box">
<tr>
	<td valign="top">
		<div class="login_list">
			$login_list
		</div>
		<br>$country_html<br>
	</td>
	<td valign="top" align="center">
		<div class="login_box">
			Chrome�̃f�[�^�Z�[�o�[�𖳌��ɂ��Ȃ��ƃA�N�Z�X�ł��܂���
			$login_box_html
		</div>
		<div align="left" style="padding: 0.2em 2em;">
			<p><a href="readme.html" class="link1">[> Readme�@</a></p>
			<p><a href="http://www13.atwiki.jp/blindjustice/" class="link1">[> �������@</a></p>
			<p><a href="http://www43.atwiki.jp/bjkurobutasaba/" class="link1">[> wiki�@</a></p>
			<p class="text_small">���₷��O�ɕK���ǂނ���!</p>
			<p><a href="new_entry.cgi" class="link1">[> �V�K�o�^</a></p>
			<p class="text_small">�o�^�O�ɐ������K��!</p>
		</div>
		
		<hr style="border: 1px dashed #CCC;">
		<form action="./html/0.html">
			<input type="submit" value="��ڲ԰�ꗗ" class="button1">
			<br><span class="text_small">�������ƂɍX�V</span>
		</form>
		<form method="$method" action="legend.cgi">
			<input type="submit" value="�I�v�̐Δ�" class="button1">
			<br><span class="text_small">$world_name�嗤�̗��j</span>
		</form>
		<form method="$method" action="contest.cgi">
			<input type="submit" value="��ýĉ��" class="button1">
			<br><span class="text_small">�˔\\�̗�</span>
		</form>
		<form method="$method" action="sales_ranking.cgi">
			<input type="submit" value="�����ݷݸ�" class="button1">
			<br><span class="text_small">$sales_ranking_cycle_day�����ƂɍX�V</span>
		</form>
		<form method="$method" action="player_ranking.cgi">
			<input type="submit" value="�p�l�ݷݸ�" class="button1">
			<br><span class="text_small">1�����ƂɍX�V</span>
		</form>
		<form method="$method" action="main_player.cgi">
			<input type="submit" value="��͕\\ " class="button1">
		</form>
		<form method="$method" action="main_player2.cgi">
			<input type="submit" value="��͕\\2 " class="button1">
		</form>
		<form method="$method" action="year_player_ranking.cgi">
			<input type="submit" value="��N�ݷݸ�" class="button1">
			<br><span class="text_small">1�N���ƂɍX�V</span>
		</form>
		<form method="$method" action="year_player_ranking_country.cgi">
			<input type="submit" value="�����ݷݸ�" class="button1">
			<br><span class="text_small">1�N���ƂɍX�V</span>
		</form>
		<form method="$method" action="pop_ranking_gold.cgi">
			<input type="submit" value="�l�C�ݷݸ�(��)" class="button1">
		</form>
		<form method="$method" action="pop_ranking_middle.cgi">
			<input type="submit" value="�l�C�ݷݸ�(��)" class="button1">
		</form>
		<form method="$method" action="./news.cgi">
			<input type="submit" value="�ߋ��̉h��" class="button1">
			<br><span class="text_small">�ŋ߂̏o����</span>
		</form>
		<form method="$method" action="library.cgi">
			<input type="submit" value="�}����" class="button1">
			<br><span class="text_small">��l�̒m�b</span>
		</form>
		<form method="$method" action="shop_big_data.cgi">
			<input type="submit" value="����" class="button1">
			<br><span class="text_small">�A�C�e�����i�̐���</span>
		</form>
		<a href="https://github.com/tamochu/bj_buu">source github�i�厖�Ȃ��Ƃ͖����A�����Ă���A�����������j</a>
<br>
		<hr style="border: 1px dashed #CCC;">
		<form action="$home">
			<input type="submit" value="�g�n�l�d" class="button1">
		</form>
		<form method="$method" action="reset_player.cgi">
			<input type="submit" name="name" value="ؾ�ď���" class="button_s">
		</form>
		<form method="$method" action="search_player.cgi">
			<input type="text" name="search_name" value=""><input type="submit" value="..." class="button_s">
		</form>
	</td>
</tr>
<tr>
	<td colspan="2">
		<div class="footer">
			���[ $w{player}/$max_entry�l ]�@��ڲ԰�ۑ����� $auto_delete_day��(1�����Lv.1��1��)<br>
			��{�S������ $GWT���@���^ $salary_hour���Ԗ��@�N��̔C�� $reset_ceo_cycle_year�N����
		</div>
	</td>
</tr>
<tr>
	<td colspan="2">
		<div class="footer">
			�S�g�ы@��Ή��F�g�т���PC�Ɠ���URL�ɱ������邾���B<br>
			��ڲ԰���쐬�����摜�E÷�ē��́A���쌠�E�ё������ɂ��Ė@�ߏ�̋`���ɏ]���A��ڲ԰�̎��ȐӔC�ɂ����ēo�^�E�f�ڂ������̂Ƃ��܂��B<br>
		</div>
	</td>
</tr>
</table>

</div>
EOM
}



1; # �폜�s��
