#=================================================
# ���� Created by Merino
#=================================================

# �ŗ��F����70�̐����𑝂₷�Ɠ�Փx���ȒP�ɁA���炷�Ɠ�Փx������Ȃ��
sub tax { ($cs{tax}[$m{country}] + 70) * 0.01 };

# ���K�͂̎���
my $GWT_s = int($GWT * 0.6);

# ��K�͂̎���
my $GWT_b = int($GWT * 2);

# ���K�͂̎���
my $GWT_l = int($GWT * 4);

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		if ($m{act} >= 100) {
			$mes .= "�x�����Ƃ�܂�<br>���ɍs���ł���̂� $GWT����ł�";
			$m{act} = 0;
			&refresh;
			&wait;
			return 0;
		}
		else {
			$mes .= '���ɑ����ĂȂ��ƍs�����Ƃ��ł��܂���<br>�d������ɂ́u�����v���u�d���v����s���Ă݂�������I��ł�������<br>';
			&refresh;
			&n_menu;
			return 0;
		}
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= "���ɉ����s���܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= '�������s�������̎����𑝂₵�܂�<br>�ǂ���s���܂���?<br>';
	}
	
	&menu('��߂�','�_��','����','����','��������');
}
sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	if    ($cmd eq '1') { $mes .= "�������̎悵�č���$e2j{food}�𑝂₵�܂�<br>"; }
	elsif ($cmd eq '2') { $mes .= "�������炨���𒥐ł�����$e2j{money}�𑝂₵�܂�<br>"; }
	elsif ($cmd eq '3') { $mes .= "���m���W���č���$e2j{soldier}�𑝂₵�܂�<br>��1�l�ɂ�1G<br>"; }
	elsif ($cmd eq '4') { $mes .= "�_��,����,�������܂Ƃ߂čs���܂�<br>"; $GWT_s *= 3; $GWT_b *= 3; $GWT *= 3; $GWT_l *= 3; }

	$m{tp} = $cmd * 100;
	$mes .= '�ǂ̂��炢�s���܂���?<br>';
	
	my @size = ('��߂�', "���K��    ($GWT_s��)", "���K��    ($GWT��)", "��K��    ($GWT_b��)");
	push @size, "���K��    ($GWT_l��)" if ($cmd eq '4');
	&menu(@size);
}

#=================================================
# ����
#=================================================
sub tp_100 { &exe1('�������̎悵�܂�<br>') }
sub tp_200 { &exe1('�����𒥐ł��܂�<br>') }
sub tp_300 { &exe1('���m���ٗp���܂�<br>') }
sub exe1 {
	return if &is_ng_cmd(1..3);
	$GWT = $cmd eq '1' ? $GWT_s
		 : $cmd eq '3' ? $GWT_b
		 :               $GWT
		 ;

	$m{tp} += 10;
	$m{turn} = $cmd;
	$mes .= "$_[0]���ʂ�$GWT����<br>";
	&before_action('icon_pet_exp', $GWT);
	&wait;
}
#=================================================
# ��������
#=================================================
sub tp_400 {
	return if &is_ng_cmd(1..4);

	$GWT = $cmd eq '1' ? $GWT_s * 3
		 : $cmd eq '3' ? $GWT_b * 3
		 : $cmd eq '4' ? $GWT_l * 3
		 :               $GWT   * 3
		 ;
	
	if ($m{nou_c} >= 5 && $m{sho_c} >= 5 && $m{hei_c} >= 5) {
		$m{tp} += 10;
		$m{turn} = $cmd;
		if($cmd eq '4'){
			$m{turn} = 5;
		}
		$mes .= "$_[0]���ʂ�$GWT����<br>";

		&before_action('icon_pet_exp', $GWT);
		&wait;
	}
	else {
		$mes .= "�����������s���ɂ́A�_��,����,�����̏n���x��5��ȏ�łȂ��Ƃł��܂���<br>";
		&begin;
	}
}
#=================================================
# ������&�N��{�[�i�X
#=================================================
sub dom_ceo_bonus {
	my $v = shift;
	# �������͓�����1.1�{
	return $v * 1.1 if $cs{dom}[$m{country}] eq $m{name};
	# �N��͓�����1.05�{�A�\�N���Ȃ��1.2�{
	if ($cs{ceo}[$m{country}] eq $m{name}) {
		return $v * ( ($w{world} eq '4' || ($w{world} eq '19' && $w{world_sub} eq '4')) ? 1.2 : 1.05 );
	}
	return $v;
}
#=================================================
# �_�ƌ���
#=================================================
sub tp_110 {
	my $v = ($m{nou_c} + $m{mat}) * $m{turn} * 10;
	$v  = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '1') {
		$v *= 1.5; # �L��
	}
	elsif ($cs{state}[$m{country}] eq '3') {
		$v *= 0.5; # �\��
	}
	
	$v = dom_ceo_bonus($v);
#	if ($cs{dom}[$m{country}] eq $m{name}) {
#		$v *= 1.1; # ��\�{�[�i�X
#	}elsif ($cs{ceo}[$m{country}] eq $m{name}) {
#		$v *= 1.05;
#	}
	
	# �e���ݒ�
	$v *= &get_modify('dom');
	
	$v = &use_pet('nou', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '28');
	
	$v = &seed_bonus('nou', $v);
	# �b��
	$v = &seed_bonus('red_moon', $v);
	
	$v = int($v);
	
	$cs{food}[$m{country}] += $v;
	$mes .= "������ $v �̎悵�܂���<br>";
	
	&c_up('nou_c') for (1..$m{turn});
	&write_yran('nou', $v, 1);
	
	return if $m{tp} eq '410';
	&after1;
}
#=================================================
# ���ƌ���
#=================================================
sub tp_210 {
	my $v = ($m{sho_c} + $m{cha}) * $m{turn} * 10;
	$v = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '2') {
		$v *= 1.5; # �i�C
	}
	elsif ($cs{state}[$m{country}] eq '4') {
		$v *= 0.5; # �s��
	}
	
	$v = dom_ceo_bonus($v);
#	if ($cs{dom}[$m{country}] eq $m{name}) {
#		$v *= 1.1; # ��\�{�[�i�X
#	} elsif ($cs{ceo}[$m{country}] eq $m{name}) {
#		$v *= 1.05;
#	}
	
	# �e���ݒ�
	$v *= &get_modify('dom');
	
	$v = &use_pet('sho', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '29');
	
	$v = &seed_bonus('sho', $v);
	# �b��
	$v = &seed_bonus('red_moon', $v);
	
	$v = int($v);

	$cs{money}[$m{country}] += $v;
	$mes .= "������ $v ���ł��܂���<br>";

	&c_up('sho_c') for (1..$m{turn});
	&write_yran('sho', $v, 1);

	return if $m{tp} eq '410';
	&after1;
}
#=================================================
# ��������
#=================================================
sub tp_310 {
	my $v = ($m{hei_c} + $m{cha}) * $m{turn} * 10;
	$v = $v > 10000 * $m{turn} ? (rand(1000) + 9000) * $m{turn} * &tax : $v * &tax;

	if ($cs{state}[$m{country}] eq '5') {
		$v *= 0.5; # �Q�[
	}
	
	$v = dom_ceo_bonus($v);
#	if ($cs{dom}[$m{country}] eq $m{name}) {
#		$v *= 1.1; # ��\�{�[�i�X
#	}elsif ($cs{ceo}[$m{country}] eq $m{name}) {
#		$v *= 1.05;
#	}
	
	# �e���ݒ�
	$v *= &get_modify('dom');
	
	if ($v < $m{money}){
		$v = &use_pet('hei', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '30');
	}
	
	$v = &seed_bonus('hei', $v);
	# �b��
	$v = &seed_bonus('red_moon', $v);

	$v = int($v);

	$v = $m{money} if $v > $m{money};
	$v = 0 if 0 > $m{money};
	$m{money} -= $v;

	$cs{soldier}[$m{country}] += $v;
	$mes .= "���m�� $v �l�ٗp���܂���<br>";

	if (0 < $v && 0 < $m{money}){
		&c_up('hei_c') for (1..$m{turn});
		&write_yran('hei', $v, 1);
	}

	return if $m{tp} eq '410';
	
	# �����͂�����������̂ŁA�o���l�ƕ]�������������׽
	$m{turn} += 2 if 0 < $v && 0 < $m{money};
	&after1;
}
#=================================================
# ������������
#=================================================
sub tp_410 {
	&tp_110;
	&tp_210;
	&tp_310;
	$m{turn} *= 4;
	&after1;
}

#=================================================
# �I������
#=================================================
sub after1 {
	my $v = int( (rand(3)+4) * $m{turn} );
	$v = &use_pet('domestic', $v) unless (($w{world} eq '17' || ($w{world} eq '19' && $w{world_sub} eq '17')) && $m{pet} ne '160');
	$m{exp} += $v;
	$m{rank_exp} += int( (rand($m{turn}) + $m{turn}) * 2);
	$m{egg_c} += int(rand(3)+3) if $m{egg};
	
	$mes .= "$m{name}�ɑ΂���]�����オ��܂���<br>";
	$mes .= "$v ��$e2j{exp}����ɓ���܂���<br>";

	# ��J��
	$m{act} = 0;
	$mes .= '��J���񕜂��܂���<br>';
	
	&special_money if ($w{world} eq '1' || ($w{world} eq '19' && $w{world_sub} eq '1'));

	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('domestic');
	}
	
	&daihyo_c_up('dom_c'); # ��\�n���x
	&refresh;
	&n_menu;
	&write_cs;
}


#=================================================
# ���J��
#=================================================
sub special_money {
	my $v = int($m{rank} * 150 * $m{turn});
	$m{money} += $v;
	$mes .= "���܂ł̌��т��F�߂�� $v G�̌��J������������ꂽ<br>";
}





1; # �폜�s��
