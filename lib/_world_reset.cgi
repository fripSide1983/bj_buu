#================================================
# ���E��⍑�ް���ؾ�ĂŎg���郂�W���[��
# �Ղ��Ɋւ�����̂��������S�̓I�ɂ����ƃV���v���ɂł������Ȃ̂� _world_reset �Ƃ��Ă���
# world reset vs_npc ���g�� add_npc_data �͂���ɊO���ɒu���������ǂ�����
#================================================

#================================================
# ��ȌĂяo����
# ./lib/world.cgi
# ./lib/reset.cgi
# ./lib/_war_result.cgi
# �푈�������̓���ⓝ��������؂ꂽ���ɕK�v�ɂȂ�
#================================================

#================================================
# ��S��
#================================================

# ���N�̏���X�g��n���ƒ���11�N�̏�Əd��������̂����O��������X�g���Ԃ��Ă���
sub unique_worlds {
	my @new_worlds = @_;
	open my $fh, "< $logdir/world_log.cgi" or &error("$logdir/world_log.cgi���J���܂���");
	my $line = <$fh>;
	my @old_worlds = split /<>/, $line;
	close $fh;
	my @next_worlds;
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
	return @next_worlds;
}

# �ʏ��̐ݒ������
sub opening_common {
	if ($w{world} eq '0') { # ���a
		$w{reset_time} += $config_test ? 0 : 3600 * 12;
		&write_world_news("<i>���E�� $world_states[$w{world}] �ɂȂ�܂���</i>");
	}
	elsif ($w{world} eq '6') { # ����
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			next if $cs{is_die}[$i] > 1;
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
		&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
	}
	elsif ($w{world} eq '18') { # �E��
		$w{reset_time} = $time;
		for my $i (1 .. $w{country}) {
			$cs{food}[$i]     = int(rand(300)) * 1000;
			$cs{money}[$i]    = int(rand(300)) * 1000;
			$cs{soldier}[$i]  = int(rand(300)) * 1000;
		}
		&write_world_news("<i>���E�� $world_states[$w{world}] �Ƃ����ӂ���(���Ȃ����ϊ��ł��Ȃ�)�ɂȂ�܂���</i>");
	}
	else {
		&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
	}
	$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.7):$w{game_lv};
}

# 1�� (int(����/2)+1)�� ������ �̍��͏��ʂ�z��ŕԂ�
sub get_strong_ranking {
	# lstrcpy �ŃK�b�Ƃ��悤�ɂ����ƊȒP�ɃR�s�y�ł����������Ǖ�����񂿂�
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
		my $j = int(rand($data[$i][0])+$data[$i][1]);
		push (@result, @{splice(@strong_rank, $j, 1)}[0] + 1 );
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
# ���� �Í����܂ލՂ��̈�
#================================================

# �N����n���Ɠ��������f���ĕԂ�
sub is_special_world {
	return ($w{year} =~ /6$/ || $w{year} =~ /0$/);
}

# �N����n���ƍՂ������f���ĕԂ�
# �Ղ��Ȃ�΃��W���[�������[�h
sub is_festival_world {
	if ($w{year} =~ /0$/) {
		require './lib/_festival_world.cgi';
		return 1;
	}
	return 0;
}

#sub add_npc_data {
#	my $country = shift;
#	
#	my %npc_statuss = (
#		max_hp => [999, 600, 400, 300, 99],
#		max_mp => [999, 500, 200, 100, 99],
#		at     => [999, 400, 300, 200, 99],
#		df     => [999, 300, 200, 100, 99],
#		mat    => [999, 400, 300, 200, 99],
#		mdf    => [999, 300, 200, 100, 99],
#		ag     => [999, 500, 300, 200, 99],
#		cha    => [999, 400, 300, 200, 99],
#		lea    => [666, 400, 250, 150, 99],
#		rank   => [$#ranks, $#ranks-2, 10, 7, 4],
#	);
#	my @npc_weas = (
#	#	[0]����[1]����No	[2]�K�E�Z
#		['��', [0],			[61..65],],
#		['��', [1 .. 5],	[1 .. 5],],
#		['��', [6 ..10],	[11..15],],
#		['��', [11..15],	[21..25],],
#		['��', [16..20],	[31..35],],
#		['��', [21..25],	[41..45],],
#		['��', [26..30],	[51..55],],
#	);
#	my $line = qq|\@npcs = (\n|;
#	my @npc_names = (qw/vipqiv(NPC) kirito(NPC) �T�̉ƒ��w(NPC) pigure(NPC) �E�F��(NPC) vipqiv(NPC) DT(NPC) �n��(NPC) �A�V�����C(NPC) �S�~�N�Y(NPC)/);
#
#	for my $i (0..4) {
#		$line .= qq|\t{\n\t\tname\t\t=> '$npc_names[$i]',\n|;
#		
#		for my $k (qw/max_hp max_mp at df mat mdf ag cha lea rank/) {
#			$line .= qq|\t\t$k\t\t=> $npc_statuss{$k}[$i],\n|;
#		}
#		
#		my $kind = int(rand(@npc_weas));
#		my @weas = @{ $npc_weas[$kind][1] };
#		my $wea  = $npc_weas[$kind][1]->[int(rand(@weas))];
#		$line .= qq|\t\twea\t\t=> $wea,\n|;
#
#		my $skills = join ',', @{ $npc_weas[$kind][2] };
#		$line .= qq|\t\tskills\t\t=> '$skills',\n\t},\n|;
#	}
#	$line .= qq|);\n\n1;\n|;
#	
#	open my $fh, "> $datadir/npc_war_$country.cgi";
#	print $fh $line;
#	close $fh;
#}

1;