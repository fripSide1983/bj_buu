#=================================================
# �b�艮 Created by Merino
#=================================================

# �C����
my $need_money = int( ($weas[$m{wea}][3]+$weas[$m{wea}][5]) * 50 + $weas[$m{wea}][4] * 2 + $m{wea_lv} * 1000);


#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if (!$m{wea}) {
		$mes .= '����𑕔����Ă���܂�����!<br>';
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	elsif($m{wea_c} > 10) {
		$mes .= '�A���^�̕���͂܂��C������K�v�͂Ȃ����낤�B�����Ǝg������ł���܂�����!<br>';
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	return 1;
}


#=================================================
sub begin {
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	$mes .= '�����͒b�艮���B�������Ă��镐����C�����邺<br>';
	$mes .= "�����Ԃ�Ǝg������ $wname ����<br>";
	$mes .= "�C����́A$need_money G�ɂȂ邺�B�ǂ�����?";
	&menu('��߂�', '�C���𗊂�');
}

sub tp_1 { # �C��
	if ($cmd eq '1' && $m{wea} && $m{wea_c} <= 10) {
		my $v = int($weas[$m{wea}][3] * 100); 
		
		if ($m{money} >= $need_money) {
			$need_money = &use_pet('smith', $need_money);
			$need_money = &seed_bonus('smith', $need_money);
			$m{money} -= $need_money;
			++$m{wea_lv} if $m{wea_lv} < 30;


			if ($m{wea} eq '31' && $m{wea_lv} >= 30) {
				$mes .= "$weas[$m{wea}][1]�͕��X�ɍӂ��U��$weas[32][1]�ɂȂ�܂���<br>";
				$m{wea} = 32;
				$m{wea_lv} = 10;
			}
			else {
				$mes .= '����!�V�i���l�ɏC������������!�܂���!<br>';
			}

			$m{wea_c} = $weas[$m{wea}][4];
		}
		else {
			$mes .= "��������Ȃ���!�܂���!<br>";
		}
	}
	
	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}


1; # �폜�s��
