my $this_file = "$logdir/colosseum/champ_$m{stock}.cgi";
#================================================
# ���Z�� Created by Merino
#=================================================
# $m{stock} ��ذ�� $m{value} �� ׳��ސ�

# ���̉񐔈ȏ�h�q����Ǝ�������
my $limit_defence_c = 50;

# �Δ�ɋL�^
my $legend_defence_c = 25;

# ׳�������
my @round_titles = ('����','������','������');

# �i��҂̾��(1+2�̑g�ݍ��킹)
my @coms_1 = ('�Ȃ��Ȃ���','��t�]��','��߰�ި���','�f���炵��','���������̂���','�S�C����','��ط�؂�','����I��','������','�|�p�I��','�ڲ�ް��','�唗�͂�','�悭�킩��Ȃ�');
my @coms_2 = ('����','����','�킢','�U��','�U�h','����','�Z','�C��','���','����','�ꌂ');

# ذ��(�ǉ������ꍇ�w./log/colosseum/�x�Ɂwchamp_?.cgi�x̧�ق�ǉ����邱��)
my @menus = (
#	[0]���O,[1]��������,[2]�h�q��,[3]�o���,[4]�߯Đ���
	['������ذ��',	800,	1000,	1000, 1],
	['�޷�Űذ��',	1500,	1000,	1000, 1],
	['�����ذ��',	3000,	2000,	2000, 1],
	['ϼ޼��ذ��',	0,		2000,	2000, 1],
	['�ټެ�ذ��',	0,		2000,	2000, 1],
	['����ߵ�ذ��',	0,		3000,	3000, 1],
	['����ذ��',	0,		3000,	3000, 0],
);

my %plus_needs = (
	'ϼ޼��ذ��'	=> ['����̑����������w���A���A���x�̂�',		sub{ $weas[$m{wea}][2] =~ /��|��|��/ }],
	'�ټެ�ذ��'	=> ['����̑����������w���A���A���x�̂�',		sub{ $weas[$m{wea}][2] =~ /��|��|��/ }],
);

#================================================
# ���p����
#================================================
sub is_satisfy {
	if ($m{tp} <= 1 && $m{hp} < 10) {
		$mes .= "���Z��ɎQ������̂�$e2j{hp}�����Ȃ����܂�<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ��J���Ă���ꍇ�͍s���Ȃ�
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	$m{tp} = 1 if $m{tp} > 1;
	$m{turn} = 0;
	my $m_st = &m_st;
	$mes .= "$m{name}�̋���[ $m_st ]<br>";
	$mes .= "�����͋��҂��W�܂铬�Z��ł�<br>�O��A���ŏ����i�ނ�����ߵ݂ɂȂ�܋����o�܂�<br>";
	$mes .= "����ߵ݂ɂȂ�A�h�q���邱�Ƃł��܂��܋������炦�܂�<br>";
	$mes .= "<hr>�ǂ�ذ�ނɒ��킵�܂���?<br>";
	for my $i (0 .. $#menus) {
		$mes .= $menus[$i][1] ? "$menus[$i][0]�F����$menus[$i][1]�܂�<br>"
			  : "$menus[$i][0]�F����������<br>";
	}
	
	&menu('��߂�',map{ $_->[0] } @menus);
}

sub tp_1 {
	return if &is_ng_cmd(1..$#menus+1);
	
	--$cmd;
	$m{tp} = 100;
	$m{stock} = $cmd;
	$mes .= "$menus[$m{stock}][0] �ɏo�ꂷ��ɂ́A$menus[$m{stock}][3] G������܂�<br>";
	$mes .= "���킵�܂���?<br>";
	
	&champ_statuses($m{stock});
	
	&menu('��߂�','���킷��');
}


#================================================
# �o�꾯�
#================================================
sub tp_100 {
	if ($cmd eq '1') {
		if ($menus[$m{stock}][1] <= 0 || &m_st <= $menus[$m{stock}][1]) {
			if (&is_champ) {
				$mes.="$m{name}�I��͖h�q�҂ł��̂Œ��킷�邱�Ƃ͂ł��܂���<br>";
				&begin;
			}
			elsif ($m{money} >= $menus[$m{stock}][3]) {
				if (!defined $plus_needs{$menus[$m{stock}][0]} || &{ $plus_needs{$menus[$m{stock}][0]}[1] }) {
					$m{money} -= $menus[$m{stock}][3];
					$m{tp} = 110;
					$m{value} = 0;
					$mes .= "$menus[$m{stock}][0] �ɏo�ꂵ�܂�!<br>";
					&n_menu;
				}
				else {
					$mes .= "$menus[$m{stock}][0]�ɏo��ł�������� $plus_needs{$menus[$m{stock}][0]}[0] �ł�<br>";
					&begin;
				}
			}
			else {
				$mes .= '����������܂���<br>';
				&begin;
			}
		}
		else {
			$mes .= "$menus[$m{stock}][0]�ɏo��ł���̂͋�����$menus[$m{stock}][1]�ȉ��̑I�肾���ł�<br>";
			&begin;
		}
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin;
	}
}


#================================================
# �D�� or �����J�n�̱ųݽ
#================================================
sub tp_110 {
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	my @lines = <$fh>;
	close $fh;
	
	# �h�q�Ґ��ɂ��׳��ސ�����
	if ($m{value} <= 0) {
		$m{value} = @lines == 0 ? 3 # �h�q�҂����Ȃ��̂ł����Ȃ�D��
				  : @lines == 1 ? 2 # ��������
				  : @lines == 2 ? 1 # ����������
				  :               0 # ���킩��
				  ;
	}
	my $battles = @lines > 2 ? 0:@lines - 3;
	
	if ($m{value} > 2) { # �D��
		&c_up('col_c') for (1..$m{value});

		--$m{value};
		
		# �h�q�ҏ�����������
		&_rewrite_champ;
		
		my $v = $menus[$m{stock}][2] * 10;
		$m{money} += $v;
		$mes.="$menus[$m{stock}][0]�ɐV���ȗD���҂��a�����܂���!<br>";
		$mes.="$m{name}�I��ł�!$m{name}�u$m{mes_win}�v<br>";
		$mes.="�܋��� $v G�������܂�!<br>";
		$mes.="����ł͍Ă�$m{name}�I��ɔ����!<br>";
		if ($menus[$m{stock}][4]) {
			$m{egg_c} += int(rand(20)+30) if $m{egg};
		} else {
			$m{egg_c} += int(rand(10)+5) if $m{egg};
		}
		$m{act} += 10;
		&write_colosseum_news(qq| <i>$menus[$m{stock}][0] �V����ߵ� <font color="$cs{color}[$m{country}]">$m{name}</font> �a��</i>|, 1);
		&send_twitter("$menus[$m{stock}][0] �V����ߵ� $m{name} �a��");
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('colosseum_top');
		}
		
		&refresh;
		&n_menu;
	}
	else {
		# �����ް��擾
		($y{name},$y{country},$y{max_hp},$y{max_mp},$y{at},$y{df},$y{mat},$y{mdf},$y{ag},$y{cha},$y{wea},$y{skills},$y{mes_win},$y{mes_lose},$y{icon},$y{defence_c},$y{wea_name},$y{gua}) = map { $_ =~ tr/\x0D\x0A//d; $_; } split /<>/, $lines[$battles + $m{value}];
		$y{hp}  = $y{max_hp};
		$y{mp}  = $y{max_mp};
		$y{icon} = $default_icon unless -f "$icondir/$y{icon}";
		
		$mes .= $coms_1[int(rand(@coms_1))].$coms_2[int(rand(@coms_2))]."�ł�����!����ł͈�������<br>" if $m{value} > 0;
		$mes .= "$menus[$m{stock}][0] $round_titles[$m{value}]<br>";
		$mes .= "$m{name} VS $y{name}<br>";
		$mes .= "�����n��!<br>";
		&n_menu;
		$m{tp} = 120;
	}
}

#================================================
# �퓬����
#================================================
sub tp_120 {
	if($menus[$m{stock}][4]) {
		require './lib/colosseum_battle.cgi';
	} else {
		require './lib/battle.cgi';
	}

	if ($m{hp} <= 0) {
		&col_lose;
	}
	elsif ($y{hp} <= 0) {
		&col_win;
	}
}

#================================================
# ����
#================================================
sub col_lose {
	$m{act} += $m{value} * 5 + 5;
	$mes .= '�c�O�ł����B�܂����킵�ɗ��Ă�����<br>';
	&_defence_c_up;
	&refresh;
	&n_menu;
}
#================================================
# ����
#================================================
sub col_win {
	my $v = int( rand(10)+ 5 );
	$v = &use_pet('colosseum', $v);
	$m{exp} += $v;
	$m{egg_c} += int(rand(2)+1) if $m{egg};

	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
	&write_colosseum_news(qq|$menus[$m{stock}][0]$round_titles[$m{value}] �� �����<font color="$cs{color}[$m{country}]">$m{name}</font> VS �h�q��<font color="$cs{color}[$y{country}]">$y{name}</font> �~|);
	&send_twitter("$menus[$m{stock}][0]$round_titles[$m{value}] �� �����$m{name} VS �h�q��$y{name} �~");
	
	$m{tp} = 110;
	++$m{value}; # ׳��޶��ı���

	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('colosseum');
	}

	&n_menu;
}

#================================================
# �h�q�����ı���
#================================================
sub _defence_c_up {
	my $count = 0;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��J���܂���");
	eval { flock $fh, 2; };
	my @temp_lines = <$fh>;
	my $count_sub = @temp_lines;
	while (my $line = shift @temp_lines) {
		if ($count == $count_sub - 3 + $m{value}) {
			my($name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$defence_c,$wea_name,$gua) = map { $_ =~ tr/\x0D\x0A//d; $_; } split /<>/, $line;
			++$defence_c;
			
			&write_colosseum_news(qq|$menus[$m{stock}][0]$round_titles[$m{value}] �~ �����<font color="$cs{color}[$m{country}]">$m{name}</font> VS �h�q��<font color="$cs{color}[$y{country}]">$y{name}</font> �� �h�q$defence_c|);
			&send_twitter("$menus[$m{stock}][0]$round_titles[$m{value}] �~ �����$m{name} VS �h�q��$y{name} �� �h�q$defence_c");

			# �K�萔�ȏゾ�Ǝ������ށ��Δ�
			if ($defence_c >= $limit_defence_c) {
				&_send_money_and_col_c_up($name, $defence_c);
				&write_colosseum_news(qq| <i><font color="$cs{color}[$country]">$name</font>��$menus[$m{stock}][0]��$defence_c��̖h�q���ʂ����h�q�҂����ނ��܂���</i>|);
				&write_legend("champ_$m{stock}", "$cs{name}[$country]��$name��$menus[$m{stock}][0]��$defence_c��̖h�q���ʂ���", 1, $name);
				&send_twitter("$name��$menus[$m{stock}][0]��$defence_c��̖h�q���ʂ����h�q�҂����ނ��܂���");
			}
			else {
				push @lines, "$name<>$country<>$max_hp<>$max_mp<>$at<>$df<>$mat<>$mdf<>$ag<>$cha<>$wea<>$skills<>$mes_win<>$mes_lose<>$icon<>$defence_c<>$wea_name<>$gua<>\n";
			}
		}
		else {
			push @lines, $line;
		}
		++$count;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#================================================
# �V����ߵݒa���B
#================================================
sub _rewrite_champ {
	my $line = '';
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��J���܂���");
	eval { flock $fh, 2; };
	my @lines = <$fh>;
	push @lines, "$m{name}<>$m{country}<>$m{max_hp}<>$m{max_mp}<>$m{at}<>$m{df}<>$m{mat}<>$m{mdf}<>$m{ag}<>$m{cha}<>$m{wea}<>$m{skills}<>$m{mes_win}<>$m{mes_lose}<>$m{icon}<>0<>$m{wea_name}<>$m{gua}<>\n";
	while(@lines > 3){
		$line = shift @lines;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	if ($line) {
		my($name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$defence_c,$wea_name,$gua) = split /<>/, $line;

		# �Δ�ɏ�������
		if ($defence_c >= $legend_defence_c) {
			&write_legend("champ_$m{stock}", "$cs{name}[$country]��$name��$menus[$m{stock}][0]��$defence_c��̖h�q���ʂ���", 1, $name);
			&write_colosseum_news(qq| <i><font color="$cs{color}[$country]">$name</font>��$menus[$m{stock}][0]��$defence_c��̖h�q���ʂ����h�q�҂����ނ��܂���</i>|);
			&send_twitter("$name��$menus[$m{stock}][0]��$defence_c��̖h�q���ʂ����h�q�҂����ނ��܂���");
		}
		else {
			&write_colosseum_news(qq| <b><font color="$cs{color}[$country]">$name</font>��$menus[$m{stock}][0]��$defence_c��̖h�q���ʂ����h�q�҂����ނ��܂���</b>|, 1, $name);
			&send_twitter("$name��$menus[$m{stock}][0]��$defence_c��̖h�q���ʂ����h�q�҂����ނ��܂���");
		}
		
		&_send_money_and_col_c_up($name, $defence_c);
	}
}

#================================================
# ���ގ҂ɂ��������Ɠ��Z��n���x���グ��
#================================================
sub _send_money_and_col_c_up {
	my($name, $defence_c) = @_;

	my $y_id = unpack 'H*', $name;
	if (-f "$userdir/$y_id/user.cgi") {
		&send_money($name, $menus[$m{stock}][0], $defence_c * $menus[$m{stock}][2]);

		my %datas = &get_you_datas($y_id, 1);
		$datas{col_c} += $defence_c;
		&regist_you_data($name, 'col_c', $datas{col_c});
	}
}


#================================================
# �������h�q�҂��ǂ���
#================================================
sub is_champ {
	open my $fh, "< $logdir/colosseum/champ_$m{stock}.cgi" or &error("$logdir/colosseum/champ_$m{stock}.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my $name = (split/<>/,$line)[0];
		return 1 if $name eq $m{name};
	}
	close $fh;
	return 0;
}

#================================================
# �h�q�҂̃X�e�[�^�X�\��
#================================================
sub champ_statuses {
	my $champ_stage = shift;
	
	open my $fh, "$logdir/colosseum/champ_$champ_stage.cgi" or &error("$logdir/colosseum/champ_$champ_stage.cgi̧�ق��ǂݍ��߂܂���");
	my @lines = <$fh>;
	close $fh;
	
	$mes .= "<hr>�h�q��<br>";
	my $count = @lines;
	for my $line (@lines) {
		my($name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$defence_c,$wea_name,$gua) = map { $_ =~ tr/\x0D\x0A//d; $_; } split /<>/, $line;
		
		my $round_c = @round_titles - $count;
		my $wname = $wea_name ? $wea_name : $weas[$wea][1];
		$mes .= "$round_titles[$round_c]:$name(�h�q$defence_c)/$wname/$guas[$gua][1]/$e2j{hp}$max_hp/$e2j{mp}$max_mp/$e2j{at}$at/$e2j{df}$df/$e2j{mat}$mat/$e2j{mdf}$mdf/$e2j{ag}$ag<br>";
		--$count;
	}
}


1; # �폜�s��
