#================================================
# ����
#================================================
require './lib/_casino_funcs.cgi';

=pod
��ȏ����̗���
_casino_funcs.cgi
	sub _default_run
		call &{$in{mode}} ۰�ް
		call @datas = &get_menber
		call &show_game_info(@datas)

this_file.cgi
	sub run
		call _default_run
	sub @datas = get_member
	sub show_game_info(@datas)
	sub &{$in{mode}}

����ނ̒l����֐����Ăяo��
get_member�Ŷ��ɂ�ͯ�ް���` �����Ŷ��ɖ��̓Ǝ��̕ϐ����`
show_game_info����ڲ��ʂȂǂ�\�� �����ɶ��ɖ��̓Ǝ��̕ϐ����n���Ă���
��ڲ��ʂŕ\���������ނ̒�`(���̺���ޒl���֐��Ƃ��ČĂяo��)
����ޒl����Ăяo�����֐����`
=cut

sub run {
#	$m{c_turn} = 0;
#	&write_user;
	&_default_run;
}

# ���ް̧�ق̓ǂݍ���
# �߂�l�͑�ꂩ���Z���Œ�($member_c, $member, $m_turn, $m_value, $m_stock, $state)�A����ȍ~�Ͷ��ɖ��ɵؼ��ٗv�f�A����炪show_game_info�ɓn���Ă���
sub get_member {
	my $member  = ''; # �Q���ҁE�{���҂Ȃǂ��ׂĂ���ڲ԰��������
	my @members = (); # ���̔z��
	my ($m_turn, $m_value, $m_stock) = (0, 0, 0); # �����̃f�[�^
	my @active_players = (); # ��ڲ���̎Q���҂̔z��
	my @non_active_players = (); # ���O���ꂽ�Q���҂̔z��
	my $penalty_coin = 0; # ���O or ؾ�Ď�������è

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	# ���ɖ��̵ؼ����ް�
	# �ްт̏�ԁA�ްт̍ŏI�X�V���ԁA�ްт̎Q���ҁAڰ�
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;

	my $is_reset = 0; # ��O�҂ɂ��ؾ�āFGAME_RESET�A�Q���҂ɂ��E���m�F�FLEAVE_PLAYER
	if (-1 < index($participants, "$m{name},")) { # �Q���҂ɂ��۰�ނŹްт̍ŏI�X�V���Ԃ��X�V
		$lastupdate = $time;
	}
	elsif (($lastupdate + $limit_game_time < $time) && $participants && (index($participants, "$m{name},") < 0) && $m{c_turn} < 1) { # ��Q���҂��~�܂��Ă���ްт��{��������ؾ��
		$is_reset = GAME_RESET;
		@non_active_players = split /,/, $participants;
		$penalty_coin = $rate if $state; # ���łɹްт��J�n���Ă����纲ݖv��
		($state, $lastupdate, $participants, $rate) = ('', '', '', '');
	}

	my %sames = ();
	my $is_find = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟

		my $index = index($participants, "$mname,");
		if ($mname eq $m{name}) {
			$is_find = 1;
#			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$mvalue<>$mstock<>\n"; # �����ŒE������̂ŗ]�v���ް��v��Ȃ��i���̶��ɍs�������ꂽ����c_turn�͕K�v�j
			($m_turn, $m_value, $m_stock) = ($m{c_turn}, $mvalue, $mstock);
			$member .= "$mname,";

			push @active_players, "$mname" if -1 < $index;
		}
		else {
			# ��è�ނȎQ���҂Ʊ�è�ނȉ{���҂����c��
			if ( ((-1 < $index) && ($time < $mtime + $limit_think_time)) || ($time < $mtime + $limit_member_time) ) {
				push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
				$member .= "$mname,";

				push @active_players, "$mname" if -1 < $index;
			}
			else {
				if (-1 < $index && -1 < index($participants, "$m{name},")) { # �Q���҂�e����͎̂Q���҂̊m�F���K�v
					substr($participants, $index, length("$mname,"), ''); # �Q���ҕ����񂩂��è����ڲ԰�����O
					push @non_active_players, "$mname"; # ���O���ꂽ�Q���҂�ǉ�
					$rate = $m{coin} unless $state; # ��ڲ���łȂ���Γq��������c������ڲ԰�̑S��݂�
				}
			}
		}
	}
	unless ($is_find) { # �������{���҂ɂ��Ȃ��Ȃ�ǉ�
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>0<>0<>\n"; # �����ŒE������̂ŗ]�v���ް��v��Ȃ��i���̶��ɍs�������ꂽ����c_turn�͕K�v�j
		($m_turn, $m_value, $m_stock) = ($m{c_turn}, $mvalue, $mstock);
		$member .= "$m{name},";
	}

	if (!$is_reset && @non_active_players > 0) { # GAME_RESET�ŏ���������Ă��炸�A���u��ڲ԰������ꍇ
		$is_reset = LEAVE_PLAYER;
		$penalty_coin = $rate if $state;
		($state, $lastupdate, $participants, $rate) = ('', '', '', '') if @active_players == 1 && $penalty_coin;
	}

	unshift @members, "$state<>$lastupdate<>$participants<>$rate<>\n"; # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($is_reset) { # ���u���ꂽ�ްт����u���Ă�����ڲ԰�̕Еt��
		my @zeros = (['c_turn', '0'], ['c_value', '0'], ['c_stock', '0']);
		for my $leave_player (@non_active_players) {
			if ($is_reset eq GAME_RESET) {
#				&coin_move(-0.5 * $penalty_coin, $leave_player) if $penalty_coin;
			}
			elsif ($is_reset eq LEAVE_PLAYER) {
				if ($penalty_coin) {
					my $cv = -1 * &coin_move(-1 * $penalty_coin, $leave_player);
					&coin_move($cv, $active_players[0]);
					&system_comment("��ڲ���̕��u��ڲ԰$leave_player�����O���܂���");
				}
				else {
					&system_comment("��W���̕��u��ڲ԰$leave_player�����O���܂���");
				}
			}
			&regist_you_array($leave_player, @zeros);
		}
		if ($is_reset eq GAME_RESET) {
			&system_comment($penalty_coin ? "���u���ꂽ��ڲ���̹ްт�ؾ�Ă��܂���" : '���u���ꂽ��W���̹ްт�ؾ�Ă��܂���');
		}
		elsif ($penalty_coin && @active_players == 1) {
			if ($active_players[0] eq $m{name}) {
				$m{c_turn} = $m{c_value} = $m{c_stock} = '0';
				&write_user;
			}
			else {
				&regist_you_array($active_players[0], @zeros);
			}
			&system_comment("�Q���҂�$active_players[0]�����ƂȂ������߹ްт�ؾ�Ă��܂���");
		}
	}

	my $member_c = @members - 1;

	return ($member_c, $member, $m_turn, $m_value, $m_stock, $state, $participants, $rate);
}

sub show_game_info {
	my ($m_turn, $m_value, $m_stock, $state, $participants, $rate) = @_;

	my @participants = split /,/, $participants;

	if ($participants) {
		print qq|�q�����:$rate �Q����:$participants|;
	}
	else {
		print qq|���ް��W��|;
	}

	if ($state) { # �ްт��J�n���Ă���
		print qq|<br>�����̔ԍ�:$m_value| if -1 < index($participants, "$m{name},");
		&play_form($m_turn, $m_value, $m_stock, $participants);
	}
	else { # �ްт��J�n���Ă��Ȃ�
		if (-1 < index($participants, "$m{name},")) { # �ްтɎQ�����Ă���
			&start_game_form($m_turn, $m_value, $m_stock, $participants); # �J�n̫��
		}
		else { # �ްтɎQ�����Ă��Ȃ�
			if ($participants[0] && $participants[1]) { # �e�Ǝq�����܂��Ă���
				print qq|<br>�ްт̊J�n��҂��Ă��܂�|;
			}
			else { # �e�Ǝq�ǂ��炩���܂��ĂȂ�
				&participate_form($participants[0], $participants[1], $rate); # �Q��̫��
			}
		}
	}
}

sub participate_form { # �u�Q������v��̫��
	my ($leader, $opponent, $rate) = @_;

	my $button = $leader ? "�Q������" : "�e�ɂȂ�";

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="participate">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="text"  name="number" class="text_box_b"> �����̔ԍ�<br>|;
	print qq|<input type="text"  name="bet" class="text_box_b"> �q���麲�<br>| if $leader;
	print qq|<input type="submit" value="$button" class="button_s"></form>|;
}

sub participate { # �u�Q������v����
	return "��݂�����܂���" unless $m{coin};

	my @number;
	if ($in{number} ne '' && $in{number} !~ /[^0-9]/) {
		@number = (int($in{number} / 100) % 10, int(($in{number} / 10) % 10), int($in{number} % 10));
		if($number[0] == $number[1] || $number[0] == $number[2] || $number[1] == $number[2]){
			return ("���������͓�x�g���܂���");
		}
	}
	else {
		return ("3�̈قȂ鐔�������Ă�������");
	}

	my @members = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mname eq $m{name}) {
			$mtime = $time;
			$mturn = 1;
			$mvalue = sprintf("%03d", $number[0] * 100 + $number[1] * 10 + $number[2]);
			$mstock = 63;
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;
	my @participants = split /,/, $participants;

	my $is_entry = 0;
	my $is_entry_full = 0;
	my $is_no_bet = 0;
	if (@participants > 1) {
		$is_entry_full = 1;
	}
	elsif (-1 < index($participants, "$m{name},")) {
		$is_entry = 1;
	}
	elsif (!$state && $m{c_turn} == 0) { # ��W�l�����܂��Ă��炸���Q�����J�n�O�őΐl���ɂ�����Ă��Ȃ�
		unless ($participants[0]) { # �Q���҂����Ȃ��Ȃ�e
			$rate = $m{coin};
			$participants .= "$m{name},";
			$lastupdate = $time;
		}
		elsif ($in{bet}) { # �e�����ēq������ݒ肵�Ă���Ȃ�
			$rate = $in{bet} > $rate ? $rate : $in{bet} ;
			$participants .= "$m{name},";
			$lastupdate = $time;
		}
		else { # �e�͂��Ďq���q������ݒ肵�Ă��Ȃ�
			$is_no_bet = 1;
		}
	}
	unshift @members, "$state<>$lastupdate<>$participants<>$rate<>\n";

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($state) {
		return "���łɹްт��n�܂��Ă��܂�";
	}
	elsif ($is_entry) {
		return "���łɎQ�����Ă��܂�";
	}
	elsif ($is_entry_full) {
		return "���łɎQ���҂��W�܂��Ă��܂�";
	}
	elsif ($is_no_bet) {
		return "�q�ɂȂ�ɂͺ�݂��ޯĂ��Ă�������";
	}
	elsif ($m{c_turn}) {
		return "�ΐl���ɂ���ڲ���ł�";
	}
	else {
		$m{c_turn} = 1;
		&write_user;
		return "$m{name} ���Ȃɒ����܂���";
	}
}

sub start_game_form {
	my ($m_turn, $m_value, $m_stock, $participants) = @_;
	my @participants = split /,/, $participants;

	print qq|<br>�����̔ԍ�:$m_value<br>|;
	if (@participants == 2) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="start_game">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="�J�n����" class="button_s"></form>|;
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="observe">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="�Q�����Ȃ�" class="button_s"></form>|;
	}
	else {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="observe">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="�Q�����Ȃ�" class="button_s"></form>|;
	}
}

sub observe { # �u�Q�����Ȃ��v����
	my @members = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		push @members, $line;
	}
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;

	my $is_entry = 0;
	my $index = index($participants, "$m{name},");
	if (!$state && -1 < $index && $m{c_turn} == 1) { # �Q���͂��Ă��邪�ްт͊J�n���Ă��Ȃ�
		$is_entry = 1;
		substr($participants, $index, length("$m{name},"), '');
	}

	my $is_reset = 0;
	if (length($participants)) { # ���ް����l�ł�����Ȃ�
		my @participants = split /,/, $participants;
		my %tmp_y = get_you_datas($participants[0]);
		unshift @members, "$state<>$time<>$participants<>$tmp_y{coin}<>\n";
	}
	else { # ���ް�̍Ō�̈�l���Ȃ𗣂ꂽ��ؾ��
		unshift @members, "<><><><><><>\n";
		$is_reset = GAME_RESET;
	}

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($state) {
		return "���łɹްт��n�܂��Ă��܂�";
	}
	elsif (!$is_entry) {
		return "�ްтɎQ�����Ă��܂���";
	}
	else {
		$m{c_turn} = $m{c_value} = $m{c_stock} = '0';
		&write_user;
		my $result_mes = "$m{name} ���Ȃ𗣂�܂���";
		if ($is_reset eq GAME_RESET) {
			&system_comment('�Q���ҕs�݂̂��߹ްт�ؾ�Ă��܂���');
			$result_mes = '';
		}
		return $result_mes;
	}
}

sub start_game {
	my @members = ();
	my @game_members = ();

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;
	my @participants = split /,/, $participants;

	my $is_start = 0;
	if (@participants == 2 && !$state && -1 < index($participants, "$m{name},") && $m{c_turn} == 1) { # �Q���҂��������܂ߓ�l�A�ްъJ�n�O�Ȃ�
		$state = 1;
		$is_start = 1;
	}
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && -1 < index($participants, "$mname,")) {
			push @game_members, $mname;
			$mturn = 2;
			$mtime = $time;
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	unshift @members, "$state<>$time<>$participants<>$rate<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($is_start) {
		for my $game_member (@game_members) {
			if ($game_member eq $m{name}) {
				$m{c_turn} = 2;
				&write_user;
			}
			else {
		 		&regist_you_data($game_member, 'c_turn', '2');
			}
		}
		return '�����I';
	}
}

sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants) = @_;
	unless (index($participants, "$m{name},") == 0) {
		print qq|<br>���肪�v�l���ł�|;
		return;
	}

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="number" class="text_box_b"> �ԍ�<input type="hidden" name="mode" value="play">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�ԍ��𓖂Ă�" class="button_s"></form>|;

	return if $m_stock == 0;

	print qq|<hr><form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="use_item">�A�C�e��<input type="text"  name="number" class="text_box_b"> �ԍ�<br>|;
	if (int($m_stock / 32) == 1) {
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="1">DOUBLE<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($m_stock / 16) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="2">HIGH&LOW<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($m_stock / 8) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="3">TARGET<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($m_stock / 4) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="4">SLASH<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($m_stock / 2) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="5">SHUFFLE<br>|;
		print qq|</label>| unless $is_moble;
	}
	if($m_stock % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="6">CHANGE |;
		print qq|</label>| unless $is_moble;
		for my $num (0 .. 2) {
			my $c = substr($m_value, $num, 1);
			print qq|<label>| unless $is_moble;
			print qq|<input type="radio" name="choicenum" value="$c">$c ����|;
			print qq|</label>| unless $is_moble;
		}
		print qq|<br>|;
	}
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�A�C�e�����g��" class="button_s"></form>|;
}

sub play {
	return "3�̐��������Ă�������" if !($in{number} ne '' && $in{number} !~ /[^0-9]/);

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;
	my @player = split /,/, $participants;
	my $is_my_turn = $player[0] eq $m{name};
	my ($e_name, $e_value);

	my %sames = ();
	my $is_find = 0;
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟

		if ($mname eq $player[1] && $is_my_turn) {
			$e_name = $mname;
			$e_value = $mvalue;
			$is_find = 1;
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	my $result_mes = '';
	my @game_member = ();
	my $is_reset = 0;
	my $penalty_coin = 0;
	if ($is_find) {
		my($hit, $blow) = &hb_count($in{number}, $e_value);
		$result_mes = "$in{number}:$hit �C�[�g $blow �o�C�g";
		$lastupdate = $time;
		if ($hit == 3) {
			$result_mes .= "����";
			@game_members = split /,/, $participants;
			$penalty_coin = $rate;
			($state, $lastupdate, $participants, $rate) = ('', '', '', '');
			$is_reset = 1;
		}
		$participants =~ s/^(.*?),(.*)/$2$1,/g; # ���쒆����ڲ԰���Ō���Ɉړ�
	}

	unshift @members, "$state<>$lastupdate<>$participants<>$rate<>\n"; # ͯ�ް
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
			for my $j (0..$i - 1) {
				$d++ if $number[$j] == $number[$i];
			}
			if ($d == 0) {
				for my $j (0..2) {
					$blow++ if $answer[$j] == $number[$i];
				}
			}
		}
	}
	return ($hit, $blow);
}

sub use_item {
	unless ($in{itemno}) {
		return "�g�����т�I��ł�������";
	}
	elsif ( ($in{itemno} == 1 || $in{itemno} == 3 || $in{itemno} == 6) && !($in{number} ne '' && $in{number} !~ /[^0-9]/) ) {
		return "���������Ă�������";
	}
	elsif ($in{itemno} == 6) {
		return "CHANGE �������鐔��I��ł�������" if $in{choicenum} eq '';
		return "CHANGE 1���̐�����I��ł�������" if 9 < $in{number};
		return "CHANGE�ŕς�����̂�HIGH���m��LOW���m�ł�" if (($in{number} < 5) xor ($in{choicenum} < 5));
	}

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;
	my @player = split /,/, $participants;
	my $is_my_turn = $player[0] eq $m{name};
	my ($e_name, $e_value);
	my ($m_turn, $m_value, $m_stock) = (0, 0, 0);
	my $my_index = -1; # @members�Ɋi�[����Ă��鎩���̃f�[�^�̃C���f�b�N�X

	my %sames = ();
	my @is_find = (0, 0); # ����f�[�^�ǂݍ��񂾂��A�����f�[�^�ǂݍ��񂾂�
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟
		$my_index++ unless $is_find[1];
		if ($mname eq $player[1] && $is_my_turn) {
			$e_name = $mname;
			$e_value = $mvalue;
			$is_find[0] = 1;
		}
		elsif ($mname eq $player[0] && $is_my_turn) {
			($m_turn, $m_value, $m_stock) = ($mturn, $mvalue, $mstock);
			$is_find[1] = 1;
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	my $result_mes = '';
	my @game_member = ();
	my $is_reset = 0;
	my $is_double = 0;
	my $penalty_coin = 0;
	my $is_ng = 0;
	if ($is_my_turn && $is_find[0] && $is_find[1]) {
		# DOUBLE �����_���ɑI�΂ꂽ������1�������J��������2��R�[���ł���
		if ($in{itemno} == 1 && int($m_stock / 32) == 1) {
			my($hit, $blow) = &hb_count($in{number}, $e_value);
			$m_stock -= 32;
			my $open_card = int(rand(3)+1);
			my @open_num = (int($m_value / 100), int($m_value / 10) % 10, $m_value % 10); # 3���̐�����z��ɕϊ�
			$result_mes .= "$m_value DOUBLE $m{name}��$open_card���ڂ�".$open_num[$open_card-1]."�ł�<br>";
			$result_mes .= "$in{number}:$hit �C�[�g $blow �o�C�g";
			if($hit == 3){
				$result_mes .= "����";
				@game_members = split /,/, $participants;
				$penalty_coin = $rate;
				($state, $lastupdate, $participants, $rate) = ('', '', '', '');
				$is_reset = 1;
			}
			else {
				$is_double = 1;
			}
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
			my @mm = (int($m_value / 100), int($m_value / 10) % 10, $m_value % 10); # 3���̐�����z��ɕϊ�
			my ($e_max, $e_min) = ($mm[0], $mm[1]);
			for my $i (0 .. 2) {
				$e_max = $mm[$i] if $e_max < $mm[$i];
				$e_min = $mm[$i] if $e_min > $mm[$i];
			}
			$result_mes = "SLASH ".($e_max - $e_min);
		}
		# SHUFFLE �����̐������V���b�t������
		elsif ($in{itemno} == 5 && int($m_stock / 2) % 2 == 1) {
			$m_stock -= 2;
			$result_mes = "SHUFFLE";
			my @num_arr = (int($m_value / 100), int($m_value / 10) % 10, $m_value % 10); # 3���̐�����z��ɕϊ�
			for my $i (0 .. 2) {
				my $j = int(rand($i + 1)); # ���񂷂�x�ɗ����͈͂��L���� 1����:0�`0 2����:0�`1 3����:0�`2
				my $tmp_n = $num_arr[$j]; # �����̃X���b�v
				$num_arr[$j] = $num_arr[$i];
				$num_arr[$i] = $tmp_n;
			}
			$m_value = int("$num_arr[0]$num_arr[1]$num_arr[2]");
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

	if ($is_my_turn && $result_mes && !$is_ng) {
		splice(@members, $my_index, 1, "$time<>$m{name}<>$addr<>$m_turn<>$m_value<>$m_stock<>\n");
		$lastupdate = $time;
		$participants =~ s/^(.*?),(.*)/$2$1,/g if $is_find[0] && $is_find[1] && !$is_double; # ���쒆����ڲ԰���Ō���Ɉړ�
	}

	unshift @members, "$state<>$lastupdate<>$participants<>$rate<>\n"; # ͯ�ް
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
