require "$datadir/contest.cgi";
#================================================
# ��ý� Created by Merino
#================================================

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ������܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '��ýĉ��ɗ��܂���<br>';
		$mes .= qq|<form method="$method" action="contest.cgi">|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="��i������" class="button1"></form>|;
	}
	
	&menu('��߂�', '��i������', '���ذ����');
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# ��i������
#=================================================
sub tp_100 {
	$mes .= qq|<form method="$method" action="contest.cgi">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="��i������" class="button1"></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	&begin;
}

#=================================================
# ���ذ
#=================================================
sub tp_200 {
	$mes .= qq|�ǂ̺�ýĂɴ��ذ���܂���?<br>|;
	$mes .= qq|<li>$non_title�̍�i�������ذ���邱�Ƃ͂ł��܂���<br>|;
	$mes .= qq|<li>���ذ�������ꍇ�A�r���ł�߂邱�Ƃ͂ł��܂���<br>|;
	$mes .= qq|<li><font color="#FF0000">���ذ���ꂽ��i�́A�ߋ��̍�i�W�����I���܂Ŏ茳�ɂ͖߂��Ă��܂���</font><br>|;
	
	&menu('��߂�', map{ $_->[0] }@contests);
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1..$#contests+1);
	$m{value} = $cmd-1;
	
	open my $fh, "< $logdir/contest/$contests[$m{value}][1]/prepare.cgi" or &error("$logdir/contest/$contests[$m{value}][1]/prepare.cgi̧�ق��J���܂���");
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	close $fh;

	$mes .= qq|����A��$round��$contests[$m{value}][0] ���ذ̫��<br>|;
	$mes .= qq|�ǂ̍�i�Ŵ��ذ���܂���?<br>|;
	$mes .= qq|<form method="$method" action="$script"><input type="radio" name="file" value="0" checked>��߂�<hr>|;
	
	opendir my $dh, "$userdir/$id/$contests[$m{value}][1]" or &error("$userdir/$id/$contests[$m{value}][1]�ިڸ�؂��J���܂���");
	while (my $file_name = readdir $dh) {
		next unless $file_name =~ /^_/;
		
		my $file_title = &get_goods_title($file_name);
		$mes .= qq|<input type="radio" name="file" value="$file_name">|;
		$mes .= $contests[$m{value}][2] eq 'img'  ? qq|$file_title <img src="$userdir/$id/$contests[$m{value}][1]/$file_name" style="vertical-align:middle;"><hr>|
			  : $contests[$m{value}][2] eq 'html' ? qq|<a href="$userdir/$id/$contests[$m{value}][1]/$file_name" target="_blank">$file_title</a><br>|
			  :                                     qq|$file_title<br>|;
			  ;
	}
	close $dh;
	
	$mes .= qq|����[�S�p30(���p60)�����܂�]<br><input type="text" name="title" class="text_box_b"><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="���ذ" class="button1"></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_220 {
	unless ($in{file}) {
		$mes .= "��߂܂���<br>";
		&begin;
		return;
	}
	&error("���ق��L�����Ă�������") unless $in{title};
	&error("���ق���ص��(.)�͎g���܂���") if $in{title} =~ /\./;
	&error("���ق̕��������ް�B�S�p30(���p60)�����܂łł�") if length $in{title} > 60;
	&error("�I��������i�����݂��܂���") unless -f "$userdir/$id/$contests[$m{value}][1]/$in{file}";
	&error("����ýĂɴ��ذ���Ă��邽�ߴ��ذ���邱�Ƃ͂ł��܂���") if !$is_renzoku_entry_contest && &is_entry_contest;
	
	my $count = 0;
	my @lines = ();
	open my $fh, "+< $logdir/contest/$contests[$m{value}][1]/prepare.cgi" or &error("$logdir/contest/$contests[$m{value}][1]/prepare.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		&error("��$round��$contests[$m{value}][0]�ɂ͂��łɴ��ذ�ς݂ł�") if $name eq $m{name};
		++$count;
		push @lines, $line;
	}
	&error("�c�O�Ȃ���������ߐ؂�܂����B����ȏ���ذ���邱�Ƃ͂ł��܂���") if $count >= $max_entry_contest;
	++$count;
	rename "$userdir/$id/$contests[$m{value}][1]/$in{file}", "$logdir/contest/$contests[$m{value}][1]/$round/_${count}_$in{file}" or &error("���ذ�Ɏ��s���܂���");
	push @lines, "$count<>$m{name}<>$in{title}<>_${count}_$in{file}<>0<><><>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= "��$round��$contests[$m{value}][0]�ɁyNo.$count $in{title}�z�Ŵ��ذ���܂���<br>";
	
	&begin;
}

# ------------------
sub is_entry_contest {
	open my $fh, "< $logdir/contest/$contests[$m{value}][1]/entry.cgi" or &error("$logdir/contest/$contests[$m{value}][1]/entry.cgi̧�ق��ǂݍ��߂܂���");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		return 1 if $name eq $m{name};
	}
	close $fh;
	return 0;
}




1; # �폜�s��
