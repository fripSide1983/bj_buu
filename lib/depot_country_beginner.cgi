my $this_file = "$logdir/$m{country}/depot_b.cgi";
my $this_log = "$logdir/$m{country}/depot_b_log.cgi";
#=================================================
# �V�K�p����
#=================================================

# �ő�ۑ���
my $max_depot = 10;

# �a�����Ȃ�����
my %taboo_items = (
	wea => [32,], # ����
	egg => [], # �Ϻ�
	pet => [127,138,188], # �߯�
	gua => [], # �h��
);

sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '���ɑ����ĂȂ��ƍs�����Ƃ��ł��܂���<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}
#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "���ɉ������܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "�����͐V�K�p���ɂł��B$max_depot�܂ŗa���邱�Ƃ��ł��܂�<br>";
		$mes .= "�ǂ����܂���?<br>";
	}
	unless (-f $this_file) {
		open my $fh, "> $this_file" or &error("$this_file���J���܂���");
		close $fh;
	}
	unless (-f $this_log) {
		open my $fh, "> $this_log" or &error("$this_log���J���܂���");
		close $fh;
	}
	&menu('��߂�', '���o��', '�a����', '��������','�����m�F');
}
sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# ���o��
#=================================================
sub tp_100 {
	$layout = 2;
	my($count, $sub_mes) = &radio_my_depot;

	$mes .= "�ǂ�����o���܂���? [ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .=  $is_mobile ? qq|<p><input type="submit" value="���o��" class="button1" accesskey="#"></p></form>|:
		qq|<p><input type="submit" value="���o��" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_110 {
	if ($cmd) {
		my $count = 0;
		my $new_line = '';
		my $flag = 1;
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			++$count;
			if (!$new_line && $cmd eq $count) {
				$new_line = $line;
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
				
				if ($kind eq '1' && $m{wea}) {
					$mes .= "���ɕ�����������Ă��܂�";
					$flag = 0;
				}
				elsif ($kind eq '2' && $m{egg}) {
					$mes .= "���ɗ����������Ă��܂�";
					$flag = 0;
				}
				elsif($kind eq '3' && $m{pet}) {
					$mes .= "�����߯Ă��������Ă��܂�";
					$flag = 0;
				}
				elsif($kind eq '4' && $m{gua}) {
					$mes .= "���ɖh����������Ă��܂�";
					$flag = 0;
				}
			}
			else {
				push @lines, $line;
			}
		}
		if ($new_line && $flag) {
			seek  $fh, 0, 0;
			truncate $fh, 0; 
			print $fh @lines;
			close $fh;
			
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line;
			if ($kind eq '1') {
				$m{wea}    = $item_no;
				$m{wea_c}  = $item_c;
				$m{wea_lv} = $item_lv;
				$mes .= "$weas[$m{wea}][1]�����o���܂���<br>";
			}
			elsif ($kind eq '2') {
				$m{egg}    = $item_no;
				$m{egg_c}  = $item_c;
				$mes .= "$eggs[$m{egg}][1]�����o���܂���<br>";
			}
			elsif ($kind eq '3') {
				$m{pet}    = $item_no;
				$m{pet_c}  = $item_c;
				$mes .= "$pets[$m{pet}][1]��$m{pet_c}�����o���܂���<br>";

				if (-f "$userdir/$id/pet_icon.cgi") {
					open my $ifh, "< $userdir/$id/pet_icon.cgi";
					my $line = <$ifh>;
					close $ifh;
					if (index($line, "<>$m{pet}_") >= 0) {
						$line =~ s/.*<>($m{pet}_.*?)<>.*/$1/;
						$m{icon_pet} = $line;
					}
					else {
						$m{icon_pet} = '';
					}
				}
			}
			elsif ($kind eq '4') {
				$m{gua}    = $item_no;
				$mes .= "$guas[$m{gua}][1]�����o���܂���<br>";
			}

			my @log_lines = ();
			open my $lfh, "+< $this_log" or &error("$this_file���J���܂���");
			eval { flock $lfh, 2; };
			my $log_count = 0;
			while (my $log_line = <$lfh>){ 
			      push @log_lines, $log_line;
			      $log_count++;
			      last if $log_count > 30;
			}
			unshift @log_lines, "$kind<>$item_no<>$item_c<>$item_lv<>$m{name}<>0<>\n";
			seek  $lfh, 0, 0;
			truncate $lfh, 0;
			print $lfh @log_lines;
			close $lfh;

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
	push @menus, $m{pet} > 0 ? $pets[$m{pet}][1] : '';
	push @menus, $m{gua} ? $guas[$m{gua}][1] : '';
	
	&menu(@menus);
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1..4);
	if ($cmd eq '1' && $m{wea_name}) {
		$mes .= "�B�ꖳ��̕����a���邱�Ƃ͂ł��܂���<br>";
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
			$mes .= "$t_item_name�͗a���邱�Ƃ͂ł��܂���<br>";
			&begin;
			return;
		}
	}
	my $line;
	my $sub_line;
	if ($cmd eq '1' && $m{wea}) {
		$line = "$cmd<>$m{wea}<>$m{wea_c}<>$m{wea_lv}<>\n";
		$sub_line = "$cmd<>$m{wea}<>$m{wea_c}<>$m{wea_lv}<>$m{name}<>1<>\n";
	}
	elsif ($cmd eq '2' && $m{egg}) {
		$line = "$cmd<>$m{egg}<>$m{egg_c}<>0<>\n";
		$sub_line = "$cmd<>$m{egg}<>$m{egg_c}<>0<>$m{name}<>1<>\n";
	}
	elsif ($cmd eq '3' && $m{pet} > 0) {
		$line = "$cmd<>$m{pet}<>$m{pet_c}<>0<>\n";
		$sub_line = "$cmd<>$m{pet}<>$m{pet_c}<>0<>$m{name}<>1<>\n";
	}
	elsif ($cmd eq '4' && $m{gua}) {
		$line = "$cmd<>$m{gua}<>0<>0<>\n";
		$sub_line = "$cmd<>$m{gua}<>0<>0<>$m{name}<>1<>\n";
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
				$m{wea_c} = 0;
				$m{wea_lv} = 0;
				$mes .= "������̎�𗣂ꂽ�r�[$m{wea_name}�͂�����$weas[$m{wea}][1]�ɂȂ��Ă��܂���";
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
			$m{icon_pet} = '';
		}
		elsif ($cmd eq '4') {
			$mes .= "$guas[$m{gua}][1]��a���܂���<br>";
			$m{gua} = 0;
		}
		
			my @log_lines = ();
			open my $lfh, "+< $this_log" or &error("$this_file���J���܂���");
			eval { flock $lfh, 2; };
			my $log_count = 0;
			while (my $log_line = <$lfh>){ 
			      push @log_lines, $log_line;
			      $log_count++;
			      last if $log_count > 30;
			}
			unshift @log_lines, $sub_line;
			seek  $lfh, 0, 0;
			truncate $lfh, 0;
			print $lfh @log_lines;
			close $lfh;
	}
	&begin;
}

#=================================================
# ����
#=================================================
sub tp_300 {
	my @lines = ();
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
# ���O�m�F
#=================================================
sub tp_400 {
	my @lines = ();
	open my $fh, "< $this_log" or &error("$this_log���J���܂���");
	while (my $line = <$fh>){
		my($kind, $item_no, $item_c, $item_lv, $name, $type) = split /<>/, $line;
		$mes .= "$name ��";
		$mes .= &get_item_name($kind, $item_no, $item_c, $item_lv);
		$mes .= "��";
		$mes .= $type eq '1' ? "�a���܂���<br>":
					$type eq '0' ? "�����o���܂���<br>":
								"�D���܂���<br>";
	}
	close $fh;
	&begin;
}

#=================================================
# <input type="radio" �t�̗a���菊�̕�
#=================================================
sub radio_my_depot {
	unless (-f $this_file) {
		open my $fh, "> $this_file" or &error("$this_file���J���܂���");
		close $fh;
	}
	unless (-f $this_log) {
		open my $fh, "> $this_log" or &error("$this_log���J���܂���");
		close $fh;
	}
	my $count = 0;
	my $sub_mes = qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		$sub_mes .= qq|<input type="radio" id="$count" name="cmd" value="$count">|;
		$sub_mes .= qq|<label for="$count">| unless $is_mobile;
		$sub_mes .= &get_item_name($kind, $item_no, $item_c, $item_lv);
		$sub_mes .= qq|</label>| unless $is_mobile;
		$sub_mes .= qq|<br>|;
	}
	close $fh;
	
	return $count, $sub_mes;
}

1; # �폜�s��
