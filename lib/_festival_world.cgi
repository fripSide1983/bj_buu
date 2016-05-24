use File::Copy::Recursive qw(rcopy);
use File::Path;
#================================================
# �Ղ��̊J�n�E�I���Ŏg���郂�W���[��
# ��ȌĂяo����
# ./lib/reset.cgi
#================================================
# �g�� ����� �n���x�ޯ����� ����ݍs�� �n���xؽı
# �O���u ����� �n���x�ޯ����� ����ݍs�� �n���xؽı
# �ّ� ɰ����� ����ݍs��
# ���� ����� �n���x�ޯ����� ����ݍs�� �n���xؽı

#================================================
# �Ղ����ɒǉ�����鍑�̐��E���́E�����E���F�̒�`
#================================================
use constant FESTIVAL_COUNTRY_PROPERTY => {
	'kouhaku' => [2, 75000, ["���̂��̎R", "�����̂��̗�"], ["#ffffff", "#ff0000"]],
	'sangokusi' => [3, 50000, ["�", "��", "�"], ["#4444ff", "#ff4444", "#44ff44"]]
};

#================================================
# �Ղ��J�n���̍�����ݒ肵�Ďn�߂�
#================================================
sub begin_festival_world {
	# �ّ��ȊO�̍Ղ��J�n���̊��������ׂĂ̌N��ƌN��t�@�C����������
	if ($w{year} % 40 != 10) {
		for my $i (1 .. $w{country}) {
			$cs{ceo}[$i] = '';
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
	}

	if ($w{year} % 40 == 0){ # �s��ՓV
		$w{world} = $#world_states-2;
		$w{game_lv} = 99;
		&run_kouhaku(1);
	} elsif ($w{year} % 40 == 20) { # �O���u
		$w{world} = $#world_states-3;
		$w{game_lv} = 99;
		&run_sangokusi(1);
	} elsif ($w{year} % 40 == 10) { # �ّ�
		$w{world} = $#world_states-5;
		$w{game_lv} = 99;
		$w{reset_time} = $config_test ? $time: $time + 3600 * 12;
		$w{limit_time} = $config_test ? $time: $time + 3600 * 36;
		for my $i (1 .. $w{country}) {
			$cs{strong}[$i] = 5000;
			$cs{tax}[$i] = 99;
			$cs{state}[$i] = 5;
		}
		&run_sessoku(1);
	} else { # ����
		$w{world} = $#world_states-1;
		&run_konran(1);
	}
}

#================================================
# �Ղ����������ďI����
#================================================
sub end_festival_world {
	if ($w{year} % 40 == 0){ # �s��ՓV
		$w{country} -= FESTIVAL_COUNTRY_PROPERTY->{kouhaku}[0];
		&run_kouhaku(0);
	} elsif ($w{year} % 40 == 20) { # �O���u
		$w{country} -= FESTIVAL_COUNTRY_PROPERTY->{sangokusi}[0];
		&run_sangokusi(0);
	} elsif ($w{year} % 40 == 10) { # �ّ�
		&run_sessoku(0);
	} else { # ����
		&run_konran(0);
	}
}

#================================================
# �g���̊J�n(1)�ƏI��(0)
#================================================
sub run_kouhaku {
	$is_start = shift;

	require "./lib/move_player.cgi";
	if ($is_start) { # �g���J�n���̏���	
		&add_festival_country('kouhaku');
		&player_shuffle($w{country}-1..$w{country});
	} # �g���J�n���̏���
	else { # �g���I�����̏���
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my($c1, $c2) = split /,/, $w{win_countries};
			if($c1 eq $you_datas{country} || $c2 eq $you_datas{country}){
				require './lib/shopping_offertory_box.cgi';
				for my $k (qw/war dom pro mil ceo/) {
					if ($cs{$k}[$you_datas{country}] eq $you_datas{name}) {
						&send_god_item(5, $cs{$k}[$you_datas{country}]);
					}
				}
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}else {
				&regist_you_data($you_datas{name}, 'shogo', $cs{name}[$you_datas{country}] . "(��)");
				&regist_you_data($you_datas{name},'trick_time',$time + 3600 * 24 * 3);
				&regist_you_data($you_datas{name},'shogo_t',$datas{shogo});
			}
			
			# �l�o��������
			&move_player($you_datas{name}, $you_datas{country}, 0);
			if ($you_datas{name} eq $m{name}){
				$m{country} = 0;
				$y{country} = 0;

				# �n���x��ؽı
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c"} = $m{$k."_c_t"};
					$m{$k."_c_t"} = 0;
				}
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', 0);
				&regist_you_data($you_datas{name}, 'y_country', 0);

				# �n���x��ؽı
				for my $k (qw/war dom pro mil/) {
					&regist_you_data($you_datas{name}, $k."_c", $you_datas{$k."_c_t"});
					&regist_you_data($you_datas{name}, $k."_c_t", 0);
				}
			}
		}
		closedir $dh;

		&remove_festival_country('kouhaku');
		&cs_data_repair;
	} # �g���I�����̏���
}

#================================================
# �O���u�̊J�n(1)�ƏI��(0)
#================================================
sub run_sangokusi {
	$is_start = shift;

	require "./lib/move_player.cgi";
	if ($is_start) { # �O���u�J�n���̏���
		&add_festival_country('sangokusi');
		&player_shuffle($w{country}-2..$w{country});
	} # �O���u�J�n���̏���
	else { # �O���u�I�����̏���
		require "./lib/shopping_offertory_box.cgi";
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			next unless &you_exists($pid, 1);
			my %you_datas = &get_you_datas($pid, 1);
			
			my($c1, $c2) = split /,/, $w{win_countries};
			if($c1 eq $you_datas{country} || $c2 eq $you_datas{country}){
				for my $k (qw/war dom pro mil ceo/) {
					if ($cs{$k}[$you_datas{country}] eq $you_datas{name}) {
						&send_god_item(5, $cs{$k}[$you_datas{country}]);
					}
				}
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}else {
				&regist_you_data($you_datas{name}, 'shogo', $cs{name}[$you_datas{country}] . "(��)");
				&regist_you_data($you_datas{name},'trick_time',$time + 3600 * 24 * 3);
				&regist_you_data($you_datas{name},'shogo_t',$datas{shogo});
			}
			
			# �l�o��������
			&move_player($you_datas{name}, $you_datas{country}, 0);
			if ($you_datas{name} eq $m{name}){
				$m{country} = 0;
				$y{country} = 0;

				# �n���x��ؽı
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c"} = $m{$k."_c_t"};
					$m{$k."_c_t"} = 0;
				}
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', 0);
				&regist_you_data($you_datas{name}, 'y_country', 0);

				# �n���x��ؽı
				for my $k (qw/war dom pro mil/) {
					&regist_you_data($you_datas{name}, $k."_c", $you_datas{$k."_c_t"});
					&regist_you_data($you_datas{name}, $k."_c_t", 0);
				}
			}
		}
		closedir $dh;

		&remove_festival_country('sangokusi');
		&cs_data_repair;
	} # �O���u�I�����̏���
}

#================================================
# �ّ��̊J�n(1)�ƏI��(0)
#================================================
sub run_sessoku {
	$is_start = shift;

	if ($is_start) { # �ّ��J�n���̏���
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			next unless &you_exists($pid, 1);
			my %you_datas = &get_you_datas($pid, 1);

			&wt_c_reset(\%m, \%you_datas); # �ғ����ݷݸނ̍X�V��ؾ��	
		}
		closedir $dh;
	} # �ّ��J�n���̏���
	else { # �ّ��I�����̏���
		require './lib/shopping_offertory_box.cgi';
		require "./lib/move_player.cgi";
		# 1�ʍ��ɂ͓���{�[�i�X�ƍՂ��V
		# (int(����/2)+1)�ʂɂ͓���{�[�i�X
		# �r���͕���
		my @strong_rank = &get_strong_ranking;

		&write_world_news("<b>$world_name�嗤��S�y�ɂ킽�鍑�͋�����$cs{name}[$strong_rank[0]]�̏����ɂȂ�܂���</b>");
		&write_legend('touitu', "$world_name�嗤��S�y�ɂ킽�鍑�͋�����$cs{name}[$strong_rank[0]]�̏����ɂȂ�܂���");

		$w{win_countries} = "$strong_rank[0],$strong_rank[1]";

		$cs{strong}[$strong_rank[2]] = 0;
		$cs{is_die}[$strong_rank[2]] = 3;

		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			next unless &you_exists($pid, 1);
			my %p = &get_you_datas($pid, 1);

			# �Ղ��V
			if ($strong_rank[0] eq $p{country} || $strong_rank[1] eq $p{country}) {
				if ($$strong_rank[0] eq $p{country}) {
					for my $k (qw/war dom pro mil ceo/) {
						if ($cs{$k}[$p{country}] eq $p{name}) {
							&send_god_item(5, $cs{$k}[$p{country}]);
						}
					}
					&send_item($p{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
				}
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
			}

			# �l�o��������
			&move_player($p{name}, $p{country}, 0);
			if ($p{name} eq $m{name}){
				$m{country} = 0;
				$y{country} = 0;
				&write_user;
			} else {
				&regist_you_data($p{name}, 'country', 0);
				&regist_you_data($p{name}, 'y_country', 0);
			}

			# �����Ŏg���̂Ŏc���Ă����Ă�������
			# �r���̍��ɂ���v���C���[�͓K���d��
			#elsif ($strong_rank[2] eq $p{country}) {
				#my $to_country = 0;
				#do {
					#$to_country = int(rand($w{country}) + 1);
				#} while ($cs{is_die}[$to_country] > 1);

				#&move_player($p{name}, $p{country}, $to_country);
				#if ($p{name} eq $m{name}){
					#$m{country} = $to_country;
					#&write_user;
				#} else {
					#&regist_you_data($p{name}, 'country', $to_country);
				#}
			#}
		}
	} # �ّ��I�����̏���
}

#================================================
# �����̊J�n(1)�ƏI��(0)
#================================================
sub run_konran {
	$is_start = shift;

	require "./lib/move_player.cgi";
	if ($is_start) { # �����J�n���̏���
		&player_shuffle(1..$w{country});
	} # �����J�n���̏���
	else { # �����I�����̏���
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			if($you_datas{name} eq $m{name}){
				&move_player($m{name}, $m{country}, 0);
				$m{country} = 0;

				# �n���x��ؽı
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c"} = $m{$k."_c_t"};
					$m{$k."_c_t"} = 0;
				}
				&write_user;
			}
			&move_player($you_datas{name}, $you_datas{country}, 0);
			&regist_you_data($you_datas{name}, 'country', 0);
			# �n���x��ؽı
			for my $k (qw/war dom pro mil/) {
				&regist_you_data($you_datas{name}, $k."_c", $you_datas{$k."_c_t"});
				&regist_you_data($you_datas{name}, $k."_c_t", 0);
			}

			my($c1, $c2) = split /,/, $w{win_countries};
			if ($c1 eq $you_datas{country} || $c2 eq $you_datas{country}) {
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}
		}
		closedir $dh;
	} # �����I�����̏���
}

#================================================
# �w�肳�ꂽ�Ղ��p�̍���ǉ����A����ȊO�̍����ޯ�����
# �ǉ�����鍑�̏��� FESTIVAL_COUNTRY_PROPERTY �Œ�`���Ă���
#================================================
sub add_festival_country {
	my $festival_name = shift;
	my $country_num = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[0];
	$w{country} += $country_num;
	my $max_c = int($w{player} / $country_num) + 3;
	for my $i ($w{country}-($country_num-1)..$w{country}){
		mkdir "$logdir/$i" or &error("$logdir/$i ̫��ނ����܂���ł���") unless -d "$logdir/$i";
		for my $file_name (qw/bbs bbs_log bbs_member depot_log patrol prison prison_member prisoner violator old_member/) {
			my $output_file = "$logdir/$i/$file_name.cgi";
			next if -f $output_file;
			open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
			close $fh;
			chmod $chmod, $output_file;
		}
		# ���ɂ�1�s�ڂ��ݒ�Ȃ̂ŗ\�ߏ�������ł����Ȃ��ƍ��ɂɂԂ�����1�ڂ̃A�C�e�����������Ă��܂�
		my $output_file = "$logdir/$i/depot.cgi";
		open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
		print $fh "1<>1<>1����Lv1�ȏオ���p�ł��܂�<>\n";
		close $fh;
		chmod $chmod, $output_file;

		for my $file_name (qw/leader member/) {
			my $output_file = "$logdir/$i/$file_name.cgi";
			open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
			close $fh;
			chmod $chmod, $output_file;
		}
		&add_npc_data($i);
		# create union file
		for my $j (1 .. $i-1) {
			my $file_name = "$logdir/union/${j}_${i}";
			$w{ "f_${j}_${i}" } = -99;
			$w{ "p_${j}_${i}" } = 2;
			next if -f "$file_name.cgi";
			open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ̧�ق����܂���");
			close $fh;
			chmod $chmod, "$file_name.cgi";
			open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ̧�ق����܂���");
			close $fh2;
			chmod $chmod, "${file_name}_log.cgi";
			open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ̧�ق����܂���");
			close $fh3;
			chmod $chmod, "${file_name}_member.cgi";
		}
		unless (-f "$htmldir/$i.html") {
			open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ̧�ق����܂���");
			close $fh_h;
		}

		my $num = $i-($w{country}+1-$country_num);
		$cs{name}[$i]     = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[2][$num];
		$cs{color}[$i]    = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[3][$num];
		$cs{member}[$i]   = 0;
		$cs{win_c}[$i]    = 999;
		$cs{tax}[$i]      = 99;
		$cs{strong}[$i]   = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[1];
		$cs{food}[$i]     = $config_test ? 999999 : 0;
		$cs{money}[$i]    = $config_test ? 999999 : 0;
		$cs{soldier}[$i]  = $config_test ? 999999 : 0;
		$cs{state}[$i]    = 0;
		$cs{capacity}[$i] = $max_c;
		$cs{is_die}[$i]   = 0;
		my @lines = &get_countries_mes();
		if ($w{country} > @lines - $country_num) {
			open my $fh9, ">> $logdir/countries_mes.cgi";
			print $fh9 "<>$default_icon<>\n";
			close $fh9;
		}
	}

	for my $i (1 .. $w{country}-$country_num) {
		$cs{strong}[$i]   = 0;
		$cs{food}[$i]     = 0;
		$cs{money}[$i]    = 0;
		$cs{soldier}[$i]  = 0;
		$cs{state}[$i]    = 0;
		$cs{capacity}[$i] = 0;
		$cs{is_die}[$i]   = 1;

		for my $j ($i+1 .. $w{country}-$country_num) {
			$w{ "f_${i}_${j}" } = -99;
			$w{ "p_${i}_${j}" } = 2;
		}

		$cs{old_ceo}[$i] = $cs{ceo}[$i];
		$cs{ceo}[$i] = '';

		open my $fh, "> $logdir/$i/leader.cgi";
		close $fh;
	}

	# �o�b�N�A�b�v�쐬
	for my $i (0 .. $w{country} - $country_num) {
		my $from = "$logdir/$i";
		my $backup = $from . "_backup";
		rcopy($from, $backup);
	}
	my $from = "$logdir/countries.cgi";
	my $backup = "$logdir/countries_backup.cgi";
	rcopy($from, $backup);
}

#================================================
# �w�肳�ꂽ�Ղ��p�̍����폜���A����ȊO�̍���ؽı
# �폜����鍑�̏��� FESTIVAL_COUNTRY_PROPERTY �Œ�`���Ă���
#================================================
sub remove_festival_country {
	my $festival_name = shift;
	my $country_num = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[0];
	# ���t�H���_�폜
	for (my $i = $w{country}+$country_num; $i > $w{country}; $i--) {
		my $from = "$logdir/$i";
		my $num = rmtree($from);
		
		my @lines = ();
		open my $fh, "+< $logdir/countries_mes.cgi";
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			push @lines, $line;
		}
		pop @lines while @lines > $w{country} + 1;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
	$w{country} -= $country_num;

	# ���f�[�^����
	for my $i (0 .. $w{country}) {
		my $from = "$logdir/$i";
		my $backup = $from . "_backup";
		my $num = rmtree($from);
		rcopy($backup, $from);
	}
	
	my $i = 1;
	open my $fh, "< $logdir/countries_backup.cgi" or &error("���ް����ǂݍ��߂܂���");
	my $world_line = <$fh>;
	while (my $line = <$fh>) {
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			if ($k eq 'name' || $k eq 'color' || $k eq 'win_c' || $k eq 'old_ceo' || $k eq 'ceo_continue') {
				$cs{$k}[$i] = $v;
			}
		}
		++$i;
	}
	close $fh;
}

#================================================
# 1�� (int(����/2)+1)�� ������ �̍��͏��ʂ�z��ŕԂ�
# �ّ��p�����ǂȂ񂩎g�������邩���H
#================================================
sub get_strong_ranking {
	# lstrcpy �Ƃ� memcpy �ŃK�b�Ƃ��悤�ɂ����ƊȒP�ɃR�s�y�ł����������Ǖ�����񂿂�
	my %tmp_cs;
	for my $i (1 .. $w{country}) {
		$tmp_cs{$i-1} = $cs{strong}[$i];
	}

	# ���͂ɒ��ڂ��č~���\�[�g
	my @strong_rank = ();
	foreach(sort {$tmp_cs{$b} <=> $tmp_cs{$a}} keys %tmp_cs){
		push(@strong_rank, [$_, $tmp_cs{$_}]);
	}

	my $_country = $w{country} - 1; # ����݂���������
	my $center = int($_country / 2);

	# top center bottom �̃_�u�萔�Ɛ擪�C���f�b�N�X�̎擾
	my @data = ([0,-1], [0,-1], [0,-1]);
	for my $i (0 .. $_country) {
		if ($strong_rank[$i][1] == $strong_rank[0][1]) {
			$data[0][0]++;
			$data[0][1] = $i if $data[0][1] < 0;
		}
		if ($strong_rank[$i][1] == $strong_rank[$center][1]) {
			$data[1][0]++;
			$data[1][1] = $i if $data[1][1] < 0;
		}
		if ($strong_rank[$i][1] == $strong_rank[$c][1]) {
			$data[2][0]++;
			$data[2][1] = $i if $data[2][1] < 0;
		}
	}

	# ���ꍑ�͂�����Ȃ�d�����Ȃ��悤�� rand �I��
	# �d�����Ȃ��l�������܂� while rand ���������������H
	my @result = ();
	for my $i (0 .. $#data) {
		my $j = int(rand($data[$i][0])+$data[$i][1]); # �_�u��̐擪�C���f�b�N�X����_�u�萔-1�̗���
		push (@result, @{splice(@strong_rank, $j, 1)}[0] + 1 ); # rand�I�����ꂽ������₩�甲�� 0 ������݂Ȃ̂� +1
		# �_�u�萔��擪�C���f�b�N�X�̏C��
		for my $k ($i+1 .. $#data) {
			if ($j > $data[$k][1]) {
				$data[$k][0]--;
			}
			elsif ($j < $data[$k][1]) {
				$data[$k][1]--;
			}
			else {
				$data[$k][0]--;
				$data[$k][1]--;
			}
		}
	}
	return @result;
}

#================================================
# �ғ����ݷݸނ̍X�V��ؾ�āi�Ղ�˓�����10�N���j
#================================================
sub wt_c_reset {
	my ($m, $you_datas) = @_;
	if ($you_datas{name} eq $m{name}){
		$$m{wt_c_latest} = $m{wt_c};
		$$m{wt_c} = 0;
		&write_user;
	} else {
		&regist_you_data($you_datas{name}, "wt_c_latest", $you_datas{wt_c});
		&regist_you_data($you_datas{name}, "wt_c", 0);
	}
}

#================================================
# �v���[���[�V���b�t��
# �ғ��������ƂɐU�蕪����B
#================================================
sub player_shuffle {
	my @countries = @_;
	
	for my $i (0..$#countries){
		my $j = int(rand(@countries));
		my $temp = $countries[$i];
 		$countries[$i] = $countries[$j];
 		$countries[$j] = $temp;
	}
	
	my %country_num = ();
	for my $c ($countries) {
		$country_num{$c} = 0;
	}
	
	# ���[�U�[�ꗗ�擾
	my @player_line = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		next unless &you_exists($pid, 1);
		my %you_datas = &get_you_datas($pid, 1);

		&wt_c_reset(\%m, \%you_datas); # �ғ����ݷݸނ̍X�V��ؾ��

		if ($you_datas{shuffle}) {
			my $c_find = 0;
			if ($you_datas{country}) {
				for my $c (@countries) {
					if ($c eq $you_datas{country}) {
						$country_num{$c}++;
						$c_find = 1;
					}
				}
			}
			if ($c_find) {
				next;
			}
		}
		
		push @player_line, "$you_datas{name}<>$you_datas{wt_c_latest}<>\n";
	}
	closedir $dh;
	
	@player_line = map { $_->[0] } sort { $a->[2] <=> $b->[2] } map { [$_, split /<>/ ] } @player_line;
	
	my $updown = 1;
	my $index = 0;
	my $round = 0;
	my @new_line = ();
	my $mc = @countries;
	for my $pl (@player_line) {
		my $c = $countries[$index];
		my($pname, $pw) = split /<>/, $pl;
		push @new_line, "$pname<>$c<>\n";
		$country_num{$c}++;
		while (1) {
			$index += $updown;
			if ($index < 0) {
				$index = 0;
				$updown = 1;
				$round++;
			} elsif ($index >= $mc) {
				$index = $mc - 1;
				$updown = -1;
				$round++;
			}
			if ($country_num{$countries[$index]} <= $round) {
				last;
			}
		}
	}
	
	require "./lib/move_player.cgi";
	# �U�蕪��
	for my $nl (@new_line) {
		my($nname, $nc) = split /<>/, $nl;
		my %you_datas = &get_you_datas($nname);
		
		&move_player($you_datas{name}, $you_datas{country}, $nc);
		if ($you_datas{name} eq $m{name}){
			$m{country} = $nc;

			# ��\�n�����ޯ�����
			for my $k (qw/war dom pro mil/) {
				$m{$k."_c_t"} = $m{$k."_c"};
				$m{$k."_c"} = 0;
			}
			&write_user;
		} else {
			&regist_you_data($you_datas{name}, 'country', $nc);

			# ��\�n�����ޯ�����
			for my $k (qw/war dom pro mil/) {
				&regist_you_data($you_datas{name}, $k."_c_t", $you_datas{$k."_c"});
				&regist_you_data($you_datas{name}, $k."_c", 0);
			}
		}
	}
}

=pod
# �Ղ��̊J�n�ƏI���ɕR�Â��̂� 1 ���󂯂�
use constant FESTIVAL_TYPE => {
	'kouhaku' => 1,
	'sangokusi' => 3,
	'konran' => 5,
	'sessoku' => 7,
	'dokuritu' => 9
};

# �Ղ��̖��̂ƁA�J�n���Ȃ� 1 �I���� �Ȃ� 0 ���w�肷��
sub festival_type {
	my ($festival_name, $is_start) = @_;
	return FESTIVAL_TYPE->{$festival_name} + $is_start;
}

sub player_migrate {
	my $type = shift;

	if ($type == &festival_type('kouhaku', 1)) { # �s��ՓV�ݒ�
	}
	elsif ($type == &festival_type('kouhaku', 0)) { # �s��ՓV����
	}
	elsif ($type == &festival_type('sangokusi', 1)) { # �O���u�ݒ�
	}
	elsif ($type == &festival_type('sangokusi', 0)) { # �O���u����
		require "./lib/move_player.cgi";
	}
#	elsif ($type == &festival_type('konran', 1) || $type == &festival_type('sessoku', 1)) { # �����ݒ�
	elsif ($type == &festival_type('konran', 1)) { # �����ݒ�
	}
#	elsif ($type == &festival_type('konran', 0) || $type == &festival_type('sessoku', 0)) { #��������
	elsif ($type == &festival_type('konran', 0)) { #��������
	}
	elsif ($type == &festival_type('sessoku', 1)) { # �ّ��J�n
#		&write_cs;
	}
	elsif ($type == &festival_type('sessoku', 0)) { # �ّ��I��
#		&cs_data_repair;
#		&write_cs;
	}
	elsif ($type == &festival_type('dokuritu', 1)) { # �Ɨ��ݒ�
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			rcopy($from, $backup);
		}
		my $from = "$logdir/countries.cgi";
		my $backup = "$logdir/countries_backup.cgi";
		rcopy($from, $backup);
	}
	elsif ($type == &festival_type('dokuritu', 0)) { # �Ɨ�����
		require "./lib/move_player.cgi";
		for my $i (1..$w{country}) {
			my @names = &get_country_members($i);
			for my $name (@names) {
				$name =~ tr/\x0D\x0A//d;
				if($name eq $m{name}){
					&move_player($m{name}, $i, 0);
					$m{country} = 0;
					&write_user;
				}
				my %you_datas = &get_you_datas($name);
				&move_player($name, $i, 0);
				&regist_you_data($name, 'country', 0);

				my($c1, $c2) = split /,/, $w{win_countries};
				if ($c1 eq $i || $c2 eq $i) {
					require './lib/shopping_offertory_box.cgi';
					if ($cs{ceo}[$you_datas{country}] eq $you_datas{name}) {
						&send_god_item(7, $cs{ceo}[$you_datas{country}]) for (1..2);
					}
					my $n_id = unpack 'H*', $name;
					open my $fh, ">> $userdir/$n_id/ex_c.cgi";
					print $fh "fes_c<>1<>\n";
					close $fh;
					
					&send_item($name, 2, int(rand($#eggs)+1), 0, 0, 1);
				}
			}
		}
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			my $num = rmtree($from);
			rcopy($backup, $from);
		}
		
		my $i = 1;
		open my $fh, "< $logdir/countries_backup.cgi" or &error("���ް����ǂݍ��߂܂���");
		my $world_line = <$fh>;
		while (my $line = <$fh>) {
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				if ($k eq 'name' || $k eq 'color' || $k eq 'win_c' || $k eq 'old_ceo' || $k eq 'ceo_continue') {
					$cs{$k}[$i] = $v;
				}
			}
			$w{country} = $i;
			++$i;
		}
		close $fh;
		
		&cs_data_repair;# ???
	}
}
=cut
1;