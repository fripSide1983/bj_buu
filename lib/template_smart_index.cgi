#================================================

# index.cgi����ڰ�(�X�}�z) Created by Merino

#================================================



#================================================

sub index {
	my($login_list, %cs_c) = @_;
	my($cook_name, $cook_pass, $cook_is_cookie) = &get_cookie;
	my $checked = $cook_is_cookie ? 'checked' : '';

	my $login_box_html = '';
	if ($cs_c{all} >= $max_login) {
		$login_box_html .= qq|<br><p style="font-size: 16px; color: #FF0; font-weight: bold;">۸޲݋K����</p><p>۸޲ݐl��������܂ł��΂炭���҂����������B�g�т����۸޲݂͉\\�ł��B</p><br>|;
	}
	else {
		$login_box_html .= qq|<form method="$method" action="login.cgi" style="margin: 0 auto; padding: 0;"><table class="table1" style="margin:0 auto;height:68px;">|;
		$login_box_html .= qq|<tr><th style="font-family: monospace;">��ڲ԰��:</th><td><input type="text" name="login_name" value="$cook_name" class="text_box1"></td><td rowspan="3"><input type="submit" value="���O�C��" class="button_login"></td></tr>|;
		$login_box_html .= qq|<tr><th style="font-family: monospace;">�߽ܰ��:</th><td><input type="password" name="pass" value="$cook_pass" class="text_box1"></td></tr>|;
		$login_box_html .= qq|<tr><td colspan="2" style="text-align:center;"><input type="checkbox" id="cookie" name="is_cookie" value="1" $checked><label for="cookie">���񂩂���͏ȗ�</label></th></tr>|;
#		$login_box_html .= qq|<tr><td colspan="2" style="font-family: monospace;"><input type="submit" value="���O�C��" class="button_login"></th></tr>|;
		$login_box_html .= qq|</table></form>|;
	}

	my $entry_box_html = '<div class="entry_box_s">';
		$entry_box_html .= qq|<form action="readme.html">\n<input type="submit" value="Readme" class="navi_button" style="">\n</form>|;
		$entry_box_html .= qq|<form action="http://www13.atwiki.jp/blindjustice/.html">\n<input type="submit" value="������" class="navi_button" style="">\n</form>|;
		$entry_box_html .= qq|<form action="http://www43.atwiki.jp/bjkurobutasaba/">\n<input type="submit" value="Wiki" class="navi_button" style="">\n</form>|;
		$entry_box_html .= qq|<br><form action="new_entry.cgi" class="new_entry">\n<input type="submit" value="�V�K�o�^" class="navi_button" style="width:100% !important;">\n</form></div>|;


	my @navigator = (
		['Readme', 'readme.html'],
		['������', 'http://www13.atwiki.jp/blindjustice/'],
		['Wiki', 'http://www43.atwiki.jp/bjkurobutasaba/'],
		['�V�K�o�^', 'new_entry.cgi'],
		['��ڲ԰�ꗗ', 'players.cgi'],
		['�I�v�̐Δ�', 'legend.cgi'],
		['���l�ݷݸ�', 'sales_ranking.cgi'],
		['��ýĉ��', 'contest.cgi'],
		['�ߋ��̉h��', 'news.cgi'],
#		['HOME', "$home_m"], # �z�[���Ƀz�[���{�^���v��Ȃ��ˁH
#		['ؾ�ď���', 'reset_player.cgi'], # �ʘg
		['�p�l�ݷݸ�', 'player_ranking.cgi'],
		['��͕\\', 'main_player.cgi'],
		['��͕\\2', 'main_player2.cgi'],
		['��N�ݷݸ�', 'year_player_ranking.cgi'],
		['�����ݷݸ�', 'year_player_ranking_country.cgi'],
		['�l�C�ݷݸ�(��)', 'pop_ranking_gold.cgi'], # �f�[�^�Ȃ�
		['�l�C�ݷݸ�(��)', 'pop_ranking_middle.cgi'], # �f�[�^�Ȃ�
		['�}����', 'library.cgi'],
		['����', 'shop_big_data.cgi'],
		['�摜�f����', '../upbbs/imgboard.cgi'],
#		['��~ɱ���', 'CatasoApp-release-signed.apk'], # �t�@�C�������炱������Ȃ��Ƃ��āA�܂��t�@�C�����Ȃ�
#		['', ''],
	);

	my $navi_html = '<div class="navi">';
	$navi_html .= qq|<form action="$navigator[0][1]">\n<input type="submit" value="$navigator[0][0]" class="navi_button">\n</form>|;
	$navi_html .= qq|<form action="$navigator[1][1]">\n<input type="submit" value="$navigator[1][0]" class="navi_button">\n</form>|;
	$navi_html .= qq|<form action="$navigator[2][1]">\n<input type="submit" value="$navigator[2][0]" class="navi_button">\n</form><br>|;
	$navi_html .= qq|<form action="$navigator[3][1]" style="width:100% !important;">\n<input type="submit" value="$navigator[3][0]" class="navi_button" style="width:240px;">\n</form><br>|;
	for $i (4 .. $#navigator) {
		$navi_html .= qq|<form action="$navigator[$i][1]">\n<input type="submit" value="$navigator[$i][0]" class="navi_button">\n</form>|;
#		if ($i > 3) {
		if ($i < $#navigator) {
			$navi_html .= qq|<br class="smart_br">| if ($i-3) % 3 == 0;
			$navi_html .= qq|<br class="tablet_br">| if ($i-3) % 5 == 0;
		}
#		}
#		else {
#			$navi_html .= qq|<br>| if $i > 1;
#		}
	}
	$navi_html .= '</div>';

	$cs_c{all} ||= 0;
	$cs_c{0}   ||= 0;

	my @lines = &get_countries_mes();

	my $country_html;
	$country_html .= qq|۸޲ݒ� $cs_c{all}�l [<font color="$cs{color}[0]">$cs{name}[0]</font> $cs_c{0}�l]<br>|;
	$country_html .= qq|<table cellpadding="4" class="blog_letter">|; # blog_letter �͂��̂��� table3 ��
	my $c_count = defined $cs_c{0} ? $cs_c{0} : 0;
	$country_html .= qq|<tr><td colspan="2">$c_count�l:$cs_c{"0_member"}</td></tr>\n| if $cs_c{"0_member"};
	for my $i (1 .. $w{country}) {
		my $c_count = defined $cs_c{$i} ? $cs_c{$i} : 0;
		my($country_mes, $country_mark) = split /<>/, $lines[$i];
		$country_mark = 'non_mark.gif' if $country_mark eq '';
		$country_html .= qq|<tr><td><img src="$icondir/$country_mark"></td>|;
		$country_html .= qq|<td style="color: #333; background-color: $cs{color}[$i];width:100%;"><b>$cs{name}[$i]</b> $cs{ceo}[$i]<br>$country_mes</td></tr>\n|;
		$country_html .= qq|<tr><td colspan="2">$c_count�l:$cs_c{"${i}_member"}</td></tr>\n| if $cs_c{"${i}_member"};
	}
	$country_html .= qq|</table>|;

	print <<"EOM";
$login_box_html
<p style="text-align:center;">
<a href="#attention">�A�N�Z�X�K���ɂ���</a>
</p>
<hr>
$navi_html
<hr>
$country_html
<hr>
���[ $w{player}/$max_entry�l ]<br>
��ڲ԰�ۑ����� $auto_delete_day��(1�����Lv.1��1��)<br>
��{�S������ $GWT��<br>
���^ $salary_hour���Ԗ� �N��̔C�� $reset_ceo_cycle_year�N����
<hr>
<ol>
<li><a href="reset_player.cgi">ؾ�ď���</a>
<li><a href="CatasoApp-release-signed.apk">��~ɱ���</a>
</ol>
<hr>
<p>
<a name="attention">�A�N�Z�X�K���ɂ���</a><br>
���C������ɂȂ邽��IP�A�h���X��铽����@�\\���g�����A�N�Z�X�͋K�����Ă��܂��B�ȉ��̗�ɓ��Ă͂܂�ꍇ�ɂ́A���ꂼ��̋@�\\���I�t�ɂ��邱�ƂŃA�N�Z�X�ł���悤�ɂȂ�܂��B
</p>
<ol>
<li>Chrome�F�f�[�^�Z�[�o�[���I���ɂȂ��Ă���</li>
<li>Opera�FTurbo(�I�t���[�h)���[�h���I���ɂȂ��Ă���</li>
<li>Mercury�F���k��L���ɂ��Ă���</li>
<li>Opera Max�F�g�p���Ă���u���E�U�ɂ��f�[�^�ʐM�𐧌����Ă���</li>
</ol>
<hr>
<form method="$method" action="login.cgi">
<div>��ڲ԰��:<input type="text" name="login_name" value="$cook_name"></div>
<div>�߽ܰ��:<input type="password" name="pass" value="$cook_pass"></div>
<div><input type="checkbox" name="is_cookie" value="1" $checked>���񂩂���͏ȗ�(Cookie�Ή��g�т̂�)</div>
<div><input type="submit" value="۸޲�"></div>
<input type="hidden" name="guid" value="ON">
</form>
<hr>
EOM
}
=pod
<ol>
<li><a href="readme.html">Readme</a>
<li><a href="http://www13.atwiki.jp/blindjustice/">������</a>
<li><a href="http://www43.atwiki.jp/bjkurobutasaba/">Wiki</a>
<li><a href="new_entry.cgi">�V�K�o�^</a>
<li><a href="../upbbs/imgboard.cgi">�摜�f����</a>
<li><a href="players.cgi">��ڲ԰�ꗗ</a>
<li><a href="legend.cgi">�I�v�̐Δ�</a>
<li><a href="sales_ranking.cgi">���l�ݷݸ�</a>
<li><a href="contest.cgi">��ýĉ��</a>
<li><a href="news.cgi">�ߋ��̉h��</a>
<li><a href="$home_m">HOME</a>
<li><a href="reset_player.cgi">ؾ�ď���</a>
<li><a href="player_ranking.cgi">�p�l�ݷݸ�</a>
<li><a href="main_player.cgi">��͕\\</a>
<li><a href="main_player2.cgi">��͕\\2</a>
<li><a href="year_player_ranking.cgi">��N�ݷݸ�</a>
<li><a href="year_player_ranking_country.cgi">�����ݷݸ�</a>
<li><a href="pop_ranking_gold.cgi">�l�C�ݷݸ�(��)</a>
<li><a href="pop_ranking_middle.cgi">�l�C�ݷݸ�(��)</a>
<li><a href="library.cgi">�}����</a>
<li><a href="shop_big_data.cgi">����</a>
<li><a href="CatasoApp-release-signed.apk">��~ɱ���</a>
</ol>
<hr>
۸޲ݒ�$cs_c{all}�l
<div>$login_list</div>
<hr>
��� $w{player}/$max_entry�l<br>
��ڲ԰�ۑ����� $auto_delete_day��<br>
(1�����1���ق�1��)<br>
��{�S������ $GWT��<br>
���^ $salary_hour���Ԗ�<br>
�N��̔C�� $reset_ceo_cycle_year�N����
<hr>
#�������牺�͉������̌��{<br>
#�X�}�z�c��ʁF<a href="http://www.pandora.nu/nyaa/cgi-bin/upbbs/img-box/img20160620044658.png">img20160620044658.png</a><br>
#�X�}�z����ʁF<a href="http://www.pandora.nu/nyaa/cgi-bin/upbbs/img-box/img20160620044721.png">img20160620044721.png</a><br>
#���݂����Ȃ��ĂȂ�������Ƃ肠���������[�h������u���E�U�̍ċN��<br>
#����ł��_���Ȃ�g���Ă�[���ƃu���E�U�� nanamie �Ɏ莆�ŕ�
#<hr>
=cut

1; # �폜�s��
