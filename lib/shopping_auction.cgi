my $this_file = "$logdir/auction.cgi";
#=================================================
# ������ Created by Merino
#=================================================
require "$datadir/buyable.cgi";

# ���D����(��)
my $limit_day = 3;

# �ő�o�i��
my $max_auction = 30;

# �o�i�֎~����
my %taboo_items = (
	wea => [1,6,11,16,21,26], # ����
	egg => [], # �Ϻ�
	pet => [], # �߯�
	gua => [], # �h��
);


#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�̕��͂��f�肵�Ă��܂�<br>";
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ������܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�����݉��ɗ��܂���<br>�������܂���?<br>';
	}
	&menu('��߂�','���D����','�o�i����');
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#=================================================
# ���D
#=================================================
sub tp_100 {
	$layout = 1;
	
	$mes .= qq|�����݂̗��D�����́A�o�i������ $limit_day���O��ł�<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
 	$mes .= $is_mobile ? qq|<hr>���D�i/���D�z/�����z/���D��/�o�i��<br>|
 		: qq|<table class="table1" cellpadding="3"><tr><th>���D�i</th><th>���D�z</th><th>�����z</th><th>���D��</th><th>�o�i��</th><th>���</th><th>���D�\\�z<br></th>|;

	open my $fh, "< $this_file" or &error("$this_file���ǂݍ��߂܂���");
	$m{total_auction} = 0;
	while (my $line = <$fh>) {
		my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price, $buyout_price) = split /<>/, $line;
		my $item_title = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
					   : $kind eq '2' ? "[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
					   : $kind eq '3' ? "[�y]$pets[$item_no][1]��$item_c"
					   : 				"[�h]$guas[$item_no][1]"
					   ;
		my $item_state = $time + 3600 * 24 > $bit_time ? "���낻��":
						$time + ($limit_day - 1) * 3600 * 24 > $bit_time ? "�܂��܂�":"new";
		unless($buyout_price){
			$buyout_price = '�Ȃ�';
		}
		my $next_min_price = int($item_price * 1.2);
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$item_title/$item_price G/��$buyout_price G/$to_name/$from_name/$item_state<br>|
			: qq|<tr><td><input type="radio" name="cmd" value="$no">$item_title</td><td align="right">$item_price G</td><td align="right">$buyout_price G</td><td>$to_name</td><td>$from_name</td><td>$item_state<br></td><td>$next_min_price</td></tr>|;
		$m{total_auction} += $item_price if ($to_name eq $m{name} && $from_name ne $m{name});
	}
	close $fh;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<p>���D���z�F<input type="text" name="money" value="0" class="text_box1" style="text-align:right" class="text1">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���D����" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_110 {
	$in{money} = int($in{money});
	if ($m{money} < $in{money} + $m{total_auction}) {
		$mes .= '����Ȃɂ����������Ă��܂���<br>';
	}
	elsif ($cmd && $in{money} && $in{money} !~ /[^0-9]/) {
		my $is_rewrite = 0;
		my $is_sokketsu = 0;
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price, $buyout_price) = split /<>/, $line;
			if ($no eq $cmd) {
				my $need_money = int($item_price * 1.2);
				if ($buyout_price && $need_money > $buyout_price) {
					$need_money = $buyout_price
				}
				if ( $in{money} >= $need_money && &is_buyable($kind, $item_no)) {
					my $item_title = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
								   : $kind eq '2' ? "[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
								   : $kind eq '3' ? "[�y]$pets[$item_no][1]��$item_c"
								   : 				"[�h]$guas[$item_no][1]"
								   ;
					
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
				my $item_title = $kind eq '1' ? "[$weas[$item_no][2]]$weas[$item_no][1]��$item_lv($item_c/$weas[$item_no][4])"
							   : $kind eq '2' ? "[��]$eggs[$item_no][1]($item_c/$eggs[$item_no][2])"
							   : $kind eq '3' ? "[�y]$pets[$item_no][1]��$item_c"
							   : 				"[�h]$guas[$item_no][1]"
							   ;
				
				my $to_id = unpack 'H*', $to_name;
				if(-e "$userdir/$to_id/user.cgi"){
					&send_item($to_name, $kind, $item_no, $item_c, $item_lv, 1);
				}
				&send_money($to_name, '�����݉��', "-$item_price");
				&send_money($from_name, '�����݉��', $item_price);
				&sale_data_log($kind, $item_no, $item_c, $item_lv, $item_price, 2);
				&write_send_news("$from_name�̏o�i����$item_title��$to_name�� $item_price G�ŗ��D���܂���");
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

#=================================================
# �o�i
#=================================================
sub tp_200 {
	$layout = 1;
	$mes .= '�ǂ���o�i���܂���?<br>';
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1">$weas[$m{wea}][1]��$m{wea_lv}($m{wea_c})<br>| if $m{wea};
	$mes .= qq|<input type="radio" name="cmd" value="2">$eggs[$m{egg}][1]($m{egg_c})<br>| if $m{egg};
	$mes .= qq|<input type="radio" name="cmd" value="3">$pets[$m{pet}][1]��$m{pet_c}<br>| if $m{pet};
	$mes .= qq|<input type="radio" name="cmd" value="4">$guas[$m{gua}][1]<br>| if $m{gua};
	$mes .= qq|���D����<br>|;
	$mes .= qq|<input type="radio" name="tlimit" value="0" checked>����<br>|;
	$mes .= qq|<input type="radio" name="tlimit" value="1">����<br>|;
	$mes .= qq|<input type="radio" name="tlimit" value="2">�Z��<br>|;
	$mes .= qq|<p>�������z<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<p>�������z<input type="text" name="buyout_price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�o�i����" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1..4);
	
	my $is_find = 0;
	my @lines = ();
	open my $fh, "< $this_file" or &error("$this_file ���J���܂���ł���");
	while (my $line = <$fh>) {
		my($name) = (split /<>/, $line)[6];
		if (!$is_find && $m{name} eq $name) {
			$is_find = 1;
		}
		push @lines, $line;
	}
	close $fh;
	
	if ($is_find) {
		$mes .= '�o�i���Ă�����̂����D�����܂ŁA�o�i���邱�Ƃ͂ł��܂���<br>';
	}
	elsif (@lines >= $max_auction) {
		$mes .= '���݁A�o�i�̎�t�͂��Ă���܂���<br>�o�i���������Ă���ēx�\\�����݂�������<br>';
	}
	elsif ($in{price} =~ /[^0-9]/ || $in{price} >= 4999999 || $in{price} < 5) {
		$mes .= '�l�i�� 5 G�ȏ� 499��9999 G�ȓ��ɂ���K�v������܂�<br>';
	}
	elsif ($in{buyout_price} =~ /[^0-9]/ || $in{buyout_price} >= 4999999) {
		$mes .= '�����l�i�� 499��9999 G�ȓ��ɂ���K�v������܂�<br>';
	}
	elsif ( ($cmd eq '1' && $m{wea})
		 || ($cmd eq '2' && $m{egg})
		 || ($cmd eq '3' && $m{pet})
		 || ($cmd eq '4' && $m{gua}) ) {
			
			my @kinds = ('', 'wea', 'egg', 'pet', 'gua');
			for my $taboo_item (@{ $taboo_items{ $kinds[$cmd] } }) {
				if ($taboo_item eq $m{ $kinds[$cmd] }) {
					my $t_item_name = $cmd eq '1' ? $weas[$m{wea}][1]
									: $cmd eq '2' ? $eggs[$m{egg}][1]
									: $cmd eq '3' ? $pets[$m{pet}][1]
									:               $guas[$m{gua}][1]
									;
					$mes .= "$t_item_name�͏o�i�֎~���тƂȂ��Ă���܂�<br>";
					&begin;
					return;
				}
			}
			
			my $item_price = $in{price} || 0;
			my $buyout_price = $in{buyout_price} || 0;
			my $item_no = $m{ $kinds[$cmd]       };
			my $item_c  = $m{ $kinds[$cmd].'_c'  } || 0;
			my $item_lv = $m{ $kinds[$cmd].'_lv' } || 0;
			
			if ($cmd eq '1' && $m{wea}) {
				if($m{wea_name}){
					$mes .= "������̎�𗣂ꂽ�r�[$m{wea_name}�͂�����$weas[$m{wea}][1]�ɂȂ��Ă��܂���<br>";
					$m{wea_name} = "";
				}
				&mes_and_send_news("$weas[$m{wea}][1]���o�i���܂���");
				$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
			}
			elsif ($cmd eq '2' && $m{egg}) {
				&mes_and_send_news("$eggs[$m{egg}][1]���o�i���܂���");
				$m{egg} = $m{egg_c} = 0;
			}
			elsif ($cmd eq '3' && $m{pet}) {
				&mes_and_send_news("$pets[$m{pet}][1]��$m{pet_c}���o�i���܂���");
				$m{pet} = 0;
			}
			elsif ($cmd eq '4' && $m{gua}) {
				&mes_and_send_news("$guas[$m{gua}][1]���o�i���܂���");
				$m{gua} = 0;
			}
			
			my $bit_time = $time + int( $limit_day * 3600 * 24 + rand(3600) ); # ���D���Ԃ��P���Ԓ��x�΂炯����
			$bit_time += int( 3600 * 24 + rand(3600) ) if $in{tlimit} eq '1'; 
			$bit_time -= int( 3600 * 24 + rand(3600) ) if $in{tlimit} eq '2'; 
			my($last_no) = (split /<>/, $lines[-1])[1];
			++$last_no;
			open my $fh2, ">> $this_file" or &error("$this_file ���J���܂���ł���");
			print $fh2 "$bit_time<>$last_no<>$cmd<>$item_no<>$item_c<>$item_lv<>$m{name}<>$m{name}<>$item_price<>$buyout_price<>\n";
			close $fh2;
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
