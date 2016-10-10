my $this_file = "$logdir/master.cgi";
#================================================
# ����
#================================================
# ���㐧��:���̐���ȏォ�����Œ�q���t���ɕ������
my $need_sedai = 2;

my %exp_to_name = (
	"nou_c"=>"�_��",
	"sho_c"=>"����",
	"hei_c"=>"����",
	"gai_c"=>"�O��",
	"gou_c"=>"���D",
	"cho_c"=>"����",
	"sen_c"=>"���]",
	"gik_c"=>"�U�v",
	"tei_c"=>"��@",
	"mat_c"=>"�ҕ�",
	"tou_c"=>"����",
	"shu_c"=>"�C�s",
	"win_c"=>"����",
	"lose_c"=>"�s��",
);

my %exp_to_needs = (
	"nou_c"=>5000,
	"sho_c"=>5000,
	"hei_c"=>5000,
	"gai_c"=>2000,
	"gou_c"=>5000,
	"cho_c"=>5000,
	"sen_c"=>5000,
	"gik_c"=>5000,
	"tei_c"=>5000,
	"mat_c"=>5000,
	"tou_c"=>20000,
	"shu_c"=>20000,
	"win_c"=>2000,
	"lose_c"=>500,
);

my $need_money = 0;
#================================================
# ���p����
#================================================
sub is_satisfy {
	return 1;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ�������܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�����͓��ꂾ<br>';
		$mes .= '�����͂Ȃ�̗p��?<br>';
	}
	
	&menu('��߂�','�t����T��','�t���o�^����','�j�傷��','���E����');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);

	$m{tp} = $cmd * 100;
	&{'tp_'. $m{tp} };
}

#================================================
# �t����T��
#================================================
sub tp_100 {
	if($m{sedai} > $need_sedai){
		$mes .= "��q�ɂȂ��̂�$need_sedai ����܂ł�<br>";
		&begin;
		return;
	}
	if($m{master}){
		$mes .= "���łɎt�������邼<br>";
		&begin;
		return;
	}
	$layout = 1;
	$mes .= '���ꂪ�A�t����ؽĂ�<br>';
	$mes .= '�K�������n���x�̎t����I��?<br>';
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>���O</th><th>$e2j{name}</th><th>�o�^��</th><th>����</th><th>�n���x</th><th>���b�Z�[�W</th><th>���E��<br></th></tr>| unless $is_mobile;

	open my $fh, "< $this_file" or &error("$this_file ���J���܂���");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		next unless $recommendation;
		$name .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$name/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/�o�^��$mdate/����$sedai/�n���x$exp_to_name{$expert}/���b�Z�[�W$message/���E��$recommendation<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$name</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$sedai</td><td>$exp_to_name{$expert}</td><td>$message</td><td>$recommendation<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���傷��" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
# ------------------
sub tp_110 {
	unless ($cmd) {
		&begin;
		return;
	}
	
	my $send_to;
	my $exp_c;
	open my $fh, "< $this_file" or &error("$this_file ���J���܂���");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		if ($cmd eq $no) {
			$send_to = $name;
			$exp_c = $expert;
			last;
		}
	}
	close $fh;

	my $y_id = unpack 'H*', $send_to;
	unless ($send_to) {
		$mes .= '�o�^��ؽĂɓo�^����Ă��Ȃ��l�ɂ͓���ł��܂���<br>';
		&begin;
		return;
	}
	unless (-f "$userdir/$y_id/user.cgi") {
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_file ���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
			unless ($cmd eq $no) {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		$mes .= "�A�C�c�͂����������I";
		&begin;
		return;
	}
	my %you_datas = &get_you_datas($send_to);
	$mes .= "$exp_to_name{$exp_c}�F$you_datas{$exp_c}<br>";
	
	if(-f "$userdir/$y_id/recommendation.cgi"){
		open my $fh, "< $userdir/$y_id/recommendation.cgi" or &error("���E��̧�ق��J���܂���");
		while (my $line = <$fh>){
			my($name, $message) = split /<>/, $line;
			$mes .= "$name����̐��E�F<br>$message<br>";
		}
		close $fh;
	}
	
	$mes .= "���̐l�̒�q�ɂȂ�܂����H<br>";
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>����<br>|;
	$mes .= qq|<input type="hidden" name="no" value="$cmd"><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="OK" class="button1"></p></form>|;	
	$m{tp} += 10;
}
# ------------------
sub tp_120 {
	return if &is_ng_cmd(1);
	
	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file ���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		if ($in{no} eq $no) {
			&regist_you_data($name, 'master', $m{name});
			$m{master} = $name;
			$m{master_c} = $expert;
			&write_world_news(qq|$m{name}��$name�ɒ�q���肵�܂���|);
			&system_letter($name, "$m{name}����q�ɂȂ�܂���")
		}
		else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	&begin;
}

#================================================
# �o�^
#================================================
sub tp_200 {
	$layout = 2;
	if($m{sedai} <= $need_sedai){
		$mes .= "�����ƏC�s���Ă��炱��<br>";
		&begin;
		return;
	}
	if($m{master}){
		$mes .= "���łɒ�q������<br>";
		&begin;
		return;
	}
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>�n���x</th></tr>| unless $is_mobile;

	for my $exp_c (keys %exp_to_name) {
		next if($exp_to_needs{$exp_c} > $m{$exp_c});
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$exp_c">$exp_to_name{$exp_c}<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$exp_c">$exp_to_name{$exp_c}</td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<textarea name="message" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�o�^����" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_210 {
	unless ($cmd){
		&begin;
		return;
	}
	my $exp_find = 0;
	for my $exp_c (keys %exp_to_name){
		if($exp_c eq $cmd){
			$exp_find= 1;
		}
	}
	unless ($exp_find){
		&begin;
		return;
	}
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		unless ($name eq $m{name}) {
			push @lines, $line;
		}
	}
	if ($m{money} < $need_money) {
		close $fh;
		$mes .= "�o�^���邨��������܂���<br>";
	}
	else {
		my($last_no) = (split /<>/, $lines[0])[0];
		++$last_no;
		unshift @lines, "$last_no<>$date<>$m{name}<>$m{country}<>$m{sedai}<>$cmd<>$m{shogo}<>$cs{name}[$m{country}]<>$in{message}<>\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		$mes .= "$m{name}���t���Ƃ��ēo�^����܂���<br>";
		$m{money} -= $need_money;
	}
	
	&begin;
}

#================================================
# �j�傷��
#================================================
sub tp_300 {
	unless($m{master}){
		$mes .= "��q�����܂���<br>";
		&begin;
		return;
	}
	$mes .= "�{���ɒ�q��j�債�܂����H<br>";
	
	&menu('��߂�','�j�傷��');
	$m{tp} += 10;
}

sub tp_310 {
	return if &is_ng_cmd(1);
	&regist_you_data($m{master}, 'master', '');
	&regist_you_data($m{master}, 'master_c', '');
	$m{master} = '';
	
	$mes .= "��q��j�債�܂���<br>";
	&begin;
}

#================================================
# ���E����
#================================================
sub tp_400 {
	$layout = 1;
	$mes .= '���ꂪ�A�t����ؽĂ�<br>';
	$mes .= '���E����t����I��?<br>';
	
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<table class="table1"><tr><th>���O</th><th>$e2j{name}</th><th>�o�^��</th><th>����</th><th>�n���x</th><th>���E��<br></th></tr>| unless $is_mobile;

	open my $fh, "< $this_file" or &error("$this_file ���J���܂���");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		next unless $recommendation;
		$name .= "[$shogo]" if $shogo;
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$name/<font color="$cs{color}[$country]">$cs{name}[$country]</font>/�o�^��$mdate/����$sedai/�n���x$exp_to_name{$expert}/���E��$recommendation<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$name</td><td><font color="$cs{color}[$country]">$cs{name}[$country]</font></td><td>$mdate</td><td align="right">$sedai</td><td>$exp_to_name{$expert}</td><td>$recommendation<br></td></tr>|;
	}
	close $fh;
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<textarea name="comment" cols="50" rows="$rows" class="textarea1"></textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���E����" class="button1"></p></form>|;
	
	$m{tp} += 10;
}

sub tp_410 {
	unless ($cmd) {
		&begin;
		return;
	}
	
	my $send_to;
	my $y_id;
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file ���J���܂���");
	while (my $line = <$fh>) {
		my($no, $mdate, $name, $country, $sedai, $expert, $shogo, $recommendation, $message) = split /<>/, $line;
		if ($cmd eq $no) {
			$send_to = $name;
			$y_id = unpack 'H*', $send_to;
			if($in{comment}){
				push @lines, "$no<>$mdate<>$name<>$country<>$sedai<>$expert<>$shogo<>$recommendation,$m{name}<>$message<>\n";
				open my $fh2, ">> $userdir/$y_id/recommendation.cgi" or &error("���E��̧�ق��J���܂���");
				print $fh2 "$m{name}<>$in{comment}<>\n";
				close $fh2;
			}else{
				push @lines, "$no<>$mdate<>$name<>$country<>$sedai<>$expert<>$shogo<>$recommendation<>$message<>\n";
			}
		}else{
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	if ($send_to) {
		if(-f "$userdir/$y_id/recommendation.cgi"){
			open my $fh2, "< $userdir/$y_id/recommendation.cgi" or &error("���E��̧�ق��J���܂���");
			while (my $line = <$fh2>){
				my($name, $message) = split /<>/, $line;
				$mes .= "$name����̐��E�F<br>$message<br>";
			}
			close $fh2;
		}
	}else{
		$mes .= '�o�^��ؽĂɓo�^����Ă��Ȃ��l�ɂ͐��E�ł��܂���<br>';
	}

	&begin;
}

sub system_letter {
	my $aname = shift;
	my $content = shift;

	my $send_id = unpack 'H*', $aname;
	local $this_file = "$userdir/$send_id/letter";
	if (-f "$this_file.cgi") {
		$in{comment} = $content;
		$mname = $m{name};
		$m{name} = '�V�X�e��';
		$mcountry = $m{country};
		$m{country} = 0;
		$micon = $m{icon};
		$m{icon} = '';
		$mshogo = $m{shogo};
		$m{shogo} = '';
		&send_letter($aname, 0);

		$in{comment} = "";
		$m{name} = $mname;
		$m{country} = $mcountry;
		$m{icon} = $micon;
		$m{shogo} = $mshogo;
		return 1;
	}
	
	return 0;
}

1; # �폜�s��
