my $this_file = "$logdir/$m{country}/review.cgi";
#=================================================
# ��\���[ Created by Merino
#=================================================

# ��ƂɕK�v�ȕ[
my $need_point = int($cs{member}[$m{country}] * 0.1)+2;

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '���ɑ����ĂȂ��ƍs�����Ƃ��ł��܂���<br>';
		&refresh;
		&n_menu;
		return 0;
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
		$mes .= "$c_m�̑�\\���Ƃ��܂�<br>";
		$mes .= "��ƂɂȂ�ɂ�$need_point�[�K�v�ł�<br>";
	}
	&menu('��߂�', '��Ɠ��[����');
}

sub tp_1 {
	return if &is_ng_cmd(1);
	
	$m{tp} = $cmd * 100;
	&{'tp_' . $m{tp} };
}

#=================================================
# �x���E�s�x���̑I��
#=================================================
sub tp_100 {
	my $dfind = 0;
	for my $k (qw/war dom pro mil/) {
		$dfind = 1 if $cs{$k}[$m{country}] ne '';
	}
	unless($dfind) {
		$mes .= '��ƌ��҂����܂���<br>';
		&begin;
		return;
	}
	
	if (!-f $this_file) {
		open my $fh, "> $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
		for my $k (qw/war dom pro mil/) {
			print $fh "$cs{$k}[$m{country}]<>dummy<>\n";
		}
		close $fh;
	}
	my $sub_mes = '';
	my $is_find = 0;
	open my $fh, "< $this_file" or &error('�����[�_�[�t�@�C�����ǂݍ��߂܂���');
	for my $k (qw/war dom pro mil/) {
		my $line = <$fh>;
		next if($cs{$k}[$m{country}] eq '');
		my($name, $vote) = split /<>/, $line;
		my @votes = split /,/, $vote;
		if($cs{$k}[$m{country}] ne $name){
			@votes = ();
		}
		my $vote_num = @votes;
		$sub_mes .= qq|<input type="radio" name="vote" value="$k">$cs{$k}[$m{country}]�F$vote_num�[<br>|;
	}
	close $fh;
	
	$mes .= '�N���Ƃ��܂���?<br>';
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="vote" value="">��߂�<hr>|;
	$mes .= qq|$sub_mes|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�� ��" class="button1"></form>|;
	$m{tp} += 10;
}
sub tp_110 {
	unless($in{vote}) {
		&begin;
		return;
	}
	
	my $review_name = '';
	my @lines = ();
	open my $fh, "+< $this_file" or &error('�����[�_�[�t�@�C�����J���܂���');
	eval { flock $fh, 2 };
	for my $k (qw/war dom pro mil/) {
		my $line = <$fh>;
		my($name, $vote) = split /<>/, $line;
		if($k eq $in{vote}){
			$review_name = $cs{$k}[$m{country}];
			if($cs{$k}[$m{country}] ne $name){
				$vote = "$m{name}";
				$name = $cs{$k}[$m{country}];
			}else{
				my @votes = split /,/, $vote;
				my $vote_num = @votes;
				my $vfind = 0;
				for my $vname (@votes){
					$vfind = 1 if($vname eq $m{name});
				}
				unless($vfind){
					$vote .= ",$m{name}";
					$vote_num++;
					if($vote_num >= $need_point){
						$c = $k . '_c';
						my $v_id = unpack 'H*', $name;
						my %datas = &get_you_datas($v_id, 1);
						&regist_you_data($name,$c,int($datas{$c} * 0.75));
						&write_world_news("<b>$name��$c_m�̑�\\���ƂɂȂ�܂���</b>", 1, $name);
						$cs{$k}[$m{country}] = '';
						$cs{$c}[$m{country}] = 0;
						$name = '';
						$vote = '';
						&write_cs;
					}
				}
			}
		}
		push @lines, "$name<>$vote<>\n"; # 0�[�͏�����
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= $review_name ? "$review_name���Ɠ��[���܂�<br>" : '��߂܂���<br>';
	
	&begin;
}

1; # �폜�s��
