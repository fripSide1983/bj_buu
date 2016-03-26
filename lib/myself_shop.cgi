my $this_file       = "$userdir/$id/shop.cgi";
my $shop_list_file  = "$logdir/shop_list.cgi";
my $this_file_detail= "$userdir/$id/shop_sale_detail.cgi";
#================================================
# ���l�̂��X Created by Merino
#================================================

# ���ݔ�p
my $build_money = 100000;

# ���X�ɂ�����ő吔
my $max_shop_item = 20;


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "���ɉ������܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "�����̏��l�̂��X�̐ݒ�����܂�<br>";
		$mes .= "��$sales_ranking_cycle_day���Ԃ��X�̔��オ�Ȃ��Ƃ��X�͎����I�ɕX�ɂȂ�܂�<br>";
	}
	&menu('��߂�','���i�{��', '�X���ɒu��', '���X�̏Љ�', '���X�����Ă�','�X������','����m�F');
}

sub tp_1 {
	return if &is_ng_cmd(1..6);
	
	$m{tp} = $cmd * 100;
	if ($cmd eq '4') {
		if (-f $this_file) {
			$mes .= "���łɎ����̂��X�������Ă��܂�<br>";
			&begin;
		}
		elsif ($jobs[$m{job}][1] ne '���l') {
			$mes .= "�E�Ƃ����l�łȂ��Ƃ��X�����Ă邱�Ƃ��ł��܂���<br>";
			&begin;
		}
		else {
			$mes .= "���X�����Ă�ɂ� $build_money G������܂�<br>";
			$mes .= "�����l�̂��X�ݷݸނ̍X�V���߂����Ɍ��Ă�Ƃ����ɕX���Ă��܂��܂�<br>";
			&menu('��߂�','���Ă�');
		}
	}
	elsif (!-f $this_file) {
		$mes .= '�܂��́A���X�����Ă�K�v������܂�<br>';
		&begin;
	}
	else {
		&{ 'tp_'. $m{tp} };
	}
}

#=================================================
# ����
#=================================================
sub tp_400 {
	if ($cmd eq '1') {
		if (-f $this_file) {
			$mes .= "���łɎ����̂��X�������Ă��܂�<br>";
		}
		elsif ($m{money} >= $build_money) {
			open my $fh, "> $this_file" or &error('���X�����Ă�̂Ɏ��s���܂���');
			close $fh;
			chmod $chmod, "$this_file";
	
			open my $fh2, "> $userdir/$id/shop_sale.cgi" or &error('��ٽ̧�ق��J���܂���');
			print $fh2 "0<>0<>$time<>";
			close $fh2;
			chmod $chmod, "$userdir/$id/shop_sale.cgi";
			
			open my $fh3, ">> $shop_list_file" or &error('���Xؽ�̧�ق��J���܂���');
			print $fh3 "$m{name}�X<>$m{name}<>$date�J�X<>0<>0<>1<>0<>\n";
			close $fh3;
	
			&mes_and_send_news("<b>���l�̂��X�����Ă܂���</b>", 1);
			$mes .= '<br>�����������X�ɏ��i����ׂ܂��傤<br>';
			$m{money} -= $build_money;
			$m{guild_number} = 0;
		}
		else {
			$mes .= '����������܂���<br>';
		}
	}
	&begin;
}

#=================================================
# ���i�{��
#=================================================
sub tp_100 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $last_time = (stat "$userdir/$id/shop_sale.cgi")[9];
	my($min,$hour,$mday,$month) = (localtime($last_time))[1..4];
	++$month;
	open my $fh2, "< $userdir/$id/shop_sale.cgi" or &error("���X̧�ق��ǂݍ��߂܂���");
	my $line = <$fh2>;
	close $fh2;
	my($sale_c, $sale_money, $update_t) = split /<>/, $line;
	$mes .= "�ŏI��������F$month/$mday $hour:$min<br>";
	$mes .= "���݂̔��グ�F$sale_c�� $sale_money G<br>";
	
	$mes .= '<hr>�a���菊�ɖ߂��܂���?<br>';
	$mes .= '���X�̏��i�ꗗ<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1"><tr><th>���i��</th><th>�l�i</th></tr>|;

	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
		$mes .= qq|<tr><td><input type="checkbox" name="cmd_$no" value="1">|;
		$mes .= $kind eq '1' ? "$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
			  : $kind eq '2' ? "$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
			  : $kind eq '3' ? "$pets[$item_no][1]��$item_c"
			  : 			   "$guas[$item_no][1]"
			  ;
		$mes .= qq|</td><td align="right">$price G<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p>�l�i�F<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<p><input type="submit" value="�l�i�ύX" class="button1"></p></form>|;
	
	$m{tp} = 110;
}
sub tp_110 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	my $checked = 0;
	if ($m{is_full} && $in{price} == 0) {
		$mes .= '�a���菊�������ς��ł�<br>';
		&begin;
		return;
	}
	else {
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
			
			if ($in{"cmd_$no"}) {
				$checked = 1;
				if($in{price} == 0){
					      &send_item($m{name}, $kind, $item_no, $item_c, $item_lv);
					      
					      $mes .= $kind eq '1' ? "$weas[$item_no][1]"
					      	   : $kind eq '2' ? "$eggs[$item_no][1]"
					      	   : $kind eq '3' ? "$pets[$item_no][1]"
					  	 	  :		   "$guas[$item_no][1]"
					  	   ;
						   $mes .= '��a���菊�ɖ߂��܂���<br>';
				}elsif ($in{price} =~ /[^0-9]/ || $in{price} <= 0 || $in{price} > 5000000) {
			      	      $mes .= '�l�i�� 1 G �ȏ� 500��0000 G�ȓ��ɂ���K�v������܂�<br>';
			      	      &begin;
			      	      return;
				}else {
				      push @lines, "$no<>$kind<>$item_no<>$item_c<>$item_lv<>$in{price}<>\n";
				}
			}
			else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
	}
	if($checked){
		&tp_100;
	}else{
		&begin;
	}
}

#=================================================
# �X���ɒu��
#=================================================
sub tp_200 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $i = 1;
	
	$mes .= '�ǂ�����X�ɏo���܂���?<br>';
	$mes .= qq|<form method="$method" action="$script"><br>|;

	open my $fh, "< $userdir/$id/depot.cgi" or &error("$userdir/$id/depot.cgi ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;

		$mes .= qq|<input type="checkbox" name="cmd$i" value="1" /><a href="shop_big_data.cgi?item=${kind}_${item_no}" target="_blank">|;
		$mes .= $kind eq '1' ? qq|[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])|
			  : $kind eq '2' ? qq|[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])|
			  : $kind eq '3' ? qq|[��]$pets[$item_no][1]��$item_c|
			  :				   qq|[$guas[$item_no][2]]$guas[$item_no][1]|
			  ;
		++$i;
		$mes .= qq|</a><br>|;
	}
	close $fh;
	$mes .= qq|<p>�l�i�F<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���X�ɒu��" class="button1"></p></form>|;
	
	$m{tp} = 210;
}
sub tp_210 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	my $put = 0;
	my @shop_items = ();
	open my $in, "< $this_file" or &error("$this_file���ǂݍ��߂܂���");
	push @shop_items, $_ while <$in>;
	close $in;
	
	my $item_num = @shop_items;
	if ($item_num >= $max_shop_item) {
		$mes .= '����ȏエ�X�ɏ��i��u�����Ƃ͂ł��܂���<br>';
		&begin;
		return;
	}
	elsif ($in{price} =~ /[^0-9]/ || $in{price} <= 0 || $in{price} > 5000000) {
		$mes .= '�l�i�� 1 G �ȏ� 500��0000 G�ȓ��ɂ���K�v������܂�<br>';
		&begin;
		return;
	}
	
	my @lines = ();
	my $i = 1;
	my($last_no) = (split /<>/, $shop_items[-1])[0];
	open my $fh, "+< $userdir/$id/depot.cgi" or &error("$userdir/$id/depot.cgi ���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if ($in{'cmd' . $i} && $item_num < $max_shop_item) {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			
			++$last_no;
			
			open my $fh2, ">> $this_file" or &error("$this_file���J���܂���");
			print $fh2 "$last_no<>$kind<>$item_no<>$item_c<>$item_lv<>$in{price}<>\n";
			close $fh2;
			
			$mes .= $kind eq '1' ? "$weas[$item_no][1]"
				  : $kind eq '2' ? "$eggs[$item_no][1]"
				  : $kind eq '3' ? "$pets[$item_no][1]��$item_c"
				  :				   "$guas[$item_no][1]"
				  ;
			$mes .= "�� $in{price} G�œX���ɕ��ׂ܂���<br>";
			$item_num++;
			$put = 1;
		}
		else {
			push @lines, $line;
		}
		
		++$i;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	if ($put) {
		&tp_200;
	}
	else {
		&begin;
	}
}

#=================================================
# ���X�̐ݒ�
#=================================================
sub tp_300 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	my $is_find = 0;
	open my $fh, "< $shop_list_file" or &error('���XؽĂ��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display ,$guild_number) = split /<>/, $line;

		if ($name eq $m{name}) {
			$is_find = 1;
			
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|�O��̔���F$sale_c�� $sale_money G<br>|;
			$mes .= qq|<hr>���X�̖��O[�S�p8(���p16)�����܂�]�F<br><input type="text" name="name" value="$shop_name" class="text_box1"><br>|;
			$mes .= qq|�Љ[�S�p20(���p40)�����܂�]�F<br><input type="text" name="message" value="$message" class="text_box_b"><br>|;
			$mes .= qq|<input type="checkbox" name="display" value="1" checked>���i���i���ꗗ�ɏ悹��<br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="�ύX����" class="button1"></p></form>|;
			last;
		}
	}
	close $fh;
	
	# ���X������̂�ؽĂɂȂ��̂͂��������̂ł�����x�ǉ�
	unless ($is_find) {
		open my $fh3, ">> $shop_list_file" or &error('���Xؽ�̧�ق��J���܂���');
		print $fh3 "$m{name}�X<>$m{name}<>$date�J�X<>0<>0<>1<>0<>\n";
		close $fh3;
	}
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	unless ($in{name}) {
		$mes .= '��߂܂���';
		&begin;
		return;
	}
	
	&error('���X�̖��O���������܂��B�S�p8(���p16)�����܂�') if length $in{name} > 16;
	&error('�Љ���������܂��B�S�p20(���p40)�����܂�') if length $in{message} > 40;

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $shop_list_file" or &error('���XؽĂ��J���܂���');
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		
		if ($name eq $m{name}) {
			unless ($shop_name eq $in{name}) {
				$mes .= "���X�̖��O�� $in{name} �ɕς��܂���<br>";
				$shop_name = $in{name};
				$is_rewrite = 1;
			}
			unless ($message eq $in{message}) {
				$mes .= "�Љ�� $in{message} �ɕς��܂���<br>";
				$message = $in{message};
				$is_rewrite = 1;
			}
			unless ($display eq $in{display}) {
				$mes .= "���i���i���ꗗ�ɏ悹�܂���<br>" if $in{display};
				$display = $in{display};
				$is_rewrite = 1;
			}
			
			if ($is_rewrite) {
				unless ($m{guild_number}){
					$m{guild_number} = 0;
				}
				$guild_number = $m{guild_number};
				$line = "$shop_name<>$name<>$message<>$sale_c<>$sale_money<>$display<>$guild_number<>\n";
			}
			else {
				last;
			}
		}
		elsif ($shop_name eq $in{name}) {
			&error("���łɓ������O�̂��X�����݂��܂�");
		}
		push @lines, $line;
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	&begin;
}


#=================================================
# ���X�̐���
#=================================================
sub tp_500 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	my @lines = ();
	my @sub_lines = ();
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	
	while (my $line = <$fh>){
		my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
		$line = "$no<>2<>42.5<>$item_c<>$item_lv<>$price<>\n" if($kind == 2 && $item_no == 53);
		$line = "$no<>3<>76.5<>$item_c<>$item_lv<>$price<>\n" if($kind == 3 && $item_no == 180);
		$line = "$no<>3<>77.5<>$item_c<>$item_lv<>$price<>\n" if($kind == 3 && $item_no == 181);
		push @lines, $line;
	}
	@lines = map { $_->[0] }
				sort { $a->[2] <=> $b->[2] || $a->[3] <=> $b->[3] }
					map { [$_, split /<>/ ] } @lines;
	my $i = 1;
	for my $line (@lines){
		my($no, $kind, $item_no, $item_c, $item_lv, $price) = split /<>/, $line;
		if($kind == 2 && $item_no == 42.5){
			$line = "$i<>2<>53<>$item_c<>$item_lv<>$price<>\n";
		}elsif($kind == 3 && $item_no == 76.5){
			$line = "$i<>3<>180<>$item_c<>$item_lv<>$price<>\n";
		}elsif($kind == 3 && $item_no == 77.5){
			$line = "$i<>3<>181<>$item_c<>$item_lv<>$price<>\n";
		}else {
			$line = "$i<>$kind<>$item_no<>$item_c<>$item_lv<>$price<>\n";
		}
		push @sub_lines, $line;
		$i++;
	}
	
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @sub_lines;
	close $fh;
	
	$mes .= "�X���𐮗����܂���<br>";
	&begin;
}

#=================================================
# ����m�F
#=================================================
sub tp_600 {
	unless (-f $this_file_detail) {
		&begin;
		return;
	}
	
	my @lines = ();
	my @sub_lines = ();
	open my $fh, "< $this_file_detail" or &error("$this_file���J���܂���");
	while (my $line = <$fh>){
		$layout = 2;
		my($item_name, $buyer, $sell_time) = split /<>/, $line;
		my($sell_min,$sell_hour,$sell_mday,$sell_mon,$sell_year) = (localtime($sell_time))[1..4];
		$sell_date = sprintf("%d/%d %02d:%02d", $sell_mon+1,$sell_mday,$sell_hour,$sell_min);
		$mes .= "$item_name�F$buyer������($sell_date)<br>";
	}
	close $fh;
	
	&begin;
}

1; # �폜�s��
