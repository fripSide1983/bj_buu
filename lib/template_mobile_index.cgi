#================================================

# index.cgi����ڰ�(�g��) Created by Merino

#================================================



#================================================

sub index {
	my($login_list, %cs_c) = @_;
	my($cook_name, $cook_pass, $cook_is_cookie) = &get_cookie;
	my $checked = $cook_is_cookie ? 'checked' : '';

	$cs_c{all} ||= 0;
	$cs_c{0}   ||= 0;
	print <<"EOM";
<h1>$title</h1>
<form method="$method" action="login.cgi">
<div>��ڲ԰��:<input type="text" name="login_name" value="$cook_name"></div>
<div>�߽ܰ��:<input type="text" name="pass" value="$cook_pass"></div>
<div><input type="checkbox" name="is_cookie" value="1" $checked>���񂩂���͏ȗ�(Cookie�Ή��g�т̂�)</div>
<div><input type="submit" value="۸޲�"></div>
<input type="hidden" name="guid" value="ON">
</form>
<hr>
<ol>
<li><a href="http://buu.pandora.nu/cgi-bin/bj/user/8d9593d8/book/526561646d65208dec3a8d9593d8.html" accesskey="1">Readme</a>
<li><a href="http://www13.atwiki.jp/blindjustice/" accesskey="2">������</a>
<li><a href="http://www43.atwiki.jp/bjkurobutasaba/" accesskey="3">Wiki</a>
<li><a href="new_entry.cgi" accesskey="4">�V�K�o�^</a>
<li><a href="players.cgi" accesskey="5">��ڲ԰�ꗗ</a>
<li><a href="legend.cgi" accesskey="6">�I�v�̐Δ�</a>
<li><a href="sales_ranking.cgi" accesskey="7">���l�ݷݸ�</a>
<li><a href="contest.cgi" accesskey="8">��ýĉ��</a>
<li><a href="news.cgi" accesskey="9">�ߋ��̉h��</a>
<li><a href="$home_m" accesskey="0">HOME</a>
<li><a href="reset_player.cgi">ؾ�ď���</a>
<li><a href="player_ranking.cgi">�p�l�ݷݸ�</a>
<li><a href="main_player.cgi">��͕\\</a>
<li><a href="year_player_ranking.cgi">��N�ݷݸ�</a>
<li><a href="year_player_ranking_country.cgi">�����ݷݸ�</a>
<li><a href="pop_ranking_gold.cgi">�l�C�ݷݸ�(��)</a>
<li><a href="pop_ranking_middle.cgi">�l�C�ݷݸ�(��)</a>
<li><a href="library.cgi">�}����</a>
<li><a href="shop_big_data.cgi">����</a>

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
EOM
}


1; # �폜�s��
