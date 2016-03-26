#================================================
# toto
#================================================
require './lib/_comment_tag.cgi';
require './lib/_casino_funcs.cgi';

# �q�����
my $bet_file = "$logdir/toto.cgi";

# 1�[������̋��z
my $rate = 10000;

# �J�ÂɕK�v�Ⱥ�݁i�[�j
my $make_fee = 100;

# �T����
my $house_edge = 0.05;
my $house_edge_dark = 0.25;

# �q���̎��
my @kinds = (
	['strong', '�D����'],
	['nou', '�_��'],
	['sho', '����'],
	['hei', '����'],
	['gou', '���D'],
	['cho', '����'],
	['sen', '���]'],
	['gik', '�U�v'],
	['res', '�~�o'],
	['esc', '�E��'],
	['tei', '��@'],
	['stop', '���'],
	['pro', '�F�D'],
	['dai', '���{'],
);

unless (-f $bet_file) {
	open my $fh, "> $bet_file" or &error('�q��̧�ق̏������݂Ɏ��s���܂���');
	print $fh "<><><>\n";
	close $fh;
}

my $wc = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};

sub run {
	if ($in{mode} eq "make_game") {
		$in{comment} = &make_game;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "bet") {
		&bet;
	}
	elsif($in{mode} eq "write" &&$in{comment}){
		&write_comment;
	}
	my ($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;
	
	if (&isPlaying) {
		my ($leadar, $year, $odds) = &get_toto_data;
		print qq|$year�N$leadar�t<br>|;
		print qq|<hr>|;
		print qq|���݂̃I�b�Y<br>$odds|;
		print qq|<hr>|;
		print qq|1�� $rate ���<br>|;
		print qq|<form method="$method" action="$this_script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="hidden" name="mode" value="bet">|;
		print qq|<input type="text" name="bet" value="1">|;
		print qq|<select name="bet_country">|;
		print qq|<option value=""></option>|;
		for my $c (1..$wc) {
			print qq|<option value="$c">$cs{name}[$c]</option>|;
		}
		print qq|</select>|;
		print qq|<input type="submit" value="�q����" class="button1"></form>|;
	} elsif (&isGaming) {
		my ($leadar, $year, $odds) = &get_toto_data;
		print qq|$year�N$leadar�t<br>|;
		print qq|<hr>|;
		print qq|���݂̃I�b�Y<br>$odds|;
		print qq|<hr>|;
	} else {
		print qq|<form method="$method" action="$this_script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="hidden" name="mode" value="make_game">|;
		print qq|<input type="submit" value="�����ɂȂ�" class="button1"></form>|;
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

sub isPlaying {
	open my $fh, "< $bet_file" or &error('�q��̧�ق��J���܂���'); 
	my $headline = <$fh>;
	my($leadar, $year, $kind) = split /<>/, $headline;
	close $fh;
	return ($year == $w{year} + 1);
}

sub isGaming {
	open my $fh, "< $bet_file" or &error('�q��̧�ق��J���܂���'); 
	my $headline = <$fh>;
	my($leadar, $year, $kind) = split /<>/, $headline;
	close $fh;
	return ($year == $w{year});
}

sub make_game {
	my $mmes = '';
	my @members = ();
	
	if ($m{coin} < $make_fee * $rate) {
		return "�e�ɂȂ�ɂ�$make_fee�[���̺�݂��K�v�ł��B";
	}
	if ($m{year} =~ /[59]$/) {
		return "�Ղ��̊J�Â͂ł��܂���B";
	}
	
	open my $fh, "+< $bet_file" or &error('�q��̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $headline = <$fh>;
	my($leadar, $year, $kind) = split /<>/, $headline;
	if ($year < $w{year}) {
		$year = $w{year} + 1;
		$kind = int(rand(@kinds));
		push @members, "$m{name}<>$year<>$kind<>\n";
		push @members, "$m{name}<>-1<>$make_fee<>\n";
		$m{coin} -= $make_fee * $rate;
		$mmes .= "$year�N$m{name}�t�J�Ì���!���[��W��!";
		&write_user;
	} else {
		push @members, $headline;
		while (my $line = <$fh>) {
			push @members, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	return $mmes;
}

sub bet {
	if($in{bet_couontry} !~ /[^0-9]/ && $in{bet_country} > 0 && $in{bet_country} <= $w{country} && 
		$in{bet} > 0 && $in{bet} !~ /[^0-9]/ && $in{bet} * $rate < $m{coin}){
		my @members = ();

		open my $fh, "+< $bet_file" or &error('�q��̧�ق��J���܂���'); 
		eval { flock $fh, 2; };
		my $headline = <$fh>;
		my($leadar, $year, $kind) = split /<>/, $headline;
		push @members, $headline;
		while (my $line = <$fh>) {
			push @members, $line;
			my($name, $country, $bet) = split /<>/, $line;
			if ($name eq $m{name} && $country != -1) {
				$in{bet_country} = $country;
			}
		}
		if ($year == $w{year} + 1) {
			push @members, "$m{name}<>$in{bet_country}<>$in{bet}<>\n";
			$m{coin} -= $in{bet} * $rate;
			&write_user;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @members;
		close $fh;
	}
}

sub get_toto_data {
	my $odds = '';
	my @bets = ();
	my @my_bets = ();
	my $total_bets = 0;
	
	open my $fh, "< $bet_file" or &error('�q��̧�ق��J���܂���'); 
	my $headline = <$fh>;
	my($leadar, $year, $kind) = split /<>/, $headline;
	while (my $line = <$fh>) {
		my($name, $country, $bet) = split /<>/, $line;
		if ($country != -1) {
			$bets[$country] += $bet;
			if ($name eq $m{name}) {
				$my_bets[$country] += $bet;
			}
		}
		$total_bets += $bet;
	}
	close $fh;
	
	for my $c (1..$wc) {
		my $cname = '';
		my $codds = 0;
		my $mbet = $my_bets[$c];
		$cname = $cs{name}[$c];
		my $bc = $bets[$c];
		if ($bc <= 0) {
			$bc = 1;
		}
		$codds = $total_bets * (1.0 - $house_edge - $house_edge_dark) / $bc;
		$odds .= "$cname : $codds �{";
		if ($mbet) {
			$odds .= " $mbet �[���[��";
		}
		$odds .= "<br>";
	}
	
	return ($leadar, $year, $odds)
}

sub pay_back {
	my $pay_year = shift;
	
	my @bets = ();
	my $total_bets = 0;
	my $total_pay = 0;
	my %name_bet = ();
	
	open my $fh, "< $bet_file" or &error('�q��̧�ق��J���܂���'); 
	my $headline = <$fh>;
	my($leadar, $year, $kind) = split /<>/, $headline;
	while (my $line = <$fh>) {
		my($name, $country, $bet) = split /<>/, $line;
		if ($country != -1) {
			$bets[$country] += $bet;
			if (!$name_bet{$name}) {
				$name_bet{$name} = ();
			}
			$name_bet{$name}[$country] += $bet;
		}
		$total_bets += $bet;
	}
	close $fh;
	
	if ($pay_year != $year) {
		return;
	}
	
	my $win_country = 0;
	
	my %sames = ();
	my $status = $kinds[$kind][0];
	my $max = 0.0;
	
	for my $country (0 .. $w{country}) {

		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgi̧�ق��J���܂���");

		while (my $player = <$cfh>) {
			$player =~ tr/\x0D\x0A//d;
			next if ++$sames{$player} > 1;
			my $player_id = unpack 'H*', $player;
			unless (-f "$userdir/$player_id/year_ranking.cgi") {
				next;
			}
			
			open my $fh, "< $userdir/$player_id/year_ranking.cgi" or &error("year_ranking.cgi̧�ق��J���܂���");
			while (my $line = <$fh>) {
				my %ydata;
				for my $hash (split /<>/, $line) {
					my($k, $v) = split /;/, $hash;
					$ydata{$k} = $v;
					if($k eq 'year'){
						if($v != $pay_year){
							next;
						}
					}
				}
				if($ydata{year} == $pay_year){
					if($ydata{$status}){
						if ($max < $ydata{$status}) {
							$max = $ydata{$status};
							$win_country = $country;
						}
					}
				}
			}
			close $fh;
		}
		close $cfh;
	}
	
	my $world_mes = '�q���Ώۂ� ' . $kinds[$kind][1];
	$world_mes .= ' �ł����B���I���� ';
	my $bc = $bets[$win_country];
	$world_mes .= $cs{name}[$win_country] . '�ŁA';
	if ($bc <= 0) {
		$bc = 1;
	}
	my $odds = $total_bets * (1.0 - $house_edge - $house_edge_dark) / $bc;
	$world_mes .= '�z����' . $odds . '�{�ł���';
	for my $name (keys(%name_bet)) {
		my $get_coin = 0;
		if ($name_bet{$name}[$win_country] > 0) {
			$get_coin += int($name_bet{$name}[$win_country] * $odds * $rate);
		}
		if ($get_coin > 0) {
			$total_pay += $get_coin;
			&item_or_coin($get_coin, $name);
		}
	}
	
	&write_send_news(qq|<font color="#0000FF">$world_mes</font>|);
	&item_or_coin(int($total_bets * $house_edge), $leadar);
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