#================================================
# ��̕ύX Created by Merino
#================================================

my %e2j_serifu = (
	mes			=> 'ү����',
	mes_win		=> '�������',
	mes_lose	=> '�������',
	mes_touitsu	=> '������',
);


#=================================================
sub begin {
	$layout = 2;
	$mes .= qq|<form method="$method" action="$script">|;
	
	for my $k (qw/mes mes_win mes_lose mes_touitsu/) {
		$mes .= qq|$e2j_serifu{$k} [�S�p20(���p40)�����܂�]�F<br><input type="text" name="$k" value="$m{$k}" class="text_box_b"><br>|;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�ύX����" class="button1"></form>|;
	&n_menu;
}

sub tp_1 {
	&refresh;
	my $is_rewrite = 0;
	
	if ($in{mes} || $in{mes_win} || $in{mes_lose} || $in{mes_touitsu}) {
		for my $k (qw/mes mes_win mes_lose mes_touitsu/) {
			unless ($in{$k} eq $m{$k}) {
				&error("$e2j_serifu{$k}�ɕs���ȕ���( ,;\"\'&<> )���܂܂�Ă��܂�") if $in{$k} =~ /[ ,;\"\'&<>]/;
				&error("$e2j_serifu{$k}�͑S�p20(���p40)�����܂łł�") if length $in{$k} > 40;
				$m{$k} = $in{$k};
				$mes .= "$e2j_serifu{$k}��$in{$k}�ɕύX���܂���<br>";
				$is_rewrite = 1;
			}
		}
	}
	
	$mes .= '��߂܂���<br>' unless $is_rewrite;
	&n_menu;
}


1; # �폜�s��
