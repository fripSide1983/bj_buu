my $this_file = "$logdir/$m{country}/depot.cgi";
my $this_log = "$logdir/$m{country}/depot_log.cgi";
#=================================================
# ����
#=================================================

# �ő�ۑ���
my $max_depot = 30;

# ���p�\������(������1���㎞�̂�)
my($need_lv, $need_sedai, $top_message) = &status_check;

$need_lv ||= 5;

# ���p�\�Ȑ���
$need_sedai ||= 1;

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
	$mes .= "���p�\\����F$need_sedai ���x���F$need_lv<br>$top_message<br>";
	if ($m{tp} > 1) {
		$mes .= "���ɉ������܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "�����͍��ɂł��B$max_depot�܂ŗa���邱�Ƃ��ł��܂�<br>";
		$mes .= "�ǂ����܂���?<br>";
	}
	&menu('��߂�', '���o��', '�a����', '��������','�����m�F', '�V�K�p');
#	&menu('��߂�', '���o��', '�a����', '��������','�����m�F','���D');
}
sub tp_1 {
#	return if &is_ng_cmd(1..5);
	return if &is_ng_cmd(1..5);
	
	if ($cmd eq '5') {
		$m{lib} = 'depot_country_beginner';
		$mes .= "�����͐V�K�p���ɂł��B10�܂ŗa���邱�Ƃ��ł��܂�<br>";
		$mes .= "�ǂ����܂���?<br>";
		&menu('��߂�', '���o��', '�a����', '��������','�����m�F');
	} else {
		$m{tp} = $cmd * 100;
		&{ 'tp_'. $m{tp} };
	}
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
	if ($m{sedai} < $need_sedai || ($m{sedai} == $need_sedai && $m{lv} < $need_lv)) {
		$mes .= "$need_sedai ��������$need_lv�����̐l�͎g�����Ƃ��ł��܂���<br>";
	} else {
		if ($cmd) {
			my $count = 0;
			my $new_line = '';
			my $flag = 1;
			my @lines = ();
			open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
			eval { flock $fh, 2; };
			my $head_line = <$fh>;
			push @lines, $head_line;
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
	
	if (@lines >= $max_depot+1) {
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
	my $head_line = <$fh>;
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
	unshift @lines, $head_line;
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
# ���D
#=================================================
sub tp_600 {
	$mes .= "�ǂ̍��̍��ɂ��P�����܂���?($GWT��)<br>";
	&menu('��߂�', @countries);
	$m{tp} += 10;
}

sub tp_610 {
	return if &is_ng_cmd(1..$w{country});
	
	if ($m{country} eq $cmd) {
		$mes .= '�����͑I�ׂ܂���<br>';
		&begin;
	}
	elsif ($union eq $cmd) {
		$mes .= '�������͑I�ׂ܂���<br>';
		&begin;
	}
	elsif ($cs{is_die}[$cmd] ne '1') {
		$mes .= '�ŖS���Ă��Ȃ����͑I�ׂ܂���<br>';
		&begin;
	}
	else {
		$m{tp} += 10;
		$y{country} = $cmd;
		
		$mes .= "$cs{name}[$y{country}]�Ɍ������܂���<br>";
		$mes .= "$GWT����ɓ�������\\��ł�<br>";
		
		&wait;
	}
}

sub tp_620 {
	$mes .= "$c_y�ɓ������܂���<br>";
	$m{tp} += 10;
	$m{value} = int(rand(20))+5;
	$m{stock} = 0;
	$m{turn} = 0;
	$mes .= "�G���̋C�z�y $m{value}% �z<br>";
	$mes .= '�ǂ����܂���?<br>';
	&menu('���D����','����������');
	$m{value} += int(rand(10)+1);
}

sub loop_menu {
	$mes .= "�G���̋C�z�y $m{value}% �z<br>";
	$mes .= '�ǂ����܂���?';
	&menu('������', '��߂�');
}

sub tp_630 {
	if ($cmd eq '0') { # ���s
		if ( $m{value} > rand(110)+35 ) { # ���s �P����rand(100)�ɂ����30%���炢�Ō������Ă��܂��̂� rand(110)+30�ɕύX
			$mes .= "�G���Ɍ������Ă��܂���!!<br>";
			
			$m{tp} = 560;
			&n_menu;
		}
		else { # ����
			++$m{turn};
			$m{tp} += 10;
			&{ 'tp_'.$m{tp} };
			&loop_menu;
			$m{tp} -= 10;
		}
		$m{value} += int(rand(10)+1);
	}
	elsif ($cmd eq '1') { # �ދp
		$mes .= '�����グ�邱�Ƃɂ��܂�<br>';
		
		if ($m{turn} <= 0) { # �������Ȃ��ň����グ
			&refresh;
			&n_menu;
		}
		else {
			$m{tp} += 20;
			&{ 'tp_'.$m{tp} };
			$m{tp} = 570;
			&n_menu;
		}
	}
	else {
		&loop_menu;
	}
}


sub tp_640{
	$mes .= "���ɂ�T��܂���!<br>[ �A��$m{turn}�񐬌�]<br>";
}

sub tp_650 {
	if(int(rand(1)) < $m{turn}) {
		my $count = 0;
		my $new_line = '';
		my @lines = ();
		my $number = int(rand(100));
		open my $fh, "+< $logdir/$y{country}/depot.cgi" or &error("$logdir/$y{country}/depot.cgi���J���܂���");
		eval { flock $fh, 2; };
		my $head_line = <$fh>;
		push @lines, $head_line;
		while (my $line = <$fh>) {
			++$count;
			if (!$new_line && $number eq $count) {
				$new_line = $line;
			}
			else {
				push @lines, $line;
			}
		}
		if ($new_line) {
			seek  $fh, 0, 0;
			truncate $fh, 0; 
			print $fh @lines;
			close $fh;
			
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line;
			$mes .= &get_item_name($kind, $item_no);
			$mes .= "��D���܂���<br>";

			my @log_lines = ();
			open my $lfh, "+< $logdir/$y{country}/depot_log.cgi" or &error("$logdir/$y{country}/depot_log.cgi���J���܂���");
			eval { flock $lfh, 2; };
			my $log_count = 0;
			while (my $log_line = <$lfh>){ 
			      push @log_lines, $log_line;
			      $log_count++;
			      last if $log_count > 30;
			}
			unshift @log_lines, "$kind<>$item_no<>$item_c<>$item_lv<>$m{name}<>2<>\n";
			seek  $lfh, 0, 0;
			truncate $lfh, 0;
			print $lfh @log_lines;
			close $lfh;

			my @mlines = ();
			open my $mfh, "+< $this_file" or &error("$this_file���J���܂���");
			eval { flock $mfh, 2; };
			push @mlines, $_ while <$mfh>;
	
			push @mlines, $new_line;
			seek  $mfh, 0, 0;
			truncate $mfh, 0;
			print $mfh @mlines;
			close $mfh;

			my @mlog_lines = ();
			open my $lmfh, "+< $this_log" or &error("$this_file���J���܂���");
			eval { flock $lmfh, 2; };
			my $mlog_count = 0;
			while (my $mlog_line = <$lmfh>){ 
			      push @mlog_lines, $mlog_line;
			      $mlog_count++;
			      last if $mlog_count > 30;
			}
			unshift @mlog_lines, "$kind<>$item_no<>$item_c<>$item_lv<>$m{name}<>1<>\n";
			seek  $lmfh, 0, 0;
			truncate $lmfh, 0;
			print $lmfh @mlog_lines;
			close $lmfh;
		}
		else {
			$mes .= "�����D���܂���ł���<br>";
			close $fh;
		}
	}else {
		$mes .= "�����D���܂���ł���<br>";
	}
	$m{tp} = 570;
	&n_menu;
	&write_cs;
}

sub tp_660 {
	$m{act} += $m{turn};

	# ����
	&refresh;
	&write_world_news("$c_m��$m{name}�����ɗ��D�Ɏ��s��$c_y�̘S���ɗH����܂���");
	&add_prisoner;
	my $v = int( (rand(4)+1) );
	$m{exp} += $v;
	$m{rank_exp}-= int(rand(6)+5);
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
}

sub tp_670 {
	$m{act} += $m{turn};

	my $v = int( rand(2) * $m{turn} );
	$m{exp} += $v;
	$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
	$m{egg_c} += int(rand($m{turn})+$m{turn}) if $m{egg};

	if ($m{turn} >= 10) {
		$mes .= "�C���ɑ听��!$m{name}�ɑ΂���]�����傫���オ��܂���<br>";
		$m{rank_exp} += $m{turn} * 3;
	}
	else {
		$mes .= "�C���ɐ���!$m{name}�ɑ΂���]�����オ��܂���<br>";
		$m{rank_exp} += int($m{turn} * 1.5);
	}

	&write_cs;
	&refresh;
	&n_menu;
}

#=================================================
# <input type="radio" �t�̗a���菊�̕�
#=================================================
sub radio_my_depot {
	my $count = 0;
	my $sub_mes = qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	my $head_line = <$fh>;
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


sub status_check {
	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	my $head_line = <$fh>;
	my($lv_s,$sedai_s,$message_s) = split /<>/, $head_line;
	close $fh;
	
	return $lv_s,$sedai_s,$message_s;
}

1; # �폜�s��
