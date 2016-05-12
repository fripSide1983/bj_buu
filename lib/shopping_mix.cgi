my $depot_file = "$userdir/$id/depot.cgi";
#================================================
# �ΑK��
#=================================================
# ���߯�
my @bad_pets = (126,197);

# ���A�߯�
my @good_pets = (3,7,8,17,18,19,20,21,58,59,60,63,127,150,151,183);

# �������E
my $max_mix = 20;

# �ߋ��̉h���ɕ\�������Œ�l
my $dragon_nest = 10;

# �ő�ۑ���
my $max_depot = $m{sedai} > 7 ? 50 : $m{sedai} * 5 + 15;
$max_depot += $m{depot_bonus} if $m{depot_bonus};

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ��������?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�h���N�G�H�m����<br>';
		$mes .= '�������̃y�b�g�Ɨa�菊�ɂ����߯Ă������ł����I��I<br>';
	}
	
	&menu('��߂�','�߯Ă���������','�܂Ƃ߂č���', '�����т̗r���Ւd��', '�����\�y�b�g���m�F');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	$layout = 2;
	if($cmd eq '1'){
		$mes .= "�ǂ�ƍ������܂���?<br>";
		$mes .= qq|<form method="$method" action="$script"><input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">��߂�</label><br>|;
	
		open my $fh, "< $depot_file" or &error("$depot_file ���ǂݍ��߂܂���");
		my $count = 0;
		while (my $line = <$fh>) {
			++$count;
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			if($kind eq '3' ){
				$mes .= qq|<input type="radio" id="$count" name="cmd" value="$count"><label for="$count">[��]$pets[$item_no][1]��$item_c</label><br>|;
			}
		}
		close $fh;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= $is_mobile ? qq|<p><input type="submit" value="��������" class="button1" accesskey="#"></p></form>|:
			qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
	} elsif ($cmd eq '4') {
		$mes .= "�������\\�Ȃ̂�<br>";
		my $line_i = 0;
		for my $pi (1..$#pets) {
			if ($pets[$pi][5] && $pi ne'180' && $pi ne'181') {
				$mes .= $pets[$pi][1] . ", ";
				$line_i++;
				if ($line_i > 5) {
					$mes .= "<br>";
					$line_i = 0;
				}
			}
		}
		$mes .= "<br>����B";
		&begin;
		return;
	}else{
		$mes .= "�ǂ�ƍ������܂���?<br>";
		$mes .= qq|<form method="$method" action="$script">|;
	
		open my $fh, "< $depot_file" or &error("$depot_file ���ǂݍ��߂܂���");
		my $count = 0;
		while (my $line = <$fh>) {
			++$count;
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			if($kind eq '3' ){
				my $checked = '';
				if ($cmd eq '3' && $item_no == 126) {
					$checked = ' checked';
				}
				$mes .= qq|<input type="checkbox" id="$count" name="pet_$count" value="1"$checked><label for="$count">[��]$pets[$item_no][1]��$item_c</label><br>|;
			}
		}
		close $fh;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= $is_mobile ? qq|<p><input type="submit" value="��������" class="button1" accesskey="#"></p></form>|:
			qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
		$cmd = 2;
	}
	$m{tp} = $cmd * 100;
}

#=================================================
# ����
#=================================================
sub tp_100 {
	if($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]){
		$mes .= "$shogos[1][0]�͍����ł��Ȃ��B�c�O<br>";
		&begin;
		return;
	}
	if($m{is_full}){
		$mes .= "�a�菊�������ς��ō��������߯Ă�����Ȃ���<br>";
		&begin;
		return;
	}
	unless ($pets[$m{pet}][5]) {
		$mes .= "�N���������Ă��߯Ă͍����ł��Ȃ��񂾁B���߂��<br>";
		&begin;
		return;
	}
	
	if ($cmd) {
		my $count = 0;
		my $pet_no;
		my $pet_c;
		my @lines = ();
		open my $fh, "+< $depot_file" or &error("$depot_file���J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			++$count;
			if ($cmd eq $count) {
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
				if($kind eq '3' && &mix($item_no, 0) == -1){
					push @lines, $line;
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
	&begin;	
}

#=================================================
# �ꊇ����
#=================================================
sub tp_200 {
	if($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]){
		$mes .= "$shogos[1][0]�͍����ł��Ȃ��B�c�O<br>";
		&begin;
		return;
	}
	unless ($pets[$m{pet}][5]) {
		$mes .= "�N���������Ă��߯Ă͍����ł��Ȃ��񂾁B���߂��<br>";
		&begin;
		return;
	}
	
	open my $fh, "< $depot_file" or &error("$depot_file ���ǂݍ��߂܂���");
	my $count = 0;
	my $rest = 0;
	while (my $line = <$fh>) {
		++$count;
		 $rest++ unless $in{"pet_$count"};
		# ������������Ă��ǂ�����
#		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
#		unless($in{"pet_$count"}){
#			$rest++;
#		}
	}
	close $fh;
	if($rest > $max_depot){
		$mes .= "�a�菊�������ς��ō��������߯Ă�����Ȃ���<br>";
		&begin;
		return;
	}
# �t�@�C���J���O�Ɋm�F����΃X�}�[�g
#	unless ($pets[$m{pet}][5]) {
#		$mes .= "�N���������Ă��߯Ă͍����ł��Ȃ��񂾁B���߂��<br>";
#		&begin;
#		return;
#	}
	
	$count = 0;
	my @lines = ();
	my %duplication = ();
	open my $fh, "+< $depot_file" or &error("$depot_file���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$count;
		if ($in{"pet_$count"}) {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			$no_logging = $duplication{$item_no};
			$duplication{$item_no}++;
			if(&mix($item_no, $no_logging) == -1){
				push @lines, $line;
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

	&begin;	
}

sub mix{
	my $pet_no = shift;
	my $no_logging = shift;
	
	if($m{pet_c} >= $max_mix){
		$mes .= "�����߯Ă͂���ȏ㍇���ł��Ȃ���<br>";
		&begin;
		return -1;
	}
	if (!$no_logging) {
		&sale_data_log(3, $pet_no, 0, 0, 500, 5);
	}
	
	my $good_bad = 1;
	for my $bpet (@bad_pets){
		if($bpet == $pet_no){
			$good_bad = 1.5;
			last;
		}
	}
	for my $gpet (@good_pets){
		if($gpet == $pet_no){
			$good_bad = 0.5;
			last;
		}
	}
	
	if(rand(&fib($m{pet_c}))*$good_bad < 1){
		$m{pet_c}++;
		$mes .= "�����ɐ���������N���߯Ă�$pets[$m{pet}][1]��$m{pet_c}�ɂȂ�����<br>";
		if($m{pet_c} >= $dragon_nest){
			&mes_and_world_news("$pets[$m{pet}][1]��$m{pet_c}�̍����ɐ������܂����B", 1);
		}
	}else{
		$mes .= "�c�O�����Ɏ��s������<br>";
	}
}

sub fib{
	my $x = shift;
	my @fib_rets = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 2000, 5000, 10000, 20000, 50000, 100000);
	return $fib_rets[$x];
}
1; # �폜�s��
