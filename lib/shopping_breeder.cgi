#=================================================
# ��ĉ�
#=================================================

#���b���Ƃɛz���l���グ�邩
my $egg_per_sec = 600;

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if (!$m{breed} && !$m{egg}) {
		$mes .= '���������Ă���<br>';
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return 0;
	}
	return 1;
}


#=================================================
sub begin {
	if($m{breed} eq '0' || $m{breed} eq ''){
		my $v = 30000 +  $eggs[$m{egg}][2] * 50;
		$mes .= "���痿�� $v G����<br>";
		$mes .= "��Ă邩��?";
		&menu('��߂�', '����');
	}else {
		$m{breed_c} += int(($time - $m{breed_time}) / $egg_per_sec);
		$m{breed_time} = $time;
		$mes .= "���O����� $eggs[$m{breed}][1] �͍� $m{breed_c} / $eggs[$m{breed}][2]����<br>";
		$mes .= "�����Ă�������?";
		&menu('��߂�', '�������');
	}
}

sub tp_1 { #
	if($cmd eq '1'){
		if($m{breed} eq '0' || $m{breed} eq ''){
			my $v = 30000 +  $eggs[$m{egg}][2] * 50;
			if ($m{money} >= $v) {
				$m{money} -= $v;
				$mes .= "�a��������<br>";
				$m{breed} = $m{egg};
				$m{breed_c} = $m{egg_c};
				$m{egg} = 0;
				$m{egg_c} = 0;
				$m{breed_time} = $time;
				&run_tutorial_quest('tutorial_breeder_1');
			}
			else {
				$mes .= "����p�ӂ��Ă���!<br>";
			}
		}
		else {
			&send_item($m{name},2,$m{breed},$m{breed_c},0, int(rand(100)));
			$m{breed} = 0;
			$m{breed_c} = 0;
			$mes .= "��������܂���낵����<br>";
		}
	}
	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}

1; # �폜�s��
