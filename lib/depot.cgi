my $this_file = "$userdir/$id/depot.cgi";
my $this_lock_file = "$userdir/$id/depot_lock.cgi";
#=================================================
# �a���菊 Created by Merino
#=================================================

# �ő�ۑ���
my $max_depot = $m{sedai} > 7 ? 50 : $m{sedai} * 5 + 15;
$max_depot += $m{depot_bonus} if $m{depot_bonus};

my $lost_depot = $max_depot * 2;

# ����ɑ���Ƃ��̎萔��(����)
my $need_money = 100;

# ����ɑ���Ƃ��̎萔��(����)
my $need_money_other = 1000;

# ����l�i
my $sall_price = 100;

# ���t�𒴂�����������è��(���o���A���鎞�Ɍ��炳���)
my $penalty_money = $m{sedai} > 10 ? 3000 : $m{sedai} * 300;

# ����ɑ��鎞�ɕK�v������(������1���㎞�̂�)
my $need_lv = 10;

# ����ɑ���̋֎~�ȱ���
my %taboo_items = (
	wea => [32,], # ����
	egg => [], # �Ϻ�
	pet => [127,188], # �߯�
	gua => [], # �h��
);

#================================================
sub begin {
	if (-f "$userdir/$id/depot_flag.cgi") {
		unlink "$userdir/$id/depot_flag.cgi";
	}
	unless (-f $this_lock_file) {
		open my $lfh, "> $this_lock_file" or &error("$this_lock_file���J���܂���");
		close $lfh;
	}
	if ($m{tp} > 1) {
		$mes .= "���ɉ������܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "�����͗a���菊�ł��B$max_depot�܂ŗa���邱�Ƃ��ł��܂�<br>";
		$mes .= "$max_depot�𒴂��Ă���ꍇ�́A$penalty_money G�̔������x�����Ă��炢�܂�<br>";
		$mes .= "�ǂ����܂���?<br>";
	}
	&depot_common;
	&menu('��߂�', '���o��', '�a����', '��������', '����ɑ���', '�ꊇ���p', '�̂Ă�', '���b�N��������');
}
sub tp_1 {
	return if &is_ng_cmd(1..7);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# ���o��
#=================================================
sub tp_100 {
	$layout = 2;
	&depot_common;
	my($count, $sub_mes) = &radio_my_depot;

	$mes .= "�ǂ�����o���܂���? [ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= $is_mobile ? qq|<p><input type="submit" value="���o��" class="button1" accesskey="#"></p></form>|:
		qq|<p><input type="submit" value="���o��" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_110 {
	if ($cmd) {
		my $count = 0;
		my $new_line = '';
		my $add_line = '';
		my $depot_line = '';
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($rkind, $ritem_no, $ritem_c, $ritem_lv) = split /<>/, $line;
			$depot_line .= "$rkind,$ritem_no,$ritem_c,$ritem_lv<>";
			++$count;
			if (!$new_line && $cmd eq $count) {
				$new_line = $line;
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
				$depot_line .= "$kind,$item_no,$item_c,$item_lv<>";
				if ($kind eq '1' && $m{wea}) { 
					if($m{wea_name}){
						$m{wea} = 32;
						$m{wea_c} = 0;
						$m{wea_lv} = 0;
						$mes .= "������̎�𗣂ꂽ�r�[$m{wea_name}�͂�����$weas[$m{wea}][1]�ɂȂ��Ă��܂���<br>";
						$m{wea_name} = "";

					}
					$add_line = "$kind<>$m{wea}<>$m{wea_c}<>$m{wea_lv}<>\n";
					$mes .= "$weas[$m{wea}][1]��a��";
				}
				elsif ($kind eq '2' && $m{egg}) {
					$add_line = "$kind<>$m{egg}<>$m{egg_c}<>0<>\n";
					$mes .= "$eggs[$m{egg}][1]��a��";
				}
				elsif($kind eq '3' && $m{pet}) {
					$add_line = "$kind<>$m{pet}<>$m{pet_c}<>0<>\n";
					$mes .= "$pets[$m{pet}][1]��$m{pet_c}��a��";
				}
				elsif($kind eq '4' && $m{gua}) {
					$add_line = "$kind<>$m{gua}<>0<>0<>\n";
					$mes .= "$guas[$m{gua}][1]��a��";
				}
			}
			else {
				push @lines, $line;
			}
		}
		if ($new_line) {
			push @lines, $add_line if $add_line;
			seek  $fh, 0, 0;
			truncate $fh, 0; 
			print $fh @lines;
			close $fh;
			
			my $s_mes;
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line;
			if ($kind eq '1') {
				$m{wea}    = $item_no;
				$m{wea_c}  = $item_c;
				$m{wea_lv} = $item_lv;
				$mes .= "$weas[$m{wea}][1]�����o���܂���<br>";
				$s_mes = "$weas[$m{wea}][1]���o��";
			}
			elsif ($kind eq '2') {
				$m{egg}    = $item_no;
				$m{egg_c}  = $item_c;
				$mes .= "$eggs[$m{egg}][1]�����o���܂���<br>";
				$s_mes = "$eggs[$m{egg}][1]���o��";
			}
			elsif ($kind eq '3') {
				$m{pet}    = $item_no;
				$m{pet_c}  = $item_c;
				$mes .= "$pets[$m{pet}][1]��$m{pet_c}�����o���܂���<br>";
				$s_mes = "$pets[$m{pet}][1]��$m{pet_c}���o��";
			}
			elsif ($kind eq '4') {
				$m{gua}    = $item_no;
				$mes .= "$guas[$m{gua}][1]�����o���܂���<br>";
				$s_mes = "$guas[$m{gua}][1]���o��";
			}
			my($tmin,$thour,$tmday,$tmon,$tyear) = (localtime($time))[1..4];
			$tdate = sprintf("%d/%d %02d:%02d", $tmon+1,$tmday,$thour,$tmin);
			$s_mes .= " ($tdate)";
			
			if(-f "$userdir/$id/depot_watch.cgi"){
				open my $wfh, ">> $userdir/$id/depot_watch.cgi";
				print $wfh "$s_mes<>$depot_line\n";
				close $wfh;
			}
			&penalty_depot($count);

			# ���o�����ݸނŐV�������т�����κڸ��݂ɒǉ�
			require './lib/add_collection.cgi';
			&add_collection;
		}
		else {
			close $fh;
		}
	}
	&begin;
}

#=================================================
# �a����
#=================================================
sub tp_200 {
	$mes .= '�ǂ��a���܂���?';
	
	my @menus = ('��߂�');
	push @menus, $m{wea} ? $weas[$m{wea}][1] : '';
	push @menus, $m{egg} ? $eggs[$m{egg}][1] : '';
	push @menus, $m{pet} ? $pets[$m{pet}][1] : '';
	push @menus, $m{gua} ? $guas[$m{gua}][1] : '';
	
	&menu(@menus);
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1..4);

	my $line;
	if ($cmd eq '1' && $m{wea}) {
		# �����ŃI������p�Ɏ��f�[�^�����������Ă͂����Ȃ�
		# ���������ňӐ}���� return ����\��������
		$line = $m{wea_name} ? "$cmd<>32<>0<>0<>\n" : "$cmd<>$m{wea}<>$m{wea_c}<>$m{wea_lv}<>\n";
	}
	elsif ($cmd eq '2' && $m{egg}) {
		$line = "$cmd<>$m{egg}<>$m{egg_c}<>0<>\n";
	}
	elsif ($cmd eq '3' && $m{pet}) {
		$line = "$cmd<>$m{pet}<>$m{pet_c}<>0<>\n";
	}
	elsif ($cmd eq '4' && $m{gua}) {
		$line = "$cmd<>$m{gua}<>0<>0<>\n";
	}
	else {
		&begin;
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	push @lines, $_ while <$fh>;
	
	if (@lines >= $max_depot) {
		close $fh;
		$mes .= '����ȏ�a���邱�Ƃ��ł��܂���<br>';
		$m{is_full} = 1;
	}
	else {
		push @lines, $line;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		if ($cmd eq '1') {
			if($m{wea_name}){
				$m{wea} = 32;
				$mes .= "������̎�𗣂ꂽ�r�[$m{wea_name}�͂�����$weas[$m{wea}][1]�ɂȂ��Ă��܂���<br>";
				$m{wea_name} = "";
			}
			$mes .= "$weas[$m{wea}][1]��a���܂���<br>";
			$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		}
		elsif ($cmd eq '2') {
			$mes .= "$eggs[$m{egg}][1]��a���܂���<br>";
			$m{egg} = $m{egg_c} = 0;
		}
		elsif ($cmd eq '3') {
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}��a���܂���<br>";
			$m{pet} = 0;
		}
		elsif ($cmd eq '4') {
			$mes .= "$guas[$m{gua}][1]��a���܂���<br>";
			$m{gua} = 0;
		}
		
		$m{is_full} = 1 if @lines >= $max_depot;
	}
	&begin;
}

#=================================================
# ����
#=================================================
sub tp_300 {
	my @lines = ();
	my @sub_lines = ();
	my $n_egg = 0;
	my $n_man = 0;
	my $n_hero = 0;	
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>){
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		if($kind == 2 && $item_no == 53){
			$line = "2<>42<>$item_c<>$item_lv<>\n";
			$n_egg++;
		}
		if($kind == 3 && $item_no == 180){
			$line = "3<>76<>$item_c<>$item_lv<>\n";
			$n_man++;
		}
		if($kind == 3 && $item_no == 181){
			$line = "3<>77<>$item_c<>$item_lv<>\n";
			$n_hero++;
		}
		push @lines, $line;
	}
	@lines = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] }
					map { [$_, split /<>/ ] } @lines;
	while($n_egg>0 || $n_man>0 || $n_hero>0){
		my $line_i = rand(@lines);
		my $o_line = $lines[$line_i];
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $o_line;
		if($kind == 2 && $item_no == 42 && $n_egg > 0){
			$o_line = "2<>53<>$item_c<>$item_lv<>\n";
			$n_egg--;
		}
		if($kind == 3 && $item_no == 76 && $n_man > 0){
			$o_line = "3<>180<>$item_c<>$item_lv<>\n";
			$n_man--;
		}
		if($kind == 3 && $item_no == 77 && $n_hero > 0){
			$o_line = "3<>181<>$item_c<>$item_lv<>\n";
			$n_hero--;
		}
		$lines[$line_i] = $o_line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= "�a���Ă�����̂𐮗����܂���<br>";
	&begin;
}

#=================================================
# ����ɑ���
#=================================================
sub tp_400 {
	$layout = 1;
	$mes .= "�N�ɉ��𑗂�܂���?<br>�����萔���F$need_money G<br>���O�萔���F$need_money_other G<br>";
	$mes .= '�����𑗂�ꍇ�͋��z����͂��Ă�������<br>';

	$mes .= qq|<form method="$method" action="$script"><p>���M��F<input type="text" name="send_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1">[$weas[$m{wea}][2]]$weas[$m{wea}][1]��$m{wea_lv}($m{wea_c}/$weas[$m{wea}][4])<br>| if $m{wea};
	$mes .= qq|<input type="radio" name="cmd" value="2">[��]$eggs[$m{egg}][1]($m{egg_c}/$eggs[$m{egg}][2])<br>| if $m{egg};
	$mes .= qq|<input type="radio" name="cmd" value="3">[�y]$pets[$m{pet}][1]��$m{pet_c}<br>| if $m{pet};
	$mes .= qq|<input type="radio" name="cmd" value="4">[$guas[$m{gua}][2]]$guas[$m{gua}][1]<br>| if $m{gua};
	$mes .= qq|<input type="radio" name="cmd" value="5">����<input type="text" name="send_money" value="0" class="text_box1" style="text-align:right">G<br>| if $m{money} > 0;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_410 {
	return if &is_ng_cmd(1..5);
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�̕��͑��邱�Ƃ��ł��܂���<br>";
		&begin;
		return;
	}
	elsif ($in{send_name} eq '') {
		$mes .= '����悪�L������Ă��܂���<br>';
		&begin;
		return;
	}
	elsif ($m{sedai} <= 1 && $m{lv} < $need_lv) {
		$mes .= "1����ڂ�����$need_lv�����̐l�͑��邱�Ƃ��ł��܂���<br>";
		&begin;
		return;
	}

	my $send_id = unpack 'H*', $in{send_name};
	my %datas = &get_you_datas($send_id, 1);
	
	# �����̏�����ς���Ƃ��납��
	if ($datas{is_full} && $cmd ne '5' && !&is_sabakan) {
		$mes .= "$in{send_name}�̗a���菊�����t�ő��邱�Ƃ��ł��܂���<br>";
		&begin;
		return;
	}
	
	my $pay = $datas{country} eq $m{country} ? $need_money : $need_money_other;
	
	if ($m{money} < $pay) {
		$mes .= "�X���萔��( $pay G)������܂���<br>";
		&begin;
		return;
	}

	if ($m{wea_name}) {
		$mes .= "�B�ꖳ��̕���𑗂邱�Ƃ͂ł��܂���<br>";
		&begin;
		return;
	}
	my @kinds = ('', 'wea', 'egg', 'pet', 'gua');
	for my $taboo_item (@{ $taboo_items{ $kinds[$cmd] } }) {
		if ($taboo_item eq $m{ $kinds[$cmd] }) {
			my $t_item_name = $cmd eq '1' ? $weas[$m{wea}][1]
							: $cmd eq '2' ? $eggs[$m{egg}][1]
							: $cmd eq '3' ? $pets[$m{pet}][1]
							:               $guas[$m{gua}][1]
							;
			$mes .= "$t_item_name�͑��̐l�ɑ��邱�Ƃ͂ł��܂���<br>";
			&begin;
			return;
		}
	}
	
	my %lock = &get_lock_item;
	my $check_line = $cmd eq '1' ? "$cmd<>$m{wea}<>"
					: $cmd eq '2' ? "$cmd<>$m{egg}<>"
					: $cmd eq '3' ? "$cmd<>$m{pet}<>"
					:               "$cmd<>$m{gua}<>"
					;
	if ($lock{$check_line}) {
			$mes .= "���b�N����Ă���A�C�e���͑��̐l�ɑ��邱�Ƃ͂ł��܂���<br>";
			&begin;
			return;
	}
	
	if ($cmd eq '1' && $m{wea}) {
		if($m{wea_name}){
			$m{wea} = 32;
			$m{wea_c} = 0;
			$m{wea_lv} = 0;
			$mes .= "������̎�𗣂ꂽ�r�[$m{wea_name}�͂�����$weas[$m{wea}][1]�ɂȂ��Ă��܂���<br>";
			$m{wea_name} = "";
		}
		&send_item($in{send_name}, $cmd, $m{wea}, $m{wea_c}, $m{wea_lv}, &is_sabakan);
		&mes_and_send_news("$in{send_name}��$weas[$m{wea}][1]�𑗂�܂���");
		$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '2' && $m{egg}) {
		&send_item($in{send_name}, $cmd, $m{egg}, $m{egg_c}, 0, &is_sabakan);
		&mes_and_send_news("$in{send_name}��$eggs[$m{egg}][1]�𑗂�܂���");
		$m{egg} = $m{egg_c} = 0;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '3' && $m{pet}) {
		&send_item($in{send_name}, $cmd, $m{pet}, $m{pet_c}, 0, &is_sabakan);
		&mes_and_send_news("$in{send_name}��$pets[$m{pet}][1]��$m{pet_c}�𑗂�܂���");
		$m{pet} = 0;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '4' && $m{gua}) {
		&send_item($in{send_name}, $cmd, $m{gua}, 0, 0, &is_sabakan);
		&mes_and_send_news("$in{send_name}��$guas[$m{gua}][1]�𑗂�܂���");
		$m{gua} = 0;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '5' && $in{send_money} > 0 && $in{send_money} !~ /[^0-9]/) {
		if ($m{money} + $pay > $in{send_money}) {
			&send_money($in{send_name}, $m{name}, $in{send_money});
			&mes_and_send_news("$in{send_name}�� $in{send_money} G�𑗂�܂���");
			$m{money} -= $in{send_money} + $pay;
		}
		else {
			$mes .= "�萔������܂߂Ă���������܂���<br>";
		}
	}
	&begin;
}

#=================================================
# �ެݸ����߂ɔ���
#=================================================
sub tp_500 {
	$layout = 2;
	my($count, $sub_mes) = &checkbox_my_depot;

	$mes .= "�ǂ�𔄂�܂���?[ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_510 {
	if ($in{uncheck_flag}) {
		$m{tp} -= 10;
		&{ 'tp_'. $m{tp} };
		return;
	}
	my($maxcount, $sub_mes) = &checkbox_my_depot;
	my $count = 0;
	my $is_rewrite = 0;
	my @junk = ();
	my @junk_log = ();
	my %lock = &get_lock_item;
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$count;
		if ($in{$count} eq '1') {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			if ($lock{"$kind<>$item_no<>"}) {
				push @lines, $line;
			} else {
				$is_rewrite = 1;
				
				$mes .= $kind eq '1' ? "$weas[$item_no][1]�𔄂�܂���<br>"
					  : $kind eq '2' ? "$eggs[$item_no][1]�𔄂�܂���<br>"
					  : $kind eq '3' ? "$pets[$item_no][1]��$item_c�𔄂�܂���<br>"
					  :                "$guas[$item_no][1]�𔄂�܂���<br>"
					  ;
				$item_c = 0 if $kind eq '3'; # �ެݸ���߯Ă𗬂����̓��x����������
				$m{money} += $sall_price;

				# ��ʂɈꊇ���p����Ƃ��̐�����̧�ٵ���݂���̂�1��ōςނ悤�ɕύX
#				if (rand(2) < 1) {
					push @junk, "$kind<>$item_no<>$item_c<>\n";
#				}
				push @junk_log, "$kind<>$item_no<>$item_c<>$m{name}<>$time<>0<>\n";
				&penalty_depot($maxcount);
			}
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rewrite) {
		# �����̑q�ɂ̏�������
		seek  $fh, 0, 0;
		truncate $fh, 0; 
		print $fh @lines;

		# �ެݸ�ɏ�������
		open my $fh2, ">> $logdir/junk_shop.cgi" or &error("$logdir/junk_shop.cgi̧�ق��J���܂���");
		print $fh2 @junk;
		close $fh2;

		# �ެݸ۸ނɏ�������
		open my $fh3, ">> $logdir/junk_shop_sub.cgi" or &error("$logdir/junk_shop_sub.cgi̧�ق��J���܂���");
		print $fh3 @junk_log;
		close $fh3;
	}
	close $fh;
	&begin;
}

#=================================================
# �̂Ă�
#=================================================
sub tp_600 {
	$layout = 2;
	my($count, $sub_mes) = &radio_my_depot;

	$mes .= "�ǂ���̂Ă܂���?[ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�̂Ă�" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_610 {
	my($maxcount, $sub_mes) = &radio_my_depot;
	my $count = 0;
	my $is_rewrite = 0;
	my %lock = &get_lock_item;
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$count;
		if ($cmd eq $count) {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			if ($lock{"$kind<>$item_no<>"}) {
				push @lines, $line;
			} else {
				$is_rewrite = 1;
				
				$mes .= $kind eq '1' ? "$weas[$item_no][1]���̂Ă܂���<br>"
					  : $kind eq '2' ? "$eggs[$item_no][1]���̂Ă܂���<br>"
					  : $kind eq '3' ? "$pets[$item_no][1]��$item_c���̂Ă܂���<br>"
					  :                "$guas[$item_no][1]���̂Ă܂���<br>"
					  ;
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
	&begin;
}

#=================================================
# ���b�N
#=================================================
sub tp_700 {
	$layout = 2;
	my($count, $sub_mes) = &checkbox_my_depot_lock_checked;

	$mes .= "�ǂ�����b�N���܂���?[ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���b�N" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_710 {
	if ($in{uncheck_flag}) {
		$m{tp} -= 10;
		&{ 'tp_'. $m{tp} };
		return;
	}
	my %lock = ();
	open my $fh, "< $this_file" or &error("$this_file���J���܂���");
	while (my $line = <$fh>) {
		++$count;
		if ($in{$count} eq '1') {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			$lock{"$kind<>$item_no<>"}++;
		}
	}
	close $fh;
	
	open my $lfh, "> $this_lock_file" or &error("$this_lock_file���J���܂���");
	foreach my $line(keys(%lock)){
		if ($lock{$line} > 0) {
			print $lfh "$line\n";
		}
	}
	close $lfh;
	&begin;
}

#=================================================
# ��������
#=================================================
sub penalty_depot {
	my $count = shift;
	return if $count eq '';

	if ($count > $max_depot) {
		$m{is_full} = 1;
		$mes .= "���� $penalty_money G���x�����܂���<br>";
		$m{money} -= $penalty_money;
	}
	else {
		$m{is_full} = 0;
	}
}


#=================================================
# <input type="radio" �t�̗a���菊�̕�
#=================================================
sub radio_my_depot {
	my $count = 0;
	my %lock = &get_lock_item;
	my $sub_mes = qq|<form method="$method" action="$script">|;
	$sub_mes .= qq|<input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		my $lock_mes = '';
		if ($lock{"$kind<>$item_no<>"}) {
			$lock_mes = ' ���b�N����Ă܂�';
		}
		$sub_mes .= qq|<input type="radio" id="no_$count" name="cmd" value="$count">|;
		$sub_mes .= qq|<label for="no_$count">| unless $is_mobile;
		
		$sub_mes .= $kind eq '1' ? qq|[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])$lock_mes|
				  : $kind eq '2' ? qq|[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])$lock_mes|
				  : $kind eq '3' ? qq|[��]$pets[$item_no][1]��$item_c$lock_mes|
				  :			       qq|[$guas[$item_no][2]]$guas[$item_no][1]$lock_mes|
				  ;
		$sub_mes .= qq|</label>| unless $is_mobile;
		$sub_mes .= qq|<br>|;
	}
	close $fh;
	
	$m{is_full} = $count >= $max_depot ? 1 : 0;
	
	return $count, $sub_mes;
}

#=================================================
# <input type="checkbox" �t�̗a���菊�̕�
#=================================================
sub checkbox_my_depot {
	my $count = 0;
	my $sub_mes = "";
	my %lock = &get_lock_item;
	if ($is_mobile) {
		$sub_mes .= qq|<form method="$method" action="$script">|;
		$sub_mes .= qq|<input type="hidden" name="uncheck_flag" value="1">|;
		$sub_mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$sub_mes .= qq|<p><input type="submit" value="�`�F�b�N���O��" class="button1"></p></form>|;
	}
	$sub_mes .= qq|<form method="$method" action="$script">|;
	if (!$is_mobile) {
		$sub_mes .= qq|<input type="button" name="all_unchecked" value="�`�F�b�N���O��" class="button1" onclick="\$('input:checkbox').prop('checked',false); "><br>|;
	}
	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		my $lock_mes = '';
		if ($lock{"$kind<>$item_no<>"}) {
			$lock_mes = ' ���b�N����Ă܂�';
		}
		$sub_mes .= qq|<input type="checkbox" id="no_$count" name="$count" value="1">|;
		$sub_mes .= qq|<label for="no_$count">| unless $is_mobile;
		
		$sub_mes .= $kind eq '1' ? qq|[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])$lock_mes|
				  : $kind eq '2' ? qq|[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])$lock_mes|
				  : $kind eq '3' ? qq|[��]$pets[$item_no][1]��$item_c$lock_mes|
				  :			       qq|[$guas[$item_no][2]]$guas[$item_no][1]$lock_mes|
				  ;
		$sub_mes .= qq|</label>| unless $is_mobile;
		$sub_mes .= qq|<br>|;
	}
	close $fh;
	
	$m{is_full} = $count >= $max_depot ? 1 : 0;
	
	return $count, $sub_mes;
}

#=================================================
# <input type="checkbox" �t�̗a���菊�̕�
#=================================================
sub checkbox_my_depot_lock_checked {
	my $count = 0;
	my $sub_mes = "";
	my %lock = &get_lock_item;
	if ($is_mobile) {
		$sub_mes .= qq|<form method="$method" action="$script">|;
		$sub_mes .= qq|<input type="hidden" name="uncheck_flag" value="1">|;
		$sub_mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$sub_mes .= qq|<p><input type="submit" value="�`�F�b�N���O��" class="button1"></p></form>|;
	}
	$sub_mes .= qq|<form method="$method" action="$script">|;
	if (!$is_mobile) {
		$sub_mes .= qq|<input type="button" name="all_unchecked" value="�`�F�b�N���O��" class="button1" onclick="\$('input:checkbox').prop('checked',false); "><br>|;
	}
	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		$sub_mes .= qq|<input type="checkbox" id="no_$count" name="$count" value="1"|;
		my $lock_mes = '';
		if ($lock{"$kind<>$item_no<>"}) {
			$sub_mes .= qq| checked|;
			$lock_mes = ' ���b�N����Ă܂�';
		}
		$sub_mes .= qq|>|;
		$sub_mes .= qq|<label for="no_$count">| unless $is_mobile;
		
		$sub_mes .= $kind eq '1' ? qq|[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])$lock_mes|
				  : $kind eq '2' ? qq|[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])$lock_mes|
				  : $kind eq '3' ? qq|[��]$pets[$item_no][1]��$item_c$lock_mes|
				  :			       qq|[$guas[$item_no][2]]$guas[$item_no][1]$lock_mes|
				  ;
		$sub_mes .= qq|</label>| unless $is_mobile;
		$sub_mes .= qq|<br>|;
}
	close $fh;
	
	$m{is_full} = $count >= $max_depot ? 1 : 0;
	
	return $count, $sub_mes;
}

#=================================================
# ���b�N�A�C�e���̎擾
#=================================================
sub get_lock_item {
	my %lock = ();
	open my $lfh, "< $this_lock_file" or &error("$this_lock_file���J���܂���");
	while (my $line = <$lfh>){
		chomp $line;
		$lock{$line}++;
	}
	close $lfh;

	return %lock;
}

#=================================================
# ���ʏ���
#=================================================
sub depot_common {
	my $count = 0;
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$count;
		if ($count >= $lost_depot) {
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
}
1; # �폜�s��
