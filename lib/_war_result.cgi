use File::Copy::Recursive qw(rcopy);
use File::Path;
#=================================================
# �푈���� Created by Merino
#=================================================
# war.cgi�ɂ����Ă��������ǂ����Ⴒ����ɂȂ肻���Ȃ̂ŕ���

# �~�o�l��
my $max_rescue = 1;

#=================================================
# ��������
#=================================================
sub war_draw {
	&c_up('draw_c');
	my $v = int( rand(11) + 10 );
	$m{rank_exp} -= int( (rand(16)+15) * $m{value} );
	$m{exp} += $v;
	&write_yran('war', 1, 1);

	$mes .= "$m{name}�ɑ΂���]����������܂���<br>";
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
	
	my $is_rewrite = 0;
	if ($m{sol} > 0) {
		$cs{soldier}[$m{country}] += $m{sol};
		$is_rewrite = 1;
	}
	if ($y{sol} > 0) {
		$cs{soldier}[$y{country}] += int($y{sol} / 3);
		$is_rewrite = 1;
	}

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&down_friendship;
	&refresh;
	&n_menu;
	&write_cs;
}

#=================================================
# ����
#=================================================
sub war_lose {
	&c_up('lose_c');
	my $v = int( rand(11) + 15 );
	&use_pet('war_result', 0) unless ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'));
	$m{rank_exp} -= int( (rand(21)+20) * $m{value} );
	$m{exp} += $v;
	&write_yran('war', 1, 1);

	$mes .= "�����S�łƂ����s���_�Ȕs�k�ׁ̈A$m{name}�ɑ΂���]����������������܂���<br>";
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";

	if($m{master_c} eq 'lose_c'){
		my $v = int( rand(11) + 15 );
		my $ve = int( (rand(21)+50) * $m{value} );
		$m{rank_exp} += $ve;
		$m{exp} += $v;
		$mes .= "�������a���𗧔h�ɖ��߂��ׁA$m{name}�ɑ΂���]�����オ��܂���<br>";
		$mes .= "�����$v��$e2j{exp}����ɓ���܂���<br>";
	}
	
	$cs{soldier}[$y{country}] += int($y{sol} / 3) if $y{sol} > 0;
	&down_friendship;

	# �A���œ��������ƍ��m��������
	&refresh;
	my $renzoku = $m{unit} eq '18' ? $m{renzoku_c} * 2: $m{renzoku_c};
	if ( ( ($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000 ) || ( ($w{world} eq '11' || ($w{world} eq '19' && $w{world_sub} eq '11')) && $renzoku > rand(4) ) || $renzoku > rand(7) + 2  || ($cs{is_die}[$m{country}] && $renzoku == 1 && rand(9) < 1) || ($cs{is_die}[$m{country}] && $renzoku == 2 && rand(8) < 1)) {
		my $mname = &name_link($m{name});
		&write_world_news("$c_m��$mname��$c_y�̘S���ɗH����܂���");
		&add_prisoner;
	}

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&write_cs;
	&n_menu;
}

#=================================================
# �ދp
#=================================================
sub war_escape {
	$mes .= "$m{name}�ɑ΂���]����������܂���<br>";
	$m{rank_exp} -= int( (rand(6)+5) * $m{value} );
	&write_yran('war', 1, 1);

	$cs{soldier}[$m{country}] += $m{sol};
	$cs{soldier}[$y{country}] += int($y{sol} / 3);

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>0<>\n";
		close $fh;
	}

	&refresh;
	&n_menu;
	&write_cs;
}


#=================================================
# ����
#=================================================
sub war_win {
	my $is_single = shift;
	
	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('war');
		if ($is_single) {
			&super_attack('single');
		}
	}
	# �D�����ް�:�K���������ق���׽�B������A�v���̎��͊K�����Ⴂ�ق���׽
	my $v = ($w{world} eq '2' || ($w{world} eq '19' && $w{world_sub} eq '2')) ? (@ranks - $m{rank}) * 10 + 10 : $m{rank} * 8 + 10;

	# ��������Ȃ�����׽������ϲŽ
#	if ($m{country}) {
#		$mem = &modified_member($m{country});
#	} else {
#		$mem = 0;
#	}
#	$v += ($cs{capacity}[$m{country}] - $mem) * 10 unless ($w{world} eq $#world_states - 3 || $w{world} eq $#world_states - 2 || ($w{world} eq $#world_states && $m{country} eq $w{country}));
	$v += ($cs{capacity}[$m{country}] - $cs{member}[$m{country}]) * 5 unless ($w{world} eq $#world_states - 3 || $w{world} eq $#world_states - 2 || ($w{world} eq $#world_states && $m{country} eq $w{country}));


	# ����ɂ��D���͑���
	if (($w{world} eq '4' || $w{world} eq '5' || ($w{world} eq '19' && ($w{world_sub} eq '4' || $w{world_sub} eq '5')))) { # �\�N�A����
		$v *= 2.5;
	}
	elsif (($w{world} eq '2' || ($w{world} eq '19' && $w{world_sub} eq '2'))) { # �v��:�㍑�L��
		my $sum = 0;
		for my $i (1 .. $w{country}) {
			$sum += $cs{win_c}[$i];
		}
		$v *= 2.5 if $cs{win_c}[$m{country}] <= $sum / $w{country};
		if ($m{sedai} < 5) {
			$v *= 3;
		}
		elsif ($m{sedai} < 10) {
			$v *= 2.5;
		}
	}
	elsif (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) { # ����
			$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10;
			$v *= 1.2;	
	}
	else {
		$v += $m{sedai} > 10 ? 100 : $m{sedai} * 10;
	}
	
	# ��풆�Ȃ�2�{
	my $p_c_c = 'p_' . &union($m{country}, $y{country});
	$v *= 2 if $w{$p_c_c} eq '2';
	
	# �e���ݒ�
	$v *= &get_modify('war');
	
	# �Q�d�͒D����1.1�{
	if ($cs{war}[$m{country}] eq $m{name}) {
		$v = int($v * 1.1) ;
	}
	# �N��͒D����1.05�{�A�\�N���Ȃ��1.2�{
	elsif ($cs{ceo}[$m{country}] eq $m{name}) {
		my $ceo_value = ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? 1.2 : 1.05;
		$v = int($v * $ceo_value);
	}
#	#��\�{�[�i�X
#	$v = int($v * 1.1) if $cs{war}[$m{country}] eq $m{name};    
#	$v = int($v * 1.05) if $cs{ceo}[$m{country}] eq $m{name};

	# �b��
	$v = &seed_bonus('red_moon', $v);
	
	$v = $v * $m{value} * (rand(0.4)+0.8);
	$v = &seed_bonus('war_win', $v);
	$v = $m{value} * 100 if $m{pet} eq '193';
	if($m{unit} eq '18'){
		$v = $v * 1.5;
		$v = &use_pet('war_result', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) || $m{pet} eq '12');
	}else{
		$v = &use_pet('war_result', $v) unless ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'));
	}
	
	if ($cs{extra}[$m{country}] eq '1' && $cs{extra_limit}[$m{country}] >= $time) {
		$v = 999;
	}
	
	if ($w{world} eq $#world_states - 5) {
		$v = int($v / 10);
	}
	
	# �Í����J�E���^�[�̊�{�D���́i��������ޗp�j
	# ��������؂ꂻ���ɂȂ�ƕ��󑤂��L���ɂȂ�̂́A
	# ��������؂ꂽ���ɈÍ������ĂĂ��������������ǂ����Ȃ炿���ƕ��󂵂���Ă����d�l���Ǝv����
	$npc_v = int(rand(400)+600) if $w{world} eq $#world_states;

	# �D���͏��
	if ($v !~ /^(\d)\1+$/) { # ��ۖ�(����۽�g�p���Ȃ�)
		if ($m{value} < 1) { # �������s
			$v = $v > 200 ? int(rand(50)+150) : int($v);
		}
		else { # �ʏ�E����
			if($m{unit} eq '18'){
				if ($time + 2 * 24 * 3600 > $w{limit_time}) { # ��������c��P��
					$v = $v > 2000 ? int(rand(250)+1750) : int($v);
				}
				else {
					$v = $v > 1500  ? int(rand(200)+1300) : int($v);
					# �Í����J�E���^�[�̒D����
					$npc_v = int(rand(525)+975) if $w{world} eq $#world_states;
				}
			}else{
				if ($time + 2 * 24 * 3600 > $w{limit_time}) { # ��������c��P��
					$v = $v > 1500 ? int(rand(250)+1250) : int($v);
				}
				else {
					$v = $v > 1000  ? int(rand(200)+800) : int($v);
					# �Í����J�E���^�[�̒D����
					$npc_v = int(rand(400)+600) if $w{world} eq $#world_states;
				}
			}
			# ����������߂Â��Ă�������׽
			$v += $time + 4 * 24 * 3600 > $w{limit_time} ? 40
			    : $time + 8 * 24 * 3600 > $w{limit_time} ? 20
			    :                                          5
			    ;
		}
	}
	
	# �ŖS���̏ꍇ����
	if ($cs{is_die}[$y{country}]) {
		$v = int($v * 0.5);
		&_penalty
	}
	else {
		$cs{soldier}[$m{country}] += $m{sol};
	}
	if ($cs{disaster}[$y{country}] eq 'paper' && $cs{disaster_limit}[$y{country}] >= $time) {
		$v += 100;
	}
	# ���̓f�[�^�}
	$cs{strong}[$m{country}] += ($w{world} eq '13' || $w{world} eq $#world_states - 2 || $w{world} eq $#world_states - 3) ? int($v * 0.75):$v;
	$cs{strong}[$y{country}] -= $v unless ($w{world} eq $#world_states - 5);
	$cs{strong}[$y{country}] = 0  if $cs{strong}[$y{country}] < 0;
	&write_yran2(
		'strong', $v, 1,
		"strong_$y{country}", $v, 1,
		'win', 1, 1,
		'war', 1, 1
	);
#	&write_yran('strong', $v, 1);
#	&write_yran("strong_$y{country}", $v, 1);
#	&write_yran('win', 1, 1);
#	&write_yran('war', 1, 1);
	
	if ($w{world} eq $#world_states - 5) {
		$mes .= "$v��$e2j{strong}�𓾂܂���<br>";
	} else {
		$mes .= "$c_y����$v��$e2j{strong}��D���܂���<br>";
	}
	
	my $mname = &name_link($m{name});
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$mname = '������';
	}
	if ($w{world} eq $#world_states - 5) {
		&write_world_news(qq|$c_m��$mname��<font color="#FF00FF"><b>$v</b> ��$e2j{strong}�𓾂鎖�ɐ���</font>�����悤�ł�|);
	} else {
		if ($is_single) {
			&write_world_news(qq|$c_m��$mname��$c_y�ɐN�U�A$y{name}�ƈ�R�����̖���������� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����ɐ���</font>�����悤�ł�|);
		}
		else {
			$m{value} < 1
				? &write_world_news(qq|���҂���$c_y�ɐN�U�A$y{name}�̕��������j�� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����Ƃɐ���</font>�����悤�ł�|)
				: &write_world_news(qq|$c_m��$mname��$c_y�ɐN�U�A$y{name}�̕��������j�� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����Ƃɐ���</font>�����悤�ł�|)
				;
		}
	}

	&down_friendship;
	&c_up('win_c');
	++$m{medal};
	my $vv = int( (rand(21)+20) * $m{value} );
	$vv = &use_pet('war_win', $vv);
	$m{exp}      += $vv;
	$m{rank_exp} += int( (rand(11)+20) * $m{value} );
	$m{egg_c}    += int(rand(6)+5) if $m{egg};

	$mes .= "$m{name}�ɑ΂���]�����傫���オ��܂���<br>";
	$mes .= "$vv��$e2j{exp}����ɓ���܂���<br>";

	if($m{master_c} eq 'win_c'){
		++$m{medal};
		my $v = int( rand(11) + 15 );
		my $ve = int( (rand(11)+20) * $m{value} );
		$m{rank_exp} += $ve;
		$m{exp} += $v;
		$mes .= "���̌��т�傫�����`�����ׁA$m{name}�ɑ΂���]��������ɏオ��܂���<br>";
		$mes .= "�����$v��$e2j{exp}����ɓ���܂���<br>";
	}
	# ڽ���
	&_rescue if -s "$logdir/$y{country}/prisoner.cgi";

	if($y{value} eq 'ambush'){
		my $send_id = unpack 'H*', $y{name};
		open my $fh, ">> $userdir/$send_id/war.cgi";
		print $fh "$m{name}<>1<>\n";
		close $fh;
	}

	&refresh;

	&daihyo_c_up('war_c'); # ��\�n���x
	
	# �Í�
	if ($w{world} eq $#world_states) {
		my $ahoalia = 1;
		for my $ac (1..$w{country} - 1) {
			if (!$cs{is_die}[$ac]) {
				$ahoalia = 0;
			}
		}
		if ($cs{strong}[$m{country}] >= $touitu_strong
			|| ($cs{strong}[$w{country}] <= 0
				&& $union ne $w{country})
			|| ($ahoalia && $m{country} eq $w{country})) {
			&_touitu;
		}
		elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 ) {
			&_hukkou;
		}
		else{
			require './lib/vs_npc.cgi';
#			if( rand(4) < $npc_war  || ($cs{strong}[$w{country}] < 30000 && rand(3) < $npc_war) ) {
			if( rand(4) < 1  || ($cs{strong}[$w{country}] < 30000 && rand(3) < 1) ) {
			    &npc_war;
			}
		}
	}
	# �I��
	elsif (($w{world} eq '13' || ($w{world} eq '19' && $w{world_sub} eq '13'))) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
		}
		my $sum_die = 0;
		for my $i (1 .. $w{country}) {
			++$sum_die if $cs{is_die}[$i];
		}
		if ($sum_die eq $w{country} - 1 && !$cs{is_die}[$m{country}]) {
			&_touitu;
		}
	}
	# �s��ՓV
	elsif ($w{world} eq $#world_states - 2) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_touitu;
		}
	}
	# �O���u
	elsif ($w{world} eq $#world_states - 3) {
		if (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
			&_metubou;
			$cs{strong}[$m{country}] += 3000;
		}
		my $sum_die = 0;
		for my $i (1 .. $w{country}) {
			++$sum_die if $cs{is_die}[$i];
		}
		if ($sum_die eq $w{country} - 1 && !$cs{is_die}[$m{country}]) {
			&_touitu;
		}
		elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 ) {
			&_hukkou;
		}
	}
	# �ّ�
	elsif ($w{world} eq $#world_states - 5) {
		my $cou = 0;
		my $max_value = 0;
		for my $i (1 .. $w{country}) {
			if ($cs{strong}[$i] > $max_value) {
				$cou = $i;
				$max_value = $cs{strong}[$i];
			}
		}
		$strongest_country = $cou;
		if ($y{country} eq $strongest_country) {
			if (rand(3) < 1) {
				my($kkk,$vvv) = &_steal_country( 'strong',  int(rand(10)+10) * 10  );
				&write_world_news("<b>سާ���݂̑嗒�I$cs{name}[$m{country}]��$cs{name}[$y{country}]��$e2j{$kkk}�� $vvv �D���܂���</b>");
			}
		} else {
			if (rand(3) < 1) {
				my $type = int(rand(12));
				if ($type == 0) {
					for my $i (1..$w{country}) {
						next if $i eq $m{country};
						$cs{strong}[$i] -= int(rand(40)+40);
					}
					&write_world_news("<b>�e����$e2j{strong}��������܂���</b>");
				} elsif ($type <= 10) {
					if (rand(3) < 1) {
						$cs{food}[$m{country}] += 100000;
						&write_world_news("$c_m��$e2j{food}��100000�������܂���");
					} elsif (rand(2) < 1) {
						$cs{money}[$m{country}] += 100000;
						&write_world_news("$c_m��$e2j{money}��100000�������܂���");
					} else {
						$cs{soldier}[$m{country}] += 50000;
						&write_world_news("$c_m��$e2j{soldier}��50000�������܂���");
					}
				} else {
					for my $i (1..$w{country}) {
						for my $j ($i+1..$w{country}) {
							$w{"f_${i}_${j}"}=int(rand(20));
							$w{"p_${i}_${j}"}=2;
						}
					}
					&write_world_news("<b>���E�����J��ƂȂ�܂���</b>");
				}
			}
		}
	}
	# ����
	elsif ($cs{strong}[$m{country}] >= $touitu_strong) {
		&_touitu;
	}
	# �ŖS
	elsif (!$cs{is_die}[$y{country}] && $cs{strong}[$y{country}] <= 0) {
		&_metubou;
	}
	# ����
	elsif ( $cs{is_die}[$m{country}] && $cs{strong}[$m{country}] >= 5000 && !($w{world} eq '9' || ($w{world} eq '13' || ($w{world} eq '19' && ($w{world_sub} eq '9' || $w{world_sub} eq '13')))) ) {
		&_hukkou;
	}
	# �S��
	elsif (($w{world} eq '7' || ($w{world} eq '19' && $w{world_sub} eq '7')) && $cs{strong}[$y{country}] <= 3000 && rand(3) < 1) {
		my($kkk,$vvv) = &_steal_country( 'strong',  int(rand(10)+10) * 100  );
		&write_world_news("<b>سާ���݂̑嗒�I$cs{name}[$m{country}]��$cs{name}[$y{country}]��$e2j{$kkk}�� $vvv �D���܂���</b>");
	}
	if($w{world} eq '19'){# ��
		if($w{sub_time} < $time){
			$w{world_sub} = int(rand(@world_states-4));
			$w{sub_time} = $time + 6 * 3600;
		}
	}
	

	&write_cs;

	&n_menu;
}

#=================================================
# �S���ɒ��Ԃ�����Ȃ�~�o
#=================================================
sub _rescue {
	my $is_rescue = 0;
	my @lines = ();
	my $count = 0;
	open my $fh, "+< $logdir/$y{country}/prisoner.cgi" or &error("$logdir/$y{country}/prisoner.cgi ���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($name,$country,$flag) = split /<>/, $line;
		if ($flag == 0 && $count < $max_rescue && ($country eq $m{country} || $union eq $country) && $country ne '0' ) {
			my $mname = $m{name};
			if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
				$mname = '������';
			}
			$mes .= "$c_y�ɕ߂炦���Ă���$name���~�o���܂���<br>";
			$is_rescue = 1;
			&write_world_news("$c_m��$mname��$c_y�ɕ߂炦���Ă���$name�̋~�o�ɐ������܂���");
			&write_yran('res', 1, 1);
			
			# ڽ����׸ލ쐬
			my $y_id = unpack 'H*', $name;
			if (-d "$userdir/$y_id") {
				open my $fh2, "> $userdir/$y_id/rescue_flag.cgi" or &error("$userdir/$y_id/rescue_flag.cgi̧�ق����܂���");
				close $fh2;
			}
			++$count;
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rescue) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		&c_up('res_c');
		&use_pet('rescue');
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('rescue');
		}
	}
	close $fh;
}

#=================================================
# ����
#=================================================
sub _touitu {
	&c_up('hero_c');
	&debug_log(\%w, 'touitsu_w');
	if ($union) {
		$w{win_countries} = "$m{country},$union";
		++$cs{win_c}[$union];
	}
	else {
		$w{win_countries} = $m{country};
	}
	++$cs{win_c}[$m{country}];

	my $mname = &name_link($m{name});
	if ($w{world} eq $#world_states) {
		if ($m{country} eq $w{country} || $union eq $w{country}) { # NPC�����̏���
			&mes_and_world_news("<em>�����B�̗���҂Ƃ���$world_name�嗤���x�z���邱�Ƃɐ������܂���</em>",1);
			&write_legend('touitu', "�[���ł��ڊo�߂�$cs{name}[$w{country}]�̖ҎҒB��$mname��M���Ƃ�$world_name�嗤���x�z����");
			&send_twitter("�[���ł��ڊo�߂�$cs{name}[$w{country}]�̖ҎҒB��$m{name}��M���Ƃ�$world_name�嗤���x�z����");
			$is_npc_win = 1;
		}
		else {
			&mes_and_world_news("<em>���E���Ăѕ��󂵁A$world_name�嗤�ɂЂƂƂ��̈��炬�����Ƃ���܂���</em>",1);
			&write_legend('touitu', "$c_m��$mname�Ƃ��̒��ԒB�����E���Ăѕ��󂵁A$world_name�嗤�ɂЂƂƂ��̈��炬�����Ƃ����");
			&send_twitter("$c_m��$m{name}�Ƃ��̒��ԒB�����E���Ăѕ��󂵁A$world_name�嗤�ɂЂƂƂ��̈��炬�����Ƃ����");
		}
	}
	elsif ($w{world} eq $#world_states-2) {
		&mes_and_world_news("<em>$world_name�嗤��񕪂���킢��$c_m��$mname�Ƃ��̒��ԒB�̏����ɏI�����</em>",1);
		&write_legend('touitu', "$c_m��$mname��$world_name�嗤�𓝈ꂷ��");
		&send_twitter("$c_m��$m{name}��$world_name�嗤�𓝈ꂷ��");
		$w{win_countries} = $m{country};
	}
	elsif ($w{world} eq $#world_states-3) {
		&mes_and_world_news("<em>$world_name�嗤���O������킢��$c_m��$mname�Ƃ��̒��ԒB�̏����ɏI�����</em>",1);
		&write_legend('touitu', "$c_m��$mname��$world_name�嗤�𓝈ꂷ��");
		&send_twitter("$c_m��$m{name}��$world_name�嗤�𓝈ꂷ��");
		$w{win_countries} = $m{country};
	}
	else {
		if ($union) {
			$mes .= "<em>$world_name�嗤�𓝈ꂵ�܂���</em>";
			&write_world_news("<em>$c_m$cs{name}[$union]������$mname��$world_name�嗤�𓝈ꂵ�܂���</em>",1);
			&write_legend('touitu', "$c_m$cs{name}[$union]������$mname��$world_name�嗤�𓝈ꂷ��");
			&send_twitter("$c_m$cs{name}[$union]������$m{name}��$world_name�嗤�𓝈ꂷ��");
		}
		else {
			&mes_and_world_news("<em>$world_name�嗤�𓝈ꂵ�܂���</em>",1);
			&write_legend('touitu', "$c_m��$mname��$world_name�嗤�𓝈ꂷ��");
			&send_twitter("$c_m��$m{name}��$world_name�嗤�𓝈ꂷ��");
		}
	}

	require "./lib/reset.cgi";
	&reset;

	$m{lib} = 'world';
	$m{tp}  = 100;
}

#=================================================
# ����
#=================================================
sub _hukkou {
	&c_up('huk_c');
	$cs{is_die}[$m{country}] = 0;
	&mes_and_world_news("<b>$c_m�𕜋������邱�Ƃɐ������܂���</b>", 1);
	
	--$w{game_lv};
#	--$w{game_lv} if $time + 7 * 24 * 3600 > $w{limit_time};
}

#=================================================
# �ŖS
#=================================================
sub _metubou {
	&c_up('met_c');
	$cs{strong}[$y{country}] = 0;
	$cs{is_die}[$y{country}] = 1;
	$w{world_sub} = int(rand(@world_states-4));
	&mes_and_world_news("<b>$c_y��łڂ��܂���</b>", 1);

	# ����Down
	for my $k (qw/food money soldier/) {
		$cs{$k}[$y{country}] = int( $cs{$k}[$y{country}] * ( rand(0.3)+0.3 ) );
	}
	
	# ����ԕω�
	for my $i (1 .. $w{country}) {
		$cs{state}[$i] = int(rand(@country_states));
	}
}
#=================================================
# �ŖS�����獑�͂�D�悵�����̔���
#=================================================
sub _penalty {
	# �ЊQ
	if ( (($w{world} eq '12' || ($w{world} eq '19' && $w{world_sub} eq '12')) && rand(3) < 1) || rand(12) < 1 ) {
		&disaster( ($w{world} eq '12' || ($w{world} eq '19' && $w{world_sub} eq '12') )); # ��N or ��(��N)�̂ݒǉ�����è

=pod
		#1�� 2�~ 3�� 4�~ 5�� 6�� 7�� 8�~ 9�� 10��
		if ($w{year} !~ /6$/ && $w{year} !~ /0$/ && $cs{strong}[$y{country}] < 5000) { # �����łȂ�������5000�����iɱ��ر�̍�������j�̂ݍ�������
			# ������Ԏ擾
			my $sleep_num = 0;
			for my $i (1 .. $w{country}) {
				$sleep_num++ if $cs{die}[$i] == 2;
			}
			unless ($sleep_num) { # �ǂ����������ĂȂ��Ȃ獽��
				$cs{is_die}[$y{country}] = 2;
				$w{game_lv} -= int(rand(3)+4) unless $w{world} eq '15' || $w{world} eq '17'; # �����Ɩ����͓����Փx�Ⴗ����̂ł���ȏ㉺�������̏�Ȃ牺����

				# �������Ă��鍑�ɓ���������ΐ؂�
				for my $i (1 .. $w{country}) {
					my $c_c = &union($y{country}, $i);
					$w{"p_$c_c"} = 0 if $w{"p_$c_c"} == 1;
				}
			}
		}
=cut
	}
}

#=================================================
# �F�D�xDown
#=================================================
sub down_friendship {
	my $c_c = &union($m{country}, $y{country});
	$w{'f_'.$c_c} -= 1;
	$w{'f_'.$c_c} -= ($m{pet_c} - 10) if ($m{pet} eq '193' && $m{pet_c} > 10);
	if ($w{'p_'.$c_c} ne '2' && $w{'f_'.$c_c} < 10 && $y{country} ne $union) {
		$w{'p_'.$c_c} = 2;
		my $mname = &name_link($m{name});
		&write_world_news("<b>$c_m��$mname�̐i�R�ɂ��$c_y�ƌ���ԂɂȂ�܂���</b>");
	}
	$w{'f_'.$c_c} = int(rand(20)) if $w{'f_'.$c_c} < 1;
}

#=================================================
# �C���㏊���l��
#=================================================
sub modified_member {
	my $i = shift;
	return $cs{member}[$i] - $cs{new_commer}[$i];
}



1; # �폜�s��
