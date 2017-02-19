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

	unless ($in{seed_name}) {
		$mes .= "�푰�����ݒ肳��Ă��܂���B";
		&begin;
		return;
	}
	
	my $pt = 0;
	my %sames = ();
	for my $i (0..$#seed_templates) {
		if ($in{'check_' . $seed_templates[$i][0]}) {
			$pt += $seed_templates[$i][3];
			my @seed_keys = keys(%{$seed_templates[$i][2]});
			for my $key (@seed_keys) {
				if ($sames{$key}++) {
					$mes .= "���n���̃X�e�[�^�X($key)�͓����ɑI�ׂ܂���B";
					&begin;
					return;
				}
			}
		}
	}

	if ($pt > $m{stock}) {
		$mes .= "�I�������X�e�[�^�X�l���傫�����܂��B";
		&begin;
		return;
	}
	
	&create_seed;
	&refresh;
	&n_menu;
}

sub show_templates {
	$mes .= qq|�U�蕪���\\pt$m{stock}<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|�푰���F<input type="text" name="seed_name"/><br>|;
	$mes .= qq|<table class="table1"><tr><th>�I��</th><th>�\\�͖�</th><th>�X�e�[�^�X�l<br></th></tr>| unless $is_mobile;
	
	for my $i (0..$#seed_templates) {
		$mes .= $is_mobile ? qq|<input type="checkbox" name="check_$seed_templates[$i][0]" value="1"/> / $seed_templates[$i][1] / $seed_templates[$i][3]<br>|
						 : qq|<tr><td><input type="checkbox" name="check_$seed_templates[$i][0]" value="1"/></td><td>$seed_templates[$i][1]</td><td>$seed_templates[$i][3]<br></td></tr>|;
	}
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<p>�V�푰�̎��\\�͂Ȃǂ̗v�]�i��������Ƃ͌���Ȃ��j</p>|;
	$mes .= qq|<textarea name="free"></textarea>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="cmd" value="1">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
	$mes .= qq|<h3>�V�푰�쐬�̐���</h3>|;
	$mes .= qq|<p>�V�푰�]�����ɂ́A�܂��߲�Ă�����U���Ď푰�̑�܂��Ȕ\\�͂ɂ��Č��߂Ă��������B�߲�Ă̏����l��1�`2�̃����_���ł����A�e�\\�͂̍��v�l�������l�Ɏ��܂�Ζ��Ȃ��̂Ń}�C�i�X�̃f�����b�g�\\�͂Ƒg�ݍ��킹�邱�Ƃō��߲�Ă̔\\�͂�I�����邱�Ƃ��ł��܂��B�܂��A�V�푰���L�̔\\�͂Ȃǎv���t�����̂�����΃R�����g���ɏ����Ă��������B</p>|;
}

sub create_seed {
	$new_seed = "new_seed_" . $time . $id;
	$fecundity = 10;
	$new_seed_name = $in{seed_name};
	$bonus_line = <<"EOM";
		'default' => sub {
			\$v = shift;
			return \$v;
		}
EOM
	my $pt = 0;
	my $seed_detail_line = '';
	for my $i (0..$#seed_templates) {
		if ($in{'check_' . $seed_templates[$i][0]}) {
			for my $key (keys(%{$seed_templates[$i][2]})) {
				if ($key eq 'fecundity') {
					$fecundity += $seed_templates[$i][2]->{$key};
				} else {
					$bonus_line .= $seed_templates[$i][2]->{$key};
				}
			}
			$pt += $seed_templates[$i][3];
			$seed_detail_line .= $seed_templates[$i][1];
		}
	}
	$blank_line = <<"EOM";
\@$new_seed = (
	'$seed_name',
	{
$bonus_line
	},
	$fecundity,
	'$seed_detail_line'
);

1;
EOM
	open my $fh, "> $add_seeds_dir/$new_seed.cgi";
	print $fh $blank_line;
	close $fh;
	chmod 0666, "$add_seeds_dir/$new_seed.cgi";
	$m{seed} = $new_seed;
	
	$in{comment} = qq|$m{name} ���񂪐V�푰$new_seed_name�ɂȂ�܂����B���}�Ή������肢���܂��B<br>|;
	$in{comment} .= qq|�L�[ : $m{seed}<br>|;
	$in{comment} .= qq|�U�蕪��pt $pt / $m{stock}<br>|;
	if ($in{free}) {
		$in{comment} .= qq|���R����<br>|;
		$in{comment} .= $in{free};
	}
	my $mname = $m{name};
	$m{name} = "�V�X�e��";
	&send_letter($admin_name, 0);
	&send_letter($admin_sub_name, 0);
	$m{name} = $mname;
}

1; # �폜�s��
