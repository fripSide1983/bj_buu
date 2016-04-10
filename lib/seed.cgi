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

#================================================
# �푰���
#================================================
sub get_seeds {
	require "$datadir/seeds.cgi";
	my %all_seeds = ();
	for my $i (0..$#default_seeds) {
		$all_seeds{$default_seeds[$i][1]} = $default_seeds[$i][2];
	}
	# ����
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
	print "aaa";
	print $seeds{$m{seed}}[0];
	print "bbb";
	print $seeds{$m{seed}}[1];
	print "ccc";
	print $seeds{$m{seed}}[2];
	print "ddd";
	if (defined($seeds{$m{seed}}[1]{$lib})) {
		$v = &{${$seeds{$m{seed}}[1]}{$lib}}($v);
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
			$m{seed} = int(rand(@seeds));
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
}

#================================================
# �V�푰
#================================================
sub create_new_seed {
	$new_seed = "new_seed_" . $time . $id;
	$blank_line = <<"EOM";
\@$new_seed = (
	'���̖�����',
	(
		'default' => sub {
			$v = shift;
			return $v;
		}
	),
	10
);
EOM
	open my $fh, "> $add_seeds_dir/$new_seed.cgi";
	print $fh $blank_line;
	close $fh;
	$m{seed} = $new_seed;
}

1; # �폜�s��
