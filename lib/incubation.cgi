
#================================================
# �z���i�X�C�b�`����̎��̏����j
#================================================
sub begin {
	&tp_1;
}
sub tp_1  {
	if ($m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
		$m{egg_c} = 0;
		$mes .= "�����Ă���$eggs[$m{egg}][1]���������܂���!<br>";
		
		# ʽ�ڴ��ސ�p����
		if ( $eggs[$m{egg}][1] eq 'ʽ�ڴ���' && rand(7) > 1 && $m{egg} != 53) {
			if (rand(6) > 1) {
				$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $eggs[$m{egg}][1]���Y�܂�܂���<br>";
			}
			else {
				$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒��͋���ۂł����c<br>";
				$m{egg} = 0;
			}
		}
		# ���ݴ���
		elsif ($eggs[$m{egg}][1] eq '���ݴ���') {
			$m{egg_c} = 0;
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : '�������[';
			$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $pets[$v][1] ���Y�܂�܂���<br>$pets[$v][1]��$pet_mes<br><br>$pets[$v][1]�͗a���菊�ɑ����܂���<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# �z�������M���O
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			if (rand(3) < 1) {
				$m{egg} = 0;
			} else {
				$mes .= "$eggs[$m{egg}][1]�������t�s����<br>";
			}
		}
		# ����è���ސ�p����(�j���ɂ��ς��)
		elsif ( $eggs[$m{egg}][1] eq '����è����' ) {
			my($wday) = (localtime($time))[6];
			my @borns = @{ $eggs[5+$wday][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : '�������[';
			$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $pets[$v][1] ���Y�܂�܂���<br>$pets[$v][1]��$pet_mes<br><br>$pets[$v][1]�͗a���菊�ɑ����܂���<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# �z�������M���O
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			$m{egg} = 0;
		}
		else {
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : '�������[';
			$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $pets[$v][1] ���Y�܂�܂���<br>$pets[$v][1]��$pet_mes<br><br>$pets[$v][1]�͗a���菊�ɑ����܂���<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# �z�������M���O
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			$m{egg} = 0;
		}

		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('incubation');
		}
	}
	$mes .= "�߂�܂�";
	&refresh;
	&n_menu;
}

1; # �폜�s��
