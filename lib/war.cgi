$is_battle = 2;  # �����׸�2
sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
#================================================
# �푈 Created by Merino
#================================================
# $m{value} �ɂ� ���m�̔{��

$m{war_select_switch} = 0;

# ��R�ł��̎��̑���̾�́B��Ԑ擪�������f��p�̾��(�����\)
my @answers = ('�f��!', '�]�ނƂ��낾!', '�Ԃ蓢���ɂ��Ă����!', '��������!', '�悩�낤!', '�������낤!', '����ɂȂ낤!', '�������Ă���!');

# �w�`��(�����s�B���O�̕ύX�\)
my @war_forms = ('�U���w�`','�h��w�`','�ˌ��w�`');

# �V�K�̃{�[�i�X�^�C��(�푈������)���~�b�g
my $new_entry_war_c = 100;
=pod
# �����_���Z���N�g�p�R�}���h�ޔ�
my $m_cmd = $cmd;
if (!$m{war_select_switch} && $m_cmd >= 0 && $m_cmd <= 2) {
	while (1) {
		$m_cmd = int(rand(3));
		if ($m{rest_a} + $m{rest_b} + $m{rest_c} <= 0) {
			last;
		}
		if ($m_cmd eq '0' && $m{rest_a} > 0) {
			last;
		}
		if ($m_cmd eq '1' && $m{rest_b} > 0) {
			last;
		}
		if ($m_cmd eq '2' && $m{rest_c} > 0) {
			last;
		}
	}
}
=cut
#================================================
# ���p����
#================================================
sub is_satisfy {
	if ($time < $w{reset_time}) {
		$mes .= '�I����ԂȂ̂Ő푈�𒆎~���܂�<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (!defined $cs{strong}[$y{country}]) {
		$mes .= '�U�߂Ă��鍑�͏��ł��Ă��܂����̂ŁA�푈�𒆎~���܂�<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub tp_100 {
	$mes .= "$c_y�ɒ����܂���<br>";
	
	my $is_ambush = &_get_war_you_data; # �҂���������Ă��ꍇ�߂�l����
	$y{hp} = $y{max_hp};
	$y{mp} = $y{max_mp};

	# ���E��ݐ�����
	$m{turn} = int( rand(6)+7 );
	if ($m{value} > 1) {
		$m{turn} += 3;
		$y{sol} = int($rank_sols[$y{rank}]);
	}
	else {
		$y{sol} = int($rank_sols[$y{rank}] * $m{value});
	}

	# ��������Ȃ�
	if ($y{sol} > $cs{soldier}[$y{country}]) {
		$mes .= "$c_y�͕��s���̂悤���c<br>�ً}�Ɋ񂹏W�߂̍��������W���ꂽ<br>";
		$cs{strong}[$y{country}] -= int(rand(100)+100);
		$cs{strong}[$y{country}] = 1 if $cs{strong}[$y{country}] < 1;
		$y{sol_lv} = int( rand(10) + 45 );
		&write_cs;
	}
	else {
		$cs{soldier}[$y{country}] -= int($y{sol} / 3);
		$y{sol_lv} = 80;
		&write_cs;
	}

	# �҂�����
	if (($pets[$m{pet}][2] ne 'no_ambush' || ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) && $is_ambush) {
		$mes .= "$c_y��$y{name}������$y{sol}��$units[$y{unit}][1]���҂��������Ă��܂���!<br>";
		if ($y{unit} eq '11') { # �ÎE����
			my $v = int( $m{sol} * (rand(0.2)+0.2) );
			$m{sol} -= $v;
			$m{sol_lv} = int( rand(15) + 15 ); # 15 �` 29
			$mes .= "$units[$y{unit}][1]�ɂ��ÎE�ŁA$v�̕�������܂���!<br>";
		}
		elsif ($y{unit} eq '14') { # ���e����
			$m{sol_lv} = int( rand(10) + 5 ); # 5 �` 14
			$mes .= "$units[$y{unit}][1]�ɂ�錶�p�ŁA���m�B�͍������傫���m�C��������܂���!<br>";
		}
		else {
			$m{sol_lv} = int( rand(15) + 10 ); # 10 �` 24
			$mes .= "�҂������ɂ�蕺�m�B�͍������傫���m�C��������܂���!<br>";
		}
		if ($pets[$y{pet}][2] eq 'no_single' && $w{world} ne '17') {
			$y{wea} = 'no_single';
			$y{sol_lv} = int( rand(10) + 5);
			$mes .= "$pets[$y{pet}][1]�̗͂Ő�΂Ɉ�R�ł��ɂ͂Ȃ�܂��񂪕��̎m�C�͉������Ă��܂�<br>";
		}
		&write_world_news("$c_m��$m{name}��$c_y�ɍU�ߍ���$y{name}�̑҂������ɂ����܂���");
		
		&c_up('tam_c');

		my $yid = unpack 'H*', $y{name};
		if (-d "$userdir/$yid") {
			my $rank_name = &get_rank_name($m{rank}, $m{name});
			if ($m{super_rank}){
				$rank_name = '';
				$rank_name .= '��' for 1 .. $m{super_rank};
				$rank_name .= $m{rank_name};
			}
			open my $fh, ">> $userdir/$yid/ambush.cgi";
			print $fh "$m{name}/$rank_name/$units[$m{unit}][1]/����$m{lea}($date)<>";
			close $fh;
		}
	}
	else {
		$m{sol_lv} = 80;
		$mes .= "$c_y����$y{name}������$y{sol}�̕����o�Ă��܂���<br>";
	}

	# ���R�n�߯�
	if ($w{world} ne '17') {
		&use_pet('war_begin');
	}
	# �������Ă��鍑����̉��R
	if ($union) {
		my $v = int( $m{sol} * (rand(0.1)+0.1) );
		$m{sol} += $v;
		$mes .= "�Ȃ�ƁA$cs{name}[$union]����$v���̉��R���삯����!<br>";
	}
=pod
	# �z�v
	if ($m{war_select_switch}) {
		$m{rest_a} = 0;
		$m{rest_b} = 0;
		$m{rest_c} = 0;
		$y{rest_a} = 0;
		$y{rest_b} = 0;
		$y{rest_c} = 0;
		
		my $idx = 0;
		for my $cnt (1..$m{turn}) {
			unless ($units[$m{unit}][7][$idx]) {
				$idx = 0;
			}
			
			if ($units[$m{unit}][7][$idx] eq '1') {
				$m{rest_a}++;
			} elsif ($units[$m{unit}][7][$idx] eq '2') {
				$m{rest_b}++;
			} elsif ($units[$m{unit}][7][$idx] eq '3') {
				$m{rest_c}++;
			} else {
				if (rand(3) < 1) {
					$m{rest_a}++;
				} elsif (rand(2) < 1) {
					$m{rest_b}++;
				} else {
					$m{rest_c}++;
				}
			}
			$idx++;
		}
		$idx = 0;
		for my $cnt (1..$m{turn}) {
			unless ($units[$y{unit}][7][$idx]) {
				$idx = 0;
			}
			
			if ($units[$y{unit}][7][$idx] eq '1') {
				$y{rest_a}++;
			} elsif ($units[$y{unit}][7][$idx] eq '2') {
				$y{rest_b}++;
			} elsif ($units[$y{unit}][7][$idx] eq '3') {
				$y{rest_c}++;
			} else {
				if (rand(3) < 1) {
					$y{rest_a}++;
				} elsif (rand(2) < 1) {
					$y{rest_b}++;
				} else {
					$y{rest_c}++;
				}
			}
			$idx++;
		}
	} else {
		$m{rest_a} = $m{turn};
		$m{rest_b} = $m{turn};
		$m{rest_c} = $m{turn};
		$y{rest_a} = $m{turn};
		$y{rest_b} = $m{turn};
		$y{rest_c} = $m{turn};
	}
=cut
	if ($config_test) {
		$y{sol} /= 10;
	}
	
	$m{tp} += 10;
	&n_menu;
}

#================================================
sub tp_110 {
	$is_battle = 2;
	$m{act} += int(rand($m{turn})+$m{turn});
	
	$mes .= "����̍��̌��E��݂� $m{turn} ��݂ł�<br>";
	$mes .= "$m{name}�R $m{sol}�l VS $y{name}�R $y{sol}�l<br>";
	$mes .= '�U�ߍ��ސw�`��I��ł�������<br>';
#	$mes .= "���� $war_forms[0]:$m{rest_a}�� $war_forms[1]:$m{rest_b}�� $war_forms[2]:$m{rest_c}��<br>";
#	$mes .= "���� $war_forms[0]:$y{rest_a}�� $war_forms[1]:$y{rest_b}�� $war_forms[2]:$y{rest_c}��<br>";
	&menu(@war_forms,'�ދp');
	
	$m{tp} += 10;
	&write_cs;
}

#================================================
sub tp_120 { &tp_190; } # tp120���Ƒދp��
sub tp_130 { &tp_190; } # tp130���ƈ�R�ł���
sub tp_140 { # ��R�ł�
	require './lib/war_battle.cgi';

	if ($m{hp} <= 0) {
		$mes .= "��R�ł��ɔs��w������������$m{name}�̕����͐�ӂ�r�����A�G�R����̒ǌ��������S�ł��܂����c<br>";
		&write_world_news("$c_m��$m{name}��$c_y�ɐN�U�A$y{name}�ƈ�R�����������邪�s�k�������͔s�������悤�ł�");
		&war_lose;
	}
	elsif ($y{hp} <= 0) {
		$mes .= "�G�R��$y{name}�̔s�k�ɐ�ӂ�r�����܂����I���������������ȂǓG�ł͂���܂���<br>�G�R��ǌ����A���Ȃ�̔�Q��^���܂����I<br>";
		&war_win(1);

		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('single');
		}
	}
}

#================================================
# ٰ���ƭ� ��ݏI�������������邩�܂�
#================================================
sub loop_menu {
	$is_battle = 2;
	$mes .= "�c��$m{turn} ���<br>";
	$mes .= "$m{name}�R $m{sol}�l VS $y{name}�R $y{sol}�l<br>";
	$mes .= '�U�ߍ��ސw�`��I��ł�������<br>';
#	$mes .= "���� $war_forms[0]:$m{rest_a}�� $war_forms[1]:$m{rest_b}�� $war_forms[2]:$m{rest_c}��<br>";
#	$mes .= "���� $war_forms[0]:$y{rest_a}�� $war_forms[1]:$y{rest_b}�� $war_forms[2]:$y{rest_c}��<br>";
	&menu(@war_forms);
}
=pod
sub _rest_check {
	if ($m{rest_a} + $m{rest_b} + $m{rest_c} > 0) {
		if ($m_cmd eq '0' && $m{rest_a} <= 0) {
			$mes .= '�c��񐔂�����܂���<br>';
			return 0;
		}
		if ($m_cmd eq '1' && $m{rest_b} <= 0) {
			$mes .= '�c��񐔂�����܂���<br>';
			return 0;
		}
		if ($m_cmd eq '2' && $m{rest_c} <= 0) {
			$mes .= '�c��񐔂�����܂���<br>';
			return 0;
		}
	}
	return 1;
}
=cut
sub tp_190 {
#	if ($m_cmd >= 0 && $m_cmd <= 2 && &_rest_check) {
	if ($cmd >= 0 && $cmd <= 2) {
		--$m{turn};
=pod
		if ($m_cmd eq '0') {
			$m{rest_a}--;
		}
		if ($m_cmd eq '1') {
			$m{rest_b}--;
		}
		if ($m_cmd eq '2') {
			$m{rest_c}--;
		}
=cut
		$mes .= "�c��$m{turn}���<br>";
		&_crash;
		
		if ($m{sol} <= 0 && $y{sol} <= 0) {
			$mes .= "���R�Ƃ��ɉ�œI���Q���󂯐퓬�p�����s�\\�ƂȂ�܂���<br>$e2j{strong}�͗��w�c�Ƃ��ω��Ȃ�<br>";
			$m{value} < 1
				? &write_world_news("���҂���$c_y�ɐN�U�A$y{name}�̕����ɑj�܂ꌃ��̖��A���R��ł����悤�ł�")
				: &write_world_news("$c_m��$m{name}��$c_y�ɐN�U�A$y{name}�̕����ɑj�܂ꌃ��̖��A���R��ł����悤�ł�")
				;

			&war_draw;
		}
		elsif ($m{sol} <= 0) {
			$mes .= '�䂪�R�͑S�ł��܂����B�P�ނ��܂��c<br>';
			$m{value} < 1
				? &write_world_news("���҂���$c_y�ɐN�U�A$y{name}�̕����̑O�ɔs�ނ����悤�ł�")
				: &write_world_news("$c_m��$m{name}��$c_y�ɐN�U�A$y{name}�̕����̑O�ɔs�ނ����悤�ł�")
				;

			&war_lose;
		}
		elsif ($y{sol} <= 0) {
			$mes .= '�G���������j���܂���!!�䂪�R�̏����ł�!<br>';
			&war_win;
		}
		elsif ($m{turn} <= 0) {
			$mes .= "�퓬���E��݂𒴂��Ă��܂����c����ȏ�͐킦�܂���<br>$e2j{strong}�͗��w�c�Ƃ��ω��Ȃ�<br>";
			$m{value} < 1
				? &write_world_news("���҂���$c_y�ɐN�U���A$y{name}�̕����ɑj�܂�퓬���E���ް�����悤�ł�")
				: &write_world_news("$c_m��$m{name}��$c_y�ɐN�U���A$y{name}�̕����ɑj�܂�퓬���E���ް�����悤�ł�")
				;

			&war_draw;
		}
		else {
			$mes .= '�U�ߍ��ސw�`��I��ł�������<br>';
#			$mes .= "���� $war_forms[0]:$m{rest_a}�� $war_forms[1]:$m{rest_b}�� $war_forms[2]:$m{rest_c}��<br>";
#			$mes .= "���� $war_forms[0]:$y{rest_a}�� $war_forms[1]:$y{rest_b}�� $war_forms[2]:$y{rest_c}��<br>";

			# ��R�ł��o���m��
			if ($y{wea} eq 'no_single') {
				&menu(@war_forms,'�ދp');
				$m{tp} = 120;
			}
			elsif ( ((($pets[$m{pet}][2] eq 'war_single' && $w{world} ne '17') && int(rand($m{turn}+3)) == 0) || int(rand($m{turn}+15)) == 0 || ($pets[$y{pet}][2] eq 'ambush_single' && $w{world} ne '17')) && $m{unit} ne '18') {
				&menu(@war_forms,'��R�ł�');
				$m{tp} = 130;
			}
			elsif ($m{turn} < 4)  {
				&menu(@war_forms);
			}
			else {
				&menu(@war_forms,'�ދp');
				$m{tp} = 120;
			}
		}
	}
#	elsif ($m_cmd eq '3' && $m{tp} eq '120') {
	elsif ($cmd eq '3' && $m{tp} eq '120') {
		$m_mes = '�S�R�ދp!!';

		if ($m{turn} < 5) {
			$mes .= '�G�R�ɓ����ޘH���ǂ���A���͂�P�ނ͕s�\\�ł�<br>';
			$m{tp} = 190;
			&loop_menu;
		}
		# �ދp�ł���m��
		elsif ( int(rand($m{turn})) == 0) {
			$mes .= '�c�O�ł������𒆎~���ދp���܂�<br>';
			$m{value} < 1
				? &write_world_news("���҂���$c_y�ɐN�U���A$y{name}�̕����ƌ��B�]�V�Ȃ��P�ނ����͗l")
				: &write_world_news("$c_m��$m{name}��$c_y�ɐN�U���A$y{name}�̕����ƌ��B�]�V�Ȃ��P�ނ����͗l")
				;

			&war_escape;
		}
		else {
			$mes .= '�ދp�Ɏ��s���܂���<br>';
			$m{tp} = 190;
			&loop_menu;
		}
	}
#	elsif ($m_cmd eq '3' && $m{tp} eq '130') {
	elsif ($cmd eq '3' && $m{tp} eq '130') {
		$m_mes = "$y{name}�ƈ�R�ł��肢����!";

		my $v = int(rand(@answers));

		if ($v <= 0) {
			$y_mes = $answers[$v];
			$mes .= '��R�ł���f���܂���<br>';
			&loop_menu;
			$m{tp} = 190;
		}
		else {
			$y_mes = $answers[$v];
			
			$mes .= "$y{name}�Ɉ�R�ł���\\�����݁A���̐킢�̏��s���˂�����R�������s�Ȃ�����!<br>";
			$m{tp} = 140;
			&n_menu;
		}
	}
	else {
		&loop_menu;
		$m{tp} = 190;
	}
}

#================================================
# �w�`�팋��
#================================================
=pod
sub _ai {
	my @y_cmds = (0, 1, 2);
	my $y_cmd;

	if ($m{rest_a} + $m{rest_b} <= 0){
		if ($y{rest_b} > 0) {
			@y_cmds = (1);
		} elsif ($y{rest_c} > 0) {
			@y_cmds = (2);
		}
	} elsif ($m{rest_b} + $m{rest_c} <= 0) {
		if ($y{rest_c} > 0) {
			@y_cmds = (2);
		} elsif ($y{rest_a} > 0) {
			@y_cmds = (0);
		}
	} elsif ($m{rest_c} + $m{rest_a} <= 0) {
		if ($y{rest_a} > 0) {
			@y_cmds = (0);
		} elsif ($y{rest_b} > 0) {
			@y_cmds = (1);
		}
	} elsif ($m{rest_a} <= 0 && $y{rest_a} + $y{rest_b} > 0) {
		@y_cmds = (0, 1);
	} elsif ($m{rest_b} <= 0 && $y{rest_b} + $y{rest_c} > 0) {
		@y_cmds = (1, 2);
	} elsif ($m{rest_c} <= 0 && $y{rest_c} + $y{rest_a} > 0) {
		@y_cmds = (0, 2);
	}

	while (1) {
		$y_cmd = $y_cmds[int(rand(@y_cmds))];
		if ($y{rest_a} + $y{rest_b} + $y{rest_c} <= 0) {
			last;
		}
		if ($y_cmd eq '0' && $y{rest_a} > 0) {
			last;
		}
		if ($y_cmd eq '1' && $y{rest_b} > 0) {
			last;
		}
		if ($y_cmd eq '2' && $y{rest_c} > 0) {
			last;
		}
	}
	return $y_cmd;
}
=cut
sub _crash {
=pod
	my $y_cmd = &_ai;
	if ($y_cmd eq '0') {
		$y{rest_a}--;
	}
	if ($y_cmd eq '1') {
		$y{rest_b}--;
	}
	if ($y_cmd eq '2') {
		$y{rest_c}--;
	}
	
	$m_mes = $war_forms[$m_cmd];
	$y_mes = $war_forms[$y_cmd];
=cut
	my $y_cmd = int(rand(3));

	$m_mes = $war_forms[$cmd];
	$y_mes = $war_forms[$y_cmd];

	my $result = 'lose';
#	if ($m_cmd eq '0') {
	if ($cmd eq '0') {
		$result = $y_cmd eq '1' ? 'win'
				: $y_cmd eq '2' ? 'lose'
				:				  'draw'
				;
	}
#	elsif ($m_cmd eq '1') {
	elsif ($cmd eq '1') {
		$result = $y_cmd eq '2' ? 'win'
				: $y_cmd eq '0' ? 'lose'
				:				  'draw'
				;
	}
#	elsif ($m_cmd eq '2') {
	elsif ($cmd eq '2') {
		$result = $y_cmd eq '0' ? 'win'
				: $y_cmd eq '1' ? 'lose'
				:				  'draw'
				;
	}
	
	my $m_lea = $m{lea};
	my $y_lea = $y{lea};
	my $m_min_wea;
	if($weas[$m{wea}][2] eq '��'){
		$m_min_wea = 1;
	}elsif($weas[$m{wea}][2] eq '��'){
		$m_min_wea = 6;
	}elsif($weas[$m{wea}][2] eq '��'){
		$m_min_wea = 11;
	}elsif($weas[$m{wea}][2] eq '��'){
		$m_min_wea = 16;
	}elsif($weas[$m{wea}][2] eq '��'){
		$m_min_wea = 21;
	}elsif($weas[$m{wea}][2] eq '��'){
		$m_min_wea = 26;
	}elsif($m{wea} == 0){
		$m_min_wea = 0;
	}else{
		$m_min_wea = 33;
	}
	my $y_min_wea;
	if($weas[$y{wea}][2] eq '��'){
		$y_min_wea = 1;
	}elsif($weas[$y{wea}][2] eq '��'){
		$y_min_wea = 6;
	}elsif($weas[$y{wea}][2] eq '��'){
		$y_min_wea = 11;
	}elsif($weas[$y{wea}][2] eq '��'){
		$y_min_wea = 16;
	}elsif($weas[$y{wea}][2] eq '��'){
		$y_min_wea = 21;
	}elsif($weas[$y{wea}][2] eq '��'){
		$y_min_wea = 26;
	}else{
		$y_min_wea = 33;
	}
	$m_wea_modify = $weas[$m{wea}][5] - $weas[$m_min_wea][5];
	$m_wea_modify -= 100 unless $m{wea};
	$m_wea_modify = 100 if ($m{wea} == 14);
	$m_wea_modify = 0 if ($m{wea} == 31);
	$m_wea_modify = 100 if ($m{wea} == 32);
	$m_lea += $m_wea_modify;
	$m_lea =  0 if ($m_lea < 0);
	$y_wea_modify = $weas[$y{wea}][5] - $weas[$y_min_wea][5];
	$y_wea_modify -= 100 unless $y{wea};
	$y_wea_modify = 100 if ($y{wea} == 14);
	$y_wea_modify = 0 if ($y{wea} == 31);
	$y_wea_modify = 100 if ($y{wea} == 32);
	$y_lea += $y_wea_modify;
	$y_lea -= 100 unless $y{wea};
	$y_lea =  0 if ($y_lea < 0);
	
	my $m_attack = ($m{sol}*0.1 + $m_lea*2) * $m{sol_lv} * 0.01 * $units[$m{unit}][4] * $units[$y{unit}][5];
	my $y_attack = ($y{sol}*0.1 + $y_lea*2) * $y{sol_lv} * 0.01 * $units[$y{unit}][4] * $units[$m{unit}][5];

	if (&is_tokkou($m{unit}, $y{unit})) {
		$is_m_tokkou = 1;
		$m_attack *= 1.3;
		$y_attack *= 0.5;
	}
	if (&is_tokkou($y{unit}, $m{unit})) {
		$is_y_tokkou = 1;
		$m_attack *= 0.5;
		$y_attack *= 1.3;
	}
	$m_attack = $m_attack < 150 ? int( rand(50)+100 ) : int( $m_attack * (rand(0.3) +0.9) );
	$y_attack = $y_attack < 150 ? int( rand(50)+100 ) : int( $y_attack * (rand(0.3) +0.9) );
	
	if ($result eq 'win') {
		$m_attack = int($m_attack * 1.3);
		$y_attack = int($y_attack * 0.5);
		
		$m{sol_lv} += int(rand(5)+10);
		$y{sol_lv} -= int(rand(5)+10);

		$mes .= qq|�����R��Q$y_attack <font color="#FF0000">���G�R��Q$m_attack</font><br><br>|;
	}
	elsif ($result eq 'lose') {
		$m_attack = int($m_attack * 0.5);
		$y_attack = int($y_attack * 1.3);
		$m{sol_lv} -= int(rand(5)+10);
		$y{sol_lv} += int(rand(5)+10);
	
		$mes .= qq|<font color="#FF0000">�����R��Q$y_attack</font> ���G�R��Q$m_attack<br><br>|;
	}
	else {
		$m{sol_lv} += int(rand(3)+5);
		$y{sol_lv} += int(rand(3)+5);
	
		$mes .= qq|�����R��Q$y_attack ���G�R��Q$m_attack<br><br>|;
	}
	
	$m{sol} -= $y_attack;
	$y{sol} -= $m_attack;
	$m{sol} = 0 if $m{sol} < 0;
	$y{sol} = 0 if $y{sol} < 0;

	$m{sol_lv} = $m{sol_lv} < 10  ? int( rand(11) )
			   : $m{sol_lv} > 100 ? 100
			   :					$m{sol_lv}
			   ;
	$y{sol_lv} = $y{sol_lv} < 10  ? int( rand(11) )
			   : $y{sol_lv} > 100 ? 100
			   :					$y{sol_lv}
			   ;
}


#================================================
# �K���Ɠ������������炢�̑���������_���ŒT���B������Ȃ��ꍇ�͗p�ӂ��ꂽNPC
#================================================
sub _get_war_you_data {
	my @lines = &get_country_members($y{country});
	
	my $war_mod = &get_modify('war');
	
	if (@lines >= 1) {
		my $retry = ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000      ? 0 # ���E��y�S�ǁz�U�߂����̍��͂�3000�ȉ��̏ꍇ�͋���NPC
				  : $w{world} eq $#world_states && $y{country} eq $w{country} ? 1 # ���E��y�Í��z�U�߂�����NPC���Ȃ���ڲ԰ϯ�ݸނ͂P��
				  : $w{world} eq $#world_states - 5 ? 3 # ���E��y�ّ��z��ڲ԰ϯ�ݸނ�3��
				  : ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 15 && $w{world} ne '17') ? 	1
				  : ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 10 && $w{world} ne '17') ? 	2
				  :																5 # ���̑���ڲ԰ϯ�ݸނ��ō��T��ق���ײ����
				  ;
		$retry = int($retry / $war_mod);
		my %sames = ();
		for my $i (1 .. $retry) {
			my $c = int(rand(@lines));
			next if $sames{$c}++; # �����l�Ȃ玟
			
			$lines[$c] =~ tr/\x0D\x0A//d; # = chomp �]���ȉ��s�폜
			
			my $y_id = unpack 'H*', $lines[$c];
			
			# ���Ȃ��ꍇ��ؽĂ���폜
			unless (-f "$userdir/$y_id/user.cgi") {
				require "./lib/move_player.cgi";
				&move_player($lines[$c], $y{country},'del');
				next;
			}
			my %you_datas = &get_you_datas($y_id, 1);
			
			$y{name} = $you_datas{name};
			
			next if $you_datas{lib} eq 'prison'; # �S���̐l�͏���
			next if $you_datas{lib} eq 'war'; # �푈�ɏo�Ă���l�͏���
			next if ($pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 20 && $w{world} ne '17'); # ��20̧���
			
			if ($m{win_c} < $new_entry_war_c) {
				if ( $m{rank} >= ($you_datas{rank} + int(rand(2)) ) && 20 >= rand(abs($m{lea}-$you_datas{lea})*0.1)+5 ) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
			} elsif ($cs{disaster}[$y{country}] eq 'mismatch' && $cs{disaster_limit}[$y{country}] >= $time) {
				# �w���n��������
				if ( $you_datas{rank} <= $m{rank}) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
			} else {
				# �҂��������Ă���l��������
				if ( $you_datas{value} eq 'ambush' && $max_ambush_hour * 3600 + $you_datas{ltime} > $time) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 1;
				}
				# �K���Ɠ������߂��l�B���̐�����0�ɂ���΂�苭���̋߂�����傫������ΐF�X�ȑ���
				elsif ( 2 >= rand(abs($m{rank}-$you_datas{rank})+2) && 20 >= rand(abs($m{lea}-$you_datas{lea})*0.1)+5 ) {
					# set %y
					while (my($k,$v) = each %you_datas) {
						next if $k =~ /^y_/;
						$y{$k} = $v;
					}
					$y_mes = $you_datas{mes};
					return 0;
				}
			}
		}
	}
	
	# ���޳ or NPC
	($pets[$m{pet}][2] eq 'no_shadow' && $w{world} ne '17') || int(rand(3 / $war_mod)) == 0 || ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7'))
		? &_get_war_npc_data : &_get_war_shadow_data;
}

#================================================
# NPC [0] �` [4] �� 5�l([0]���� >>> [4]�ア)
#================================================
sub _get_war_npc_data {
	&error("���荑($y{country})��NPC�f�[�^������܂���") unless -f "$datadir/npc_war_$y{country}.cgi";
	
	my $war_mod = &get_modify('war');
	
	require "$datadir/npc_war_$y{country}.cgi";

	my $v = $m{lea} > 600 ? 0
		  : $m{lea} > 400 ? int(rand(2) * $war_mod)
		  : $m{lea} > 250 ? int((rand(2)+1) * $war_mod)
		  : $m{lea} > 120 ? int((rand(2)+2) * $war_mod)
		  :                 int((rand(2)+3) * $war_mod)
		  ;
	if($pets[$m{pet}][2] eq 'no_shadow' && $w{world} ne '17'){
		$v += int(rand($m{pet_c}*0.2));
	}

	# ���ꍑ�̏ꍇ��NPC���
	my($c1, $c2) = split /,/, $w{win_countries};
	# ���͒Ⴂ�ꍇ�͋���NPC
	if ($cs{strong}[$y{country}] <= 3000) {
		$v = 0;
	}
	elsif ($c1 eq $y{country} || $c2 eq $y{country}) {
		$v += 1;
	}
	$v = $#npcs if $v > $#npcs;
	
	while ( my($k, $v) = each %{ $npcs[$v] }) {
		unless($k eq 'name' && $pets[$m{pet}][2] eq 'no_shadow' && $m{pet_c} >= 10 && rand(2) < 1){
			$y{$k} = $v;
		}
	}
	$y{unit} = int(rand(@units));
	$y{icon} ||= $default_icon;
	$y{mes_win} = $y{mes_lose} = '';
	
	return 0;
}

#================================================
# ���޳
#================================================
sub _get_war_shadow_data {
	# ���͒Ⴂ�ꍇ��1.5�{
	my $pinch = $cs{strong}[$y{country}] <= 3000 ? 1.5 : 1;
	
	for my $k (qw/max_hp max_mp at df mat mdf ag cha lea/) {
		$y{$k} = int($m{$k} * $pinch);
	}
	for my $k (qw/wea skills mes_win mes_lose icon rank unit/) {
		$y{$k} = $m{$k};
	}
	$y{rank} += 2;
	$y{rank} = $#ranks if $y{rank} > $#ranks;

	# ���ꍑ�̏ꍇ��NPC���
	my($c1, $c2) = split /,/, $w{win_countries};
	$y{rank} -= 2 if $c1 eq $y{country} || $c2 eq $y{country};

	$y{name}  = '���޳�R�m(NPC)';
	
	return 0;
}


#================================================
# ���킪���U(�L��)���ǂ���
#================================================
sub is_tokkou {
	my($m_unit, $y_unit) = @_;
	
	for my $tokkou (@{ $units[$m_unit][6] }) {
		return 1 if $tokkou eq $y_unit;
	}
	return 0;
}


#================================================
# _war_result.cgi�ɏ������ʂ�n��
#================================================
sub war_win {
	my $is_single = shift;
	require "./lib/_war_result.cgi";
	&war_win($is_single);
}
sub war_lose {
	require "./lib/_war_result.cgi";
	&war_lose;
}
sub war_draw {
	require "./lib/_war_result.cgi";
	&war_draw;
}
sub war_escape {
	require "./lib/_war_result.cgi";
	&war_escape;
}


1; # �폜�s��
