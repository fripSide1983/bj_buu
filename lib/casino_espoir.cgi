#================================================
# ���肶��񂯂�
#================================================
require './lib/_comment_tag.cgi';
require './lib/_casino_funcs.cgi';

# �Q���҈ꗗ
my $all_member_file = "$logdir/espoir_member.cgi";

# ���[�U�[�f�[�^
my $my_espoir_file = "$userdir/$id/espoir.cgi";

# ��z
my $rate = 10;

my $overflow = 2500000;
my $bonus_coin = 2500000;

# �o�`�ɕK�v�ȍŒ�v���C���[��
my $min_espoir = 3;

unless (-f $all_member_file) {
	open my $fh, "> $all_member_file" or &error('�q��̧�ق̏������݂Ɏ��s���܂���');
	print $fh "<>0<>0<>0<>\n";
	close $fh;
}

sub run {
	if ($in{mode} eq "participate") {
		$in{comment} = &participate;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "send_star") {
		&send_star($in{to});
	}
	elsif ($in{mode} eq "send_a") {
		&send_a($in{to});
	}
	elsif ($in{mode} eq "send_b") {
		&send_b($in{to});
	}
	elsif ($in{mode} eq "send_c") {
		&send_c($in{to});
	}
	elsif ($in{mode} eq "receive") {
		&receive($in{type});
	}
	elsif ($in{mode} eq "refuse") {
		&refuse($in{type});
	}
	elsif ($in{mode} eq "check_a") {
		$in{comment} = &check_a($in{to});
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "check_b") {
		$in{comment} = &check_b($in{to});
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "check_c") {
		$in{comment} = &check_c($in{to});
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "recheck") {
		&recheck($in{hand});
	}
	elsif ($in{mode} eq "uncheck") {
		$in{comment} = &uncheck;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "goal") {
		&goal;
	}
	elsif($in{mode} eq "write" &&$in{comment}){
		&write_comment;
	}
	my ($member_c, $member) = &get_member;

	my ($game_year, $all_rest_a, $all_rest_b, $all_rest_c, $participate, @all_member) = &get_state;
	
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;
	
	if ($game_year eq $w{year}) {
		print qq|�S�̎c�� �O�[:$all_rest_a �`���L:$all_rest_b �p�[:$all_rest_c<br>|;
		if ($participate) {
			my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
			print qq|�� $star �c�� �O�[:$rest_a �`���L:$rest_b �p�[:$rest_c|;
			my $no_stack = 1;
			if (@{$stack{star}}) {
				my $yname = ${stack{star}}[0];
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="1">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="$yname����̐����󂯎��" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="1">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="$yname����̐����󂯎��Ȃ�" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{a}}) {
				my $yname = ${stack{a}}[0];
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="2">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="$yname����̃O�[���󂯎��" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="2">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="$yname����̃O�[���󂯎��Ȃ�" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{b}}) {
				my $yname = ${stack{b}}[0];
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="3">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="$yname����̃`���L���󂯎��" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="3">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="$yname����̃`���L���󂯎��Ȃ�" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{c}}) {
				my $yname = ${stack{c}}[0];
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="4">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="$yname����̃p�[���󂯎��" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="4">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="$yname����̃p�[���󂯎��Ȃ�" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{check}}) {
				my $yname = ${stack{check}}[0];
				if ($rest_a + $rest_b + $rest_c > 0) {
					print qq|<form method="$method" action="$this_script" name="form">|;
					print qq|<input type="hidden" name="mode" value="recheck">|;
					print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
					for my $i (1..3) {
						if (($i == 1 && $rest_a <= 0) || ($i == 2 && $rest_b <= 0) || ($i == 3 && $rest_c <= 0)) {
							next;
						}
						
						print qq|<input type="radio" name="hand" value="$i">|;
						print $i == 1 ? '�O�[' :
								$i == 2 ? '�`���L' :
										'�p�[';
					}
					print qq|<input type="submit" value="$yname�Ə���" class="button_s"><br>|;
					print qq|</form>|;
				}
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="uncheck">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="$yname�Ə������Ȃ�" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{send}}) {
				$no_stack = 0;
			}
			if ($no_stack) {
				if ($rest_a + $rest_b + $rest_c > 0) {
					print qq|<form method="$method" action="$this_script" name="form">|;
					print qq|<select name="mode">|;
					if ($rest_a > 0) {
						print qq|<option value="check_a">�O�[�ŏ���</option>|;
					}
					if ($rest_b > 0) {
						print qq|<option value="check_b">�`���L�ŏ���</option>|;
					}
					if ($rest_c > 0) {
						print qq|<option value="check_c">�p�[�ŏ���</option>|;
					}
					if ($rest_a > 0) {
						print qq|<option value="send_a">�O�[��n��</option>|;
					}
					if ($rest_b > 0) {
						print qq|<option value="send_b">�`���L��n��</option>|;
					}
					if ($rest_c > 0) {
						print qq|<option value="send_c">�p�[��n��</option>|;
					}
					if ($star > 1) {
						print qq|<option value="send_star">����n��</option>|;
					}
					print qq|</select>|;
					print qq|����F|;
					&print_player_select('to');
					print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
					print qq|<input type="submit" value="���M" class="button_s"><br>|;
					print qq|</form>|;
				} else {
					if (($count > 1 && $star >= 4) ||$star >= 3) {
						print qq|<form method="$method" action="$this_script" name="form">|;
						print qq|<input type="hidden" name="mode" value="goal">|;
						print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
						print qq|<input type="submit" value="������" class="button_s"><br>|;
						print qq|</form>|;
					}
				}
			}
		}
	} else {
		print qq|��D�ҕ�W��|;
		if ($participate) {
			print qq|���Ȃ��͏�D�\\��ł��B|;
		} else {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="participate">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="��D" class="button_s"><br>|;
			print qq|</form>|;
		}
	}
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="����" class="button_s"><br>|;
	print qq|</form>|;

	print qq|<div id="body_mes"><font size="2">$member_c�l:$member</font><br>|;
	
	print qq|<hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$bcomment = &comment_change($bcomment, 1);
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
	print qq|</div>|;
	print qq|</td>|;
	print qq|</tr></table>|;
}

sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # �����l�Ȃ玟
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, $line;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members;

	return ($member_c, $member);
}

sub get_state {
	my @all_players = ();
	my $participate = 0;
	my $star;
	my $my_rest_a = 0;
	my $my_rest_b = 0;
	my $my_rest_c = 0;
	
	open my $fh, "< $all_member_file" or &error('�Q����̧�ق��J���܂���'); 
	my $headline = <$fh>;
	my($play_year, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
	while (my $line = <$fh>) {
		chomp $line;
		if ($line) {
			push @all_players, $line;
			if ($line eq $m{name}) {
				$participate = 1;
			}
		}
	}
	close $fh;
	
	return ($play_year, $rest_a, $rest_b, $rest_c, $participate, @all_players);
}

sub get_my_state {
	my %stack = ();
	my @star = ();
	my @a = ();
	my @b = ();
	my @c = ();
	my @check = ();
	my @send = ();
	open my $fhm, "< $my_espoir_file" or &error('�Q����̧�ق��J���܂���'); 
	my $headline = <$fhm>;
	my ($star, $rest_a, $rest_b, $rest_c, $count, $year, $check_h) = split /<>/, $headline;
	while (my $line = <$fhm>) {
		my ($type, $name) = split /<>/, $line;
		if ($type eq '1') {
			push @star, $name;
		} elsif ($type eq '2') {
			push @a, $name;
		} elsif ($type eq '3') {
			push @b, $name;
		} elsif ($type eq '4') {
			push @c, $name;
		} elsif ($type eq '5') {
			push @check, $name;
		} else {
			push @send, $name;
		}
	}
	close $fhm;
	
	$stack{star} = \@star;
	$stack{a} = \@a;
	$stack{b} = \@b;
	$stack{c} = \@c;
	$stack{check} = \@check;
	$stack{send} = \@send;
	
	return ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack);
}

sub participate {
	open my $fh, "< $all_member_file" or &error('�Q����̧�ق��J���܂���'); 
	my $headline = <$fh>;
	my($play_year, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
	my @all_players = ();
	my $find = 0;
	while (my $line = <$fh>) {
		chomp $line;
		if ($line) {
			push @all_players, $line;
			if ($line eq $m{name}) {
				$find = 1;
			}
		}
	}
	close $fh;
	
	if (!$find && $m{coin} >= $rate) {
		&coin_move(-1 * $rate, $m{name}, 1);
		
		push @all_players, $m{name};
		
		if (@all_players >= $min_espoir) {
			if ($play_year != $w{year} + 1) {
				$play_year = $w{year} + 1;
				&system_comment("$play_year�ɃG�X�|���[��<��]>�͏o�`�������܂��B");
			}
			for my $en (@all_players) {
				my $en_id = unpack 'H*', $en;
				&change_my_status($en_id, 'year', $play_year);
			}
		}
		my $player_num = @all_players;
		my $cards = $player_num * 3;
		$headline = "$play_year<>$cards<>$cards<>$cards<>\n";
		
		unshift @all_players, $headline;
		
		open my $wfh, "> $all_member_file" or &error('�Q����̧�ق��J���܂���'); 
		for my $line (@all_players) {
			print $wfh "$line\n";
		}
		close $wfh;
		&change_my_status($id, 'star', 3);
		&change_my_status($id, 'a', 3);
		&change_my_status($id, 'b', 3);
		&change_my_status($id, 'c', 3);
		&change_my_status($id, 'count_add', 1);
		&change_my_status($id, 'set', '');
		&clear_stack($id);
		return "$m{name}����D���܂����B";
	}
	return "";
}

sub send_star {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_star', -1);
	&add_my_status_line($id, -1, $to);
	&add_my_status_line($to_id, 1, $m{name});
}

sub send_a {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_a', -1);
	&add_my_status_line($id, -2, $to);
	&add_my_status_line($to_id, 2, $m{name});
}

sub send_b {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_b', -1);
	&add_my_status_line($id, -3, $to);
	&add_my_status_line($to_id, 3, $m{name});
}

sub send_c {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_c', -1);
	&add_my_status_line($id, -4, $to);
	&add_my_status_line($to_id, 4, $m{name});
}

sub receive {
	my $type = shift;
	my ($find, $name) = &remove_my_status_line($id, $type, '');
	if ($find) {
		my $from_id = unpack 'H*', $name;
		&remove_my_status_line($from_id, -1 * $type, $m{name});
		my $sta = $type == 1 ? 'star_add' :
					$type == 2 ? 'a_add' :
					$type == 3 ? 'b_add' :
					$type == 4 ? 'c_add' :
								'';
		&change_my_status($id, $sta, 1);
	}
}

sub refuse {
	my $type = shift;
	my ($find, $name) = &remove_my_status_line($id, $type, '');
	if ($find) {
		my $from_id = unpack 'H*', $name;
		&remove_my_status_line($from_id, -1 * $type, $m{name});
		my $sta = $type == 1 ? 'star_add' :
					$type == 2 ? 'a_add' :
					$type == 3 ? 'b_add' :
					$type == 4 ? 'c_add' :
								'';
		&change_my_status($from_id, $sta, 1);
	}
}

sub check_a {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
	if ($rest_a > 0 && !$check_h) {
		&change_my_status($id, 'set', 1);
		&add_my_status_line($id, -5, $to);
		&add_my_status_line($to_id, 5, $m{name});
		&change_my_status($id, 'add_a', -1);
	}
	return '�`�F�b�N';
}

sub check_b {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
	if ($rest_b > 0 && !$check_h) {
		&change_my_status($id, 'set', 2);
		&add_my_status_line($id, -5, $to);
		&add_my_status_line($to_id, 5, $m{name});
		&change_my_status($id, 'add_b', -1);
	}
	return '�`�F�b�N';
}

sub check_c {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
	if ($rest_c > 0 && !$check_h) {
		&change_my_status($id, 'set', 3);
		&add_my_status_line($id, -5, $to);
		&add_my_status_line($to_id, 5, $m{name});
		&change_my_status($id, 'add_c', -1);
	}
	return '�`�F�b�N';
}

sub recheck {
	my $hand = shift;
	my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
	if (($hand == 1 && $rest_a <= 0) || ($hand == 2 && $rest_b <= 0) || ($hand == 3 && $rest_c <= 0)) {
		return;
	}
	
	my $type = 5;
	my ($find, $name) = &remove_my_status_line($id, $type, '');
	if ($find) {
		my $from_id = unpack 'H*', $name;
		&remove_my_status_line($from_id, -1 * $type, $m{name});
		my $y_hand = &change_my_status($from_id, 'set', '');
		&system_comment('�Z�b�g');
		my $win = 0;
		my $omes = "�I�[�v��<br>$m{name}:";
		if ($hand == 1) {
			&change_my_status($id, 'add_a', -1);
			$omes .= '�O�[ vs ';
			if ($y_hand == 1) {
				$omes .= "$name:�O�[<br>������";
			} elsif ($y_hand == 2) {
				$omes .= "$name:�`���L<br>$m{name}����";
				$win = 1;
			} else {
				$omes .= "$name:�p�[<br>$name����";
				$win = -1;
			}
		} elsif ($hand == 2) {
			&change_my_status($id, 'add_b', -1);
			$omes .= '�`���L vs ';
			if ($y_hand == 1) {
				$omes .= "$name:�O�[<br>$name����";
				$win = -1;
			} elsif ($y_hand == 2) {
				$omes .= "$name:�`���L<br>������";
			} else {
				$omes .= "$name:�p�[<br>$m{name}����";
				$win = 1;
			}
		} else {
			&change_my_status($id, 'add_c', -1);
			$omes .= '�p�[ vs ';
			if ($y_hand == 1) {
				$omes .= "$name:�O�[<br>$m{name}����";
				$win = 1;
			} elsif ($y_hand == 2) {
				$omes .= "$name:�`���L<br>$name����";
				$win = -1;
			} else {
				$omes .= "$name:�p�[<br>������";
			}
		}
		&decrease_all($hand);
		&decrease_all($y_hand);
		&system_comment($omes);
		if ($win != 0) {
			&change_my_status($id, 'add_star', $win);
			&change_my_status($from_id, 'add_star', -1 * $win);
		}
	}
}

sub uncheck {
	my ($find, $name) = &remove_my_status_line($id, 5, '');
	if ($find) {
		my $from_id = unpack 'H*', $name;
		&remove_my_status_line($from_id, -5, $m{name});
		my $y_hand = &change_my_status($from_id, 'set', '');
		my $sta = $y_hand == 1 ? 'a_add' :
					$y_hand == 2 ? 'b_add' :
					$y_hand == 3 ? 'c_add' :
								'';
		&change_my_status($from_id, $sta, 1);
	}
	return '�����ۂ���D';
}

sub goal {
	my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
	my $need_star = 3;
	if ($count> 1) {
		$need_star = 4;
	}
	
	if (@{$stack{star}}) {
		return '�����󂯎�邩���ۂ��Ă��������B';
	}
	if (@{$stack{a}}) {
		return '�O�[���󂯎�邩���ۂ��Ă��������B';
	}
	if (@{$stack{b}}) {
		return '�`���L���󂯎�邩���ۂ��Ă��������B';
	}
	if (@{$stack{c}}) {
		return '�p�[���󂯎�邩���ۂ��Ă��������B';
	}
	if (@{$stack{check}}) {
		return '�������󂯎�邩���ۂ��Ă��������B';
	}
	if (@{$stack{send}}) {
		return '���������肪�󂯎���Ă��Ȃ������ۂ��Ă��܂���B';
	}
	
	if ($rest_a <= 0 && $rest_b <= 0 && $rest_c <= 0 && $star >= $need_star && !$check_h) {
		my $else_star = $star - $need_star;
		my $recv = $rate * (3 + $else_star);
		while ($recv > $overflow) {
			$recv -= $bonus_coin;
			&bonus($m{name}, '', '');
		}
		&end_player($m{name});
		return '';
	}
	return '�I�������𖞂����Ă��܂���B';
}

sub lose {
	my $name = shift;
	&end_player($name);
}

sub end_player {
	my $name = shift;

	open my $fh, "< $all_member_file" or &error('�Q����̧�ق��J���܂���'); 
	while (my $line = <$fh>) {
		chomp $line;
		if ($line) {
			if ($line ne $name) {
				push @all_players, $line;
			}
		}
	}
	close $fh;
	
	open my $wfh, "> $all_member_file" or &error('�Q����̧�ق��J���܂���'); 
	for my $line (@all_players) {
		print $wfh "$line\n";
	}
	close $wfh;
}

sub add_my_status_line {
	my $to_id = shift;
	my $type = shift;
	my $name = shift;
	
	unless (-f "$userdir/$to_id/espoir.cgi") {
		open my $fh, "> $userdir/$to_id/espoir.cgi" or &error('�q��̧�ق̏������݂Ɏ��s���܂���');
		print $fh "<>0<>0<>0<>0<><><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$to_id/espoir.cgi" or &error('�Q����̧�ق��J���܂���'); 
	my $headline = <$fhm>;
	push @lines, $headline;
	while (my $line = <$fhm>) {
		push @lines, $line;
	}
	close $fhm;
	
	push @lines, "$type<>$name<>\n";
	
	open my $fhw, "> $userdir/$to_id/espoir.cgi" or &error('�Q����̧�ق��J���܂���'); 
	print $fhw @lines;
	close $fhw;
}

sub remove_my_status_line {
	my $to_id = shift;
	my $type = shift;
	my $rm_name = shift;
	
	unless (-f "$userdir/$to_id/espoir.cgi") {
		open my $fh, "> $userdir/$to_id/espoir.cgi" or &error('�q��̧�ق̏������݂Ɏ��s���܂���');
		print $fh "<>0<>0<>0<>0<><><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$to_id/espoir.cgi" or &error('�Q����̧�ق��J���܂���'); 
	my $headline = <$fhm>;
	push @lines, $headline;
	
	my $find = 0;
	while (my $line = <$fhm>) {
		my ($t, $n) = split /<>/, $line;
		if (!$find && $t eq $type && (!$rm_name || $n eq $rm_name)) {
			$find = 1;
			$rm_name = $n;
		} else {
			push @lines, $line;
		}
	}
	close $fhm;
	
	open my $fhw, "> $userdir/$to_id/espoir.cgi" or &error('�Q����̧�ق��J���܂���'); 
	print $fhw @lines;
	close $fhw;
	
	return ($find, $rm_name);
}

sub change_my_status {
	my $change_id = shift;
	my $key = shift;
	my $value = shift;
	my $ret = '';
	
	unless (-f "$userdir/$change_id/espoir.cgi") {
		open my $fh, "> $userdir/$change_id/espoir.cgi" or &error('�q��̧�ق̏������݂Ɏ��s���܂���');
		print $fh "<>0<>0<>0<>0<><><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$change_id/espoir.cgi" or &error('�Q����̧�ق��J���܂���'); 
	my $headline = <$fhm>;
	my($star, $rest_a, $rest_b, $rest_c, $count, $year, $check_h) = split /<>/, $headline;
	if ($key eq 'star') {
		$star = $value;
	} elsif ($key eq 'star_add') {
		$star += $value;
	} elsif ($key eq 'a') {
		$rest_a = $value;
	} elsif ($key eq 'a_add') {
		$rest_a += $value;
	} elsif ($key eq 'b') {
		$rest_b = $value;
	} elsif ($key eq 'b_add') {
		$rest_b += $value;
	} elsif ($key eq 'c') {
		$rest_c = $value;
	} elsif ($key eq 'c_add') {
		$rest_c += $value;
	} elsif ($key eq 'count_add') {
		$count += $value;
	} elsif ($key eq 'year') {
		$year = $value;
	} elsif ($key eq 'set') {
		$ret = $check_h;
		$check_h = $value;
	}
	push @lines, "$star<>$rest_a<>$rest_b<>$rest_c<>$count<>$year<>$check_h<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	close $fhm;
	
	open my $fhw, "> $userdir/$change_id/espoir.cgi" or &error('�Q����̧�ق��J���܂���'); 
	print $fhw @lines;
	close $fhw;
	
	return $ret;
}
sub clear_stack {
	my $clear_id = shift;
	
	unless (-f "$userdir/$clear_id/espoir.cgi") {
		open my $fh, "> $userdir/$clear_id/espoir.cgi" or &error('�q��̧�ق̏������݂Ɏ��s���܂���');
		print $fh "<>0<>0<>0<>0<><><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$clear_id/espoir.cgi" or &error('�Q����̧�ق��J���܂���'); 
	my $headline = <$fhm>;
	push @lines, $headline;
	close $fhm;
	
	open my $fhw, "> $userdir/$clear_id/espoir.cgi" or &error('�Q����̧�ق��J���܂���'); 
	print $fhw @lines;
	close $fhw;
}

sub decrease_all {
	my $hand = shift;
	
	my @all_players = ();
	
	open my $fh, "< $all_member_file" or &error('�Q����̧�ق��J���܂���'); 
	my $headline = <$fh>;
	my($play_year, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
	while (my $line = <$fh>) {
		push @all_players, $line;
	}
	close $fh;
	if ($hand == 1) {
		$rest_a--;
	} elsif ($hand == 2) {
		$rest_b--;
	} elsif ($hand == 3) {
		$rest_c--;
	}
	unshift @all_players, "$play_year<>$rest_a<>$rest_b<>$rest_c<>\n";

	open my $fhw, "> $all_member_file" or &error('�Q����̧�ق��J���܂���'); 
	print $fhw @all_players;
	close $fhw;
}

sub print_player_select {
	my $name = shift;

	my @all_players = ();
	open my $fh, "< $all_member_file" or &error('�Q����̧�ق��J���܂���'); 
	my $headline = <$fh>;
	my($play_year, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
	while (my $line = <$fh>) {
		push @all_players, $line;
	}
	close $fh;

	print qq|<select name="$name">|;
	for my $pl (@all_players) {
		chomp $pl;
		if ($pl) {
			print qq|<option value="$pl">$pl</option>|;
		}
	}
	print qq|</select>|;
}

sub item_or_coin {
	my ($m_coin, $name) = @_;
	
	while ($m_coin > 2500000) {
		$m_coin -= 1000000;
		&bonus($name, '', '�Ă̌i�i��Ⴂ�܂���');
	}
	&coin_move($m_coin, $name, 1);
}

1;