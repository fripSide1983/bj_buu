require 'lib/_write_tag.cgi';
#=================================================
# BBS,CHAT�⏕���ٰ�� Created by Merino
#=================================================

#=================================================
# �������ݏ���
#=================================================
sub write_comment {
	&error('�{���ɉ���������Ă��܂���') if $in{comment} eq '';
	&error("�{�����������܂�(���p$max_comment�����܂�)") if length $in{comment} > $max_comment;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	
	my $mname;
	($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 0);
	
	my $head_line = <$fh>;
	my ($htime,$hname,$hcomment) = (split /<>/, $head_line)[0,2,6];
	my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
	return 0 if $in{comment} eq $hcomment;
	if ($hname eq $m{name} && $htime + $bad_time > $time) {
		&error("�A�����e�͋֎~���Ă��܂��B<br>���΂炭�҂��Ă��珑������ł�������");
	}
	push @lines, $head_line;

	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	if($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')){
		$mname = "������";
	}
	my $mshogo = length($m{shogo}) > 16 ? substr($m{shogo}, 0, 16) : $m{shogo};
	unshift @lines, "$time<>$date<>$mname<>$m{country}<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}


#=================================================
# ���ް�擾
#=================================================
sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # �����l�Ȃ玟
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, $line;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members;

	return ($member_c, $member);
}

1; # �폜�s��
