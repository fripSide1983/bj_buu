my $this_monster_file = "$logdir/monster/horror.cgi";
#=================================================
# �̎��� Created by Merino
#=================================================

# ���яE���m��(����1)
my $get_item_par = 20;

my @egg_nos = (12, 22, 24, 26, 35, 39);

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time);
	if ($hour < 1 || $hour > 3) {
		$mes .= "�̎������鎞�Ԃ���Ȃ���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	if ($m{tp} <= 1 && $m{hp} < 10) {
		$mes .= "�̎�������̂�$e2j{hp}�����Ȃ����܂�<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ��J���Ă���ꍇ�͍s���Ȃ�
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	$m{turn} = 0;
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= '�̎����ɍs���܂�<br>';
	$mes .= '�ǂ��Ɍ������܂���?<br>';
	
	my $m_st = &m_st;
	my @menus = ('��߂�', '�s��');
	&menu(@menus);
}
sub tp_1 {
	if ($cmd) {
		&_get_hunt_you_data;
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin;
	}
}

#=================================================
# Get ����f�[�^
#=================================================
sub _get_hunt_you_data {
	my $line = '';
	open my $fh, "< $this_monster_file" or &error("$this_monster_filȩ�ق�����܂���");
	$line = <$fh>;
	close $fh;

	my @datas = split /<>/, $line;
	my $i = 0;
	for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
		$y{$k} = $datas[$i];
		++$i;
	}
	$y{hp} = $y{max_hp};
	$y{mp} = $y{max_mp};
	$y{icon} = $default_icon unless -f "$icondir/$y{icon}";
	$y{wea_name} = '';
	$y{gua} = 0;
	if ( rand($m{cha}) < rand($y{cha}) ) {
		$m{tp} = 200;
		$mes .= "$y{name} ���P���������Ă��܂���<br>";
		&n_menu;
	}
	else {
		$m{tp} = 100;
		$mes .= "$y{name} �����܂�<br>";
		&menu('�키','������');
	}
}

#=================================================
# �키 or ������
#=================================================
sub tp_100 {
	if ($cmd eq '0') {
		$mes .= "$y{name} �Ɛ킢�܂�<br>";
		$m{tp} = 200;
		&n_menu;
	}
	elsif ( rand($m{ag}) > rand($y{ag}) ) {
		$mes .= '�����܂���<br>';
		&begin;
	}
	else {
		$mes .= '�������܂���ł����B�퓬�Ԑ��ɓ���܂�<br>';
		$m{tp} = 200;
		&n_menu;
	}
}

#=================================================
# �퓬
#=================================================
sub tp_200 {
	require './lib/hunting_battle.cgi';

	# ����
	if ($m{hp} <= 0) {
		$m{pop_vote}++;
		$mes .= "���[�����E����<br>";
		$m{act} += 20;
		&refresh;
		&n_menu;
	}
	# ����
	elsif ($y{hp} <= 0) {
		$m{pop_vote}++;
		$mes .= "���[�����E����<br>";
		# İ�ٽð������������҂��ƌo���l���Ȃ�
		my $y_st = &y_st;
		my $st_lv = &st_lv($y_st);
		my $v = $st_lv eq '2' ? int( rand(10) + 10) 
			  : $st_lv eq '0' ? int( rand(3)  + 1)
			  :                 int( rand(5)  + 5)
			  ;
		my $vv = int(3000 + $y_st * 0.3);
		
		$m{exp} += $v;
		$m{act} += 20;
		$m{egg_c} += int(rand(60)+70) if $m{egg};
		$m{money} += $vv;
		$mes .= "$v ��$e2j{exp}�� $vv G����ɓ���܂���<br>";
		
		# ���ѹޯ�
		&_get_item if int(rand($get_item_par)) == 0;
		
		$mes .= '�̎����𑱂��܂���?<br>';
		&menu('������','��߂�');
		$m{tp} += 10;
	}
}

#=================================================
# �p�� or ��߂�
#=================================================
sub tp_210 {
	if ($cmd eq '0') {
		&_get_hunt_you_data;
	}else {
		$mes .= '�̎������I�����܂�<br>';
		&refresh;
		&n_menu;
	}
}

#=================================================
# ����(�Ϻ�)�E������
#=================================================
sub _get_item {
	my $egg_no = $egg_nos[int(rand(@egg_nos))];
	
	$mes .= qq|<font color="#FFCC00">$eggs[$egg_no][1]���E���܂���!</font><br>|;
	if ($m{is_full}) {
		$mes .= "�������A�a���菊�������ς��Ȃ̂�$eggs[$egg_no][1]��������߂܂���<br>";
	}
	else {
		$mes .="$eggs[$egg_no][1]��a���菊�ɑ���܂���!<br>";
		&send_item($m{name}, 2, $egg_no);
	}
}

#=================================================
# �K���ȃA�C�R����\��
#=================================================
sub random_icon {
	my $ricon;
	my @icons = ();
	opendir my $dh, "$icondir" or &error('�A�C�R���t�H���_���J���܂���');
	while(my $file_name = readdir $dh){
		next if $file_name =~ /^\./;
		next if $file_name =~ /\.html$/;
		next if $file_name =~ /\.db$/;
		
		push @icons, $file_name;
	}
	$ricon = @icons[int(rand(@icons))];
	if($ricon eq ''){
		$ricon = $default_icon;
	}
	return $ricon;
}

#=================================================
# �����X�^�[���x���A�b�v
#=================================================
sub monster_lv_up {
	my $up = shift;

	my @lines = ();
	open my $fh, "+< $this_monster_file" or &error("$this_monster_filȩ�ق�����܂���");
	eval { flock $fh, 2 };
	$line = <$fh>;

	my @datas = split /<>/, $line;
	for my $i (2..9) {
		if ($up) {
			if (rand(30) < 1) {
				$datas[$i]++;
			}
		} else {
			if (rand(10) < 1) {
				$datas[$i]--;
			}
		}
	}
	my $new_line = join '<>', @datas;
	push @lines, "$new_line<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


1; # �폜�s��
