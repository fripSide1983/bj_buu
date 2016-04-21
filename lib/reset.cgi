use File::Copy::Recursive qw(rcopy);
use File::Path;
require './lib/_world_reset.cgi';
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
	$w{win_countries} = '';
	if (&is_festival_world) { # �Ղ����Ɋ����؂�
		&time_limit_festival;
		&write_cs;
	}
	else { # �Í��E�ʏ��Ŋ����؂�
		&write_world_news("<b>$world_name�嗤�𓝈ꂷ��҂͌���܂���ł���</b>");
		&write_legend('touitu', "$world_name�嗤�𓝈ꂷ��҂͌���܂���ł���");

		# �����O���ł��Ȃ��Í��I�����ł��Ȃ��Ȃ�
		# �����ŏ㏑�������̂Ōv�Z���邾������
		unless ($w{year} =~ /5$/ || $w{year} =~ /6$/ || $w{year} =~ /9$/) {
			my @new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
			my @next_worlds = &unique_worlds(@new_worlds);
			$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
		}
	}

	&reset; # �����܂ō��������؂ꎞ�̏���

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

	&opening_common;

	$w{game_lv} = 0;

	&write_cs;
}

#================================================
# ���ް�ؾ�ď���
# ����Ɗ����؂�ŌĂ΂��̂Œ��ۓI�Ƃ���
# reset��ɏ���m�肷�邽�߁A������ʂ��Ă�����\�����邱��
#================================================
sub reset {
	require './lib/casino_toto.cgi';
	&pay_back($w{year});

	# reset countries
	for my $i (1 .. $w{country}) {
		$cs{strong}[$i] = 8000 if $cs{is_die}[$i] != 2;
	}

	# �I������
	if (&is_special_world) { # �����I��
		if ($w{year} =~ /6$/) { # �Í��E�p�Y�I��
			unless ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # �Í��I��
				require './lib/vs_npc.cgi';
				&delete_npc_country;
			}
			# �p�Y�I�������͓��ɂȂ�
		}
		else { # �Ղ��I��
			require './lib/_festival_world.cgi';
			my $migrate_type = &ending_festival;
			&player_migrate($migrate_type);
		}
		$w{world} = int(rand($#world_states-5));
	}

	# �d���ł���l��
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
	my $ave_c = int($w{player} / $country);

	# set world
	$w{year}++;
	$w{reset_time} = $config_test ? $time : $time + 3600 * 8; #12
#	$w{limit_time} = $time + 3600 * 24 * $limit_touitu_day;
	$w{limit_time} = $config_test ? $time: $time + 3600 * 24 * $limit_touitu_day;
	$w{game_lv} = $game_lv;

	# set countries
	my($c1, $c2) = split /,/, $w{win_countries};
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

	# �����J�n����
	if (&is_special_world) { # �����J�n
		if ($w{year} =~ /6$/) { # �Í��E�p�Y�J�n
			# �����炭6�N��16�N�ňÍ�������
			# $w{year} =~ /^6$/ || �Ƃł�������H
			if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # �p�Y�J�n
				$w{world} = $#world_states-4;
				$w{game_lv} += 20;
				for my $i (1 .. $w{country}) {
					$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
				}
			}
			else { # �Í��J�n
				require './lib/vs_npc.cgi';
				&add_npc_country;
			}
		}
		else { # �Ղ��J�n
			require './lib/_festival_world.cgi';
			my $migrate_type = &opening_festival;
			&wt_c_reset;
			&player_migrate($migrate_type);
		}
	}

	# 1000�N�f�t�H���g
	if ($w{year} =~ /000$/) {
		for my $i (1 .. $w{country}) {
			$cs{win_c}[$i] = 0;
		}
	}

	&write_cs;
}

1; # �폜�s��