use File::Copy::Recursive qw(rcopy);
use File::Path;
#================================================
# ��ؾ�� Created by Merino
#================================================

# �����Փx�F[��� 60 �` 40 �ȒP]
#my $game_lv = $config_test ? int(rand(6) + 55) : int( rand(11) + 40 );
my $game_lv = $config_test ? int( rand(11) + 45 ) : int( rand(11) + 45 );

# �������(��)
my $limit_touitu_day = int( rand(6)+5 );

#================================================
# �������߂����ꍇ
#================================================
sub time_limit {
	$w{win_countries} = '';
	unless ($w{world} eq $#world_states-5) { # �ّ��ȊO�̏�Ŋ����؂�
		&write_world_news("<b>$world_name�嗤�𓝈ꂷ��҂͌���܂���ł���</b>");
		&write_legend('touitu', "$world_name�嗤�𓝈ꂷ��҂͌���܂���ł���");

		# �����O���ł��Ȃ��Í��I�����ł��Ȃ��Ȃ�
		# �����ŏ㏑�������̂Ōv�Z���邾������
		unless ($w{year} =~ /5$/ || $w{year} =~ /6$/ || $w{year} =~ /9$/) {
			($w{world}, $w{world_sub}) = &choice_unique_world(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
		}
	}

	&reset; # �����܂ō��������؂ꎞ�̏���

	if ($w{world} eq '0') { # ���a
		&write_world_news("<i>���E�� $world_states[$w{world}] �ɂȂ�܂���</i>");
		&send_twitter("���E�� $world_states[$w{world}] �ɂȂ�܂���");
	}
	elsif ($w{world} eq '18') { # �E��
		&write_world_news("<i>���E�� $world_states[$w{world}] �Ƃ����ӂ���(���Ȃ����ϊ��ł��Ȃ�)�ɂȂ�܂���</i>");
		&send_twitter("���E�� $world_states[$w{world}] �Ƃ����ӂ���(���Ȃ����ϊ��ł��Ȃ�)�ɂȂ�܂���");
	}
	else {
		&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
		&send_twitter("���E�� $world_states[$w{world}] �ƂȂ�܂���");
	}

	&add_world_log($w{world});
	&begin_common_world;

	&write_cs;
}

#================================================
# ���ް�ؾ�ď����i��͊܂܂�Ȃ����ۂ��j
# ����Ɗ����؂�ŌĂ΂��̂Œ��ۓI�Ƃ���
# ��{�I�ɂ����� $w{world} �����������Ă͂����Ȃ��i�����͓���҂����I�΂Ȃ������Ȃ��ɂȂ�̂�������邽�߁H�j
# reset��ɏ���m�肷�邽�߁A������ʂ��Ă�����\�����邱��
# reset �O��� $w{world} ��ς��鏈��������̂ŏ�����߂�֐��Ƃ��Ďg�����̂ł͂Ȃ��Ǝv����
#================================================
sub reset {
	$this_file = "$logdir/chat_casino_toto";
	require './lib/casino_toto.cgi';
	&pay_back($w{year});
	$this_file = "$logdir/chat_casino_e";
	require './lib/casino_espoir.cgi';
	&game_end_espoir($w{year});

	# �����I������
	if (&is_special_world) { # �����I��
		if ($w{year} =~ /6$/) { # �Í��E�p�Y�I��
#			if ($w{year} =~ /16$/ || $w{year} =~ /36$/ || $w{year} =~ /56$/ || $w{year} =~ /76$/ || $w{year} =~ /96$/) { # �Í��I��
			if ($w{year} % 20 > 9) { # �Í��I��
				require './lib/vs_npc.cgi';
				&delete_npc_country;
			}
			# �p�Y�I�������͓��ɂȂ�
		}
		else { # �Ղ��I��
			require './lib/_festival_world.cgi';
			&end_festival_world;
		}
		$w{world} = int(rand($#world_states-5));
	}

	# �����܂ł���N�̍Ō�̍Ō�
	# ��������͈�N�̍ŏ��̍ŏ�

	# set world
	$w{year}++;
	$w{reset_time} = $config_test ? $time : $time + 3600 * 12;
	$w{limit_time} = $config_test ? $time + 3600 * 36 : $time + 3600 * 24 * $limit_touitu_day;
	$w{game_lv} = $game_lv;

	# reset countries
	my $sleep_num = 0;
	for my $i (1 .. $w{country}) {
		$cs{strong}[$i] = 8000;
#		$sleep_num++ if $cs{is_die}[$i] > 2;
	}

	# �d���ł���l��
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
#	$country -= $sleep_num if $sleep_num > 0;
	my $ave_c = int($w{player} / $country);
	$ave_c = $ave_c < 2 ? 2 : $ave_c;
#	$ave_c = $config_test ? 11 : $ave_c;

	# set countries
	my($c1, $c2) = split /,/, $w{win_countries};
	for my $i (1 .. $w{country}) {
		# ���ꍑ�̏ꍇ��NPC���
#		$cs{strong}[$i] = $c1 eq $i || $c2 eq $i ? 8000 : int(rand(6) + 10) * 1000;
		$cs{strong}[$i] = $c1 eq $i || $c2 eq $i ? 8000 : int(rand(4) + 12) * 1000;
		$cs{state}[$i]    = rand(2) > 1 ? 0 : int(rand(@country_states));
		$cs{food}[$i]     = $config_test ? 999999 : int(rand(30) + 5) * 1000;
		$cs{money}[$i]    = $config_test ? 999999 : int(rand(30) + 5) * 1000;
		$cs{soldier}[$i]  = $config_test ? 999999 : int(rand(30) + 5) * 1000;
		$cs{modify_war}[$i]   = 0;
		$cs{modify_dom}[$i]   = 0;
		$cs{modify_mil}[$i]   = 0;
		$cs{modify_pro}[$i]   = 0;
#		if ($cs{is_die}[$i] > 2) {
#			$cs{strong}[$i]   = 0;
#			$cs{capacity}[$i] = 0;
#		}
#		else {
			$cs{is_die}[$i]   = 0;
			$cs{capacity}[$i] = $ave_c;
#		}
		
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
		&send_twitter("�e����$e2j{ceo}�̔C���������ƂȂ�܂���");
	}
	if ($w{year} % $reset_daihyo_cycle_year == 0) {
		&write_world_news("<b>�e���̑�\\�҂̔C���������ƂȂ�܂���</b>");
		&send_twitter("�e���̑�\\�҂̔C���������ƂȂ�܂���");
	}

	# �����J�n����
	if (&is_special_world) { # �����J�n
		if ($w{year} =~ /6$/) { # �Í��E�p�Y�J�n
#			if ($w{year} =~ /16$/ || $w{year} =~ /36$/ || $w{year} =~ /56$/ || $w{year} =~ /76$/ || $w{year} =~ /96$/) { # �Í��J�n
			if ($w{year} % 20 > 9) { # �Í��J�n
				require './lib/vs_npc.cgi';
				&add_npc_country;
			}
			else { # �p�Y�J�n
				$w{world} = $#world_states-4;
				$w{game_lv} += 20;
				for my $i (1 .. $w{country}) {
					$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
				}
			}
		}
		else { # �Ղ��J�n
			require './lib/_festival_world.cgi';
			&begin_festival_world;
		}
	}

	# 1000�N�f�t�H���g
	# ���ݒ������Č`�[�����Ă��ɍՂ��̊J�n�ޯ����߂ƏI��ؽı�ɋ��܂��Ă邩�疳�������ꂻ���H
	if ($w{year} =~ /000$/) {
		for my $i (1 .. $w{country}) {
			$cs{win_c}[$i] = 0;
		}
	}

	&write_cs;
}

#================================================
# �N����n���Ɠ��������f���ĕԂ�
#================================================
sub is_special_world {
	return $w{year} > 0 ? ($w{year} =~ /6$/ || $w{year} =~ /0$/) : 0 ;
}

#================================================
# �N����n���ƍՂ������f���ĕԂ�
# �Ղ��Ȃ�΃��W���[�������[�h
#================================================
sub is_festival_world {
	if ($w{year} > 9 && $w{year} =~ /0$/) {
		require './lib/_festival_world.cgi';
		return 1;
	}
	return 0;
}

#================================================
# ����X�g��n���ƒ���11�N�̏�Əd��������̂����O���������烉���_���ŏ��I��ł����
# �߂�l�� (world, world_sub)
#================================================
sub choice_unique_world {
	my @new_worlds = @_;
	open my $fh, "< $logdir/world_log.cgi" or &error("$logdir/world_log.cgi���J���܂���");
	my $line = <$fh>;
	close $fh;
	my @old_worlds = split /<>/, $line;
	my @next_worlds = ();
	for my $new_v (@new_worlds){
		my $old_year = 0;
		my $old_flag = 0;
		for my $o (@old_worlds){
			last if $old_year > 10;
			if ($new_v == $o){
				$old_flag = 1;
				last;
			}
			$old_year++;
		}
		push @next_worlds, $new_v unless $old_flag;
	}

	# �d��������̂΂��肾�����ꍇ�ɂ́u���a�v�ɂȂ�悤�ɂȂ��Ă������u��v�̕����K������
	return ( $next_worlds[int(rand(@next_worlds))], int(rand($#world_states-5)) ) if @next_worlds;
	return ( 19, int(rand($#world_states-5)) );
}

#================================================
# �n���ꂽ�������O�̐擪�ɑ}������
#================================================
sub add_world_log {
	my $world = shift;
	my $nline = "$world<>";
	my $saved_w = 0;
	open my $fh, "+< $logdir/world_log.cgi" or &error("$logdir/world_log.cgi���J���܂���");
	my $line = <$fh>;
	my @old_worlds = split /<>/, $line;
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	seek $fh, 0, 0;
	truncate $fh, 0;
	print $fh "$nline\n";
	close $fh;
}

#================================================
# �ʏ��̐ݒ������
#================================================
sub begin_common_world {
	my $old_world = $w{world};

	if ($w{world} eq '0') { # ���a
		$w{reset_time} += $config_test ? 0 : 3600 * 12;
#		&write_world_news("<i>���E�� $world_states[$w{world}] �ɂȂ�܂���</i>");
	}
	elsif ($w{world} eq '6') { # ����
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			next if $cs{is_die}[$i] > 2;
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
#		&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
	}
	elsif ($w{world} eq '18') { # �E��
		$w{reset_time} = $time;
		for my $i (1 .. $w{country}) {
			$cs{food}[$i]     = int(rand(300)) * 1000;
			$cs{money}[$i]    = int(rand(300)) * 1000;
			$cs{soldier}[$i]  = int(rand(300)) * 1000;
		}
#		&write_world_news("<i>���E�� $world_states[$w{world}] �Ƃ����ӂ���(���Ȃ����ϊ��ł��Ȃ�)�ɂȂ�܂���</i>");
	}
	else {
#		&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
	}
	$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.9):$w{game_lv};
}

1; # �폜�s��