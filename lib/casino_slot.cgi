#================================================
# �ۯď��i�v���O���b�V�u�W���b�N�|�b�g�j
#================================================
require "$datadir/casino_bonus.cgi";
require "./lib/_casino_funcs.cgi";

$header_size = 2; # �ۯď��p��ͯ�ް���� JP�A����JP
($_jp, $_ceil) = ($_header_size .. $_header_size + $header_size - 1); # ͯ�ް�z��̲��ޯ��

sub run {

	&_default_run;
}

sub show_head_info { # ���ׂĂ���ڲ԰�ɕ\�����������1
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	# ���ɖ��̏���
	print qq|�ެ���߯āF$head[$_jp]|;
	my @bets = ('1bet', '2bet', '3bet');
	print qq|<form method="$method" action="$this_script" name="form">|;
	print &create_submit("play", "��");
	print &create_select_menu("bet_value", $in{bet_value}, @bets);
	print qq|</form>|;
}

sub play {
	return unless $m{name} eq 'VIPPER' || $m{name} eq 'nanamie';
	my $value = $in{bet_value} + 1;

	# my $this_pool_file  = "$userdir/$id/casino_pool.cgi"; # ��`�Y��H ��`����ĂȂ�����
	# ���̏������������ ��݂� 1000 �����Ȃ��ꍇ�� 3 bet �ł��Ă��܂��A
	# ������݂� -2000 �ɂȂ�s����C�������Ƃ��A����ł��ȉ��̏������K�v�Ȃ̂��H
	if ($m{coin} < (1000 * $value)) { # ������݂� 1000 �������ǂ����������Ă��Ȃ������̂ŁA1000 ��݂���� 3 bet 3000 ��ݏ���ł���
=pod
������݂� 1000 �����̂Ƃ��A��@���ɂ����ĂĂ��āA�����߰ٺ�݂� 1 �ȏ�ł͂Ȃ��Ȃ珊����݂� 0 �ɂȂ�
$this_pool_file ����`����ĂȂ������̂ŁA���ǂ̂Ƃ��뺲݂� 1000 �����̏�Ԃŉ񂻂��Ƃ���Ƃ݂�ȏ�����݂������Ă���
		my $pool_find = 0;
		if (-f "$userdir/$id/casino_pool.cgi") {
			open my $fh, "< $this_pool_file" or &error("$this_pool_file���J���܂���");
			while (my $line = <$fh>){
				my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
				if ($pool > 0) {
					$pool_find = 1;
				}
				last;
			}
			close $fh;
		}
		unless ($pool_find) {
			$m{coin} = 0;
			&write_user;
		}
=cut
		return ('��݂�����܂���');
	}
	$m{coin} -= (1000 * $value);

	my @m = ('�V');
	my @m_exval = ('��','��','��','��','��','��','��','��','��','��','�~','��','��','��','��','��','��','��','��','��'); # 20��
	for my $val (@m_exval){
		push @m, $val for (0..5); # 6��
	}
	# 20��ϰ���6���ǉ� 120��ϰ��̒��� 7 ��1�� 1/121 �̊m���� 7
	my @s = ();
	my $gflag = 0;
	my $rets = '';
	my @prizes = ();
	$s[$_] = int(rand(@m)) for (0 .. 8);

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ͯ�ް
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		next if $sames{$mname}++; # �����l�Ȃ玟
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
	}

	# �ެ���߯Ăɺ�ݗ��܂肷���Ȃ��悤�ɂ��邽�߂̋����ެ���߯�
	$s[0] = $s[1] = $s[2] = 0 if $head[$_jp] > $head[$_ceil];

	$rets .= "<p>�y$m[$s[3]]�z�y$m[$s[4]]�z�y$m[$s[5]]�z</p>";
	$rets .= "<p>�y$m[$s[0]]�z�y$m[$s[1]]�z�y$m[$s[2]]�z</p>";
	$rets .= "<p>�y$m[$s[6]]�z�y$m[$s[7]]�z�y$m[$s[8]]�z</p>";

	if ($m[$s[0]] eq $m[$s[1]] && $m[$s[0]] eq $m[$s[2]]) {
		if ($s[0] != 0) { # jackpot�ȊO
			$m{coin} += 50000;
			$rets .= "�Ȃ��!! $m[$s[0]] ��3���낢�܂���!!��� 50000 ���l��<br>";
		}
		else {
			$rets .= "Jackpot!!!";
			$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes);
		}
		$gflag = 1;
	}

	if ($value >= 2) {
		if ($m[$s[3]] eq $m[$s[4]] && $m[$s[3]] eq $m[$s[5]]) {
			if ($s[3] != 0) { # jackpot�ȊO
				$m{coin} += 50000;
				$rets .= "�Ȃ��!! $m[$s[3]] ��3���낢�܂���!!��� 50000 ���l��<br>";
			}
			else {
				$rets .= "Jackpot!!!";
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes);
			}
			$gflag = 1;
		}
		if ($m[$s[6]] eq $m[$s[7]] && $m[$s[6]] eq $m[$s[8]]) {
			if ($s[6] != 0) { # jackpot�ȊO
				$m{coin} += 50000;
				$rets .= "�Ȃ��!! $m[$s[6]] ��3���낢�܂���!!��� 50000 ���l��<br>";
			}
			else {
				$rets .= "Jackpot!!!";
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes);
			}
			$gflag = 1;
		}
	}
	
	if ($value == 3) {
		if ($m[$s[3]] eq $m[$s[1]] && $m[$s[3]] eq $m[$s[8]]) {
			if ($s[3] != 0) { # jackpot�ȊO
				$m{coin} += 50000;
				$rets .= "�Ȃ��!! $m[$s[3]] ��3���낢�܂���!!��� 50000 ���l��<br>";
			}
			else {
				$rets .= "Jackpot!!!";
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes);
			}
			$gflag = 1;
		}
		if ($m[$s[6]] eq $m[$s[1]] && $m[$s[6]] eq $m[$s[5]]) {
			if ($s[6] != 0) { # jackpot�ȊO
				$m{coin} += 50000;
				$rets .= "�Ȃ��!! $m[$s[6]] ��3���낢�܂���!!��� 50000 ���l��<br>";
			}
			else {
				$rets .= "Jackpot!!!";
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes);
			}
			$gflag = 1;
		}
	}

	unless ($gflag) {
		$head[$_jp] += 50 * ($value);
		$rets .= '<p>ʽ��</p>';
	}

	unshift @members, &h_to_s(@head);
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	&send_item($m{name},$bonus[$prizes[$_]][0],$bonus[$prizes[$_]][1],$bonus[$prizes[$_]][2],$bonus[$prizes[$_]][3], 1) for (0 .. $#prizes);

	&write_user;
	return ($rets);
}

sub jackpot {
	my ($ref_jp, $ref_ceil, $ref_prizes) = @_;
	my $prize = '';

	while ($$ref_jp > 2500000) {
		my $item_no = int(rand($#bonus+1));
		push @$ref_prizes, $item_no;
		if ($bonus[$item_no][0] == 1) {
			$prize .= "$weas[$bonus[$item_no][1]][1]";
		}
		elsif ($bonus[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus[$item_no][1]][1]";
		}
		$$ref_jp -= 1000000;
	}

#	&mes_and_world_news("<b>�ެ���߯Ă��o���܂���</b>", 1);

	$m{coin} += $$ref_jp;
	$$ref_jp = 3000000;
	$$ref_ceil = int(rand(100000000) + 3000000);
	return "��� $jp �� $prize ���l�����܂���<br>";
}

1;#�폜�s��
