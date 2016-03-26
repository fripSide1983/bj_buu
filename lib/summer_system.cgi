require './lib/jcode.pl';
#================================================
# ﾒｲﾝでよく使う処理
#================================================
sub read_summer { # Get %s
	$mid   = $in{id} || unpack 'H*', $in{login_name};
	%s = ();
	
	unless (-f "$userdir/$mid/summer.cgi") {
		open my $fh, "> $userdir/$mid/summer.cgi";
		close $fh;
	}
	open my $fh, "< $userdir/$mid/summer.cgi" or &error("そのような名前$in{login_name}のﾌﾟﾚｲﾔｰが存在しません");
	my $line = <$fh>;
	close $fh;
	
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$s{$k} = $v;
	}
	$s{dummy} = 1;
}
1; # 削除不可
