#================================================
# �]�E�� Created by Merino ###
#================================================

# �]�E�ɕK�v�ȋ��z
my $need_money = $m{sedai} > 10 ? 20000 : $m{sedai} * 2000;


#=================================================
sub begin {
	$mes .= '�����͓]�E������B����̐E�Ƃ�ς��邱�Ƃ��ł��邼<br>';
	$mes .= "�������A�]�E����ɂ� $need_money G�K�v���Ⴜ<br>";
	$mes .= '�E�Ƃ�ς���̂�?<br>';

	my @menus = ('��߂�');
	for my $i (0 .. $#jobs) {
		push @menus, $jobs[$i][11]->() ? $jobs[$i][1] : '';
	}
	&menu(@menus);
}

sub tp_1 {
	--$cmd;
	if ($m{job} eq $cmd) {
		$mes .= "$jobs[$cmd][1]�ɂȂ肽���Ɛ\\�����c<br>��?�ł��A���łɂ��̐E�ƂɂȂ��Ă���ł͂Ȃ���?<br>";
	}
	elsif ($m{job} eq '24') {
		$mes .= '���@���������@�����łȂ��Ȃ�͍̂ŏI�񂾂�����<br>';
	}
	elsif ($cmd >= 0 && &{ $jobs[$cmd][11] }) {
		if ($m{money} >= $need_money) {
			$m{money} -= $need_money;
			&remove_pet if $cmd eq '21';
			$m{job} = $cmd;
			$mes .= "$jobs[$cmd][1]�ƂȂ��ĐV���ȓ���i�ނ��悢<br>$m{name}��$jobs[$cmd][1]�ɓ]�E���܂���<br>";
		}
		else {
			$mes .= '����������񂼂�<br>���������߂Ă܂����Ȃ���<br>';
		}
	}
	else {
		$mes .= '���̐E�Ƃɓ]�E�����������������Ă��Ȃ��悤����<br>';
	}

	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
}




1; # �폜�s��
