#================================================
# ����
#================================================
require './lib/_casino_funcs.cgi'; # ���ĎQ��

$header_size = 0; # ���ݗp��ͯ�ް����
$coin_lack = 0; # 0 ��݂�ڰĂɑ���Ȃ��ƎQ���ł��Ȃ� 1 ��݂�ڰĂɑ���Ȃ��Ă��Q���ł���
$min_entry = 2; # �Œ�2�l
$max_entry = 2; # �ō�2�l

sub run {
	&_default_run;
}

#================================================
# �ްщ�ʂɕ\���������̒�`
#================================================
sub show_game_info { # �e���ޯĊz�Ȃǂ̕\�� �Q���҂��O�ɕ\�������
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|�q�����:$head[$_rate]|;
}
sub show_start_info { # ��W���̹ްтɎQ�����Ă�����ڲ԰�ɕ\����������� _start_game_form �̏�ɕ\������� ��`���ĂȂ��Ă�����ɖ��Ȃ�
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|�����̔ԍ�:$m_value<br>|;
}
sub show_started_game { # �n�܂��Ă���ްт̕\�� �Q���҂������łȂ����� is_member �Ŕ��ʂ��؂�ւ���
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|<br>�����̔ԍ�:$m_value|;
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants]) if &is_member($head[$_participants], "$m{name}"); # �ްтɎQ�����Ă���
}

#================================================
# �Q������̫��
#================================================
sub participate_form {
	my ($leader) = @_;
	my $button = $leader ? "�Q������" : "�e�ɂȂ�";
	# ���ɖ��̏���
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="number" class="text_box_b"> �����̔ԍ�<br>|;
	print qq|<input type="text"  name="bet" class="text_box_b"> �q���麲�<br>| unless $leader;
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

	if ($in{number} ne '' && $in{number} !~ /[^0-9]/ && length($in{number}) == 3) {
		my @number = (int($in{number} / 100) % 10, int(($in{number} / 10) % 10), int($in{number} % 10));
		return '���������͓�x�g���܂���' if $number[0] == $number[1] || $number[0] == $number[2] || $number[1] == $number[2];
		&_participate($in{bet}, $in{number}, '63');
	}
	else { return ("3�̈قȂ鐔�������Ă�������"); }
}

#================================================
# �J�n���鏈�� ���ۂ̃t�@�C������� _casino_funcs.cgi _start_game
#================================================
sub start_game {
	my ($fh, $head_line, $ref_members, $ref_game_members) = @_;
	my @head = split /<>/, $$head_line; # ͯ�ް
	my @participants = split /,/, $head[$_participants];
	my $is_start = 0;
	# ���ɖ��̏���

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # �Q���҂��K�v�\���A�ްъJ�n�O�Ȃ�
		($is_start, $head[$_state], $head[$_lastupdate]) = (1, 1, $time);
		$$head_line = &h_to_s(@head);
	}
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			# ���ɖ��̏���
			($mtime, $mturn) = ($time, 2);

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
}

#================================================
# ��ڲ��̫�� ��{���ɖ��ɊہX����������K�v������
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants) = @_;
	unless (&is_my_turn($participants, $m{name})) {
		print qq|<br>���肪�v�l���ł�|;
		return;
	}

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="number" class="text_box_b"> �ԍ�|;
	print &create_submit('play', '�ԍ��𓖂Ă�');
	print qq|</form>|;
	return if $m_stock == 0;

	print qq|<hr><form method="$method" action="$this_script" name="form">|;
	print qq|�A�C�e��<input type="text"  name="number" class="text_box_b"> �ԍ�<br>|;
	print &create_radio_button('itemno', '1', 'DOUBLE ���s���ł���<br>') if int($m_stock / 32) == 1;
	print &create_radio_button('itemno', '2', 'HIGH&LOW 0�`4, 5�`9�̈ʒu�𒲂ׂ�<br>') if int($m_stock / 16) % 2 == 1;
	print &create_radio_button('itemno', '3', 'TARGET �����̈ʒu�𒲂ׂ�<br>') if int($m_stock / 8) % 2 == 1;
	print &create_radio_button('itemno', '4', 'SLASH �ő�l - �ŏ��l�𒲂ׂ�<br>') if int($m_stock / 4) % 2 == 1;
	print &create_radio_button('itemno', '5', 'SHUFFLE �����̐����������<br>') if int($m_stock / 2) % 2 == 1;
	if ($m_stock % 2 == 1) {
		print &create_radio_button('itemno', '6', 'CHANGE ');
		for my $num (0 .. 2) {
			my $c = substr($m_value, $num, 1);
			print &create_radio_button('choicenum', $c, "$c ����");
		}
		print '<br>';
	}
	print &create_submit('use_item', '�A�C�e�����g��');
	print '</form>';
}

#================================================
# ��ڲ�̏���
#================================================
sub play {
	return "3�̐��������Ă�������" if !($in{number} ne '' && $in{number} !~ /[^0-9]/ && length($in{number}) == 3);

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my @game_members = &get_members($head[$_participants]);
	my $is_my_turn = $head[$_state] && $game_members[0] eq $m{name} && 2 <= $m{c_turn};
	my ($e_name, $e_value);

	my %sames = ();
	my $is_find = 0;
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟

		if ($mname eq $game_members[1] && $is_my_turn) {
			($e_name, $e_value, $is_find) = ($mname, $mvalue, 1);
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	my $result_mes = '';
	my $is_reset = 0;
	my $penalty_coin = 0;
	if ($is_find) {
		my($hit, $blow) = &hb_count($in{number}, $e_value);
		$result_mes = "$in{number}:$hit �C�[�g $blow �o�C�g";
		$head[$_lastupdate] = $time;
		if ($hit == 3) {
			$result_mes .= "����";
			$penalty_coin = $head[$_rate];
			$is_reset = 1;
			&init_header(\@head);
			&reset_members(\@members);
		}
		$head[$_participants] = &change_turn($head[$_participants]); # ��ݏI�� 1��݂ŕ�����s������悤�ȹްтȂ���ı�Ă��A�ŏI�I�ȍs���Ŏ��s
	}

	unshift @members, &h_to_s(@head); # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	# �I������
	if ($is_my_turn && $is_find && $is_reset) {
		for my $game_member (@game_members) {
			if ($game_member eq $m{name}) {
				$m{c_turn} = 0;
				&write_user;
			}
			else {
		 		&regist_you_data($game_member, 'c_turn', '0');
			}
		}
		my $cv = -1 * &coin_move(-1 * $penalty_coin, $e_name);
		&coin_move($cv, $m{name});
	}

	return $result_mes;
}

sub hb_count {
	my ($m_number, $y_number) = @_;
	my @number = (int($m_number / 100), int($m_number / 10) % 10, $m_number % 10);
	my @answer = (int($y_number / 100), int($y_number / 10) % 10, $y_number % 10);
	my ($hit, $blow) = (0, 0);
	for my $i (0..2) {
		if ($answer[$i] == $number[$i]) {
			$hit++;
		}
		else {
			my $d = 0;
			$d = $number[$_] == $number[$i] ? $d + 1 : $d for (0 .. $i - 1);
			if ($d == 0) {
				$blow = $answer[$_] == $number[$i] ? $blow + 1 : $blow for (0 .. 2);
			}
		}
	}
	return ($hit, $blow);
}

sub use_item {
	unless ($in{itemno}) { return "�g�����т�I��ł�������"; }
	elsif ( ($in{itemno} == 1) && !($in{number} ne '' && $in{number} !~ /[^0-9]/ && length($in{number}) == 3) ) {
		return "3�̐��������Ă�������";
	}
	elsif ($in{itemno} == 3) {
		return "1�̐��������Ă�������" if !($in{number} ne '' && $in{number} !~ /[^0-9]/ && length($in{number}) == 1);
	}
	elsif ($in{itemno} == 6) {
		return "1�̐��������Ă�������" if !($in{number} ne '' && $in{number} !~ /[^0-9]/ && length($in{number}) == 1);
		return "CHANGE �������鐔��I��ł�������" if $in{choicenum} eq '';
		return "CHANGE 1���̐�����I��ł�������" if 9 < $in{number};
		return "CHANGE�ŕς�����̂�HIGH���m��LOW���m�ł�" if (($in{number} < 5) xor ($in{choicenum} < 5));
	}

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line;
	my @members = ();
	my @game_members = &get_members($head[$_participants]);
	my $is_my_turn = $head[$_state] && $game_members[0] eq $m{name};
	my ($e_name, $e_value) = ('', '');
	my ($m_turn, $m_value, $m_stock) = (0, 0, 0);
	my $my_index = -1; # @members�Ɋi�[����Ă��鎩���̃f�[�^�̃C���f�b�N�X

	my %sames = ();
	my @is_find = (0, 0); # ����f�[�^�ǂݍ��񂾂��A�����f�[�^�ǂݍ��񂾂�
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟
		$my_index++ unless $is_find[1];
		if ($mname eq $game_members[1] && $is_my_turn) {
			($e_name, $e_value, $is_find[0]) = ($mname, $mvalue, 1);
		}
		elsif ($mname eq $m{name} && $is_my_turn) {
			($m_turn, $m_value, $m_stock, $is_find[1]) = ($mturn, $mvalue, $mstock, 1);
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	my $result_mes = '';
	my ($is_reset, $is_double, $is_ng) = (0, 0, 0);
	my $penalty_coin = 0;
	if ($is_my_turn && $is_find[0] && $is_find[1]) {
		# DOUBLE �����_���ɑI�΂ꂽ������1�������J��������2��R�[���ł���
		if ($in{itemno} == 1 && int($m_stock / 32) == 1) {
			my ($hit, $blow) = &hb_count($in{number}, $e_value);
			$m_stock -= 32;
			my $open_card = int(rand(3)+1);
			$result_mes .= "DOUBLE $m{name}��$open_card���ڂ�" . substr($m_value, $open_card-1, 1) . "�ł�<br>";
			$result_mes .= "$in{number}:$hit �C�[�g $blow �o�C�g";
			if ($hit == 3) {
				$result_mes .= "����";
				$penalty_coin = $head[$_rate];
				&init_header(\@head);
				&reset_members(\@members);
				$is_reset = 1;
			}
			$is_double = 1;
		}
		# HIGH&LOW ����̊e����5�ȏォ�ǂ����m�邱�Ƃ��ł���
		elsif ($in{itemno} == 2 && int($m_stock / 16) % 2 == 1) {
			$m_stock -= 16;
			my @hl = ();
			$hl[$_] = 5 <= substr($e_value, $_, 1) ? 'high' : 'low' for (0 .. 2); # 3���̐�����1��������
			$result_mes = "HIGH&LOW $hl[0],$hl[1],$hl[2]";
		}
		# TARGET �w�肵���l������̉����ڂɂ���̂��m�邱�Ƃ��ł���
		elsif ($in{itemno} == 3 && int($m_stock / 8) % 2 == 1) {
			$m_stock -= 8;
			my ($target_num, $target_place) = ($in{number} % 10, '����܂���');
			$target_place = $target_num == substr($e_value, $_, 1) ? ($_ + 1)."���ڂł�" : $target_place for (0 .. 2); # 3���̐�����1��������
			$result_mes .= "TARGET $target_num��$target_place";
		}
		# SLASH ����̎莝���̐����̍ő�l����ŏ��l������������m�邱�Ƃ��ł���
		elsif ($in{itemno} == 4 && int($m_stock / 4) % 2 == 1) {
			$m_stock -= 4;
			my @mm = ();
			$mm[$_] = substr($e_value, $_, 1) for (0 .. 2); # 3���̐�����z��ɕϊ�
			my ($e_max, $e_min) = ($mm[0], $mm[1]);
			for my $i (0 .. 2) {
				$e_max = $mm[$i] if $e_max < $mm[$i];
				$e_min = $mm[$i] if $mm[$i] < $e_min;
			}
			$result_mes = "SLASH ".($e_max - $e_min);
		}
		# SHUFFLE �����̐������V���b�t������
		elsif ($in{itemno} == 5 && int($m_stock / 2) % 2 == 1) {
			$m_stock -= 2;
			$result_mes = "SHUFFLE";
			my @num_arr = ();
			$num_arr[$_] = substr($m_value, $_, 1) for (0 .. 2); # 3���̐�����z��ɕϊ�
			for my $i (0 .. 2) {
				my $j = int(rand($i + 1)); # ���񂷂�x�ɗ����͈͂��L���� 1����:0�`0 2����:0�`1 3����:0�`2
				my $tmp_n = $num_arr[$j]; # �����̃X���b�v
				$num_arr[$j] = $num_arr[$i];
				$num_arr[$i] = $tmp_n;
			}
			$m_value = "$num_arr[0]$num_arr[1]$num_arr[2]";
		}
		# CHANGE �����̔ԍ���1����HIGH�ELOW���m�ŐV���������Ɍ���
		elsif ($in{itemno} == 6 && $m_stock % 2 == 1) {
			$m_stock -= 1;
			my $index = index($m_value, $in{choicenum});
			my $old_num = substr($m_value, $index, 1);
			if ($index == -1) {
				$result_mes = "CHANGE �������鐔��I��ł�������";
				$is_ng = 1;
			}
			elsif (($in{number} < 5) xor ($old_num < 5)) {
				$result_mes = "CHANGE �ς�����̂�HIGH���m��LOW���m�ł�";
				$is_ng = 1;
			}
			elsif ($old_num eq $in{number}) {
				$result_mes = "CHANGE �����O�ƌ�����̐����������ł�";
				$is_ng = 1;
			}
			elsif (-1 < index($m_value, $in{number})) {
				$result_mes = "CHANGE �d�����Ȃ�������I��ł�������";
				$is_ng = 1;
			}
			else {
				my $diff_hl = 5 <= $old_num ? 'high' : 'low';
				substr($m_value, $index, 1, $in{number});
				$result_mes = "CHANGE $m{name}��".($index + 1)."���ڂ�$diff_hl�ł�";
			}
		}
	}

	if ($is_my_turn && $result_mes && !$is_ng && !$is_reset) {
		splice(@members, $my_index, 1, "$time<>$m{name}<>$addr<>$m_turn<>$m_value<>$m_stock<>\n");
		$head[$_lastupdate] = $time;
		$head[$_participants] = &change_turn($head[$_participants]) if $is_find[0] && $is_find[1] && !$is_double; # ��ݏI�� 1��݂ŕ�����s������悤�ȹްтȂ���ı�Ă��A�ŏI�I�ȍs���Ŏ��s
	}

	unshift @members, &h_to_s(@head); # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	# �I������
	if ($is_my_turn && $is_reset) {
		for my $game_member (@game_members) {
			if ($game_member eq $m{name}) {
				$m{c_turn} = 0;
				&write_user;
			}
			else {
		 		&regist_you_data($game_member, 'c_turn', '0');
			}
		}
		my $cv = -1 * &coin_move(-1 * $penalty_coin, $e_name);
		&coin_move($cv, $m{name});
	}

	return $result_mes;
}

1;#�폜�s��