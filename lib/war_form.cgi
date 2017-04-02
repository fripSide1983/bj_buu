#=================================================
# �푈�o������ Created by Merino
#=================================================

# �S������
$GWT = int($GWT * 1.5);

my @needs = (0.5, 1.0, 2.0); #�ʏ핔��
if ($m{unit} eq '16') { # �y������ �����0.75�{
	$needs[$_] = $needs[$_] * 0.75 for (0 .. $#needs);
}
elsif ($m{unit} eq '18') { # �m���� �����1.5�{
	$needs[$_] = $needs[$_] * 1.5 for (0 .. $#needs);
}
if ($m{pet} eq '193') { $needs[$_] = $needs[$_] * 0.5 for (0 .. $#needs); } # �ް���ޯ� �����0.5�{


# �i�R���
my @war_marchs = (
#	[0]���O,[1]�i�R���ԕ��m�̔{��,[2]�o��̔{��,[3]�K�v����
	['�������s',	0.5,	$needs[0],	sub{ $pets[$m{pet}][2] ne 'speed_down' }],
	['�ʏ�푈',	1.0,	$needs[1],	sub{ $m{win_c} >= 1  }],
	['��������',	1.5,	$needs[2],	sub{ $m{unit} ne '11' && $m{win_c} >= 10 && $m{win_c} > $m{lose_c} }]
);
if($m{value} < 0 || $m{value} >= @war_marchs){$m{value} = $#war_marchs;}
my $need_costs = $rank_sols[$m{rank}] * $war_marchs[$m{value}][2];

#=================================================
# ���p����
#================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '���ɑ����ĂȂ��ƍs�����Ƃ��ł��܂���<br>�d������ɂ́u�����v���u�d���v����s���Ă݂�������I��ł�������<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ��J���Ă���ꍇ�͍s���Ȃ�
		return 0;
	}
	elsif ($time < $w{reset_time}) {
		$mes .= '�I����Ԓ��͐푈�ƌR���͂ł��܂���<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ( $cs{is_die}[$m{country}] && ($w{world} eq '9' || $w{world} eq '13' || ($w{world} eq '19' && ($w{world_sub} eq '9' || $w{world_sub} eq '13'))) ) {
		$mes .= "���E���$world_states[$w{world}]�ŁA�������ŖS���Ă���̂Ő푈���邱�Ƃ͂ł��܂���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	if ($m{tp} > 1) {
		$m{tp} = 1;
		$mes .= '�ǂ̂悤�ɍU�ߍ��݂܂���?<hr>';
	}
	else {
		$mes .= "�����֍U�ߍ���$e2j{strong}��D���܂�<br>";
		$mes .= "�ǂ̂悤�ɍU�ߍ��݂܂���?<hr>";
	}

	my @menus = ('��߂�');
	for my $war_march (@war_marchs) {
		if (&{ $war_march->[3] }) {
			my $need_fm  = $rank_sols[$m{rank}] * $war_march->[2];
			my $need_GWT = &_unit_march($GWT * $war_march->[1]);
			# ������Ƌ��� _unit_march() �̓����� $m{value} ���Q�Ƃ���̂Ŗ������ begin �Ăяo�����ɈӐ}���Ȃ����l���Ԃ�
			# �����i�R��蒷���S�����Ԃ̐i�R���@���������ꂽ�ꍇ�ɁA�܂��\���Ɠ����̍S�����Ԃ̃Y������������
			$need_GWT = 20 if $war_march->[1] > 1 && $need_GWT < 20;
			$mes .= "$war_march->[0] [����ƁF$need_fm ����\\�Z�F$need_fm ���ԁF$need_GWT��]<br>";
			push @menus, $war_march->[0];
		}
		else {
			push @menus, '';
		}
	}

	&menu(@menus);
}

#================================================
# ���I��
#================================================
sub tp_1 {
	return if &is_ng_cmd(1..$#war_marchs+1);
	--$cmd;

	# �ÎE�����͒��������֎~
	if ($m{unit} eq '11' && $cmd eq '2') {
		$mes .= "$units[$m{unit}][1]��$war_marchs[$cmd][0]�Ői�R���邱�Ƃ��ł��܂���<br>";
		&begin;
	}
	elsif (!&{$war_marchs[$cmd][3]}) {
		$mes .= "$war_marchs[$cmd][0]�Ői�R��������𖞂����Ă��܂���<br>";
		&begin;
	}
	elsif (defined $war_marchs[$cmd]) {
		$m{value} = $cmd;
		$mes .= "$war_marchs[$cmd][0]�Ői�R���܂�<br>";
		$mes .= '�ǂ̍��ɍU�ߍ��݂܂���?<br>';
		
		&menu('��߂�', @countries);
		$m{tp} = 100;
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin;
	}
}

#================================================
# �푈���
#================================================
sub tp_100 {
	return if &is_ng_cmd(1..$w{country});

	if ($m{country} eq $cmd) {
		$mes .= '�����͑I�ׂ܂���<br>';
		&begin;
	}
	elsif ($cs{is_die}[$cmd]) {
		$mes .= '�ł�ł��鍑�͍U�ߍ��߂܂���<br>';
		&begin;
	}
	elsif ($union eq $cmd) {
		$mes .= '�������ɍU�ߍ��ނ��Ƃ͂ł��܂���<br>';
		&begin;
	}
	elsif ($need_costs > $cs{food}[$m{country}]) {
		$mes .= "�i�R����̂ɕK�v��$e2j{food}������܂���<br>";
		&begin;
	}
	elsif ($need_costs > $cs{money}[$m{country}]) {
		$mes .= "�i�R����̂ɕK�v��$e2j{money}������܂���<br>";
		&begin;
	}
	elsif ($rank_sols[$m{rank}] * $war_marchs[$m{value}][1] > $cs{soldier}[$m{country}]) {
		$mes .= "$e2j{soldier}������܂���<br>��������镺�m�����Ȃ��Ȃ��Ă��܂��܂�<br>";
		&begin;
	}
	# �i�R
	elsif ($cmd && defined $war_marchs[$m{value}]) {
		$m{lib} = 'war';
		$m{tp}  = 100;
		$y{country} = $cmd;
		
		# ���E��u�����v
		if (($w{world} eq '15' || ($w{world} eq '19' && $w{world_sub} eq '15'))) {
			$y{country} = int(rand($w{country}))+1;
			if ($cs{is_die}[&get_most_strong_country]){
				my $loop = 0;
				while ($cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union){
					if($loop > 30) {
						$y{country} = &get_most_strong_country;
					}
					$y{country} = int(rand($w{country}))+1;
					$loop++;
				}
			}else {
				$y{country} = &get_most_strong_country if rand(3) < 1 || $cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union;
			}
		} elsif ($w{world} eq $#world_states - 5) {
			$y{country} = int(rand($w{country}))+1;
			my $loop = 0;
			while ($cs{is_die}[$y{country}] || $y{country} eq $m{country} || $y{country} eq $union){
				if($loop > 30) {
					$y{country} = &get_most_strong_country;
				}
				$y{country} = int(rand($w{country}))+1;
				$loop++;
			}
		}
		
		my $v = int( $rank_sols[$m{rank}] * $war_marchs[$m{value}][1] );

		$cs{soldier}[$m{country}] -= $v;
		$cs{food}[$m{country}]    -= int($need_costs);
		$cs{money}[$m{country}]   -= int($need_costs);
		
		$m{sol} = int( $v + int($m{cha} * 0.005) * 500 ); # cha200�������Ƃ�+500
		$m{sol} += 500 if($m{cha} == 999); # cha999��+500
		$m{value} = $war_marchs[$m{value}][1];

		$GWT = &_unit_march($GWT * $m{value});

		$mes .= "$v�̕��𗦂���$cs{name}[$y{country}]�ɐi�R���J�n���܂�<br>";
		$mes .= "$GWT����ɓ�������\\��ł�<br>";

		if ($y{country} eq $m{renzoku}) {
			++$m{renzoku_c};
		}
		else {
			$m{renzoku} = $y{country};
			$m{renzoku_c} = 1;
		}

		&before_action('icon_pet_exp', $GWT);
		&wait;
		&write_cs;
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin;
	}
}

#================================================
# �����ɂ��i�R���Ԃ̑���(�ɒ[�ɒ������E�Z�����͹ް����ݽ���󂷂�̂Ŏ��Ԑ���)
#================================================
sub _unit_march {
	my $need_GWT = shift;
	# �d���B�ō��i�R����90��
	if ($m{unit} eq '1' && ($pets[$m{pet}][2] ne 'speed_up' || ($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17'))) && $need_GWT * 1.5 < 90) {
		$need_GWT = $need_GWT * 1.5;
	}
	# �V�n,�򗳁B�Œ�i�R����20��
	elsif ( ($m{unit} eq '7' || $m{unit} eq '8' || ($pets[$m{pet}][2] eq 'speed_up' && $w{world} ne '17')) && $need_GWT * 0.5 > 20 && $m{unit} ne '18') {
		$need_GWT = $need_GWT * 0.5;
	}

	if ($pets[$m{pet}][2] eq 'speed_down' && $w{world} ne '17') {
		$need_GWT *= $m{unit} eq '7' || $m{unit} eq '8' ? 4 : 2;
		$m{value} *= 3 unless $m{unit} eq '18';
	}
	elsif ($m{pet} eq '193' && $w{world} ne '7'
#	&& $w{world} ne $#world_states	
	) {
		$need_GWT -= 10;
		$need_GWT = 20 if $m{value} > 1 && $need_GWT < 20;
	}
	return int($need_GWT);
}


1; # �폜�s��
