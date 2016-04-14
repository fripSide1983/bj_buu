#!/usr/local/bin/perl --
require './config.cgi';
require './config_game.cgi';
require './lib/_bbs_chat.cgi';
require "$datadir/profile.cgi";
#================================================
# ���L Created by Merino
#================================================

# �A���������݋֎~����(�b)
$bad_time    = 60;

# �ő�۸ޕۑ�����
$max_log     = 30;

# �ő���Đ�(���p)
$max_comment = 3000;

# ���l�̓��L�ɺ��Ă�����@�\(0:�g��Ȃ�,1:�g��)
$is_comment = 1;


#================================================

&decode;
$this_file = "$userdir/$in{id}/blog"; # _bbs_chat.cgi���g������.cgi��������_��

&header;
if ($in{id} && $in{pass}) {
	if ($in{mode} eq 'comment_exe') { &header_profile; &comment_exe; } # ���Ēǉ�����
	else                            { &myself_blog; } # �����p
}
elsif ($in{mode} eq 'comment_form') { &header_profile; &comment_form; } # ���Ēǉ�̫��
elsif (-s "$this_file.cgi")         { &header_profile; &view_blog; } # ���l�p
else                                { &header_profile; } # �L��/��ڲ԰�����݂��Ȃ�
&footer;
exit;

#================================================
# �����̓��L������
#================================================
sub myself_blog {
	&read_user;
	
	if ($in{mode} eq 'delete_kiji') {
		&delete_kiji;
	}
	elsif ($in{mode} eq "write" && $in{comment}) {
		&read_cs;
		&error('�薼���������܂�') if length $in{title} > 60;

		$in{title} ||= $non_title;
		$addr = $in{title}; # ���ق��������̂ŁAaddr�����ق�����

		my $name = $m{name};
		$name .= "[$m{shogo}]" if $m{shogo};
		$in{comment} .= qq|<hr><font color="$cs{color}[$m{country}]">$cs{name}[$m{country}]</font> $name|;

		my $icon_temp = $m{icon};
		$m{icon} = $in{is_secret} || 0; # ���J/����J�׸ނ�icon
		my $is_ok = &write_comment;
		
		&write_blog_news(qq|�w$in{title}�x<a href="blog.cgi?id=$in{id}&country=$m{country}&title=Blog">$m{name}�̓��L</a>|) if $is_ok && !$in{is_secret};
		
		if (&on_summer && &time_to_date($time) ne &time_to_date($m{blog_time})) {
			$m{blog_time} = $time;
			$m{summer_blog}++;
			$m{icon} = $icon_temp;
			&write_user;
		}
	}
	
	require "$datadir/header_myroom.cgi";
	&header_myroom;
	
	print qq|$delete_message| if $delete_message;
	print qq|<ul><li>$max_log���܂ŕۑ�(�Â����̂��玩���폜)</ul>|;

	my $rows = $is_mobile ? 2 : 14;
	print qq|<form method="$method" action="blog.cgi"><input type="hidden" name="mode" value="write"><input type="hidden" name="no" value="$in{no}">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|�薼[�S�p30(���p60)�����܂�]�F<input type="text" name="title" class="text_box_b"><br>|;
	print qq|<textarea name="comment" cols="80" rows="$rows" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="���L������" class="button_s"><input type="hidden" name="no" value="1">|;
	print qq|�@ <input type="checkbox" name="is_secret" value="1">���̋L�������J�ɂ���</form>|;

	print qq|<form method="$method" action="blog.cgi"><input type="hidden" name="mode" value="delete_kiji"><input type="hidden" name="no" value="$in{no}">|;

	my $count = 0;
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		my $secret_mark = $bicon ? '�y��z' : '';
		$bname .= "[$bshogo]" if $bshogo;

		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;

		if ($is_mobile) {
			print qq|<br><input type="checkbox" name="delete" value="$btime"> $bdate|;
			print qq|<hr>$baddr $secret_mark|;
			print qq|<hr>$bcomment<br>|;
			print qq|<hr>����<br>@bcomments| if $is_comment && @bcomments;
			print qq|<hr><br>|;
		}
		else {
			print qq|<table class="table1" cellpadding="5" width="440">|;
			print qq|<tr><th align="left"><input type="checkbox" name="delete" value="$btime"> $baddr <font size="1">($bdate)</font> $secret_mark<br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr>|;
			print qq|<tr><td>����<br>@bcomments</td></tr>| if $is_comment && @bcomments;
			print qq|</table><br>|;
		}
		++$count;
	}
	close $fh;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<p><input type="submit" value="�폜" class="button_s"> ($count/$max_log)</p></form>|;
}

#================================================
# ���l�̓��L������
#================================================
sub view_blog {
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		next if $bicon;
		$bname .= "[$bshogo]" if $bshogo;
		# �s���͑����邪�O�����Z�q�͏d���C���[�W������̂ŕ���
#		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		if ($is_mobile) {
			$bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g;
#			print qq|<br>$bdate|;
#			print qq|<hr>$baddr|;
#			print qq|<hr>$bcomment<br>|;
#			print qq|<hr><a href="?id=$in{id}&country=$in{country}&kiji=$btime&mode=comment_form">���Ă�����</a><br>@bcomments| if $is_comment;
#			print qq|<hr><br>|;
			print qq|$bdate <a href="?id=$in{id}&country=$in{country}&kiji=$btime&mode=comment_form">$baddr</a><hr>|;
		}
		else {
			$bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
			print qq|<table class="table1" cellpadding="5" width="440">|;
			print qq|<tr><th align="left">$baddr <font size="1">($bdate)</font><br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr>|;
			print qq|<tr><td><a href="?id=$in{id}&country=$in{country}&kiji=$btime&mode=comment_form">���Ă�����</a><br>@bcomments</td></tr>| if $is_comment;
			print qq|</table><br>|;
		}
	}
	close $fh;
}


#================================================
# ���ď�������̫��
#================================================
sub comment_form {
	return unless $is_comment;
	my($cook_name, $cook_pass) = &get_cookie;

	my $cline = '';
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		next if $bicon;
		if ($in{kiji} eq $btime) {
			$cline = $line;
			last;
		}
	}
	close $fh;

	if ($cline) {
		print '�ȉ��̋L���ɺ��Ă��܂�<hr>';
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $cline;
		$bname .= "[$bshogo]" if $bshogo;
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		if ($is_mobile) {
			print qq|<br>$bdate|;
			print qq|<hr>$baddr|;
			print qq|<hr>$bcomment<br>|;
			print qq|<hr>����<br>@bcomments| if @bcomments;
			print qq|<hr><br>|;
		}
		else {
			print qq|<table class="table1" cellpadding="5" width="440">|;
			print qq|<tr><th align="left">$baddr <font size="1">($bdate)</font><br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr>|;
			print qq|<tr><td>����<br>@bcomments</td></tr>| if @bcomments;
			print qq|</table><br>|;
		}
	
		print qq|<form method="$method" action="blog.cgi">|;
		print qq|<input type="hidden" name="mode" value="comment_exe"><input type="hidden" name="id" value="$in{id}">|;
		print qq|<input type="hidden" name="country" value="$in{country}"><input type="hidden" name="kiji" value="$in{kiji}">|;
		print qq|<table class="table1"><tr><th><tt>��ڲ԰��:</tt></th><td><input type="text" name="name" value="$cook_name" class="text_box1"><br></td></tr>|;
		print qq|<tr><th><tt>�߽ܰ��:</tt></th><td><input type="password" name="pass" value="$cook_pass" class="text_box1"><br></td></tr></table>|;
		print qq|�S�p300(���p600)�����܂ŁF<br><textarea name="comment" cols="60" rows="4" class="textarea1"></textarea><br>|;
		print qq|<input type="submit" value="��������" class="button_s"></form>|;
	}
	else {
		print '�Y���L����������܂���<br>';
	}
}

#================================================
# ���ď������ݏ���
#================================================
sub comment_exe {
	return unless $is_comment;
	if ($in{name} eq '' || $in{pass} eq '' || $in{comment} eq '' || $in{comment} =~ /^(<br>|\s|�@)+$/) {
		print "��߂܂���<br>";
		return;
	}
	&error("���������ް�S�p300(���p600)�����܂łł�") if length $in{comment} > 600;
	
	my $blog_uid = $in{id};
	my $send_name = pack 'H*', $in{id};
	$in{id} = unpack 'H*', $in{name};
	&read_user;
	# �����������݂��邩�̃`�F�b�N��ɓǂ�ł��u���OID��߂��Ȃ��ƁA
	# �R�����g���e����ɕ\�������u���O�́u���Ă������v�悪�����̓��L�ɂȂ��Ă��܂�
	$in{id} = $blog_uid;

	if (-f "$userdir/$blog_uid/blacklist.cgi") {
		open my $fh, "< $userdir/$blog_uid/blacklist.cgi" or &error("$userdir/$blog_uid/blacklist.cgi̧�ق��J���܂���");
		while (my $line = <$fh>) {
			my($blackname) = split /<>/, $line;
			if ($blackname eq $m{name}) {
				&error('������');
			}
		}
		close $fh;
	}

	my $is_rewrite = 0;
	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		
		if (!$bicon && $in{kiji} eq $btime) {
			$is_rewrite = 1;
			push @bcomments, qq|<><b>$m{name}</b>�w$in{comment}�x<font size="1">($date)</font><br>|;
			$line = "$btime<>$bdate<>$bname<>$bcountry<>$bshogo<>$baddr<>$bcomment<>$bicon<>@bcomments<>";
			
			unless ($send_name eq $m{name}) {
				# ���Ď莆�𑗂� 
				$in{comment} .= "<hr>�y���L$baddr�ւ̺��āz";
				&send_letter($send_name);
			}
		}
		push @lines, "$line\n";
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		print "���Ă��������݂܂���<br>";
		&view_blog;
	}
	else {
		close $fh;
		print "�Y���L����������܂���<br>";
	}
}


#================================================
# �����̓��L�̋L���폜
#================================================
sub delete_kiji {
	return if @delfiles <= 0; 
	
	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi̧�ق��ǂݍ��߂܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		
		my $is_delete = 0;
		for my $i (0 .. $#delfiles) {
			if ($delfiles[$i] eq $btime) {
				$is_delete = 1;
				$delete_message .= "$bdate $baddr�̋L�����폜���܂���<br>";
				splice(@delfiles, $i, 1);
				last;
			}
		}
		
		next if $is_delete;
		push @lines, "$line\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


