#================================================
# ���l�̂��X Created by Merino
#================================================
require "$datadir/buyable.cgi";

# �S�����̍s���p�֐�
sub is_rest { return $m{lib_r} eq 'shopping_akindo'; } # �S�����̍s����
sub set_tp { (&is_rest ? $m{tp_r} : $m{tp}) = shift; } # �S�����E��S������tp����
sub get_tp { return &is_rest ? $m{tp_r} : $m{tp}; } # �S�����E��S�����̹ޯ��
sub refresh_r { $m{lib_r} = $m{tp_r} = ''; } # refresh�̍S������

# �S�����Ɠ����s�����S�����ɂ����ꍇ�A�S�����̕���ݾ�
&refresh_r if $m{lib_r} eq $m{lib};

my $mobile_max = 50;

sub begin {
	$layout = 2;
#	&confiscate_shop(1);
#	&confiscate_shop(2);

	&set_tp(1) if &get_tp > 1;

	$mes .= "�ǂ̂��X�Ŕ������܂���?<br>";
	$mes .= qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
	$mes .= qq|<input type="radio" id="total_list" name="cmd" value="total_list"><label for="total_list">���i�ꗗ</label><br>|;

	my $count = 0;
	$mes .= qq|<table class="table1"><tr><th>�X��</th><th>�X��</th><th>�Љ</th></tr>| unless $is_mobile;

	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;

		# ���i���Ȃ��X�͔�\��
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";

		my $gc = "#ffffff";
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name"><font color="$gc">$shop_name</font><br>|
			 : qq|<tr><td><label><input type="radio" name="cmd" value="$name"><font color="$gc">$shop_name</font></label></td><td>$name</td><td>$message<br></td></tr>|;
		$count++;
	}
	close $fh;

	$m{stock} = $count;

	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���X�ɓ���" class="button1"></p></form>|;
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
	if ($cmd eq 'total_list') {
		&set_tp(200);
		&menu('����Ȃ�','�������ȉ�');
		return;
	}

	$layout = 2;

	my $shop_id = unpack 'H*', $y{name};

	my $shop_message = '';
	my $is_find = 0;
	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��J���܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		if ($y{name} eq $name) {
			$is_find = 1;
			$m{stock} = $shop_name;
			$shop_message = $message;
			last;
		}
	}
	close $fh;

	# ���X�����݂��Ȃ�
	if (!$is_find || !-f "$userdir/$shop_id/shop.cgi") {
		$mes .= "$m{stock}�Ƃ������X�͕X���Ă��܂����悤�ł�<br>";
		&begin;
	}
	# �����̂��X�Ŕ������ł��Ă��܂��ƁA�����ݷݸނ����󂵂Ă��܂��̂ŁB
	elsif ($m{name} eq $y{name}) {
		$mes .= "�����̂��X�Ŕ��������邱�Ƃ͂ł��܂���<br>";
		&begin;
	}
	elsif (-s "$userdir/$shop_id/shop.cgi") {
		my $tmp_mes = '';

		$tmp_mes .= qq|�y$m{stock}�z$y{name}�u$shop_message�v<br>|;
		$tmp_mes .= qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
		$tmp_mes .= qq|<table class="table1"><tr><th>���i��</th><th>�l�i<br></th></tr>|;

		my $cnt = 0;
		open my $fh, "< $userdir/$shop_id/shop.cgi" or &error("$y{name}�ɓ���܂���");
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			next if ($price == 5000000);
			$cnt++;
			$tmp_mes .= qq|<tr><td><input type="radio" id="$no" name="cmd" value="$no">|;
			$tmp_mes .= qq|<label for="$no">| unless $is_mobile;
			$tmp_mes .= &get_item_name($kind, $item_no, $item_c, $item_lv, 1); # ��ޔ�\��
			$tmp_mes .= qq|</label>| unless $is_mobile;
			$tmp_mes .= qq|</td><td align="right">$price G<br></td></tr>|;
		}
		close $fh;

		$tmp_mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$tmp_mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;

		if ($cnt) {
			$mes .= $tmp_mes;
			&set_tp(100);
		}
		else {
			$mes .= "$m{stock}�ɂ͏��i���Ȃ��悤�ł�<br>";
			&begin;
		}
	}
	else {
		&begin;
	}
}

#================================================
# ����������
#================================================
sub tp_100 {
	my $shop_id = unpack 'H*', $y{name};
	if ($cmd && -f "$userdir/$shop_id/shop.cgi") {
		my $line = ''; # �������A�C�e����񂪓���
		my @lines = (); # ���̑��̏��i������
		open my $fh, "+< $userdir/$shop_id/shop.cgi" or &error("���iؽĂ��J���܂���");
		eval { flock $fh, 2; };
		while (my $_line = <$fh>) {
			if (index($_line, "$cmd<>") == 0) { $line = $_line; }
			else { push @lines, $_line; }
		}
		if ($line) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			if ($m{money} >= $price) {
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
			}
			close $fh;
			if ($m{money} >= $price) {
				$m{money} -= $price;
				my $item_name = &get_item_name($kind, $item_no);
				$mes .= "$item_name�𔃂��܂���<br>$item_name�͗a���菊�ɑ����܂���<br>";
				my $sell_id = int(rand(1000)+1); # �I�ʌ����Ō������ID�H send_item �ł͔��������t���O�Ƃ����g���ĂȂ�
				&send_item($m{name}, $kind, $item_no, $item_c, $item_lv, $sell_id);
				&send_money($y{name}, "�y$m{stock}($item_name)�z$m{name}", $price, 1);
				&sale_data_log($kind, $item_no, $item_c, $item_lv, $price, 1);

				# ��������Z
				open my $fh2, "+< $userdir/$shop_id/shop_sale.cgi" or &error("����̧�ق��J���܂���");
				eval { flock $fh2, 2; };
				my $line2 = <$fh2>;
				my($sale_c, $sale_money, $update_t) = split /<>/, $line2;
				$sale_c++;
				$sale_money += $price;
				seek  $fh2, 0, 0;
				truncate $fh2, 0;
				print $fh2 "$sale_c<>$sale_money<>$update_t<>";
				close $fh2;

				# �������
				if(-f "$userdir/$shop_id/shop_sale_detail.cgi"){
					my @sell_detail = ();
					open my $fh3, "+< $userdir/$shop_id/shop_sale_detail.cgi" or &error("����̧�ق��J���܂���");
					eval { flock $fh3, 2; };
					while (my $line3 = <$fh3>){
						last if @sell_detail >= 30;
						push @sell_detail, $line3;
					}
					unshift @sell_detail, "$item_name<>$m{name}<>$time<>\n" if $sell_id; # true �ɂ����Ȃ�Ȃ�
					seek  $fh3, 0, 0;
					truncate $fh3, 0;
					print $fh3 @sell_detail;
					close $fh3;
				}else{
					open my $fh3, "> $userdir/$shop_id/shop_sale_detail.cgi" or &error("����̧�ق��J���܂���");
					print $fh3 "$item_name<>$m{name}<>$time<>\n" if $sell_id; # true �ɂ����Ȃ�Ȃ�
					close $fh3;
				}

				# send_item�̃��M���O�@�\���ĂȂ� �������̂������I�Ȃ̂ł��̂����ړ�
				# �V���b�s���O�����M���O
				open my $fh4, ">> $logdir/shopping_log.cgi";
				print $fh4 "$m{name}<>$y{name}<>$item_name<>$price<>$time\n";
				close $fh4;
			}
			else {
				$mes .= "$y{name}�u����������܂���v<br>";
			}
		}
		else {
			$mes .= "$y{name}�u���̏��i�́A������������؂�Ă��܂��܂����v<br>" ;
			close $fh;
		}

		$cmd = $y{name}; # ���O��cmd�ɓ����&tp_1
		&tp_1;
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin;
	}
}

#================================================
# �ꗗ�\��
#================================================
sub tp_200 {
	$layout = 2;

	my @item_list = ();
	my $num = 0;

	if ($is_mobile) {
		&set_tp(210);
	}
	else {
		&set_tp(1) if &get_tp > 1;
	}

	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display) = split /<>/, $line;
		next if $display ne '1';

		# ���i���Ȃ��X�͔�\��
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";

		if (-s "$userdir/$shop_id/shop.cgi") {
			open my $ifh, "< $userdir/$shop_id/shop.cgi" or &error("$shop_name�̏��i���ǂݍ��߂܂���");
			while (my $iline = <$ifh>) {
				my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $iline;
				next if (($cmd eq '1' && $price > $m{money}) || $price == 5000000);
				$price = 99999999 if $display ne '1';
				$item_no = 42 if ($kind == 2 && $item_no == 53);
				$item_no = 76 if ($kind == 3 && $item_no == 180);
				$item_no = 77 if ($kind == 3 && $item_no == 181);
				$item_no = 194 if ($kind == 3 && $item_no == 195);
				push @item_list, "$kind<>$item_no<>$item_c<>$item_lv<>$price<>$name<>$display<>$guild_number<>\n";
			}
			close $ifh;
		}
	}
	close $fh;

	@item_list = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] || $a->[5] <=> $b->[5]}
					map { [$_, split /<>/ ] } @item_list;

	my ($b_name, $b_kind, $b_item_no) = (-1, -1, -1);
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>���i��</th><th>�X��</th><th>���i</th></tr>|;
	for my $line (@item_list) {
		my($kind, $item_no, $item_c, $item_lv, $price, $name, $display, $guild_number) = split /<>/, $line;
		next if $name eq $b_name && $kind == $b_kind && $item_no == $b_item_no;
		($b_name, $b_kind, $b_item_no) = ($name, $kind, $item_no);
		$num++;
		next if $is_mobile && $num >= $cmd * $mobile_max && $num < ($cmd + 1) * $mobile_max;
		$price = '��\��' if $price == 99999999;

		$mes .= qq|<tr><td>|;
		$mes .= qq|<label>| unless $is_mobile;
		$mes .= qq|<input type="radio" name="cmd" value="$name">|;
		$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv, 1); # ��ޔ�\��
		$mes .= qq|</label>| unless $is_mobile;
		$mes .= qq|</td><td>|;
		$mes .= $is_mobile ? qq|$name| : qq|<font color="#ffffff">$name</font>|;
		$mes .= qq|</td><td>$price</td></tr>|;
	}
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���X�ɓ���" class="button1"></p></form><br>|;

	if ($is_mobile) { # ��׹��p���߰�ެ�
		$mes  .= qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
		my ($prev, $next) = ($cmd-1, $cmd+1);
		$mes .= qq|<option value="$prev">�O��</option>|;
		$mes .= qq|<option value="$next">����</option>|;
		$mes .= qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="mode" value="list">|;
		$mes .= qq|<br><input type="submit" value="�� ��" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
	}
}

sub tp_210 { # ��׹��p���߰�ެ�
	if ($in{mode} eq 'list') {
		&tp_200;
	}
	else {
		&set_tp(1);
		&tp_1;
	}
}

sub is_buyable{
	my ($kind, $item_no) = @_;
	return 1;
	if($m{is_full}){
		if($kind eq '1'){
			for my $i (@full_buyable_wea){
				if($item_no == $i){
					return 1;
				}
			}
			return 0;
		}elsif($kind eq '2'){
			for my $i (@full_buyable_egg){
				if($item_no == $i){
					return 1;
				}
			}
			return 0;
		}else{
			for my $i (@full_buyable_pet){
				if($item_no == $i){
					return 1;
				}
			}
			return 0;
		}
	}
	return 1;
}

1; # �폜�s��
