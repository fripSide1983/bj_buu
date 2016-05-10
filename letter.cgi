#!/usr/local/bin/perl --
require './config.cgi';
require "$datadir/header_myroom.cgi";
#================================================
# �莆 Created by Merino
#================================================
&get_data;
&header_myroom;
&delete_kiji if $in{mode} eq 'delete_kiji';
if ($in{type} eq 'send') { &letter_box_send; }
else { &letter_box_get; }
&footer;
exit;

#================================================
sub letter_box_get {
	if (-f "$userdir/$id/letter_flag.cgi") {
		unlink "$userdir/$id/letter_flag.cgi";
	}

	if ($in{mode} eq "write" && $in{comment}) {
	    my $rflag = 0;
	    open my $rfh, "+< $logdir/refuse_list.cgi" or &error("$logdir/refuse_list.cgi̧�ق��ǂݍ��߂܂���");
	    while (my $line = <$rfh>) {
		$line =~ tr/\x0D\x0A//d;
		$rflag++ if $line eq $m{name}
	    }
	    close $fh;

		&send_letter($in{name}, $in{is_save_log}) if $in{name} ne $admin_name || $rflag == 0;
		print qq|<p>$in{name} �Ɏ莆�𑗂�܂���</p>|;
	}

	if ($in{mode} eq "refuse") {
		&add_refuse;
	}

	my $rows = $is_mobile ? 2 : 8;
	if($in{type} eq 'country'){
		print qq|<p>��M��(<a href="?id=$id&pass=$pass&no=$in{no}&type=get">���ׂ�</a> / �ꊇ���M / <a href="?id=$id&pass=$pass&no=$in{no}&type=ncountry">�l��</a>) / <a href="?id=$id&pass=$pass&no=$in{no}&type=send">���M��</a> / <a href="?id=$id&pass=$pass&no=$in{no}&type=new_year">�N���</a></p>|;
	}elsif($in{type} eq 'ncountry'){
		print qq|<p>��M��(<a href="?id=$id&pass=$pass&no=$in{no}&type=get">���ׂ�</a> / <a href="?id=$id&pass=$pass&no=$in{no}&type=country">�ꊇ���M</a> / �l��) / <a href="?id=$id&pass=$pass&no=$in{no}&type=send">���M��</a> / <a href="?id=$id&pass=$pass&no=$in{no}&type=new_year">�N���</a></p>|;
	}elsif($in{type} eq 'new_year'){
		print qq|<p>��M��(<a href="?id=$id&pass=$pass&no=$in{no}&type=get">���ׂ�</a> / <a href="?id=$id&pass=$pass&no=$in{no}&type=country">�ꊇ���M</a> / <a href="?id=$id&pass=$pass&no=$in{no}&type=ncountry">�l��</a>) / <a href="?id=$id&pass=$pass&no=$in{no}&type=send">���M��</a> / �N���</p>|;
	}else{
		print qq|<p>��M��(���ׂ� / <a href="?id=$id&pass=$pass&no=$in{no}&type=country">�ꊇ���M</a> / <a href="?id=$id&pass=$pass&no=$in{no}&type=ncountry">�l��</a>) / <a href="?id=$id&pass=$pass&no=$in{no}&type=send">���M��</a> / <a href="?id=$id&pass=$pass&no=$in{no}&type=new_year">�N���</a></p>|;
	}
	
	if ($in{type} eq 'new_year' && -f "$userdir/$id/greeting_card.cgi") {
		my $pic_size = q|width="25px" height="25px"|;
		my $count = 0;
		open my $fh, "< $userdir/$id/greeting_card.cgi" or &error("$userdir/$id/greeting_card.cgi̧�ق��J���܂���");
		while (my $line = <$fh>) {
			my($from_name, $from_id, $number) = split /<>/, $line;
			if ($is_mobile) {
				print qq|From $from_name<br>|;
				if ($number % 3 == 0) {
					print qq|��(��^o^)����������|;
				} elsif ($number % 3 == 1) {
					print qq|<img src="$icondir/kappa.png" style="vertical-align:middle;" $pic_size>���މ�V�N|;
				} else {
					print qq|<img src="$icondir/chikuwa.jpeg" style="vertical-align:middle;" $pic_size>|;
				}
				print qq|<br>���N�ʕt���N��󒊑I�ԍ� $number<br><hr><br>|;
			}
			else {
#				print qq|<table class="table1" cellpadding="5" width="440"><tr><th align="left">|;
				print qq|<table class="table1" cellpadding="5"><tr><th align="left">|;
				print qq|From $from_name</th></tr>|;
				print qq|<tr><td>|;
				if ($number % 3 == 0) {
					print qq|��(��^o^)����������|;
				} elsif ($number % 3 == 1) {
					print qq|<img src="$icondir/kappa.png" style="vertical-align:middle;" $pic_size>���މ�V�N|;
				} else {
					print qq|<img src="$icondir/chikuwa.jpeg" style="vertical-align:middle;" $pic_size>|;
				}
				print qq|<hr>���N�ʕt���N��󒊑I�ԍ� $number|;
				print qq|</td></tr></table><br>|;
			}
		}
		close $fh;
		return;
	}
	
	print qq|<form method="$method" action="letter.cgi"><input type="hidden" name="mode" value="delete_all">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="no" value="$in{no}"><input type="hidden" name="type" value="$in{type}">|;
	print qq|<p><input type="submit" value="�S�`�F�b�N" class="button_s"></p></form>|;
	
	print qq|<form method="$method" action="letter.cgi">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="mode" value="write"><input type="hidden" name="no" value="$in{no}">|;
	print qq|����於 <input type="text" name="name" class="text_box1" value="$in{send_name}"><br>|;
	print qq|<textarea name="comment" cols="60" rows="$rows" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="�莆�𑗂�" class="button_s">|;
	print qq|�@ <input type="checkbox" name="is_save_log" value="1" checked>���M���ɕۑ�</form><br>|;

	print qq|<form method="$method" action="letter.cgi"><input type="hidden" name="mode" value="delete_kiji">|;
	my $count = 0;
	open my $fh, "< $userdir/$id/letter.cgi" or &error("$userdir/$id/letter.cgi̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		next if($bcomment =~ /�S���ɑ��M�z/ && $in{type} eq 'ncountry');
		next if($bcomment !~ /�S���ɑ��M�z/ && $in{type} eq 'country');
		$bshogo = $bshogo ? "[$bshogo]" : '';
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		if ($is_mobile) {
			if($in{mode} eq 'delete_all'){
				print qq|<hr><input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<hr><input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|From <font color="$cs{color}[$bcountry]">$cs{name}[$bcountry]</font><a href="letter.cgi?id=$id&pass=$pass&no=$in{no}&send_name=$bname">$bname</a>[$bshogo] <font size="1">($bdate)</font><hr>|;
			print qq|$bcomment<br><hr><br>|;
		}
		else {
			$bshogo = "" if $is_smart;
#			print qq|<table class="table1" cellpadding="5" width="440"><tr><th align="left">|;
			print qq|<table class="table1" cellpadding="5"><tr><th align="left">|;
			if($in{mode} eq 'delete_all'){
				print qq|<input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|From <font color="$cs{color}[$bcountry]">$cs{name}[$bcountry]</font> <a href="letter.cgi?id=$id&pass=$pass&no=$in{no}&send_name=$bname">$bname</a>$bshogo <font size="1">($bdate)</font><br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr></table><br>|;
		}
		++$count;
	}
	close $fh;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="no" value="$in{no}"><input type="hidden" name="type" value="$in{type}">|;
	print qq|<p><input type="submit" value="�폜" class="button_s"> ($count/$max_log)</p></form>|;
	if($m{name} eq $admin_name){
	    print qq|<form method="$method" action="letter.cgi">|;
	    print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	    print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="no" value="$in{no}">|;
	    print qq|�� <input type="text" name="rname" class="text_box1" value="$in{send_name}"><br>|;
	    print qq|<input type="submit" value="refuse" class="button_s"></form>|;
	    print qq|refuse list<br>|;
	    open my $rfh, "< $logdir/refuse_list.cgi" or &error("$logdir/$id/letter.cgi̧�ق��J���܂���");
	    while (my $line = <$rfh>) {
		print qq|$line<br>|;
	    }
	    close $rfh;
	}
}

sub letter_box_send {
	print qq|<p>��M��(<a href="?id=$id&pass=$pass&type=get">���ׂ�</a> / <a href="?id=$id&pass=$pass&no=$in{no}&type=country">�ꊇ���M</a> / <a href="?id=$id&pass=$pass&no=$in{no}&type=ncountry">�l��</a>) / ���M��</p>|;

	print qq|<form method="$method" action="letter.cgi"><input type="hidden" name="mode" value="delete_all">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="no" value="$in{no}"><input type="hidden" name="type" value="$in{type}">|;
	print qq|<p><input type="submit" value="�S�`�F�b�N" class="button_s"></p></form>|;
	
	print qq|<form method="$method" action="letter.cgi"><input type="hidden" name="mode" value="delete_kiji">|;
	my $count = 0;
	open my $fh, "< $userdir/$id/letter_log.cgi" or &error("$userdir/$id/letter_log.cgi̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		if ($is_mobile) {
			if($in{mode} eq 'delete_all'){
				print qq|<hr><input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<hr><input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|To $bname <font size="1">($bdate)</font><hr>|;
			print qq|$bcomment<br><hr><br>|;
		}
		else {
#			print qq|<table class="table1" cellpadding="5" width="440"><tr><th align="left">|;
			print qq|<table class="table1" cellpadding="5"><tr><th align="left">|;
			if($in{mode} eq 'delete_all'){
				print qq|<input type="checkbox" name="delete" value="$btime" checked>|;
			}else{
				print qq|<input type="checkbox" name="delete" value="$btime">|;
			}
			print qq|To $bname <font size="1">($bdate)</font><br></th></tr>|;
			print qq|<tr><td>$bcomment<br></td></tr></table><br>|;
		}
		++$count;
	}
	close $fh;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="hidden" name="no" value="$in{no}"><input type="hidden" name="type" value="$in{type}">|;
	print qq|<p><input type="submit" value="�폜" class="button_s"> ($count/$max_log)</p></form>|;
}

#================================================
# �L���폜
#================================================
sub delete_kiji {
	return if @delfiles <= 0; 
	
	my $this_file = "$userdir/$id/letter.cgi";
	   $this_file = "$userdir/$id/letter_log.cgi" if $in{type} eq 'send';
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		
		my $is_delete = 0;
		for my $i (0 .. $#delfiles) {
			if ($delfiles[$i] eq $btime) {
				$is_delete = 1;
				print "$bdate $bname�̎莆���폜���܂���<br>";
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

sub delete_all {
	my $this_file = "$userdir/$id/letter.cgi";
	   $this_file = "$userdir/$id/letter_log.cgi" if $in{type} eq 'send';
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,@bcomments) = split /<>/, $line;
		
		my $is_delete = 1;
		if($bcomment =~ /�S���ɑ��M�z/ && $in{type} eq 'ncountry') {
			$is_delete = 0;
		}
		if($bcomment !~ /�S���ɑ��M�z/ && $in{type} eq 'country') {
			$is_delete = 0;
		}
		
		next if $is_delete;
		push @lines, "$line\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;

	print "�莆���폜���܂���<br>";

}

sub add_refuse {
	my @lines = ();
	open my $rfh, "+< $logdir/refuse_list.cgi" or &error("$logdir/refuse_list.cgi̧�ق��ǂݍ��߂܂���");
	eval { flock $rfh, 2; };
	while (my $line = <$rfh>) {
		$line =~ tr/\x0D\x0A//d;
	$rflag++ if $line eq $m{name} ;
		push @lines, "$line\n";
	}
	push @lines, "$in{rname}\n";
	seek  $rfh, 0, 0;
	truncate $rfh, 0;
	print $rfh @lines;
	close $rfh;
}

