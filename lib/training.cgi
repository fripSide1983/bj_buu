#================================================
# �C�s Created by Merino
#================================================
require "$datadir/skill.cgi";

# �ΐ�ґI���ł̕\����
my $max_training_member = 25;


#================================================
# ���p����
#================================================
sub is_satisfy {
	if ($m{tp} <= 1 && $m{hp} < 5) {
		$mes .= "�C�s������̂�$e2j{hp}�����Ȃ����܂�<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ��J���Ă���ꍇ�͍s���Ȃ�
		return 0;
	}
	return 1;
}

#================================================
sub begin {
	$m{turn} = 0;
	$mes .= '���̐l�Ɛ킢�Ȃ�b���܂�<br>';
	$mes .= '�N�Ɛ킢�܂���?<br>';
	
#	if ($y{icon} && $y{name}) { # �O��̐퓬�n���ۂ��f�[�^���c���Ă���
#		&menu('��߂�','�ΐ�ґI��','�O��̑ΐ푊��');
#	}
#	else {
		&menu('��߂�','�ΐ�ґI��',);
#	}
}

#================================================
# �ΐ�҈ꗗ�\��
#================================================
sub tp_1 {
	if ($cmd eq '1') {
		$layout = 1;
		my $m_st = &m_st;
		
		$mes .= qq|�擾$e2j{exp}<br><font color="#FF0000">����</font>�F���� �����F���� <font color="#3366FF">����</font>�F���Ȃ�<br>|;
		$mes .= qq|<form method="$method" action="$script"><input type="radio" name="cmd" value="0" checked> ��߂�<br>|;
		$mes .= qq|<input type="radio" name="cmd" value="myself"> ���޳ ${e2j{hp}}[$m{max_hp}] ����[$m_st] ����[$weas[$m{wea}][2]]<br>|;
		open my $fh, "< $logdir/training.cgi" or &error("�ڰ�ݸ�̧�ق��ǂݍ��߂܂���");
		while (my $line = <$fh>) {
			my($no,$name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$wea_name,$gua) = split /<>/, $line;
			
			next if $name eq $m{name};
			my $y_st = int($max_hp + $max_mp + $at + $df + $mat + $mdf + $ag + $cha * 0.5);
			my $st_lv = &st_lv($y_st);
			
			my $font_color = $st_lv eq '2' ? '#FF0000'
						   : $st_lv eq '0' ? '#0000FF'
						   :                 '#CCCCCC'
						   ;
			
			my $skill_str = '';
			my @y_skills = split /,/, $skills;
			for my $i (0..3){
				$skill_str .= $y_skills[$i] == 0 ? "�U��,":"$skills[$y_skills[$i]][1],";
			}
			$skill_str .= $y_skills[4] == 0 ? "�U��":"$skills[$y_skills[4]][1]";
			
			$mes .= qq|<input type="radio" name="cmd" value="$no"><font color="$font_color"> $name ${e2j{hp}}[$max_hp] ����[$y_st] ����[$weas[$wea][2]] �Z$skill_str �h��[$guas[$gua][1]]</font><br>|;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
		
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="�C�s����" class="button1"></form>|;
		$m{tp} = 100;
	}
	elsif ($cmd eq '2' && $y{max_hp} && $y{name}) {
		$y{hp} = $y{max_hp};
		$y{mp} = $y{max_mp};
		$mes .= "$y{name}�Ɛ킢�܂�<br>";
		&n_menu;
		
		$m{tp} = 200;
	}
	else {
		&begin;
	}
}

#================================================
# ����f�[�^�擾
#================================================
sub tp_100 {
	if ($cmd eq 'myself') {
		for my $k (qw/country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name gua/) {
			$y{$k} = $m{$k};
		}
		$y{name} = '���޳';
		$y{hp}   = $m{max_hp};
		$y{mp}   = $m{max_mp};
		$mes .= "$y{name}�Ɛ킢�܂�<br>";
		$m{tp} = 200;
		&n_menu;
	}
	elsif ($cmd) {
		my $is_find   = 0;
		my $is_myself = 0;
		my @lines = ();
		open my $fh, "+< $logdir/training.cgi" or &error("�ڰ�ݸ�̧�ق��ǂݍ��߂܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($no,$name,$country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$wea_name,$gua) = split /<>/, $line;
			($country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$wea_name,$gua) = map { $_ =~ tr/\x0D\x0A//d; $_; } ($country,$max_hp,$max_mp,$at,$df,$mat,$mdf,$ag,$cha,$wea,$skills,$mes_win,$mes_lose,$icon,$wea_name,$gua);
			if ($cmd == $no) {
				$is_find = 1;
				
				$y{name} = $name eq $m{name} ? '���޳' : $name;
				$y{country} = $country;
				$y{max_hp} = $max_hp;
				$y{hp}     = $max_hp;
				$y{max_mp} = $max_mp;
				$y{mp}     = $max_mp;
				$y{at}   = $at;
				$y{df}   = $df;
				$y{mat}  = $mat;
				$y{mdf}  = $mdf;
				$y{ag}   = $ag;
				$y{cha}  = $cha;
				$y{wea}  = $wea;
				$y{gua}  = $gua;
				$y{skills}  = $skills;
				$y{mes_win}  = $mes_win;
				$y{mes_lose} = $mes_lose;
				$y{icon} = -f "$icondir/$icon" ? $icon : $default_icon;
				$y{wea_name} = $wea_name;
			}
			# �����̃f�[�^�X�V
			if ($name eq $m{name}) {
				$is_myself = 1;
				$line = "$no<>$m{name}<>$m{country}<>$m{max_hp}<>$m{max_mp}<>$m{at}<>$m{df}<>$m{mat}<>$m{mdf}<>$m{ag}<>$m{cha}<>$m{wea}<>$m{skills}<>$m{mes_win}<>$m{mes_lose}<>$m{icon}<>$m{wea_name}<>$m{gua}<>\n";
			}
			push @lines, $line;
			
			last if @lines > $max_training_member;
		}
		unless ($is_myself) {
			my($last_no) = (split /<>/, $lines[0])[0];
			++$last_no;
			unshift @lines, "$last_no<>$m{name}<>$m{country}<>$m{max_hp}<>$m{max_mp}<>$m{at}<>$m{df}<>$m{mat}<>$m{mdf}<>$m{ag}<>$m{cha}<>$m{wea}<>$m{skills}<>$m{mes_win}<>$m{mes_lose}<>$m{icon}<>$m{wea_name}<>$m{gua}<>\n";
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		if ($is_find) {
			$mes .= "$y{name}�Ɛ킢�܂�<br>";
			$m{tp} = 200;
			&n_menu;
		}
		else {
			$mes .= '�ΐ푊�肪������܂���ł���<br>';
			$m{tp} = 1;
			&begin;
		}
	}
	else {
		$mes .= '��߂܂���<br>';
		&refresh;
		&n_menu;
	}
}

#================================================
# �퓬
#================================================
sub tp_200 {
	require './lib/battle.cgi';
	
	if ($m{hp} <= 0) {
		$m{act} += 10;
		my $v = int( rand(5) + 5 );
		$m{exp} += $v;

		$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
		&run_tutorial_quest('tutorial_training_1');

		&refresh;
		&n_menu;
	}
	elsif ($y{hp} <= 0) {
		$m{act} += 5;
		&c_up('shu_c');

		# İ�ٽð������������҂��ƌo���l���Ȃ�
		my $st_lv = &st_lv;
		my $v = $st_lv eq '2' ? int( rand(10)+ 15 ) 
			  : $st_lv eq '0' ? int( rand(3) + 3 )
			  :                 int( rand(5) + 8 )
			  ;
		$v = int(rand(15) + 25) if ($m{master_c} eq 'shu_c');
		$v = &use_pet('training', $v);
		$m{exp} += $v;
		$m{egg_c} += 1 if $m{egg};
	
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('training');
		}
		
		$mes .= "$v��$e2j{exp}����ɓ���܂���<br>";
		$mes .= '�C�s�𑱂��܂���?<br>';
		&run_tutorial_quest('tutorial_training_1');

		&menu('������','�ΐ푊��ύX','��߂�');
		$m{tp} += 10;
	}
}

#================================================
# �p�� or ��߂�
#================================================
sub tp_210 {
	if ($cmd eq '0') {
		$cmd = 2;
		&tp_1;
	}
	elsif ($cmd eq '1') {
		$cmd = 1;
		&tp_1;
	}
	else {
		$mes .= '�C�s���I�����܂�<br>';
		&refresh;
		&n_menu;
	}
}




1; # �폜�s��
