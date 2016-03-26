require './lib/_bbs_chat.cgi';
require './lib/_comment_tag.cgi';
require './lib/_auto_loader_js.cgi';
#================================================
# Chat Created by Merino
#================================================

# �A���������݋֎~����(�b)
$bad_time    = 5;

# �ő�۸ޕۑ�����
$max_log     = 60;

# �ő���Đ�(���p)
$max_comment = 200;

# ���ް�ɕ\������鎞��(�b)
$limit_member_time = 60 * 3;

# �����۰�ގ���
@reload_times = (0, 30, 60, 90, 120);


#================================================
sub run {
	if ($in{comment} && $m{silent_time} > $time) {
		if ($m{silent_kind} eq '0') {
			$in{comment} = '��[�I��[�I';
		} elsif ($m{silent_kind} eq '1') {
			$in{comment} = '̫��I';
		} elsif ($m{silent_kind} eq '2') {
			$in{comment} = '�ߩ�I';
		} elsif ($m{silent_kind} eq '3') {
			$in{comment} .= '�ۂۂۂہ[��';
		} elsif ($m{silent_kind} eq '4') {
			$in{comment} .= $m{silent_tail};
		}
	}
	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="����" class="button_s"><br>|;

	unless ($is_mobile) {
		print qq|�����۰��<select name="reload_time" class="select1"><option value="0">�Ȃ�|;
		for my $i (1 .. $#reload_times) {
			print $in{reload_time} eq $i ? qq|<option value="$i" selected>$reload_times[$i]�b| : qq|<option value="$i">$reload_times[$i]�b|;
		}
		print qq|</select>|;
		
		print qq|<span style="font-size:14px;">|;
		print qq|�@<span onClick="textset('�z�H�V')"><font color="#FFD700">��</font></span>|;
		print qq|�@<span onClick="textset('�I�D�v')"><font color="#00FA9A">��</font></span>|;
		print qq|�@<span onClick="textset('�n�@�g')"><font color="#FFB6C1">&hearts;</font></span>|;
		print qq|</span>|;
	}

	print qq|<div id="body_mes">|;
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		print qq|</form><font size="2">$member_c�l</font><hr>|;
	}else{
		print qq|</form><font size="2">$member_c�l:$member</font><hr>|;
	}
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		unless ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
			$bname .= "[$bshogo]" if $bshogo;
		}
		$bcomment = &comment_change($bcomment, 1);

		if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
			print qq|<font color="#ffffff">$bname�F$bcomment <font size="1">(�����Ȃ�: $bdate)</font></font><hr size="1">\n|;
		}else{
			print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
		}
	}
	close $fh;
	print qq|</div>|;
}


#================================================
# chat�pheader
#================================================
sub header {
	print qq|Content-type: text/html; charset=shift_jis\n\n|;
	print qq|<html><head>|;
	print qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	print qq|<meta name="viewport" content="width=320, ">| if $is_smart;
	print qq|<title>$title</title>|;
}

sub header2 {
	if ($is_mobile) {
		print qq|</head><body $body><a name="top"></a>|;
	}
	else {
		$auto_loader_head = &auto_loader($this_file);
		print <<"EOM";
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<link rel="stylesheet" type="text/css" href="$htmldir/bj.css">

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
</head>
<body $body>
EOM
	}
}

1; # �폜�s��
