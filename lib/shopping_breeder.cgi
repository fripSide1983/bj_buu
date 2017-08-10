#=================================================
# ��ĉ�
#=================================================

#���b���Ƃɛz���l���グ�邩
my @egg_per_sec = (600, 1200, 400);
my @gold_ratios = (1, 0.5, 2);
my @mode_names = ('ɰ�ٺ��', '����غ��', '��������');

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	my @breeds = split /,/, $m{breed};
	return 1 if $breeds[0] || $breeds[1] || $breeds[2] || $m{egg}; # �a���Ă邩���������Ă�

	$mes .= '���������Ă���<br>';
	&refresh;
	$m{lib} = 'shopping';
	&n_menu;
	return 0;
}

#=================================================
sub begin {
	my @breeds = split /,/, $m{breed};
	my @breed_cs = split /,/, $m{breed_c};
	my @breed_times = split /,/, $m{breed_time};
	my $fn = "$userdir/$in{id}/shopping_breeder_";

	my @menus = ('��߂�');
	for my $i (0 .. 2) {
		if ($breeds[$i]) {
			$breed_cs[$i] += int(($time - $breed_times[$i]) / $egg_per_sec[$i]);
			$breed_times[$i] = $time;

			if (-f "$fn$i.cgi") {
				my $bc = ($eggs[$breeds[$i]][2] - $breed_cs[$i]) * $egg_per_sec[$i];
				$bc = $bc < 0 ? 0 : $bc;
				utime ($time, $bc + $time, "$fn");
			}
			$mes .= "$mode_names[$i]�� $eggs[$breeds[$i]][1] �͍� $breed_cs[$i] / $eggs[$breeds[$i]][2]����<br>";
			push @menus, '�������';
		}
		elsif ($m{egg} == 0 || $m{egg} eq '') {
			$mes .= "$mode_names[$i]���g�������Ȃ痑�������Ă���<br>";
			push @menus, '��Ă�';
		}
		else {
			my $v = (30000 +  $eggs[$m{egg}][2] * 50) * $gold_ratios[$i];
			$mes .= "$mode_names[$i]�̎��痿�� $v G����<br>";
			push @menus, '��Ă�';
		}
	}
	&menu(@menus);
	$m{breed} = join(',', @breeds);
	$m{breed_c} = join(',', @breed_cs);
	$m{breed_time} = join(',', @breed_times);
}

sub tp_1 { #
	if ($cmd < 1 || 3 < $cmd) {
		&refresh;
		$m{lib} = 'shopping';
		&n_menu;
		return;
	}
	$cmd--;

	my @breeds = split /,/, $m{breed};
	my @breed_cs = split /,/, $m{breed_c};
	my @breed_times = split /,/, $m{breed_time};
	my $fn = "$userdir/$in{id}/shopping_breeder_";

	if($breeds[$cmd] eq '0' || $breeds[$cmd] eq ''){
		my $v = (30000 +  $eggs[$m{egg}][2] * 50) * $gold_ratios[$cmd];
		unless ($m{egg}) {
			$mes .= '���������Ă���<br>';
		}
		elsif ($m{money} >= $v) {
			$m{money} -= $v;
			$mes .= "�a��������<br>";
			$breeds[$cmd] = $m{egg};
			$breed_cs[$cmd] = $m{egg_c};
			$breed_times[$cmd] = $time;

			open my $fh, "> $fn$cmd.cgi" or &error("$fn$cmd.cgi̧�ق��J���܂���");
			close $fh;
			my $bc = ($eggs[$m{egg}][2] - $m{egg_c}) * $egg_per_sec[$cmd];
			$bc = $bc < 0 ? 0 : $bc;
			utime ($time, $bc + $time, "$fn$cmd.cgi");

			$m{egg} = 0;
			$m{egg_c} = 0;
			&run_tutorial_quest('tutorial_breeder_1');
		}
		else {
			$mes .= "����p�ӂ��Ă���!<br>";
		}
	}
	else {
		&send_item($m{name}, 2, $breeds[$cmd], $breed_cs[$cmd], 0, int(rand(100)));
		$breeds[$cmd] = 0;
		$breed_cs[$cmd] = 0;

		unlink "$fn$cmd.cgi" if -f "$fn$cmd.cgi";

		$mes .= "��������܂���낵����<br>";
	}

	&refresh;
	$m{lib} = 'shopping';
	$m{breed} = join(',', @breeds);
	$m{breed_c} = join(',', @breed_cs);
	$m{breed_time} = join(',', @breed_times);
	&n_menu;
}

1; # �폜�s��
