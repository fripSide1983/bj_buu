#================================================
# �N���C�x���g
#=================================================

# �����l�i
my $buy_price  = 500;

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '�����[�V�c�a����<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�悢�N�z����<br>';
	}
	
	&menu('��߂�','�C���𔃂�','�N���𑗂�');
}

sub tp_1 {
	return if &is_ng_cmd(1..2);
	$m{tp} = $cmd * 100;
	
	if ($cmd eq '1') {
		$mes .= "�C��������?<br>�Е������Ȃ����� $buy_price G�ł��<br>";
		&menu('��߂�','����');
	}
	elsif ($cmd eq '2') {
		$mes .= "���ǂ����܂� $buy_price G�ő���<br>";
		&menu('��߂�', '����');
	}
	else {
		&begin;
	}
}

#=================================================
# �C��
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);
	
	if ($m{money} < $buy_price) {
		$mes .= '���O�n�R�B���킢������������B�Е������Ȃ����ǂȁB<br>';
	}
	else {
		$m{money} -= $buy_price;
	}
	if ($m{sox_kind}) {
		$mes .= '�����C���͗p�ӂ��Ă��邯�Ǖʂ̂Ǝ��ւ��悤<br>';
	}
	$mes .= '�C���ɂǂ�Ȋ肢����悤��';
	
	$m{tp} += 10;
	&menu('��ٍ��m', '�̫��', '���̊G���~����', '�������������킪�~����');
}

sub tp_110 {
	if ($cmd eq '1') {
		$m{sox_kind} = 3;
		$m{sox_no} = 183;
	} elsif ($cmd eq '2') {
		$m{sox_kind} = 3;
		$m{sox_no} = 168;
	} elsif ($cmd eq '3') {
		if (rand(30) < 1) {
			$m{sox_kind} = 1;
			$m{sox_no} = 33;
		} else {
			$m{sox_kind} = 3;
			$m{sox_no} = 191;
		}
	} else {
		$m{sox_kind} = 3;
		$m{sox_no} = 21;
	}
	&begin;
}

#=================================================
# �N���
#=================================================
sub tp_200 {
	$mes .= "�N�ɔN���𑗂�܂���?<br>";
	$mes .= "���ʂ͈���ς݂Ȃ̂ŏ����K�v�͂Ȃ���?<br>";

	$mes .= qq|<form method="$method" action="$script"><p>�����F<input type="text" name="to_name" class="text_box1"></p>|;
	$mes .= qq|<p>�����F<input type="text" name="from_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1">����<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
	$m{tp} += 10;
}

sub tp_210 {
	return if &is_ng_cmd(1);
	
	if ($m{money} < $buy_price) {
		$mes .= '�͂����㑫��Ȃ��B�A��B<br>';
	}
	else {
		$m{money} -= $buy_price;
		my $to_id = unpack 'H*', $in{to_name};
		my $number = int(rand(1000000000));
		open my $fh, ">> $userdir/$to_id/greeting_card.cgi" or &error("�|�X�g���J���܂���");
		print $fh "$in{from_name}<>$id<>$number<>\n";
		close $fh;
	}
	&begin;
}
1; # �폜�s��
