$mes .= qq|��� $m{coin} ��<br>| if ($is_mobile || $is_smart);
#================================================
# ��@�J�W�m
#================================================
require "$datadir/slots.cgi";

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�̕��͏o����֎~�ł�<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ��J���Ă���ꍇ�͍s���Ȃ�
		return 0;
	}
	return 1;
}

sub begin {
	$layout = 2;
	
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= "�ǂ̶��ɂőł��܂���?<br>";
	
	my $count = 0;
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>�X��</th><th>�X��</th><th>�Љ<br></th></tr>| unless $is_mobile;

	open my $fh, "< $logdir/shop_list_casino.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
		# ���i���Ȃ��X�͔�\��
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop_casino.cgi";
		
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name">$shop_name<br>|
			 : qq|<tr><td><input type="radio" name="cmd" value="$name">$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
		$count++;
	}
	close $fh;

	$m{stock} = $count;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���ɂɓ���" class="button1"></p></form>|;
}

#================================================
# ���X�̏��i�ꗗ�\��
#================================================
sub tp_1 {
	$y{name} = $cmd;
	if ($cmd eq '') {
		&begin;
		return;
	}
	
	$layout = 2;
	my $shop_id = unpack 'H*', $y{name};
	
	my $shop_message = '';
	my $is_find = 0;
	open my $fh, "< $logdir/shop_list_casino.cgi" or &error('�����ؽ�̧�ق��J���܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		if ($y{name} eq $name) {
			$is_find = 1;
			$m{stock} = $shop_name;
			$shop_message = $message;
			last;
		}
	}
	close $fh;

	# ���X�����݂��Ȃ�
	if (!$is_find || !-f "$userdir/$shop_id/shop_casino.cgi") {
		$mes .= "$m{stock}�Ƃ������X�͕X���Ă��܂����悤�ł�<br>";
		&begin;
	}
	# �����̂��X�Ŕ������ł��Ă��܂��ƁA�����ݷݸނ����󂵂Ă��܂��̂ŁB
	elsif ($m{name} eq $y{name}) {
		$mes .= "�����̂��X�Ŕ��������邱�Ƃ͂ł��܂���<br>";
		&begin;
	}
	elsif (-s "$userdir/$shop_id/shop_casino.cgi") {
		$mes .= qq|�y$m{stock}�z$y{name}�u$shop_message�v<br>|;
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
		$mes .= qq|<table class="table1"><tr><th>��</th><th>���[�g<br></th></tr>|;
		
		open my $fh, "< $userdir/$shop_id/shop_casino.cgi" or &error("$y{name}�ɓ���܂���");
		while (my $line = <$fh>) {
			my($no, $slot_no, $ratio, $profit) = split /<>/, $line;
			$mes .= qq|<tr><td><input type="radio" name="cmd" value="$no">$slots[$slot_no][1]</td><td align="right">$ratio ���<br></td></tr>|;
		}
		close $fh;
		
		$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="�ł�" class="button1"></p></form>|;
		$m{tp} = 100;
	}
	else {
		&begin;
	}
}

#================================================
# ���ɊJ�n����
#================================================
sub tp_100 {
	my $shop_id = unpack 'H*', $y{name};
	if ($cmd && -f "$userdir/$shop_id/shop_casino.cgi") {
		open my $fh, "< $userdir/$shop_id/shop_casino.cgi" or &error("���iؽĂ��J���܂���");
		while (my $line = <$fh>) {
			my($no, $slot_no, $ratio, $profit) = split /<>/, $line;
			
			if ($cmd eq $no) {
				$y{cha} = 0;
				$y{lea} = $slot_no;
				$y{wea} = $ratio;
				$y{ag} = $profit;
				$m{tp} = 110;
				&menu('Play', '��߂�');
			}
		}
		close $fh;
	} else {
		$mes .= '��߂܂���<br>';
		&begin
	}
}

sub tp_110 {
	&{ $slots[$y{lea}][4][$y{cha}] };
}

1; # �폜�s��
