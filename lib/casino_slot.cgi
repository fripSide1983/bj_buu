#================================================
# �ۯď��i�v���O���b�V�u�W���b�N�|�b�g�j
#================================================
#require "$datadir/casino_bonus.cgi";
# �ެ���߯Ă̎d�l�ς������̂ŁA���p����Ă遪�͎g��Ȃ����ƂɁc
@bonus_5 = ( # 50000 / 225 * 3000 = 666666���
	[2,17,0,0],		# ���è����
	[2,19,0,0],		# ���߰����
	[2,34,0,0],		# ������
	[3,121,0,0],	# �߲��ݿ����
);

@bonus_10 = ( # 100000 / 225 * 3000 = 1333333���
	[2,3,0,0],		# ����
	[3,1,0,0],		# ���
	[3,14,0,0],		# �ȷȺ
	[3,124,0,0],	# �޽
);

@bonus_25 = (  # 250000 / 225 * 3000 = 3333333���
	[2,2,0,0],		# �H��
	[3,16,0,0],		# �ޯ��
	[3,17,0,0],		# �̧��
	[3,18,0,0],		# ж��
);

@bonus_50 = (  # 500000 / 225 * 3000 = 6666666���
	[2,32,0,0],		# ���ذ����
	[2,38,0,0],		# �ذĴ���
	[2,39,0,0],		# �޽����
);

@bonus_100 = (  # 500000 / 225 * 3000 = 6666666���
	[2,37,0,0],		# �ޯ�޴���
	[2,41,0,0],		# Ͻ������
	[2,46,0,0],		# ��´���
	[2,47,0,0],		# �ײѴ���
);

@bonus_200 = (  # 1000000 / 225 * 3000 = 13333333���
	[1,32,500,30],	#���ʰ�30
	[3,168,0,0],	# �߲���
	[3,7,0,0],		# �޸�
	[3,8,0,0],		# �ް��
);

@bonus_300 = ( # 2000000 / 225 * 3000 = 26666666���
	[2,54,0,0],		# ����
	[3,183,0,0],	# ���
	[3,21,0,0],		# ����ش�
);

require "./lib/_casino_funcs.cgi";

$header_size = 2; # �ۯď��p��ͯ�ް���� JP�A����JP
($_jp, $_ceil) = ($_header_size .. $_header_size + $header_size - 1); # ͯ�ް�z��̲��ޯ��

sub run {
	$option_form .= qq|<form method="$method" action="$this_script" name="form">|;
	$option_form .= &create_submit("view_log", "JP���O");
	$option_form .= qq|</form>|;

	&_default_run;
}

sub show_head_info { # ���ׂĂ���ڲ԰�ɕ\�����������1
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	# ���ɖ��̏���
	print qq|�ެ���߯āF$head[$_jp]|;
	my @bets = ('1bet', '2bet', '3bet');
	print qq|<form method="$method" action="$this_script" name="form">|;
	print &create_select_menu("bet_value", $in{bet_value}, @bets);
	print &create_submit("play", "��");
	print qq|</form>|;
}

sub play {
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
	my @m_exval = ('��','��','��','��','��','��','��','��','��','��','��','��','��','��','��','��','��'); # 17�� ,'��','��','�~'
	for my $val (@m_exval) {
		push @m, $val for (0..3); # 4�� ���� 6
	}
	# 17���ϰ���4���ǉ� �v68��ϰ��̒��� 7 ��1�� 1/69 �̊m���� 7
	my @s = ();
	my $gflag = 0;
	my ($rets, $jp_log) = ('', '');
	my @prizes = ();
	$s[$_] = int(rand(@m)) for (0 .. 8);
	# 17���ϰ���4���ǉ� �v68��ϰ��̒��� 7 ��1�� 1/69 �̊m���� 7 7 ��3�o��̂� 1/(69^3) = 1/250047
	# 9�ӏ��̃}�X�ň�񑵂��Γ����� 1/(9^2) = 1/81 �̊m���ő����i7�ȊO�͕�������̂ňႤ�͂��j
	# 1/(63^3) = 1/250047 1/(9^2) = 1/81 �܂�JP���o��m���� 1/20253807�H
	# 2/13468869 poppo

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
	$s[0] = $s[1] = $s[2] = 0 if 2500000 < $head[$_jp] && 2500000 < $head[$_ceil] && $head[$_ceil] < $head[$_jp];

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
			$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes, \$jp_log);
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
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes, \$jp_log);
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
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes, \$jp_log);
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
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes, \$jp_log);
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
				$rets .= &jackpot(\$head[$_jp], \$head[$_ceil], \@prizes, \$jp_log);
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

	for my $i (0 .. $#prizes) {
		my @bonus = split /<>/, $prizes[$i];
		&send_item($m{name},$bonus[0],$bonus[1],$bonus[2],$bonus[3], 1);
	}

	if ($jp_log) {
		my @logs = ();
		my $log_num = 0;
		open my $fh, "+< ${this_file}_log.cgi" or &error('���ް̧�ق��J���܂���'); 
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			push @logs, $line;
			$log_num++;
			last if 29 <= $log_num;
		}
		unshift @logs, "$m{name} $jp_log $date\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @logs;
		close $fh;

		&mes_and_world_news("<b>�ެ���߯Ă��o���܂���</b>", 1);
	}

	&write_user;
	return ($rets);
}

sub jackpot {
	my ($ref_jp, $ref_ceil, $ref_prizes, $ref_log) = @_;
	my $prize = '';

	$$ref_log .= "jackpot:$$ref_jp my_coin:$m{coin} ";
	my $jp = 2500000 - $m{coin}; # ������̶݂ݽĂ�D�悵�ė]������݂��щ�
	$$ref_log .= "get_coin:$jp�� ";
	$$ref_jp = $$ref_jp - $jp;
	$m{coin} = 2500000;

	# �֐������������ǂ���������ƂȂ񂩕ʂɗǂ����Ȃ̃R�s�y
	if ($$ref_jp > 3000000) {
		my $item_no = int(rand($#bonus_300+1));
		push @$ref_prizes, join('<>', @{$bonus_300[$item_no]});
		if ($bonus_300[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_300[$item_no][1]][1]";
		}
		elsif ($bonus_300[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_300[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_300[$item_no][1]][1]";
		}
		$$ref_jp -= 3000000;
	}
	if ($$ref_jp > 2000000) {
		my $item_no = int(rand($#bonus_200+1));
		push @$ref_prizes, join('<>', @{$bonus_200[$item_no]});
		if ($bonus_200[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_200[$item_no][1]][1]";
		}
		elsif ($bonus_200[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_200[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_200[$item_no][1]][1]";
		}
		$$ref_jp -= 2000000;
	}
	if ($$ref_jp > 1000000) {
		my $item_no = int(rand($#bonus_100+1));
		push @$ref_prizes, join('<>', @{$bonus_100[$item_no]});
		if ($bonus_100[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_100[$item_no][1]][1]";
		}
		elsif ($bonus_100[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_100[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_100[$item_no][1]][1]";
		}
		$$ref_jp -= 1000000;
	}
	if ($$ref_jp > 500000) {
		my $item_no = int(rand($#bonus_50+1));
		push @$ref_prizes, join('<>', @{$bonus_50[$item_no]});
		if ($bonus_50[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_50[$item_no][1]][1]";
		}
		elsif ($bonus_50[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_50[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_50[$item_no][1]][1]";
		}
		$$ref_jp -= 500000;
	}
	if ($$ref_jp > 250000) {
		my $item_no = int(rand($#bonus_25+1));
		push @$ref_prizes, join('<>', @{$bonus_25[$item_no]});
		if ($bonus_25[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_25[$item_no][1]][1]";
		}
		elsif ($bonus_25[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_25[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_25[$item_no][1]][1]";
		}
		$$ref_jp -= 250000;
	}
	if ($$ref_jp > 100000) {
		my $item_no = int(rand($#bonus_10+1));
		push @$ref_prizes, join('<>', @{$bonus_10[$item_no]});
		if ($bonus_10[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_10[$item_no][1]][1]";
		}
		elsif ($bonus_10[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_10[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_10[$item_no][1]][1]";
		}
		$$ref_jp -= 100000;
	}
	if ($$ref_jp > 50000) {
		my $item_no = int(rand($#bonus_5+1));
		push @$ref_prizes, join('<>', @{$bonus_5[$item_no]});
		if ($bonus_5[$item_no][0] == 1) {
			$prize .= "$weas[$bonus_5[$item_no][1]][1]";
		}
		elsif ($bonus_5[$item_no][0] == 2) {
			$prize .= "$eggs[$bonus_5[$item_no][1]][1]";
		}
		else {
			$prize .= "$pets[$bonus_5[$item_no][1]][1]";
		}
		$$ref_jp -= 50000;
	}
=pod
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
=cut

#	$m{coin} += $$ref_jp;
#	$$ref_jp = $$ref_jp > 0 ? $$ref_jp + 2500000 : 2500000 ;
	$$ref_jp = 2500000;
	# ����JP ������m���߂�����Ⴍ����JP���߂����Ă���œf��������A���������f������JP���܂�Ȃ��悤�ɂ����������S�Ȃ̂ł́H
	# �Ȃ��Ȃ�JP������Ȃ��̂ɂ���œf�����ƑS�R������Ȃ��̂ɓ��������l�ɂ͑�ʃ��^�[���ŕs����������
	$$ref_ceil = int(rand(5000000) + 2500000);
	$$ref_log .= "get_prize:$prize";
	return "��� $jp �� $prize ���l�����܂���<br>";
}

sub view_log {
	open my $fh, "< ${this_file}_log.cgi" or &error('���ް̧�ق��J���܂���'); 
	while (my $line = <$fh>) {
		$mes .= "$line<br>";
	}
	close $fh;
	return '';
}

1;#�폜�s��
