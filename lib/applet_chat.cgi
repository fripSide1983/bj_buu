require './lib/_bbs_chat.cgi';
require './lib/_comment_tag.cgi';
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
#	if ($in{comment} && $m{silent_time} > $time) {
#		if($m{silent_kind} eq '0'){
#			$in{comment} = '��[�I��[�I' ;
#		}elsif($m{silent_kind} eq '1'){
#			$in{comment} = '̫��I' ;
#		}elsif($m{silent_kind} eq '2'){
#			$in{comment} = '�ߩ�I' ;
#		}else{
#			$in{comment} .= '�ۂۂۂہ[��' ;
#		}
#	}
#	&write_comment if ($in{mode} eq "write") && $in{comment};
	my($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		print qq|</form><font size="2">$member_c�l</font><hr>|;
	}else{
		print qq|</form><font size="2">$member_c�l:$member</font><hr>|;
	}
	print qq|<applet code="Chat.class" width="800" height="500">|;
	print qq|<param name=file_name value="$this_file">|;
	print qq|<param name=cgi_name value="$this_script">|;
	print qq|<param name=m_name value="$m{name}">|;
	print qq|<param name=m_id value="$id">|;
	print qq|<param name=m_pass value="$pass">|;
	print qq|</applet>|;
}


#================================================
# chat�pheader
#================================================
sub header {
	print qq|Content-type: text/html; charset=shift_jis\n\n|;
	print qq|<html><head>|;
	print qq|<meta http-equiv="Cache-Control" content="no-cache">|;
	print qq|<title>$title</title>|;

	if ($is_mobile) {
		print qq|</head><body $body><a name="top"></a>|;
	}
	else {
		if ($in{reload_time}) {
			print qq|<meta http-equiv="refresh" content="$reload_times[$in{reload_time}];URL=$this_script?id=$in{id}&pass=$in{pass}&reload_time=$in{reload_time}">|;
		}
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
</head>
<body $body onLoad="return textfocus()">
EOM
	}
}


1; # �폜�s��
