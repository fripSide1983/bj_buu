#================================================
# �ŋ��Z Created by Merino
#================================================

# �؂�����z
my $fall_money = $m{sedai} > 100 ? 2000000 : $m{sedai} * 20000;

# ���q
my $interest = 1.3;


#================================================
sub begin {
	# �g���E�O���u�ł��S�~�N�Y�����͂ł���
	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		my $v = int($fall_money * $interest);
		$mes .= "$v G�������藘�q�����낦�āA�͂�Ԃ��񂩂�!";
		&menu('������','�ԍς���');
	}
	else {
		# �g���E�O���u���͎؋��ł��Ȃ�
		if ($w{year} % 40 == 0 || $w{year} % 40 == 20){
			$mes .= '���莆�u�x����̗��R�Ŗ{���͂��x�݂ł��v<br>';

			&refresh;
			$m{lib} = 'shopping';
			&n_menu;
		}
		else {
			$mes .= '��������Ⴂ�܂��A�����ɂ�����ł���?<br>';
			$mes .= '���݂��ł�����z�͐�����d�˂�قǑ������݂��ł��܂�<br>';
			$mes .= "$m{name}�l�� $m{sedai} ����ڂł��̂� $fall_money G���݂����邱�Ƃ��ł��܂�<br>";
			&menu('��߂�', '�؂��');
		}
	}
}

sub tp_1 {
	return if &is_ng_cmd(1);
	
	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		my $v = $config_test ? 0 : int($fall_money * $interest);
		if ($m{money} >= $v) {
			$m{money} -= $v;
			$m{shogo} = '';
			$m{shogo_t} = '';
			$mes .= '�����p�͌v��I�ɂ�!<br>';
		}
		else {
			$mes .= '������!��������Ȃ���!<br>';
			$mes .= "$m{name} �͓�����悤�ɗ����������c<br>";
		}
	}
	else {
		$m{shogo} = $shogos[1][0];
		$m{money} += $fall_money;
		$mes .= "$fall_money G�m���ɂ��݂����܂���<br>";
		$mes .= "���݂��������͂�����ƕԍς��Ă���������<br>";
	}
	
	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}



1; # �폜�s��
