require './lib/jcode.pl';
#================================================
# Ҳ݂ł悭�g������
#================================================
sub read_summer { # Get %s
	return unless &on_summer;
	$mid   = $in{id} || unpack 'H*', $in{login_name};
	# ???
	# %s �� summer.cgi �ɏ������ޏ������ǂ��ɂ��Ȃ���ɋ���ۂ��ǂݍ��܂��
	# system_game.cgi �� write_user �� write_summer �I�ȏ�����ǉ�����
	# %s��%m�Ƃŏd������\���͂��邪�A�������� $s{hoge} ���Q�Ƃ��Ă��Ȃ��̂� $m{hoge} �ɓ���
#	%s = ();
	
	unless (-f "$userdir/$mid/summer.cgi") {
		open my $fh, "> $userdir/$mid/summer.cgi";
		close $fh;
	}
	open my $fh, "< $userdir/$mid/summer.cgi" or &error("���̂悤�Ȗ��O$in{login_name}����ڲ԰�����݂��܂���");
	my $line = <$fh>;
	close $fh;

	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$m{$k} = $v; # $s
	}
	$m{dummy} = 0; # $s
}
1; # �폜�s��
