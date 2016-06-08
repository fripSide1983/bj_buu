#================================================
# ���l�̂��X Created by Merino
#================================================
$script_r = 'bj_rest_shop.cgi';
require "$datadir/buyable.cgi";
my $this_file_a = "$logdir/auction.cgi";

my $mobile_max = 50;

sub begin {
	$layout = 2;
	
	$m{tp_r} = 1 if $m{tp_r} > 1;
	$mes .= "�ǂ̂��X�Ŕ������܂���?<br>";
	
	my $count = 0;
	$mes .= qq|<form method="$method" action="$script_r"><input type="radio" id="no_0" name="cmd" value="total_list" checked><label for="no_0">���i�ꗗ</label><br>|;
	$mes .= qq|<table class="table1"><tr><th>�X��</th><th>�X��</th><th>�Љ<br></th></tr>| unless $is_mobile;

	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		
		# ���i���Ȃ��X�͔�\��
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";

		my $gc = "#ffffff";
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name"><font color="$gc">$shop_name</font><br>|
			 : qq|<tr><td><input type="radio" id="$shop_id" name="cmd" value="$name"><font color="$gc"><label for="$shop_id">$shop_name</label></font></td><td>$name</td><td>$message<br></td></tr>|;
		$count++;
	}
	close $fh;

	$m{stock} = $count;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���X�ɓ���" class="button1"></p></form>|;
	$mes .= qq|<br><form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="��߂�" class="button1"></p></form>|;
	
	$mes .= qq|<form method="$method" action="$script_r">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="hidden" name="cmd" value="shop_auction">|;
	$mes .= qq|<p><input type="submit" value="�����݉��" class="button1"></p></form>|;
}

#================================================
# ���X�̏��i�ꗗ�\��
#================================================
sub tp_1 {
	$layout = 2;
	$y{name} = $cmd;
	if ($cmd eq '') {
		&begin;
		return;
	}
	if ($cmd eq 'total_list') {
		$m{tp_r} = $is_mobile ? 300:200;
		if($is_smart){
			$mes .= qq|<table boder=0 cols=3 width=90 height=90><tr>|;
			$mes .= qq|<td><form method="$method" action="$script_r">|;
			$mes .= qq|<input type="submit" value="����Ȃ�" class="button1s"><input type="hidden" name="cmd" value="0">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|</form>|;
			$mes .= qq|</td>|;
			$mes .= qq|<td><form method="$method" action="$script_r">|;
			$mes .= qq|<input type="submit" value="�������ȉ�" class="button1s"><input type="hidden" name="cmd" value="1">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|</form>|;
			$mes .= qq|</td>|;
			$mes .= qq|</tr>|;
			$mes .= qq|</table>|;
		}else{
			$mes  = qq|<form method="$method" action="$script_r"><select name="cmd" class="menu1">|;
			$mes .= qq|<option value="0">����Ȃ�</option>|;
			$mes .= qq|<option value="1">�������ȉ�</option>| unless $is_mobile;
			$mes .= qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= $is_mobile ? qq|<br><input type="submit" value="�� ��" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<br><input type="submit" value="�� ��" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
		}
		return;
	}
	if ($cmd eq 'shop_auction') {
		$m{tp_r} = 400;
		&{ 'tp_'. $m{tp_r} };
		return;
	}
	
	my $shop_id = unpack 'H*', $y{name};
	
	my $shop_message = '';
	my $is_find = 0;
	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��J���܂���');
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
		$mes .= qq|�y$m{stock}�z$y{name}�u$shop_message�v<br>|;
		$mes .= qq|<form method="$method" action="$script_r"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
		$mes .= qq|<table class="table1"><tr><th>���i��</th><th>�l�i<br></th></tr>|;
		
		open my $fh, "< $userdir/$shop_id/shop.cgi" or &error("$y{name}�ɓ���܂���");
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			next if ($price == 5000000);
			$mes .= qq|<tr><td><input type="radio" id="$no" name="cmd" value="$no">|;
			$mes .= qq|<label for="$no">| unless $is_mobile;
			$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv, 1); # ��ޔ�\��
			$mes .= qq|</label>| unless $is_mobile;
			$mes .= qq|</td><td align="right">$price G<br></td></tr>|;
		}
		close $fh;
		
		$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
		$m{tp_r} = 100;
	}
	else {
#		$mes .= "�y$cmd�z������<br>";
		&begin;
	}
}

#================================================
# ����������
#================================================
sub tp_100 {
	my $shop_id = unpack 'H*', $y{name};
	if ($cmd && -f "$userdir/$shop_id/shop.cgi") {
		my $is_find    = 0;
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $userdir/$shop_id/shop.cgi" or &error("���iؽĂ��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			
			if ($cmd eq $no) {
				$is_find = 1;

				if ($m{money} >= $price && &is_buyable($kind, $item_no)) {
					$m{money} -= $price;
					
					my $item_name = &get_item_name($kind, $item_no); # �A�C�e�����̂�
					$mes .= "$item_name�𔃂��܂���<br>$item_name�͗a���菊�ɑ����܂���<br>";
					my $sell_id = int(rand(1000)+1);
					
					&send_item($m{name}, $kind, $item_no, $item_c, $item_lv, $sell_id);
					&send_money($y{name}, "�y$m{stock}($item_name)�z$m{name}", $price, 1);
					&sale_data_log($kind, $item_no, $item_c, $item_lv, $price, 1);
					$is_rewrite = 1;

					# �V���b�s���O�����M���O
					my $ltime = time();
					open my $fh, ">> $logdir/shopping_log.cgi";
					print $fh "$m{name}<>$y{name}<>$item_name<>$price<>$ltime\n";
					close $fh;

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
						open my $fh3, "+< $userdir/$shop_id/shop_sale_detail.cgi" or &error("����̧�ق��J���܂���");
						while (my $line3 = <$fh3>){
							last if @sell_detail >= 30;
							push @sell_detail, $line3;
						}
						unshift @sell_detail, "$item_name<>$m{name}<>$time<>\n" if $sell_id;
						seek  $fh3, 0, 0;
						truncate $fh3, 0;
						print $fh3 @sell_detail;
						close $fh3;
					}else{
						open my $fh3, "> $userdir/$shop_id/shop_sale_detail.cgi" or &error("����̧�ق��J���܂���");
						print $fh3 "$item_name<>$m{name}<>$time<>\n" if $sell_id;
						close $fh3;
					}
				}
				else {
					$mes .= "$y{name}�u����������܂���v<br>";
					last;
				}
			}
			else {
				push @lines, $line;
			}
		}
		if ($is_rewrite) {
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
		}
		close $fh;
		
		unless ($is_find) {
			$mes .= "$y{name}�u���̏��i�́A������������؂�Ă��܂��܂����v<br>" ;
		}
		$cmd = $y{name}; # ���O��cmd�ɓ����&tp_1
		&tp_1;
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin
	}
}


#================================================
# �ꗗ�\��
#================================================

sub tp_200 {
	$layout = 2;

	$m{tp_r} = 1 if $m{tp_r} > 1;

	my @item_list = ();
	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		next if ($display ne '1' && $in{d_flag} ne '1');

		# ���i���Ȃ��X�͔�\��
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";

		if (-s "$userdir/$shop_id/shop.cgi") {
			open my $ifh, "< $userdir/$shop_id/shop.cgi" or &error("$shop_name�̏��i���ǂݍ��߂܂���");
			while (my $iline = <$ifh>) {
				my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $iline;
				$item_no = 42 if ($kind == 2 && $item_no == 53);
				$item_no = 76 if ($kind == 3 && $item_no == 180);
				$item_no = 77 if ($kind == 3 && $item_no == 181);
				$item_no = 194 if ($kind == 3 && $item_no == 195);
				next if (($cmd eq '1' && $price > $m{money}) || $price == 5000000);
				push @item_list, "$kind<>$item_no<>$item_c<>$item_lv<>$price<>$name<>$display<>$guild_number<>\n";
			}
			close $ifh;
		}
	}
	close $fh;
	
	@item_list = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] || $a->[5] <=> $b->[5]}
					map { [$_, split /<>/ ] } @item_list;
	
	$mes .= qq|<form method="$method" action="$script_r"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
	$mes .= qq|<table class="table1"><tr><th>���i��</th><th>�X��</th><th>���i<br></th></tr>|;
	my $b_name = -1;
	my $b_kind = -1;
	my $b_item_no = -1;
	for my $line (@item_list) {
		my($kind, $item_no, $item_c, $item_lv, $price, $name, $display, $guild_number) = split /<>/, $line;
		if($name eq $b_name && $kind == $b_kind && $item_no == $b_item_no){
			next;
		}
		my $gc = "#ffffff";
		$mes .= qq|<tr><td><input type="radio" id="$name$item_no" name="cmd" value="$name">|;
		$mes .= qq|<label for="$name$item_no">| unless $is_mobile;
		$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv, 1); # ��ޔ�\��
		$price = '��\��' if $price == 99999999;
		$mes .= qq|</label>| unless $is_mobile;
		$mes .= qq|</td><td><font color="$gc">$name</font></td><td>$price<br></td></tr>|;
		$b_name = $name;
		$b_kind = $kind;
		$b_item_no = $item_no;
	}
	$mes .= qq|</table>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���X�ɓ���" class="button1"></p></form>|;
}


sub tp_300 {#mobile

	$layout = 2;
	$m{tp_r} = 310;
	my $num = 0;
	my @item_list = ();
	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display) = split /<>/, $line;
		
		# ���i���Ȃ��X�͔�\��
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";

		if (-s "$userdir/$shop_id/shop.cgi") {
			open my $ifh, "< $userdir/$shop_id/shop.cgi" or &error("$shop_name�̏��i���ǂݍ��߂܂���");
			while (my $iline = <$ifh>) {
				my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $iline;
				next if ($price == 5000000);
				$price = 99999999 if $display ne '1';
				$item_no = 42 if ($kind == 2 && $item_no == 53);
				$item_no = 76 if ($kind == 3 && $item_no == 180);
				$item_no = 77 if ($kind == 3 && $item_no == 181);
				$item_no = 194 if ($kind == 3 && $item_no == 195);
				push @item_list, "$kind<>$item_no<>$item_c<>$item_lv<>$price<>$name<>\n";
			}
			close $ifh;
		}
	}
	close $fh;

	@item_list = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] || $a->[5] <=> $b->[5]}
					map { [$_, split /<>/ ] } @item_list;
	
	$mes .= qq|<form method="$method" action="$script_r"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>���i��</th><th>�X��</th><th>���i<br></th></tr>|;
	my $b_name = -1;
	my $b_kind = -1;
	my $b_item_no = -1;
	for my $line (@item_list) {
		my($kind, $item_no, $item_c, $item_lv, $price, $name, $display) = split /<>/, $line;
		if($name eq $b_name && $kind == $b_kind && $item_no == $b_item_no){
			next;
		}
		$num++;
		if ($num >= $cmd * $mobile_max && $num < ($cmd + 1) * $mobile_max){
			$mes .= qq|<tr><td><input type="radio" name="cmd" value="$name">|;
			$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv, 1); # ��ޔ�\��
			$price = '��\��' if $price == 99999999;
			$mes .= qq|</td><td>$name</td><td>$price<br></td></tr>|;
		}
		$b_name = $name;
		$b_kind = $kind;
		$b_item_no = $item_no;
	}
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���X�ɓ���" class="button1"></p></form><br>|;

	$mes  .= qq|<form method="$method" action="$script_r"><select name="cmd" class="menu1">|;
	$pre = $cmd-1;
	$nex = $cmd+1;
	$mes .= qq|<option value="$pre">�O��</option>|;
	$mes .= qq|<option value="$nex">����</option>|;
	$mes .= qq|</select><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="mode" value="list">|;
	$mes .= qq|<br><input type="submit" value="�� ��" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
}

sub tp_310 {
    if($in{mode} eq 'list'){
    		 &tp_300;
    }else {
    	  $m{tp_r} = 1;
    	  &tp_1;
    }
}

#================================================
# ������
#================================================

sub tp_400 {
	# ���D����(��)
	my $auction_limit_day = 3;

	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�̕��͂��f�肵�Ă��܂�<br>";
		&begin;
		return;
	}
	
	$layout = 1;
	
	$mes .= qq|�����݂̗��D�����́A�o�i������ $auction_limit_day���O��ł�<br>|;
	$mes .= qq|<form method="$method" action="$script_r">|;
	$mes .= qq|<input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
 	$mes .= $is_mobile ? qq|<hr>���D�i/���D�z/���D��/�o�i��/�Œ���D�z<br>|
 		: qq|<table class="table1" cellpadding="3"><tr><th>���D�i</th><th>���D�z</th><th>�����z</th><th>���D��</th><th>�o�i��</th><th>���</th><th>�Œ���D�z<br></th>|;

	open my $fh, "< $this_file_a" or &error("$this_file_a���ǂݍ��߂܂���");
	$m{total_auction} = 0;
	while (my $line = <$fh>) {
		my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price, $buyout_price) = split /<>/, $line;
		my $item_title = &get_item_name($kind, $item_no, $item_c, $item_lv);
		my $item_state = $time + 3600 * 24 > $bit_time ? "���낻��":
						$time + ($auction_limit_day - 1) * 3600 * 24 > $bit_time ? "�܂��܂�":"new";
		unless($buyout_price){
			$buyout_price = '�Ȃ�';
		}
		my $next_min_price = int($item_price * 1.2);
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$item_title/$item_price G/��$buyout_price G/$to_name/$from_name/$item_state/$next_min_price<br>|
			: qq|<tr><td><input type="radio" id="$no" name="cmd" value="$no"><label for="$no">$item_title</label></td><td align="right">$item_price G</td><td align="right">$buyout_price G</td><td>$to_name</td><td>$from_name</td><td>$item_state</td><td>$next_min_price<br></td></tr>|;
		$m{total_auction} += $item_price if($to_name eq $m{name} && $from_name ne $m{name});
	}
	close $fh;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<p>���D���z�F<input type="text" name="money" value="0" class="text_box1" style="text-align:right" class="text1">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���D����" class="button1"></p></form>|;
	
	$m{tp_r} += 10;
}

sub tp_410 {
	$in{money} = int($in{money});
	if ($m{money} < $in{money} + $m{total_auction}) {
		$mes .= '����Ȃɂ����������Ă��܂���<br>';
	}
	elsif ($cmd && $in{money} && $in{money} !~ /[^0-9]/) {
		my $is_rewrite = 0;
		my $is_sokketsu = 0;
		my @lines = ();
		open my $fh, "+< $this_file_a" or &error("$this_file_a���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price, $buyout_price) = split /<>/, $line;
			if ($no eq $cmd) {
				my $need_money = int($item_price * 1.2);
				if ($buyout_price && $need_money > $buyout_price) {
					$need_money = $buyout_price
				}
				if ( $in{money} >= $need_money && &is_buyable($kind, $item_no) ) {
					my $item_title = &get_item_name($kind, $item_no, $item_c, $item_lv);
					
					$m{total_auction} += $in{money};
					$mes .= "$item_title�� $in{money} G�œ��D���܂���<br>";
					if($buyout_price && $in{money} >= $buyout_price){
						my $to_id = unpack 'H*', $m{name};
						if(-e "$userdir/$to_id/user.cgi"){
							&send_item($m{name}, $kind, $item_no, $item_c, $item_lv, 1);
						}
						&send_money($m{name}, '�����݉��', "-$in{money}");
						&send_money($from_name, '�����݉��', $in{money});
						&sale_data_log($kind, $item_no, $item_c, $item_lv, $in{money}, 3);
						$mes .= "�������i��񎦂��܂���<br>";
						&write_send_news("$from_name�̏o�i����$item_title��$m{name}�� $in{money} G(����)�ŗ��D���܂���");
						&send_twitter("$from_name�̏o�i����$item_title��$m{name}�� $in{money} G(����)�ŗ��D���܂���");
						$is_sokketsu = 1;
						$is_rewrite = 1;
					}else{
						$line = "$bit_time<>$no<>$kind<>$item_no<>$item_c<>$item_lv<>$from_name<>$m{name}<>$in{money}<>$buyout_price<>\n";
						$is_rewrite = 1;
					}
				}
				else {
					$mes .= "���D�͌��݂̗��D�z��1.2�{�ȏ�̋��z( $need_money G)���K�v�ł�<br>";
				}
				unless($is_sokketsu){
					push @lines, $line;
				}
			}
			# ���D����
			elsif ($time > $bit_time) {
				my $item_title = &get_item_name($kind, $item_no, $item_c, $item_lv);
				
				my $to_id = unpack 'H*', $to_name;
				if(-e "$userdir/$to_id/user.cgi"){
					&send_item($to_name, $kind, $item_no, $item_c, $item_lv, 1);
				}
				&send_money($to_name, '�����݉��', "-$item_price");
				&send_money($from_name, '�����݉��', $item_price);
				&sale_data_log($kind, $item_no, $item_c, $item_lv, $item_price, 2);
				&write_send_news("$from_name�̏o�i����$item_title��$to_name�� $item_price G�ŗ��D���܂���");
				&send_twitter("$from_name�̏o�i����$item_title��$to_name�� $item_price G�ŗ��D���܂���");
				$is_rewrite = 1;
			}
			else {
				push @lines, $line;
			}
		}
		if ($is_rewrite) {
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
		}
		close $fh;
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
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
