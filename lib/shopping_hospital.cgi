#=================================================
# ���\���a�@ Created by Merino
#=================================================

# ------------------
# ���`��p�̱��ݕ\��
# [PC]�ꗗ�\���̐܂�Ԃ���
my $tr = 10;

# [�g��]�P�߰�ނ̕\����
my $max_mobile_icon = 30;

# ------------------
# �ް��ƂȂ���z
my $base_price = $m{sedai} > 8 ? 400 + ($m{lv} * 10) : ($m{sedai} * 50) + ($m{lv} * 10);

# �ƭ�
my @menus = (
	# �ƭ���,		�l�i
	['��߂�',		0],
	['����',		$base_price * 20],
	['���]����p',	$base_price * 50],
	['����а��p',	500000],
	['���`��p',	1000], # ���݂��g��Ȃ��ꍇ�͂��̍s�� sub tp_400�ȍ~���폜����OK
	['��֌���',	1000], # ���݂��g��Ȃ��ꍇ�͂��̍s�� sub tp_400�ȍ~���폜����OK
	['�����X�V',	10000], # ���݂��g��Ȃ��ꍇ�͂��̍s�� sub tp_400�ȍ~���폜����OK
);


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ�������܂�����?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '���\���a�@�ւ悤������<br>�{���͂ǂ̂悤�Ȃ��p���ł��傣����?';
	}
	
	&menu(map { $_->[0] } @menus);
}
sub tp_1 {
	return if &is_ng_cmd(1..$#menus+1);
	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#================================================
# ����
#================================================
sub tp_100 {
	$mes .= "$menus[1][0]�킟�A�M���̏���������Ƃ��ł����悧<br>";
	$mes .= "���������A$menus[1][1] G�̂�����������̂�<br>";
	$mes .= "�ǂ����那�H<br>";
	$m{tp} += 10;
	&menu("��߂�", "$menus[1][0]����");
}
sub tp_110 {
	return if &is_ng_cmd(1);

	if ($m{money} >= $menus[1][1]) {
		$mes .= "���m�̐_��̗͂��g���ċM���̑̂������悧<br>";
		$mes .= "������Aʯ�٩�`ʯ�٩�`�􌳋C�ɂȂ����ł���<br>";
		$mes .= "���������K�v�ɂȂ�����܂����Ă�<br>";
		$m{hp} = $m{max_hp};
		$m{mp} = $m{max_mp};
		$m{money} -= &use_pet('hospital',$menus[1][1]);
		&refresh;
		&n_menu;
	}
	else {
		$mes .= '���炟�A����������܂���킟<br>';
		&begin;
	}
}

#================================================
# ���]��
#================================================
sub tp_200 {
	$mes .= "$menus[2][0]������ƁA$sexes[$m{sex}]����Ȃ��Ȃ����Ⴄ���ǂ����̂����炟?<br>";
	$mes .= "��p������ɂ́A$menus[2][1] G�Ǝ�p����$GWT���K�v�悧<br>";
	$mes .= "�ǂ����那�H<br>";
	$m{tp} += 10;
	&menu("��߂�", "$menus[2][0]����");
}
sub tp_210 {
	return if &is_ng_cmd(1);

	if ($m{money} >= $menus[2][1]) {
		$mes .= '������ł��Ď�p���n�߂���<br>';
		$mes .= '���ɖڊo�߂��Ƃ��ɂ킟�ʐl�ƂȂ��Ă����悧<br>';
		$m{sex} = $m{sex} eq '1' ? 2 : 1;
		$m{hp}  = $m{max_hp};
		$m{mp}  = $m{max_mp};
		$m{act} = 0;
		$m{money} -= $menus[2][1];
		if ($m{job} eq '22' || $m{job} eq '23') {
			$m{job} = 0;
		}
		&refresh;
		&wait;
		&write_memory("�ӂ������� $sexes[$m{sex}] �ɐ��]����p�����܂���");
	}
	else {
		$mes .= '���炟�A����������܂���킟<br>';
		&begin;
	}
}

#================================================
# ����а��p
#================================================
sub tp_300 {
	$mes .= "$menus[3][0]������Ƃ��A�M���̂����O���߽ܰ�ނ�ς��邱�Ƃ��ł���킟<br>";
	$mes .= "������ĥ���ޥȑ��p�����炟�A$cs{name}[0]�̕��������邱�Ƃ��ł��Ȃ��̂�<br>" if $m{country};
	$mes .= "��p������ɂ́A$menus[3][1] G�Ǝ�p����$GWT���K�v�悧<br>";
	$mes .= "��p������Ƃ��A���ݗ��p���Ă����s�̂����͂Ȃ��Ȃ��Ă��܂���悧<br>" if $m{bank};
	$mes .= "�ǂ����那�H<br>";
	$m{tp} += 10;
	&menu("��߂�", "$menus[3][0]����");
}
sub tp_310 {
	return if &is_ng_cmd(1);
	if ($m{country}) {
		$mes .= "$cs{name}[0]�ɂȂ��Ă��炟�A�܂����Ă�<br>";
		&begin;
		return;
	}

	$mes .= qq|����ł킟�A�V���������O���߽ܰ�ނ������Ă�<br>|;
	$mes .= qq|<form method="GET" action="$script"><table class="table1">|;
	$mes .= qq|<tr><td><tt>��ڲ�-���F</tt></td><td><input type="text" name="new_name" value="$m{name}" class="text_box1"><br></td></tr>|;
	$mes .= qq|<tr><td><tt>�߽ܰ�� �F</tt></td><td><input type="text" name="new_pass" value="$m{pass}" class="text_box1"><br></td></tr>|;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�m��" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_320 {
	if ($m{country}) {
		$mes .= "$cs{name}[0]�ɂȂ��Ă��炟�A�܂����Ă�<br>";
		&begin;
		return;
	}
	elsif ($m{money} < $menus[3][1]) {
		$mes .= '���炟�A����������܂���킟<br>';
		&begin;
		return;
	}
	elsif (!$in{new_name} && $in{new_pass} eq '') {
		&begin;
		return;
	}
	elsif ($in{new_name} eq $m{name} && $in{new_pass} eq $m{pass}) {
		&begin;
		return;
	}

	&error('��ڲ�-�������͂���Ă��܂���')	unless $in{new_name};
	&error('�߽ܰ�ނ����͂���Ă��܂���')	if $in{new_pass} eq '';

	&error('��ڲ�-���ɕs���ȕ���( ,;\"\'&<>\\\/ )���܂܂�Ă��܂�')	if $in{new_name} =~ /[,;\"\'&<>\\\/]/;#"
	&error('��ڲ�-���ɕs���ȋ󔒂��܂܂�Ă��܂�')				if $in{new_name} =~ /�@/ || $in{new_name} =~ /\s/;
	&error('��ڲ�-���͑S�p6(���p12)�����ȓ��ł�')				if length($in{new_name}) > 12;
	&error('�߽ܰ�ނ͔��p�p�����œ��͂��ĉ�����')				if $in{new_pass} =~ m/[^0-9a-zA-Z]/;
	&error('�߽ܰ�ނ͔��p�p����4�`12�����ł�')					if length $in{new_pass} < 4 || length $in{new_pass} > 12;
	&error('��ڲ�-�����߽ܰ�ނ����ꕶ����ł�')					if $in{new_name} eq $in{new_pass};

	unless ($m{name} eq $in{new_name}) {
		my $new_id = unpack 'H*', $in{new_name};
		&error('���̖��O�͂��łɎg���Ă��܂�') if -d "$userdir/$new_id";
		&write_world_news("$m{name} �� $in{new_name} �Ɖ��������܂���", 1);

		rename "$userdir/$id", "$userdir/$new_id" or &error('���O�̕ϊ��Ɏ��s���܂���');

		my @lines = ();
		open my $fh, "+< $logdir/0/member.cgi" or &error("$cs{name}[0]�����ް̧�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			$line =~ tr/\x0D\x0A//d;
			next if $line eq $m{name};
			push @lines, "$line\n";
		}
		push @lines, "$in{new_name}\n";
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;

		$id = $new_id;
		$m{name} = $in{new_name};
		$mes .= qq|<font color="#FF0000">�V��ڲ԰��:$in{new_name}</font><br>|;
	}

	unless ($m{pass} eq $in{new_pass}) {
		$m{pass} = $in{new_pass};
		$pass    = $in{new_pass};
		$mes .= qq|<font color="#FF0000">�V�߽ܰ��:$in{new_pass}</font><br>|;
	}
	
	$m{hp}  = $m{max_hp};
	$m{mp}  = $m{max_mp};
	$m{act} = 0;
	$m{bank} = '';
	$m{money} -= $menus[3][1];
	&refresh;
	&wait;
	
	$mes .= qq|�̂̋M���͂������݂��Ȃ��킟<br><font color="#FF0000"><b>�V�������O���߽ܰ�ނ�Y��Ȃ��悤�ɂ�</b></font><br>|;
	$mes .= qq|[���񂩂���͏ȗ�]����������ꂢ�Ă���l�킟�A��x۸޲݂�����������������悧<br>| unless $is_mobile;
}

#================================================
# ���`
#================================================
sub tp_400 {
	if ($default_icon eq '') {
		$mes .= '���߂�Ȃ������B���̕a�@�ɂ͐��`���޸�������Ȃ��̂�<br>';
		&begin;
		return;
	}
	if ($m{icon_t} ne '') {
		$mes .= '����Ȃ�����ς����Ⴄ�Ȃ�Ă��������Ȃ��킟<br>';
		&begin;
		return;
	}
	$mes .= "$menus[4][0]�́A�M���̊���܂������̕ʐl�ɂ����Ⴄ��悧<br>";
#	$mes .= "���g�p���Ă�����۸ނ́Aϲ�߸���ɖ߂��悧<br>" if -f "$icondir/$m{icon}";
	$mes .= "��p������ɂ́A$menus[4][1] G�Ǝ�p����$GWT��������܂����ǂ�<br>";
	$mes .= "�ǂ����那�H<br>";
	$m{tp} += 10;
	&menu("��߂�", "�����̱��݂�$menus[4][0]����", "��̫�ı��݂�$menus[4][0]����");
}
sub tp_410 {
	return if &is_ng_cmd(1..2);
	if ($default_icon eq '') {
		&begin;
		return;
	}
	
	$layout = 2;
	$mes .= '�ǂ̂悤�Ȃ���ɂ��܂���?<br>��۸ނ��炨�I�т���������<br>';
	unless ($m{icon} eq $default_icon) {
		my $file_title = &get_goods_title($m{icon});
		$mes .= "���݂̊籲�����فw$file_title�x<br>";
	}

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="icon" value="0" checked> ��߂�<hr>|;
	
	if($cmd eq '1'){
		opendir my $dh, "$userdir/$id/picture" or &error('ϲ�߸�����J���܂���');
		while (my $file_name = readdir $dh) {
			next if $file_name =~ /^\./;
			next if $file_name =~ /^_/;
			next if $file_name =~ /\.html$/;

			my $file_title = &get_goods_title($file_name);
			$mes .= qq|<input type="radio" name="icon" value="$file_name"><img src="$userdir/$id/picture/$file_name" $mobile_icon_size> $file_title<hr>|;
		}
		closedir $dh;
	}
	
	$mes .= qq|<input type="radio" name="icon" value="$default_icon"><img src="$icondir/$default_icon" $mobile_icon_size> ��̫��<hr>|;

	if($cmd eq '2'){
		my %add_num = ();
		open my $fh, "< $logdir/add_icon_number.cgi" or &error('����ؽĂ��J���܂���');
		while (my $line = <$fh>) {
			my($i_name, $number) = split /<>/, $line;
			$add_num{$i_name} = $number;
		}
		close $fh;

		my $icon_no;
		$icon_no = 0;
		opendir my $dh_d, "$icondir" or &error('��̫���߸�����J���܂���');
		while (my $file_name_d = readdir $dh_d) {
			next if $file_name_d =~ /^\./;
			next if $file_name_d =~ /\.html$/;

			if ($file_name_d =~ /^_add/){
				my $file_title_d = "No.$icon_no";
				$file_title_d .= ":$add_num{$file_name_d}�l";
				$mes .= qq|<input type="radio" name="icon" value="$file_name_d"><img src="$icondir/$file_name_d" $mobile_icon_size> $file_title_d<hr>|;
				$icon_no++;
			}
		}
		closedir $dh_d;
	}


	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="����" class="button1"></form>|;

	$m{tp} += 10;
	&n_menu;
}
sub tp_420 {
	if ($default_icon eq '') {
		&begin;
		return;
	}

	if ($in{icon} && ($in{icon} eq $default_icon || -f "$icondir/$in{icon}" || -f "$userdir/$id/picture/$in{icon}") ) {
		if ($m{money} >= $menus[4][1]) {
			# ���챲��
			unless ($in{icon} eq $default_icon || $in{icon} =~ /^_add/) {
				&error("$non_title�̂��̂͐��`���邱�Ƃ��ł��܂���") if $in{icon} =~ /^_/;
				&error("�������ق̂��̂����łɎg���Ă��܂�") if -f "$icondir/$in{icon}";
				
				rename "$userdir/$id/picture/$in{icon}", "$icondir/$in{icon}"  or &error("����₾�A���`�Ɏ��s����������킟");
			}

			# �ύX�O�̱��݂����챲�݂Ȃ�ϲ�߸���ɖ߂�
			if($m{icon} =~ /^_add/){
				my %add_num = ();
				my @lines = ();
				my $new = 1;
				open my $fh, "+< $logdir/add_icon_number.cgi" or &error('����ؽĂ��J���܂���');
				eval { flock $fh, 2; };
				while (my $line = <$fh>) {
					my($i_name, $number) = split /<>/, $line;
					if($i_name eq $in{icon}){
						$number--;
						$number = 0 if $number < 0;
						$new = 0;
					}
					push @lines, "$i_name<>$number<>\n";
				}
				if($new){
					push @lines, "$in{icon}<>0<>\n";
				}
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
			}elsif ($m{icon} ne $default_icon && -f "$icondir/$m{icon}") {
				if (-f "$userdir/$id/picture/$m{icon}") {
					$mes .= "�������ق̊G��ϲ�߸���ɂ��������߁A�ύX�O�̊��۸ނ͏��ł��܂���<br>";
				}
				else {
					rename "$icondir/$m{icon}", "$userdir/$id/picture/$m{icon}" or &error("����₾�A���`�Ɏ��s����������킟");
					my $file_title = &get_goods_title($m{icon});
					$mes .= "�ύX�O�Ɏg�p���Ă����w$file_title�x��ϲ�߸���ɖ߂�܂���<br>";
				}
			}


			$m{icon} = $in{icon};

			$mes .= '������ł��Ď�p���n�߂���<br>';
			$mes .= '���ɖڊo�߂��Ƃ��ɂ킟�ʐl�ƂȂ��Ă����悧<br>';
			
			$m{hp}  = $m{max_hp};
			$m{mp}  = $m{max_mp};
			$m{act} = 0;
			$m{money} -= $menus[4][1];
			if($in{icon} =~ /^_add_/){
				my $img_name = $in{icon};
				$img_name =~ s/^_add_//;
				my $img_title = &get_goods_title($img_name);
				$img_title =~ s/.*��://;
				&send_money($img_title,'��Ŏ����Ƃ��č��\���a�@',$menus[4][1]*0.3);
				my @lines = ();
				my $new = 1;
				open my $fh, "+< $logdir/add_icon_number.cgi" or &error('����ؽĂ��J���܂���');
				eval { flock $fh, 2; };
				while (my $line = <$fh>) {
					my($i_name, $number) = split /<>/, $line;
					if($i_name eq $in{icon}){
						$number++;
						$new = 0;
					}
					push @lines, "$i_name<>$number<>\n";
				}
				if($new){
					push @lines, "$in{icon}<>1<>\n";
				}
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh @lines;
				close $fh;
			}
			&refresh;
			&wait;
		}
		else {
			$mes .= '���炟�A����������܂���킟<br>';
			&begin;
		}
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin;
	}
}

#================================================
# ���
#================================================
sub tp_500 {
	if ($default_icon eq '') {
		$mes .= '���߂�Ȃ������B���̕a�@�ɂ͏b�オ���Ȃ��̂�<br>';
		&begin;
		return;
	}
	elsif ($pets[$m{pet}][0] == 0) {
		$mes .= '���߂�Ȃ������B�܂����߯Ă�A��Ă��Ă�<br>';
		&begin;
		return;
	}
	elsif ($pets[$m{pet}][0] < 0) {
		$mes .= '���߂�Ȃ������B�����߯Ăɂ͎�ւ͎�����Ȃ��킟<br>';
		&begin;
		return;
	}
	$mes .= "$menus[5][0]�́A�M�����߯Ă̌����`���C�A�Q�������Ⴄ��悧<br>";
	$mes .= "��ւ���������ɂ́A$menus[5][1] G������܂����ǂ�<br>";
	$mes .= "�ǂ����那�H<br>";
	$m{tp} += 10;
	&menu("��߂�", "$menus[5][0]����");
}
sub tp_510 {
	return if &is_ng_cmd(1);
	if ($default_icon eq '') {
		&begin;
		return;
	}
	
	$layout = 2;
	$mes .= '�ǂ̂悤�Ȏ�ւɂ��܂���?<br>��۸ނ��炨�I�т���������<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="icon" value="0" checked> ��߂�<hr>|;

	$mes .= qq|<input type="radio" name="icon" value="1">��ւ��O��<hr>|;

	if($cmd eq '1'){
		opendir my $dh, "$icondir/pet" or &error('�߯�̫��ނ��J���܂���');
		while (my $file_name = readdir $dh) {
			next if $file_name =~ /^\./;
			next if $file_name =~ /\.html$/;
			# �ޯ�ܲ̂���Ȃ��Ȃ�莝�����߯Ă̱��݂̂� �ޯ�ܲ̂Ȃ炷�ׂĂ��߯Ă̱���
			unless (($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24') && ($m{boch_pet} && $m{pet})) {
				next unless $file_name =~ /^$m{pet}_/;
			}

			my $checked = " checked=\"checked\"" if $file_name eq $m{icon_pet};

			# ������ƍs��������΂�����̋���
			my $name = $file_name;
			my $pet_n = $file_name;
			$pet_n =~ s/^(\d+)_.*/\1/;
			my $petname = ($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24') && ($m{boch_pet} && $m{pet}) ? $pets[$pet_n][1] : '';
			$name =~ s/^\d+_//;
			my $file_title = &get_goods_title($name);
			$file_title =~ s/.*?\s//;
			$mes .= qq|<input type="radio" name="icon" value="$file_name"$checked><img src="$icondir/pet/$file_name" $mobile_icon_size>$petname $file_title<hr>|;
		}
		closedir $dh;
	}

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="����" class="button1"></form>|;

	$m{tp} += 10;
	&n_menu;
}
sub tp_520 {
	if ($default_icon eq '') {
		&begin;
		return;
	}

	if ($in{icon} && ($in{icon} == 1)) {
		$m{icon_pet} = '';
		$mes .= '�O������ւ͂������ŉ�����Ă������<br>';
		&refresh;
		&n_menu;
	}
	elsif ($in{icon} && ($in{icon} eq $m{icon_pet})) {
		$mes .= '��߂܂���<br>';
		&begin;
	}
	elsif ($in{icon} && (-f "$icondir/pet/$in{icon}") ) {
		if ($m{money} >= $menus[5][1]) {
			$m{pet_icon} = '';

			$m{icon_pet} = $in{icon};

			$mes .= '����ł��Ȃ����߯Ă��C�P�C�P���悧<br>';

			$m{money} -= $menus[5][1];

			# ������ƍs��������΂�����̋���
			my $file_name = $in{icon};
			$file_name =~ s/^\d+_//;
			my $name = &get_goods_title($file_name);
			$name =~ s/.*��://; # ��Җ�
			&send_money($name,'��Ŏ����Ƃ��č��\���a�@',$menus[5][1]*0.3);

			my $id = unpack 'H*', $m{name};
			my $this_file = "$userdir/$id/pet_icon.cgi";
			if (-f "$this_file") {
				open my $fh, "+< $this_file" or &error("$this_file ̧�ق��J���܂���");
				eval { flock $fh, 2; };
				my $line = <$fh>;
				if(index($line, "<>$m{pet};") >= 0){
					$line =~ s/<>($m{pet});.*?;(.*?)<>/<>$1;$m{icon_pet};$2<>/;
				}else{
					$line = $line . "$m{pet};$m{icon_pet};1<>";
				}
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh $line;
				close $fh;
			}
			else {
				open my $fh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
				print $fh "<>$m{pet};$m{icon_pet};1<>";
				close $fh;
			}

			&refresh;
			&n_menu;
		}
		else {
			$mes .= '���炟�A����������܂���킟<br>';
			&begin;
		}
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin;
	}
}

#================================================
# �����X�V
#================================================
sub tp_600 {
	$mes .= "$menus[5][0]������Ƃ��A�M�����߽ܰ�ނ�ς��邱�Ƃ��ł���킟<br>";
	$mes .= "�ύX������ɂ́A$menus[5][1] G�K�v�悧<br>";
	$mes .= "�ǂ����那�H<br>";
	$m{tp} += 10;
	&menu("��߂�", "$menus[5][0]����");
}
sub tp_610 {
	return if &is_ng_cmd(1);

	$mes .= qq|����ł킟�A�V���������O���߽ܰ�ނ������Ă�<br>|;
	$mes .= qq|<form method="GET" action="$script"><table class="table1">|;
	$mes .= qq|<tr><td><tt>�߽ܰ�� �F</tt></td><td><input type="text" name="new_pass" value="$m{pass}" class="text_box1"><br></td></tr>|;
	$mes .= qq|</table><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�m��" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_620 {
	if ($m{money} < $menus[5][1]) {
		$mes .= '���炟�A����������܂���킟<br>';
		&begin;
		return;
	}
	elsif ($in{new_pass} eq '') {
		&begin;
		return;
	}
	elsif ($in{new_pass} eq $m{pass}) {
		&begin;
		return;
	}

	&error('�߽ܰ�ނ����͂���Ă��܂���')	if $in{new_pass} eq '';

	&error('�߽ܰ�ނ͔��p�p�����œ��͂��ĉ�����')				if $in{new_pass} =~ m/[^0-9a-zA-Z]/;
	&error('�߽ܰ�ނ͔��p�p����4�`12�����ł�')					if length $in{new_pass} < 4 || length $in{new_pass} > 12;
	&error('��ڲ�-�����߽ܰ�ނ����ꕶ����ł�')					if $m{name} eq $in{new_pass};

	unless ($m{pass} eq $in{new_pass}) {
		$m{pass} = $in{new_pass};
		$pass    = $in{new_pass};
		$mes .= qq|<font color="#FF0000">�V�߽ܰ��:$in{new_pass}</font><br>|;
	}
	
	$m{hp}  = $m{max_hp};
	$m{mp}  = $m{max_mp};
	$m{act} = 0;
	$m{money} -= $menus[5][1];
	&refresh;
	&n_menu;

	$mes .= qq|�̂��߽ܰ�ނł͂������O�C���ł��Ȃ��Ȃ��킟<br><font color="#FF0000"><b>�V�����߽ܰ�ނ�Y��Ȃ��悤�ɂ�</b></font><br>|;
	$mes .= qq|[���񂩂���͏ȗ�]����������ꂢ�Ă���l�킟�A��x۸޲݂�����������������悧<br>| unless $is_mobile;
}

1; # �폜�s��
