require "$datadir/hunting.cgi";
require "$datadir/skill.cgi";
sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
#================================================
# �����̖����ǉ� Created by Merino
#================================================

# �ő吶����(�Â��������玩���폜)
my $max_monster = 30;

# �������瑗���Ă����Ϻ�
my @egg_nos = (1..34,42..51);

# �����̍Ō�̌��t
my @m_messages = (qw/��ְ �����߰ ���߹�߰ ӹ�ӹ� ι�ι� ��Ʈ��Ʈ �������� �߲����� ѷ������� ������ ����� ùùù� ��ԯ��� Ʈ�Ʈ� ð�ï�ð/);


#================================================
sub tp_100 {
	my $v = &use_pet('myself');
	my $skill_st = 0;
	my $i = 0;
	for my $skill (split /,/, $m{skills}) {
		$i++;
		if ($skills[$skill][2] eq $weas[$m{wea}][2]) {
			$skill_st += $skills[$skill][7];
		} else {
			$skill_st += $skills[0][7];
		}
	}
	for (my $j = $i; $j < 5; $j++) {
		$skill_st += $skills[0][7];
	}
	$skill_st = 100 if $skill_st > 100;
	$skill_st = 0 if $skill_st < 0;
	my $m_st = int(&m_st * $v * 0.5 * (0.5 + 1.0 * $skill_st / 100));
	my $place = '';
	for my $i (0 .. $#places) {
		my $j = $#places-$i;
		if ($m_st >= $places[$j][1]) {
			$place = $places[$j][2];
			last;
		}
	}

	$layout = 1;
	$mes .= qq|�����̖��O�����߂Ă�������<br>|;
	$mes .= qq|�����F$m_st �����n�F$place<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|���O[�S�p10(���p20)�����܂�]�F<input type="text" name="name" value="$m{name}�ݽ��" class="text_box1"><br>|;
	$mes .= qq|�������[�S�p20(���p40)�����܂�]�F<input type="text" name="mes_win"  value="$m{mes_win}" class="text_box1"><br>|;
	$mes .= qq|�������[�S�p20(���p40)�����܂�]�F<input type="text" name="mes_lose" value="$m{mes_lose}" class="text_box1"><br>|;

	if ($default_icon) {
		$mes .= qq|<hr>�����̉摜��I�����Ă�������<br>|;
		$mes .= qq|������摜�̏ꍇ�́A�����������n���炢�Ȃ��Ȃ����Ƃ��ɖ߂��Ă��܂�<br>|;
	
		$mes .= qq|<input type="radio" name="file_name" value="$default_icon" checked><img src="$icondir/$default_icon" style="vertical-align:middle;" $mobile_icon_size><hr>|;
		opendir my $dh, "$userdir/$id/picture" or &error("$userdir/$id/picture �ިڸ�؂��J���܂���");
		while (my $file_name = readdir $dh) {
			next if $file_name =~ /^\./;
			next if $file_name =~ /^_/;
			next if $file_name =~ /^index.html$/;
			$mes .= qq|<input type="radio" name="file_name" value="$file_name"><img src="$userdir/$id/picture/$file_name" style="vertical-align:middle;" $mobile_icon_size><hr>|;
		}
		closedir $dh;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
	
	$m{tp} += 10;
}

# ------------------
sub tp_110 {
	my $is_error = 0;
	unless ($in{name}) {
		$is_error = 1;
	}
	
	my %e2j_checks = (name => '���O', mes_win => '�������', mes_lose => '�������');
	for my $k (keys %e2j_checks) {
		if ($in{$k} =~ /[,;\"\'&<>]/) {
			$mes .= "$e2j_checks{$k}�ɕs���ȕ���( ,;\"\'&<> )���܂܂�Ă��܂�<br>";
			$is_error = 1;
			last;
		}
		elsif ($in{$k} =~ /�@/ || $in{name} =~ /\s/) {
			$mes .= "$e2j_checks{$k}�ɕs���ȋ󔒂��܂܂�Ă��܂�<br>";
			$is_error = 1;
			last;
		}
		else {
			if ($k eq 'name' && length($in{$k}) > 20) {
				$mes .= "$e2j_checks{$k}�͑S�p10(���p20)�����ȓ��ł�<br>";
				$is_error = 1;
				last;
			}
			elsif (length($in{$k}) > 40) {
				$mes .= "$e2j_checks{$k}�͑S�p20(���p40)�����ȓ��ł�<br>";
				$is_error = 1;
				last;
			}
		}
	}
	
	if ($is_error) {
		$m{tp} = 100;
		&{ 'tp_'. $m{tp} };
	}
	else {
		my $v = &use_pet('myself');
		
		if ($v > 0) {
			my $skill_st = 0;
			my $i = 0;
			for my $skill (split /,/, $m{skills}) {
				$i++;
				if ($skills[$skill][2] eq $weas[$m{wea}][2]) {
					$skill_st += $skills[$skill][7];
				} else {
					$skill_st += $skills[0][7];
				}
			}
			for (my $j = $i; $j < 5; $j++) {
				$skill_st += $skills[0][7];
			}
			$skill_st = 100 if $skill_st > 100;
			$skill_st = 0 if $skill_st < 0;
			my $m_st = int(&m_st * $v * 0.5 * (0.5 + 1.0 * $skill_st / 100));
		
			for my $i (0 .. $#places) {
				my $j = $#places-$i;
				if ($m_st >= $places[$j][1]) {
					&add_monster($j, $v, (0.5 + 1.0 * $skill_st / 100));
					&c_up('mon_c');
					$mes .= "$in{name}��$places[$j][2]�̒��ɖ��߂܂���<br>";
					&remove_pet;
					last;
				}
			}
		}
		
		&refresh;
		&n_menu;
	}
}

# ------------------
sub add_monster {
	my($place, $v, $vv) = @_;
	my $p_name = $places[$place][0];
	
	my $monster = "$in{name}<>$m{country}<>";
	for my $k (qw/max_hp max_mp at df mat mdf ag cha /) {
		$monster .= int($m{$k} * $v * 0.5 * $vv) .'<>';
	}
	my $m_icon = $default_icon;
	if ($default_icon && $in{file_name} !~ /^_/ && -f "$userdir/$id/picture/$in{file_name}") {
		if (-f "$icondir/$in{file_name}") {
			$mes .= "�������ق̱��݂����łɎg���Ă����̂ŁA���݂����邱�Ƃ͂ł��܂���ł���<br>";
		}
		else {
			$m_icon = $in{file_name};
			rename "$userdir/$id/picture/$in{file_name}", "$icondir/$in{file_name}";
		}
	}
	$monster .= "$m{wea}<>$m{skills}<>$in{mes_win}<>$in{mes_lose}<>$m_icon<>$m{name}<>\n";
	
	my @lines = ();
	open my $fh, "+< $logdir/monster/$p_name.cgi" or &error("$logdir/monster/$p_name.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		# �����摜��Ԃ�����
		if (@lines+1 >= $max_monster) {
			next unless $default_icon;
			my($ymname, $ymes_win, $yicon, $yname) = (split /<>/, $line)[0,-5,-3,-2];
			next if $yicon eq $default_icon;
			next unless -f "$icondir/$yicon"; # �摜���Ȃ�
			my $y_id  = unpack 'H*', $yname;
			next unless -d "$userdir/$y_id/picture"; # ��ڲ԰�����݂��Ȃ�
			
			# ���������ւ̎莆
			my $m_message = $m_messages[ int( rand(@m_messages) ) ];
			$in{comment}  = qq|$places[$place][2]�ɏZ�ޖ���$ymname�̍Ō�����͂���$m{name}����̎莆<br><br>|;
			$in{comment} .= qq|$ymname�̍Ō�̌��t�w$m_message$ymes_win�x<br>|;
			$in{comment} .= qq|$ymname�̉摜��ϲ�߸���ɖ߂�܂���<br>|;
			$in{comment} .= qq|$ymname�����Ϻނ�����ꂽ�悤��<br>|;

			$bad_time = 0;
			&send_letter($yname);
			rename "$icondir/$yicon", "$userdir/$y_id/picture/$yicon"; 
			
			my $egg_no = $egg_nos[int(rand(@egg_nos))];
			&send_item($yname, 2, $egg_no, 0, 0, 1);
		}
		else {
			push @lines, $line;
		}
	}
	unshift @lines, $monster;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}



1; # �폜�s��
