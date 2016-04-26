my %action_weight = (
    dom => 0.8,
    pro  => 1.0,
    mil  => 1.0,
    war  => 1.1
);

#================================================
# �s�����O�̏�������
# �S�����S�������Ȃ荑�ʂ̍s�����O�ɏ������ނƃ��o�����Ȃ̂ł܂��͌l�t�@�C���ɗ��߂Ă���
#================================================
sub write_action_log {
	return 0 unless $w{year} =~ /[1-5]$/;
	my ($action_type, $wait_time) = @_;
	my $key = $action_type."_".$wait_time;
	my %action_log = ($key => 1);
	my $nline = "";
	my $fh;

	if (-e "$userdir/$id/action_log.cgi") {
		open $fh, "+< $userdir/$id/action_log.cgi" or &error("action_log.cgi���J���܂���");
		my $line = <$fh>;
		$line =~ tr/\x0D\x0A//d;
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$action_log{$k} += $v;
		}
		for my $k (keys(%action_log)) {
			$nline .= "$k;$action_log{$k}<>";
		}

		seek $fh, 0, 0;
		truncate $fh, 0;
	}
	else {
		open $fh, "> $userdir/$id/action_log.cgi" or &error("action_log.cgi���J���܂���");
		$nline = "$key;1<>";
	}

	print $fh "$nline";
	close $fh;
}

#================================================
# �v���C���[���O�C�����ɍs�����O�����ʂ̍s�����O�֌v�シ��
# �t�@�C������悭������񂵉���̂��|������Ȃ�ƂȂ��ǂ�œǂ�ŏ����ď�����
#================================================
sub add_action_log_country {
	return 0 unless $w{year} =~ /[1-6]$/;
	return 0 unless -e "$userdir/$id/action_log.cgi";
	my %action_log = ();
	my $line = "";
	my $nline = "";
	my $fh1;
	my $fh2;

	open $fh2, "< $userdir/$id/action_log.cgi" or &error("action_log.cgi���J���܂���");
	$line = <$fh2>;
	$line =~ tr/\x0D\x0A//d;
	unless ($line) {
		close $fh2;
		return 0;
	}
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$action_log{$k} = $v;
	}
	close $fh2;

	open $fh1, "< $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgi���J���܂���");
	$line = <$fh1>;
	$line =~ tr/\x0D\x0A//d;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$action_log{$k} += $v;
	}
	close $fh1;

	for my $k (keys(%action_log)) {
		$nline .= "$k;$action_log{$k}<>";
	}

	open $fh1, "> $logdir/action_log_country_$m{country}.cgi" or &error("action_log_country.cgi���J���܂���");
	eval { flock $fh1, 2; };
	print $fh1 "$nline";
	close $fh1;

	open $fh2, "> $userdir/$id/action_log.cgi" or &error("action_log.cgi���J���܂���");
	print $fh2 "";
	close $fh2;
}

1;