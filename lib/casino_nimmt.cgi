#================================================
# 6 Nimmt
#================================================
@rates = (100, 1000, 3000, 10000, 30000);
require './lib/_casino_funcs.cgi';
my $game_file = "${this_file}_data.cgi";

sub run {
	if ($in{mode} eq "play") {
		&play_card($in{card});
	}
	elsif ($in{mode} eq "get_line") {
		$in{comment} = &get_line($in{line});
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "participate") {
		$in{comment} = &participate;
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
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member) = &get_member;
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	if(!(&is_playing) && &is_player) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="exit">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="��߂�" class="button_s"></form><br>|;
	} else {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="�߂�" class="button1"></form>|;
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
	print qq|���[�g:$rate<br>|;
	for my $p (@players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		print qq|$pname|;
		if ($selected < 0) {
			print qq|��I��|;
		} elsif ($selected == 0) {
			print qq|�J�[�h�I��|;
		} else {
			print qq|�J�[�h�I���ς�|;
		}
		print qq|<br>|;
	}
	if(&is_playing){
		&print_lines;
		print qq|<br>|;
		if (&is_player) {
			&print_my_hand;
			&print_gotten;
		}
		if (&is_put_minimum) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="get_line">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<select name="line" class="menu1">|;
			for my $i(1..4){
				print qq|<option value="$i">$i</option>|;
			}
			print qq|</select>��ڂ��Ƃ�|;
			print qq|<input type="submit" value="�I��" class="button_s"></form><br>|;
		}
	}else {
		if (&is_player) {
			if (@players >= 2) {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="start">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="�J�n����" class="button_s"></form><br>|;
			}
		} else {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="participate">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			if (@players <= 0) {
				print qq|���[�g<select name="rate" class="menu1">|;
				for my $i(0..$#rates){
					print qq|<option value="$i">$rates[$i]</option>|;
				}
				print qq|</select>|;
			}
			print qq|<input type="submit" value="�Ȃɒ���" class="button_s"></form><br>|;
		}
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

sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			if($mturn > 0){
				$leave_name = $mname if $state ne 'waiting';
				&regist_you_data($mname,'c_turn',0);
				&regist_you_data($mname,'c_value',0);
				&regist_you_data($mname,'c_stock',0);
			}else {
				next;
			}
		}
		next if $sames{$mname}++; # �����l�Ȃ玟
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>\n";
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
	
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	for my $p (@players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		my $pfind = 0;
		for my $mm (@members) {
			my($mtime, $mname, $maddr) = split /<>/, $mm;
			if ($pname eq $mname) {
				$pfind = 1;
				last;
			}
		}
		unless ($pfind) {
			if ($selected == 0) {
				&auto_play($pname);
			} elsif ($selected < 0) {
				&auto_get_line($pname);
			}
		}
	}
	
	my $member_c = @members;
	return ($member_c, $member);
}

sub play_card {
	my $card = shift;
	
	if (&is_playing && &is_player) {
		my($pname, $selected, $rest, $nimmt) = &get_my_state;
		if ($selected == 0) {
			my @rests = split /,/, $rest;
			my @new_rests = ();
			for my $c (@rests) {
				if ($c == $card) {
					$selected = $c;
				} else {
					push @new_rests, $c;
				}
			}
			$rest = join ',', @new_rests;
			&set_player_state($pname, $selected, $rest, $nimmt);
		}
		&round_check;
	}
}

sub auto_play {
	my $name = shift;
	
	if (&is_playing && &is_player($name)) {
		my($pname, $selected, $rest, $nimmt) = &get_my_state($name);
		if ($selected == 0) {
			my @rests = split /,/, $rest;
			my @new_rests = ();
			for my $c (@rests) {
				if ($selected) {
					push @new_rests, $c;
				} else {
					$selected = $c;
				}
			}
			$rest = join ',', @new_rests;
			&set_player_state($pname, $selected, $rest, $nimmt);
		}
		&round_check;
	}
}

sub round_check {
	my @play_cards = ();
	
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	for my $p (@players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		if ($selected <= 0) {
			return;
		}
	}
	my @sorted_players = map { $_->[0] } sort { $a->[2] <=> $b->[2] } map { [$_, split /<>/ ] } @players;
	for my $p (@sorted_players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		&put_card($pname, $selected);
		$selected = 0;
		&set_player_state($pname, $selected, $rest, $nimmt);
	}
	&exec_culc;
}

sub put_card {
	my($pname, $selected) = @_;
	&system_comment("$pname��$selected���o���܂���");
	
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	my @suspends = split /,/, $suspend;
	push @suspends, "$pname:$selected";
	$suspend = join ',', @suspends;
	
	&set_state($rate, $line1, $line2, $line3, $line4, $suspend);
}

sub exec_culc {
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	my @lines = ($line1, $line2, $line3, $line4);
	my @suspends = split /,/, $suspend;
	while (@suspends) {
		my $s = shift @suspends;
		my($sname, $scard) = split /:/, $s;
		my $put_index = -1;
		my $min_head = 0;
		for my $li (0..3) {
			my @la = split /,/, $lines[$li];
			my $lhead = pop @la;
			if ($lhead < $scard && $min_head < $lhead) {
				$min_head = $lhead;
				$put_index = $li;
			}
		}
		if ($put_index >= 0) {
			my @la = split /,/, $lines[$put_index];
			if (@la >= 5) {
				while (@la) {
					my $get_card = shift @la;
					&add_nimmt($sname, $get_card);
				}
			}
			push @la, $scard;
			$lines[$put_index] = join ',', @la;
		} else {
			my($pname, $selected, $rest, $nimmt) = &get_my_state($sname);
			$selected = -1;
			&set_player_state($pname, $selected, $rest, $nimmt);
			
			unshift @suspends, $s;
			last;
		}
	}
	
	$suspend = join ',', @suspends;
	$line1 = $lines[0];
	$line2 = $lines[1];
	$line3 = $lines[2];
	$line4 = $lines[3];
	&set_state($rate, $line1, $line2, $line3, $line4, $suspend);
	
	unless ($suspend) {
		my $is_end = 1;
		for my $p (@players) {
			my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
			if ($selected || $rest) {
				$is_end = 0;
			}
		}
		if ($is_end) {
			&end_game;
		}
	}
}

sub get_line {
	my $line_no = shift;
	
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	my @suspends = split /,/, $suspend;
	my $s = shift @suspends;
	my($sname, $scard) = split /:/, $s;
	if ($sname ne $m{name}) {
		return;
	}
	if ($line_no == 1) {
		my @la = split /,/, $line1;
		while (@la) {
			my $get_card = shift @la;
			&add_nimmt($sname, $get_card);
		}
		$line1 = $scard;
	} elsif ($line_no == 2) {
		my @la = split /,/, $line2;
		while (@la) {
			my $get_card = shift @la;
			&add_nimmt($sname, $get_card);
		}
		$line2 = $scard;
	} elsif ($line_no == 3) {
		my @la = split /,/, $line3;
		while (@la) {
			my $get_card = shift @la;
			&add_nimmt($sname, $get_card);
		}
		$line3 = $scard;
	} elsif ($line_no == 4) {
		my @la = split /,/, $line4;
		while (@la) {
			my $get_card = shift @la;
			&add_nimmt($sname, $get_card);
		}
		$line4 = $scard;
	} else {
		return;
	}
	
	$suspend = join ',', @suspends;
	&set_state($rate, $line1, $line2, $line3, $line4, $suspend);

	my($pname, $selected, $rest, $nimmt) = &get_my_state($sname);
	$selected = 0;
	&set_player_state($pname, $selected, $rest, $nimmt);

	&exec_culc;
	return "$line_no��ڂ����܂����B";
}

sub auto_get_line {
	my $name = shift;
	
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	my @suspends = split /,/, $suspend;
	my $s = shift @suspends;
	my($sname, $scard) = split /:/, $s;
	if ($sname ne $name) {
		return;
	}
	my @la = split /,/, $line1;
	while (@la) {
		my $get_card = shift @la;
		&add_nimmt($sname, $get_card);
	}
	$line1 = $scard;
	
	$suspend = join ',', @suspends;
	&set_state($rate, $line1, $line2, $line3, $line4, $suspend);

	my($pname, $selected, $rest, $nimmt) = &get_my_state($sname);
	$selected = 0;
	&set_player_state($pname, $selected, $rest, $nimmt);

	&exec_culc;
	system_comment("$sname�s�݂̂��ߎ�����1��ڂ����܂����B");
}

sub print_my_hand {
	my($pname, $selected, $rest, $nimmt) = &get_my_state;
	
	if ($selected == 0 && &is_selectable) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="play">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	}

	my @rests = split /,/, $rest;
	for my $r (@rests) {
		if ($selected == 0 && &is_selectable) {
			print qq|<input type="radio" name="card" value="$r" id="card_$r"/>|;
		}
		print qq|<label for="card_r">|;
		&print_card($r);
		print qq|</label>,|;
	}
	if ($selected == 0 && &is_selectable) {
		print qq|<input type="submit" value="�I������" class="button_s"></form><br>|;
	}
}

sub print_lines {
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	my @lines = ($line1, $line2, $line3, $line4);
	for my $l (@lines) {
		my @la = split /,/, $l;
		for $lc (@la) {
			&print_card($lc);
			print qq|,|;
		}
		print qq|<br>|;
	}
}

sub print_gotten {
	my($pname, $selected, $rest, $nimmt) = &get_my_state;
	
	my $nsum = 0;
	my @nimmts = split /,/, $nimmt;
	for my $c (@nimmts) {
		$nsum += $c == 55 ? 7 :
				$c =~ /^(\d)\1+$/ ? 5 :
				$c =~ /0$/ ? 3 :
				$c =~ /5$/ ? 2 :
				1;
		&print_card($c);
		print qq|,|;
	}
	print qq|<br>�v ��$nsum��<br>|;
}

sub print_card {
	$c = shift;
	my $c_color = $c == 55 ? 'purple' :
				$c =~ /^(\d)\1+$/ ? 'red' :
				$c =~ /0$/ ? 'yellow' :
				$c =~ /5$/ ? 'cyan' :
				'white';
	print qq|<span style="color:$c_color;">$c</span>|;
}

sub start_game{
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	if (@players < 2 || @players > 10 || &is_playing || !(&is_player)) {
		return;
	}
	
	my @deck = &shuffled_deck;
	
	for my $p (@players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		$selected = 0;
		my @rests = ();
		for (1..10) {
			my $c = shift @deck;
			push @rests, $c;
		}
		$rest = join ',', @rests;
		$nimmt = '';
		&set_player_state($pname, $selected, $rest, $nimmt);
	}
	$line1 = shift @deck;
	$line2 = shift @deck;
	$line3 = shift @deck;
	$line4 = shift @deck;
	$suspend = '';
	&set_state($rate, $line1, $line2, $line3, $line4, $suspend);
	
	return ("�Q�[���X�^�[�g");
}

sub end_game {
	my $rank = '';
	my @ranks = ();
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	
	my $seat = 1;
	for my $p (@players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		
		my $nsum = 0;
		my @nimmts = split /,/, $nimmt;
		for my $c (@nimmts) {
			$nsum += $c == 55 ? 7 :
					$c =~ /^[1-9]{2}$/ ? 5 :
					$c =~ /0$/ ? 3 :
					$c =~ /5$/ ? 2 :
					1;
		}
		push @ranks, "$pname<>$nimmt<>$nsum<>$seat<>";
		$seat++;
	}

	@ranks = map { $_->[0] } sort { $a->[3] <=> $b->[3] || $a->[4] <=> $b->[4] } map { [$_, split /<>/ ] } @ranks;
	my $rank_i = 1;
	for my $r (@ranks) {
		my($pname, $nimmt, $nsum, $seat) = split /<>/, $r;
		$rank .= "$rank_i�� $pname ��$nsum�� $nimmt<br>";
		$rank_i++;
	}
	
	open my $fh, "> $game_file" or &error('�ް�̧�ق��J���܂���'); 
	print $fh "$rate<><><><><><>\n";
	close $fh;
	&system_comment($rank);
}

sub participate{
	return("��݂�����܂���") if $m{coin} <= 0;
	
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	unless (@players) {
		$rate = $rates[$in{rate}];
	}
	return("��݂�����܂���") if $m{coin} <= $rate;
	
	return("��x�Ƀv���C�ł���̂�10�l�܂łł��B") if @players >= 10;
	
	push @players, "$m{name}<>0<><><>\n";
	
	open my $fh, "> $game_file" or &error('�ް�̧�ق��J���܂���'); 
	print $fh "$rate<><><><><><>\n";
	print $fh @players;
	close $fh;
	
	$m{c_turn} = 1;
	$m{c_value} = '';
	$m{c_stock} = '';
	&write_user;
	return("$m{name} ���Ȃɒ����܂���");
}

sub exit_game{
	if (&is_playing) {
		return("�Q�[�����n�܂��Ă��܂��B");
	}
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;

	open my $fh, "> $game_file" or &error('�ް�̧�ق��J���܂���'); 
	print $fh "$rate<>$line1<>$line2<>$line3<>$line4<>$suspend<>\n";
	for my $p (@players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		if ($pname ne $m{name}) {
			print $fh $p;
		}
	}
	close $fh;
	
	$m{c_turn} = 0;
	$m{c_value} = 0;
	$m{c_stock} = 0;
	&write_user;
	return("$m{name} �� ��߂܂���");
}

sub is_playing {
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	return ($line1 && $line2 && $line3 && $line4);
}

sub is_player {
	my $name =  shift;
	$name ||= $m{name};
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	for my $p (@players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		if ($pname eq $name) {
			return 1;
		}
	}
	
	return 0;
}

sub is_selectable {
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	for my $p (@players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		if ($selected < 0) {
			return 0;
		}
	}
	
	return 1;
}

sub is_put_minimum {
	my($pname, $selected, $rest, $nimmt) = &get_my_state;
	
	return ($selected < 0);
}

sub get_state {
	open my $fh, "< $game_file" or &error('�ް�̧�ق��J���܂���'); 
	my $head_line = <$fh>;
	my($rate, $line1, $line2, $line3, $line4, $suspend) = split /<>/, $head_line;
	my @players = ();
	while (my $p = <$fh>) {
		push @players, $p;
	}
	close $fh;

	return ($rate, $line1, $line2, $line3, $line4, $suspend, @players);
}

sub get_my_state {
	my $name = shift;
	$name ||= $m{name};
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;
	for my $p (@players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		if ($pname eq $name) {
			return ($pname, $selected, $rest, $nimmt);
		}
	}
	return ('', 0, '', '');
}

sub set_state {
	my($rate, $line1, $line2, $line3, $line4, $suspend) = @_;
	my($orate, $oline1, $oline2, $oline3, $oline4, $osuspend, @players) = &get_state;

	open my $fh, "> $game_file" or &error('�ް�̧�ق��J���܂���'); 
	print $fh "$rate<>$line1<>$line2<>$line3<>$line4<>$suspend<>\n";
	print $fh @players;
	close $fh;
}

sub set_player_state {
	my($pn, $sel, $res, $nm) = @_;
	
	my($rate, $line1, $line2, $line3, $line4, $suspend, @players) = &get_state;

	open my $fh, "> $game_file" or &error('�ް�̧�ق��J���܂���'); 
	print $fh "$rate<>$line1<>$line2<>$line3<>$line4<>$suspend<>\n";
	for my $p (@players) {
		my($pname, $selected, $rest, $nimmt) = split /<>/, $p;
		if ($pname eq $pn) {
			print $fh "$pn<>$sel<>$res<>$nm<>\n";
		} else {
			print $fh $p;
		}
	}
	close $fh;
}

sub add_nimmt {
	my($name, $card) = @_;
	
	my($pname, $selected, $rest, $nimmt) = &get_my_state($name);
	my @nimmts = split /,/, $nimmt;
	push @nimmts, $card;
	$nimmt = join ',', @nimmts;
	&set_player_state($pname, $selected, $rest, $nimmt);
}

sub shuffled_deck{
	my @deck;
	for my $i (1..104){
		push @deck, $i;
	}
	for my $i (0..103){
		my $j = int(rand(104-$i)) + $i;
		my $temp = $deck[$i];
		$deck[$i] = $deck[$j];
		$deck[$j] = $temp;
	}
	return @deck;
}
1;#�폜�s��
