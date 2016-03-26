#================================================
# ��{����
#================================================

sub run {
	if ($in{mode} eq "p_set") {
	    $in{comment} = &player_set($in{b_1} + $in{b_2}*10 + $in{b_3}*100 + $in{b_4}*1000);
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "c_open") {
		$in{comment} .= &open_card;
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
	elsif ($in{mode} eq "c_set") {
	    $in{comment} = &set_card($in{waiting});
	    &write_comment if $in{comment};
	}
	elsif ($in{mode} eq "exit") {
	    $in{comment} = &exit_game;
	    &write_comment if $in{comment};
	}
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember, $number_log) = &get_member;

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
	print $leader eq '' ? qq|�e:��W�� ������: �ځF$number_log<br>|:qq|�e:$leader ������:$max_bet �ځF$number_log<br>$wmember<br>|;
	if($leader){
		if($state eq 'playing' && $m{c_turn} > 1){
			if($m{name} eq $leader){
				if($waiting <= 0 && $in{mode} ne 'c_set'){
					print qq|<form method="$method" action="$this_script" name="form">|;
					print qq|<input type="hidden" name="mode" value="c_open">|;
					print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
					print qq|<input type="submit" value="�J��" class="button_s"></form><br>|;
				}
			}elsif($m{c_turn} eq '5') {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="p_set">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="radio" name="b_1" value="0">��߂�<br>|;
				for my $i (1..$m{c_value}){
					print qq|<input type="radio" name="b_$i" value="1" checked>1<input type="radio" name="b_$i" value="2">2<input type="radio" name="b_$i" value="3">3<input type="radio" name="b_$i" value="4">4<input type="radio" name="b_$i" value="5">5<input type="radio" name="b_$i" value="6">6<br>|;
				}
				print qq|<input type="submit" value="����" class="button_s"></form><br>|;
			}
		}elsif($m{name} ne $leader && ($m{c_turn} eq '0' || $m{c_turn} eq '')) {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="text"  name="comment" class="text_box_b"> ��� <input type="hidden" name="mode" value="bet"><input type="hidden" name="max_bet" value="$max_bet">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="radio" name="cmd" value="1" checked>1�_����<input type="radio" name="cmd" value="2">2�_����<input type="radio" name="cmd" value="3">3�_����<input type="radio" name="cmd" value="4">4�_����|;
			print qq|<input type="submit" value="�q����" class="button_s"></form><br>|;
		}elsif($m{name} eq $leader && $in{mode} ne 'leader') {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="c_set">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="waiting" value="$waiting"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="radio" name="cmd" value="0" checked>��<br>|;
			print qq|<input type="radio" name="cmd" value="1">1<input type="radio" name="cmd" value="2">2<input type="radio" name="cmd" value="3">3<input type="radio" name="cmd" value="4">4<input type="radio" name="cmd" value="5">5<input type="radio" name="cmd" value="6">6<br>|;
			print qq|<input type="submit" value="�����" class="button_s"></form><br>|;
		}
	}else {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print qq|<input type="hidden" name="mode" value="leader">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="text"  name="comment" class="text_box_b" value="10"> ��� <input type="submit" value="�e�ɂȂ�" class="button_s"></form><br>|;
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
	my $l_is_in = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	my $waiting = 0;
	my $wmember = '';
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state, $number_log) = split /<>/, $head_line;
	push @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			if($mturn > 0){
				$mturn = 0;
				$mvalue = 0;
			}else {
				next;
			}
		}
		next if $sames{$mname}++; # �����l�Ȃ玟
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		}
		if ($mname eq $leader && $time - $limit_member_time < $mtime) {
		    $l_is_in = 1;
		    $waiting--;
		}
		if ($mturn > 0) {
			my @values = ($mvalue % 10, int($mvalue / 10) % 10, int($mvalue / 100) % 10, int($mvalue / 1000));
			$wmember .= "$mname�F";
			if($mname ne $leader){
				if($mturn == 1){
					$wmember .= "�X�C�`�i5.5�{�j$values[0]";
				}
				elsif($mturn == 2){
					$wmember .= "�P�b�^�c�i3.5�{�j$mvalue[0] (2.0�{)$mvalue[1]";
				}
				elsif($mturn == 3){
					$wmember .= "�|���E�P�i3.8�{�j$mvalue[0] (1.0�{)$mvalue[1] (1.0�{)$mvalue[2]";
				}
				elsif($mturn == 4){
					$wmember .= "�\\�E�_�C�i3.0�{�j$mvalue[0] (1.0�{)$mvalue[1] (1.0�{)$mvalue[2] (1.0�{)$mvalue[3]";
				}else {
					$wmember .= "�l����";
				}
			}else {
				$wmember .= "�e";
			}
			$wmember .= "<br>";
		}
		$waiting++ if $mturn == 5;
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

	my $member_c = @members - 1;

	if($l_is_in eq '0' && $state ne ''){
	    &leader_penalty;
	}

	return ($member_c, $member, $leader, $max_bet, $waiting, $state, $wmember, $number_log);
}

sub make_leader {
	return("��݂�����܂���") if $m{coin} < 0;
	my @members = ();
	my %sames = ();
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state, $number_log) = split /<>/, $head_line;
	if($leader eq ''){
		$leader = $m{name};
		my $v;
		if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
			$v = $in{comment};
			$v = $m{coin} if $v > $m{coin};
			if($v > 0){
				$m{coin} -= $v;
				$m{c_turn} = 5;
				&write_user;
			}
		}
		$max_bet = $v;
#		$max_bet = 10;
		$state = 'waiting';
	}
	push @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
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
	&write_user;
	return ("$leader ���e�ł� �q�����:$max_bet");
}

sub set_card{
	my @members = ();
	my $p_mes = "����܂����I";
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state, $number_log) = split /<>/, $head_line;
	$state = 'playing';
	if($cmd == 0){
		$p_mes = "�􂢂܂����B$max_bet �̎󂩂�";
		$m{coin} += $max_bet;
		$leader = '';
		$max_bet = 0;
		$state = '';
		$m{c_turn} = 0;
	}else {
		$m{c_value} = $cmd;
	}
	&write_user;
	push @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
	while (my $line = <$fh>) {
		if($m{c_turn} eq '0'){
			my($mtime, $mname, $maddr, $mturn) = split /<>/, $line;
			push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n";
	    }else{
	    	push @members, $line;
	    }
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	return ($p_mes);
}

sub bet{
	my $max = shift;
	my $v;
	if($in{comment} > 0 && $in{comment} !~ /[^0-9]/){
		$v = $in{comment};
		$v = $m{coin} if $v > $m{coin};
		if($v > 0){
			$v = $max if $v > $max;
			$m{c_stock} = $v;
			$m{c_turn} = 5;
			$m{c_value} = $cmd;
			&write_user;
			return("$m{name} �� $v ��� ����܂���");
		}
	}
}

sub player_set {
	my $value = shift;
	my $dmes = '';
	$m{c_turn} = $m{c_value};
	$m{c_value} = $value;
	&write_user;
	my @values = ($value % 10, int($value / 10) % 10, int($value / 100) % 10, int($value / 1000));
	if($m{c_turn} == 1){
		$dmes = "�X�C�`�i5.5�{�j$values[0]";
	}
	elsif($m{c_turn} == 2){
		$dmes = "�P�b�^�c�i3.5�{�j$values[0] (2.0�{)$values[1]";
	}
	elsif($m{c_turn} == 3){
		$dmes = "�|���E�P�i3.8�{�j$values[0] (1.0�{)$values[1] (1.0�{)$values[2]";
	}
	else{
		$dmes = "�\\�E�_�C�i3.0�{�j$values[0] (1.0�{)$values[1] (1.0�{)$values[2] (1.0�{)$values[3]";
	}
	return ($dmes);
}


sub open_card{
	my @members = ();
	my %sames = ();
	my $lmes = "$m{c_value} !";
	my $total = 0;
	my $sum_win = 0;
	my %vs = ();
	my @names = ();
	my $rate = 1;

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state, $number_log) = split /<>/, $head_line;
	push @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟
		my $kid = unpack 'H*', $mname;
		next unless (-f "$userdir/$kid/user.cgi");
		if($mturn ne '0' && $mturn ne '5' && $mname ne $m{name}){
			my $v = 0;
			my %datas = &get_you_datas($mname);
			$v = $datas{c_stock};
			my @values = ($mvalue % 10, int($mvalue / 10) % 10, int($mvalue / 100) % 10, int($mvalue / 1000));
			if($mturn == 1){
				$v *= $values[0] eq $m{c_value} ? 4.5:
						-1;
			}
			elsif($mturn == 2){
				$v *= $values[0] eq $m{c_value} ? 2.5:
						$values[1] eq $m{c_value} ? 1.0:
						-1;
			}
			elsif($mturn == 3){
				$v *= $values[0] eq $m{c_value} ? 2.8:
						$values[1] eq $m{c_value} ? 0:
						$values[2] eq $m{c_value} ? 0:
						-1;
			}
			else{
				$v *= $values[0] eq $m{c_value} ? 2.0:
						$values[1] eq $m{c_value} ? 0:
						$values[2] eq $m{c_value} ? 0:
						$values[3] eq $m{c_value} ? 0:
						-1;
			}
			$v = int($v);
			push @names, $mname;
			$vs{$mname} = $v;
			$total += $v;
		}
		next if $time - $limit_member_time > $mtime;
		push @members, "$mtime<>$mname<>$maddr<>0<>0<>\n";
	}
	if($total >= $max_bet) {
		$rate = 1.0 * $max_bet / $total;
	}
	my @new_log = (int($number_log / 100000), int($number_log / 10000) % 10, int($number_log / 1000) % 10, int($number_log / 100) % 10, int($number_log / 10) % 10, $number_log % 10);
	$number_log = $m{c_value};
	my $count = 0;
	for my $i (@new_log){
		if ($i == 0) {
			$number_log = 123456;
			last;
		}
		if ($i eq $m{c_value}) {
			if($count eq '0'){
				$lmes .= "��";
			}elsif($count eq '1'){
				$lmes .= "���߂�";
			}elsif($count eq '2'){
				$lmes .= "�O��";
			}elsif($count eq '3'){
				$lmes .= "�l��";
			}elsif($count eq '4'){
				$lmes .= "�t���c�L";
			}else{
				$lmes .= "��";
			}
			next;
		}
		$number_log *= 10;
		$number_log += $i;
		$count++;
	}
	for my $k (@names){
		my $kid = unpack 'H*', $k;
		if (-f "$userdir/$kid/user.cgi") {
			my %datas = &get_you_datas($k);
			&regist_you_data($k,'coin',$datas{coin} + int($vs{$k} * $rate));
			&regist_you_data($k,'c_turn',0);
			if($vs{$k} > 0){
				$lmes .= "<br>$k �� $vs{$k} ��� �����܂���";
			}elsif($vs{$k} < 0){
				$vs{$k} *= -1;
				$lmes .= "<br>$k �� $vs{$k} ��� �����܂���";
			}else{
				$lmes .= "<br>$k �͎�ł�";
			}
		}
	}
	$max_bet -= $total;
	$state = 'waiting';
	
	if($max_bet <= 0){
		$max_bet = 0;
		$leader = '';
		$max_bet = 0;
		$state = '';
		$m{c_turn} = 0;
		&write_user;
	}
	
	shift @members;
	unshift @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;
	return $lmes;
}


sub exit_game{
	$m{c_turn} = 0 if $m{c_turn} == 5;
	&write_user;
	return("$m{name} �� ��߂܂���");
}

sub leader_penalty{
	my @members = ();
	my %sames = ();
	my $mes = "";
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($leader, $max_bet, $state, $number_log) = split /<>/, $head_line;
	my $lname = $leader;
	my $sum_penalty = $max_bet;
	$leader = '';
	$max_bet = 0;
	$state = '';
	push @members, "$leader<>$max_bet<>$state<>$number_log<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # �����l�Ȃ玟

		if($mturn ne '0' && $mname ne $lname){
			my $v = 0;
			my %datas = &get_you_datas($mname);
			$v = $datas{c_stock};
			$sum_penalty -= $v;
			&regist_you_data($mname,'coin',$datas{coin} + $v);
			&regist_you_data($mname,'c_turn',0);
			$mes .= "<br>�e�����f�ސȂ������� $mname �� $v ��� �Ⴂ�܂���";
		}

		push @members, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my %datas = &get_you_datas($lname);
	&regist_you_data($lname,'coin',$datas{coin} + $sum_penalty);
	&regist_you_data($lname,'c_turn',0);
	return $mes;
}

1;#�폜�s��
