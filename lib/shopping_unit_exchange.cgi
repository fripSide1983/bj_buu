$mes .= qq|�M�� $m{medal}��<br>| if $is_mobile;
#=================================================
# �����ύX Created by Merino
#=================================================

# �M��1�̋��z
my $exchange_money = 3000;

# ��30����̉��l
my $exchange_medal = $m{wea} == 0 ? 0:
					$m{wea} <= 30 ? (($m{wea} - 1) % 5 + 1) * 5:
					($m{wea} % 5 + 5) * 5;

# ���������i
my @prizes = (
# ��� 1=����,2=��,3=�߯� 
#	[0]���,[1]No,[2]�M��
	[0,	0,	0,	],
	[1,	12,	5,	],
	[1,	17,	5,	],
	[1,	27,	5,	],
	[2,	21,	15,	],
	[2,	33,	20,	],
	[2,	27,	25,	],
	[2,	3,	30,	],
	[2,	45,	80,	],
	[2,	37,	90,	],
	[2,	46,	99,	],
);


# ���ʏ����Ÿ׽��ݼނł������
my %plus_needs = (
# ����No => ������,					if����									# �����ر��̏���
	7  => ['�ް�ΰ�����',			sub{ $pets[$m{pet}][2] eq 'speed_up' },	sub{ $mes.="$pets[$m{pet}][1]��$m{pet_c}���тɂ��܂���<br>"; $m{pet} = 0; } ],
	8  => ['��׺�݌n���߯Ă���',	sub{ $pets[$m{pet}][1] =~ /��׺��/ },	sub{ $mes.="$pets[$m{pet}][1]��$m{pet_c}���тɂ��܂���<br>"; $m{pet} = 0; } ],
	11 => ['�E�Ƃ��E��',			sub{ $jobs[$m{job}][1] eq '�E��' },		sub{} ],
	12 => ["$eggs[23][1]����",	sub{ $m{egg} eq '23'},					sub{ $mes.="$eggs[$m{egg}][1]���тɂ��܂���<br>"; $m{egg} = 0; $m{egg_c} = 0; } ],
	15 => ['�E�Ƃ������g��',		sub{ $jobs[$m{job}][1] eq '�����g��' },	sub{} ],
	16 => ['��ɽ����+�����n���x���v5000�ȏ�',			sub{ ($pets[$m{pet}][0] eq '42' && $m{nou_c}+$m{sho_c}+$m{hei_c}>=5000) },	sub{$mes.="$pets[$m{pet}][1]��$m{pet_c}���тɂ��܂���<br>"; $m{pet} = 0;} ],
	17 => ['�ް�Ă���+�D�R��3��n���x���v10000�ȏ�',			sub{ ($pets[$m{pet}][2] eq 'no_ambush' && $m{gou_c}+$m{cho_c}+$m{sen_c}>=10000) },	sub{$mes.="$pets[$m{pet}][1]��$m{pet_c}���тɂ��܂���<br>"; $m{pet} = 0;} ],
	18 => ['۷����+�푈������500�ȏ�',			sub{ ($pets[$m{pet}][0] eq '12' && $m{win_c}>=500) },	sub{$mes.="$pets[$m{pet}][1]��$m{pet_c}���тɂ��܂���<br>"; $m{pet} = 0;} ],
);


#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ�������܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "�����ł�$m{name}�̎����Ă���M�͂ɉ����ĕ�����׽��ݼނ�����ł��܂�<br>";
		$mes .= '�ǂ����܂���?<br>';
	}
	&menu('��߂�','�������~����','���т��~����','������ς�����','���_�E�ɂȂ�','���������̕��킪�~����','�M�͂��~����');
}
sub tp_1 {
	return if &is_ng_cmd(1..6);
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# �M�́�����
#=================================================
sub tp_100 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "$m{name}�̏������Ă���M�͂�$m{medal}�ł���<br>";
	$mes .= "�M��1�ɂ� $exchange_money G�Ɋ����邱�Ƃ��ł��܂�<br>";
	$mes .= "���̌M�͂����サ�܂���?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="medal" value="0" class="text_box1" style="text-align:right">��|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���シ��" class="button1"></p></form>|;
}
sub tp_110 {
	if ($in{medal} && $in{medal} !~ /[^0-9]/) {
		if ($in{medal} > $m{medal}) {
			$mes .= "$in{medal}���M�͂������Ă��܂���<br>";
		}
		else {
			my $v = $in{medal} * $exchange_money;
			$m{money} += $v;
			$m{medal} -= $in{medal};
			
			$mes .= "�M��$in{medal}�����サ�� $v G�����炢�܂���<br>";
		}
	}
	&begin;
}

#=================================================
# �M�́�����
#=================================================
sub tp_200 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "$m{name}�̏������Ă���M�͂�$m{medal}�ł���<br>";
	$mes .= "�ǂ�ƌ������܂���?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1" cellpadding="3"><tr><th>���O</th><th>�M��<br></th></tr>|;
	$mes .= qq|<tr><td colspan="2"><input type="radio" name="cmd" value="0" checked>��߂�<br></td></tr>|;
	for my $i (1 .. $#prizes) {
		$mes .= qq|<tr><td><input type="radio" name="cmd" value="$i">|;
		$mes .= $prizes[$i][0] eq '1' ? qq|[$weas[ $prizes[$i][1] ][2]]$weas[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '2' ? qq|[��]$eggs[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '3' ? qq|[�y]$pets[ $prizes[$i][1] ][1]</td>|
			  : 						qq|[$guas[ $prizes[$i][1] ][2]]$guas[ $prizes[$i][1] ][1]</td>|
			  ;
		$mes .= qq|<td align="right">$prizes[$i][2]��<br></td></tr>|;
	}
	$mes .= qq|</table>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p>�~<input type="text" name="loop" value="1" class="text_box1" style="text-align:right"></p>|;
	$mes .= qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
}
sub tp_210 {
	if ($cmd && defined $prizes[$cmd]) {
		if ($in{loop} && $in{loop} !~ /[^0-9]/) {
			for my $loop (1..$in{loop}) {
				if ($m{medal} >= $prizes[$cmd][2]) {
					$m{medal} -= $prizes[$cmd][2];
					
					$mes .= "�M��$prizes[$cmd][2]�����サ��";

					if ($prizes[$cmd][0] eq '1') {
						$mes .= "$weas[ $prizes[$cmd][1] ][1]�Ɍ������܂���<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], $weas[ $prizes[$cmd][1] ][4], 0, 1);
					}
					elsif ($prizes[$cmd][0] eq '2') {
						$mes .= "$eggs[ $prizes[$cmd][1] ][1]�Ɍ������܂���<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], 0, 0, 1);
					}
					elsif ($prizes[$cmd][0] eq '3') {
						$mes .= "$pets[ $prizes[$cmd][1] ][1]�Ɍ������܂���<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], 0, 0, 1);
					}
					elsif ($prizes[$cmd][0] eq '4') {
						$mes .= "$guas[ $prizes[$cmd][1] ][1]�Ɍ������܂���<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], 0, 0, 1);
					}
				}
				else {
					$mes .= '�M�͂�����܂���<br>';
				}
			}
		}
	}
	&begin;
}

#=================================================
# �M�́������{����
#=================================================
sub tp_300 {
	$m{tp} += 10;
	$mes .= "$m{name}�̏������Ă���M�͂�$m{medal}�ł���<br>";
	$mes .= "�׽��ݼނŗ]�����M�͂͂����Ɋ������܂�<br>";
	$mes .= "�ǂ̕����ɸ׽��ݼނ��܂���?<hr>";
	$mes .= "���̕�������Ÿ׽��ݼނł���͈̂ȉ��ł�<br>";
	
	$mes .= "$units[0][1] �����F�Ȃ�<br>";
	my @menus = ('��߂�', $units[0][1]);
	for my $i (1 .. $#units) {
		if ($i eq $units[$m{unit}][2]) {
			$mes .= "$units[$i][1] �����F�Ȃ�<br>";
			push @menus, $units[$i][1];
		}
		elsif ($m{unit} eq $units[$i][2]) {
			$mes .= "$units[$i][1] �����F$units[ $units[$i][2] ][1]/�M��$units[$i][3]��/";
			$mes .= $plus_needs{$i}[0] if defined $plus_needs{$i};
			$mes .= "<br>";
			
			push @menus, $units[$i][1];
		}
		else {
			push @menus, '';
		}
	}
	
	&menu(@menus);
}
sub tp_310 {
	if ($cmd) {
		--$cmd;
		
		if ($cmd) {
			# �׽�޳�
			unless ($cmd eq $units[$m{unit}][2]) {
				# �������
				if (defined $plus_needs{$cmd}) {
					if (&{ $plus_needs{$cmd}[1] } && $units[$cmd][2] eq $m{unit} && $m{medal} >= $units[$cmd][3]) {
						&{ $plus_needs{$cmd}[2] };
						$m{medal} -= $units[$cmd][3];
					}
					else {
						$mes .= "�׽��ݼނł�������𖞂����Ă��܂���<br>";
						&begin;
						return;
					}
				}
				elsif ($units[$cmd][2] eq $m{unit} && $m{medal} >= $units[$cmd][3]) {
					$m{medal} -= $units[$cmd][3];
				}
				else {
					$mes .= "�׽��ݼނł�������𖞂����Ă��܂���<br>";
					&begin;
					return;
				}
			}
		}
		
		$m{unit} = $cmd;
		$mes .= "$units[$m{unit}][1]�ɸ׽��ݼނ��܂���<br>";

		if ($m{medal} > 0) {
			my $v = $m{medal} * $exchange_money;
			$m{money} += $v;
			$mes .= "�c��̌M��$m{medal}�����サ�� $v G�����炢�܂���<br>";
			$m{medal} = 0;
		}
	}
	&begin;
}

#=================================================
# ���_�E
#=================================================
sub tp_400 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "1�������̖��_�E�ɏA���܂�<br>";
	$mes .= "�v���l10000�ŊK���������R�ɕς����܂�<br>";
	$mes .= "���_�E�ɂȂ�܂���?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="s_rank" value="" class="text_box1" style="text-align:right">�K����|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���_�E�ɂȂ�" class="button1"></p></form>|;
}
sub tp_410 {
	&error("�K�������������܂��S�p5(���p10)�����܂łł�") if length $in{s_rank} > 10;
	if ($in{s_rank}) {
		if ($m{rank_exp} < 10000) {
			$mes .= "�v���l������܂���<br>";
		}
		else {
			$m{rank_exp} -= 10000;
			$m{super_rank} += 1;
			$in{s_rank} =~ s/��/��/g;
			$m{rank_name} = $in{s_rank};
			
			$mes .= "���_�E�u��$m{rank_name}�v�ɂȂ�܂���<br>";
		}
	}
	&begin;
}

#=================================================
# ���
#=================================================
sub tp_500 {
	$m{tp} += 10;
	$mes .= "���ʰƈ��������Ɏ����̕���������܂�<br>";
	&menu('��߂�','���ʰ������');
}
sub tp_510 {
	if ($cmd eq '1' && $m{wea} eq '32' && $m{wea_lv} >= 30) {
		$mes .= "�߯Ă𑗂�܂���<br>";
		$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		&send_item($m{name}, 3, 191, 0, 0, 1);
	}else{
		$mes .= "��30�̸��ʰƌ����ł��܂�<br>";
	}
	&begin;
}

#=================================================
# ���큨�M��
#=================================================
sub tp_600 {
	$m{tp} += 10;
	$mes .= "$m{name}�̏������Ă���M�͂�$m{medal}�ł���<br>";
	$mes .= "�����p�̕�����M�� $exchange_medal �Ɋ����邱�Ƃ��ł��܂�<br>";
	$mes .= "���蕥���܂���?<br>";
	
	&menu('��߂�','���蕥��');
}
sub tp_610 {
	if ($cmd eq '1') {
		if ($m{wea_lv} ne '30') {
			$mes .= "�V�i�ł͌M�͂ɕς����܂���<br>";
		}
		else {
			$m{wea} = 0;
			$m{wea_c} = 0;
			$m{wea_lv} = 0;
			if($m{wea_name}){
				$m{wea_name} = "";
				$exchange_medal += 0;
			}
			$m{medal} += $exchange_medal;
			
			$mes .= "���p�̕�������ɓ���A�M�͂� $exchange_medal ���炢�܂���<br>";
		}
	}
	&begin;
}


1; # �폜�s��
