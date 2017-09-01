#================================================
# ���ɋ��p�֐�
#================================================

use constant GAME_RESET => 1; # �ްт̍X�V���~�܂��Ă���
use constant LEAVE_PLAYER => 2; # �Q���҂���è�ނɂȂ��Ă���

$_header_size = 5; # ͯ�ް�z����ް�����
($_state, $_lastupdate, $_participants, $_participants_datas, $_rate) = (0 .. $_header_size - 1); # ͯ�ް�z��̲��ޯ��

$limit_think_time = 60 * 10; # 10�����u����ڲ԰���O
$limit_game_time = 60 * 20; # 20�����u�Źް�ؾ��

sub init_header {
	my $ref_arr = shift; # �̧�ݽ�� shift ����Ȃ��Ǝ擾�ł��Ȃ��i$_���Ǝ��̂�[0]�����o�����H�j
	$ref_arr->[$_] = '' for (0 .. $_header_size + $header_size - 1);
}

sub h_to_s { # ͯ�ް�z��𕶎���ɂ��ĕԂ�
	my @arr = @_;
	my $str = '';
	$str .= "$arr[$_]<>" for (0 .. $_header_size + $header_size - 1);
	return "$str\n";
}

sub admin_reset {
	$m{c_turn} = 0;
	&write_user;

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh '';
	close $fh;

	my @head = split /<>/, $head_line; # ͯ�ް
	my @participants = &get_members($head[$_participants]);
	for my $game_member (@participants) {
		if ($game_member eq $m{name}) {
			$m{c_turn} = 0;
			&write_user;
		}
		else {
	 		&regist_you_data($game_member, 'c_turn', '0');
		}
	}
}

sub admin_reset2 {
	&regist_you_data($in{name}, 'c_turn', '0');
#	my $r = '';
#	my %p = &get_you_datas($in{name}, 0);
#	$mes .= "$in{name} c_turn $p{c_turn}";
#	my @members = ();

#	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
#	while (my $id = readdir $dh) {
#		next if $id =~ /\./;
#		next if $id =~ /backup/;

#		my %p = &get_you_datas($id, 1);
#		if ($p{c_turn} ne '0') {
#			my $name = pack 'H*', $id;
#			push @members, $name;
#			$r .= "$name $p{c_turn} ";
#		}
#	}
#	closedir $dh;

#	for my $i (0 .. $#members) {
#		&regist_you_data($members[$i], 'c_turn', '0');
#	}

	return $r;
}

=pod
��ȏ����̗���
_casino_funcs.cgi
	sub _default_run
		call &{$in{mode}} ۰�ް ����ނ̒l����֐����Ăяo��
		call @datas = &_get_menber
	sub _get_menber
		call &show_game_info(@datas)
	sub _participate �u�Q������v����
	sub observe �u�Q�����Ȃ��v����

this_file.cgi
	sub run
		call _default_run
	sub show_game_info(@datas)
	sub participate_form �u�Q������v��̫��
	sub participate �u�Q������v���� ڰĂ�n������
	sub start_game_form �u�J�n����v�u�Q�����Ȃ��v��̫��
	sub start_game �u�J�n����v���� ͯ�ް���`
	�u�Q�����Ȃ��v������_casino_funcs.cgi�Œ�`
	sub play_form ��ڲ��̫��
	sub play ��ڲ����
	�ȏ�̻��ٰ�݂������Ă���΂Ƃ肠��������
	sub &{$in{mode}} ���̑�۰�ް�ɑΉ����鏈��

show_game_info����ڲ��ʂȂǂ�\�� ������ͯ�ް�ް����n���Ă���
��ڲ��ʂŕ\���������ނ̒�`(���̺���ޒl���֐��Ƃ��ČĂяo��)
����ޒl����Ăяo�����֐����`
=cut

#================================================
# �ΐl���ɂ̊�{�I��Ҳ݉��
# $option_form �ɒǉ���̫�т�ݒ肵�Ă����Βǉ��ł���
#================================================
sub _default_run {
#	my $_default = $_; # ���ĕ����̗L��
	$in{comment} = &{$in{mode}} if $in{mode} && $in{mode} ne 'write'; # �e����ނɑΉ�����֐��ւ�۰�ް
	&write_comment if $in{comment};

	my ($member_c, $member, @datas) = &_get_member;

#	if($m{c_turn} eq '0' || $m{c_turn} eq ''){
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;

	if ($m{c_turn}) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="comment" value="������Ɨ���"><input type="hidden" name="mode" value="write">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="������Ɨ���" class="button_s">|;
		print qq|</form>|;
	}
	if ($m{name} eq 'nanamie') {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("admin_reset", "ؾ��");
		print qq|</form>|;

		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="text"  name="name" class="text_box_b"> հ�ް��|;
		print &create_submit('admin_reset2', 'c_turn');
		print qq|</form>|;
	}

	print $option_form;
#	}

	print qq|<h2>$this_title</h2>|;
	print qq|$mes|;
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

	&_show_game_info(@datas);

	print qq|<hr>|;
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my ($btime, $bdate, $bname, $bcountry, $bshogo, $baddr, $bcomment, $bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
}

#================================================
# �ΐl���ɂ����ް�Ǘ�
# show_game_info �ɓn���߂�l�̌Œ蕔�� ($m_turn, $m_value, $m_stock, $state, $lastupdate, $participants, $participants_datas, $rate)
# �ȍ~�̖߂�l�Ͷ��ɖ��̵ؼ����ް� �ؼ����ް����̂� start_game �Őݒ肷��
# $participants_datas �ɑS�Q���҂� name, value, stock ���������񂪓����Ă��� ex. name1:value1:stock1;name2:value2:stock2;
# $participants_datas �𑀍삷��K�v�͓��ɂȂ� ����ށ�_get_member�̏��ŌĂ΂��̂ŁA����ނ���ڲ԰�ް�������������΂��Ƃ͎����œǂݒ���
# $participants ����݂̗���������Ă���̂ŕ��я�����o�^�����t�Z�ł��Ȃ�
# ����ɁAmember.cgi �t�@�C���̕��я����Q�����ɂȂ��Ă���i��l�ڂ̎Q���ҁi�e�j�� member.cgi ��2�s��(1�s�ڂ�ͯ�ް)�A��l�ڂ̎Q���҂�3�s��...�j
#================================================
sub _get_member {
	my $member  = ''; # �Q���ҁE�{���҂Ȃǂ��ׂĂ���ڲ԰��������
	my @members = (); # ���̔z��
	my ($m_turn, $m_value, $m_stock) = (0, '', ''); # �����̃f�[�^
	my @active_players = (); # ��ڲ���̎Q���҂̔z��
	my @non_active_players = (); # ���O���ꂽ�Q���҂̔z��
	my $penalty_coin = 0; # ���O or ؾ�Ď�������è
	my $is_game = 0; # �ްт��J�n���Ă��邩

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	# ���ɂ��ް����
	# �ްт̏�ԁA�ްт̍ŏI�X�V���ԁA�ްт̎Q���ҁA�Q���҂��ް��AڰāA�ȍ~�Ͷ��ɖ��̵ؼ����ް�
	my @head_datas = split /<>/, $head_line;

	my $is_reset = 0; # ��O�҂ɂ��ؾ�āFGAME_RESET�A�Q���҂ɂ��E���m�F�FLEAVE_PLAYER
	if (&is_member($head_datas[2], "$m{name}")) { # �Q���҂ɂ��۰�ނŹްт̍ŏI�X�V���Ԃ��X�V
		$head_datas[1] = $time;
	}
	elsif ($head_datas[1] && $m{c_turn} < 1 && ($head_datas[1] + $limit_game_time < $time) && $head_datas[2] && $head_datas[2] !~ "\Q$m{name},\E") { # ��Q���҂��~�܂��Ă���ްт��{��������ؾ��
		$is_reset = GAME_RESET;
		@non_active_players = split /,/, $head_datas[2];
		$penalty_coin = $head_datas[4] if $head_datas[0]; # ���łɹްт��J�n���Ă����纲ݖv��
		$is_game = $head_datas[0];
		$head_datas[$_] = '' for (0 .. $_header_size + $header_size - 1);
	}

	my %sames = ();
	my $is_find = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟

		unless ($head_datas[2]) { # �Q���҂���l�����Ȃ�
			if ($mname eq $m{name}) {
				$is_find = 1;
				push @members, "$time<>$m{name}<>$maddr<>$m{c_turn}<><><>\n";
				$member .= "$mname($m{c_turn}),";
			}
			else {
				if ($time < $mtime + $limit_member_time) {
					push @members, "$mtime<>$mname<>$maddr<>$mturn<><><>\n";
					$member .= "$mname($mturn),";
				}
			}
			next;
		}

		my $is_entry = &is_member($head_datas[2], "$mname");
		if ($mname eq $m{name}) {
			$is_find = 1;
			$member .= "$mname($m{c_turn}),";
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$mvalue<>$mstock<>\n"; # �����ŒE������̂ŗ]�v���ް��v��Ȃ��i���̶��ɍs�������ꂽ����c_turn�͕K�v�j
			($m_turn, $m_value, $m_stock) = ($m{c_turn}, $mvalue, $mstock);
			if ($is_entry) {
				push @active_players, "$m{name}";
				$head_datas[3] = &update_member_datas($head_datas[3], $mname, $mvalue, $mstock); # s/(.*?)$name:.*?;(.*)/$1$name:$mvalue:$mstock;$2/;
#				my $name = unpack 'H*', "$m{name}";
#				$head_datas[3] =~ s/(.*?)$name:.*?;(.*)/$1$name:$mvalue:$mstock;$2/;
			}
		}
		else {
			# ��è�ނȎQ���҂Ʊ�è�ނȉ{���҂����c��
			if ( ($is_entry && ($time < $mtime + $limit_think_time)) || ($time < $mtime + $limit_member_time) ) {
				$member .= "$mname($mturn),";
				push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
				if ($is_entry) {
					push @active_players, "$mname";
					$head_datas[3] = &update_member_datas($head_datas[3], $mname, $mvalue, $mstock); # s/(.*?)$name:.*?;(.*)/$1$name:$mvalue:$mstock;$2/;
#					my $name = unpack 'H*', "$mname";
#					$head_datas[3] =~ s/(.*?)$name:.*?;(.*)/$1$name:$mvalue:$mstock;$2/;
				}
			}
			else {
				if ($is_entry && &is_member($head_datas[2], "$m{name}")) { # �Q���҂�e����͎̂Q���҂̊m�F���K�v
#					my $name = unpack 'H*', "$mname";
					$head_datas[2] = &remove_member($head_datas[2], $mname); # �Q���ҕ����񂩂��è����ڲ԰�����O
					$head_datas[3] = &remove_member_datas($head_datas[3], $mname); # �S�Q�����ް������񂩂��è����ڲ԰���ް������O

#					$head_datas[2] =~ s/(.*?)$name,(.*)/$1$2/; # �Q���ҕ����񂩂��è����ڲ԰�����O
#					$head_datas[3] =~ s/(.*?)$name:.*?;(.*)/$1$2/; # �S�Q�����ް������񂩂��è����ڲ԰���ް������O
					push @non_active_players, "$mname"; # ���O���ꂽ�Q���҂�ǉ�
					# �قڂقڃk�������p�H
#					$rate = $m{coin} unless $state; # ��ڲ���łȂ���Γq��������c������ڲ԰�̑S��݂�
				}
			}
		}
	}
	unless ($is_find) { # �������{���҂ɂ��Ȃ��Ȃ�ǉ�
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<><><>\n"; # �����ŒE������̂ŗ]�v���ް��v��Ȃ��i���̶��ɍs�������ꂽ����c_turn�͕K�v�j
		($m_turn, $m_value, $m_stock) = ($m{c_turn}, '', '');
		$member .= "$m{name}($m{c_turn}),";
	}

	if (!$is_reset && @non_active_players > 0) { # GAME_RESET�ŏ���������Ă��炸�A���u��ڲ԰������ꍇ
		$is_reset = LEAVE_PLAYER;
		$penalty_coin = $head_datas[4] if $head_datas[0];
		$is_game = $head_datas[0];
		if (@active_players == 1 && $is_game) {
			$head_datas[$_] = '' for (0 .. $_header_size + $header_size - 1);
		}
	}

	my $header = '';
	$header .= "$head_datas[$_]<>" for (0 .. $_header_size + $header_size - 1);
	unshift @members, "$header\n"; # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($is_reset) { # ���u���ꂽ�ްт����u���Ă�����ڲ԰�̕Еt��
		my @zeros = (['c_turn', '0'], ['c_value', '0'], ['c_stock', '0']);
		for my $leave_player (@non_active_players) {
			# �ް�ؾ��
#			if ($is_reset eq GAME_RESET) {
#				&coin_move(-0.5 * $penalty_coin, $leave_player) if $penalty_coin;
#			}
#			elsif ($is_reset eq LEAVE_PLAYER) {
			if ($is_reset eq LEAVE_PLAYER) {
				if ($is_game) {
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
			&system_comment($is_game ? "���u���ꂽ��ڲ���̹ްт�ؾ�Ă��܂���" : '���u���ꂽ��W���̹ްт�ؾ�Ă��܂���');
		}
		elsif ($is_game && @active_players == 1) {
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

#	if (!&is_member($head_datas[2], "$m{name}") && 0 < $m{c_turn}) {
#		$m{c_turn} = 0;
#		&write_user;
#	}

	my $member_c = @members - 1;

	return ($member_c, $member, $m_turn, $m_value, $m_stock, @head_datas);
}

#================================================
# �ްщ�ʂɕ\���������̒�`
#================================================
sub _show_game_info {
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	my @participants = &get_members($head[$_participants]);

	if ($head[$_participants]) {
		&show_game_info($m_turn, $m_value, $m_stock, @head);
		print qq| �Q����:|;
		print qq|$participants[$_],| for (0 .. $#participants);
	}
	else { print qq|���ް��W��|; }
	&show_head_info($m_turn, $m_value, $m_stock, @head) if defined(&show_head_info); # ���ׂĂ���ڲ԰�ɕ\�����������1
	if ($head[$_state]) { # �ްт��J�n���Ă���
		&show_started_game($m_turn, $m_value, $m_stock, @head);
	}
	else { # �ްт��J�n���Ă��Ȃ�
		if (&is_member($head[$_participants], "$m{name}")) { # �ްтɎQ�����Ă���
			print qq|<br>|;
			&show_start_info($m_turn, $m_value, $m_stock, @head) if defined(&show_start_info); # ��W���̹ްтɎQ�����Ă�����ڲ԰�ɕ\�����������
			&_start_game_form($m_turn, $m_value, $m_stock, $head[$_participants]); # �J�n�E�Q�����Ȃ�̫��
		}
		else { # �ްтɎQ�����Ă��Ȃ�
			if ($max_entry <= @participants) { print qq|<br>�ްт̊J�n��҂��Ă��܂�|; } # �Q���҂����܂��Ă���
			else { # �Q���҂����܂��Ă��Ȃ�
				if (!$coin_lack && $m{coin} < $head[$_rate]) { print '<br>��݂�ڰĂɑ���Ă��܂���'; } # ��݂�����Ă��Ȃ�
				else { &participate_form(@participants); } # �Q��̫��
			}
		}
	}
	&show_tale_info($m_turn, $m_value, $m_stock, @head) if defined(&show_tale_info); # ���ׂĂ���ڲ԰�ɕ\�����������2
}

#================================================
# �ΐl���ɂɎQ������
#================================================
sub _participate { # �u�Q������v����
	my ($in_rate, $m_value, $m_stock, $is_rate) = @_;

	my @members = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($state, $lastupdate, $participants, $participants_datas, $rate, @datas) = split /<>/, $head_line; # ͯ�ް
	my @participants = split /,/, $participants;
	my $is_find = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($mname eq $m{name}) {
			$is_find = 1;
			if (!$state && @participants < $max_entry) {
				($mtime, $mturn, $mvalue, $mstock) = ($time, 1, $m_value, $m_stock);
				splice(@members, @participants, 0, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n"); # ���ް̧�ُ�ŎQ������\�����邽�߂ɎQ���҂̌��Ɉړ�
			}
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
		}
	}
	unless ($is_find) { # �������Ȃ��Ă����ȂǁA���ް̧�ُォ������Ă����ꍇ
		if (!$state && @participants < $max_entry) {
			splice(@members, @participants, 0, "$time<>$m{name}<>$addr<>1<>$m_value<>$m_stock<>\n");
		}
	}

	my ($is_entry, $is_entry_full, $is_no_coin) = (0, 0, 0);
	my $leader_mes = '';
	if ($max_entry <= @participants) {
		$is_entry_full = 1;
	}
	elsif (&is_member($participants, "$m{name}")) {
		$is_entry = 1;
	}
	elsif (!$is_rate && $m{coin} < $rate) {
		$is_no_coin = 1;
	}
	elsif (!$state && $m{c_turn} == 0) { # ��W�l�����܂��Ă��炸���Q�����J�n�O�őΐl���ɂ�����Ă��Ȃ�
		unless ($participants[0]) { # �Q���҂����Ȃ��Ȃ�e
			$rate = $in_rate;
			$participants .= "$m{name},";
			$leader_mes = " ڰ�:$rate";
			$lastupdate = $time;
		}
		else {
			$participants .= "$m{name},";
			$lastupdate = $time;
		}
		$participants_datas .= "$m{name}:$m_value:$m_stock;";
	}

	my $header = "$state<>$lastupdate<>$participants<>$participants_datas<>$rate<>";
	$header .= "$datas[$_]<>" for (0 .. $header_size - 1);
	unshift @members, "$header\n"; # ͯ�ް
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
	elsif ($is_no_coin) {
		return "��݂�ڰĂɑ���Ă��܂���";
	}
	elsif ($m{c_turn}) {
		return "�ΐl���ɂ���ڲ���ł�";
	}
	else {
		$m{c_turn} = 1;
		&write_user;
		return "$m{name} ���Ȃɒ����܂���$leader_mes";
	}
}

#================================================
# �Q�����̑ΐl���ɂ��痣���
#================================================
sub _observe { # �u�Q�����Ȃ��v����
	my @members = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���');
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head_datas = split /<>/, $head_line;
	my $is_entry = 0;
	my $me = '';
	if (!$head_datas[0] && &is_member($head_datas[2], "$m{name}") && $m{c_turn} < 2) { # �Q���͂��Ă��邪�ްт͊J�n���Ă��Ȃ�
		$is_entry = 1;
#		my $name = unpack 'H*', "$m{name}";
		$head_datas[2] = &remove_member($head_datas[2], $m{name}); # �Q���҂��珜�O
#		$head_datas[2] =~ s/(.*?)$name,(.*)/$1$2/; # �Q���҂��珜�O
		$head_datas[3] = &remove_member_datas($head_datas[3], $m{name}); # �S�Q�����ް����珜�O
#		$head_datas[3] =~ s/(.*?)$name:.*?;(.*)/$1$2/; # �S�Q�����ް����珜�O
	}

	while (my $line = <$fh>) {
		if ($is_entry && $line =~ "\Q$m{name}<>\E") {
			$me = $line;
		}
		else {
			push @members, $line;
		}
	}
	if ($me) {
		my @participants = split /,/, $head_datas[2];
		splice(@members, @participants, 0, $me); # ���ް̧�ُ�ŎQ������\�����Ă���̂ŁA�Ȃ𗣂ꂽ��Q���҂̌��Ɉړ�
	}
	my $is_reset = 0;
	unless ($head_datas[2]) { # ���ް�̍Ō�̈�l���Ȃ𗣂ꂽ��ؾ��
		$is_reset = GAME_RESET;
		$head_datas[$_] = '' for (0 .. $_header_size + $header_size - 1);
	}
	my $header = '';
	$header .= "$head_datas[$_]<>" for (0 .. $_header_size + $header_size - 1);
	unshift @members, "$header<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($head_datas[0]) {
		return "���łɹްт��n�܂��Ă��܂�";
	}
	elsif (!$is_entry) {
		return "�ްтɎQ�����Ă��܂���";
	}
	else {
		$m{c_turn} = 0; # $m{c_value} = $m{c_stock} = '0';
		&write_user;
		my $result_mes = "$m{name} ���Ȃ𗣂�܂���";
		if ($is_reset eq GAME_RESET) {
			&system_comment('�Q���ҕs�݂̂��߹ްт�ؾ�Ă��܂���');
			$result_mes = '';
		}
		return $result_mes;
	}
}

#================================================
# �J�n����E�Q�����Ȃ�̫��
#================================================
sub _start_game_form {
	my ($m_turn, $m_value, $m_stock, $participants) = @_;
	my @participants = &get_members($participants);

	if ($participants[0] eq $m{name} && $min_entry <= @participants && @participants <= $max_entry) { # �Q���҂��K�v�\���Ȃ�J�n���ݕ\��
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("_start_game", "�J�n����");
		print qq|</form>|;
	}
	elsif ($participants[0] ne $m{name} && $min_entry <= @participants && @participants <= $max_entry) {
		print "�e�̹ްъJ�n��҂��Ă��܂�";
	}
	print qq|<form method="$method" action="$this_script" name="form">|;
	print &create_submit("_observe", "�Q�����Ȃ�");
	print qq|</form>|;
}

#================================================
# �J�n�̋��ʏ���
#================================================
sub _start_game {
	my @members = ();
	my @game_members = ();

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;

	# ̧������فAͯ�ް�A�S��ڲ԰�A�S�Q����
	&start_game($fh, \$head_line, \@members, \@game_members);

	unshift @members, $head_line;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

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

#================================================
# �J�n���鏈�� ���ۂ̃t�@�C������� _casino_funcs.cgi _start_game
#================================================
sub reset_members {
	my $ref_members = shift;
	for my $i (0 .. $#$ref_members) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $ref_members->[$i];
		$ref_members->[$i] = "$mtime<>$mname<>$maddr<>0<><><>\n";
	}
}

#================================================
# �J�n�̋��ʏ���
#================================================
=pod
sub _start_game {
	my (@game_members) = @_;
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
=cut
#================================================
# ��݂̐؂�ւ�
#================================================
sub change_turn {
	my $participants = shift;
#	$mes .= "<br>member $participants";
	my $new_members = '';#"$participants[0],"; #$$participants = '';
	if ($participants) {
		my @participants = &get_members($participants);
		for my $i (1 .. $#participants) {
	#		$mes .= "i $i<br>";
			$new_members .= "$participants[$i],";# for (0 .. $#participants);
		}
		$new_members .= "$participants[0],";
	}
#	push @participants, splice(@participants, 0, 1);
#	my $new_members = ''; #$$participants = '';
#	$new_members .= "$participants[$_]," for (0 .. $#participants);
	return $new_members;
#	$$participants .= "$participants[$_]," for (0 .. $#participants);
#	$$participants =~ s/^(.*?),(.*)/$2$1,/; # ���쒆����ڲ԰���Ō���Ɉړ�
}

#================================================
# ��݂̑���
#================================================
sub coin_move{
	my ($m_coin, $name, $no_system_comment) = @_;
	return if $m_coin == 0 || $m_coin eq '';
	my $ret_v;
	
	my $player_id = unpack 'H*', $name;

	# ���݂��Ȃ��ꍇ�̓X�L�b�v
	unless (-f "$userdir/$player_id/user.cgi") {
		return $ret_v;
	}
	if($name eq $m{name}){
		if ($m{coin} + $m_coin < 0){
			$ret_v = -1 * $m{coin};
		}else {
			$ret_v = $m_coin;
		}
		
		$m{coin} += $ret_v;
		&write_user;
	}else{
		my %datas1 = &get_you_datas($name);
		my $temp = $datas1{coin} + $m_coin;

		if ($temp < 0){
			$temp = 0;
			$ret_v = -1 * $datas1{coin};
		} else {
			if ($temp > 2500000) {
				$temp = 2500000;
			}
			$ret_v = $m_coin;
		}
		&regist_you_data($name,'coin',$temp);
	}

	unless ($no_system_comment) {
		if($ret_v > 0){
			&system_comment("$name �� $ret_v ��ݓ��܂���");
		}else{
			my $temp = -1 * $ret_v;
			&system_comment("$name �� $temp ��ݕ����܂���");
		}
	}
	
	if ($m_coin < $ret_v) {
		my $diff = ($ret_v - $m_coin) * 10;
			
		my $shop_id = unpack 'H*', $name;
		my $this_pool_file = "$userdir/$shop_id/casino_pool.cgi";
		my @lines = ();
		if (-f $this_pool_file) {
			open my $fh, "+< $this_pool_file" or &error("$this_pool_file���J���܂���");
			eval { flock $fh, 2; };
			
			while (my $line = <$fh>){
				my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
				$pool -= $diff;
				push @lines, "$pool<>$this_term_gain<>$slot_runs<>\n";
				last;
			}
			
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
	}
	
	return $ret_v;
}

sub bonus {
	my $name = shift;
	my $mes_as = shift;
	my $mes_news = shift;
	
	my $player_id = unpack 'H*', $name;

	# ���݂��Ȃ��ꍇ�̓X�L�b�v
	unless (-f "$userdir/$player_id/user.cgi") {
		return;
	}
	
	require "$datadir/casino_bonus.cgi";
	my $prize;
	my $item_no = int(rand($#bonus+1));
	&send_item($name,$bonus[$item_no][0],$bonus[$item_no][1],$bonus[$item_no][2],$bonus[$item_no][3], 1);
	if($bonus[$item_no][0] == 1){
		$prize .= "$weas[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 2){
		$prize .= "$eggs[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 3){
		$prize .= "$pets[$bonus[$item_no][1]][1]";
	}
	if ($mes_as ne '') {
		&system_comment("$name �� $mes_as �Ƃ��� $prize ���l�����܂���");
	}
	if ($mes_news ne '') {
		&write_send_news(qq|<font color="#FF0000">$name �� $mes_news</font>|);
	}
}

sub system_comment{
	my $s_mes = shift;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };

	# ����ݸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, "$time<>$date<>�V�X�e�����b�Z�[�W<>0<><>$addr<>$s_mes<>$default_icon<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#================================================
# �ΐl���Ɋ֌W�̕ϐ���������
#================================================
sub you_c_reset {
	my $name = shift;
	if ($name eq $m{name}) {
		$m{c_turn} = 0;
		$m{c_value} = 0;
		$m{c_stock} = 0;
		&write_user;
	}else {
		&regist_you_data($name,'c_turn',0);
		&regist_you_data($name,'c_value',0);
		&regist_you_data($name,'c_stock',0);
	}
}

#================================================
# �ΐl���Ɋ֌W�̕ϐ���������(����հ�ް)
#================================================
sub you_lot_c_reset {
	my @names = @_;

	my @data = (
		['c_turn', 0],
		['c_value', 0],
		['c_stock', 0],
	);

	for $name (@names) {
		if ($name eq $m{name}) {
			$m{c_turn} = $m{c_value} = $m{c_stock} = 0;
			&write_user;
		}
		else {
			&regist_you_array($datas{name}, @data);
		}
	}
}

#================================================
# �T�u�~�b�g�{�^�� form�^�O�̊Ԃɋ���
#================================================
sub create_submit {
	my ($mode, $value) = @_;
	my $result_str = '';
	$result_str .= qq|<input type="hidden" name="mode" value="$mode">|;
	$result_str .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$result_str .= qq|<input type="hidden" name="guid" value="ON">|;
	$result_str .= qq|<input type="submit" value="$value" class="button_s">|;
	return $result_str;
}

#================================================
# �Z���N�g���j���[ form�^�O�̊Ԃɋ���
#================================================
sub create_select_menu {
	my ($name, @menus) = @_;
	my $result_str = '';
	$result_str .= qq|<select name="$name" class="menu1">|;
	for my $i (0 .. $#menus) {
		$result_str .= qq|<option value="$i">$menus[$i]</option>| if $menus[$i] <= $m{coin};
	}
	$result_str .= qq|</select>|;
	return $result_str;
}

#================================================
# ���W�I�{�^�� form�^�O�̊Ԃɋ���
#================================================
sub create_radio_button {
	my ($name, $value, $str) = @_;
	my $result_str = '';
	$result_str .= qq|<label>| unless $is_moble;
	$result_str .= qq|<input type="radio" name="$name" value="$value">$str|;
	$result_str .= qq|</label>| unless $is_moble;
	return $result_str;
}

#================================================
# �`�F�b�N�{�b�N�X form�^�O�̊Ԃɋ���
#================================================
sub create_check_box {
	my ($name, $value, $str) = @_;
	my $result_str = '';
	$result_str .= qq|<label>| unless $is_moble;
	$result_str .= qq|<input type="checkbox" name="$name" value="$value">$str|;
	$result_str .= qq|</label>| unless $is_moble;
	return $result_str;
}

sub get_members {
	my @members = split /,/, shift; # ���ް�ͺ�ϋ�؂�
	return @members;
}
sub remove_member {
	my ($game_members, $remove_name) = @_;
	my @game_members = &get_members($game_members);
	my $new_game_members = '';
	for my $i (0 .. $#game_members) {
		$new_game_members .= "$game_members[$i]," if $game_members[$i] ne $remove_name
	}
	return $new_game_members;
}

sub is_member {
	my ($game_members, $find_name) = @_;
	my @game_members = &get_members($game_members);
#	my $is_find = 0;
	for my $i (0 .. $#game_members) {
		return 1 if $game_members[$i] eq $find_name;
#		if ($find_name eq $game_member) {
#			$is_find = 1;
#			last;
#		}
	}
	return 0;
}

sub is_my_turn {
	my ($game_members, $find_name) = @_;
	my @game_members = &get_members($game_members);
	return $find_name eq $game_members[0];

#	my ($target_str, $find_str) = @_;
#	$find_str = unpack 'H*', $find_str;
#	return $target_str =~ "^$find_str,";
}

sub get_member_datas {
	my @member_datas = split /;/, shift;
#	$members[$_] = pack 'H*', $members[$_] for (0 .. $#members);
	return @member_datas;
}

sub remove_member_datas {
	my ($game_member_datas, $remove_name) = @_;
	my @game_member_datas = &get_member_datas($game_member_datas);
	my $new_game_member_datas = '';
	for my $i (0 .. $#game_member_datas) {
		my @game_member_data = split /:/, $game_member_datas[$i];
		$new_game_member_datas .= "$game_member_datas[$i];" if $game_member_data[0] ne $remove_name;
	}
	return $new_game_member_datas;
}

sub update_member_datas {
	my ($game_member_datas, $name, $value, $stock) = @_;
	my @game_member_datas = &get_member_datas($game_member_datas);
	my $new_game_member_datas = '';
	for my $i (0 .. $#game_member_datas) {
		my @game_member_data = split /:/, $game_member_datas[$i];
		if ($game_member_data[0] eq $name) {
			$game_member_datas[$i] = "$name:$value:$stock";
		}
		$new_game_member_datas .= "$game_member_datas[$i];";
	}
	return $new_game_member_datas;
}

sub esc4re {
	my $str = shift;
	$str =~ s/([\x21\x24-\x26\x28-\x2b\x2e\x2f\x3f\x40\x5b-\x5e\x7b-\x7d])/\\$1/g if $str;
	return $str;
}

sub is_match {
	my ($target_str, $find_str) = @_;

	$target_str = &esc4re($target_str);
	$find_str = &esc4re($find_str);
	return $target_str =~ $find_str;
}

1;#�폜�s��
