#!/usr/local/bin/perl --
use CGI::Carp qw(fatalsToBrowser);
require 'config.cgi';
require 'config_game.cgi';
require 'lib/_write_tag.cgi';
require './lib/_auto_loader_js.cgi';
require "$datadir/casino.cgi";

&decode;
&header1;
&read_user;
&access_check;
&read_cs;

if(defined $in{no}){
	$m{c_type} = int($in{no});
	$m{c_turn} = 0;
	$m{c_value} = 0;
	&write_user;
}
	$m{c_type} = int($m{c_type});

if($m{c_type} < 0 || $m{c_type} > $#files){
	$m{c_type} = 0;
	&write_user;
}

$this_title  = "$files[$m{c_type}][1]";
$this_file   = "$logdir/chat_casino$files[$m{c_type}][2]";
$this_script = 'chat_casino.cgi';

require "./lib/casino_$files[$m{c_type}][1].cgi";#run,get_member,etc

&header2;

# �ő�۸ޕۑ�����
$max_log     = 60;

# �ő���Đ�(���p)
$max_comment = 2000;

# ���ް�ɕ\������鎞��(�b)
$limit_member_time = 60;

# �����۰�ގ���
@reload_times = (0, 30, 60, 90, 120);

sub header1 {
	print qq|Content-type: text/html; charset=shift_jis\n\n|;
	print qq|<html><head>|;
	print qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	print qq|<title>$title</title>|;
}

sub header2 {
	my $auto_loader_head = '';
	if ($is_mobile) {
		print qq|</head><body $body><a name="top"></a>|;
	}
	else {
		if ($files[$m{c_type}][3]) {
			$auto_loader_head = &auto_loader($this_file, 1);
		}
		print <<"EOM";
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<link rel="stylesheet" type="text/css" href="$htmldir/bj.css?$jstime">
<link rel="stylesheet" type="text/css" href="$htmldir/themes/green/style.css">

<script language="JavaScript">
<!--
function textset(text){
	document.form.comment.value = document.form.comment.value + text;
}
function textfocus() {
	document.form.comment.focus();
	return true;
}
-->
</script>
<script type="text/javascript" src="$htmldir/jquery-1.11.1.min.js"></script>
$auto_loader_head
<script type="text/javascript" src="$htmldir/enchant.js"></script>
$enchant_game
</head>
<body $body>
EOM
	}
}

sub write_comment {
	&error('�{���ɉ���������Ă��܂���') if $in{comment} eq '';
	&error("�{�����������܂�(���p$max_comment�����܂�)") if length $in{comment} > $max_comment;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	
	# ����ݸ
	my $mname;
	($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 1);

	my $head_line = <$fh>;
	my ($htime,$hname,$hcomment) = (split /<>/, $head_line)[0,2,6];
	my ($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
	push @lines, $head_line;

	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	my $mshogo = length($m{shogo}) > 16 ? substr($m{shogo}, 0, 16) : $m{shogo};
	unshift @lines, "$time<>$date<>$mname<>$m{country}<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	return 1;
}

#=================================================

if(($m{c_turn} eq '0' || $m{c_turn} eq '') && ($in{mode} eq 'write' || $in{mode} eq '')){
	for my $i (0 .. $#files) {
		print $i eq $m{c_type} ? qq|$files[$i][0] / | : qq|<a href="?id=$id&pass=$pass&no=$i">$files[$i][0]</a> / |;
	}
}
print qq|<br>��݁F$m{coin}��|;
&run;
&footer;
exit;
