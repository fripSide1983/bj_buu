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
my $rate = 1000000;

unless (-f $all_member_file) {
	open my $fh, "> $bet_file" or &error('�q��̧�ق̏������݂Ɏ��s���܂���');
	print $fh "<>0<>0<>0<>\n";
	close $fh;
}

sub run {
	my ($game_year, $all_rest_a, $all_rest_b, $all_rest_c, $participate, $my_rest_a, $my_rest_b, $my_rest_c, @all_member) = &get_state;
	
	
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
		&receive();
	}
	elsif ($in{mode} eq "check") {
		&check($in{to});
	}
	elsif ($in{mode} eq "recheck") {
		&recheck;
	}
	elsif ($in{mode} eq "uncheck") {
		&uncheck;
	}
	elsif ($in{mode} eq "set") {
		&set($in{set});
	}
	elsif ($in{mode} eq "goal") {
		&goal;
	}
	elsif($in{mode} eq "write" &&$in{comment}){
		&write_comment;
	}
	my ($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;
	
	if ($game_year eq $w{year}) {
		print qq|�S�̎c�� �O�[:$all_rest_a �`���L:$all_rest_b �p�[:$all_rest_c|;
	} elsif ($participate) {
		
	} else {
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
	
	if ($participate) {
		open my $fhm, "< $my_espoir_file" or &error('�Q����̧�ق��J���܂���'); 
		my $headline = <$fhm>;
		my($star, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
		close $fhm;
	}
	
	return ($play_year, $rest_a, $rest_b, $rest_c, $participate, $my_rest_a, $my_rest_b, $my_rest_c, @all_players);
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