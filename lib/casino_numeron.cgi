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
	sub get_member
	sub show_game_info
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
# �߂�l�͑��Ƒ�񂪌Œ�($member_c, $member)�A����ȍ~�Ͷ��ɖ��ɵؼ��ٗv�f�A����炪show_game_info�ɓn���Ă���
sub get_member {
	# �Œ�ϐ�
	my $member  = ''; # �Q���ҁE�{���҂Ȃǂ��ׂĂ���ڲ԰��������
	my @members = (); # ���̔z��
	my @active_players = (); # ��ڲ���̎Q���҂̔z��
	my @non_active_players = (); # ���O���ꂽ�Q���҂̔z��

	# ���ɖ��̕ϐ�
	my $penalty_coin = 0;
	my @result_my_datas = ();

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
			@result_my_datas = ($m{c_turn}, $mvalue, $mstock);
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
#		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>$m{c_stock}<>\n";
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>0<>0<>\n"; # �����ŒE������̂ŗ]�v���ް��v��Ȃ��i���̶��ɍs�������ꂽ����c_turn�͕K�v�j
		@result_my_datas = ($m{c_turn}, $mvalue, $mstock);
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
		my @array = (['c_turn', '0'], ['c_value', '0'], ['c_stock', '0']);
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
			&regist_you_array($leave_player, @array);
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
				&regist_you_array($active_players[0], @array);
			}
			&system_comment("�Q���҂�$active_players[0]�����ƂȂ������߹ްт�ؾ�Ă��܂���");
		}
	}

	# �Œ菈��
	my $member_c = @members - 1;
	return ($member_c, $member, $state, $participants, $rate, @result_my_datas);
}

sub show_game_info {
	my ($state, $participants, $rate, @result_my_datas) = @_;

	my @participants = split /,/, $participants;

	print qq|<br>���ݏC�����ɂ�����܂�G��Ȃ������ǂ��Ǝv��<br>|;
	print qq|��ڲ���ɎQ���҂�10�����u��(�v�l�P�\\�𒴂�)�Ă���̂𑼂̎Q���҂��{������ƕ��u��ڲ԰������<br>|;
	print qq|�ްт̍ŏI��ڲ����20�����u����Ă���̂�ްтɎQ�����Ă��Ȃ��{���҂��{������Ɨ���<br><br>|;
	if ($participants) {
		print qq|�q�����:$rate �Q����:$participants|;
	}
	else {
		print qq|���ް��W��|;
	}

	if ($state) { # �ްт��J�n���Ă���
		print qq|<br>�����̔ԍ�:$result_my_datas[1]| if -1 < index($participants, "$m{name},");
		&play_form($participants, @result_my_datas);
	}
	else { # �ްт��J�n���Ă��Ȃ�
		if (-1 < index($participants, "$m{name},")) { # �ްтɎQ�����Ă���
			&start_game_form($participants, @result_my_datas); # �J�n̫��
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

sub show_game {
	my @members = ();
	$m{c_turn} = 0;
	&write_user;

	open my $fh, "< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;

	my %sames = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟

		if (-1 < index($participants, "$mname,") && $mname eq $m{name}) { # �Q���҂��ް�����
			print qq|<br>�����̔ԍ�:$mvalue<br>|;
		}
	}
	close $fh;
	return;
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
	if ($in{number} > 0 && $in{number} !~ /[^0-9]/) {
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
			$mvalue = $number[0] * 100 + $number[1] * 10 + $number[2];
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
	my ($participants, @result_my_datas) = @_;
	my @participants = split /,/, $participants;

	print qq|<br>�����̔ԍ�:$result_my_datas[1]<br>|;
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
	my ($participants, @result_my_datas) = @_;
	return unless index($participants, "$m{name},") == 0;

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="number" class="text_box_b"> �ԍ�<input type="hidden" name="mode" value="play">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�ԍ��𓖂Ă�" class="button_s"></form>|;

	print qq|���ьn���ڐA|;
=pod
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="hidden" name="mode" value="use_item">�A�C�e��<input type="text"  name="number" class="text_box_b"> �ԍ�<br>|;
	if(int($result_my_datas[2] / 32) == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="1">DOUBLE<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($result_my_datas[2] / 16) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="2">HIGH&LOW<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($result_my_datas[2] / 8) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="3">TARGET<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($result_my_datas[2] / 4) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="4">SLASH<br>|;
		print qq|</label>| unless $is_moble;
	}
	if(int($result_my_datas[2] / 2) % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="5">SHUFFLE<br>|;
		print qq|</label>| unless $is_moble;
	}
	if($result_my_datas[2] % 2 == 1){
		print qq|<label>| unless $is_moble;
		print qq|<input type="radio" name="itemno" value="6">CHANGE<br>|;
		print qq|</label>| unless $is_moble;
	}
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�A�C�e�����g��" class="button_s"></form>|;
=cut
}

sub play {
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $rate) = split /<>/, $head_line;
	my @player = split /,/, $participants;
	my ($e_name, $e_value);

	my %sames = ();
	my $is_find = 0;
	my @members = ();
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟

		if ($mname eq $player[1]) {
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
	if($in{number} > 0 && $in{number} !~ /[^0-9]/){
		my($hit, $blow) = &hb_count($in{number}, $e_value);
		$result_mes = "$in{number}:$hit �C�[�g $blow �o�C�g";
		$lastupdate = $time;
		if($hit == 3){
			$result_mes .= "����";
			@game_members = split /,/, $participants;
			$penalty_coin = $rate;
			($state, $lastupdate, $participants, $rate) = ('', '', '', '');
			$is_reset = 1;
		}
		$participants =~ s/^(.*?),(.*)/$2$1,/g if $is_find; # ���쒆����ڲ԰���Ō���Ɉړ�
	}

	unshift @members, "$state<>$lastupdate<>$participants<>$rate<>\n"; # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	# �I������
	if ($is_reset) {
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
#=====
=pod
	my $e_name;
	my $e_value;
	my $ret_mes = '';
	my @members = ();
	my $reset_flag = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		push @members, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			$e_name = $mname;
			$e_value = $mvalue;
		};
	}
	close $fh;

	return("����̔Ԃł�") if $state ne $m{name}; # ���얢�m�F�����ǁAwhile���[�v����O�� $state ������ꂽ����� close return ���������ǂ��̂ł�

	if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
		my($hit, $blow) = &hb_count($in{comment}, $e_value);
		$state = $e_name;
		$ret_mes = "$in{comment}:$hit �C�[�g $blow �o�C�g";
		if($hit == 3){
			$ret_mes .= "����";
			my $cv = -1 * &coin_move(-1 * $max_bet, $e_name);
			&coin_move($cv, $m{name});
			$state = '';
			$leader = '';
			$max_bet = 0;
			$reset_flag = 1;
		}
		unshift @members, "$leader<>$max_bet<>$state<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
		print $fh @members;
		close $fh;
	}

	if($reset_flag){
		&reset_game;
	}

	return ($ret_mes);
=cut
}

sub hb_count {
    my ($m_number, $y_number) = @_;
	my @number = (int($m_number / 100), int($m_number / 10) % 10, $m_number % 10);
	my @answer = (int($y_number / 100), int($y_number / 10) % 10, $y_number % 10);
	my $hit = 0;
	my $blow = 0;
	for my $i (0..2) {
		if($answer[$i] == $number[$i]){
			$hit++;
		}else{
			my $d = 0;
			for my $j (0..$i - 1){
				if($number[$j] == $number[$i]) {
					$d++;
				}
			}
			if($d == 0){
				for my $j (0..2){
					if($answer[$j] == $number[$i]) {
						$blow++;
					}
				}
			}
		}
	}
	return ($hit, $blow);
}


=pod
sub run {
	if ($in{mode} eq "play") {
	    $in{comment} = &play_number;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "item") {
	    $in{comment} = &use_item;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "leader") {
	    $in{comment} = &make_leader;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "bet") {
	    $in{comment} = &bet($in{max_bet});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "start") {
	    $in{comment} = &start_game;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "exit") {
	    $in{comment} = &exit_game;
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "reset") {
	    $in{comment} = &reset_game;
	    &write_comment if $in{comment};
	}
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember) = &get_member;

	if($m{c_turn} eq '0' || $m{c_turn} eq ''){
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	}elsif($m{name} ne $leader) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="exit">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="��߂�" class="button_s"></form><br>|;
	}
	print qq|<h2>$this_title</h2>|;

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="����" class="button_s"><br>|;

	unless ($is_mobile) {
		print qq|�����۰��<select name="reload_time" class="select1"><option value="0">�Ȃ�|;
		for my $i (1 .. $#reload_times) {
			print $in{reload_time} eq $i ? qq|<option value="$i" selected>$reload_times[$i]�b| : qq|<option value="$i">$reload_times[$i]�b|;
		}
		print qq|</select>|;
	}
	print qq|</form><font size="2">$member_c�l:$member</font><br>|;
	print $leader eq '' ? qq|�e:��W�� �q�����:<br>|:qq|�e:$leader �q�����:$max_bet �ΐ푊��:$wmember<br>���Ȃ��̔ԍ�:$m{c_value}<br>|;

	if($leader){
		
		if($state eq $m{name} && $m{c_turn}){
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="text"  name="comment" class="text_box_b"> �ԍ�<input type="hidden" name="mode" value="play">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="�ԍ��𓖂Ă�" class="button_s"></form><br>|;
			
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="item">�A�C�e��<input type="text"  name="comment" class="text_box_b"> �ԍ�<br>|;
			if(int($m{c_stock} / 32) == 1){
				print qq|<input type="radio" name="itemno" value="1">DOUBLE<br>|;
			}
			if(int($m{c_stock} / 16) % 2 == 1){
				print qq|<input type="radio" name="itemno" value="2">HIGH&LOW<br>|;
			}
			if(int($m{c_stock} / 8) % 2 == 1){
				print qq|<input type="radio" name="itemno" value="3">TARGET<br>|;
			}
			if(int($m{c_stock} / 4) % 2 == 1){
				print qq|<input type="radio" name="itemno" value="4">SLASH<br>|;
			}
			if(int($m{c_stock} / 2) % 2 == 1){
				print qq|<input type="radio" name="itemno" value="5">SHUFFLE<br>|;
			}
			if($m{c_stock} % 2 == 1){
				print qq|<input type="radio" name="itemno" value="6">CHANGE<br>|;
			}
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="�A�C�e�����g��" class="button_s"></form><br>|;
		}elsif($state eq 'waiting' && $m{name} ne $leader && ($m{c_turn} eq '0' || $m{c_turn} eq '')) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="text"  name="number" class="text_box_b"> �����̔ԍ�<br><input type="text"  name="comment" class="text_box_b"> ��� <input type="hidden" name="mode" value="bet"><input type="hidden" name="max_bet" value="$max_bet">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="�q����" class="button_s"></form><br>|;
		}elsif($state eq 'waiting' && $m{name} eq $leader && $in{mode} ne 'leader' && $waiting) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="start">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="waiting" value="$waiting"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="�J�n" class="button_s"></form><br>|;
		}elsif($state eq 'waiting' && $m{name} eq $leader && $in{mode} ne 'leader' && !$waiting) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="reset">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="waiting" value="$waiting"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="��߂�" class="button_s"></form><br>|;
		}
	}else {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="text"  name="number" class="text_box_b"> �����̔ԍ�<br><input type="hidden" name="mode" value="leader">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="�e�ɂȂ�" class="button_s"></form><br>|;
	}
	print qq|<hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
}

sub get_member { # flock
	my $is_find = 0;
	my $leave_name = '';
	my @leave_members = ();
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $waiting = 0;
	my $wmember = '';
	my $leader_find = 0;
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	push @members, "$leader<>$max_bet<>$state<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			if($mturn > 0){
				$leave_name = $mname if $state ne 'waiting';
				push @leave_members, $mname;
			}else {
				next;
			}
		}
		# push @leave_members, $mname; �����ȑO�ɂȂ��ƃ}�Y���C������
		next if $sames{$mname}++; # �����l�Ȃ玟
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		}
		if ($mturn > 0 && $mname ne $leader){
			$waiting++;
			$wmember = $mname;
		}elsif($mname eq $leader){
			$leader_find = 1;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if (@leave_members) {
		for my $name (@leave_members) {
			&you_c_reset($name);
		}
	}

	if($leave_name){
		&reset_game($leave_name);
	}elsif($leader && !$leader_find){
		&reset_game;
	}

	my $member_c = @members - 1;

	return ($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember);
}
=cut
sub play_number {
	my $e_name;
	my $e_value;
	my $ret_mes = '';
	my @members = ();
	my $reset_flag = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		push @members, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			$e_name = $mname;
			$e_value = $mvalue;
		};
	}
	close $fh;

	return("����̔Ԃł�") if $state ne $m{name}; # ���얢�m�F�����ǁAwhile���[�v����O�� $state ������ꂽ����� close return ���������ǂ��̂ł�

	if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
		my($hit, $blow) = &hb_count($in{comment}, $e_value);
		$state = $e_name;
		$ret_mes = "$in{comment}:$hit �C�[�g $blow �o�C�g";
		if($hit == 3){
			$ret_mes .= "����";
			my $cv = -1 * &coin_move(-1 * $max_bet, $e_name);
			&coin_move($cv, $m{name});
			$state = '';
			$leader = '';
			$max_bet = 0;
			$reset_flag = 1;
		}
		unshift @members, "$leader<>$max_bet<>$state<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
		print $fh @members;
		close $fh;
	}

	if($reset_flag){
		&reset_game;
	}

	return ($ret_mes);
}

sub use_item {
	my $e_name;
	my $e_value;
	my $ret_mes = '';
	my @members = ();
	my $reset_flag = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		push @members, $line;
		if ($mturn > 0 && $mname ne $m{name}){
			$e_name = $mname;
			$e_value = $mvalue;
		};
	}
	close $fh;

	return("����̔Ԃł�") if $state ne $m{name};
	
	if($in{itemno} == 1 && int($m{c_stock} / 32) == 1){
		if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
			my($hit, $blow) = &hb_count($in{comment}, $e_value);
			$m{c_stock} -= 32;
			&write_user;
			my $open_card = int(rand(3)+1);
			my $open_num = 0;
			if($open_card == 1){
				$open_num = int($m{c_value} / 100);
			}elsif($open_card == 2){
				$open_num = int($m{c_value} / 10) % 10;
			}else{
				$open_num = $m{c_value} % 10;
			}
			$ret_mes .= "DOUBLE $m{name}��$open_card���ڂ�$open_num�ł�<br>";
			$ret_mes .= "$in{comment}:$hit �C�[�g $blow �o�C�g";
			if($hit == 3){
				$ret_mes .= "����";
				my $cv = -1 * &coin_move(-1*$max_bet, $e_name);
				&coin_move($cv, $m{name});
				$state = '';
				$leader = '';
				$max_bet = 0;
				$reset_flag = 1;
			}
			unshift @members, "$leader<>$max_bet<>$state<>\n";
			open my $fh, "> ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
			print $fh @members;
			close $fh;
		}
	}elsif($in{itemno} == 2 && int($m{c_stock} / 16) % 2 == 1){
		$m{c_stock} -= 16;
		&write_user;
		$state = $e_name;
		my @hl = ();
		if(int($e_value / 100) >= 5){
			$hl[0] = "high";
		}else{
			$hl[0] = "low";
		}
		if(int($e_value / 10) % 10 >= 5){
			$hl[1] = "high";
		}else{
			$hl[1] = "low";
		}
		if($e_value % 10 >= 5){
			$hl[2] = "high";
		}else{
			$hl[2] = "low";
		}
		$ret_mes = "HIGH&LOW $hl[0],$hl[1],$hl[2]";
		unshift @members, "$leader<>$max_bet<>$state<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
		print $fh @members;
		close $fh;
	}elsif($in{itemno} == 3 && int($m{c_stock} / 8) % 2 == 1){
		if($in{comment} >= 0 && $in{comment} !~ /[^0-9]/){
			$m{c_stock} -= 8;
			&write_user;
			my $target_num = $in{comment} % 10;
			my $target_place;
			if(int($e_value / 100) == $target_num){
				$target_place = "1���ڂł�";
			}elsif(int($e_value / 10) % 10 == $target_num){
				$target_place = "2���ڂł�";
			}elsif($e_value % 10 == $target_num){
				$target_place = "3���ڂł�";
			}else{
				$target_place = "����܂���";
			}
			$ret_mes .= "TARGET $target_num��$target_place";
			$state = $e_name;
			unshift @members, "$leader<>$max_bet<>$state<>\n";
			open my $fh, "> ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
			print $fh @members;
			close $fh;
		}
	}elsif($in{itemno} == 4 && int($m{c_stock} / 4) % 2 == 1){
		$m{c_stock} -= 4;
		&write_user;
		$state = $e_name;
		my $e_max = int($e_value / 100);
		my $e_min = int($e_value / 100);
		if(int($e_value / 10) % 10 > $e_max){
			$e_max = int($e_value / 10) % 10;
		}
		if(int($e_value / 10) % 10 < $e_min){
			$e_min = int($e_value / 10) % 10;
		}
		if($e_value % 10 > $e_max){
			$e_max = $e_value % 10;
		}
		if($e_value % 10 < $e_min){
			$e_min = $e_value % 10;
		}
		my $s_num = $e_max - $e_min;
		$ret_mes = "SLASH $s_num";
		unshift @members, "$leader<>$max_bet<>$state<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
		print $fh @members;
		close $fh;
	}elsif($in{itemno} == 5 && int($m{c_stock} / 2) % 2 == 1){
		$m{c_stock} -= 2;
		$state = $e_name;
		$ret_mes = "SHUFFLE";
		my @num_arr = (int($m{c_value} / 100), int($m{c_value} / 10) % 10, $m{c_value} % 10);
		my @n_rank = (int(rand(3)), int(rand(3)), int(rand(3)));
		if($n_rank[0] == $n_rank[1]){
			$n_rank[1] = ($n_rank[1] + 1) % 3;
		}
		while($n_rank[0] == $n_rank[2] || $n_rank[1] == $n_rank[2]){
			$n_rank[2] = ($n_rank[2] + 1) % 3;
		}
		my $new_num = 100 * $num_arr[$n_rank[0]] + 10 * $num_arr[$n_rank[1]] + $num_arr[$n_rank[2]];
		$m{c_value} = $new_num;
		&write_user;
		unshift @members, "$leader<>$max_bet<>$state<>\n";
		open my $fh, "> ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
		print $fh @members;
		close $fh;
	}elsif($in{itemno} == 6 && $m{c_stock} % 2 == 1){
		if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
			$m{c_stock} -= 1;
			$state = $e_name;
			my @old_arr = (int($m{c_value} / 100), int($m{c_value} / 10) % 10, $m{c_value} % 10);
			my @new_arr = (int($in{comment} / 100) % 10, int($in{comment} / 10) % 10, $in{comment} % 10);
			my $diff = 0;
			my $diff_hl;
			if($old_arr[0] != $new_arr[0]){
				$diff++;
				$diff_pos = 1;
				if($old_arr[0] < 5 && $new_arr[0] < 5){
					$diff_hl = 'low';
				}elsif($old_arr[0] >= 5 && $new_arr[0] >= 5){
					$diff_hl = 'high';
				}else{
					return "CHANGE�ŕς�����̂�HIGH���m��LOW���m�ł�"
				}
			}
			if($old_arr[1] != $new_arr[1]){
				$diff++;
				$diff_pos = 2;
				if($old_arr[1] < 5 && $new_arr[1] < 5){
					$diff_hl = 'low';
				}elsif($old_arr[1] >= 5 && $new_arr[1] >= 5){
					$diff_hl = 'high';
				}else{
					return "CHANGE�ŕς�����̂�HIGH���m��LOW���m�ł�"
				}
			}
			if($old_arr[2] != $new_arr[2]){
				$diff++;
				$diff_pos = 3;
				if($old_arr[2] < 5 && $new_arr[2] < 5){
					$diff_hl = 'low';
				}elsif($old_arr[2] >= 5 && $new_arr[2] >= 5){
					$diff_hl = 'high';
				}else{
					return "CHANGE�ŕς�����̂�HIGH���m��LOW���m�ł�"
				}
			}
			if($diff != 1){
				return "CHANGE�ŕς�����͈̂ꖇ�ł� $diff"
			}
			my $new_num = 100 * $new_arr[0] + 10 * $new_arr[1] + $new_arr[2];
			$m{c_value} = $new_num;
			&write_user;
			$ret_mes .= "CHANGE $m{name}��$diff_pos���ڂ�$diff_hl�ł�<br>";
			unshift @members, "$leader<>$max_bet<>$state<>\n";
			open my $fh, "> ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
			print $fh @members;
			close $fh;
		}
	}else{
		return;
	}
	
	if($reset_flag){
		&reset_game;
	}
	return ($ret_mes);
}

sub make_leader { # flock
	my @number;
	return("��݂�����܂���") if $m{coin} < 0;
	if($in{number} > 0 && $in{number} !~ /[^0-9]/){
		@number = (int($in{number} / 100) % 10, int(($in{number} / 10) % 10), int($in{number} % 10));
		if($number[0] == $number[1] || $number[0] == $number[2] || $number[1] == $number[2]){
			return ("���������͓�x�g���܂���");
		}
	}else{
		return ("3�̈قȂ鐔�������Ă�������");
	}
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	if($leader eq ''){
		$leader = $m{name};
		$max_bet = $m{coin};
#		$max_bet = 10;
		$state = 'waiting';
		$m{c_turn} = 1;
		$m{c_value} = $number[0] * 100 + $number[1] * 10 + $number[2];
		$m{c_stock} = 63;
		&write_user;
	}
	push @members, "$leader<>$max_bet<>$state<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # �����l�Ȃ玟
		push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	return ("$leader ���e�ł� �q�����:$max_bet");
}
=pod
sub start_game{
	my @members = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	$state = $leader;
	push @members, "$leader<>$max_bet<>$state<>\n";
	while (my $line = <$fh>) {
		push @members, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	return ("�����I");
}
=cut
sub reset_game{ # flock
	my $leave_name = shift;
	my $is_find = 0; # $leave_name ����ڲ԰�����݂��邩
	my @winners = (); # �ްя�����
	my @members = (); # �{���Ҋ܂ޑS��ڲ԰

	$m{c_turn} = 0;
	&write_user;

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($leave_name ne '' && $mturn) { # �s�҂����݂���ްт̎Q����
			if ($leave_name eq $mname) { # �s��
				$is_find = 1;
			}
			else {
				push @winners, $mname; # ����
			}
		}
		push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n"; # �{���Ҋ܂ޑS��ڲ԰
	}
	unshift @members, "<>0<><>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my($leader, $max_bet, $state) = split /<>/, $head_line; # �ްт̏��
	my $ev = 0;

	# ��݈ŗN���΍� �܂��s�҂��纲݂ނ�����
	if ($is_find) {
		$ev = -1 * &coin_move(-1*$max_bet, $leave_name);
		&you_c_reset($leave_name);
	}

	# �s�҂���ނ���������݂������҂ɕ��z
	for my $name (@winners) {
		&coin_move($ev, $name) if $is_find;
		&you_c_reset($name);
	}

	return ("���Z�b�g���܂���");
}

sub bet{
	my @number;
	my @members = ();
	return("��݂�����܂���") if $m{coin} < 0;
	if($in{number} > 0 && $in{number} !~ /[^0-9]/){
		@number = (int($in{number} / 100) % 10, int(($in{number} / 10) % 10), int($in{number} % 10));
		if($number[0] == $number[1] || $number[0] == $number[2] || $number[1] == $number[2]){
			return ("���������͓�x�g���܂���");
		}
	}else{
		return ("3�̈قȂ鐔�������Ă�������");
	}
	open my $fh, "< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		push @members, $line;
		if ($mname eq $leader) {
			$waiting--;
		}
		$waiting++ if $mturn > 0;
	}
	close $fh;
	
	if($waiting){
		return("���łɑΐ�҂����܂�");
	}else{
		my $max = shift;
		my $v;
		if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
			$v = $in{comment};
			$v = $m{coin} if $v > $m{coin};
			if($v > 0){
				$v = $max if $v > $max;
				$max_bet = $v;
				$m{c_turn} = 1;
				$m{c_value} = $number[0] * 100 + $number[1] * 10 + $number[2];
				$m{c_stock} = 63;
				&write_user;
				unshift @members, "$leader<>$max_bet<>$state<>\n";
				open my $fh, "> ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
				print $fh @members;
				close $fh;
				return("$m{name} �� $v ��� �q���܂���");
			}
		}
	}
}

sub exit_game{
	my $waiting = 0;
	open my $fh, "< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	my $head_line = <$fh>;
	my($leader, $max_bet, $state) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($mturn > 0 && $mname ne $leader){
			$waiting++;
		}
	}
	close $fh;
	
	if($m{name} eq $leader && $waiting){
		return("�ΐ푊�肪���܂��Ă��܂�")
	}
	if ($state ne 'waiting'){
		return("�Q�[�����n�܂��Ă��܂�");
	}
	
	$m{c_turn} = 0;
	&write_user;
	return("$m{name} �� ��߂܂���");
}

1;#�폜�s��
