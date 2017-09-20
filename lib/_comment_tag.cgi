sub comment_change {
	my ($bcomment, $chat_flag) = @_;
	if ($chat_flag){
		$pic_size = q|width="25px" height="25px"|;
	}else{
		$pic_size = $mobile_icon_size;
	}
	my $pai_size = q|width="12px" height="16px"|;
	$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;

	# ���K�\�����g�����u���A�ł��Ȃ�ׂ����点�Ȃ�
	# ���K�\���Ńp�t�H�[�}���X��������̂̓}�b�`����Ώۂ����݂��Ȃ������ꍇ�炷���i�{���Ƀ}�b�`���Ȃ��̂��ꐶ�����T�����邽�߁j
	# �u&big(hoge)�v�������ꂽ���͂ł�&big�̒u�������������Ƀ}�b�`���Ȃ� small,color,chikuwa... �̊e���K�\�����삪�l�b�N�ɂȂ��Ă���
	# if index �ŐU�蕪���Ă���̂��������ǂ����͕������
	$mes .= "$bcomment<br>";
#	while ($bcomment =~ /([^\x80-\x9f|^\xE0-\xFF])([\xF7\xF9\xFB])([\x41-\x7E\x80-\x9B\xA1-\xFA])/) {
#		my $tail = $1;
#		my @emoji = ();
#		$emoji[0] = unpack("H*", $2);
#		$emoji[1] = unpack("H*", $3);
#		my $icon_name = "$emoji[0]$emoji[1]";#sprintf("%X%X", $emoji[0], $emoji[1]);
#		$bcomment =~ s/[^\x80-\x9f|^\xE0-\xFF][\xF7\xF9\xFB][\x41-\x7E\x80-\x9B\xA1-\xFA]/$tail<img src="$icondir\/emoji\/$icon_name.gif" style="vertical-align:middle;" width="20px" height="20px">/;
#	}
	if (index($bcomment, '&amp;') > -1) {
		$bcomment =~ s|&amp;big\((.*?)\)|<font size="+1">\1</font>|g;
		$bcomment =~ s|&amp;big(\d+)\((.*?)\)|<font size="+\1">\2</font>|g;
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
		$bcomment =~ s|&amp;italic\((.*?)\)|<i>\1</i>|g;
		while ($bcomment =~ /&amp;mahjong\(([mspz][1-9])(.*?)\)/) {
			$bcomment =~ s|&amp;mahjong\(([mspz][1-9])(.*?)\)|<img src="$icondir/mahjongpai/\1.gif" style="vertical-align:middle;" $pai_size>&amp;mahjong(\2)|g;
		}
		while ($bcomment =~ /&amp;#(\d+)&#59;/) {
			my $icon_name = sprintf("%x", $1);
			my $len = length($icon_name);
			$bcomment =~ s|&amp;#(\d+)&#59;|<img src="$icondir/emoji/$icon_name.png" style="vertical-align:middle;" width="20px" height="20px">|;
#			$bcomment =~ s|&amp;#(\d+)&#59;|<img src="$icondir/emoji/$icon_name.gif" style="vertical-align:middle;" width="20px" height="20px">| if $len == 4;
		}
		$bcomment =~ s|&amp;mahjong\((.*?)\)|\1|g;
	
		# ���K�\���Ƃ��Ȃ����ꂸ���Ǝg���ĂĂ悭������񂵗͋Z
		if (!$is_mobile) {
			if ($chat_flag) {
				$bcomment =~ s!&amp;img\(([^&]*?)(jpg|png)\)!<a href="./../upbbs/img-box/\1\2"><img src="./../upbbs/img-box/\1\2" $pic_size></a>!g;
			}
			else {
				$bcomment =~ s!&amp;img\(([^&]*?)(jpg|png)\)!<p class="img"><a href="./../upbbs/img-box/\1\2"><img src="./../upbbs/img-box/\1\2"></a></p>!g;
			}
			$bcomment =~ s|&amp;img\((.*?)\)|<a href="./../upbbs/img-box/\1">\1</a>|g;
		}
		else {
			$bcomment =~ s|&amp;img\((.*?)\)|<a href="./../upbbs/img-box/\1">\1</a>|g;
		}
	}

	return $bcomment;
}


1; # �폜�s��
