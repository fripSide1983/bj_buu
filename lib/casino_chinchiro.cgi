#================================================
# ������
#================================================
require './lib/_casino_funcs.cgi';

$header_size = 1; # �����ݗp��ͯ�ް���� �e
($_leader) = ($_header_size .. $_header_size + $header_size - 1); # ͯ�ް�z��̲��ޯ��
$coin_lack = 1; # 0 ��݂�ڰĂɑ���Ȃ��ƎQ���ł��Ȃ� 1 ��݂�ڰĂɑ���Ȃ��Ă��Q���ł���
$min_entry = 2; # �Œ�2�l
$max_entry = 32; # �ō�32�l

sub run {
	&_default_run;
}

#================================================
# �ްщ�ʂɕ\���������̒�`
#================================================
sub show_game_info { # �e���ޯĊz�Ȃǂ̕\�� �Q���҂��O�ɕ\�������
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	my @participants = &get_members($head[$_participants]);

	if ($head[$_state]) {
		print qq|�e:$head[$_leader] �q�����:$head[$_rate]|;
	}
	else {
		print qq|�e:$participants[0] �q�����:|;
		my @participants_datas = split /;/, $head[$_participants_datas];
		for my $i (0 .. $#participants_datas) {
			my @datas = split /:/, $participants_datas[$i];
#			my $name = pack 'H*', $datas[0];
			print $datas[2] if $datas[0] eq $participants[0];
		}
	}
}
#sub show_start_info { } # ��W���̹ްтɎQ�����Ă�����ڲ԰�ɕ\����������� _start_game_form �̏�ɕ\������� ��`���ĂȂ��Ă�����ɖ��Ȃ�
sub show_started_game { # �n�܂��Ă���ްт̕\�� �Q���҂������łȂ����� is_member �Ŕ��ʂ��؂�ւ���
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants_datas], $head[$_leader]); # �ްтɎQ�����Ă���
}
sub show_tale_info { # ��`���ĂȂ��Ă�����ɖ��Ȃ�
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	&show_status($head[$_participants_datas]) if $head[$_participants];
}

#================================================
# �Q������̫��
#================================================
sub participate_form {
	my ($leader) = @_;
	my $button = $leader ? "�Q������" : "�e�ɂȂ�";
	# ���ɖ��̏���
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="bet" class="text_box_b" value="$m{coin}"> ��� |;
	print &create_submit("participate", "$button");
	print qq|</form>|;
}

#================================================
# �Q�����鏈�� ڰĂ̂��߂��ݸ����
#================================================
sub participate {
	$in{bet} ||= 0;
	return '���������Ă�������' unless $in{bet} !~ /[^0-9]/;
	$in{bet} = $m{coin} if $m{coin} < $in{bet};
#	$in{bet} = int($m{coin} / 10) if $m{coin} < $in{bet};
#	$in{bet} = int($m{coin} / 10) if int($m{coin} / 10) < $in{bet};
	
	open my $fh, "< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	my $head_line = <$fh>;
	close $fh;
	my @head = split /<>/, $head_line; # ͯ�ް
	$in{bet} = $head[$_rate] if $head[$_rate] && $head[$_rate] < $in{bet};
	&_participate($in{bet}, '', $in{bet});
}

#================================================
# �J�n���鏈�� ���ۂ̃t�@�C������� _casino_funcs.cgi _start_game
#================================================
sub start_game {
	my ($fh, $head_line, $ref_members, $ref_game_members) = @_;
	my @head = split /<>/, $$head_line; # ͯ�ް
	my @participants = &get_members($head[$_participants]);
	my $is_start = 0;

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # �Q���҂��K�v�\���A�ްъJ�n�O�Ȃ�
		($is_start, $head[$_state], $head[$_lastupdate], $head[$_leader]) = (1, 1, $time, $participants[0]);
	}
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			$head[$_rate] = $mstock if $mname eq $head[$_leader];

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
	$$head_line = &h_to_s(@head);
}

#================================================
# ��ڲ��̫�� ��{���ɖ��ɊہX����������K�v������
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants_datas, $leader) = @_;

	my $diced_num = 0;
	my @participants_datas = split /;/, $participants_datas;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		$diced_num++ if $datas[1] ne '';
	}

	if ( 1 < $m_turn && $m_turn < 5 && ($leader ne $m{name} || $diced_num == (@participants_datas-1)) ) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("play", "���ۂ�U��");
		print qq|</form>|;
	}
	else { print qq|<br>| }
}

#================================================
# ��ڲ�̏���
#================================================
sub play {
	my @members = ();
	my ($result_mes, $result_mes2) = ('', '');
	my $is_play = 0;
	my ($m_value, $m_stock) = (0, 0);
	my @participants_datas = ();
	my $tmp_leader = '';

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ͯ�ް
	my @participants = split /,/, $head[$_participants];
	my $diced_num = 0;
	my @participants_datas = split /;/, $head[$_participants_datas];
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		$diced_num++ if $datas[1] ne '';
	}

	my $is_my_turn = $head[$_state] && 1 < $m{c_turn} && $m{c_turn} < 5 && ($leader ne $m{name} || $diced_num == (@participants_datas-1)); # �J�n���Ă���ްтɎQ�����Ă��Ď�������� �����݂ͻ��ۂ̐U��鐔���܂� 2 + 3
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_my_turn && $mname eq $m{name}) {
			($head[$_lastupdate], $mtime) = ($time, $time);

			# ���ɖ��̏���
			if (5 <= $m{c_turn}) { $result_mes = '�����U��܂���'; } # ���ېU��x����ݐ�+1 2 �� 0 �Ƃ� 3 �»��ېU��̂� 5
			else {
				$is_play = 1;
				my @d_set = ();
				$d_set[$_] = int(rand(6)+1) for (0 .. 2);
				@d_set = sort {$a <=> $b} @d_set;
				if ($d_set[0] == $d_set[1]) {
					$mvalue = $d_set[2];
					if ($d_set[1] == $d_set[2]) {
						$mvalue += 10;
						$mvalue += 10 if $d_set[2] == 1;
					}
					$mturn = $m{c_turn} = 5;
				}
				elsif ($d_set[1] == $d_set[2]) {
					$mvalue = $d_set[0];
					$mturn = $m{c_turn} = 5;
				}
				elsif ($d_set[2] == 3) {
					$mvalue = -1;
					$mturn = $m{c_turn} = 5;
				}
				elsif ($d_set[0] == 4) {
					$mvalue = 7;
					$mturn = $m{c_turn} = 5;
				}
				else {
					$mturn++;
					$m{c_turn} = $mturn;
					$mvalue = 0 if $mturn == 5;
				}
				my $n = $mturn - 2;
				if (5 <= $mturn && $m{name} eq $head[$_leader]) { # �e׽�
					$n = '�e���X�g';
					($m_value, $m_stock) = ($mvalue, $mstock);
					@participants_datas = split /;/, $head[$_participants_datas];
					$tmp_leader = $head[$_leader];
					&init_header(\@head);
				}
				else {
					$n = $n == 3 ? '���X�g' : $n . ' ����';
				}
				$result_mes = "$n $d_set[0],$d_set[1],$d_set[2]";
			}
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	if ($is_play && $m{name} eq $tmp_leader && $m{c_turn} == 5) {
		&reset_members(\@members);
	}

	unshift @members, &h_to_s(@head); # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($is_play) {
		if ($m{name} eq $tmp_leader && $m{c_turn} == 5) {
			my $total = 0;
			my %p_players = ();
			for my $i (0 .. $#participants_datas) {
				my @datas = split /:/, $participants_datas[$i];
#				&system_comment("$datas[0]");
				next if $datas[0] eq '';
				next if $datas[0] eq $tmp_leader;
				my $v = 0;
				if ($m_value < $datas[1]) {
					$v = $datas[2];
					$v *= $m_value == -1 ? 2 : 1;
					$v *= $datas[1] == 21 ? 5 :
					10 < $datas[1] ? 3 :
					$datas[1] == 7 ? 2 : 1;
				}
				elsif ($datas[1] < $m_value) {
					$v = $datas[2] * -1;
					$v *= $datas[1] == -1 ? 2 : 1;
					$v *= $m_value == 21 ? 5 :
					10 < $m_value ? 3 :
					$m_value == 7 ? 2 : 1;
				}
				$v = &coin_move($v, $datas[0], 1);
#				&system_comment("�����炭������1���");
				&coin_move(-1 * $v, $datas[0], 1);
#				&system_comment("���������̃`����");
				$total -= $v;
				$p_players{$datas[0]} = $v;
				&regist_you_data($datas[0], 'c_turn', '0');
				if (0 < $v) {
					$result_mes2 .= "<br>$datas[0] �� $v ��� �����܂���[".&get_yaku_name($datas[1])."]";
				}
				elsif ($v < 0) {
					$v *= -1;
					$result_mes2 .= "<br>$datas[0] �� $v ��� �����܂���[".&get_yaku_name($datas[1])."]";
				}
				else {
					$result_mes2 .= "<br>$datas[0] �͕����ł�[".&get_yaku_name($datas[1])."]";
				}
			}

			my $p_rate = 1.0;
			if ($m{coin} < -1 * $total) {
				$p_rate = $m{coin} / (-1 * $total);
#				&system_comment("$m{name} �����I������ݐ� $m{coin} / (-1 * $total) = $p_rate");
			}
			for my $mn (keys(%p_players)) {
				my $v = int($p_players{$mn} * $p_rate);
				&coin_move($v, $mn, 1);
#				&system_comment("$mn �����I������ݐ� $p_players{$mn} * $p_rate = $v");
			}
			&coin_move($total, $m{name}, 1);
#			&system_comment("$m{name} �����I������ݐ�����2 $total");
			if (0 < $total) {
				$result_mes .= "<br>$m{name} �� $total ��� �̕����ł�[".&get_yaku_name($m_value)."]";
			}
			elsif ($total < 0) {
				$total *= -1;
				$result_mes .= "<br>$m{name} �� $total ��� �̒��݂ł�[".&get_yaku_name($m_value)."]";
			}
			else {
				$result_mes .= "<br>$m{name} �͕����Ȃ��ł�[".&get_yaku_name($m_value)."]";
			}
			$m{c_turn} = 0;
			&write_user;
		}
		else {
			&write_user;
		}
	}

	return "$result_mes$result_mes2"; # ��ڲ�̕�
}

sub show_status {
	my @participants_datas = split /;/, shift;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
#		my $name = pack 'H*', $datas[0];
			print "$datas[0]";
			print " �o�ځF" . &get_yaku_name($datas[1]) if $datas[1] ne '';
			print " �ޯāF$datas[2]���";
			print "<br>" if $i != $#participants_datas;
	}
}

sub get_yaku_name {
	my $yaku = shift;
	return $yaku == -1 ? "�q�t�~" : $yaku == 0 ? "�ڂȂ�" : $yaku < 7 ? $yaku : ($yaku % 10)."�]��";
}

1;#�폜�s��
