#================================================
# �̍��؂�ւ� Created by Merino
#================================================

# ���R�̍����g�p�\�Ȑ���
my $free_shogo_sedai = 15;

# @shogos�ȊO�̓��ʂȏ̍� ���w���x��t���Ȃ��Ǝ��R�̍��łȂ邱�Ƃ��\
my @special_shogos = (
	# �̍���,		��ڲ԰��
#	['���Ǘ��l��',	'�Ǘ��Җ�'],
#	['�����Ǘ��l',	'�������'],
	['���I�Ǒ�s�a',	'�ϑԕ���'],
);


#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0] �͏̍���ύX���邱�Ƃ��ł��܂���<br>";
		$mes .= "�ŋ��Z�ł����𕥂��Ă�������<br>";
		&refresh;
		&n_menu;
		return 0;
	}elsif ($m{shogo_t} ne ''){
		$mes .= "�����ς���Ȃ�ĂƂ�ł��Ȃ�<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	
	return 1;
}

#================================================
sub begin {
	&n_menu;
	$layout = 2;
	my $count = 0;
	my $sub_mes = qq|<input type="radio" name="no" value="0">�Ȃ�<br>|;
	#-----------------------------------
	# �W���̍�
	for my $i (1 .. $#shogos) {
		my($k, $v) = each %{ $shogos[$i][1] };
		if ($m{$k} >= $v) {
			$sub_mes .= $m{shogo} eq $shogos[$i][0]
				? qq|<input type="radio" name="no" value="$i" checked>$shogos[$i][0]<br>|
				: qq|<input type="radio" name="no" value="$i">$shogos[$i][0]<br>|
				;
			++$count;
		}
	}
	#-----------------------------------
	# �}�X�^�[
	if (-f "$userdir/$id/shogo_master_flag.cgi") {
		$sub_mes .= $m{shogo} eq $shogos[2][0]
			? qq|<input type="radio" name="no" value="2" checked>$shogos[2][0]<br>|
			: qq|<input type="radio" name="no" value="2">$shogos[2][0]<br>|
			;
	}
	elsif ($count == $#shogos - 2) {
		&write_comp_legend;
	}
	#-----------------------------------
	# ���ʂȏ̍�
	for my $i (0 .. $#special_shogos) {
		$i+=1000;
		if ($m{name} eq $special_shogos[$i-1000][1]) {
			$sub_mes .= $m{shogo} eq $special_shogos[$i-1000][0]
				? qq|<input type="radio" name="no" value="$i" checked>$special_shogos[$i-1000][0]<br>|
				: qq|<input type="radio" name="no" value="$i">$special_shogos[$i-1000][0]<br>|
				;
		}
	}

	#-----------------------------------
	# �t���[�̍�
	$sub_mes .= qq|<p>���R�̍��F�S�p5(���p10)�����܂�<br><input type="text" name="free_shogo" class="text_box_s"></p>| if $m{sedai} >= $free_shogo_sedai;

	my $comp_par = $count <= 0 ? 0 : int($count / ($#shogos-2) * 100);
	$comp_par = 100 if $comp_par > 100;
	
	$mes .= qq|�y$m{name}�̎擾�̍��ꗗ�z�s���ߗ� <b>$comp_par</b>%�t<hr>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�ύX����" class="button1"></form>|;
}

#================================================
sub tp_1 {
	#-----------------------------------
	# �t���[�̍�
	if ($in{free_shogo} && $m{sedai} >= $free_shogo_sedai) {
		&error("���R�̍��ɕs���ȕ���( ,;\"\'&<> )���܂܂�Ă��܂�") if $in{free_shogo} =~ /[,;\"\'&<>]/;
		&error("���R�̍��ɔ��p�����݂͎̂g���܂���") if $in{free_shogo} =~ /^\d+$/;
		&error("���R�̍����������܂��S�p5(���p10)�����܂łł�") if length $in{free_shogo} > 10;
		
		$in{free_shogo} =~ s/��/��/g;
		$m{shogo} = $in{free_shogo};
		$mes .= "$m{shogo}�ɕύX���܂���<br>";
	}
	#-----------------------------------
	# ���ʂȏ̍�
	elsif ($in{no} >= 1000 && $m{name} eq $special_shogos[$in{no}-1000][1]) {
		$m{shogo} = $special_shogos[$in{no}-1000][0];
		$mes .= "$m{shogo}�ɕύX���܂���<br>";
	}
	elsif (defined $in{no} && defined $shogos[$in{no}] && $shogos[$in{no}][0] ne $m{shogo}) {
		my($k, $v) = each %{ $shogos[$in{no}][1] };
		#-----------------------------------
		# �}�X�^�[
		if ($in{no} eq '2' && -f "$userdir/$id/shogo_master_flag.cgi") {
			$m{shogo} = $shogos[$in{no}][0];
			$mes .= "$m{shogo}�ɕύX���܂���<br>";
		}
		#-----------------------------------
		# �W���̍�
		elsif ($m{$k} >= $v) {
			$m{shogo} = $shogos[$in{no}][0];
			if ($m{shogo}) {
				$mes .= "$m{shogo}�ɕύX���܂���<br>";
			}
			else {
				$mes .= "�̍����O���܂���<br>";
			}
		}
		else {
			$mes .= '��߂܂���<br>';
		}
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&refresh;
	&n_menu;
}

#=================================================
# ����ذď����׸�̧�ٍ쐬
#=================================================
sub write_comp_legend {
	&write_legend('comp_shogo', "$c_m��$m{name}���S�Ă̏̍�����ɓ����", 1);
	&mes_and_world_news("<i>�S�Ă̏̍������ذĂ��܂����B$m{name}��$shogos[2][0]�̏̍������������܂���</i>");

	open my $fh, "> $userdir/$id/shogo_master_flag.cgi" or &error("$userdir/$id/shogo_master_flag.cgi̧�ق��J���܂���");
	close $fh;
}


1; # �폜�s��
