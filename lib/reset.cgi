use File::Copy::Recursive qw(rcopy);
use File::Path;
require './lib/_world_reset.cgi';
require './lib/_festival_world.cgi';
#================================================
# ��ؾ�� Created by Merino
#================================================

# �����Փx�F[��� 60 �` 40 �ȒP]
my $game_lv = $config_test ? int(rand(6) + 5) : int( rand(11) + 40 );

# �������(��)
my $limit_touitu_day = int( rand(6)+5 );

#================================================
# �������߂����ꍇ
#================================================
sub time_limit {
	# �Ղ����Ɋ����؂�
	if (&is_festival_world($w{world})) {
		if ($w{world} eq @world_states-2) { # ����
			$migrate_type = &festival_type('konran', 0);
		}
		elsif ($w{world} eq @world_states-3) { # �s��ՓV
			$migrate_type = &festival_type('kouhaku', 0);
			$w{country} -= 2;
		}
		elsif ($w{world} eq @world_states-4) { # �O���u
			$migrate_type = &festival_type('sangokusi', 0);
			$w{country} -= 3;
		}
		elsif ($w{world} eq @world_states-6) { # �ّ�
			$migrate_type = &festival_type('sessoku', 0);
			my $strongest_country = 0;
			my $max_value = 0;
			for my $i (1 .. $w{country}) {
				if ($cs{strong}[$i] > $max_value) {
					$strongest_country = $i;
					$max_value = $cs{strong}[$i];
				}
			}
			&write_world_news("<b>$world_name�嗤��S�y�ɂ킽�鍑�͋�����$cs{name}[$strongest_country]�̏����ɂȂ�܂���</b>");
			&write_legend('touitu', "$world_name�嗤��S�y�ɂ킽�鍑�͋�����$cs{name}[$strongest_country]�̏����ɂȂ�܂���");
			$w{win_countries} = $strongest_country;
		}
		$w{world} = int(rand($#world_states-5));
		&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
		&player_migrate($migrate_type);
	}
	else { # �ʏ��Ŋ����؂�
		&write_world_news("<b>$world_name�嗤�𓝈ꂷ��҂͌���܂���ł���</b>");
		&write_legend('touitu', "$world_name�嗤�𓝈ꂷ��҂͌���܂���ł���");
		$w{win_countries} = '';

		# �Ղ�O���Ȃ�
		if ($w{year} =~ /5$/ || $w{year} =~ /9$/) {
			if ($w{year} % 40 == 0) { # �s��ՓV
				&write_world_news("<i>���E�� $world_states[$#world_states-2}] �ƂȂ�܂���</i>");
			}
			elsif ($w{year} % 40 == 20) { # �O���u
				&write_world_news("<i>���E�� $world_states[$#world_states-3}] �ƂȂ�܂���</i>");
			}
			elsif ($w{year} % 40 == 10) { # �ّ�
				&write_world_news("<i>���E�� $world_states[$#world_states-5}] �ƂȂ�܂���</i>");
			}
			else { # ����
				&write_world_news("<i>���E�� $world_states[$#world_states-1}] �ƂȂ�܂���</i>");
			}
		}
		else {
			my @new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
			my @next_worlds = &unique_worlds(@new_worlds);

			unless ($w{year} =~ /6$/ || $w{year} =~ /0$/) {
				$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
				# �Í���Ղ���̏����� reset �ł��̂ł����ŕ\�����Ȃ��ėǂ�
				&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>") unless $w{year} =~ /5$/ || $w{year} =~ /9$/;
			}
		}
	}
}

	&reset; # �����܂ō��������؂ꎞ�̏���

	my $migrate_type = 0;
	# ���E� �����˓�
	if ($w{year} =~ /0$/) {
		require './lib/_festival_world.cgi';
		$migrate_type = &opening_festival;
		&wt_c_reset;
	}

#	unshift @old_worlds, $w{world};
	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgi���J���܂���");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$w{world}<>$nline\n";
	close $fh;

	if ($w{world} eq '0') { # ���a
		$w{reset_time} += 3600 * 12;
	}
	elsif ($w{world} eq '6') { # ����
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			push @win_cs, [$i, $cs{win_c}[$i]];
		}
		@win_cs = sort { $b->[1] <=> $a->[1] } @win_cs;

		# ��̏ꍇ�͈�ԍ��͏���
		shift @win_cs if @win_cs % 2 == 1;
		
		my $half_c = int(@win_cs*0.5-1);
		for my $i (0 .. $half_c) {
			my $c_c = &union($win_cs[$i][0],$win_cs[$#win_cs-$i][0]);
			$w{'p_'.$c_c} = 1;
		}
	}
	elsif ($w{world} eq '18') { # �E��
		$w{reset_time} = $time;
		for my $i (1 .. $w{country}) {
			$cs{food}[$i]     = int(rand(300)) * 1000;
			$cs{money}[$i]    = int(rand(300)) * 1000;
			$cs{soldier}[$i]  = int(rand(300)) * 1000;
		}
	}
	elsif ($w{world} eq $#world_states) { # �Í��Ȃ��
		&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
	}
	elsif ($w{world} eq $#world_states-4) { # �p�Y
		$w{game_lv} += 20;
		for my $i (1 .. $w{country}) {
			$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
		}
	}

	$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.7):$w{game_lv};
	$w{game_lv} = 0;

	&write_cs;
	&player_migrate($migrate_type) if &is_festival_world($w{world});
}

#================================================
# ���ް�ؾ�ď���
# ���ꎞ�Ɗ����؂ꎞ�ŌĂ΂��̂�
# ���ۓI�ɂ��Ȃ��Ƃǂ��炩�ɕ΂��Ă��܂�
#================================================
sub reset {
	require './lib/casino_toto.cgi';
	&pay_back($w{year});
	
#	my $migrate_type = 0;
	# reset countries
	for my $i (1 .. $w{country}) {
		$cs{strong}[$i] = 8000;
	}
	
	# ���E� �Í�����
	if ($w{year} =~ /6$/) {
		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) {
			$w{world} = int(rand($#world_states-5));
		} else {
			require './lib/vs_npc.cgi';
			&delete_npc_country;
			$w{world} = int(rand($#world_states-5));
		}
		# ���ꁨreset�Ń����_��������[�U�[�������
		# ���[�U�[�����I�΂Ȃ�����Í��������̂Ŏd���Ȃ����H
#		&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
	}
#	# ���E� ��������
#	if ($w{year} =~ /0$/) {
#		if($w{year} % 40 == 0){#�s��ՓV
#			$migrate_type = &festival_type('kouhaku', 0);
#			$w{country} -= 2;
#		}elsif($w{year} % 40 == 20){# �O���u
#			$migrate_type = &festival_type('sangokusi', 0);
#			$w{country} -= 3;
#		}elsif($w{year} % 40 == 10){# �ّ�
#			$migrate_type = &festival_type('sessoku', 0);
#		}else {#����
#			$migrate_type = &festival_type('konran', 0);
#		}
#		$w{world} = int(rand($#world_states-5));
#		# �Ƃ肠�������[�U�[�����I�ԗ]�n���Ȃ��ّ������\��
#		# �����炭��������؂�ł�����ʂ��Ă���Ȃ瑼�̍Ղ��ł��\�����Ȃ��ƍ��x�͉����\������Ȃ�
#		# �푈�œ��ꂵ���̂������؂�Ȃ̂��v���f
#		&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>") if $w{year} % 40 == 10;
#	}
	# �d���ł���l��
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
	my $ave_c = int($w{player} / $country);
	
	# set world
	$w{year}++;
	$w{reset_time} = $config_test ? $time : $time + 3600 * 8; #12
#	$w{limit_time} = $time + 3600 * 24 * $limit_touitu_day;
	$w{limit_time} = $config_test ? $time: $time + 3600 * 24 * $limit_touitu_day;
	$w{game_lv} = $game_lv;
	if($w{year} % 40 == 10){
		$w{reset_time} = $config_test ? $time: $time + 3600 * 12;
		$w{limit_time} = $config_test ? $time: $time + 3600 * 36;
		$w{game_lv} = 99;
	}
	
	my($c1, $c2) = split /,/, $w{win_countries};

	# set countries
	for my $i (1 .. $w{country}) {
		# ���ꍑ�̏ꍇ��NPC���
		if($w{year} % 40 == 10){
			$cs{strong}[$i] = 5000;
			$cs{tax}[$i] = 99;
			$cs{state}[$i] = 5;
		} else {
			$cs{strong}[$i] = $c1 eq $i || $c2 eq $i ? 8000 : int(rand(6) + 10) * 1000;
			$cs{state}[$i]    = rand(2) > 1 ? 0 : int(rand(@country_states));
		}
		$cs{food}[$i]     = int(rand(30) + 5) * 1000;
		$cs{money}[$i]    = int(rand(30) + 5) * 1000;
		$cs{soldier}[$i]  = int(rand(30) + 5) * 1000;
		$cs{capacity}[$i] = $ave_c;
		$cs{is_die}[$i]   = 0;
		$cs{modify_war}[$i]   = 0;
		$cs{modify_dom}[$i]   = 0;
		$cs{modify_mil}[$i]   = 0;
		$cs{modify_pro}[$i]   = 0;
		
		for my $j ($i+1 .. $w{country}) {
			$w{ "f_${i}_${j}" } = int(rand(40));
			$w{ "p_${i}_${j}" } = 0;
		}
		
		if ($w{year} % $reset_ceo_cycle_year == 0) {
			if ($cs{ceo}[$i]) {
				my $n_id = unpack 'H*', $cs{ceo}[$i];
				open my $fh, ">> $userdir/$n_id/ex_c.cgi";
				print $fh "ceo_c<>1<>\n";
				close $fh;
			}
			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
		
		if ($w{year} % $reset_daihyo_cycle_year == 0) {
			for my $k (qw/war dom pro mil/) {
				my $kc = $k . "_c";
				next if $cs{$k}[$i] eq '';
				my $trick_id = unpack 'H*', $cs{$k}[$i];
				my %datas = &get_you_datas($trick_id, 1);
				&regist_you_data($cs{$k}[$i], $kc, int($datas{$kc} * 0.5));
				
				$cs{$k}[$i] = '';
				$cs{$kc}[$i] = 0;
				
			}
		}
	}
	
	if ($w{year} % $reset_ceo_cycle_year == 0) {
		&write_world_news("<b>�e����$e2j{ceo}�̔C���������ƂȂ�܂���</b>");
	}
	if ($w{year} % $reset_daihyo_cycle_year == 0) {
		&write_world_news("<b>�e���̑�\\�҂̔C���������ƂȂ�܂���</b>");
	}
	
	# ���E� �Í��˓�
	if ($w{year} =~ /6$/) {
		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) {
			$w{world} = $#world_states-4;
		} else {
			require './lib/vs_npc.cgi';
			&add_npc_country;
		}
	}
#	# ���E� �����˓�
#	if ($w{year} =~ /0$/) {
#		require './lib/_festival_world.cgi';
#		if ($w{year} % 40 == 0){ # �s��ՓV
#			$w{world} = $#world_states-2;
#		} elsif ($w{year} % 40 == 20) { # �O���u
#			$w{world} = $#world_states-3;
#		} elsif ($w{year} % 40 == 10) { # �ّ�
#			$w{world} = $#world_states-5;
#		} else { # ����
#			$w{world} = $#world_states-1;
#		}
#		&wt_c_reset;
#	}
	
	# 1000�N�f�t�H���g
	if ($w{year} =~ /000$/) {
		for my $i (1 .. $w{country}) {
			$cs{win_c}[$i] = 0;
		}
	}

	&write_cs;
#	return $migrate_type;
}

1; # �폜�s��