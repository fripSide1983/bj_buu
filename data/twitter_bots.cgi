@twitter_bots = (
	sub {
		# ������bot
		return "�悧�A�A�A�A";
	},
	sub {
		# ��`
		return "�ɂႠ�IBlind Justice\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		# ��`2
		my $job_name = $jobs[int(rand(@jobs))][1];
		return "�y�}��z$job_name\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		# ��`3
		return "���̃Q�[���ōŋ��̍����낤��\nhttp://www.pandora.nu/nyaa/cgi-bin/bj/index.cgi";
	},
	sub {
		require "$datadir/hunting.cgi";
		my $place = int(rand(@places));
		my $filename =  "$logdir/monster/$places[$place][0].cgi";
		
		my $all_skills = 0;
		my $all_self_burning = 0;
		open my $fh, "< $filename" or &error("$filenamȩ�ق��J���܂���");
		while (my $line = <$fh>) {
			my @datas = split /<>/, $line;
			my $i = 0;
			my %y = ();
			for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
				$y{$k} = $datas[$i];
				++$i;
			}
			my $skill_st = 0;
			my $si = 0;
			my $skill_str = '';
			for my $skill (split /,/, $y{skills}) {
				$si++;
				if ($skills[$skill][2] eq $weas[$y{wea}][2]) {
					$skill_st += $skills[$skill][7];
					if ($skill eq '32') {
						$all_self_burning++;
					}
				} else {
					$skill_st += $skills[0][7];
				}
			}
			for (my $j = $si; $j < 5; $j++) {
				$skill_st += $skills[0][7];
			}
			$all_skills += 5;
		}
		close $fh;
		
		my $sp = int((10 * $all_self_burning / $all_skills) + rand(4) - 2) * 10;
		return "�A���A���Z���o�\\�z�[���~\n���݂�$places[$place][2]��$sp���̃Z���o�m���ł�";
	},
);

1;
