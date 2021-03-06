#=================================================
# 育て屋
#=================================================

#何秒ごとに孵化値を上げるか
my @egg_per_sec = (600, 1200, 400);
my @gold_ratios = (1, 0.5, 2);
my @mode_names = ('ﾉｰﾏﾙｺｰｽ', 'ﾉﾝﾋﾞﾘｺｰｽ', 'ｽﾊﾟﾙﾀｺｰｽ');

#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	my @breeds = split /,/, $m{breed};
	return 1 if $breeds[0] || $breeds[1] || $breeds[2] || $m{egg}; # 預けてるか卵を持ってる

	$mes .= '卵を持ってきな<br>';
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

	my @menus = ('やめる');
	for my $i (0 .. 2) {
		if ($breeds[$i]) {
			$breed_cs[$i] += int(($time - $breed_times[$i]) / $egg_per_sec[$i]);
			$breed_times[$i] = $time;

			if (-f "$fn$i.cgi") {
				my $bc = ($eggs[$breeds[$i]][2] - $breed_cs[$i] + 1) * $egg_per_sec[$i];
				$bc = $bc < 0 ? 0 : $bc;
				utime ($time, $bc + $time, "$fn$i.cgi");
			}
			$mes .= "$mode_names[$i]の $eggs[$breeds[$i]][1] は今 $breed_cs[$i] / $eggs[$breeds[$i]][2]だよ<br>";
			push @menus, '引き取る';
		}
		elsif ($m{egg} == 0 || $m{egg} eq '') {
			$mes .= "$mode_names[$i]を使いたいなら卵を持ってきな<br>";
			push @menus, '育てる';
		}
		else {
			my $v = (30000 +  $eggs[$m{egg}][2] * 50) * $gold_ratios[$i];
			$mes .= "$mode_names[$i]の飼育料は $v Gだよ<br>";
			push @menus, '育てる';
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
			$mes .= '卵を持ってきな<br>';
		}
		elsif ($m{money} >= $v) {
			$m{money} -= $v;
			$mes .= "預かったよ<br>";
			$breeds[$cmd] = $m{egg};
			$breed_cs[$cmd] = $m{egg_c};
			$breed_times[$cmd] = $time;

			open my $fh, "> $fn$cmd.cgi" or &error("$fn$cmd.cgiﾌｧｲﾙが開けません");
			close $fh;
			my $bc = ($eggs[$m{egg}][2] - $m{egg_c} + 1) * $egg_per_sec[$cmd];
			$bc = $bc < 0 ? 0 : $bc;
			utime ($time, $bc + $time, "$fn$cmd.cgi");

			$m{egg} = 0;
			$m{egg_c} = 0;
			&run_tutorial_quest('tutorial_breeder_1');
		}
		else {
			$mes .= "金を用意してきな!<br>";
		}
	}
	else {
		&send_item($m{name}, 2, $breeds[$cmd], $breed_cs[$cmd], 0, int(rand(100)));
		$breeds[$cmd] = 0;
		$breed_cs[$cmd] = 0;

		unlink "$fn$cmd.cgi" if -f "$fn$cmd.cgi";

		$mes .= "送ったよまたよろしくな<br>";
	}

	&refresh;
	$m{lib} = 'shopping';
	$m{breed} = join(',', @breeds);
	$m{breed_c} = join(',', @breed_cs);
	$m{breed_time} = join(',', @breed_times);
	&n_menu;
}

1; # 削除不可
