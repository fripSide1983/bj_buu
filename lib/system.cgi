require './lib/jcode.pl';
require './lib/summer_system.cgi';
use Time::Local;
&get_date; # ���ԂƓ��t�͏펞�K�v�Ȃ̂ŏ�Ɏ擾
#================================================
# Ҳ݂ł悭�g������ Created by Merino
#================================================

#================================================
# �� + ���E �f�[�^�ǂݍ��� countries
#================================================
sub read_cs {
	# -------------------
	# Get %cs
	# ���ɑ����Ă��Ȃ��ꍇ�̍����ƐF
	%cs = (
		name  => ['��ް����'],
		color => ['#CCCCCC'],
	);
	my $i = 1;
	open my $fh, "< $logdir/countries.cgi" or &error("���ް����ǂݍ��߂܂���");
	my $world_line = <$fh>;
	while (my $line = <$fh>) {
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$cs{$k}[$i] = $v;
		}
		++$i;
	}
	close $fh;
	
	# -------------------
	# Get %w
	%w  = ();
	$union = 0;
	for my $hash (split /<>/, $world_line) {
		my($k, $v) = split /;/, $hash;
		$w{$k} = $v;
		
		# �������������Ă��鍑�ɓ�����������Ȃ� $union �� set
		if ($k =~ /^p_(\d)_(\d)$/ && $v eq '1') {
			if ($m{country} eq $1) {
				$union = $2;
			}
			elsif ($m{country} eq $2) {
				$union = $1;
			}
		}
	}
	
	# -------------------
	# ���ꍑ�� �� ���������܂܂Ȃ����������̔z��쐬
	@contries = ();
	my $all_strong = 0;
	for my $i (1 .. $w{country}) {
		$all_strong += $cs{strong}[$i];
		push @countries, $cs{name}[$i];
	}
	$touitu_strong = int($all_strong * $w{game_lv} * 0.01);
	
	# -------------------
	# �������Ƒ��荑���p�ɂɎg���̂ŊȒP�ȕϐ���
	$c_m = $cs{name}[$m{country}];
	$c_y = $cs{name}[$y{country}];
	
	# ���ް��ǂݍ��ݐ���
	&error("���ް��̓ǂݍ��݂Ɏ��s���܂���") if $cs{name}[1] eq '';
}

#================================================
# �v���C���[�f�[�^�ǂݍ���
#================================================
sub read_user { # Get %m %y
	%m = ();
	%y = ();
	
	$id   = $in{id} || unpack 'H*', $in{login_name};
	$pass = $in{pass};
	
	open my $fh, "< $userdir/$id/user.cgi" or &error("���̂悤�Ȗ��O$in{login_name}����ڲ԰�����݂��܂���");
	my $line = <$fh>;
	close $fh;
	
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		
		if ($k =~ /^y_(.+)$/) {
			$y{$1} = $v;
		}
		else {
			$m{$k} = $v;
		}
	}
	&error('�߽ܰ�ނ��Ⴂ�܂�') unless $m{pass} eq $pass;
	
	# �S�����Ԃ�����ꍇ�A�o�ߎ��ԕ����炷
	$m{wt} -= ($time - $m{ltime}) if $m{wt} > 0;
	
	$m{money_limit} = $m{money};
	
	$m{cha_org} = $m{cha};
	
	$m{debug} = $line;
	
	&read_summer;
}

#==========================================================
# header�Ȃǈꎮ��� bj.cgi bbs_xxxx.cgi chat_xxxx.cgi�ȂǂŎg�p
#==========================================================
sub get_data {
	&decode;
	&header;
	&read_user;
	&access_check;
	&read_cs;
}

#================================================
# �������I�ǂ��ǂ���
#================================================
sub is_sabakan {
	for my $k ($admin_name, $admin_sub_name, $admin_support_name) {
		return 1 if $m{name} eq $k;
	}
	return 0;
}

#================================================
# ���������̑�\�҂��ǂ���
#================================================
sub is_daihyo {
	for my $k (qw/war dom pro mil ceo/) {
		return 1 if $m{name} eq $cs{$k}[$m{country}];
	}
	return 0;
}

#================================================
# ���������̌N�傩�ǂ���
#================================================
sub is_ceo {
	if ($m{name} eq $cs{ceo}[$m{country}]) {
		return 1;
	}
	return &is_sabakan;
}

#==========================================================
# ���̏�����Ԃ� 1_2,1_3�Ƃ��B(2_1̧�ق͑��݂��Ȃ��̂�)
#==========================================================
# &union(��1,��2); ���ď����Ǝ擾�ł����
sub union {
	my($country_1, $country_2) = @_;
	return $country_1 < $country_2 ? "${country_1}_${country_2}" : "${country_2}_${country_1}";
}

#==========================================================
# �莆�������ݏ��� letter.cgi marriage.cgi�Ŏg�p
#==========================================================
sub send_letter {
	my($name, $is_save_log) = @_;
	
	&error('�����̖��O������܂���') if $name eq '';
	my $send_id = unpack 'H*', $name;
	
	local $this_file = "$userdir/$send_id/letter";
	&error("$name�Ƃ�����ڲ԰�����݂��܂���") unless -f "$this_file.cgi";

	require './lib/_bbs_chat.cgi';
	&write_comment;
	
	# �莆��������׸ނ����Ă�
	my $letters = 0;
	if(-f "$userdir/$send_id/letter_flag.cgi"){
		open my $fh, "< $userdir/$send_id/letter_flag.cgi";
		my $line = <$fh>;
		($letters) = split /<>/, $line;
		close $fh;
	}
	$letters++;
	
	open my $fh, "> $userdir/$send_id/letter_flag.cgi";
	print $fh "$letters<>";
	close $fh;
	
	&send_letter_save_log($name) if $is_save_log eq '1';
}
# ------------------
# ���M����ۑ�
sub send_letter_save_log {
	my $name = shift;
	my @lines = ();
	open my $fh, "+< $userdir/$id/letter_log.cgi" ;
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, "$time<>$date<>$name<><><>$addr<>$in{comment}<><>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


#==========================================================
# ���̕��j�擾(���̈�����^����Ƃ��̍��̕��j����)
#==========================================================
sub get_countries_mes {
	my $country = shift;

	my @lines = ();
	open my $fh, "< $logdir/countries_mes.cgi" or &error("$logdir/countries_mes.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	close $fh;
	return $country ? $lines[$country] : @lines;
}


#================================================
# �f�R�[�h
#================================================
sub decode {
	local ($k,$v,$buf);
	my $err_flag = 0;

	if ($ENV{REQUEST_METHOD} eq 'POST') {
		&error('���e�ʂ��傫�����܂�',1) if $ENV{CONTENT_LENGTH} > 51200;
		read STDIN, $buf, $ENV{CONTENT_LENGTH};
	}
	else {
		&error('���e�ʂ��傫�����܂�',1) if length $ENV{QUERY_STRING} > 51200;
		$buf = $ENV{QUERY_STRING};
	}
	
	for my $pair (split /&/, $buf) {
		($k,$v) = split /=/, $pair;
		$v =~ tr/+/ /;
		$v =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack 'H2', $1/eg;

		# jcode.pl ���������h�~�p
		&jcode'convert(*v, 'sjis', 'sjis');#'

		# �L���u����
		$v =~ s/&/&amp/g;
		$v =~ s/;/&#59;/g;
		$v =~ s/&amp/&amp;/g;
		$v =~ s/,/&#44;/g;
		$v =~ s/</&lt;/g;
		$v =~ s/>/&gt;/g;
		$v =~ s/"/&quot;/g;#"
		$v =~ s/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]//g;
		$v =~ s/\.\.\///g;
		$v =~ s/�y�_�C�X�z/(�_�C�X)/g;
		
		# BBS�n�̏�������
		if ($k eq 'comment') {
			$v =~ s/\r\n/<br>/g;
			$v =~ s/\r/<br>/g;
			$v =~ s/\n/<br>/g;
			$v =~ s|�z�H�V|<font color="#FFD700">��</font>|g;
			$v =~ s|�I�D�v|<font color="#00FA9A">��</font>|g;
		}
		else {
			$v =~ tr/\x0D\x0A//d; # ���s�폜
		}

		$in{$k} = $v;
		
		push @delfiles, $v if $k eq 'delete';
	}
	$cmd = $in{cmd};
}

#================================================
# �������� Get $addr $host $agent
#================================================
sub access_check {
	$addr = $ENV{REMOTE_ADDR};
	$host = $ENV{REMOTE_HOST};
	
#	if ($gethostbyaddr && ($host eq '' || $host eq $addr)) {
#		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
#	}

	$host = $addr if $host eq '';

	for my $deny (@deny_lists) {
		$deny =~ s/\./\\\./g;
		$deny =~ s/\*/\.\*/g;
		
		if ($is_mobile) {
			&error($deny_message) if $agent =~ /$deny/;
		}
		else {
			&error($deny_message) if $addr =~ /^$deny$/i;
			&error($deny_message) if $host =~ /^$deny$/i;
		}
	}
	my $logging = 1;
	for my $nolog (@nolog_lists) {
		$nolog =~ s/\./\\\./g;
		$nolog =~ s/\*/\.\*/g;
		
		if ($is_mobile) {
			$logging = 0 if $agent =~ /$nolog/;
		}
		else {
			$logging = 0 if $addr =~ /^$nolog$/i;
			$logging = 0 if $host =~ /^$nolog$/i;
		}
	}
	
	if ($logging) {
		my $is_find = 0;
		if(-f "$userdir/$id/access_log.cgi"){
			open my $fh, "< $userdir/$id/access_log.cgi" or &error("���̂悤�Ȗ��O$in{login_name}����ڲ԰�����݂��܂���");
			while (my $line = <$fh>){
				my($access_addr, $access_host, $access_agent) = split /<>/, $line;
				if($is_mobile){
					if($access_agent eq $agent){
						$is_find = 1;
					}
				}else{
					if($access_addr eq $addr && $access_host eq $host && $access_agent eq $agent){
						$is_find = 1;
					}
				}
			}
			close $fh;
		}
		if(!$is_find && $id){
			open my $fh2, ">> $userdir/$id/access_log.cgi" or &error("���̂悤�Ȗ��O$in{login_name}����ڲ԰�����݂��܂���");
			print $fh2 "$addr<>$host<>$agent<>\n";
			close $fh2;
			
		}
	} else {
		$agent = 'admin_agent';
		$addr = '0.0.0.0';
		$host = 'admin_login';
	}
}

#================================================
# ���Ԏ擾 Get $time $date
#================================================
sub get_date {
	$time = time();
	my($min,$hour,$mday,$mon,$year) = (localtime($time))[1..4];
	$date = sprintf("%d/%d %02d:%02d", $mon+1,$mday,$hour,$min);
}

#================================================
# header
#================================================
sub header {
	print "Content-type: text/html; charset=Shift_JIS\n";
	if ($gzip ne '' && $ENV{HTTP_ACCEPT_ENCODING} =~ /gzip/){  
		if ($ENV{HTTP_ACCEPT_ENCODING} =~ /x-gzip/) {
			print "Content-encoding: x-gzip\n\n";
		}
		else{
			print "Content-encoding: gzip\n\n";
		}
		open STDOUT, "| $gzip -1 -c";
	}
	else {
		print "\n";
	}
	
	print qq|<html><head>|;
	print qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	unless ($is_mobile) {
		print qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|;
		print qq|<link rel="shortcut icon" href="$htmldir/favicon.ico">|;
		print qq|<link rel="stylesheet" type="text/css" href="$htmldir/bj.css?$jstime">|;
		print qq|<script type="text/javascript" src="$htmldir/nokori_time.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/jquery-1.11.1.min.js?$jstime"></script>\n|;
		print qq|<script type="text/javascript" src="$htmldir/js/bj.js?$jstime"></script>\n|;
	}
	print qq|<meta name="viewport" content="width=320, ">| if $is_smart;
	print qq|<title>$title</title>|;
	print qq|</head><body $body><a name="top"></a>|;
}
#================================================
# footer
#================================================
sub footer {
	print qq|<p><a href="#top">����</a></p>| if $is_mobile;
	print qq|<br><div align="right" style="font-size:11px">|;
	print qq|Blind Justice Ver$VERSION<br><a href="http://cgi-sweets.com/" target="_blank">CGI-Sweets</a><br><a href="http://amaraku.net/" target="_blank">Ama�y.net</a><br>|; # ����\��:�폜�E��\�� �֎~!!
	print qq|$copyright|;
	print qq|</div></body></html>|;
}

#==========================================================
# �G���[��ʕ\��
#==========================================================
sub error {
	my($error_mes, $is_need_header) = @_;
	
	&header if $is_need_header;
	print qq|<div class="mes">$error_mes<br><br></div>\n|;
	print qq|<form action="$script_index"><p><input type="submit" value="�s�n�o" class="button1"></p></form>|;
#	&cs_data_repair;
	&log_errors($error_mes);

	&footer;
	exit;
}

#=========================================================
# �N�b�L�[�擾
#=========================================================
sub get_cookie {
	my $cook = $ENV{HTTP_COOKIE};
	my %cooks;
	my @cooks;

	for my $pair (split /;/, $ENV{HTTP_COOKIE}) {
		my($k, $v) = split /=/, $pair;
		$k =~ s/\s//g;
		$cook{$k} = $v;
	}
	for my $c (split /<>/, $cook{bj}) {
		$c =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack 'H2', $1/eg;
		push @cooks, $c;
	}
	return @cooks;
}

#================================================
# �������Ă��镨�̌�
#================================================
sub my_goods_count {
	my $dir_path = shift;
	
	my $count = 0;
	opendir my $dh, $dir_path or &error("$dir_path�ިڸ�؂��J���܂���");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;
		++$count;
	}
	closedir $dh;
	
	return $count;
}

#================================================
# ��i�����َ擾
#================================================
sub get_goods_title {
	my $file_name = shift;
	my($file_base) = ($file_name =~ /^(.+)\.[^\.]+$/);
	return $file_base =~ /^_/ || $file_base eq '' ? $non_title : pack 'H*', $file_base;
}

#================================================
# ���t��time��(YYYY-MM-DD)
#================================================
sub date_to_time {
	my $date = shift;
	my ($year, $mon, $day) = ($date =~ /(\d{4})\-([01]\d)\-([0-3]\d)/);
	return timelocal(0, 0, 0, $day, $mon - 1, $year);
}

#================================================
# time����t��(YYYY-MM-DD)
#================================================
sub time_to_date {
	my $time2 = shift;
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($time2);
	$year += 1900;
	$mon++;
	return sprintf("%04d-%02d-%02d",$year,$mon,$mday);
}

#================================================
# ���M���O
#================================================
sub log_errors {
	my $text = shift;
	
	my $url = "http://" . $ENV{'HTTP_HOST'} . $ENV{'REQUEST_URI'};
	open my $fh, ">> ./log/error.cgi";
	print $fh "$text\n$url\n\n";
	close $fh;
}

#================================================
# ��ڲ԰�������N
#================================================
sub name_link {
	my $name = shift;
	
	my $id = unpack("H*", $name);
	return "<span data-id=\"$id\" class=\"namelink\">$name</span>";
}

#================================================
# ��ڲ԰���u��
#================================================
sub name_replace {
	$text = shift;
	
	my @names = ();
	open my $fh, "< $logdir/player_name_list.cgi";
	while (my $name = <$fh>) {
		chomp($name);
		if ($name) {
			push @names, $name;
		}
	}
	close $fh;
	
	for my $name (@names) {
		my @pre_links = ();
		while ($text =~ /^(.*?)(<a\s.*?>.*?<\/a>)(.*)$/) {
			$text = $1 . '__a_dummy__' . $3;
			push @pre_links, $2;
		}
		my @pre_tags = ();
		while ($text =~ /^(.*?)(<.*?>)(.*)$/) {
			$text = $1 . "__tag__" . $3;
			push @pre_tags, $2;
		}
		my $text_new = '';
		my $q_name = quotemeta $name;
		while ($text =~ /^(.*?)$q_name(.*)$/) {
			$text_new .= $1 . &name_link($name);
			$text = $2;
		}
		$text = $text_new . $text;
		while ($text =~ /^(.*?)__tag__(.*)$/) {
			my $tag = shift @pre_tags;
			$text = $1 . $tag . $2;
		}
		while ($text =~ /^(.*?)__a_dummy__(.*)$/) {
			my $a_tag = shift @pre_links;
			$text = $1 . $a_tag . $2;
		}
	}
	return $text;
}

#================================================
# ��ڲ԰���X�g�쐬
#================================================
sub make_player_name_list {
	my @lines = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		$name = pack 'H*', $id;
		push @lines, "$name\n";
	}
	closedir $dh;
	
	open my $fh, "> $logdir/player_name_list.cgi";
	print $fh @lines;
	close $fh;
}




1; # �폜�s��
