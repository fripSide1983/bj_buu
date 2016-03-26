#!/usr/local/bin/perl --
require 'config.cgi';
require "$datadir/contest.cgi";
#================================================
# ��ý� Created by Merino
#================================================
# past �ߋ�, prepare ���ذ��t(���̺�ý�), entry ����ý�

# �a������@�ǉ��폜���בւ��\
my @legends = (
#	['����',		'۸�̧�ٖ�','���'	],
	['���ɂ̔�',	'picture',	'img',	],
	['���̖���',	'book',		'html'	],
);
# �P�ʂɓ��[�����l�ɑ������Ϻ�
my @egg_nos = (1..34,42..50);


#================================================
&decode;
$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @contests;
my $this_dir = "$logdir/contest/$contests[$in{no}][1]";

&header;
&header_contest;

if    ($in{mode} eq 'past')   { &past; }
elsif ($in{mode} eq 'legend') { &legend; }
elsif ($in{mode} eq 'vote' && $in{vote} && $in{id} && $in{pass}) { &vote; &top; }
else { &top; }

&footer;
exit;

#================================================
# ��ýėpheader
#================================================
sub header_contest {
	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index"><input type="submit" value="�s�n�o" class="button1"></form>|;
	}
	
	for my $i (0 .. $#contests) {
		print $in{mode} ne 'legend' && $i eq $in{no} ? qq|$contests[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$contests[$i][0]</a> / |;
	}

	for my $i (0 .. $#legends) {
		print $in{mode} eq 'legend' && $i eq $in{no} ? qq|$legends[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i&mode=legend">$legends[$i][0]</a> / |;
	}
	print qq|<hr>|;
}


#================================================
# �a������
#================================================
sub legend {
	print qq|<h1>$legends[$in{no}][0]</h1><hr>|;
	open my $fh, "< $logdir/legend/$legends[$in{no}][1].cgi" or &error("$logdir/legend/$legends[$in{no}][1].cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($round, $name, $file_title, $file_name, $ldate) = split /<>/, $line;
		print $legends[$in{no}][2] eq 'img'  ? qq|<img src="$logdir/legend/$legends[$in{no}][1]/$file_name" style="border: 5px ridge #FC3; vertical-align:middle;"> ��$round��$contests[$in{no}][0]�D�G��i�w$file_title�x��:$name <font size="1">($ldate)</font><hr>|
			: $legends[$in{no}][2] eq 'html' ? qq|��$round��$contests[$in{no}][0]�D�G��i �w<a href="$logdir/legend/$legends[$in{no}][1]/$file_name" target="_blank">$file_title</a>�x��:$name <font size="1">($ldate)</font><hr>|
			:                                  qq|��$round��$contests[$in{no}][0]�D�G��i �w$file_title�x��:$name <font size="1">($ldate)</font><hr>|
			;
	}
	close $fh;
}


#================================================
# �O��̺�ýČ���
#================================================
sub past {
	print qq|<form method="$method" action="contest.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="no" value="$in{no}">|;
	print qq|<input type="submit" value="���݂̺�ý�" class="button1"></form>|;

	if (-s "$this_dir/past.cgi") {
		open my $fh, "< $this_dir/past.cgi" or &error("$this_dir/past.cgi̧�ق��ǂݍ��߂܂���");
		my $head_line = <$fh>;
		my($etime, $round) = split /<>/, $head_line;
		print qq|<h1>��$round��$contests[$in{no}][0] ����</h1><hr>|;
		while (my $line = <$fh>) {
			my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
			
			print $contests[$in{no}][2] eq 'img'  ? qq|<img src="$this_dir/$round/$file_name" style="vertical-align:middle;"> �w$file_title�x ��:$name �� <b>$vote</b>�[<br>$comment<hr>|
				: $contests[$in{no}][2] eq 'html' ? qq|�w<a href="$this_dir/$round/$file_name" target="_blank">$file_title</a>�x ��:$name �� <b>$vote</b>�[<br>$comment<hr>|
				:                                   qq|�w$file_title�x ��:$name �� <b>$vote</b>�[<br>$comment<hr>|;
				;
		}
		close $fh;
	}
	else {
		print qq|<p>�O��̺�ýĂ͊J�Â���Ă��܂���</p>|;
	}
}


#================================================
# top
#================================================
sub top {
	print qq|<form method="$method" action="contest.cgi">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="mode" value="past"><input type="hidden" name="no" value="$in{no}">|;
	print qq|<input type="submit" value="�O��̌���" class="button1"></form>|;
	
	my $sub_mes = '<hr>';
	open my $fh, "< $this_dir/entry.cgi" or &error("$this_dir/entry.cgi̧�ق��ǂݍ��߂܂���");
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		
		$sub_mes .= qq|<input type="radio" name="vote" value="$no">| if $in{id} && $in{pass};
		$sub_mes .= $contests[$in{no}][2] eq 'img'  ? qq|<img src="$this_dir/$round/$file_name" style="vertical-align:middle;"> No.$no�w$file_title�x<hr>|
				  : $contests[$in{no}][2] eq 'html' ? qq|No.$no�w<a href="$this_dir/$round/$file_name" target="_blank">$file_title</a>�x<hr>|
				  :                                   qq|No.$no�w$file_title�x<hr>|;
				  ;
		++$count;
	}
	close $fh;
	
	my($min,$hour,$day,$month) = (localtime($etime))[1..4];
	++$month;
	
	# �ߋ���ýč폜������ýĂ��ߋ���ýā�����ýĂ�����ýĂɂ��鏈��
	if ($time > $etime) {
		++$round;
		print qq|<h1>��$round��$contests[$in{no}][0]</h1>|;
		print qq|<p>�c�W�v�������c</p>|;

		if ($count > 0) {
			&_send_goods_to_creaters if -s "$this_dir/past.cgi";
			&_result_contest;
		}
		&_start_contest;
	}
	elsif ($min_entry_contest > $count) {
		++$round;
		print qq|<h1>��$round��$contests[$in{no}][0]</h1>|;
		print qq|<p>�y���[�I�����E�����ý� $month��$day��$hour��$min���z</p>|;
		print qq|<p>�o�^�҂��W�܂��Ă��Ȃ����ߊJ�É������ł�</p>|;
	}
	elsif ($in{id} && $in{pass}) {
		print qq|<h1>��$round��$contests[$in{no}][0]</h1>|;
		print qq|<p>�y���[�I�����E�����ý� $month��$day��$hour��$min���z</p>|;
		print qq|<p><font color="#FF9999"><b>$mes</b></font></p>| if $mes;
		print qq|<p>���[�͈�l��[�܂�</p>|;
		print qq|<form method="$method" action="contest.cgi">|;
		print qq|<input type="radio" name="vote" value="0" checked>��߂�$sub_mes|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="hidden" name="mode" value="vote"><input type="hidden" name="no" value="$in{no}">|;
		print qq|����[�S�p30(���p60)�����܂�]:<br><input type="text" name="vote_comment" class="text_box_b"><br>|;
		print qq|<input type="submit" value="���[" class="button_s"></form>|;
	}
	else {
		print qq|<h1>��$round��$contests[$in{no}][0]</h1>|;
		print qq|<p>�y���[�I�����E�����ý� $month��$day��$hour��$min���z</p>|;
		print $sub_mes;
	}
}
# ------------------
# �ߋ��̺�ýč�i����҂ɕԕi��̧�٥̫��ލ폜
sub _send_goods_to_creaters {
	my $count = 0;
	open my $fh, "+< $this_dir/past.cgi" or &error("$this_dir/past.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		++$count;
		next unless -f "$this_dir/$round/$file_name";
		
		my $y_id = unpack 'H*', $name;
		if (-d "$userdir/$y_id/picture") {
			# ��i����҂֕Ԋ�
			rename "$this_dir/$round/$file_name", "$userdir/$y_id/$contests[$in{no}][1]/$file_name" or &error("Cannot rename $this_dir/$round/$file_name to $userdir/$y_id/$contests[$in{no}][1]/$file_name");

			# ��i��������׸ނ����Ă�
			open my $fh5, "> $userdir/$y_id/goods_flag.cgi";
			close $fh5;
		}
		else {
			unlink "$this_dir/$round/$file_name" or &error("$this_dir/$round/$file_namȩ�ق��폜���邱�Ƃ��ł��܂���");
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	close $fh;
	
	opendir my $dh, "$this_dir/$round" or &error("$this_dir/$round�ިڸ�؂��J�����Ƃ��ł��܂���");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		unlink "$this_dir/$round/$file_name" or &error("$this_dir/$round/$file_namȩ�ق��폜���邱�Ƃ��ł��܂���");
	}
	closedir $dh;
	rmdir "$this_dir/$round" or &error("$this_dir/$round�ިڸ�؂��폜���邱�Ƃ��ł��܂���");
}
# ------------------
# ���ʂ��W�v���ĉߋ���ýĂ��Ȱ�
sub _result_contest {
	my @lines = ();
	open my $fh, "+< $this_dir/entry.cgi" or &error("$this_dir/entry.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	
	# ��������sort
	@lines = map { $_->[0] } sort { $b->[5] <=> $a->[5] } map { [$_, split/<>/] } @lines;
	
	unshift @lines, $head_line;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	rename "$this_dir/entry.cgi", "$this_dir/past.cgi" or &error("Cannot rename $this_dir/entry.cgi to $this_dir/past.cgi");
	
	# ��i���߰���ēa������
	&__copy_goods_to_legend($head_line, $lines[1]) if @lines > $min_entry_contest;
	
	&__send_prize(@lines);
}


# ��ʂɏܕi����
sub __send_prize {
	my @lines = @_;

	require 'config_game.cgi'; # regist_you_data()�̂���

	my $head_line = shift @lines;
	my($etime, $round) = split /<>/, $head_line;
	
	my $count = 1;
	for my $line (@lines) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		
		# 1�ʂȂ�̍�
		if ($count eq '1') {
			&regist_you_data($name, 'shogo', $contests[$in{no}][3]);
			
			for my $v_name (split /,/, $vote_names) {
				next unless $v_name;
				my $egg_no = $egg_nos[int(rand(@egg_nos))];
				&send_item($v_name, 2, $egg_no, 0, 0, 1);
			}
			&write_send_news("��$round��$contests[$in{no}][0]��$count�ʂ�$name�ɓ��[�����l���Ϻނ������܂���");
		}
		
		&send_item($name, 2, $c_prizes[$count-1][0], 0, 0, 1);
		&send_money($name, $contests[$in{no}][0], $c_prizes[$count-1][1]);
		&write_send_news("<b>��$round��$contests[$in{no}][0]��$count�ʂ�$name��$c_prizes[$count-1][1] G�� $eggs[ $c_prizes[$count-1][0] ][1]�������܂���</b>", 1, $name);

		last if ++$count > @c_prizes;
	}
}


sub __copy_goods_to_legend {
	my($head_line, $line) = @_;
	my($etime, $round) = split /<>/, $head_line;
	my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
	
	# ���łɓ���̧�ٖ������݂��Ă�����a������͂��Ȃ�
	return if -f "$logdir/legend/$contests[$in{no}][1]/$file_name";
	
	# ��i��a������̫��ނɺ�߰
	open my $in, "< $this_dir/$round/$file_name";
	binmode $in;
	my @datas = <$in>;
	close $in;

	open my $out, "> $logdir/legend/$contests[$in{no}][1]/$file_name";
	binmode $out;
	print $out @datas;
	close $out;
	
	# �a������̧�قɍ�҂�̧�ٖ��ȂǋL��
	my @lines = ();
	open my $fh, "+< $logdir/legend/$contests[$in{no}][1].cgi";
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if (@lines > $max_log - 1) {
			my($dround, $dname, $dfile_title, $dfile_name) = split /<>/, $line;
			unlink "$logdir/legend/$contests[$in{no}][1]/$dfile_name" if -f "$logdir/legend/$contests[$in{no}][1]/$dfile_name";
		}
		else {
			push @lines, $line;
		}
	}
	unshift @lines, "$round<>$name<>$file_title<>$file_name<>$date<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

# ------------------
# ����ýĂ�����ýĂ��Ȱ�
sub _start_contest {
	my $end_time = $time + 24 * 60 * 60 * $contest_cycle_day;

	my @lines = ();
	open my $fh, "+< $this_dir/prepare.cgi" or &error("$this_dir/prepare.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my($etime, $round) = split /<>/, $head_line;
	push @lines, "$end_time<>$round<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	# ���ذ�����Œ���ذ���𒴂����ꍇ�͊J��
	if ( @lines > $min_entry_contest ) {
		rename "$this_dir/prepare.cgi", "$this_dir/entry.cgi" or &error("Cannot rename $this_dir/prepare.cgi to $this_dir/entry.cgi");
		
		# ���[/�����[����̧�ق�������
		open my $fh3, "> $this_dir/vote_name.cgi" or &error("$this_dir/vote_name.cgi̧�ق����܂���");
		print $fh3 ",";
		close $fh3;
		
		# �J�Ð錾
		require 'config_game.cgi'; # write_send_news()�̂���
		my($min,$hour,$day,$month) = (localtime($end_time))[1..4];
		++$month;
		&write_world_news("<i>��$round��$contests[$in{no}][0]���J�Â���܂����I���[���ߐ؂��$month��$day��$hour���܂łł�</i>");

		# ����ýĂ�������
		++$round;
	 	open my $fh2, "> $this_dir/prepare.cgi" or &error("$this_dir/prepare.cgi̧�ق��J���܂���");
		print $fh2 "$end_time<>$round<>\n";
		close $fh2;
		mkdir "$this_dir/$round" or &error("$this_dir/$round�ިڸ�؂����܂���");
	}
	else {
		# ���Ԃ�����
		--$round;
	 	open my $fh2, "> $this_dir/entry.cgi" or &error("$this_dir/entry.cgi̧�ق��J���܂���");
		print $fh2 "$end_time<>$round<>\n";
		close $fh2;
	}
}

#=================================================
# ���[����
#=================================================
sub vote {
	&read_user;
	&error("���Ă̕��������ް�B�S�p30[���p60]�����܂�") if length $in{vote_comment} > 60;

	# ���[�ς݂Ȃ����݁B�����[�Ȃ疼�O��ǉ�
	if (&add_vote_name) {
		$mes .= "���ݍs���Ă��� $contests[$in{no}][0] �ɂ͂��łɓ��[�ς݂ł�<br>";
		return;
	}

	my @lines = ();
	open my $fh, "+< $this_dir/entry.cgi" or &error("$this_dir/entry.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		my($no, $name, $file_title, $file_name, $vote, $comment, $vote_names) = split /<>/, $line;
		
		if ($in{vote} eq $no) {
			++$vote;
			if ($in{vote_comment}) {
				$comment .= qq|<b>$m{name}</b>�$in{vote_comment}�,|;
				$mes .= "$in{vote_comment}�Ƃ������Ă�";
			}
			$mes .= "No.$no $file_title�ɓ��[���܂���<br>";

			$line = "$no<>$name<>$file_title<>$file_name<>$vote<>$comment<>$m{name},$vote_names<>\n";
		}
		
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}
# ------------------
sub add_vote_name {
	open my $fh, "+< $this_dir/vote_name.cgi" or &error("$this_dir/vote_name.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $line = <$fh>;
	$line =~ tr/\x0D\x0A//d;
	if ($line =~ /,\Q$m{name}\E,/) {
		close $fh;
		return 1;
	}
	$line .= "$m{name},";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh $line;
	close $fh;
	return 0;
}

