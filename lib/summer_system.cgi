require './lib/jcode.pl';
#================================================
# Ҳ݂ł悭�g������
#================================================
sub read_summer { # Get %s
	$mid   = $in{id} || unpack 'H*', $in{login_name};
	%s = ();
	
	unless (-f "$userdir/$mid/summer.cgi") {
		open my $fh, "> $userdir/$mid/summer.cgi";
		close $fh;
	}
	open my $fh, "< $userdir/$mid/summer.cgi" or &error("���̂悤�Ȗ��O$in{login_name}����ڲ԰�����݂��܂���");
	my $line = <$fh>;
	close $fh;
	
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$s{$k} = $v;
	}
	$s{dummy} = 1;
}
1; # �폜�s��
