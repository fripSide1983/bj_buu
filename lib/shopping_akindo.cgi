#================================================
# ���l�̂��X Created by Merino
#================================================
require "$datadir/buyable.cgi";

sub begin {
	$layout = 2;
#	&confiscate_shop(1);
#	&confiscate_shop(2);
	
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= "�ǂ̂��X�Ŕ������܂���?<br>";
	
	my $count = 0;
	$mes .= qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
	$mes .= qq|<input type="radio" id="total_list" name="cmd" value="total_list"><label for="total_list">���i�ꗗ</label><br>| unless $is_mobile;
	$mes .= qq|<table class="table1"><tr><th>�X��</th><th>�X��</th><th>�Љ</th></tr>| unless $is_mobile;
	
	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		
		# ���i���Ȃ��X�͔�\��
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop.cgi";
		
		my $gc = "#ffffff";
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name"><font color="$gc">$shop_name</font><br>|
			 : qq|<tr><td><input type="radio" id="$name" name="cmd" value="$name"><font color="$gc"><label for="$name">$shop_name</label></font></td><td>$name</td><td>$message<br></td></tr>|;
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
		$m{tp} = 200;
		&menu('����Ȃ�','�������ȉ�');
		return;
	}
	
	$layout = 2;
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
		$mes .= qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
		$mes .= qq|<table class="table1"><tr><th>���i��</th><th>�l�i<br></th></tr>|;
		
		open my $fh, "< $userdir/$shop_id/shop.cgi" or &error("$y{name}�ɓ���܂���");
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			next if ($price == 5000000);
			$mes .= qq|<tr><td><input type="radio" id="$no" name="cmd" value="$no">|;
			$mes .= qq|<label for="$no">| unless $is_mobile;
			$mes .= $kind eq '1' ? "$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
				  : $kind eq '2' ? "$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
				  : $kind eq '3' ? "$pets[$item_no][1]��$item_c"
				  : 			   "$guas[$item_no][1]"
				  ;
			$mes .= qq|</label>| unless $is_mobile;
			$mes .= qq|</td><td align="right">$price G<br></td></tr>|;
		}
		close $fh;
		
		$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
		$m{tp} = 100;
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
					
					my $item_name = $kind eq '1' ? $weas[$item_no][1]
								  : $kind eq '2' ? $eggs[$item_no][1]
								  : $kind eq '3' ? $pets[$item_no][1]
								  :				   $guas[$item_no][1]
								  ;
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
					my @sell_detail = ();
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

	$m{tp} = 1 if $m{tp} > 1;

	my @item_list = ();
	open my $fh, "< $logdir/shop_list.cgi" or &error('�����ؽ�̧�ق��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		next if $display ne '1';

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
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
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
		$mes .= $kind eq '1' ? "$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
			  : $kind eq '2' ? "$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
			  : $kind eq '3' ? "$pets[$item_no][1]��$item_c"
			  : 			   "$guas[$item_no][1]"
			  ;
		$price = '��\��' if $price == 99999999;
		$mes .= qq|</label>| unless $is_mobile;
		$mes .= qq|</td><td><font color="$gc">$name</font></td><td>$price<br></td></tr>|;
		$b_name = $name;
		$b_kind = $kind;
		$b_item_no = $item_no;
	}
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���X�ɓ���" class="button1"></p></form>|;
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
