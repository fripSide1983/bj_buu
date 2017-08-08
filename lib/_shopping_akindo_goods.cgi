my $shop_list_file = "$logdir/shop_list_$goods_dir.cgi";
#================================================
# �����̍�i�̂��X Created by Merino
#================================================
# ������CGI�P�̂ł͓����܂��� shopping_akindo_book.cgi,shopping_akindo_picture.cgi���Q��

# �S�����̍s���p�֐�
sub is_rest { return $m{lib_r} eq 'shopping_akindo_book' || $m{lib_r} eq 'shopping_akindo_picture'; } # �S�����̍s����
sub set_tp { (&is_rest ? $m{tp_r} : $m{tp}) = shift; } # �S�����E��S������tp����
sub get_tp { return &is_rest ? $m{tp_r} : $m{tp}; } # �S�����E��S�����̹ޯ��
sub refresh_r { $m{lib_r} = $m{tp_r} = ''; } # refresh�̍S������

# �S�����Ɠ����s�����S�����ɂ����ꍇ�A�S�����̕���ݾ�
&refresh_r if $m{lib_r} eq $m{lib};

#================================================
# ���X�̖��O�ꗗ�\��
#================================================
sub begin {
	$layout = 2;

#	$m{tp} = 1 if $m{tp} > 1;
	&set_tp(1) if &get_tp > 1;
	$mes .= "�ǂ̂��X�Ŕ������܂���?<br>";
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>�X��</th><th>�X��</th><th>�Љ<br></th></tr>| unless $is_mobile;

	open my $fh, "< $shop_list_file" or &error("$shop_list_file ̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
		# ���i���Ȃ��X�͔�\��
		my $shop_id = unpack 'H*', $name;
		next unless -s "$userdir/$shop_id/shop_$goods_dir.cgi";
		
		$mes .= $is_mobile ? qq|<input type="radio" name="cmd" value="$name">$shop_name<br>|
			 : qq|<tr><td><input type="radio" name="cmd" value="$name">$shop_name</td><td>$name</td><td>$message<br></td></tr>|;
	}
	close $fh;
	
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
	
	$layout = 2;
	my $shop_id = unpack 'H*', $y{name};
	
	my $shop_message = '';
	my $is_find    = 0;
	open my $fh, "< $shop_list_file" or &error("$shop_list_file ̧�ق��J���܂���");
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
	if (!$is_find || !-f "$userdir/$shop_id/shop_$goods_dir.cgi") {
		$mes .= "$m{stock}�Ƃ������X�͕X���Ă��܂����悤�ł�<br>";
		&begin;
	}
	# �����̂��X�Ŕ������ł��Ă��܂��ƁA�����ݷݸނ����󂵂Ă��܂��̂ŁB
	elsif ($m{name} eq $y{name}) {
		$mes .= "�����̂��X�Ŕ��������邱�Ƃ͂ł��܂���<br>";
		&begin;
	}
	elsif (-s "$userdir/$shop_id/shop_$goods_dir.cgi") {
		$mes .= qq|�y$m{stock}�z$y{name}�u$shop_message�v<br>|;
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="file_name" value="0" checked>��߂�<br>|;
		$mes .= qq|<table class="table1"><tr><th>���i��</th><th>�l�i<br></th></tr>|;
		
		open my $fh, "< $userdir/$shop_id/shop_$goods_dir.cgi" or &error("$y{name}�ɓ���܂���");
		while (my $line = <$fh>) {
			my($file, $name, $price) = split /<>/, $line;
			
			if ($price > 4999999) {
				$mes .= qq|<tr><td>|;
				$mes .= $goods_type eq 'img'  ? qq|<img src="$userdir/$shop_id/$goods_dir/$file" style="vertical-align:middle;">$name<br>|
					  : $goods_type eq 'html' ? qq|<a href="$userdir/$shop_id/$goods_dir/$file" target="_blank">$name</a><br>|
					  :                         qq|$name<br>|;
					  ;
				$mes .= qq|</td><td align="right">�񔄕i<br></td></tr>|;
			}
			else {
				$mes .= qq|<tr><td><input type="radio" name="file_name" value="$file">|;
				$mes .= $goods_type eq 'img' ? qq|<img src="$userdir/$shop_id/$goods_dir/$file" style="vertical-align:middle;">$name<br>|
					  :                        qq|$name<br>|;
					  ;
				$mes .= qq|</td><td align="right">$price G<br></td></tr>|;
			}
		}
		close $fh;
		
		$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
#		$m{tp} = 100;
		&set_tp(100);
	}
	else {
#		$mes .= "�y$y{name}�z������<br>";
		&begin;
	}
	&n_menu;
}

#================================================
# ����������
#================================================
sub tp_100 {
	my %e2j_goods = (
		picture => 'ϲ�߸��',
		book    => 'ϲ�ޯ�',
		music   => 'ϲЭ��ޯ�',
		etc     => 'ϲ�ľ��',
	);

	my $shop_id = unpack 'H*', $y{name};
	
	if ($in{file_name} && -f "$userdir/$shop_id/shop_$goods_dir.cgi") {
		my $is_find    = 0;
		my $is_rewrite = 0;
		my @lines = ();
		open my $fh, "+< $userdir/$shop_id/shop_$goods_dir.cgi" or &error("$userdir/$shop_id/shop_$goods_dir.cgi ̧�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($file, $name, $price) = split /<>/, $line;
			
			if ($in{file_name} eq $file) {
				# ̧�ق��Ȃ��ꍇ
				unless (-f "$userdir/$shop_id/$goods_dir/$file") {
					$is_rewrite = 1;
					next;
				}

				$is_find = 1;

				if ($m{money} >= $price) {
					$m{money} -= $price;
					
					rename "$userdir/$shop_id/$goods_dir/$file", "$userdir/$id/$goods_dir/$file" or &error("�Ȱя����Ɏ��s���܂���");
					if($goods_type eq 'img' || $goods_type eq 'html'){
				     		my $img_title = $name;
				     		$img_title =~ s/.*��://;
						if($img_title ne $ y{name}){
				     			&send_money($img_title,"��Ŏ����Ƃ���$m{stock}",int($price*0.1));
						}		
					}
					&send_money($y{name}, "�y$m{stock}($name)�z$m{name}", $price, 1);
					$is_rewrite = 1;

					$mes .= "$name�𔃂��܂���<br>$name��$e2j_goods{$goods_dir}�ɑ����܂���<br>";
					
					# ��i��������׸ނ����Ă�
					open my $fh5, "> $userdir/$id/goods_flag.cgi";
					close $fh5;
					
					# ��������Z
					open my $fh2, "+< $userdir/$shop_id/shop_sale_$goods_dir.cgi" or &error("����̧�ق��J���܂���");
					eval { flock $fh2, 2; };
					my $line2 = <$fh2>;
					my($sale_c, $sale_money, $update_t) = split /<>/, $line2;
					$sale_c++;
					$sale_money += $price;
					seek  $fh2, 0, 0;
					truncate $fh2, 0;
					print $fh2 "$sale_c<>$sale_money<>$update_t<>";
					close $fh2;
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
		&begin;
	}
}


1; # �폜�s��
