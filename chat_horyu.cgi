#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/_comment_tag.cgi';
#=================================================
# �����ē��_���ꗗ
#=================================================
&get_data;

$this_title  = "�����ē��[��";
$this_list   = "$logdir/chat_horyu_list";
$this_dir    = "$logdir/kaizou";
$this_script = 'chat_horyu.cgi';
$write_script = 'chat_horyu_w.cgi';
$save_script = 'chat_horyu_s.cgi';
$detail_script = 'chat_horyu_d.cgi';

# �A���������݋֎~����(�b)
$bad_time    = 5;

# �ő�۸ޕۑ�����
$max_log     = 50;

# �ő���Đ�(���p)
$max_comment = 2000;

#=================================================
&run;
&footer;
exit;

#=================================================
sub run {
	&write_comment if ($in{mode} eq "write") && $in{comment};
	&good_comment if ($in{mode} eq "good");
	&bad_comment if ($in{mode} eq "bad");
	my($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;
	
	print qq|<form method="$method" action="$write_script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�c��쐬" class="button1"></form>|;
	
	print qq|<form method="$method" action="$save_script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�I���c��" class="button1"></form>|;
	
	my $rows = $is_mobile ? 2 : 5;
	open my $fh, "< $this_list.cgi" or &error("$this_list.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
		chomp($line);
		open my $fh2, "< $this_dir/$line.cgi" or &error("$this_dir/$line.cgi ̧�ق��J���܂���");
		my @linest = <$fh2>;
		my $head_linet = $linest[0];
		my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_linet;
		my @goods = split /,/, $bgood;
		my $goodn = @goods;
		my @bads = split /,/, $bbad;
		my $badn = @bads;
		if ($hidden) {
			$bgood = "����";
			$bbad = "����";
		}
		print qq|<hr size="1">|;
		print qq|<form method="$method" action="$detail_script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="�c�_������" class="button_s">|;
		print qq|<input type="hidden" name="line" value="$line"><br>|;
		print qq|</form>|;
		if($limit > $time + 7 * 24 * 3600){
			print qq|�c�_�i�K<br>\n|;
		}elsif($limit > $time){
			print qq|������]�� $goodn �l:$bgood �������Ύ� $badn �l:$bbad<br>\n|;
		}else{
			if($goodn > $badn){
				print qq|<font size="5"><font color="blue">������]�� $goodn �l:$bgood</font> �������Ύ� $badn �l:$bbad ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
			}elsif($goodn < $badn){
				print qq|<font size="5">������]�� $goodn �l:$bgood <font color="red">�������Ύ� $badn �l:$bbad</font> ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
			}else{
				print qq|<font size="5"><font color="yellow">������]�� $goodn �l:$bgood �������Ύ� $badn �l:$bbad</font> ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
			}
		}
		my $linet = $linest[1];
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bid) = split /<>/, $linet;
		$bname .= "[$bshogo]" if ($bshogo && $bname ne '����������@���؎I');
		$bicon = qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>|;
		if ($hidden) {
			$bname = "����";
			$bicon = $default_icon;
			$bcountry = 0;
		}
		$bcomment = &comment_change($bcomment, 1);
		print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><br><br>\n|;
		my $last_linet = $linest[-1];
		my($lbtime,$lbdate,$lbname,$lbcountry,$lbshogo,$lbaddr,$lbcomment,$lbicon,$lbid) = split /<>/, $last_linet;
		print qq|�Ō�̔����F$lbcomment<font size="1">($lbdate)</font>\n|;
		close $fh2;
		print qq|<hr size="5">\n|;
	}
	close $fh;
}

#=================================================
# �������ݏ���
#=================================================
sub write_comment {
	&error('�{���ɉ���������Ă��܂���') if $in{comment} eq '';
	&error("�{�����������܂�(���p$max_comment�����܂�)") if length $in{comment} > $max_comment;
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("�t�@�C�������ُ�ł�") if ($target =~ /[^0-9]/);
	&error("$target.cgi�Ƃ����t�@�C�������݂��܂���") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, ">> $this_dir/$target.cgi" or &error("$this_dir/$target.cgi ̧�ق��J���܂���");

	# ����ݸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"

	my $wname = $in{tokumei} ? '����������@���؎I' : $m{name};
	my $mshogo = length($m{shogo}) > 16 ? substr($m{shogo}, 0, 16) : $m{shogo};
	print $fh "$time<>$date<>$wname<>$m{country}<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>\n";
	close $fh;
	return 1;
}

#=================================================
# �Ǖ]��
#=================================================
sub good_comment {
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("�t�@�C�������ُ�ł�") if ($target =~ /[^0-9]/);
	&error("$target.cgi�Ƃ����t�@�C�������݂��܂���") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, "+< $this_dir/$target.cgi" or &error("$target.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($bgood,$bbad,$limit) = split /<>/, $head_line;
	my @goods = split /,/, $bgood;
	my @bads = split /,/, $bbad;
	$bgood = "";
	for my $gname (@goods){
		unless($gname eq $m{name}){
			if($bgood eq ""){
				$bgood .= "$gname";
			}else{
				$bgood .= ",$gname";
			}
		}
	}
	$bbad = "";
	for my $bname (@bads){
		unless($bname eq $m{name}){
			if($bbad eq ""){
				$bbad .= "$bname";
			}else{
				$bbad .= ",$bname";
			}
		}
	}
	if($bgood eq ""){
		$bgood .= "$m{name}";
	}else{
		$bgood .= ",$m{name}";
	}
	push @lines, "$bgood<>$bbad<>$limit<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

#=================================================
# ���]��
#=================================================
sub bad_comment {
	my $target = $in{target};
	return 1 if ($target eq "no_write");
	&error("�t�@�C�������ُ�ł�") if ($target =~ /[^0-9]/);
	&error("$target.cgi�Ƃ����t�@�C�������݂��܂���") unless(-e "$this_dir/$target.cgi");
	my @lines = ();
	open my $fh, "+< $this_dir/$target.cgi" or &error("$target.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my ($bgood,$bbad,$limit) = split /<>/, $head_line;
	my @goods = split /,/, $bgood;
	my @bads = split /,/, $bbad;
	$bgood = "";
	for my $gname (@goods){
		unless($gname eq $m{name}){
			if($bgood eq ""){
				$bgood .= "$gname";
			}else{
				$bgood .= ",$gname";
			}
		}
	}
	$bbad = "";
	for my $bname (@bads){
		unless($bname eq $m{name}){
			if($bbad eq ""){
				$bbad .= "$bname";
			}else{
				$bbad .= ",$bname";
			}
		}
	}
	if($bbad eq ""){
		$bbad .= "$m{name}";
	}else{
		$bbad .= ",$m{name}";
	}
	push @lines, "$bgood<>$bbad<>$limit<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
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
	
	open my $fh, "+< ${this_list}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
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

