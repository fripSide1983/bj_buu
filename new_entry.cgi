#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# �V�K�o�^ Created by Merino
#================================================
&decode;
&header;
&access_check;
&read_cs;
&error('���ݒ���̂��߁A�V�K�o�^�͎󂯕t���Ă���܂���') if $w{player} >= $max_entry;

$in{mode} eq 'new_entry' ? &new_entry : &new_form;

&footer;
exit;

#================================================
# �V�K�o�^̫��
#================================================
sub new_form {
	# �d���ł���l���𒲐�
	my ($s, $e) = $w{world} eq $#world_states ? (1, $w{country} - 1) :
					$w{world} eq $#world_states-2 ? ($w{country} - 1, $w{country}) :
					$w{world} eq $#world_states-3 ? ($w{country} - 2, $w{country}) : (1, $w{country});

	++$w{player};

	my $ave_c = int($w{player} / ($e - $s));
	if($w{world} eq $#world_states-2){
		for my $i (1 .. $w{country}) {
			$cs{capacity}[$i] = $i < $w{country} - 1 ? 0 : $ave_c;
		}
	
	}elsif($w{world} eq $#world_states-3){
		for my $i (1 .. $w{country}) {
			$cs{capacity}[$i] = $i < $w{country} - 2 ? 0:$ave_c;
		}
	
	}else {
		for my $i ($s .. $e) {
			$cs{capacity}[$i] = $ave_c;
		}
	}

	my @list;
	for my $i ($s .. $e) {
		push(@list, $i) if $cs{member}[$i] < $cs{capacity}[$i];
	}

	my $country_html;
	if (!$is_mobile && @list) {
		my @lines = &get_countries_mes();
		$country_html .= qq|<br><table cellpadding="4" class="table2">|;
		for my $i (0 .. $#list) {
			my($country_mes, $country_mark) = split /<>/, $lines[$list[$i]];
			$country_mark = 'non_mark.gif' if $country_mark eq '';
			$country_html .= qq|<tr><td><img src="$icondir/$country_mark"></td></td><td style="color: #333; background-color: $cs{color}[$list[$i]]; text-align: right;" nowrap><b>$cs{name}[$list[$i]]</b><br>$cs{ceo}[$list[$i]]<br><br></td><td style="width:100%;">$country_mes<br></td></tr>\n|;
		}
		$country_html .= qq|</table>|;
	}

	my $to_country_html;
	for my $i (0 .. $#list) {
		$to_country_html .= qq|<input type="radio" id="cmd_$i" name="cmd" value="$list[$i]"><label for="cmd_$i">$cs{name}[$list[$i]]</label><br>|;
	}
	my $j = $w{country} + 1;
	$to_country_html .= qq|<input type="radio" id="cmd_$j" name="cmd" value="$j"><label for="cmd_$j">�K���Ɏd������</label>|;

	print <<"EOM";
<form action="$script_index">
	<input type="submit" value="�s�n�o" class="button1">
</form>
<h1>�V�K�o�^</h1>
<div class="mes">
	<ul>
		<li>��ڲ԰���͑S�p6(���p12)�����܂łł��B</li>
		<li>�߽ܰ�ނ͔��p�p����4�`12�����œ��͂��Ă��������B</li>
		<li>���p�L��(,;"'&<>)�Ƌ󔒂͎g���܂���B</li>
		<li>�l���s�����Ǝv�����O�A�����֎~�p�ꓙ���܂ޖ��O�͓o�^���Ă��폜����܂��B</li>
		<li><b>���d�o�^�͋֎~�ł��B��������폜���܂��B</b></li>
		<li>�K�ǁ�<a href="readme.html" class="link1">readme</a></li>
	</ul>
</div>
<br>
<form method="$method" action="new_entry.cgi">
	<input type="hidden" name="guid" value="ON">
	<input type="hidden" name="mode" value="new_entry">
	<table class="table1">
		<tr><td><tt>��ڲ�-���F</tt></td><td><input type="text" name="name" class="text_box1"><br></td></tr>
		<tr><td><tt>�߽ܰ�� �F</tt></td><td><input type="text" name="pass" class="text_box1"><br></td></tr>
		<tr><td><tt>���ʁ@�@�F</tt></td><td><tt><input type="radio" name="sex" value="1" checked>�j�@<input type="radio" name="sex" value="2">��<br></tt></td></tr>
		<tr><td><tt>�d����@�F</tt></td><td><tt>$to_country_html<br></tt></td></tr>
	</table>
	$country_html
	<p><input type="submit" value="�o�^����" class="button1"></p>
</form>
EOM
}

#================================================
# �V�K�o�^�`�F�b�N����������
#================================================
sub new_entry {
	&error('��ڲ�-�������͂���Ă��܂���')	unless $in{name};
	&error('�߽ܰ�ނ����͂���Ă��܂���')	if $in{pass} eq '';
	&error('���ʂ����͂���Ă��܂���')		if $in{sex} eq '';
	&error('�d���悪�I������Ă��܂���')		if $cmd eq '';

	&error('��ڲ�-���ɕs���ȕ���( ,;\"\'&<>\\\/ )���܂܂�Ă��܂�')	if $in{name} =~ /[,;\"\'&<>\\\/]/;
	&error('��ڲ�-���ɕs���ȋ󔒂��܂܂�Ă��܂�')				if $in{name} =~ /�@/ || $in{name} =~ /\s/;
	&error('��ڲ�-���͑S�p6(���p12)�����ȓ��ł�')				if length($in{name}) > 12;
	&error('�߽ܰ�ނ͔��p�p�����œ��͂��ĉ�����')				if $in{pass} =~ m/[^0-9a-zA-Z]/;
	&error('�߽ܰ�ނ͔��p�p����4�`12�����ł�')					if length $in{pass} < 4 || length $in{pass} > 12;
	&error('��ڲ�-�����߽ܰ�ނ����ꕶ����ł�')					if $in{name} eq $in{pass};
	&error('���ʂ��ُ�ł�')									if $in{sex} =~ m/[^12]/;
	
	&error("�ő̎��ʔԍ��𑗂�ݒ�ɂ��Ă�������") if $agent =~ /DoCoMo/ && !$ENV{HTTP_X_DCMGUID};
	&error("�ő̎��ʔԍ��𑗂�ݒ�ɂ��Ă�������") if $agent =~ /KDDI|UP\.Browser/ && !$ENV{HTTP_X_UP_SUBNO};

	&error('���Ȃ���IP���ڽ�͓o�^���֎~����Ă��܂�') if &is_deny_addr;
	&error('���d�o�^�͋֎~���Ă��܂�')                if (&is_renzoku_entry && !$config_test);

	&create_user;

	# create_user���̂����������������邯�ǂȂ�ׂ�����݂���d������Ƃ�����Ԃ��Č�
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
	if ($country < $cmd || $cmd eq '0') { # �K���d��
		$cmd = int(rand($country) + 1);
		&mes_and_world_news("�K����$cs{name}[$cmd]�Ɏd�����܂���",1);
	}
	else {
		&mes_and_world_news("$cs{name}[$cmd]�Ɏd�����܂���",1);
	}
	$m{value} = $cmd;
	require './lib/country_move.cgi';
	&is_move_from_neverland; # $cmd �ɓK�؂Ȏd����̍��ԍ�������
	&move_to_country;
	&write_user;

	print <<"EOM";
<p>�ȉ��̓��e�œo�^���܂���</p>

<p><font color="#FF0000">�����O���߽ܰ�ނ�۸޲݂���Ƃ��ɕK�v�Ȃ̂ŁA�Y��Ȃ��悤��!</font><p>
<table class="table1">
	<tr><th>��ڲ�-��</th><td>$m{name}<br></td>
	<tr><th>�߽ܰ��</th><td>$m{pass}<br></td>
	<tr><th>����</th><td>$sexes[$m{sex}]<br></td>
	<tr><th>�d����</th><td>$cs{name}[$m{country}]<br></td>
	<tr><th>$e2j{max_hp}</th><td align="right">$m{max_hp}<br></td>
	<tr><th>$e2j{max_mp}</th><td align="right">$m{max_mp}<br></td>
	<tr><th>$e2j{at}</th><td align="right">$m{at}<br></td>
	<tr><th>$e2j{df}</th><td align="right">$m{df}<br></td>
	<tr><th>$e2j{mat}</th><td align="right">$m{mat}<br></td>
	<tr><th>$e2j{mdf}</th><td align="right">$m{mdf}<br></td>
	<tr><th>$e2j{ag}</th><td align="right">$m{ag}<br></td>
	<tr><th>$e2j{cha}</th><td align="right">$m{cha}<br></td>
	<tr><th>$e2j{lea}</th><td align="right">$m{lea}<br></td>
</table>
<div>
<a href="http://www13.atwiki.jp/blindjustice/" target="_blank">������</a>�͓ǂ݂܂������H<br>
�킩��Ȃ����Ƃ�����ꍇ�́A�܂���������ǂ݂܂��傤�B
</div>
<form method="$method" action="login.cgi">
	<input type="hidden" name="guid" value="ON">
	<input type="hidden" name="is_cookie" value="1">
	<input type="hidden" name="login_name" value="$in{name}">
	<input type="hidden" name="pass" value="$in{pass}">
	<input type="submit" value="Play!" class="button1">
</form>
EOM
}

#================================================
# �o�^����
#================================================
sub create_user {
	$id = unpack 'H*', $in{name};
	
	# ̫���̧�ٍ쐬
	mkdir "$userdir/$id" or &error("���̖��O�͂��łɓo�^����Ă��܂�");
	for my $file_name (qw/blog collection depot letter letter_log memory money profile proposal skill user summer tutorial/) {
		my $output_file = "$userdir/$id/$file_name.cgi";
		open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
		close $fh;
		chmod $chmod, $output_file;
	}
	
	for my $dir_name (qw/book etc music picture/) {
		mkdir "$userdir/$id/$dir_name" or &error("$userdir/$id/$dir_name �ިڸ�؂����܂���ł���");
		open my $fh, "> $userdir/$id/$dir_name/index.html" or &error("$userdir/$id/$dir_name/index.html ̧�ق����܂���ł���");
		close $fh;
	}

	open my $fh2, ">> $userdir/$id/collection.cgi" or &error("$userdir/$id/collection.cgi ̧�ق����܂���ł���");
	print $fh2 ",\n,\n,\n";
	close $fh2;
	
	open my $fh3, ">> $userdir/$id/skill.cgi" or &error("$userdir/$id/skill.cgi ̧�ق����܂���ł���");
	print $fh3 ",";
	close $fh3;


	%m = ();
	$m{name} = $in{name};
	$m{pass} = $in{pass};
	$m{sex}  = $in{sex};
	$m{max_hp} = int(rand(3)) + 20;
	$m{max_mp} = int(rand(3)) + 7;
	$m{hp}  = $m{max_hp};
	$m{mp}  = $m{max_mp};
	
	$m{sedai} = 1;
	$m{lv}    = 1;
	$m{egg}   = 51;
	$m{money} = $config_test ? 4999999 : 10000;
	$m{icon}  = $default_icon;
	
	$m{start_time} = $time;

	# �ð��
	for my $k (qw/at df mat mdf ag lea cha/) {
		$m{$k} = int(rand(3)) + 7;
	}

	# �����l0
	my @zeros = (qw/
		wt act country job exp rank rank_exp unit sol sol_lv medal coin renzoku renzoku_c
		wea wea_c wea_lv egg_c pet is_full 
		nou_c sho_c hei_c gai_c gou_c cho_c sen_c gik_c kou_c tei_c mat_c cas_c tou_c shu_c col_c mon_c
		win_c lose_c draw_c hero_c huk_c met_c war_c dom_c mil_c pro_c esc_c res_c no1_c fes_c
		turn stock value shogo_t icon_t breed breed_c depot_bonus
		y_max_hp y_hp y_max_mp y_mp y_at y_df y_mat y_mdf y_ag y_cha y_lea y_wea
		y_country y_rank y_sol y_unit y_sol_lv
	/);
	for my $k (@zeros) {
		$m{$k} = 0;
	}

	# �����l1
	my @ones = (qw/
		disp_top disp_news disp_chat disp_ad disp_daihyo
	/);
	for my $k (@ones) {
		$m{$k} = 1;
	}

	$m{shuffle}  = 0; # 0 �ō������V���b�t�������
	$m{seed} = 'human';
	$m{coin} = $config_test ? 2500000 : 0;

	require './lib/tutorial.cgi';
	&start_tutorial;

	&write_user;
	
	open my $fh9, ">> $logdir/0/member.cgi" or &error("$cs{name}[0]�����ް̧�ق��J���܂���");
	print $fh9 "$m{name}\n";
	close $fh9;
	
	++$w{player};
	
	my $country = ($w{world} eq $#world_states) ? $w{country} - 1 : $w{country};
	# �d���ł���l���𒲐�
	my $country = $w{world} eq $#world_states ? $w{country} - 1 :
					$w{world} eq $#world_states-2 ? 2 :
					$w{world} eq $#world_states-3 ? 3 : $w{country};
	my $ave_c = int($w{player} / $country);
	if($w{world} eq $#world_states-2){
		for my $i (1 .. $w{country}) {
			$cs{capacity}[$i] = $i < $w{country} - 1 ? 0:$ave_c;
		}
	
	}elsif($w{world} eq $#world_states-3){
		for my $i (1 .. $w{country}) {
			$cs{capacity}[$i] = $i < $w{country} - 2 ? 0:$ave_c;
		}
	
	}else {
		for my $i (1 .. $country) {
			$cs{capacity}[$i] = $ave_c;
		}
	}
	&write_cs;
	
	&write_world_news("$m{name}�Ƃ����҂��Q�����܂���",1);
	&write_entry_news("$m{name}�Ƃ����҂��Q�����܂���");
}

#================================================
# �Ǘ����A�N�哊�[�ō폜���ꂽIP�EUA������
#================================================
sub is_deny_addr {
	open my $fh, "< $logdir/deny_addr.cgi" or &error("$logdir/deny_addr.cgi̧�ق��J���܂���");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		if ($is_mobile) {
			return 1 if $line eq $agent;
		}
		elsif ($line eq $addr) {
			return 1;
		}
	}
	close $fh;
	
	return 0;
}

#================================================
# �o�^���Ă���S�v���C���[��IP��UA������
#================================================
sub is_renzoku_entry {
	opendir my $dh, "$userdir" or &error("$userdir�f�B���N�g�����J���܂���");
	while (my $dir_name = readdir $dh) {
		next if $dir_name =~ /\./;
		next if $dir_name =~ /backup/;
		
		open my $fh, "< $userdir/$dir_name/user.cgi" or &error("$userdir/$dir_name/user.cgi�t�@�C�����ǂݍ��߂܂���");
		my $line_data = <$fh>;
		my $line_info = <$fh>;
		close $fh;
		
		my($paddr, $phost, $pagent) = split /<>/, $line_info;
		if ($is_mobile) {
			return 1 if $pagent eq $agent;
		}
		elsif ($paddr eq $addr) {
			return 1;
		}
		if(-f "$userdir/$dir_name/access_log.cgi"){
			open my $fh2, "< $userdir/$dir_name/access_log.cgi" or &error("$userdir/$dir_name/access_log.cgi�t�@�C�����ǂݍ��߂܂���");
			while(my $line = <$fh2>){
				my($access_addr, $access_host, $access_agent) = split /<>/, $line;
				
				if ($is_mobile) {
					&warning_mail if $pagent eq $agent;
				}
				elsif ($paddr eq $addr) {
					&warning_mail;
					return 1;
				}
			}
			close $fh2;
		}
	}
	closedir $dh;
	return 0;
}

sub warning_mail{
	my $send_id = unpack 'H*', $admin_name;
	
	local $this_file = "$userdir/$send_id/letter";
	&error("$admin_name�Ƃ�����ڲ԰�����݂��܂���") unless -f "$this_file.cgi";
	
	$in{comment} = "$in{name}���񂪑��v���C���[�����O�C���������Ƃ̂���IP�œo�^����܂���";

	require './lib/_bbs_chat.cgi';
	&write_comment;
	
	# �莆��������׸ނ����Ă�
	my $letters = 0;
	if(-f "$userdir/$send_id/letter_flag.cgi"){
		open my $fh, "< $userdir/$send_id/letter_flag.cgi";
		my $line = <$fh>;
		($letters) = split /<>/, $line;
		close $fh;
	}
	$letters++;
	
	open my $fh, "> $userdir/$send_id/letter_flag.cgi";
	print $fh "$letters<>";
	close $fh;
}

