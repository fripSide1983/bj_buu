require './lib/_comment_tag.cgi';
require 'lib/_write_tag.cgi';
#================================================
# BBS2 Arranged by Oiiuii
#================================================

# 連続書き込み禁止時間(秒)
$bad_time    = 10;

# 最大ﾛｸﾞ保存件数
$max_log     = 50;

# 最大ﾛｸﾞ保存期間
$max_time     = 5 * 24 * 3600;

# 最大ｺﾒﾝﾄ数(半角)
$max_comment = 400;
$rmax_comment = 30;

# ﾒﾝﾊﾞｰに表示される時間(秒)
$limit_member_time = 60 * 4;

my @menus = ([999, 'その他'], [1000, '金'], @weas, @eggs, @pets);


#================================================
sub run {
	if ($in{mode} eq "write" && $in{ad_type} ne '2' && ($in{comment} || $in{is_del} eq '1' || ($in{want} ne '0' || $in{pay} ne '0'))) {
		&write_comment;
	}
	if ($in{mode} eq "write_res") {
		if($in{is_letter}){
			$in{comment} .= "<hr>【宣伝言板へのレス】";
			&send_letter($in{res_name}, 1);
		}else {
			&write_res;
		}
	}
	
	my($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title <font size="2" style="font-weight:normal;">$this_sub_title</font></h2>|;
	print qq|<p>$mes</p>| if $mes;
	
	my $rows = $is_mobile ? 2 : 5;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<br><textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1"></textarea><br>|;
	print qq|<input type="submit" value="書き込む" class="button_s">|;
	print qq|<input type="checkbox" name="is_del" value="1">広告を取り下げる<br>|;
#	print qq|<input type="radio" name="ad_type" value="0">通常<br>|;
	print qq|<input type="radio" name="ad_type" value="1" checked>広告<br>|;
	print qq|<input type="radio" name="ad_type" value="2">検索<br>|;
	print qq|求<select name="want" class="menu1">|;
	for my $i (0 .. $#menus) {
		next if $menus[$i][0] eq '0';
		print qq|<option value="$i">$menus[$i][1]</option>|;
	}
	print qq|</select>|;
	print qq|出<select name="pay" class="menu1">|;
	for my $i (0 .. $#menus) {
		next if $menus[$i][0] eq '0';
		print qq|<option value="$i">$menus[$i][1]</option>|;
	}
	print qq|</select></form><br>|;

	print qq|<font size="2">$member_c人:$member</font><hr>|;

	my @lines;
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	@lines = <$fh>;
	while (my $line = shift @lines) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bwant,$bpay,$btype,$bres1,$bres2,$bres3,$bres4,$bres5) = split /<>/, $line;
		if($in{ad_type} eq '2'){
				next if $bwant ne $in{want} && $bpay ne $in{pay};
		}
		$bicon = $bicon ? qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>| : '';
		$bcomment = &comment_change($bcomment, 0);
		my $reses = "----<br>";
		$reses .= "$bres1<br>" if $bres1;
		$reses .= "$bres2<br>" if $bres2;
		$reses .= "$bres3<br>" if $bres3;
		$reses .= "$bres4<br>" if $bres4;
		$reses .= "$bres5<br>" if $bres5;
		if($in{mode} eq "res" && $in{res_name} eq $bname){
			print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="write_res"><input type="hidden" name="res_name" value="$bname">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<br><textarea name="comment" cols="30" rows="1" wrap="soft" class="textarea1"></textarea><br>|;
			print qq|<input type="checkbox" name="is_letter" value="1">手紙で送る<br>|;
			print qq|<input type="submit" value="レス" class="button_s">|;
			print qq|</form><br>|;
		}else{
			print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="res"><input type="hidden" name="res_name" value="$bname">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="レス" class="button_s"></form><br>|;
		}
		$bname = &name_link($bname);
		$bname .= "[$bshogo]" if $bshogo;
		if ($is_mobile) {
			print qq|<div>$bicon<font color="$cs{color}[$bcountry]">$bname<br>$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font>$reses</div><hr size="1">\n|;
		}
		else {
			print qq|<table border="0"><tr><td valign="top" style="padding-right: 0.5em;">$bicon<br><font color="$cs{color}[$bcountry]">$bname</font></td><td valign="top"><font color="$cs{color}[$bcountry]">$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font><br>$reses</td></tr></table><hr size="1">\n|;
		}
	}
	close $fh;
}

sub write_res{
	&error('本文に何も書かれていません') if $in{comment} eq '';
	&error("本文が長すぎます(半角$rmax_comment文字まで)") if length $in{comment} > $rmax_comment;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	
	# ｵｰﾄﾘﾝｸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"

	while (my $line = <$fh>) {
		my($otime,$odate,$oname,$ocountry,$oshogo,$oaddr,$ocomment,$oicon,$owant,$opay,$otype,$ores1,$ores2,$ores3,$ores4,$ores5) = split /<>/, $line;
		if ($oname eq $in{res_name}){
			push @lines, "$otime<>$odate<>$oname<>$ocountry<>$oshogo<>$oaddr<>$ocomment<>$oicon<>$owant<>$opay<>$otype<>$in{comment}($m{name})<>$ores1<>$ores2<>$ores3<>$ores4<>\n";
		}else{
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

sub write_comment {
	&error('本文に何も書かれていません') if $in{comment} eq '' && $in{is_del} ne '1' && ($in{want} eq '0' && $in{pay} eq '0');
	&error("本文が長すぎます(半角$max_comment文字まで)") if length $in{comment} > $max_comment;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	eval { flock $fh, 2; };
	
	my $mname;
	($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 0);
	
	if($in{want} ne '0'){
		     $in{comment} = "求)$menus[$in{want}][1]<br>" . $in{comment};
	}
	if($in{pay} ne '0'){
		     $in{comment} = "出)$menus[$in{pay}][1]<br>" . $in{comment};
	}
	my $head_line = <$fh>;
	my ($htime,$hname,$hcomment,$htype) = (split /<>/, $head_line)[0,2,6,10];
	my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bwant,$bpay,$btype) = split /<>/, $line;
	return 0 if $in{comment} eq $hcomment;
	if ($hname eq $m{name} && $htime + $bad_time > $time) {
		&error("連続投稿は禁止しています。<br>しばらく待ってから書き込んでください");
	}
	push @lines, $head_line unless $hname eq $m{name} && $htype eq '1' && ($in{ad_type} eq '1' || $in{is_del} eq '1');

	while (my $line = <$fh>) {
		my ($otime,$oname,$ocomment,$otype) = (split /<>/, $line)[0,2,6,10];
		next if $oname eq $m{name} && $otype eq '1' && ($in{ad_type} eq '1' || $in{is_del} eq '1');
		if ($otype == 0){
		   next if @lines >= $max_log - 1;
		}else {
		      next if $otime + $max_time < $time;
		}
		push @lines, $line;
	}
	my $mshogo = length($m{shogo}) > 16 ? substr($m{shogo}, 0, 16) : $m{shogo};
	unshift @lines, "$time<>$date<>$mname<>$m{country}<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>$in{want}<>$in{pay}<>1<>以降のレスはありません<><><><><>\n" unless $in{is_del} eq '1';

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次
		
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

1; # 削除不可
