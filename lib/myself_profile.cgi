require "$datadir/profile.cgi";
#================================================
# ���̨�ِݒ� Created by Merino
#================================================

#================================================
sub begin {
	$layout = 2;

	my %datas = ();
	open my $fh, "< $userdir/$id/profile.cgi" or &error("$userdir/$id/profile.cgi̧�ق��J���܂���");
	my $line = <$fh>;
	close $fh;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$datas{$k} = $v;
	}

	$mes .= qq|$m{name}�����̨�فF�S�p80����(���p160)�܂�<br>|;
	$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="mode" value="write">|;
	for my $profile (@profiles) {
		$mes .= qq|<hr>$profile->[1]<br><input type="text" name="$profile->[0]" value="$datas{$profile->[0]}" class="text_box_b"><br>|; 
	}
	if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
		my $boch_pet = $m{sex} eq '1' ? '�]����' : 'Ͻ��ķ��';
		$mes .= qq|<hr>$boch_pet<br><input type="text" name="boch_pet" value="$m{boch_pet}" class="text_box_b"><br>|; 
	}
	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		$mes .= &regist_mes(0);
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����" class="button1"></p></form>|;
	&n_menu;
}

sub tp_1 {
	if ($in{mode} eq 'write') {
		my %datas = ();
		open my $fh, "+< $userdir/$id/profile.cgi" or &error("$userdir/$id/profile.cgi̧�ق��J���܂���");
		eval { flock $fh, 2; };
		my $line = <$fh>;
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$datas{$k} = $v;
		}
		
		my $is_rewrite = 0;
		for my $profile (@profiles) {
			unless ($in{$profile->[0]} eq $datas{$profile->[0]}) {
				&error("$profile->[1] �ɕs���ȕ���( ,\'\"\;<> )���܂܂�Ă��܂�")	if $in{$profile->[0]} =~ /[;<>]/;
				&error("$profile->[1] �͑S�p80(���p160)�����ȓ��ł�")		if length($in{$profile->[0]}) > 160;
				$datas{$profile->[0]} = $in{$profile->[0]};
				$is_rewrite = 1;
			}
		}
		if ($is_rewrite) {
			my $new_line = '';
			while ( my($k, $v) = each %datas ) {
				$new_line .= "$k;$v<>";
			}
			
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh $new_line;
			close $fh;
			
			$mes .= '���̨�ق�ύX���܂���<br>';
			&n_menu;
		}
		else {
			close $fh;
			$mes .= '��߂܂���<br>';
		}
		if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
			unless ($in{boch_pet} eq $m{boch_pet}){
				&error("�߯Ė��͑S�p10(���p20)�����ȓ��ł�") if length($in{boch_pet}) > 20;
			}
			$m{boch_pet} = $in{boch_pet};
			$mes .= $m{sex} eq '1' ? '�]���łɖ��O��t���܂���<br>':'Ͻ��ķ�ׂɖ��O��t���܂���<br>';
		}
		if ($w{world} eq $#world_states-4) {
			if ($in{voice}) {
				require './lib/fate.cgi';
				if (&regist_attack($in{trigger}, $in{timing}, $in{demerit}, $in{max_count}, $in{effect}, $in{voice}, $in{random})) {
					$mes .= '�K�E�Z��ݒ肵�܂����B';
				}
			}
		}
	}
	else {
		$mes .= '��߂܂���<br>';
	}

	&refresh;
	&n_menu;
}


1; # �폜�s��
