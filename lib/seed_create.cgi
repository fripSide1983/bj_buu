require "$datadir/seed_templates.cgi";
#================================================
# �V�푰�e���v���[�g�I��
#================================================

#================================================
sub begin {
	$m{tp} = 100;
	&n_menu;
}
sub tp_1  {
	$m{tp} = 100;
	&n_menu;
}

sub tp_100  {
	$mes .= "�e���v���[�g��I��ł��������B";
	$layout = 2;
	&show_templates;
	$m{tp} = 200;
	&n_menu;
}

sub tp_200 {
	if ($cmd ne '1') {
		&begin;
		return;
	}
	my $pt = 0;
	my %sames = ();
	for my $i (0..$#seed_templates) {
		if ($in{'check_' . $seed_templates[$i][0]}) {
			$pt += $seed_templates[$i][3];
			my @seed_keys = keys($seed_templates[$i][2]);
			for my $key (@seed_keys) {
				if ($sames{$key}++) {
					$mes .= "���n���̃X�e�[�^�X�͓����ɑI�ׂ܂���B";
					&begin;
					return;
				}
			}
		}
	}

	if ($pt > $m{stock}) {
		$mes .= "�I���������X�e�[�^�X�l���傫�����܂��B";
		&begin;
		return;
	}
	
	&create_seed;
	&refresh;
	&n_menu;
}

sub show_templates {
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1"><tr><th>�I��</th><th>�\�͖�</th><th>�X�e�[�^�X�l<br></th></tr>| unless $is_mobile;
	
	for my $i (0..$#seed_templates) {
		$mes .= $is_mobile ? qq|<input type="checkbox" name="check_$seed_templates[$i][0]" value="1"/> / $seed_templates[$i][1] / $seed_templates[$i][3]<br>|
						 : qq|<tr><td><input type="checkbox" name="check_$seed_templates[$i][0]" value="1"/></td><td>$seed_templates[$i][1]</td><td>$seed_templates[$i][3]<br></td></tr>|;
	}
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<textarea name="free"></textarea>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="cmd" value="1">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
}

sub create_seed {
	$new_seed = "new_seed_" . $time . $id;
	$fecundity = 10;
	$bonus_line = <<"EOM";
		'default' => sub {
			\$v = shift;
			return \$v;
		}
EOM
	for my $i (0..$#seed_templates) {
		if ($in{'check_' . $seed_templates[$i][0]}) {
			for my $key (keys($seed_templates[$i][2])) {
				if ($key eq 'fecundity') {
					$fecundity += $seed_templates[$i][2]->{$key};
				} else {
					$bonus_line .= $seed_templates[$i][2]->{$key};
				}
			}
		}
	}
	$blank_line = <<"EOM";
\@$new_seed = (
	'���̖�����',
	{
$bonus_line
	},
	$fecundity
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

1; # �폜�s��
