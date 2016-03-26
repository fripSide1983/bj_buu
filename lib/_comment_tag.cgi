sub comment_change {
	my ($bcomment, $chat_flag) = @_;
	if ($chat_flag){
		$pic_size = q|width="25px" height="25px"|;
	}else{
		$pic_size = $mobile_icon_size;
	}
	my $pai_size = q|width="12px" height="16px"|;
	$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
	$bcomment =~ s|&amp;big\((.*?)\)|<font size="+1">\1</font>|g;
#	$bcomment =~ s|&amp;big(\d+)\((.*?)\)|<font size="+\1">\2</font>|g;
	$bcomment =~ s|&amp;small\((.*?)\)|<font size="-1">\1</font>|g;
	$bcomment =~ s|&amp;small(\d+)\((.*?)\)|<font size="-\1">\2</font>|g;
	$bcomment =~ s|&amp;color([0-9A-Fa-f]{6})\((.*?)\)|<font color="#\1">\2</font>|g;
	$bcomment =~ s|&amp;chikuwa\(\)|<img src="$icondir/chikuwa.jpeg" style="vertical-align:middle;" $pic_size>|g;
	$bcomment =~ s|&amp;homashinchiw\(\)|<img src="$icondir/homashinchiw.jpg" style="vertical-align:middle;" $pic_size>|g;
	$bcomment =~ s|&amp;kappa\(\)|<img src="$icondir/kappa.png" style="vertical-align:middle;" $pic_size>|g;
	$bcomment =~ s|&amp;homo\(\)|��(��^o^)���z���H|g;
	$bcomment =~ s|&amp;italic\((.*?)\)|<i>\1</i>|g;
	$bcomment =~ s|&amp;bold\((.*?)\)|<b>\1</b>|g;
	$bcomment =~ s|&amp;underline\((.*?)\)|<u>\1</u>|g;
	while ($bcomment =~ /&amp;mahjong\(([mspz][1-9])(.*?)\)/) {
		$bcomment =~ s|&amp;mahjong\(([mspz][1-9])(.*?)\)|<img src="$icondir/mahjongpai/\1.gif" style="vertical-align:middle;" $pai_size>&amp;mahjong(\2)|g;
	}
	$bcomment =~ s|&amp;mahjong\((.*?)\)|\1|g;
	
	return $bcomment;
}


1; # �폜�s��
