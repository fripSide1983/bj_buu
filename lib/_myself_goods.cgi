my $this_file      = "$userdir/$id/shop_$goods_dir.cgi";
my $this_path_dir  = "$userdir/$id/$goods_dir";
my $shop_list_file = "$logdir/shop_list_$goods_dir.cgi";
#=================================================
# �����̍�i Created by Merino
#=================================================
# ������CGI�P�̂ł͓����܂��� myself_book.cgi,myself_picture.cgi���Q��

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$m{tp} = 1;
		$mes .= "���ɉ������܂���?<br>";
	}
	else {
		$mes .= "$goods_name�̏��L�͍ő�$max_goods�܂łł�<br>";
	}
	&menu("��߂�", "$goods_name������", "$goods_name���̂Ă�", "$goods_name�𑗂�", "�W���i������", "$goods_name��W������", "���X�̐ݒ�", "���X�����Ă�");
}
sub tp_1 {
	return if &is_ng_cmd(1..7);
	$m{tp} = $cmd * 100;
	
	if ($cmd eq '7') {
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
			&menu("��߂�","���Ă�");
		}
	}
	elsif ( $cmd >= 4 && $cmd <= 6 && !-f $this_file ) {
		$mes .= "�܂��́A���X�����Ă�K�v������܂�<br>";
		&begin;
	}
	else {
		&{ "tp_". $m{tp} };
	}
}

#=================================================
# ��i������
#=================================================
sub tp_100 {
	$layout = 2;
	my $count = 0;
	my $sub_mes .= qq|<form method="$method" action="$script"><hr><input type="radio" name="file_name" value="0" checked>��߂�|;
	opendir my $dh, $this_path_dir or &error("$this_path_dir�ިڸ�؂��J���܂���");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;

		my $file_title = &get_goods_title($file_name);
		$sub_mes .= $goods_type eq 'img'  ? qq|<hr><img src="$this_path_dir/$file_name" style="vertical-align:middle;"> $file_title |
				  : $goods_type eq 'html' ? qq|<li><a href="$this_path_dir/$file_name" target="_blank">$file_title</a>|
				  :                         qq|<li>$file_title|;
				  ;
		$sub_mes .= qq|<input type="radio" name="file_name" value="$file_name">| if $file_name =~ /^_/;
		++$count;
	}
	closedir $dh;
	
	$mes .= qq|���L�� $count / $max_goods��<br>|;
	$mes .= qq|$non_title��$goods_name�����ق����邱�ƂŁA�������著�����肷�邱�Ƃ��ł��܂�<br>|;
	$mes .= qq|<font color="#FF0000">����x�������ق͕ύX���邱�Ƃ��ł��܂���</font><br>|;
	$mes .= qq|$sub_mes<hr>|;
	$mes .= qq|����[�S�p8(���p16)�����܂�]<br><input type="text" name="title" class="text_box1"><br>|;
	$mes .= qq|<input type="checkbox" name="is_ad" value="1">$goods_name���`����($need_ad_money G)<br>|;
	$mes .= qq|<input type="checkbox" name="is_send_public" value="1">$goods_name���f�t�H���g�A�C�R���ɒǉ�����<br>| if $goods_type eq 'img';
	$mes .= qq|<input type="checkbox" name="is_send_library" value="1">$goods_name��}���قɊ񑡂���<br>| if $goods_type eq 'html';
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���ق�����" class="button1"></p></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	if ($in{is_ad} && $m{money} < $need_ad_money) {
		$mes .= "��`��p��������܂���<br>";
	}
	elsif ($in{file_name} =~ /^_/) {
		&error("���ق��L�����Ă�������") unless $in{title};
		&error("���ق���ص��(.)�͎g���܂���") if $in{title} =~ /\./;
		&error("���ق̐擪�ɱ��ްײ�(_)�͎g���܂���") if $in{title} =~ /^_/;
		&error("���������傫�����܂��ő�S�p8(���p16)�����܂�") if length $in{title} > 16;
		
		my $file_title = unpack 'H*', "$in{title} ��:$m{name}";
		$file_title .= $goods_type eq 'img'  ? '.jpeg'
					 : $goods_type eq 'html' ? '.html'
					 :                         '.cgi'
					 ;
		
		&error("���łɓ������O�̍�i�����݂��܂�") if -f "$this_path_dir/$file_title";
		
		if (-f "$this_path_dir/$in{file_name}") {
			rename "$this_path_dir/$in{file_name}", "$this_path_dir/$file_title" or &error("�Ȱя����Ɏ��s���܂���");
			$mes .= "$in{title}�Ƃ������ق����܂���<br>";
			
			# ��`
			if ($in{is_ad}) {
				if    ($goods_dir eq 'picture') { &write_picture_news(qq|$cs{name}[$m{country}]��$m{name}�� <a href="$this_path_dir/$file_title"><img src="$this_path_dir/$file_title" style="vertical-align:middle;" width="25px" heigth="25px"></a>�w$in{title}�x�Ƃ�����i�𔭕\\���܂���|); }
				elsif ($goods_dir eq 'book')    { &write_book_news(qq|$cs{name}[$m{country}]��$m{name}���w$in{title}�x�Ƃ�����i�𔭕\\���܂���|); }
				$mes .= "��i�𔭕\\���܂���<br>";
				$m{money} -= $need_ad_money;
			}elsif($in{is_send_public}){
				my $def_file_title = unpack 'H*', "$time ��:$m{name}";
				rename "$this_path_dir/$file_title", "$icondir/_add_$def_file_title" or &error("�Ȱя����Ɏ��s���܂���");
				$mes .= "�f�t�H���g�A�C�R���ɒǉ����܂���<br>";
			}elsif($in{is_send_library}){
				rename "$this_path_dir/$file_title", "$logdir/library/$file_title" or &error("�Ȱя����Ɏ��s���܂���");
				$mes .= "�}���قɊ񑡂��܂���<br>";
			}
		}
		else {
			$mes .= "�I������$goods_name�����݂��܂���<br>";
		}
	}
	else {
		$mes .= "��߂܂���<br>";
	}
	&begin;
}


#=================================================
# ��i���̂Ă�
#=================================================
sub tp_200 {
	$layout = 2;
	$mes .= qq|�ǂ�$goods_name���̂Ă܂���?<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= &radio_my_goods;
	$mes .= qq|<p><input type="submit" value="�̂Ă�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_210 {
	if ($in{file_name}) {
		my $file_title = &get_goods_title($in{file_name});
		unlink "$this_path_dir/$in{file_name}" or &error("�I������$goods_name($file_title)�����݂��܂���");
		$mes .= qq|$file_title���̂Ă܂���<br>|;

		&remove_shop_goods($in{file_name});
	}
	else {
		$mes .= "��߂܂���<br>";
	}
	&begin;
}

#=================================================
# ��i�𑗂�
#=================================================
sub tp_300 {
	$layout = 2;
	$mes .= "�N�ɂǂ�$goods_name�𑗂�܂���?<br>�����萔���F$need_send_money G<br>���O�萔���F$need_send_money_other G<br>";
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<p>���M��F<input type="text" name="send_name" class="text_box1"></p>|;
	$mes .= &radio_my_goods;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	if (!$in{file_name}) {
		$mes .= "��߂܂���<br>";
		&begin;
		return;
	}
	elsif ($in{file_name} =~ /^_/) {
		$mes .= "$non_title�̍�i�͑��邱�Ƃ��ł��܂���<br>";
		&begin;
		return;
	}
	elsif ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�̕��͑��邱�Ƃ��ł��܂���<br>";
		&begin;
		return;
	}
	elsif ($in{send_name} eq "") {
		$mes .= "����悪�L������Ă��܂���<br>";
		&begin;
		return;
	}

	my $send_id = unpack "H*", $in{send_name};
	my %datas = &get_you_datas($send_id, 1);
	my $pay = $datas{country} eq $m{country} ? $need_send_money : $need_send_money_other;
	
	if ($m{money} < $pay) {
		$mes .= "�X���萔��( $pay G)������܂���<br>";
	}
	elsif (!-f "$this_path_dir/$in{file_name}") {
		$mes .= "�I������$goods_name�͑��݂��܂���<br>";
	}
	elsif (-f "$userdir/$send_id/$goods_dir/$in{file_name}") {
		$mes .= "$datas{name}�͂��łɂ���$goods_name���������Ă��܂�<br>";
	}
	elsif (&my_goods_count("$userdir/$send_id/$goods_dir") >= $max_goods) {
		$mes .= "$in{send_name}�̏����i�������ς��ł�<br>";
	}
	else {
		rename "$this_path_dir/$in{file_name}", "$userdir/$send_id/$goods_dir/$in{file_name}" or &error("$goods_name�𑗂�̂Ɏ��s���܂���");
		my $file_title = &get_goods_title($in{file_name});
		&mes_and_send_news("$datas{name}��$file_title�𑗂�܂���");
		$m{money} -= $pay;

		my $img_title = $file_title;
		$img_title =~ s/.*��://;
		&send_money($img_title,"$file_title�̈�Ŏ����Ƃ��č�",int($pay*0.1));
		
		# ��i��������׸ނ����Ă�
		open my $fh, "> $userdir/$send_id/goods_flag.cgi";
		close $fh;

		&remove_shop_goods($in{file_name});
	}
	
	&begin;
}

#=================================================
# ����
#=================================================
sub tp_700 {
	if ($cmd eq '1') {
		if (-f $this_file) {
			$mes .= "���łɎ����̂��X�������Ă��܂�<br>";
		}
		elsif ($m{money} >= $build_money) {
			open my $fh, "> $this_file" or &error("���X�����Ă�̂Ɏ��s���܂���");
			close $fh;
			chmod $chmod, "$this_file";
	
			open my $fh2, "> $userdir/$id/shop_sale_$goods_dir.cgi" or &error("$userdir/$id/shop_sale_$goods_dir.cgi ̧�ق��J���܂���");
			print $fh2 "0<>1<>";
			close $fh2;
			chmod $chmod, "$userdir/$id/shop_sale_$goods_dir.cgi";
			
			open my $fh3, ">> $shop_list_file" or &error("$shop_list_filȩ�ق��J���܂���");
			print $fh3 "$m{name}�X<>$m{name}<>$date�J�X<>0<>0<>\n";
			close $fh3;
	
			&mes_and_send_news("<b>$goods_name�̂��X�����Ă܂���</b>", 1);
			$mes .= "<br>�����������X�ɍ�i����ׂ܂��傤<br>";
			$m{money} -= $build_money;
		}
		else {
			$mes .= "����������܂���<br>";
		}
	}
	else {
		$mes .= "��߂܂���<br>";
	}
	&begin;
}

#=================================================
# �W���i������
#=================================================
sub tp_400 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	$layout = 2;
	my $last_time = (stat "$userdir/$id/shop_sale_$goods_dir.cgi")[9];
	my($min,$hour,$mday,$month) = (localtime($last_time))[1..4];
	++$month;
	open my $fh2, "< $userdir/$id/shop_sale_$goods_dir.cgi" or &error("$userdir/$id/shop_sale_$goods_dir.cgi̧�ق��ǂݍ��߂܂���");
	my $line = <$fh2>;
	close $fh2;
	my($sale_c, $sale_money) = split /<>/, $line;
	
	$mes .= "�ŏI��������F$month/$mday $hour:$min<br>";
	$mes .= "���݂̔��グ�F$sale_c�� $sale_money G<br>";
	
	$mes .= "<hr>�W������̂���߂܂���?<br>";
	$mes .= "���X�̍�i�ꗗ<br>";

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="file_name" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>����</th><th>�l�i</th></tr>|;

	open my $fh, "< $this_file" or &error("$this_file ̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($file, $name, $price) = split /<>/, $line;
		$mes .= qq|<tr><td><input type="radio" name="file_name" value="$file">$name</td>|;
		$mes .= $price > 4999999 ? qq|<td align="right">�񔄕i($price G)<br></td></tr>| : qq|<td align="right">$price G<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�W������߂�" class="button1"></p></form>|;
	
	$m{tp} = 410;
	&n_menu;
}
sub tp_410 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	if ($in{file_name}) {
		if (&my_goods_count($this_path_dir) >= $max_goods) {
			$mes .= "�����i�������ς��ł�<br>";
			&begin;
		}
		else {
			&remove_shop_goods($in{file_name});
			&tp_400;
		}
	}
	else {
		&begin;
	}
}


#=================================================
# �W������
#=================================================
sub tp_500 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	$layout = 2;
	$mes .= "�ǂ�$goods_name��W���ɏo���܂���?<br>";
	$mes .= "�l�i��500��G�ȏ�ɂ��邱�ƂŔ񔄕i�ɂ��邱�Ƃ��ł��܂�<br>";
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= &radio_my_goods;
	$mes .= qq|<p>�l�i�F<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<p><input type="submit" value="�W������" class="button1"></p></form>|;
	$m{tp} = 510;
	&n_menu;
}
sub tp_510 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	if (!$in{file_name}) {
		$mes .= "��߂܂���<br>";
		&begin;
	}
	elsif ($in{file_name} =~ /^_/) {
		$mes .= "$non_title�̍�i�͓W�����邱�Ƃ��ł��܂���<br>";
		&begin;
	}
	elsif (-f "$this_path_dir/$in{file_name}") {
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($file) = (split /<>/, $line)[0];
			&error("���łɓW������Ă��܂�") if $file eq $in{file_name};
			push @lines, $line;
		}
		
		if (@lines >= $max_shop_item) {
			$mes .= "����ȏエ�X�ɍ�i��W�����邱�Ƃ͂ł��܂���<br>";
			&begin;
			return;
		}
		elsif ($in{price} =~ /[^0-9]/ || $in{price} <= 0) {
			$mes .= "�l�i�� 1 G �ȏ�ɂ���K�v������܂�<br>";
			&begin;
			return;
		}
		
		my $file_title = &get_goods_title($in{file_name});
		unshift @lines, "$in{file_name}<>$file_title<>$in{price}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		$mes .= $in{price} > 4999999 ? "$file_title��񔄕i�Ƃ��ēW�����܂���<br>" : "$file_title�� $in{price} G�œW�����܂���<br>";
		&tp_500;
	}
	else {
		&begin;
	}
}

#=================================================
# ���X�̐ݒ�
#=================================================
sub tp_600 {
	unless (-f $this_file) {
		&begin;
		return;
	}

	my $is_find = 0;
	open my $fh, "< $shop_list_file" or &error("$shop_list_file ̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;

		if ($name eq $m{name}) {
			$is_find = 1;
			
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|�O��̔���F$sale_c�� $sale_money G<br>|;
			$mes .= qq|<hr>���X�̖��O[�S�p8(���p16)�����܂�]�F<br><input type="text" name="name" value="$shop_name" class="text_box1"><br>|;
			$mes .= qq|�Љ[�S�p20(���p40)�����܂�]�F<br><input type="text" name="message" value="$message" class="text_box_b"><br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="�ύX����" class="button1"></p></form>|;
			last;
		}
	}
	close $fh;
	
	# ���X������̂�ؽĂɂȂ��̂͂��������̂ł�����x�ǉ�
	unless ($is_find) {
		open my $fh3, ">> $shop_list_file" or &error("$shop_list_file ̧�ق��J���܂���");
		print $fh3 "$m{name}�X<>$m{name}<>$date�J�X<>0<>0<>\n";
		close $fh3;
	}

	$m{tp} += 10;
	&n_menu;
}
sub tp_610 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	unless ($in{name}) {
		$mes .= "��߂܂���";
		&begin;
		return;
	}
	
	&error("���X�̖��O���������܂��B�S�p8(���p16)�����܂�") if length $in{name} > 16;
	&error("�Љ���������܂��B�S�p20(���p40)�����܂�") if length $in{mes} > 40;

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $shop_list_file" or &error("$shop_list_file ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
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
			
			if ($is_rewrite) {
				$line = "$shop_name<>$name<>$message<>$sale_c<>$sale_money<>\n";
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
# <input type="radio" �t�̎����̊G
#=================================================
sub radio_my_goods {
	my $sub_mes .= qq|<input type="radio" name="file_name" value="0" checked>��߂�<hr>|;
	opendir my $dh, $this_path_dir or &error("$this_path_dir �ިڸ�؂��J���܂���");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;
		
		my $file_title = &get_goods_title($file_name);
		$sub_mes .= qq|<img src="$this_path_dir/$file_name" style="vertical-align:middle;" $mobile_icon_size>| if $goods_type eq 'img';
		$sub_mes .= qq|<input type="radio" name="file_name" value="$file_name">$file_title<hr>|;
	}
	closedir $dh;
	$sub_mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	
	return $sub_mes;
}


#=================================================
# �W���i���珜��
#=================================================
sub remove_shop_goods {
	my $file_name = shift;

	return unless -f $this_file;

	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($file, $name, $price) = split /<>/, $line;
		
		if ($file_name eq $file) {
			$mes .= "$name��W���i���珜���܂���<br>";
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





1; # �폜�s��
