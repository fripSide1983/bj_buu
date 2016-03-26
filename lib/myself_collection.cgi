require './lib/add_collection.cgi';
#=================================================
# �ڸ���ٰ� Created by Merino
#=================================================

# �ڸ�������,legenḑ��,�ꎞ�I�̍�
my @collections = (
	['����}��', 'comp_wea', '���ŏI����'],
	['�Ϻސ}��', 'comp_egg', '��������'],
	['�߯Đ}��', 'comp_pet', '���߯Ėq��'],
	['�h��}��', 'comp_gua', '���h�q���u'],
);


#=================================================
sub begin {	
	$layout = 2;
	my @lines = &add_collection;
	my $kind = 1;
	for my $line (@lines) {
		$line =~ tr/\x0D\x0A//d;
		
		my $count = 0;
		my $sub_mes  = '';
		for my $no (split /,/, $line) {
			next if $no eq ''; # �擪�̋�
			next if $kind == 2 && $no == 53;
			next if $kind == 3 && $no == 180;
			next if $kind == 3 && $no == 181;
			next if $kind == 3 && $no == 195;
			++$count;
			next unless $no;
			$sub_mes .= $kind eq '1' ? "<li>[$weas[$no][2]]$weas[$no][1]</li>"
					  : $kind eq '2' ? "<li>$eggs[$no][1]</li>"
					  : $kind eq '3' ? "<li>$pets[$no][1]</li>"
					  :                "<li>[$guas[$no][2]]$guas[$no][1]</li>"
					  ;
		}
		
		my $comp_par = 0;
		if ($count > 0) {
			if ($kind eq '1') {
				$comp_par = int($count / $#weas * 100);
				$comp_par = 100 if $comp_par > 100;
				&write_comp_legend($kind) if $count eq $#weas;
			}
			elsif ($kind eq '2') {
				$comp_par = int($count / ($#eggs - 1) * 100);
				$comp_par = 100 if $comp_par > 100;
				&write_comp_legend($kind) if $count eq ($#eggs - 1);
			}
			elsif ($kind eq '3') {
				$comp_par = int($count / ($#pets - 3) * 100);
				$comp_par = 100 if $comp_par > 100;
				&write_comp_legend($kind) if $count eq ($#pets - 3);
			}
		}
		
		$mes .= "$collections[$kind-1][0] �s���ߗ� $comp_par%�t<br>";
		$mes .= "<ul> $sub_mes </ul>";
		
		++$kind;
	}
	
	&refresh;
	&n_menu;
}

#=================================================
# ����ذď���
#=================================================
sub write_comp_legend {
	my $kind = shift;
	
	&write_legend($collections[$kind-1][1], "$c_m��$m{name}��$collections[$kind-1][0]�����ذĂ���", 1);
	&mes_and_world_news("<i>$collections[$kind-1][0]�����ذĂ��܂����B$m{name}��$collections[$kind-1][2]�̏̍������������܂���</i>");
	
	# �ꎞ�I�ȏ̍�
	$m{shogo} = $collections[$kind-1][2];

	$kind--;
	# 0 ��ǉ����邱�Ƃ� 100%�𒴂��邱�ƂɂȂ�
	my @lines = ();
	open my $fh, "+< $userdir/$id/collection.cgi" or &error("�ڸ���̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if ($kind eq @lines) {
			$line =~ tr/\x0D\x0A//d; # \n���s�폜
			$line .= "0,\n";
		}
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


1; # �폜�s��
