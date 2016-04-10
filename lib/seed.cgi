#================================================
# �푰�֐�
#================================================
require './lib/jcode.pl';
use File::Copy::Recursive qw(rcopy);
use File::Path;

# �ǉ��푰�f�B���N�g��
$add_seeds_dir = "$datadir/add_seeds";

# �]�������m��(%)
$change_percent = 50;

# �V�푰�m��(%)
$change_new_seed_percent = 10;

# ������푰�]���m��(%)
$change_marriage_percent = 30;

# ������˭��݂ɂȂ�m��(%)
$unmarried_human_percent = 50;

%seeds = &get_seeds;

# ��{�푰
$default_seed = 'human';

# �푰��臒l
$seeds_max = 10;

#================================================
# �푰���
#================================================
sub get_seeds {
	require "$datadir/seeds.cgi";
	my %all_seeds = ();
	for my $i (0..$#default_seeds) {
		$all_seeds{$default_seeds[$i][1]} = $default_seeds[$i][2];
	}
	opendir my $dh, "$add_seeds_dir" or &error("�ǉ��푰�ިڸ�؂��J���܂���");
	while (my $fname = readdir $dh) {
		next if $fname !~ /\.cgi/;
		$fname =~ s/\.cgi//g;
		require "$add_seeds_dir/$fname.cgi";
		$all_seeds{$fname} = \@$fname;
	}
	closedir $dh;

	return %all_seeds;
}

#================================================
# �푰�{�[�i�X
#================================================
sub seed_bonus {
	my $lib = shift;
	my $v = shift;
	if ($m{seed} eq '' || !defined($seeds{$m{seed}})) {
		$m{seed} = $default_seed;
	}
	if (defined($seeds{$m{seed}}[1]{$lib})) {
		$v = &{$seeds{$m{seed}}[1]->{$lib}}($v);
	}
	return $v;
}

#================================================
# �푰�ύX
#================================================
sub seed_change {
	my $sta = shift;
	if ($sta eq 'keep') {
		return;
	}
	if ($sta eq 'change' && rand(100) < $change_percent) {
		if (rand(100) < $change_new_seed_percent) {
			&create_new_seed;
		} else {
			my @seed_keys = ();
			foreach $key (keys(%seeds)) {
				push @seed_keys, $key for 1..$seeds{$key}[2];
			}
			$m{seed} = $seed_keys[int(rand(@seed_keys))];
		}
	} else {
		if ($m{marriage} && &you_exists($m{marriage})) {
			my %datas = &get_you_datas($m{marriage});
			if (rand($seeds{$m{seed}}[2] * 100) <= rand($seeds{$datas{seed}}[2] * 100)) {
				$m{seed} = $datas{seed};
			}
		} elsif (rand(100) < $unmarried_human_percent)  {
			$m{seed} = 0;
		}
	}
	&seed_overflow;
}

#================================================
# �V�푰
#================================================
sub create_new_seed {
	$new_seed = "new_seed_" . $time . $id;
	$blank_line = <<"EOM";
\@$new_seed = (
	'���̖�����',
	{
		'default' => sub {
			\$v = shift;
			return \$v;
		}
	},
	10
);

1;
EOM
	open my $fh, "> $add_seeds_dir/$new_seed.cgi";
	print $fh $blank_line;
	close $fh;
	$m{seed} = $new_seed;
	
	$in{comment} = qq|$m{name} ���񂪐V�푰�ɂȂ�܂����B���}�Ή������肢���܂��B|;
	my $mname = $m{name};
	$m{name} = "�V�X�e��";
	&send_letter($admin_name, 0);
	&send_letter($admin_sub_name, 0);
	$m{name} = $mname;
}

#================================================
# ���
#================================================
sub seed_overflow {
	my $seeds_num = keys(%seeds);
	if ($seeds_num > $seeds_max) {
		my %seed_players = ();

		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $uid = readdir $dh) {
			next if $uid =~ /\./;
			next if $uid =~ /backup/;
			my %datas = &get_you_datas($uid, 1);
			$seed_players{$datas{seed}}++;
		}
		closedir $dh;
		for my $key (keys(%seeds)) {
			if (!$seed_players{$key}) {
				if (-f "$add_seeds_dir/$key.cgi") {
					unlink "$add_seeds_dir/$key.cgi";
				}
			}
		}
	}
}
1; # �폜�s��
