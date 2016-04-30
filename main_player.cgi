#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# �p�l�ݷݸ� Created by oiiiuiiii
#=================================================

my $max_ranking = 100;

my %calc_name = (
	rank => "�K��",
	lea => "����",
	nou_c => "�_��",
	sho_c => "����",
	hei_c => "����",
	mil5_sum => "�R��5�퍇�v",
	mil3_sum => "�R��3�퍇�v",
	str => "����",
	win_c => "�푈������",
	win_par => "����",
	gai_c => "�O��",
	gou_c => "���D",
	cho_c => "����",
	sen_c => "���]",
	gik_c => "�U�v",
	tei_c => "��@",
	mat_c => "�ҕ�",
	year_strong => "��N�D����",
	year_nou => "��N�_��",
	year_sho => "��N����",
	year_hei => "��N����",
	year_gou => "��N���D",
	year_cho => "��N����",
	year_sen => "��N���]",
	year_gou_t => "��N���D(�݌v)",
	year_cho_t => "��N����(�݌v)",
	year_sen_t => "��N���](�݌v)",
	year_gik => "��N�U�v",
	year_res => "��N�~�o",
	year_esc => "��N�E��",
	year_tei => "��N��@",
	year_stop => "��N���",
	year_pro => "��N�F�D",
	year_dai => "��N���{"
);

#=================================================
&decode;
&header;
&read_cs;

my $this_file = "$logdir/main_player.cgi";
my $this_script = 'main_player.cgi';

my $default_calc = "rank:8:1::lea:300:1:::nou_c:500:1::sho_c:500:1:::nou_c:500:1::sho_c:500:1::hei_c:500:1:::mil5_sum:2500:1:::mil5_sum:5000:1:::gai_c:350:1:::win_c:200:1::win_par:75:1:::win_c:400:1::win_par:80:1";
#my $default_calc = "rank:15:1::lea:900:1:::nou_c:1000:1::sho_c:1000:1:::nou_c:1000:1::sho_c:1000:1::hei_c:1000:1:::mil5_sum:7000:1:::mil5_sum:10000:1:::gai_c:1400:1:::win_c:800:1::win_par:75:1:::win_c:1000:1::win_par:80:1";

&update_main_player if $in{reload} == 1;
&run;
&footer;
exit;

#=================================================
# �ݷݸމ��
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="�s�n�o" class="button1"></form>|;
	print qq|<h1>��͕\\</h1>|;
	print qq|<div class="mes">�ݷݸނ͏o�͂����x��ؾ�Ă���X�V����܂�</div><br>|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="reset" value="1"><input type="submit" value="�������Z�b�g" class="button1"></form>|;

	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	$head_line = <$fh>;
	my($output_time, $calc_min, $calc) = split /<>/, $head_line;
	print qq|<form method="$method" action="$this_script">|;
	print qq|<table class="table1"><tr><th>����</th><th>���Z�l</th></tr>|;
	&input_form($calc);
	$calc_min = $in{reset} ? 1 : $calc_min;
	print qq|臒l<input type="text" name="min" value="$calc_min" class="text_box_s"><br>|; # value="4"
	print qq|<input type="hidden" name="reload" value="1"><input type="submit" value="�o��" class="button1">|;
	print qq|</form>|;

	my($min,$hour,$mday,$mon,$year) = (localtime($output_time))[1..4];
	my $output_date = sprintf("%d/%d %02d:%02d", $mon+1,$mday,$hour,$min);
	print qq|<h2>�o�͓�:$output_date 臒l:$calc_min</h2>|;
	
	my $rank = 1;
	my $pre_number = 0;
	my $d_rank;

	print qq|<h3>�S���̎��</h3>|;
	print qq|<table class="table1" cellpadding="2"><tr><th>����</th><th>���l</th><th>���O</th><th>������</th><th>�]��</th></tr>| unless $is_mobile;
	my @lines = ();
	while ($line = <$fh>) {
		push @lines, $line;
		my($number,$name,$country,$type) = split /<>/, $line;
		my $player_id =  unpack 'H*', $name;
		$d_rank = $rank if ($pre_number != $number);
		$pre_number = $number;
		print $is_mobile     ? qq|<hr><b>$d_rank</b>��/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/$type/\n|
			: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank��</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
			:  qq|<tr class="stripe1"><th>$d_rank��</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
	
	for my $country_i(0..$w{country}) {
		$rank = 1;
		print qq|<h3>$cs{name}[$country_i]�̎��</h3>|;
		print qq|<table class="table1" cellpadding="2"><tr><th>����</th><th>���l</th><th>���O</th><th>������</th><th>�]��</th></tr>| unless $is_mobile;
		
		for my $line (@lines) {
			my($number,$name,$country,$type) = split /<>/, $line;
			next if $country != $country_i;
			my $player_id =  unpack 'H*', $name;
			$d_rank = $rank if ($pre_number != $number);
			$pre_number = $number;
			print $is_mobile     ? qq|<hr><b>$d_rank</b>��/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/$type/\n|
				: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank��</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
				:  qq|<tr class="stripe1"><th>$d_rank��</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]</td><td>$type</td></tr>\n|
				;
			++$rank;
		}
		close $fh;
		
		print qq|</table>| unless $is_mobile;
	}
}

sub input_form {
	my @calc = split(/;/, shift);
	@calc = (10, 300, 500, 500, 500, 2500, 5000, 350, 200, 75, 400, 80) if $in{reset};

	# �K�� x �ȏォ���� y �ȏ�
	print qq|<tr><td>�K��<select name="rank" class="select1">|;
	for my $i (0 .. $#ranks) {
		my $j = $#ranks-$i;
		my $selected = $j eq @calc[0] ? " selected=\"selected\"" : "";
		print qq|<option value="$j" label="$ranks[$j]"$selected>$ranks[$j]</option>|;
	}
	print qq|</select>�ȏさ����<input type="text" name="lea" value="$calc[1]" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	# �_�� x �ȏォ���� y �ȏ�
	print qq|<tr><td>�_��<input type="text" name="nou_c" value="$calc[2]" class="text_box_s">�ȏさ����<input type="text" name="sho_c" value="$calc[3]" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	# �_�� x �ȏォ���� y �ȏォ���� z �ȏ�
	print qq|<tr><td>�������𖞂�������Œ���<input type="text" name="hei_c" value="$calc[4]" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	# �R��5�퍇�v n �ȏ�
	print qq|<tr><td>�R��5�퍇�v<input type="text" name="mil5_1" value="$calc[5]" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	# �R��5�퍇�v n+a �ȏ�
	print qq|<tr><td>�R��5�퍇�v<input type="text" name="mil5_2" value="$calc[6]" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	# �O�� n �ȏ�
	print qq|<tr><td>�O��<input type="text" name="gai_c" value="$calc[7]" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	# �푈������ x �ȏォ���� y �ȏ�
	print qq|<tr><td>�폟��<input type="text" name="win_c_1" value="$calc[8]" class="text_box_s">�ȏさ����<input type="text" name="win_par_1" value="$calc[9]" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	# �푈������ x+a �ȏォ���� y+b �ȏ�
	print qq|<tr><td>�폟��<input type="text" name="win_c_2" value="$calc[10]" class="text_box_s">�ȏさ����<input type="text" name="win_par_2" value="$calc[11]" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	print qq|</table>|;

# �r���ŖO�����_����̂Ă����Q
=pod
	# ���� x �ȏ�
	print qq|<tr><td>����<input type="text" name="sedai" value="5" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	# �K�� x �ȏ�
	print qq|<tr><td>�K��<select name="rank" class="select1">|;
	for my $i (0 .. $#ranks) {
		my $j = $#ranks-$i;
		my $selected = $i eq 6 ? " selected=\"selected\"" : "";
		print qq|<option value="$j" label="$ranks[$j]"$selected>$ranks[$j]</option>|;
	}
	print qq|</select>�ȏ�</td>|;
	print qq|<td>+1�`2</td></tr>|;

	# ����3�퍇�v n �ȏ�
	print qq|<tr><td>����3�퍇�v<input type="text" name="dom3_2" value="1500" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+2</td></tr>|;

	# ����3�퍇�v n �ȏ�
	print qq|<tr><td>����3�퍇�v<input type="text" name="dom3_1" value="600" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	# �R��3�퍇�v n �ȏ�
	print qq|<tr><td>�R��3�퍇�v<input type="text" name="mil3_2" value="1500" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+2</td></tr>|;

	# �R��3�퍇�v n �ȏ�
	print qq|<tr><td>�R��3�퍇�v<input type="text" name="mil3_1" value="600" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+1</td></tr>|;

	# �푈������ x �ȏ�
	print qq|<tr><td>�폟��<input type="text" name="win_c_2" value="100" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+2</td></tr>|;

	# �푈������ x �ȏ�
	print qq|<tr><td>�폟��<input type="text" name="win_c_1" value="50" class="text_box_s">�ȏ�</td>|;
	print qq|<td>+2</td></tr>|;
=cut
}

#=================================================
# ��͕\���X�V
#=================================================
sub update_main_player  {
	my %sames = ();
	my @p_ranks = ();
	my @ranks_num = (0, 0, 0, 0, 0, 0, 0, 0);

	for my $country (0 .. $w{country}) {
		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgi̧�ق��J���܂���");
		while (my $player = <$cfh>) {
			$player =~ tr/\x0D\x0A//d;
			next if ++$sames{$player} > 1;
			my $player_id = unpack 'H*', $player;
			unless (-f "$userdir/$player_id/user.cgi") {
				next;
			}
			my %p = &get_you_datas($player_id, 1);
			$p{dom3} = $p{nou_c} + $p{sho_c} + $p{hei_c};
			$p{mil5} = $p{gou_c} + $p{cho_c} + $p{sen_c} + $p{gik_c} + $p{tei_c};
			$p{win_par} = $p{win_c} > 0 ? int( $p{win_c} / ($p{win_c} + $p{lose_c} + $p{draw_c}) * 100 ) : 0;
			$p{pt} = 0;

			# �K�� x �ȏォ���� y �ȏ�
			if ($p{rank} >= $in{rank} && $p{lea} >= $in{lea}) {
				$p{pt} += 1;
			}

			# �_�� x �ȏォ���� y �ȏ�
			if ($p{nou_c} >= $in{nou_c} && $p{sho_c} >= $in{sho_c}) {
				$p{pt} += $p{hei_c} >= $in{hei_c} ? 2 : 1; # ������ z �ȏ�
			}

			# �R��5�퍇�v n �ȏ�
			if ($p{mil5} >= $in{mil5_1}) {
				$p{pt} += $p{mil5} >= $in{mil5_2} ? 2 : 1; # ���� +a �ȏ�
			}

			# �O�� n �ȏ�
			if ($p{gai_c} >= $in{gai_c}) {
				$p{pt} += 1;
			}

			# �푈������ x �ȏォ���� y �ȏ�
			if ($p{win_c} >= $in{win_c_1} && $p{win_par} >= $in{win_par_1}) {
				$p{pt} += $p{win_c} >= $in{win_c_2} && $p{win_par} >= $in{win_par_2} ? 2 : 1; # ���푈������ x+a �ȏォ���� y+b �ȏ�
			}

			next if $p{pt} < $in{min};

			# �������� ������ ����*1 �R��*0.3 �푈*3 �Ōv�Z���Ă��C������
			$p{mil5} *= 0.5;
			$p{win_c} *= 3;
			$p{lose_c} *= 3;
			$p{draw_c} *= 3;

			if ($p{dom3} > ($p{mil5} * 2) && $p{dom3} > ($p{win_c} * 2)) { # �������R���푈�̔{�Ȃ�����Ɣ���
				$p{$type} = "�����p�l";
				if ( ($p{dom3}/3) > $p{hei_c} ) {
					$p{$type} .= "�i��K�z�j";
				}
			}
			elsif ($p{mil5} > ($p{dom3} * 2) && $p{mil5} > ($p{win_c} *2)) { # �R���������푈�̔{�Ȃ�����Ɣ���
				$p{$type} = "�R���p�l";
				if ( ($p{mil5}/5) < $p{gik_c} ) {
					$p{$type} .= "�i�i�i�R�j";
				}
				elsif ( ($p{mil5}/5) < $p{gik_c} ) {
					$p{$type} .= "�i�A�N���}�j";
				}
			}
			elsif ($p{win_c} > ($p{dom3} * 2) && $p{win_c} > ($p{mil5} *2)) { # �푈�������R���̔{�Ȃ�����Ɣ���
				$p{$type} = "�푈�p�l";
			}

			# �������Ȃ��Ő푈�΂����A�[�T�[

			# �}���\�[�g�H �ʏ͕̂�����񂪃t�H���_�ƃt�@�C�����\�[�g����̂ɂ悭������@�������悤��
			# �߲�Ė��ɂǂꂮ�炢�}���������L�^���Ă����e��ٰ�߂̖����ɑ}�����Ă������߲�Ė��Ƀ\�[�g�����
			my $pt = $#ranks_num - $p{pt};
			my $num = 0;
			for my $i (0 .. $pt) {
				$num += $ranks_num[$i];
				$ranks_num[$i] += 1 if $i == $pt;
			}
			splice(@p_ranks, $num, 0, "$p{pt}<>$p{name}<>$p{country}<>$p{type}\n");
		}
		close $cfh;
	}

	#my @nums = (5, 11, 3, 2);
#	@p_ranks = sort {$b[0] <=> $a[0]} @p_ranks;

	my $calc = join(";" , (
		$in{rank}, $in{lea},
		$in{nou_c}, $in{sho_c}, $in{hei_c},
		$in{mil5_1}, $in{mil5_2},
		$in{gai_c},
		$in{win_c_1}, $in{win_par_1}, $in{win_c_2}, $in{win_par_2}));
	unshift @p_ranks, "$time<>$in{min}<>$calc\n";

	open my $fh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
	print $fh @p_ranks;
	close $fh;
}
