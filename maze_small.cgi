#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# Ҳ�CGI Created by Merino
#================================================
&decode;
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
function disp(url){
	if(!window.opener || window.opener.closed){
		window.alert('���C���E�B���h�E������܂���');
	}else{
		window.opener.location.href = url;
	}
}
-->
</script>
</head>
<body $body onLoad="return textfocus()">
EOM
}
&read_user;
&access_check;
&read_cs;
&error("��������ݽ���ł��B���΂炭���҂���������(�� $mente_min ����)") if $mente_min;

print qq|<table>|;

print qq|<tr><td>��</td>|;
print qq|<td><a href="maze_small.cgi?id=$id&pass=$pass&leader=$in{leader}" onclick="disp('chat_casino.cgi?id=$id&pass=$pass&mode=move&leader=$in{leader}&direction=0'); return false;">��</a></td>|;
print qq|<td>��</td></tr>|;

print qq|<tr>|;
print qq|<td><a href="maze_small.cgi?id=$id&pass=$pass&leader=$in{leader}" onclick="disp('chat_casino.cgi?id=$id&pass=$pass&mode=move&leader=$in{leader}&direction=3'); return false;">��</a></td>|;
print qq|<td><a href="maze_small.cgi?id=$id&pass=$pass&leader=$in{leader}" onclick="disp('chat_casino.cgi?id=$id&pass=$pass&mode=move&leader=$in{leader}&direction=2'); return false;">��</a></td>|;
print qq|<td><a href="maze_small.cgi?id=$id&pass=$pass&leader=$in{leader}" onclick="disp('chat_casino.cgi?id=$id&pass=$pass&mode=move&leader=$in{leader}&direction=1'); return false;">�E</a></td>|;
print qq|</tr>|;

print qq|</table>|;

&footer;

1;