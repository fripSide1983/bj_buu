
#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($w{world} ne $#world_states-4) {
		$mes .= "�܂���������Ȃ��c<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	if ($m{sedai} < 10) {
		$mes .= "10���ギ�炢�o����ς�ł���o�����Ă���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	if ($m{name} eq $cs{ceo}[$m{country}]) {
		$mes .= "�����������Ɨ��͂����������ł���I<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	if ($w{country} >= 10) {
		$mes .= "�Ɨ�����̓y�������Ȃ���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
# �Ɨ�
#================================================
sub begin {
	&tp_1;
}

sub tp_1 {
	$mes .= "��O���N���ēƗ����܂���?";
	$m{tp} = 100;
	&menu('��߂�', '�Ɨ�');
}

sub tp_100 {
	if ($cmd) {
		&create_country;
	
		require "./lib/move_player.cgi";
		
		&move_player($m{name}, $m{country}, $w{country});
		$m{country} = $w{country};

		$cs{ceo}[$w{country}] = $m{name};
		$m{vote} = $m{name};

		&write_cs;
		&mes_and_world_news("�Ɨ����܂����B");
		
		&cs_data_repair;
	}
	&refresh;
	&n_menu;
}
1; # �폜�s��
