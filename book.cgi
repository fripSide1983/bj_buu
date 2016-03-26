#!/usr/local/bin/perl --
require './config.cgi';
require './config_game.cgi';
require "$datadir/header_myroom.cgi";
#================================================
# �{�쐬 Created by Merino
#================================================

# �ő���Đ�(���p)
$max_comment = 4000;

# ��`��
$need_ad_money = 500;


#================================================
&decode;
&header;
&read_user;
&header_myroom;
&run;
&footer;
exit;

#================================================
# �{�쐬
#================================================
sub run {
	&write_book if $in{mode} eq "write";
	
	my $sub_mes = '';
	my $count = 0;
	opendir my $dh, "$userdir/$id/book" or &error("$userdir/$id/book�ިڸ�؂��J���܂���");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;
		next if $file_name =~ /^backup$/;
		my $file_title = &get_goods_title($file_name);
		$sub_mes .= qq|<li><a href="$userdir/$id/book/$file_name" target="_blank">$file_title</a>|;
		++$count;
	}
	closedir $dh;

	print qq|<p>$mes</p>|;
	print qq|<p>$m{name}�̖{�̏����� $count / $max_my_book��</p>|;

	if ($max_my_book > $count) {
		print qq|<ul><li>�쐬����÷�Ăɂ��ẮA���쌠�E�ё������ɂ��Ė@�ߏ�̋`���ɏ]���A<br>�쐬������ڲ԰�̎��ȐӔC�ɂ����ēo�^�E�f�ڂ������̂Ƃ��܂��B</ul>|;
		my $rows = $is_mobile ? 2 : 20;
		print qq|<form method="$method" action="book.cgi"><input type="hidden" name="mode" value="write"><input type="hidden" name="no" value="$in{no}">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		print qq|����[�S�p30(���p60)�����܂�]<br><input type="text" name="title" class="text_box_b"><br>|;
		print qq|�{��[�S�p| .int($max_comment * 0.5). qq|(���p$max_comment)�����܂�]<br>|;
		print qq|<textarea name="comment" cols="80" rows="$rows" class="textarea1"></textarea><br>|;
		print qq|<input type="radio" name="option" value="" checked>�ʏ�<br>|;
		print qq|<input type="radio" name="option" value="ad">������{���`����($need_ad_money G)<br>|;
		print qq|<input type="radio" name="option" value="contest">��ýėp(���قƂ͕ʂ�̧�ٖ�������ƂȂ�܂�)<br>|;
		print qq|<input type="submit" value="�{���쐬" class="button_s"></form>|;
	}
	
	print qq|<hr>�������Ă���{<ul>$sub_mes</ul><br>|;
}

sub write_book {
	&error("���ق��L�����Ă�������") unless $in{title};
	&error("���ق���ص��(.)�͎g���܂���") if $in{title} =~ /\./;
	&error("���ق̐擪�ɱ��ްײ�(_)�͎g���܂���") if $in{title} =~ /^_/;
	&error("���ق̕��������ް�B���p60�����܂łł�") if length $in{title} > 60;
	&error("�{�����L�����Ă�������") unless $in{comment};
	&error("�{���̕��������ް�B���p$max_comment�����܂łł�") if length $in{comment} > $max_comment;

	my $file_title = '';
	if ($in{option} eq 'contest') {
		$file_title = "_$time.html";
	}
	else {
		$file_title = unpack 'H*', "$in{title} ��:$m{name}";
		$file_title .= '.html';
	}
	&error("���łɓ������O�̍�i�����݂��܂�") if -f "$userdir/$id/book/$file_title";

	my $goods_c = &my_goods_count("$userdir/$id/book");
	&error("$max_my_book���ȏ�{�����L���邱�Ƃ��ł��܂���") if $goods_c >= $max_my_book;

	$html .= qq|<html><head>|;
	$html .= qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	$html .= qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
	$html .= qq|<link rel="stylesheet" type="text/css" href="../../../$htmldir/bj.css">|;
	$html .= $in{option} eq 'contest' ? qq|<title>$in{title}</title>| : qq|<title>$in{title} ��:$m{name}</title>|;
	$html .= qq|</head><body $body>|;
	$html .= qq|<form action="../../../"><input type="submit" value="�s�n�o" class="button1"></form>|;
	$html .= $in{option} eq 'contest' ? qq|<h1>$in{title}</h1>| : qq|<h1>$in{title} ��:$m{name}</h1>|;
	$html .= qq|<div>$in{comment}</div>|;
	$html .= qq|<br><div align="right" style="font-size:11px">|;
	$html .= qq|Blind Justice Ver$VERSION<br><a href="http://cgi-sweets.com/" target="_blank">CGI-Sweets</a><br><a href="http://amaraku.net/" target="_blank">Ama�y.net</a><br>|; # ����\��:�폜�E��\�� �֎~!!
	$html .= qq|$copyright|;
	$html .= qq|</div></body></html>|;
	
	open my $fh, "> $userdir/$id/book/$file_title" or &error("$userdir/$id/book/$file_titlȩ�ق����܂���");
	print $fh $html;
	close $fh;
	
	if ($in{option} eq 'contest') {
		$mes .= "$non_title�̖{�����܂���<br>";
	}
	else {
		$mes .= "�w$in{title}�x�Ƃ����{�����܂���<br>";

		# ��`
		if ($in{option} eq 'ad') {
			&read_cs;
			&write_book_news("$cs{name}[$m{country}]��$m{name}���w$in{title}�x�Ƃ�����i�𔭕\\���܂���");
			$mes .= "�w$in{title}�x�Ƃ�����i�𔭕\\���܂���<br>";
			$m{money} -= $need_ad_money;
			&write_user;
		}
	}
}
