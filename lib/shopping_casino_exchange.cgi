$mes .= qq|��� $m{coin} ��<br>| if $is_mobile;
#================================================
# ���Ɍ����� Created by Merino
#================================================

# �l�グ��
my $price_up = 0.1;

# �����ܕi
my @prizes = (
# ��� 1=����,2=��,3=�߯� 
#	[0]���,[1]No,[2]����,[3]���̑��׸�
	[0,	0,	0,		0,	0,],
	[2,	22,	1000,	0,	0,],
	[2,	24,	3000,	0,	0,],
	[2,	16,	5000,	0,	0,],
	[2,	51,	5000,	0,	0,],
	[2,	23,	5000,	0,	0,],
	[1,	2,	10000,	0,	0,],
	[1,	7,	10000,	0,	0,],
	[1,	22,	10000,	0,	0,],
	[2,	25,	20000,	0,	0,],
	[3,	126,40000,	0,	100,],
	[3,	197,40000,	0,	100,],
	[2,	3,	100000,	0,	30,],
	[2,	2,	200000,	0,	10,],
	[2,	54,	2500000,1,	5,],
);


#================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�͂��f�肾<br>";
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ�������܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�����́A�莝���̂�����݂Ɍ���������<br>';
		$mes .= '��݂Əܕi�̌��������邱�Ƃ��ł��܂�<br>';
		$mes .= '�ǂ����܂����H<br>';
	}
	&menu('��߂�','��݂Ɍ���','�ܕi�ƌ���');
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#=================================================
# ��������݂Ɍ���
#=================================================
sub tp_100 {
	$layout = 1;
	
	$mes .= "$m{name}�l�ͺ�݂�$m{coin}���������ł�<br>";
	$mes .= '���1��20G�ł�<br>�����炨���߂ł���?<br>';
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="coin" value="0" class="text_box1" style="text-align:right">��|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_110 {
	if ($in{coin} && $in{coin} !~ /[^0-9]/) {
		my $v = int($in{coin} * 20);
		if ($m{money} >= $v) {
			$m{money} -= $v;
			$m{coin}  += $in{coin};
			$mes .= "$v G��� $in{coin} ���Ɍ������܂���<br>";
		}
		else {
			$mes .= '����������܂���<br>';
		}
	}
	&begin;
}


#=================================================
# ��݁��ܕi�Ɍ���
#=================================================
sub tp_200 {
	$layout = 1;
	
	$mes .= "$m{name}�l�ͺ�݂�$m{coin}���������ł�<br>";
	$mes .= "�ǂ̏ܕi�ƌ������܂���?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1"><tr><th>�ܕi</th><th>�K�v���<br></th></tr>|;
	$mes .= qq|<tr><td colspan="2"><input type="radio" name="cmd" value="0" checked> ��߂�<br></td></tr>|;
	for my $i (1 .. $#prizes) {
		$mes .= qq|<tr><td><input type="radio" name="cmd" value="$i"> |;
		$mes .= $prizes[$i][0] eq '1' ? qq|[$weas[ $prizes[$i][1] ][2]]$weas[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '2' ? qq|[��]$eggs[ $prizes[$i][1] ][1]</td>|
			  : 						qq|[�y]$pets[ $prizes[$i][1] ][1]</td>|
			  ;
		my $price = &modified_price($i);
		if($prizes[$i][3]){
			$mes .= qq|<td align="right">$price���+���������ׂ�(4999999G�ȏ�)<br></td></tr>|;
		}else{
			$mes .= qq|<td align="right">$price���<br></td></tr>|;
		}
	}
	$mes .= qq|</table>|;
	$mes .= qq|<p>�~<input type="text" name="loop" value="1" class="text_box1" style="text-align:right"></p>|;
	$mes .= qq|<p><input type="submit" value="��������" class="button1"></p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"></form>|;
	$m{tp} += 10;
}
sub tp_210 {
	if ($in{loop} && $in{loop} !~ /[^0-9]/ && $in{loop} < 300) {
		for my $loop (1..$in{loop}) {
			if ($cmd) {
				for my $i (1 .. $#prizes) {
					next unless $cmd eq $i;
					
					my $other_flag = 0;
					my $total_money = $m{money};
					if($m{bank} && -f "$userdir/$shop_id/shop_bank.cgi"){
						my $shop_id = unpack 'H*', $m{bank};
						open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgi̧�ق��J���܂���");

						my $head_line = <$fh>;
						my $v;
						while (my $line = <$fh>) {
							my($year, $name, $money) = split /<>/, $line;

							if ($m{name} eq $name) {
								$total_money += $money;
							}
						}
						close $fh;
					}
					if($total_money >= 4999999){
						$other_flag = 1;
					}
					unless($prizes[$i][3]){
						$other_flag = 1;
					}
					
					my $price = &modified_price($i);
					if ($m{coin} >= $price && $other_flag) {
						$m{coin} -= $price;
						&count_up_exchange($i);
						if($prizes[$i][3]){
							$m{money} = 0;
							if($m{bank}){
								my $shop_id = unpack 'H*', $m{bank};
								my $is_rewrite = 0;
								my @lines = ();
								open my $fh, "+< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgi̧�ق��J���܂���");
								eval { flock $fh, 2; };

								my $head_line = <$fh>;
								push @lines, $head_line;
								while (my $line = <$fh>) {
									my($year, $name, $money) = split /<>/, $line;

									if ($m{name} eq $name) {
										$is_rewrite = 1;
									} else {
										push @lines, $line;
									}
								}
								if ($is_rewrite) {
									seek  $fh, 0, 0;
									truncate $fh, 0;
									print $fh @lines;
								}
								close $fh;
								$m{bank} = '';
							}
						}
						if ($prizes[$i][0] eq '1') {
							$mes .= "$weas[ $prizes[$i][1] ][1]�Ɍ������܂���<br>";
							&send_item($m{name}, $prizes[$i][0], $prizes[$i][1], $weas[ $prizes[$i][1] ][4], 0, 1);
						}
						elsif ($prizes[$i][0] eq '2') {
							$mes .= "$eggs[ $prizes[$i][1] ][1]�Ɍ������܂���<br>";
							&send_item($m{name}, $prizes[$i][0], $prizes[$i][1], 0, 0, 1);
						}
						elsif ($prizes[$i][0] eq '3') {
							$mes .= "$pets[ $prizes[$i][1] ][1]�Ɍ������܂���<br>";
							&send_item($m{name}, $prizes[$i][0], $prizes[$i][1], 0, 0, 1);
						}
					}
					else {
						$mes .= '��݂�����܂���<br>';
					}
					last;
				}
			}
		}
	}
	&begin;
}


#=================================================
# ���i�l�グ
#=================================================
sub modified_price {
	my $item_no = shift;
	
	unless ($m{exchange_count}) {
		my @dummy = ();
		for (0..$#prizes) {
			push @dummy, 0;
		}
		$m{exchange_count} = join ":", @dummy;
	}
	my @counts = split /:/, $m{exchange_count};
	if ($prizes[$item_no][4] && $prizes[$item_no][4] < $counts[$item_no]) {
		return int($prizes[$item_no][2] * (1.0 + $price_up * ($counts[$item_no] - $prizes[$item_no][4])));
	}
	return $prizes[$item_no][2];
}

#=================================================
# �������v��
#=================================================
sub count_up_exchange {
	my $item_no = shift;
	
	unless ($m{exchange_count}) {
		my @dummy = ();
		for (0..$#prizes) {
			push @dummy, 0;
		}
		$m{exchange_count} = join ":", @dummy;
	}
	my @counts = split /:/, $m{exchange_count};
	
	$counts[$item_no]++;
	
	$m{exchange_count} = join ":", @counts;
}

1; # �폜�s��
