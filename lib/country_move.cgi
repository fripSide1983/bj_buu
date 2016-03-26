require './lib/move_player.cgi';
#=================================================
# �d�� Created by Merino
#=================================================

# �S������
$GWT *= 2;

# �d������̂ɕK�v������
my $need_lv = 1;

# �d������̂ɕK�v�ȋ��z
my $need_money = $m{sedai} > 100 ? $rank_sols[$m{rank}]+300000 : $rank_sols[$m{rank}]+$m{sedai}*3000;

# ���E����Í��̏ꍇ�ANPC���֎d������̂ɕK�v�ȋ��z
my $need_money_npc = 1000000;

# �K���d���̐_�l�~�Պm��(���̈�)
my $random_god_par = 20;

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�͎d�����邱�Ƃ��ł��܂���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{lv} < $need_lv) {
		$mes .= "�d������ɂ� $need_lv ���وȏ�K�v�ł�<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($m{random_migrate} eq $w{year}) {
		$mes .= "���N�����ς��͈ڐЂł��܂���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{country}) {
		$mes .= "�d������葱���Ƃ���$GWT��������܂�<br>";
		$mes .= "���̍��Ɏd������Ƒ�\\���߲�ĂƊK����������܂�<br>";
		$mes .= "�������Ɏd������ꍇ�͊K����������܂���<br>" if $union;
		$mes .= "�ڐЗ��Ƃ��� $need_money G�x�����K�v������܂�<br>";
		
		# �Í�
		if ($w{world} eq $#world_states) {
			$mes .= qq|<font color="#FF0000">$cs{name}[$w{country}]�Ɏd������ꍇ�́A���̔N�ɂȂ�܂ő��̍��Ɏd�����邱�Ƃ͂ł��܂���<br>|;
			$mes .= qq|$cs{name}[$w{country}]�Ɏd������ꍇ�́A��\\�߲�Ă� 0 �ɂȂ�A$need_money_npc G�x�����K�v������܂�<br></font>|;
		}
		
		$mes .= '�ǂ̍��Ɏd�����܂���?<br>';
		
		&menu('��߂�', @countries, '���Q����');
	}
	else {
		if ($w{world} eq $#world_states) {
			$mes .= qq|<font color="#FF0000">$cs{name}[$w{country}]�Ɏd������ꍇ�́A���̔N�ɂȂ�܂ő��̍��Ɏd�����邱�Ƃ͂ł��܂���<br>|;
			$mes .= qq|$cs{name}[$w{country}]�Ɏd������ꍇ�́A��\\�߲�Ă� 0 �ɂȂ�A$need_money_npc G�x�����K�v������܂�<br></font>|;
		}
		$mes .= '�ǂ̍��Ɏd�����܂���?<br>';
		&menu('��߂�', @countries, '�K��');
	}
}

sub tp_1 {
	return if &is_ng_cmd(1 .. $w{country}+1);

	$m{tp} = 200;
	&{ 'tp_'.$m{tp} };
}

sub tp_200 {
	if (&is_ng_cmd(1 .. $w{country}+1)){
		&refresh;
		return;
	}
	if($cmd <= $w{country}){
		my $line = &get_countries_mes($cmd);
		my($country_mes, $country_mark, $country_rule) = split /<>/, $line;
		$mes .= $country_rule;
	}
	$mes .= '<br>�{���Ɏd�����܂����H';
	$m{value} = $cmd;
	&menu('��߂�','�d��');
	$m{tp} = 300;
}

sub tp_300 {
	if (&is_ng_cmd(1)){
		&refresh;
		&n_menu();
		$mes = '��߂܂���';
		return;
	}
	
	$cmd = $m{value};
	if (&is_ng_cmd(1 .. $w{country}+1)){
		&refresh;
		return;
	}
	
	if ($cmd eq $m{country}) {
		$mes .= "�����Ɏd���͂ł��܂���<br>";
		&begin;
	}
	# �������Q
	elsif ($cmd == $w{country} + 1) {
	      	if($m{country}){
			# ������
			if ($m{name} eq $m{vote}) {
			   $mes .= "$c_m��$e2j{ceo}�̗��������C����K�v������܂�<br>";
			   &begin;
			   return;
			}
			# �Í�
			if ($w{world} eq $#world_states) {
			   if ($m{country} eq $w{country}) {
				$mes .= "$cs{name}[$m{country}]���甲���o�����Ƃ͋�����܂���<br>";
				&begin;
				return;
			   }
			}
			# ����
			if($w{world} eq $#world_states-2 || $w{world} eq $#world_states-3 || $w{world} eq $#world_states-5){
				     $mes .= "���𗣂�邱�Ƃ͂ł��܂���<br>";
				     &begin;
				     return;
			}
			&move_player($m{name}, $m{country}, 0);
			$m{country} = 0;
			$m{rank} = 0;
			$m{rank_exp} = 0;
		
			&mes_and_world_news("$c_m���痧��������Q�̗��ɏo�܂���",1);
		
			# ��\�߲��0
			for my $k (qw/war dom mil pro/) {
			    $m{$k.'_c'} = 0;
			}

			$mes .= "���ɍs���ł���̂�$GWT����ł�<br>";
			&refresh;
			&wait;
		}else {
			$cmd = int(rand($w{country}) + 1);
			# �Í�
			if ($w{world} eq $#world_states) {
				if ($m{country} eq $w{country}) {
					$mes .= "$cs{name}[$m{country}]���甲���o�����Ƃ͋�����܂���<br>";
					&begin;
					return;
				}
				elsif ($cmd eq $w{country}) {
					require './lib/vs_npc.cgi';
					if ($need_money_npc > $m{money}) {
						$mes .= "�����ƌ_�񂷂�ɂ� $need_money_npc G�K�v�ł�<br>";
						&begin;
						return;
					}
					elsif (!&is_move_npc_country) {
						&begin;
						return;
					}
					$need_money = $need_money_npc;
					$m{money} -= $need_money;
					$mes .= "�ڐЗ��Ƃ��� $need_money G�x�����܂���<br>";
					$mes .= "�K����$ranks[$m{rank}]�ɂȂ�܂���<br>";
					$mes .= "�ڐЂ̎葱����$GWT��������܂�<br>" ;
					&wait;
				}
			}
			$m{rank} = 1 if $m{rank} < 1;
			&n_menu;
			if($w{world} eq $#world_states-2){
				$cmd = $w{country} - int(rand(2));
			}
			elsif($w{world} eq $#world_states-3){
				$cmd = $w{country} - int(rand(3));
			}
			&move_player($m{name}, $m{country}, $cmd);
			$m{next_salary} = $time + 3600 * $salary_hour;
			$m{country} = $cmd;
			$m{vote} = '';
			$m{random_migrate} = $w{year};
			&mes_and_world_news("�K����$cs{name}[$cmd]�Ɏd�����܂���",1);
			if (rand($random_god_par) < 1) {
				require './lib/shopping_offertory_box.cgi';
				&get_god_item(5);
			}
			&refresh;
		}
	}
	elsif ($cs{member}[$cmd] >= $cs{capacity}[$cmd]) {
		$mes .= "$cs{name}[$cmd]�͒���������ς��ł�<br>";
		&begin;
	}
	elsif($w{world} eq $#world_state-2){
		if($cmd eq $w{country} || $cmd eq $w{country}-1){
			$cmd2 = $cmd;
		}else{
			$mes .= "���͂��̍��ɂ͎d���ł��܂���<br>";
			&begin;
		}
	}
	elsif (defined $cs{name}[$cmd]) { # �������݂���
		# �������̍�
		if ($m{country}) {
			# �N��
			if ($m{name} eq $cs{ceo}[$m{country}]) {
				$mes .= "$c_m��$e2j{ceo}�����C����K�v������܂�<br>";
				&begin;
				return;
			}
			elsif ($need_money > $m{money}) {
				$mes .= "�ڐЂ���ɂ� $need_money G�K�v�ł�<br>";
				&begin;
				return;
			}
			# �Í�
			elsif ($w{world} eq $#world_states) {
				if ($m{country} eq $w{country}) {
					$mes .= "$cs{name}[$m{country}]���甲���o�����Ƃ͋�����܂���<br>";
					&begin;
					return;
				}
				elsif ($cmd eq $w{country}) {
					require './lib/vs_npc.cgi';
					if ($need_money_npc > $m{money}) {
						$mes .= "�����ƌ_�񂷂�ɂ� $need_money_npc G�K�v�ł�<br>";
						&begin;
						return;
					}
					elsif (!&is_move_npc_country) {
						&begin;
						return;
					}
					$need_money = $need_money_npc;
				}
			}
			# ����
			if($w{world} eq $#world_states-2 || $w{world} eq $#world_states-3 || $w{world} eq $#world_states-5){
				$mes .= "���𗠐؂邱�Ƃ͂ł��܂���<br>";
				&begin;
				return;
			}
		
			$m{money} -= $need_money;
			$cs{money}[$m{country}] += $need_money;
			$mes .= "�ڐЗ��Ƃ��� $need_money G�x�����܂���<br>";
			
			unless ($union eq $cmd) {
				$m{rank} -= $m{rank} > 10 ? 2 : 1;
				$m{rank} = 1 if $m{rank} < 1;
				$mes .= "�K����$ranks[$m{rank}]�ɂȂ�܂���<br>";

				# ��\�߲�Ĕ���
				for my $k (qw/war dom mil pro/) {
					$m{$k.'_c'} = int($m{$k.'_c'} * 0.5);
				}
			}
			
			$mes .= "�ڐЂ̎葱����$GWT��������܂�<br>" ;
			&wait;
		}
		# ����������
		else {
			# �Í�
			if ($w{world} eq $#world_states) {
				if ($m{country} eq $w{country}) {
					$mes .= "$cs{name}[$m{country}]���甲���o�����Ƃ͋�����܂���<br>";
					&begin;
					return;
				}
				elsif ($cmd eq $w{country}) {
					require './lib/vs_npc.cgi';
					if ($need_money_npc > $m{money}) {
						$mes .= "�����ƌ_�񂷂�ɂ� $need_money_npc G�K�v�ł�<br>";
						&begin;
						return;
					}
					elsif (!&is_move_npc_country) {
						&begin;
						return;
					}
					$need_money = $need_money_npc;
					$m{money} -= $need_money;
					$mes .= "�ڐЗ��Ƃ��� $need_money G�x�����܂���<br>";
					$mes .= "�K����$ranks[$m{rank}]�ɂȂ�܂���<br>";
					$mes .= "�ڐЂ̎葱����$GWT��������܂�<br>" ;
					&wait;
				}
			}
			$m{rank} = 1 if $m{rank} < 1;
			&n_menu;
		}

		if($w{world} eq $#world_states-2){
			$cmd = $w{country} - int(rand(2));
		}
		elsif($w{world} eq $#world_states-3){
			$cmd = $w{country} - int(rand(3));
		} elsif($w{world} eq $#world_states-1) {
			$cmd = int(rand($w{country}) + 1);
		}
		
		&move_player($m{name}, $m{country}, $cmd);
		$m{next_salary} = $time + 3600 * $salary_hour;
		$m{country} = $cmd;
		$m{vote} = '';
		
		&mes_and_world_news("$cs{name}[$cmd]�Ɏd�����܂���",1);
		
		&refresh;
	}
	else {
		&begin;
	}
}

sub tp_100 {
	$mes .= '�������犩�U���󂯂܂���<br>';
	$m{tp} += 10;
	&n_menu;
}

sub tp_110 {
	my @head_hunt;
	$mes .= '�ǂ̊��U���󂯂܂���?<br>';
	open my $fh, "+< $userdir/$id/head_hunt.cgi" or &error("$userdir/$id/head_hunt.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($hname, $hcountry) = split /<>/, $line;
		push @head_hunt, $cs{name}[$hcountry];
	}
	close $fh;
	$m{tp} += 10;
	&menu('�f��', @head_hunt);
}

sub tp_120 {
	my $i_c = 0;
	open my $fh, "+< $userdir/$id/head_hunt.cgi" or &error("$userdir/$id/head_hunt.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$i_c;
		if($i_c == $cmd){
			my($hname, $hcountry) = split /<>/, $line;
			if ($hcountry eq $m{country}) {
				$mes .= "�����Ɏd���͂ł��܂���<br>";
				&begin;
			}
			elsif (defined $cs{name}[$hcountry]) { # �������݂���
				if ($m{country}) {
					# �N��
					if ($m{name} eq $cs{ceo}[$m{country}]) {
						$mes .= "$c_m��$e2j{ceo}�����C����K�v������܂�<br>";
						&begin;
						return;
					}
					$cs{money}[$m{country}] += $need_money;
				}
				&move_player($m{name}, $m{country}, $hcountry);
				$m{country} = $hcountry;
				$m{vote} = '';
				&mes_and_world_news("$hname�̗U����$cs{name}[$hcountry]�Ɏd�����܂���",1);
			}
			else {
				&begin;
			}
			last;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	close $fh;
	&refresh;
	&n_menu;
}


1; # �폜�s��
