my $this_file      = "$userdir/$id/shop_bank.cgi";
my $shop_list_file = "$logdir/shop_list_bank.cgi";
#================================================
# ���l�̋�s Created by Merino
#================================================

# ���ݔ�p
my $build_money = 300000;

# �ŏ��a�����x
my $min_deposit = 1000000;
# �ő�a�����x
my $max_deposit = 4999999;

# �ŏ��萔��
my $min_fee = 500;
# �ő�萔��
my $max_fee = 100000;

# �ŏ��a���Ґ�
my $min_mem = 2;
# �ő�a���Ґ�
my $max_mem = 20;


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "���ɉ������܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "�ȉ��̏ꍇ�ɋ�s���|�Y�ƂȂ�܂�<br>";
		$mes .= "<li>$m{name}�̎����� 0 G����";
		$mes .= "<li>�ݷݸލX�V�����ݸނŋ�s�ւ̑��a���z�� 100�� G�ȉ�";
		$mes .= "<li>�ݷݸލX�V�����ݸނ�(�����ȊO)�N����s�𗘗p���Ă��Ȃ�";
	}
	&menu('��߂�', '��s�̐ݒ�', '��s�����Ă�','�ڋq�f�[�^','��Y�v��');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	$m{tp} = $cmd * 100;
	if ($cmd eq '2') {
		if (-f $this_file) {
			$mes .= "���łɎ����̋�s�������Ă��܂�<br>";
			&begin;
		}
		elsif ($jobs[$m{job}][1] ne '���l') {
			$mes .= "�E�Ƃ����l�łȂ��Ƌ�s�����Ă��Ƃ��ł��܂���<br>";
			&begin;
		}
		else {
			$mes .= "��s�����Ă�ɂ� $build_money G������܂�<br>";
			$mes .= "����s�ݷݸނ̍X�V���߂����Ɍ��Ă�Ƃ����ɓ|�Y���Ă��܂��܂�<br>";
			&menu('��߂�','���Ă�');
		}
	}
	elsif (!-f $this_file) {
		$mes .= '�܂��́A��s�����Ă�K�v������܂�<br>';
		&begin;
	}
	else {
		&{ 'tp_'. $m{tp} };
	}
}

#=================================================
# ����
#=================================================
sub tp_200 {
	if ($cmd eq '1') {
		if ($m{money} >= $build_money) {
			open my $fh, "> $this_file" or &error('��s�����Ă�̂Ɏ��s���܂���');
			print $fh "1000<>5<>10<>4999999<>\n";
			close $fh;
			chmod $chmod, "$this_file";
	
			open my $fh2, "> $userdir/$id/shop_sale_bank.cgi" or &error('��ٽ̧�ق��J���܂���');
			print $fh2 "0<>0<>";
			close $fh2;
			chmod $chmod, "$userdir/$id/shop_sale_bank.cgi";
			
			open my $fh3, ">> $shop_list_file" or &error('��sؽ�̧�ق��J���܂���');
			print $fh3 "$m{name}��s<>$m{name}<>$date�J�X<>0<>0<>\n";
			close $fh3;
	
			&mes_and_send_news("<b>��s�����Ă܂���</b>", 1);
			$m{money} -= $build_money;
		}
		else {
			$mes .= '����������܂���<br>';
		}
	}
	&begin;
}

#=================================================
# ��s�̐ݒ�
#=================================================
sub tp_100 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	my $head_line = <$fh>;
	close $fh;
	my($fee,$rishi,$max_pla,$max_dep) = split /<>/, $head_line;
	$max_pla = 10 unless $max_pla;
	$max_dep = 4999999 unless $max_dep;
	
	my $is_find = 0;
	open my $fh, "< $shop_list_file" or &error('��sؽĂ��ǂݍ��߂܂���');
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		my($year, $name, $money) = split /<>/, $line;
		
		if ($name eq $m{name}) {
			$is_find = 1;
			
			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|�O��[�葱�����F $sale_c�� / ���v�F$sale_money G]<br>|;
			$mes .= qq|<hr>�萔��[$min_fee�`$max_fee G]�F<input type="text" name="fee" value="$fee" class="text_box_s" style="text-align: right">G<br>|;
			$mes .= qq|����[0.1%�`20.0%]�F<input type="text" name="rishi" value="$rishi" class="text_box_s" style="text-align: right">�~0.1%<br>|;
			$mes .= qq|���p�l��[$min_mem�`$max_mem�l]�F<input type="text" name="max_pla" value="$max_pla" class="text_box_s" style="text-align: right">�l<br>|;
			$mes .= qq|�a�����x[$min_deposit�`$max_deposit G]�F<input type="text" name="max_dep" value="$max_dep" class="text_box_s" style="text-align: right">G<br>|;
			$mes .= qq|<hr>��s�̖��O[�S�p8(���p16)�����܂�]�F<br><input type="text" name="name" value="$shop_name" class="text_box1"><br>|;
			$mes .= qq|�Љ[�S�p20(���p40)�����܂�]�F<br><input type="text" name="message" value="$message" class="text_box_b"><br>|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<p><input type="submit" value="�ύX����" class="button1"></p></form>|;
			last;
		}
	}
	close $fh;
	
	# ��s������̂�ؽĂɂȂ��̂͂��������̂ł�����x�ǉ�
	unless ($is_find) {
		open my $fh3, ">> $shop_list_file" or &error('��sؽ�̧�ق��J���܂���');
		print $fh3 "$m{name}�X<>$m{name}<>$date�J�X<>0<>0<>\n";
		close $fh3;
	}
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	unless ($in{name}) {
		$mes .= '��߂܂���';
		&begin;
		return;
	}
	
	&error("��s�̖��O���������܂��B�S�p8(���p16)�����܂�") if length $in{name} > 16;
	&error("�Љ���������܂��B�S�p20(���p40)�����܂�") if length $in{mes} > 40;
	&error("�萔����$min_fee�`$max_fee G�܂łł�") if $in{fee} eq '' || $in{fee} =~ /[^0-9]/ || $in{fee} < $min_fee || $in{fee} > $max_fee;
	&error("������0.1%�`20.0%�܂łł�") if $in{rishi} eq '' || $in{rishi} =~ /[^0-9]/ || $in{rishi} < 1 || $in{rishi} > 200;
	&error("���p�l����$min_mem�`$max_mem�l�܂łł�") if $in{max_pla} eq '' || $in{max_pla} =~ /[^0-9]/ || $in{max_pla} < $min_mem || $in{max_pla} > $max_mem;
	&error("�a�����x��$min_deposit�`$max_deposit G�܂łł�") if $in{max_dep} eq '' || $in{max_dep} =~ /[^0-9]/ || $in{max_dep} < $min_deposit || $in{max_dep} > $max_deposit;

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $shop_list_file" or &error('��sؽĂ��J���܂���');
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		
		if ($name eq $m{name}) {
			unless ($shop_name eq $in{name}) {
				$mes .= "��s�̖��O�� $in{name} �ɕς��܂���<br>";
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
			&error("���łɓ������O�̋�s�����݂��܂�");
		}
		push @lines, $line;
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;
	
	&regist_my_bank;

	&begin;
}

#=================================================
# �ڋq���
#=================================================
sub tp_300 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		$mes .= qq|�u$name �l�v$world_name��$year�N���� $money G �a���Ă��܂�<br>|;
	}
	close $fh;

	&begin;
}

#=================================================
# ��Y�v���i�L�������Ȃ��Ȃ����l�̗a���f�[�^�������܂��j
#=================================================
sub tp_400 {
	unless (-f $this_file) {
		&begin;
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		my $id = unpack 'H*', $name;
		unless(-f "$userdir/$id/user.cgi"){
			$mes .= qq|��$name �l�̗a�� $money G ��������܂���<br>|;
			&send_money($m{name}, "�y��Y�v���z$name", $money);
		}else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	&begin;
}



sub regist_my_bank {
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($fee,$rishi,$max_pla,$max_dep) = split /<>/, $head_line;
	$max_pla = 10 unless $max_pla;	
	$max_dep = 4999999 unless $max_dep;

	unless ($fee eq $in{fee}) {
		$mes .= "�萔���� $in{fee} G�ɕς��܂���<br>";
		$is_rewrite = 1;
	}
	unless ($rishi eq $in{rishi}) {
		my $r = $in{rishi} / 10.0;
		$mes .= "������ $r%�ɕς��܂���<br>";
		$is_rewrite = 1;
	}
	unless ($max_pla eq $in{max_pla}) {
		$mes .= "���p�l���� $in{max_pla}�l�ɕς��܂���<br>";
		$is_rewrite = 1;
	}
	unless ($max_dep eq $in{max_dep}) {
		$mes .= "�a�����x�z�� $in{max_dep} G�ɕς��܂���<br>";
		$is_rewrite = 1;
	}
	if ($is_rewrite) {
		push @lines, "$in{fee}<>$in{rishi}<>$in{max_pla}<>$in{max_dep}<>\n";
	}
	else {
		return;
	}
	
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


1; # �폜�s��
