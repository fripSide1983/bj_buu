require "$datadir/skill.cgi";
my $this_file = "$userdir/$id/skill.cgi";
#================================================
# ��ٌp�� Created by Merino
#================================================

#=================================================
sub begin {
	my @m_skills = split /,/, $m{skills};
	my @m_skills_s = split /,/, $m{skills_sub};
	my @m_skills_s2 = split /,/, $m{skills_sub2};
	my @m_skills_s3 = split /,/, $m{skills_sub3};
	$layout = 2;
	if ($m{tp} > 1) {
		$mes .= '���ɉ������܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�K���ς݂̋Z���w�񂾂�A���o���Ă���Z��Y��邱�Ƃ��ł��܂�<br>';
	}

	$mes .= '<hr>�o���Ă���Z<br>';
	for my $no (@m_skills) {
		$mes .= "[$skills[$no][2]]$skills[$no][1],";
	}
	$mes .= '<hr>�Z�b�g���Ă���Z1<br>';
	for my $no (@m_skills_s) {
		$mes .= "[$skills[$no][2]]$skills[$no][1],";
	}
	$mes .= '<hr>�Z�b�g���Ă���Z2<br>';
	for my $no (@m_skills_s2) {
		$mes .= "[$skills[$no][2]]$skills[$no][1],";
	}
	$mes .= '<hr>�Z�b�g���Ă���Z3<br>';
	for my $no (@m_skills_s3) {
		$mes .= "[$skills[$no][2]]$skills[$no][1],";
	}
	$mes .= '<hr>';
	
	open my $fh, "< $this_file" or &error("$this_file���ǂݍ��߂܂���");
	my $line = <$fh>;
	close $fh;
	$line =~ tr/\x0D\x0A//d;
	
	my $count = 0;
	my $sub_mes = '';
	for my $no (split /,/, $line) {
		next if $no eq ''; # �擪�̋�
		
		$sub_mes .= "[$skills[$no][2]]$skills[$no][1] ����$e2j{mp}$skills[$no][3]<br>" if $no;
		++$count;
	}
	my $comp_par = $count <= 0 ? 0 : int($count / $#skills * 100);
	$comp_par = 100 if $comp_par > 100;
	&write_comp_legend if $count eq $#skills;
	
	$mes .= "�K���ς݂̋Z�s���ߗ� <b>$comp_par</b>%�t<hr>";
	$mes .= $sub_mes;
	
	&menu('��߂�','�o����','�Y���','�Z�b�g����','�Z�b�g�Z�ɕύX');
}
sub tp_1 {
	return if &is_ng_cmd(1..4);
	
	$m{tp} = $cmd * 100;
	&{ 'tp_' .$m{tp} };
}


#=================================================
# �o����
#=================================================
sub tp_100 {
	$layout = 2;
	$m{tp} += 10;
	$mes .= "�ǂ̋Z���o���܂���?<br>";
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked> ��߂�<br>|;
	
	open my $fh, "< $this_file" or &error("$this_file���ǂݍ��߂܂���");
	my $line = <$fh>;
	close $fh;
	$line =~ tr/\x0D\x0A//d;
	for my $no (split /,/, $line) {
		next unless $no;
		$mes .= qq|<input type="radio" name="cmd" value="$no">[$skills[$no][2]]$skills[$no][1]<br>|;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= $is_mobile ? qq|<input type="submit" value="�o����" class="button1" accesskey="0"></form>|:
		qq|<input type="submit" value="�o����" class="button1"></form>|;
	&n_menu;
}
sub tp_110 {
	my @m_skills = split /,/, $m{skills};
	if ($cmd) {
		if (@m_skills >= 5) {
			$mes .= '5�܂ł����o���邱�Ƃ��ł��܂���<br>';
		}
		else {
			open my $fh, "< $this_file" or &error("$this_file���ǂݍ��߂܂���");
			my $line = <$fh>;
			close $fh;
			$line =~ tr/\x0D\x0A//d;

			for my $no (split /,/, $line) {
				next unless $no;
				if ($no eq $cmd) {
					$mes .= "[$skills[$no][2]]$skills[$no][1]���o���܂���!<br>";
					$m{skills} .= "$no,";
					last;
				}
			}
		}
	}
	&begin;
}

#=================================================
# �Y���
#=================================================
sub tp_200 {
	$m{tp} += 10;
	$mes .= "�ǂ̋Z��Y��܂���?<br>";
	$mes .= qq|<form method="$method" action="$script">|;
	my $count = 0;
	for my $skill (split /,/, $m{skills}) {
		++$count;
		$mes .= qq|<input type="checkbox" id="no_$count" name="$count" value="1">|;
		$mes .= qq|<label for="no_$count">| unless $is_mobile;
		$mes .= qq|[$skills[$skill][2]]$skills[$skill][1]|;
		$mes .= qq|</label>| unless $is_mobile;
		$mes .= qq|<br>|;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= $is_mobile ? qq|<input type="submit" value="�Y���" class="button1" accesskey="0"></form>|:
		qq|<input type="submit" value="�Y���" class="button1"></form>|;
	&n_menu;

}
sub tp_210 {
	my @m_skills = split /,/, $m{skills};
	my $line = '';
	for my $count (0 .. $#m_skills) {
		if ($in{$count+1}) {
			$mes .= "[$skills[ $m_skills[$count] ][2]]$skills[ $m_skills[$count] ][1]��Y��܂���<br>";
		}
		else {
			$line .= "$m_skills[$count],";
		}
	}
	$m{skills} = $line;
	&begin;
}

sub tp_300{
	$mes .= "���ԂɃZ�b�g���܂����H";
	$m{tp} += 10;
	&menu('��߂�','1','2','3');
}

sub tp_310{
	if($cmd eq '1'){
		$m{skills_sub} = $m{skills};
		$mes .= "���o���Ă���Z���Z�b�g���܂���";
	}elsif($cmd eq '2'){
		$m{skills_sub2} = $m{skills};
		$mes .= "���o���Ă���Z���Z�b�g���܂���";
	}elsif($cmd eq '3'){
		$m{skills_sub3} = $m{skills};
		$mes .= "���o���Ă���Z���Z�b�g���܂���";
	}else{
		$mes .= "��߂܂���";
	}
    &begin;
}


sub tp_400{
	$mes .= "���Ԃ��Z�b�g���܂����H";
	$m{tp} += 10;
	&menu('��߂�','1','2','3');
}

sub tp_410{
	if($cmd eq '1'){
		$m{skills} = $m{skills_sub};
		$mes .= "�Z�b�g���Ă���Z�ɕς��܂���";
	}elsif($cmd eq '2'){
		$m{skills} = $m{skills_sub2};
		$mes .= "�Z�b�g���Ă���Z�ɕς��܂���";
	}elsif($cmd eq '3'){
		$m{skills} = $m{skills_sub3};
		$mes .= "�Z�b�g���Ă���Z�ɕς��܂���";
	}else{
		$mes .= "��߂܂���";
	}
	&begin;
}

#=================================================
# ����ذď���
#=================================================
sub write_comp_legend {
	&write_legend('comp_skill', "$c_m��$m{name}���S�Ă̋Z���ɂ߂�", 1);
	&mes_and_world_news("<i>�S�Ă̋Z�����ذĂ��܂����B$m{name}�Ɂ����`�t�͂̏̍������������܂���</i>");

	# �ꎞ�I�ȏ̍�
	$m{shogo} = '�����`�t��';

	# 0 ��ǉ����邱�Ƃ� ����flag�Ƃ���0��ǉ�100%�𒴂��������ɂȂ�
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��J���܂���");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	$line =~ tr/\x0D\x0A//d; # \n���s�폜
	$line .= '0,';
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	close $fh;
}


1; # �폜�s��
