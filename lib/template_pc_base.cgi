#================================================
# PC�ްщ�� Created by Merino
#================================================

#================================================
# Ҳ�
#================================================
if ($is_battle eq '1') {
	&battle_html;
}
elsif ($is_battle eq '2') {
	&war_html;
}
elsif (!$main_screen) {
	&status_html;
}
&framework;

#================================================
# �S�̘̂g�g��
#================================================
sub framework {
	my $country_menu = '';
	$country_menu .= qq|<form method="$method" action="chat_prison.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="�S��" class="button1"></form>|;
	$country_menu .= qq|<form method="$method" action="bbs_country.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="����c��" class="button1"></form>|;

	# ������������Ȃ�
	if ($union) {
		$country_menu .= qq|<form method="$method" action="bbs_union.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="������c��" class="button1"></form>|;
	}

	# ���E��Í��̂�
	if (($w{world} eq $#world_states) && $m{country} ne $w{country}) {
		$country_menu .= qq|<form method="$method" action="bbs_vs_npc.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="�{ �� �� �� �c �{" class="button1"></form>|;
	}

	# �M���h�����Ȃ�
#	if ($m{akindo_guild}) {
#		$country_menu .= qq|<form method="$method" action="bbs_akindo.cgi">|;
#		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
#		$country_menu .= qq|<input type="submit" value="�M���h" class="button1"></form>|;
#	}

	if($m{disp_casino}){
		require "$datadir/casino.cgi";
		my $a_line = &all_member_n;
		$country_menu .= $a_line;
	}
	$country_menu .= qq|<form method="$method" action="chat_casino.cgi">|;
	$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$country_menu .= qq|<input type="submit" value="�ΐl����" class="button1"></form>|;
	
	unless ($m{disp_daihyo} eq '0'){
		$country_menu .= qq|<form method="$method" action="bbs_daihyo.cgi">|;
		$country_menu .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$country_menu .= qq|<input type="submit" value="��\\�]�c��" class="button1"></form>|;
	}

	print qq|<div align="center"><table border="0"><tr>|;
	if ($layout eq '2') { # �c��
		print qq|<td valign="top">|;
		print qq|<table width="500" border="0" cellspacing="3" cellpadding="3" height="200" bgcolor="#CCCCCC"><tr>|;
		print qq|<td bgcolor="#000000" align="left" valign="top"><tt>���� $m{money} G<br>$mes</tt></td></tr></table></td>|;
	}
	else {
		print qq|<td valign="top">|;
		print qq|<table width="500" border="0" cellspacing="3" cellpadding="3" height="200" bgcolor="#CCCCCC"><tr>|;
		print qq|<td bgcolor="#000000" align="left" valign="top"><tt>$main_screen</tt></td></tr></table><br>|;
		&my_country_html if !$is_battle && $m{country};
	}
	print qq|</td><td width="160" valign="top" align="right">|;
	unless ($m{disp_top} eq '0'){
		print qq|<form action="$script_index"><input type="submit" value="�s �n �o" class="button1"></form>|;
	}
	
	if (!$is_battle) { # �퓬����\��
		unless ($m{disp_news} eq '0'){
			print qq|<form method="$method" action="news.cgi">|;
			print qq|<input type="submit" value="�ߋ��̉h��" class="button1">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			print qq|</form>|;
		}
		print qq|<form method="$method" action="bbs_public.cgi">|;
		print qq|<input type="submit" value="�f �� ��" class="button1">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		unless ($m{disp_chat} eq '0'){
			print qq|<form method="$method" action="chat_public.cgi">|;
			print qq|<input type="submit" value="�𗬍L��" class="button1">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			print qq|</form>|;
		}
		print qq|<form method="$method" action="chat_horyu.cgi">|;
		print qq|<input type="submit" value="�����ē��[��" class="button1">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
		unless ($m{disp_ad} eq '0'){
			print qq|<form method="$method" action="bbs_ad.cgi">|;
			print qq|<input type="submit" value="��`����" class="button1">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			print qq|</form>|;
		}
		print qq|$country_menu|;
		print qq|<form method="$method" action="letter.cgi">|;
		print qq|<input type="submit" value="�l�� �q������" class="button1">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|</form>|;
	}
	print qq|<p>$menu_cmd</p>| if $layout eq '2' && $menu_cmd;
	print qq|</td></tr><tr>|;

	if ($layout eq '1') { # ����
		print qq|<td colspan="2" border="0" cellspacing="2" cellpadding="3" valign="top" width="100%">|;
		print qq|<table width="100%" height="100" bgcolor="#CCCCCC"><tr>|;
		print qq|<td bgcolor="#000000" align="left" valign="top"><tt>$mes</tt></td></tr></table></td>|;
	}
	elsif ($layout ne '2') { # �ʏ�
		print qq|<td valign="top">|;
		if (!$mes && ($m{wt} > 1 || $m{lib} eq '') ) {
			# �ŐV���
			open my $fh, "< $logdir/world_news.cgi" or &error("$logdir/world_news.cgi̧�ق��ǂݍ��߂܂���");
			my $line = <$fh>;
			close $fh;
			print qq|<table width="500" border="0" cellspacing="2" cellpadding="3" height="60" bgcolor="#CCCCCC"><tr>|;
			print qq|<td bgcolor="#000000" align="left" valign="top"><tt>���ŐV���<br>$line</tt></td>|;
			print qq|</tr></table>|;
		}
		elsif ($mes) { # ү����
			print qq|<table width="500" border="0" cellspacing="2" cellpadding="3" height="100" bgcolor="#CCCCCC"><tr>|;
			print qq|<td bgcolor="#000000" align="left" valign="top"><tt>$mes</tt></td>|;
			print qq|</tr></table>|;
		}
		
		print qq|</td><td valign="top" align="right">$menu_cmd</td>|;
	}
	print qq|</tr><tr><td colspan="2">|;

	if (!$mes && ($m{wt} > 1 || $m{lib} eq '') ) {
		# ��ð���
		&countries_html;
		&world_info;
		&promise_table_html;
	}
	print qq|</td></tr></table></div>|;
}


#================================================
# Ҳ݉��
#================================================
sub status_html {
	my $head_mes = '';
	if (-f "$userdir/$id/letter_flag.cgi") {
		open my $fh, "< $userdir/$id/letter_flag.cgi";
		my $line = <$fh>;
		my($letters) = split /<>/, $line;
		close $fh;
		$head_mes .= qq|<font color="#FFCC66">�莆�� $letters ���͂��Ă��܂�</font><br>|;
	}
	if (-f "$userdir/$id/depot_flag.cgi") {
		$head_mes .= qq|<font color="#FFCC00">�a���菊�ɉו����͂��Ă��܂�</font><br>|;
	}
	if (-f "$userdir/$id/goods_flag.cgi") {
		$head_mes .= qq|<font color="#FFCC99">ϲٰтɉו����͂��Ă��܂�</font><br>|;
	}
	
	my $country_info = '';
	if ($m{country}) {
		my $next_rank = $m{rank} * $m{rank} * 10;
		my $nokori_time = $m{next_salary} - $time;
		$nokori_time = 0 if $nokori_time < 0;
		my $nokori_time_mes = sprintf("<b>%d</b>��<b>%02d</b>��<b>%02d</b>�b��", $nokori_time / 3600, $nokori_time % 3600 / 60, $nokori_time % 60);
		my $reset_rest = int($w{reset_time} - $time);
		my $gacha_time = $m{gacha_time} - $time;
		$gacha_time = 0 if $gacha_time < 0;
		my $gacha_time_mes = sprintf("<b>%d</b>��<b>%02d</b>��<b>%02d</b>�b��", $gacha_time / 3600, $gacha_time % 3600 / 60, $gacha_time % 60);
		my $gacha_time2 = $m{gacha_time2} - $time;
		$gacha_time2 = 0 if $gacha_time2 < 0;
		my $gacha_time2_mes = sprintf("<b>%d</b>��<b>%02d</b>��<b>%02d</b>�b��", $gacha_time2 / 3600, $gacha_time2 % 3600 / 60, $gacha_time2 % 60);
		my $offertory_time = $m{offertory_time} - $time;
		$offertory_time = 0 if $offertory_time < 0;
		my $offertory_time_mes = sprintf("<b>%d</b>��<b>%02d</b>��<b>%02d</b>�b��", $offertory_time / 3600, $offertory_time % 3600 / 60, $ofertory_time % 60);

		$country_info .= qq|<hr size="1">|;
		$country_info .= qq|$units[$m{unit}][1] <b>$rank_sols[$m{rank}]</b>��<br>|;
		$country_info .= qq|$e2j{rank_exp} [ <b>$m{rank_exp}</b> / <b>$next_rank</b> ]<br>|;
		$country_info .= qq|�G��[�O��F<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> �A��<b>$m{renzoku_c}</b>��]<br>| if $m{renzoku_c};
		$country_info .= qq|<hr size="1">|;
		$country_info .= qq|�c�莞��<br>\n|;
		$country_info .= qq|<table class="table1">|;
		if ($m{disp_gacha_time}) {
			$country_info .= qq|<tr><th>���^</th><th>�ΑK</th></tr>\n|;
			$country_info .= qq|<tr><td><span id="nokori_time">$nokori_time_mes</span></td><td><span id="offertory_time">$offertory_time_mes</span></td></tr>\n|;
			$country_info .= qq|<tr><th>�K�`��</th><th>�K�`���i���j</th></tr>\n|;
			$country_info .= qq|<tr><td><span id="gacha_time">$gacha_time_mes</span></td><td><span id="gacha_time2">$gacha_time2_mes</span></td></tr>\n|;
		} else {
			$country_info .= qq|<tr><th>���^</th></tr>\n|;
			$country_info .= qq|<tr><td><span id="nokori_time">$nokori_time_mes</span></td></tr>\n|;
		}
		$country_info .= qq|<script type="text/javascript"><!--\n nokori_time($nokori_time, $reset_rest, $gacha_time, $gacha_time2, $offertory_time);\n// --></script>\n|;
		$country_info .= qq|</table>|;
		$country_info .= qq|<br>|;
	}
	
	my $name = $m{name};
	$name .= "[$m{shogo}]" if $m{shogo};
	my $marriage = '';
	if ($m{marriage}) {
		my $yid = unpack 'H*', $m{marriage};
		$marriage = qq|�������� <a href="profile.cgi?id=$yid">$m{marriage}</a><br>|;
	}
	my $master = '';
	if ($m{master}){
		if($m{master_c}){
			$master = qq|�t�� <a href="letter.cgi?id=$id&pass=$pass&send_name=$m{master}">$m{master}</a><br>|;
		}else{
			$mid = unpack 'H*', $m{master};
			if (-f "$userdir/$mid/user.cgi") {
				$master = qq|��q <a href="letter.cgi?id=$id&pass=$pass&send_name=$m{master}">$m{master}</a><br>|;
			} else {
				$master = qq|��q <font color="#FF0000">$m{master} ���S</font><br>|;
			}
		}
	}
	my $fuka = $m{egg} ? int($m{egg_c} / $eggs[$m{egg}][2] * 100) : 0;
	my $rank_name = $ranks[$m{rank}];
	if ($m{super_rank}){
		$rank_name = '';
		$rank_name .= '��' for 1 .. $m{super_rank};
		$rank_name .= $m{rank_name};
	}

	$main_screen .= qq|<table width="100%" border="0"><tr><td width="60%" valign="top" align="left"><tt>$head_mes|;
	$main_screen .= qq|<img src="$icondir/$m{icon}" style="vertical-align: middle;">| if $m{icon};
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	my $pet_c = $m{pet} ? "��$m{pet_c}":'';
	$main_screen .=<<"EOM";

		$name<br>
		$marriage
		$master
		<font color="$cs{color}[$m{country}]">$c_m</font> $rank_name<br>
		$country_info
		<hr size="1">
		
		<font color="#9999CC">����F[$weas[$m{wea}][2]]$wname��<b>$m{wea_lv}</b>(<b>$m{wea_c}</b>/<b>$weas[$m{wea}][4]</b>)</font><br>
		<font color="#9999CC">�h��F[$guas[$m{gua}][2]]$guas[$m{gua}][1]</font><br>
		<font color="#99CCCC">�߯āF$pets[$m{pet}][1]$pet_c</font><br>
		<font color="#99CC99">�ϺށF$eggs[$m{egg}][1](<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)</font><br>
		<div class="bar5"><img src="$htmldir/space.gif" style="width: $fuka%"></div>
		<font color="#CCCC99">��  �F$m{insect_name}</font><br>
		
	</tt></td><td valign="top" align="left"><tt>
		
		<b>$m{sedai}</b>����� $sexes[ $m{sex} ]<br>
		Lv.<b>$m{lv}</b> [$jobs[$m{job}][1]]<br>
		<font color="#CC9999">$e2j{hp} [ <b>$m{hp}</b>/<b>$m{max_hp}</b> ]</font><br>
		<font color="#CC99CC">$e2j{mp} [ <b>$m{mp}</b>/<b>$m{max_mp}</b> ]</font><br>
		<hr size="1">
		��J�x <b>$m{act}</b>%<br>
		<div class="bar3" width="140px"><img src="$htmldir/space.gif" style="width: $m{act}%"></div>
		<hr size="1">
		$e2j{exp} <b>$m{exp}</b>Exp<br>
		<div class="bar4"><img src="$htmldir/space.gif" style="width: $m{exp}%"></div>

		<hr size="1">
		���� <b>$m{money}</b>G<br>
		<hr size="1">
		�M�@�́@<b>$m{medal}</b>��<br>
		���ɺ�� <b>$m{coin}</b>��<br>
		�� � �ށy$m{lot}�z<br>
		
	</tt></td></tr></table>
EOM
}



#================================================
# �퓬���
#================================================
sub battle_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" style="vertical-align: middle;">| : '';;
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" style="vertical-align: middle;">| : '';

	my $m_hp_par = $m{max_hp} <= 0 ? 0 : int($m{hp} / $m{max_hp} * 100);
	my $y_hp_par = $y{max_hp} <= 0 ? 0 : int($y{hp} / $y{max_hp} * 100);
	my $m_mp_par = $m{max_mp} <= 0 ? 0 : int($m{mp} / $m{max_mp} * 100);
	my $y_mp_par = $y{max_mp} <= 0 ? 0 : int($y{mp} / $y{max_mp} * 100);
	my $fuka = $m{egg} ? int($m{egg_c} / $eggs[$m{egg}][2] * 100) : 0;
	
	$m_mes = qq|<span style="color: #333; background-color: #FFF;">< $m_mes )</span>| if $m_mes;
	$y_mes = qq|<span style="color: #333; background-color: #FFF;">< $y_mes )</span>| if $y_mes;

	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00">��</font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00">��</font>' : '';

	$main_screen .= qq|$m_icon $m{name} $m_mes<br>|;
	$main_screen .= qq|<table border="0">|;
	$main_screen .= qq|<tr><td>$e2j{max_hp}�F</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $m_hp_par%"></div></td><td> (<b>$m{hp}</b>/<b>$m{max_hp}</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td>$e2j{max_mp}�F</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $m_mp_par%"></div></td><td> (<b>$m{mp}</b>/<b>$m{max_mp}</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td colspan="3">�U���� [ <b>$m_at</b> ] / �h��� [ <b>$m_df</b> ] / �f����[ <b>$m_ag</b> ]<br></td></tr>|;
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	$main_screen .= qq|<tr><td colspan="3">$m_tokkou����F[$weas[$m{wea}][2]] $wname��$m{wea_lv} ($m{wea_c})<br></td></tr>| if $m{wea};
	$main_screen .= qq|<tr><td colspan="3">�h��F[$guas[$m{gua}][2]] $guas[$m{gua}][1]<br></td></tr>| if $m{gua};
	$main_screen .= qq|<tr><td colspan="3">�߯āF$pets[$m{pet}][1]��$m{pet_c}<br></td></tr>| if $pets[$m{pet}][2] eq 'battle';
	$main_screen .= qq|<tr><td>$e2j{exp}�F</td><td><div class="bar4"><img src="$htmldir/space.gif" style="width: $m{exp}%"></div></td><td> (<b>$m{exp}</b>/<b>100</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td>$eggs[$m{egg}][1]�F</td><td><div class="bar5"><img src="$htmldir/space.gif" style="width: $fuka%"></div></td><td> (<b>$m{egg_c}</b>/<b>$eggs[$m{egg}][2]</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td>��J�x�F</td><td><div class="bar3" width="140px"><img src="$htmldir/space.gif" style="width: $m{act}%"></div></td><td> (<b>$m{act}</b>/<b>100</b>)<br></td></tr>|;

	$main_screen .= qq|</table>�@ VS<br>|;
	
	$main_screen .= qq|$y_icon $y{name} $y_mes<br>|;
	$main_screen .= qq|<table border="0">|;
	$main_screen .= qq|<tr><td>$e2j{max_hp}�F</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $y_hp_par%"></div></td><td> (<b>$y{hp}</b>/<b>$y{max_hp}</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td>$e2j{max_mp}�F</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $y_mp_par%"></div></td><td> (<b>$y{mp}</b>/<b>$y{max_mp}</b>)<br></td></tr>|;
	$main_screen .= qq|<tr><td colspan="3">�U���� [ <b>$y_at</b> ] / �h��� [ <b>$y_df</b> ] / �f����[ <b>$y_ag</b> ]<br></td></tr>|;
	my $ywname = $y{wea_name} ? $y{wea_name} : $weas[$y{wea}][1];
	$main_screen .= qq|<tr><td colspan="3">$y_tokkou����F[$weas[$y{wea}][2]] $ywname<br></td></tr>| if $y{wea};
	$main_screen .= qq|<tr><td colspan="3">�h��F[$guas[$y{gua}][2]] $guas[$y{gua}][1]<br></td></tr>| if $y{gua};
	$main_screen .= qq|</table>|;
}

#================================================
# �푈���
#================================================
sub war_html {
	my $m_icon = $m{icon} ? qq|<img src="$icondir/$m{icon}" style="vertical-align: middle;">| : '';;
	my $y_icon = $y{icon} ? qq|<img src="$icondir/$y{icon}" style="vertical-align: middle;">| : '';
	
	$war_march = 1 if $war_march <= 0;
	my $m_sol_par = $rank_sols[$m{rank}] * $war_march <= 0 ? 0 : int($m{sol} / ($rank_sols[$m{rank}] * $war_march) * 100);
	my $y_sol_par = $rank_sols[$y{rank}] * $war_march <= 0 ? 0 : int($y{sol} / ($rank_sols[$y{rank}] * $war_march) * 100);
	
	$m_mes = qq|<span style="color: #333; background-color: #FFF;">< $m_mes )</span>| if $m_mes;
	$y_mes = qq|<span style="color: #333; background-color: #FFF;">< $y_mes )</span>| if $y_mes;
	
	my $m_tokkou = $is_m_tokkou ? '<font color="#FFFF00"><b>�����U��</b></font>' : '';
	my $y_tokkou = $is_y_tokkou ? '<font color="#FFFF00"><b>�����U��</b></font>' : '';
	
	my $rank_name = $ranks[$m{rank}];
	if ($m{super_rank}){
		$rank_name = '';
		$rank_name .= '��' for 1 .. $m{super_rank};
		$rank_name .= $m{rank_name};
	}
	$main_screen .= qq|$m_icon $m{name} [$rank_name] $m_mes<br>|;
	$main_screen .= qq|$m_tokkou$units[$m{unit}][1] ����[<b>$m{lea}</b>] <br>|;
	$main_screen .= qq|<table border="0">|;
	$main_screen .= qq|<tr><td>���m�F</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $m_sol_par%"></div></td><td> (<b>$m{sol}</b>��)<br></td></tr>|;
	$main_screen .= qq|<tr><td>�m�C�F</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $m{sol_lv}%"></div></td><td> (<b>$m{sol_lv}</b>%)<br></td></tr>|;
	$main_screen .= qq|</table>|;
	$main_screen .= qq|�@ VS�@ �c��$m{turn}���<br>|;
	$main_screen .= qq|$y_icon $y{name} [$ranks[$y{rank}]] $y_mes<br>|;
	$main_screen .= qq|$y_tokkou$units[$y{unit}][1] ����[<b>$y{lea}</b>]<br>|;
	$main_screen .= qq|<table border="0">|;
	$main_screen .= qq|<tr><td>���m�F</td><td><div class="bar1"><img src="$htmldir/space.gif" style="width: $y_sol_par%"></div></td><td> (<b>$y{sol}</b>��)<br></td></tr>|;
	$main_screen .= qq|<tr><td>�m�C�F</td><td><div class="bar2"><img src="$htmldir/space.gif" style="width: $y{sol_lv}%"></div></td><td> (<b>$y{sol_lv}</b>%)<br></td></tr>|;
	$main_screen .= qq|</table>|;
}


#================================================
# ���X�̍��́A��\��
#================================================
sub countries_html {
	my($c1, $c2) = split /,/, $w{win_countries};

	print qq|<table class="table1">|;
	print qq|<tr><th>$e2j{name}</th>|;
	print qq|<td align="center" style="color: #333; background-color: $cs{color}[$_];">$cs{name}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;
	
	unless ($w{world} eq '10') {
		print qq|<tr><th>$e2j{strong}</th>|;
		for my $i (1 .. $w{country}) {
			print $cs{is_die}[$i] ? qq|<td align="center">�� �S</td>| : qq|<td align="center">$cs{strong}[$i]</td>|;
		}
		print qq|</tr>\n|;
	}

	for my $k (qw/ceo war dom pro mil/) {
		print qq|<tr><th>$e2j{$k}</th>|;
		for my $i (1 .. $w{country}) {
			print qq|<td align="center">$cs{$k}[$i]</td>|;
		}
		print qq|</tr>\n|;
	}
	print qq|<tr><th>�l��</th>|;
	print qq|<td align="center">$cs{member}[$_]/$cs{capacity}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;

	print qq|</table><br>|;
}

#================================================
# ���E�̏��
#================================================
sub world_info {
	my($c1, $c2) = split /,/, $w{win_countries};
	my $limit_hour = int( ($w{limit_time} - $time) / 3600 );
	my $limit_day  = $limit_hour <= 24 ? $limit_hour . '����' : int($limit_hour / 24) . '��';
	my $reset_rest = int($w{reset_time} - $time);
	my $reset_time_mes = sprintf("<b>%d</b>����<b>%02d</b>��<b>%02d</b>�b��", $reset_rest / 3600, $reset_rest % 3600 / 60, $reset_rest % 60);

	print $w{playing} >= $max_playing ? qq|<font color="#FF0000">��</font>| : qq|<font color="#00FF00">��</font>|;
	print qq|��ڲ���y$w{playing}/$max_playing�l�z/ |;
	print qq|���E��y$world_states[$w{world}]�z/ |;
	print qq|$world_name��y$w{year}�N�z/ |;
	print qq|��������y�c��$limit_day�z<br>|;
	
	if ($reset_rest > 0){
		print qq|�I����ԁy�c��<span id="reset_time">$reset_time_mes</span>|;
		print qq|<noscript>$reset_time_mes</noscript>|;
		print qq|�z<br>|;
	}
	print qq|��Փx�yLv.$w{game_lv}�z/ ����$e2j{strong}�y$touitu_strong�z/ | unless $w{world} eq '10';
	print $c2 ? qq|���ꍑ�y<font color="$cs{color}[$c1]">$cs{name}[$c1]</font><font color="$cs{color}[$c2]">$cs{name}[$c2]</font>�����z|
		: $c1 ? qq|���ꍑ�y<font color="$cs{color}[$c1]">$cs{name}[$c1]</font>�z|
		:       ''
		;
}


#================================================
# �F�D�x/���(table��)
#================================================
sub promise_table_html {
	my @promise_js = (
		'<td align="center">�|</td>',
		'<td align="center" style="background-color: #090">����</td>',
		'<td align="center" style="background-color: #C00">��풆</td>',
	);
	
	print qq|<table class="table1s"><tr><td>���/�F�D�x</td>|;
	print qq|<td style="color: #333; background-color: $cs{color}[$_]">$cs{name}[$_]</td>| for 1 .. $w{country};
	print qq|</tr>|;
	
	for my $i (1 .. $w{country}) {
		print qq|<tr><td style="color: #333; background-color: $cs{color}[$i]">$cs{name}[$i]</td>|;
		for my $j (1 .. $w{country}) {
			if ($i eq $j) {
				print qq|<td align="center">�@</td>|;
			}
			elsif ($i > $j) {
				my $p_c_c = "p_${j}_${i}";
				print $promise_js[ $w{$p_c_c} ];
			}
			else {
				my $f_c_c = "f_${i}_${j}";
				print qq|<td align="right">$w{$f_c_c}%</td>|;
			}
		}
		print qq|</tr>|;
	}
	print qq|</table><br>|;
}


#================================================
# ����/�������̏��
#================================================
sub my_country_html {
	print <<"EOM";
		<table class="table1" width="500" cellpadding="3">
			<tr>
				<th>������</th>
				<th>$e2j{state}</th>
				<th>$e2j{tax}</th>
				<th>$e2j{strong}</th>
				<th>$e2j{food}</th>
				<th>$e2j{money}</th>
				<th>$e2j{soldier}</th>
			</tr><tr>
				<td style="color: #333; background-color: $cs{color}[$m{country}]; text-align: center;">$cs{name}[$m{country}]</td>
				<td align="center">$country_states[ $cs{state}[$m{country}] ]</td>
				<td align="right"><b>$cs{tax}[$m{country}]</b>%</td>
				<td align="right"><b>$cs{strong}[$m{country}]</b></td>
				<td align="right"><b>$cs{food}[$m{country}]</b></td>
				<td align="right"><b>$cs{money}[$m{country}]</b></td>
				<td align="right"><b>$cs{soldier}[$m{country}]</b></td>
			</tr>
		</table>
		<br>
EOM
	if ($union) {
		print <<"EOM";
		<table class="table1" width="500" cellpadding="3">
			<tr>
				<th>������</th>
				<th>$e2j{state}</th>
				<th>$e2j{tax}</th>
				<th>$e2j{strong}</th>
				<th>$e2j{food}</th>
				<th>$e2j{money}</th>
				<th>$e2j{soldier}</th>
			</tr><tr>
				<td style="color: #333; background-color: $cs{color}[$union]; text-align: center;">$cs{name}[$union]</td>
				<td align="center">$country_states[ $cs{state}[$union] ]</td>
				<td align="right"><b>$cs{tax}[$union]</b>%</td>
				<td align="right"><b>$cs{strong}[$union]</b></td>
				<td align="right"><b>$cs{food}[$union]</b></td>
				<td align="right"><b>$cs{money}[$union]</b></td>
				<td align="right"><b>$cs{soldier}[$union]</b></td>
			</tr>
		</table>
		<br>
EOM
	}
}

#================================================
# ���ɂ̐l��
#================================================
sub all_member_n {
	my $ret_str = '';
	for my $i (0 .. $#files) {
		my $member_c  = 0;
		my %sames = ();
		my $tf_name = "$logdir/chat_casino$files[$i][2]_member.cgi";
	
		open my $fh, "< $tf_name" or &error('���ް̧�ق��J���܂���'); 
		my $head_line = <$fh>;
		while (my $line = <$fh>) {
			my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
			if ($time - 60 > $mtime) {
				next;
			}
			next if $sames{$mname}++; # �����l�Ȃ玟
			
			$member_c++;
		}
		close $fh;
		$ret_str .= substr($files[$i][0], 0, 2) . "/$member_c ";
		$ret_str .= "<br>" if $i % 4 == 3;
	}
	return $ret_str;
}


1; # �폜�s��
