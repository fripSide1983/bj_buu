#!/usr/local/bin/perl

#===========================================================
# jinro: Version 1 maziro  �ߋ����O�Q�Ɛ�p
#===========================================================

require './lib/jcode.pl';
require './config.cgi';
require './douke/lib_jinro.cgi';

#-[ �ݒ�J�n ]-----------------------------------------------------------

# �Q�[����
$sys_title = "�����̗a��";
# �摜�t�H���_
$imgpath = "./douke/img2/";
#CGI �p�X�t�@�C����
$cgi_path = "log_buu.cgi";
# �v���C���[�f�[�^�f�B���N�g��
$dat_dir = "./douke/playlog/";
# �v���C���[�f�[�^ �p�X�t�@�C���� (�g���q����)
$dat_path = "./douke/playlog/dat_buu";
# ���O�f�[�^ �p�X�t�@�C���� (�g���q����)
$log_path = "./douke/playlog/log_buu";
# �߂�p�X
$return_url = "chat_casino.cgi";
# ���b�N�t�@�C�� �p�X
$lock_path = "./douke/lock/jinro.loc";
# ID & PASSWORD
$sys_ID[1] = 'arum';
$sys_ID[2] = 'amam';
$sys_ID[3] = 'tott';
$sys_ID[4] = '0004';
$sys_ID[5] = '0005';
$sys_ID[6] = '0006';

$sys_pass[1] = 'pass';
$sys_pass[2] = '2222';
$sys_pass[3] = '3333';
$sys_pass[4] = '4444';
$sys_pass[5] = '5555';
$sys_pass[6] = '6666';

$sys_name[1] = '�����ԁ@���Y';
$sys_name[2] = '�J�{';
$sys_name[3] = '�Ƃ��Ƃ�';
$sys_name[4] = '�Ǘ��҂S��';
$sys_name[5] = '�Ǘ��҂T��';
$sys_name[6] = '�Ǘ��҂U��';

#�L�����N�^�[
$chr_hum = '���@�l';
$chr_wlf = '�l�@�T';
$chr_ura = '�肢�t';
$chr_nec = '��\��';
$chr_mad = '���@�l';
$chr_fre = '���L��';
$chr_bgd = '��@�l';
$chr_fox = '�d�@��';
$chr_rol = '�L�@��';

#-[ �ݒ�I�� ]-----------------------------------------------------------

$ENV{'TZ'} = "JST-9";

$wk_color[1] = "#DDDDDD";
$wk_color[2] = "#999999";
$wk_color[3] = "#FFFF33";
$wk_color[4] = "#FF9900";
$wk_color[5] = "#FF0000";
$wk_color[6] = "#99CCFF";
$wk_color[7] = "#0066FF";
$wk_color[8] = "#00EE00";
$wk_color[9] = "#CC00CC";
$wk_color[10] = "#FF9999";


# Japanese KANJI code
if (-f "jcode.pl") {
	$jflag = 1;
	require "jcode.pl";
	$code = ord(substr("��", 0, 1));
	if ($code == 0xb4) {
		$ccode = "euc";
	} elsif ($code == 0x1b) {
		$ccode = "jis";
	} else {
		$ccode = "sjis";
	}
}

&decode;
&read_user;
&read_cs;
$return_url .= "?id=$id&pass=$pass";

# File lock
foreach $i ( 1, 2, 3, 4, 5, 6 ) {
		if (mkdir($lock_path, 0755)) {
				last;
		} elsif ($i == 1) {
				($mtime) = (stat($lock_path))[9];
				if ($mtime < time() - 600) {
						rmdir($lock_path);
				}
		} elsif ($i < 6) {
				sleep(2);
		} else {
				&disp_head1;
				print "<H1>�t�@�C�����b�N</H1>\n";
				print "�ēx�A�N�Z�X���肢���܂��B<BR>\n";
				print "<A href='javascript:window.history.back()'>�߂�</A>\n";
				&disp_foot;
				exit(1);
		}
}

# Remove lockfile when terminated by signal
sub sigexit { rmdir($lock_path); exit(0); }
$SIG{'PIPE'} = $SIG{'INT'} = $SIG{'HUP'} = $SIG{'QUIT'} = $SIG{'TERM'} = "sigexit";

# Write current message. EDATA
($sec, $min, $hour, $mday, $mon, $year, $wday) = localtime(time);
	$date = sprintf("%02d/%02d-%02d:%02d",$mon + 1, $mday, $hour, $min);

$sys_loginflg = $in{'TXTLOGIN'};
$sys_plyerno  = 0;
if ($in{'TXTPNO'} ne ''){
	$sys_plyerno  = $in{'TXTPNO'};
}
$sys_village = $in{'VILLAGENO'};
$sys_logviewflg = 0;
$sys_storytype = $in{'STORYTYPE'};

# FileName
$cnt = sprintf("%06d",$sys_village);
$file_pdata = $dat_path.$cnt.".bak";
$tmp_pdata  = $dat_path.$cnt.".tmp";
$file_log   = $log_path.$cnt.".bak";
$tmp_log    = $log_path.$cnt.".tmp";

#cookie
if ($in{'COMMAND'} eq 'ENTER') {
	print &setCookie('SELECTROOM', $in{'VILLAGENO'});
}
if ($in{'COMMAND'} eq 'LOGIN') {
	print &setCookie('PLAYERNO'.$sys_village, $in{'CMBPLAYER'});
	print &setCookie('PASSWORD'.$sys_village, $in{'TXTPASS'});
}

print "Content-type: text/html\n";
print "\n";

# ***************************************************************** ���O�C���L��
if ($in{'TXTLOGIN'} ne '') {
	#--------------------------------------------------------------------- ���O�{��
	if ($in{'COMMAND'} eq 'LOGVIEW') {
		$sys_loginflg = '2';
		$sys_plyerno = 60;
		$sys_logviewflg = 1;
	}
	#=================================================================== ���O�C���n�j
	if ($sys_loginflg eq '2') {
		# ���݂̏�Ԃ��m�F
		if( open(IN, $file_pdata)){
			$wk_count = 0;
			while (<IN>) {
				$value = $_;
				$value =~ s/\n//g;
				$wk_count++;
				if ($wk_count == 1){
					@data_vildata = split(/,/, $value);
				}else{
					@wk_player = split(/,/, $value);
					for ($i = 0; $i <= 14; $i++) {
						$data_player[$wk_count-1][$i] = $wk_player[$i];
					}
				}
			}
		}else{
			print "<TR><TD>���t�@�C���I�[�v���G���[�F$file_pdata</TD></TR>\n";
		}
		close(IN);
		
		
		# [ HEAD ]
		&disp_head2;

		# [ PLAYER LIST ]
		&disp_players;

		# [ MY DATA ]
		&disp_mydata;
		
		if ($sys_logviewflg != 1 || $sys_storytype != "2"){
			print "<TR><TD class=\"CLSTD01\">�� �o����</TD></TR>\n";
			print "<TR><TD>\n";
			# [ ���t ]
			&disp_time(@data_vildata);
			print "<BR>\n";
			# [ �R�����g ]
			&disp_msg;
			print "</TD></TR>\n";
		}
		
		# [ �s���ݒ� ]
		&disp_command;
		
		# [ �R�����gdead ]
		&disp_msgdead;
		
		# [ ���O ]
		&disp_msgall;
		
	}
	
	print "</TD></TR>\n";
	print "<TR><TD class=\"CLSTD01\"><A href=\"$return_url\">�߂�</A>\n";
	print "<INPUT type=\"hidden\" name=\"TXTPNO\" value=\"$sys_plyerno\">";
	print "<INPUT type=\"hidden\" name=\"VILLAGENO\" value=\"$sys_village\">";
	print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"2\">";
	$wk_rnd = int(rand(1000000)) + 1;
	print "<INPUT type=\"hidden\" name=\"FORMID\" value=\"$wk_rnd\">";
	print "</TD></TR>\n";
} else {
	# ***************************************************************** ���O�C���Ȃ�
	
	&disp_head1;
	
	#�Q�Ƃ��郍�O��I�������ʂ�
	&disp_logview_back;
}

# [ FOOT ]
&disp_foot;

# Lock����
rmdir($lock_path);
