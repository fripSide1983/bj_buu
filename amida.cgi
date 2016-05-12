#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
use List::Util;
use CGI;
my $this_script = 'amida.cgi';
$this_file = "$logdir/amida";
#================================================
# ���݂����� Created by nanamie
#================================================

# qq|�|| �S�p�}�C�i�X�Ƃ��S�p�`���_�̓G���[

$max_log = 30;
$cgi = CGI->new;


#================================================
&header;

$in{id} = $cgi->param("id");
$in{login_name} = pack 'H*', $in{id};
$in{pass} = $cgi->param("pass");

&read_user;
&access_check;

$in{step} = $cgi->param("step");
$in{title} = $cgi->param("title");
$in{count} = $cgi->param("count");
$in{items} = $cgi->param("items");
$in{open} = $cgi->param("open");
$in{amida} = $cgi->param("amida");
$in{no} = $cgi->param("no");
$in{cmp} = $cgi->param("cmp");

$mes = "";

&run;

&footer;
exit;

#================================================

sub run {

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;

	# ���݂����ꗗ���J��
	if ($in{step} == 0 || $in{step > 3}) {
		&view_amida;	# $in{amida} ����Ȃ�ꗗ
	}
	# ���݂��쐬���
	elsif ($in{step} == 1) {
		&create_amida_form;
	}
	# ���݂��쐬
	elsif ($in{step} == 2) {
		&create_amida;
	}
	# ���݂��̏㏑��
	elsif ($in{step} == 3) {
		&write_amida;
	}
	# ���݂�����L�b�N
	elsif ($in{step} == 4) {
		&kick_amida;
	}
}

sub show_head {
	my $head = @_[0];
	print $head ? "<h1>$head</h1>" : "<h1>���݂�����</h1>" ;
	if (($in{step} || $in{amida}) && $in{step} != 2) {
		print qq|<form method="$method" action="$this_script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="step" value="0">|;
		print qq|<input type="submit" value="�ꗗ�ɖ߂�" class="button1"></form>|;
	}
	elsif ($in{step} != 2) {
		print qq|<form method="$method" action="$this_script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="step" value="1">|;
		print qq|<input type="submit" value="���݂������" class="button1"></form>|;
	}
}

# ���݂���ݒ肷��t�H�[��
sub create_amida_form {
	&show_head;
	print qq|<form method="$method" action="$this_script"><table>|;
	print qq|<tr><td><label for="title">�����̃^�C�g���F</label></td><td><input type="text" name="title" id="title" min="1" max="30" required="required" value="$in{title}"></td></tr>|;
	print qq|<tr><td><label for="count">�����̖{���F</label></td><td><input type="number" name="count" id="count" min="2" max="30" required="required" value="$in{count}"></td></tr>|;
	print qq|<tr><td><label for="items">������ܕi�F<br>�i1�s1�ܕi�j</label></td><td><textarea name="items" rows="8" cols="10" word="soft" id="items" required="required">$in{items}</textarea></td></tr>|;
	print qq|<tr><td><label for="open">���܂�������J�F</label></td><td><input type="checkbox" name="open" value="1"/></td></tr>|;
	print qq|<tr><td colspan="2" style="text-align:center;"><input type="submit" value="���݂��쐬" class="button1"></td></tr>|;
	print qq|</table><input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="step" value="2"></form>|;
}

# ���݂����Đݒ肷��t�H�[��
sub rewrite_amida_form {
	my ($err, @data) = @_;
	print "<h1>���݂�����</h1>";
	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="step" value="0">|;
	print qq|<input type="submit" value="�ꗗ�ɖ߂�" class="button1"></form>|;

	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="id" value="$data[0]"><input type="hidden" name="pass" value="$data[1]"><input type="hidden" name="title" value="$data[2]"><input type="hidden" name="count" value="$data[3]"><input type="hidden" name="items" value="$data[4]"><input type="hidden" name="open" value="$data[5]"><input type="hidden" name="step" value="1">|;
	print qq|<input type="submit" value="���݂�����蒼��" class="button1"></form>|;
	&error($err);
}

# ���݂����ꗗ���J��
sub view_amida {
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi̧�ق��J���܂���");
	if ($in{amida}) {
		while (my $line = <$fh>) {
			$line =~ tr/\x0D\x0A//d;
			my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $bopen, $busers, $bcmp, $bscount, $bsusers, $bsitems) = split /<>/, $line;
			next	if $btime != $in{amida};

			my @user_list = split /,/, $busers;
			my @suser_list = split /,/, $bsusers;
			my @sitem_list = split /,/, $bsitems;

			&show_head("$btitle ��F$bmaker $bdate");

			print qq|<p>���̂��݂������͏I�����Ă��܂�</p>|	if $bcmp;
			print qq|<span>�����̖{���F$bcount</span><br>|;
			print qq|<span>�ܕi���X�g�F$bitems</span><br>|;
			print qq|<span>�Q���Ґ��F$bscount�l</span><br>|;
			my $open = $bopen ? "ON" : "OFF" ;
			print qq|<span>�������J�F$open</span><br><br>|;

			print "<table>";
			for (my $i = 0; $i < $bcount; $i++) {
				print "<tr><td>".($i+1).".";
				if ($in{login_name} eq $bmaker && !$bcmp) {
					print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=4&amida=$btime&no=$i">$user_list[$i]������L�b�N����</a>|	if $user_list[$i];
				}
				else {
					print qq|$user_list[$i]|	if $user_list[$i];
				}
#				print qq|$user_list[$i]| if $user_list[$i];
				print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=3&amida=$btime&no=$i">���̂����ɂ���</a>|	unless $user_list[$i] || $bcmp;
				print "</td><td>�|���݂����͏ȗ��|</td>";
				print "<td>$suser_list[$i]</td>"	if $bcmp;
				print "<td>$sitem_list[$i]</td>"	if $bcmp;
				print "</tr>";
			}
			print "</table>";
		} # while (my $line = <$fh>) {
	} # if ($in{amida}) {
	else {
		&show_head;
		print "<ul>";
		while (my $line = <$fh>) {
			$line =~ tr/\x0D\x0A//d;
			my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $bopen, $busers, $bcmp, $bscount, $bsusers, $bsitems) = split /<>/, $line;

			if ($bcmp) { print "<li>[���J��]"; } else { print "<li>[��W��]"; } 
			print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=0&amida=$btime">$btitle</a> $bmaker�� $bdate|;
			if (!$bcmp && $in{login_name} eq $bmaker) {
				print qq| <a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$btime&step=3&cmp=1">���J����</a>|;
			}
			print "</li>";
		}
		print "</ul>";
	}
	close $fh;
}

# ���݂���V�K�쐬�A�ł��Ȃ���΍Đݒ�𑣂�
sub create_amida {
	&rewrite_amida_form('�^�C�g��������܂���', ($in{id}, $in{pass}, $in{title}, $in{count}, $in{items}, $in{open}))	unless $in{title};
	&rewrite_amida_form('�^�C�g���ɕs���ȕ���( ,;\"\'&<>\\\/ )���܂܂�Ă��܂�', ($in{id}, $in{pass}, $in{title}, $in{count}, $in{items}, $in{open}))	if $in{title} =~ /[,;\"\'&<>\\\/]/;#"
	&rewrite_amida_form('�{���ɓ��͂ł���̂� 2 �ȏ�̐��l�����ł�', ($in{id}, $in{pass}, $in{title}, $in{count}, $in{items}, $in{open}))	unless $in{count}  =~ /^[0-9]+$/;#"
	&rewrite_amida_form('�ܕi���X�g�ɕs���ȕ���( ,;\"\'&<>\\\/ )���܂܂�Ă��܂�', ($in{id}, $in{pass}, $in{title}, $in{count}, $in{items}, $in{open}))	if $in{items} =~ /[,;\"\'&<>\\\/]/;#"
	&rewrite_amida_form('�ܕi���X�g�ɉ������͂���Ă��܂���', ($in{id}, $in{pass}, $in{title}, $in{count}, $in{items}, $in{open}))	unless $in{items};

	$in{items} =~ s/^\s+//gm;
	$in{items} =~ s/\s+$//gm;
	$in{items} =~ s/\r\n/,/g;
	$in{items} =~ s/\r/,/g;
	$in{items} =~ s/\n/,/g;
	my @item_list = split /,/, $in{items};

	&rewrite_amida_form('�ܕi���X�g�ɉ������͂���Ă��܂���', ($in{id}, $in{pass}, $in{title}, $in{count}, $in{items}, $in{open}))	unless @item_list;
	&rewrite_amida_form('�ܕi���������̖{���𒴂��Ă��܂�', ($in{id}, $in{pass}, $in{title}, $in{count}, $in{items}, $in{open}))	if @item_list > $in{count};

	my $users = "," x ($in{count}-1);
	my $sitems = "," x ($in{count}-1);

	&show_head;
	print "���݂��������쐬���܂���<br>";
	print "<ul>";
	print qq|<li>[��W��]<a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$time">$in{title}</a> $in{login_name}�� $date|;
	print qq| <a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$time&step=3&cmp=1">���J����</a></li>|;

	my @lines = ();
	push @lines, "$time<>$date<>$in{login_name}<>$in{title}<>$in{count}<>$in{items}<>$in{open}<>$users<>0<>0<>$users<>$sitems<>\n";
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $bopen, $busers, $bcmp, $bscount, $bsusers, $bsitems) = split /<>/, $line;

		if ($bcmp) { print "<li>[���J��]"; } else { print "<li>[��W��]"; } 
		print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$btime">$btitle</a> $bmaker�� $bdate|;
		if (!$bcmp && $in{login_name} eq $bmaker) {
			print qq| <a href="$this_script?id=$in{id}&pass=$in{pass}&amida=$btime&step=3&cmp=1">���J����</a>|;
		}
		print "</li>";
		push @lines, "$line\n";
		last if @lines >= $max_log;
	}
	print "</ul>";

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

# ���݂��ɎQ����������J����
sub write_amida {
	if ($in{amida}) {
		my @lines = ();
		open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi̧�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			$line =~ tr/\x0D\x0A//d;
			my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $bopen, $busers, $bcmp, $bscount, $bsusers, $bsitems) = split /<>/, $line;
			if ($btime ne $in{amida}) {
				push @lines, "$line\n";
				next;
			}

			my @user_list = split /,/, $busers;
			@user_list = realloc_array($bcount, @user_list);
			my @item_list = split /,/, $bitems;
			@item_list = realloc_array($bcount, @item_list);

			&show_head("$btitle ��F$bmaker $bdate");
#			print qq|<p>$btitle ��F$bmaker $bdate</p>|;

			if ($bcmp || ($in{login_name} eq $bmaker && $in{cmp}) ) {
				print qq|<p>���̂��݂������͏I�����Ă��܂�</p>| if $bcmp;
				print qq|<p>���݂����������J���܂���</p>| unless $bcmp;
			}
			elsif ( -1 < index($busers, $in{login_name}) ) {
				print qq|<p>���łɴ��ذ�ς݂ł��B�d�����Ĵ��ذ���邱�Ƃ͂ł��܂���</p>|;
			}
			elsif ($user_list[$in{no}]) {
				print qq|<p>���̂����͂��ł�$user_list[$in{no}]���񂪴��ذ���Ă��܂�</p>|;
			}
			else {
				print "<p>".($in{no}+1)."�Ԗڂ̂����ɴ��ذ���܂���</p>";
				$user_list[$in{no}] = $in{login_name};
				$bscount++;
				print qq|<p>���ׂĂ̂��������܂������ߌ��ʂ����J���܂�</p>|	if ($bcount <= $bscount) && $bopen;
				$busers = join(',', @user_list);
			}

			print qq|<span>�����̖{���F$bcount</span><br>|;
			print qq|<span>�ܕi���X�g�F$bitems</span><br>|;
			print qq|<span>�Q���Ґ��F$bscount�l</span><br>|;
			my $open = $bopen ? "ON" : "OFF" ;
			print qq|<span>�������J�F$open</span><br><br>|;

			my @suser_list = ();
			if ( !$bcmp && ($bcount <= $bscount) && $bopen  || ($in{login_name} eq $bmaker && $in{cmp}) ) {
				# �Q���҂����܂��������J���ꂽ�C�R�[���������J
				@suser_list = List::Util::shuffle(@user_list);
				$bsusers = join(',', @suser_list);
				@item_list = List::Util::shuffle(@item_list);
				$bsitems = join(',', @item_list);
				$bcmp = 1;
			}

			print "<table>";
			for (my $i = 0; $i < $bcount; $i++) {
				print "<tr><td>".($i+1).".";
				if ($in{login_name} eq $bmaker && !$bcmp) {
					print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=4&amida=$btime&no=$i">$user_list[$i]������L�b�N����</a>|	if $user_list[$i];
				}
				else {
					print qq|$user_list[$i]|	if $user_list[$i];
				}
				print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=3&amida=$btime&no=$i">���̂����ɂ���</a>|	unless $user_list[$i] || $bcmp;
				print "</td><td>�|���݂����͏ȗ��|</td>";
				print "<td>$suser_list[$i]</td>"	if $bcmp;
				print "<td>$item_list[$i]</td>"	if $bcmp;
				print "</tr>";
			}
			print "</table>";
			$line = "$btime<>$bdate<>$bmaker<>$btitle<>$bcount<>$bitems<>$bopen<>$busers<>$bcmp<>$bscount<>$bsusers<>$bsitems<>";

			push @lines, "$line\n";
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
	else {
		&show_head;
		print "<p>���̂��݂������͑��݂��܂���</p>";
	}
}

# ���݂��ɎQ����������J����
sub kick_amida {
	if ($in{amida}) {
		my @lines = ();
		open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi̧�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			$line =~ tr/\x0D\x0A//d;
			my ($btime, $bdate, $bmaker, $btitle, $bcount, $bitems, $bopen, $busers, $bcmp, $bscount, $bsusers, $bsitems) = split /<>/, $line;
			if ($btime ne $in{amida}) {
				push @lines, "$line\n";
				next;
			}

			my @user_list = split /,/, $busers;
			@user_list = realloc_array($bcount, @user_list);
			my @item_list = split /,/, $bitems;
			@item_list = realloc_array($bcount, @item_list);

			&show_head("$btitle ��F$bmaker $bdate");
#			print qq|<p>$btitle ��F$bmaker $bdate</p>|;

#			if (($bcmp && $bopen) || ($in{login_name} eq $bmaker && $in{cmp}) ) {
#				print qq|<p>���̂��݂������͏I�����Ă��܂�</p>| if $bcmp;
#				print qq|<p>���݂����������J���܂���</p>| unless $bcmp;
#			}
			if (!$bcmp && $in{login_name} eq $bmaker) {
				print "<p>$user_list[$in{no}]������L�b�N���܂���</p>";
				$user_list[$in{no}] = "";
				$bscount--;
				$busers = join(',', @user_list);
			}

			print qq|<span>�����̖{���F$bcount</span><br>|;
			print qq|<span>�ܕi���X�g�F$bitems</span><br>|;
			print qq|<span>�Q���Ґ��F$bscount�l</span><br>|;
			my $open = $bopen ? "ON" : "OFF" ;
			print qq|<span>�������J�F$open</span><br><br>|;

			print "<table>";
			for (my $i = 0; $i < $bcount; $i++) {
				print "<tr><td>".($i+1).".";
				if ($in{login_name} eq $bmaker && !$bcmp) {
					print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=4&amida=$btime&no=$i">$user_list[$i]������L�b�N����</a>|	if $user_list[$i];
				}
				else {
					print qq|$user_list[$i]|	if $user_list[$i];
				}
				print qq|<a href="$this_script?id=$in{id}&pass=$in{pass}&step=3&amida=$btime&no=$i">���̂����ɂ���</a>|	unless $user_list[$i] || $bcmp;
				print "</td><td>�|���݂����͏ȗ��|</td>";
				print "<td>$suser_list[$i]</td>"	if $bcmp;
				print "<td>$item_list[$i]</td>"	if $bcmp;
				print "</tr>";
			}
			print "</table>";
			$line = "$btime<>$bdate<>$bmaker<>$btitle<>$bcount<>$bitems<>$bopen<>$busers<>$bcmp<>$bscount<>$bsusers<>$bsitems<>";

			push @lines, "$line\n";
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
	else {
		&show_head;
		print "<p>���̂��݂������͑��݂��܂���</p>";
	}
}

sub realloc_array {
	my ($size, @array) = @_;
	for (my $i = 0; $i < $size; $i++) {
		$array[$i] = ""	unless $array[$i];
	}
	return @array;
}