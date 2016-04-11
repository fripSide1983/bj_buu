@seed_templates = (
	[0, '�ɐB�͏㏸',
		{
			'fecundity' => 10
		},
		1
	],
	[1, '�ɐB�͒ቺ',
		{
			'fecundity' => -5
		},
		-1
	],
	[2, '�b�艮',
		{
			'smith' => <<'EOM'
		,'smith' => sub {
			$v = shift;
			++$m{wea_lv} if ($m{wea_lv} < 30 && rand(2) < 1);
			return 0;
		}
EOM
		},
		2
	],
	[3, '��������',
		{
			'sho' => <<'EOM'
		,'sho' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-2
	],
	[4, '�������',
		{
			'sho' => <<'EOM'
		,'sho' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		2
	],
	[5, '�_�Ɖ���',
		{
			'nou' => <<'EOM'
		,'nou' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-2
	],
	[6, '�_�Ə��',
		{
			'nou' => <<'EOM'
		,'nou' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		2
	],
	[7, '�푈����',
		{
			'hei' => <<'EOM'
		,'hei' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-3
	],
	[8, '���@��',
		{
			'hei' => <<'EOM'
		,'hei' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		4
	],
	[9, '�Z��',
		{
			'sedai_lv' => <<'EOM'
		,'sedai_lv' => sub {
			$v = shift;
			$v -= 10;
			return $v;
		}
EOM
		},
		-2
	],
	[10, '����',
		{
			'sedai_lv' => <<'EOM'
		,'sedai_lv' => sub {
			$v = shift;
			$v += 10;
			return $v;
		}
EOM
		},
		4
	],
	[11, '�s�҂��P��',
		{
			'war_win' => <<'EOM'
		,'war_win' => sub {
			$v = shift;
			if (&you_exists($y{name})) {
				%datas = &get_you_datas($y{name});
				if ($datas{sex} ne $m{sex}) {
					my $marriage_file_man = "$logdir/marriage_man.cgi";
					my $marriage_file_woman = "$logdir/marriage_woman.cgi";
					my $is_find = 0;

					open my $fh, "< $marriage_file_man" or &error("$marriage_file_maņ�ق��J���܂���");
					while (my $line = <$fh>) {
						my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
						if ($name eq $datas{name}) {
							$is_find = 1;
						}
					}
					close $fh;

					open my $fh2, "< $marriage_file_woman" or &error("$marriage_file_womaņ�ق��J���܂���");
					while (my $line = <$fh2>) {
						my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
						if ($name eq $datas{name}) {
							$is_find = 1;
						}
					}
					close $fh2;
					
					if (($is_find || $datas{seed} eq 'elf') && rand(3) < 1) {
						$m{marriage} = $datas{name};
						&regist_you_data($datas{name}, 'marriage', $m{name});

						&write_world_news(qq|<font color="#740A00">����:�*'�����荥'*�:����$m{name}��$datas{name}���������܂���</font>|);

						my @lines = ();
						open my $fh3, "+< $marriage_file_woman" or &error("$marriage_file_womaņ�ق��J���܂���");
						eval { flock $fh3, 2; };
						while (my $line = <$fh3>) {
							my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
							unless ($name eq $datas{name} || $name eq $m{name}) {
								push @lines, $line;
							}
						}
						seek  $fh3, 0, 0;
						truncate $fh3, 0;
						print $fh3 @lines;
						close $fh3;

						my @lines2 = ();
						open my $fh4, "+< $marriage_file_woman" or &error("$marriage_file_womaņ�ق��J���܂���");
						eval { flock $fh4, 2; };
						while (my $line = <$fh4>) {
							my($no, $mdate, $name, $country, $lv, $rank, $shogo, $message, $icon) = split /<>/, $line;
							unless ($name eq $datas{name} || $name eq $m{name}) {
								push @lines2, $line;
							}
						}
						seek  $fh4, 0, 0;
						truncate $fh4, 0;
						print $fh4 @lines2;
						close $fh4;
					}
				}
			}
			return $v;
		}
EOM
		},
		2
	],
	[12, '���~',
		{
			'gou' => <<'EOM'
		,'gou' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		2
	],
	[13, '��肱�ڂ�',
		{
			'gou' => <<'EOM'
		,'gou' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-2
	],
	[14, '007',
		{
			'cho' => <<'EOM'
		,'cho' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		2
	],
	[15, '���ڗ���',
		{
			'cho' => <<'EOM'
		,'cho' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-2
	],
	[16, '�i���p',
		{
			'sen' => <<'EOM'
		,'sen' => sub {
			$v = shift;
			$v = int($v * 1.05);
			return $v;
		}
EOM
		},
		2
	],
	[17, '������',
		{
			'sen' => <<'EOM'
		,'sen' => sub {
			$v = shift;
			$v = int($v * 0.95);
			return $v;
		}
EOM
		},
		-2
	],
);

1;
