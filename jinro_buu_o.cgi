#!/usr/local/bin/perl --

#================================================================================
# jinro: Version 1 maziro
# ���� = clowning
# �a�� = prophecy
# 2005/03/14      ���l�o�^�����@�\��ǉ�
# 2005/03/19      �f�[�^�ƃ��O�t�@�C���̕ۑ����ύX
#                 �t�@�C�����ɕt����ԍ���O�[���t���U���ɕύX
#                 ���ꗗ�̎擾���@���f�B���N�g���̃t�@�C���ꗗ����擾������@�ɕύX
# 2005/03/20      �l�T�̏������ɐ����c���Ă��鑺�l���E���悤�ɏC��
#                 �A�C�R����ǉ�
# 2005/04/03      ���S�҂͑S���������Ŕs�҂Ƃ���
# 2005/06/12      �����̐��уL������ǉ��A�ő�Q�������Q�R�l��
#                 �A�C�R���ƊǗ��҂̈ꗗ���t�@�C����
#================================================================================

require './lib/jcode.pl';
require './config.cgi';
require './douke/lib_jinro.cgi';

#-[ �ݒ�J�n ]-----------------------------------------------------------

# �Q�[����
$sys_title = "�����̗a��";
# �摜�t�H���_
$imgpath = "./douke/img2/";
#CGI �p�X�t�@�C����
$cgi_path = "jinro_buu.cgi";

# �v���C���[�f�[�^�f�B���N�g��
$dat_dir = "./douke/playdata/";
# �v���C���[�f�[�^ �p�X�t�@�C���� (�g���q����)
$dat_path = "./douke/playdata/dat_buu";
# ���O�f�[�^ �p�X�t�@�C���� (�g���q����)
$log_path = "./douke/playdata/log_buu";
# �o�b�N�A�b�v �p�X�t�@�C���� (�g���q����)
$dat_path_bak = "./douke/playlog/dat_buu";
$log_path_bak = "./douke/playlog/log_buu";
#�Ǘ��ҏ��t�@�C��
$sys_path_bak = "./douke/sys_id.dat";
#�A�C�R�����t�@�C��
$ico_path_bak = "./douke/icon.dat";
# �߂�p�X
$return_url = "chat_casino.cgi";
# ���b�N�t�@�C�� �p�X
$lock_path = "./douke/lock/jinro.loc";

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
$wak_village =  sprintf("%06d",$sys_village);
$file_pdata = $dat_path.$wak_village.".dat";
$tmp_pdata  = $dat_path.$wak_village.".tmp";
$file_log	= $log_path.$wak_village.".dat";
$tmp_log	= $log_path.$wak_village.".tmp";

#cookie
if ($in{'COMMAND'} eq 'ENTER') {
	print &setCookie('SELECTROOM', $in{'VILLAGENO'});
}
if ($in{'COMMAND'} eq 'LOGIN') {
	print &setCookie('PLAYERNO'.$sys_village, $in{'CMBPLAYER'});
	print &setCookie('PASSWORD'.$sys_village, $in{'TXTPASS'});
}
if ($in{'COMMAND'} eq 'ENTRY') {
	print &setCookie('HN', $in{'TXTHN'});
	print &setCookie('MAILADRES', $in{'TXTMAIL'});
}
print "Content-type: text/html\n";
print "\n";

# ***************************************************************** ���O�C���L��
if ($in{'TXTLOGIN'} ne '') {
	# =================================================================== �����O�C�� 
	if ($sys_loginflg eq '1') {
		#--------------------------------------------------------------------- �G���g���[���� 
		if ($in{'COMMAND'} eq 'ENTRY') {
			$wk_entryflg = 0;
			if ($in{'TXTNAME'} ne '' && $in{'CMBICON'} ne '') {
				# �o�^�������l�̏����f�[�^�t�@�C���֏�������
				open(IN, $file_pdata);
				$wk_count = 0;
				while (<IN>) {
					$value = $_;
					$value =~ s/\n//g;
					$wk_count++;
					if ($wk_count == 1){
						@data_vildata = split(/,/, $value);
						$data_no = $data_vildata[1];
					}else{
						$data_player[$wk_count-1] = $value;
					}
				}
				close(IN);

				if ($data_vildata[0] >= 1) {
					$wk_entryflg = 2;
				}elsif ($data_vildata[1] >= 23){
					$wk_entryflg = 3;
				}else{
					#WRITE
					$data_no++;
					# 0:NO , 1:ALIVE/DEAD , 2:VOTE , 3:JOB , 4:JOBwk , 5:WinLose , 6:COLOR , 7:NAME , 8:HN , 9:silent , 10:date, 11:ICON
					$data_player[$data_no] = $data_no.',A,0,NON,0,-,'.$in{'CMBCOLOR'}.','.$in{'TXTNAME'}.','.$m{name}.',0,'.$date.','.$in{'CMBICON'};
					open(OUT, "> ".$file_pdata);
					$data_vildata[1] = $data_no;
					# 0:GAMESTART , 1:PLAYERNO , 2:DATE , 3:FAZE , 4:TIME , 5:VILNAME , 6:FORMID , 7:�Ǘ��҂h�c , 8:RULE , 9:PASTTIME
					print OUT "$data_vildata[0],$data_vildata[1],$data_vildata[2],$data_vildata[3],$data_vildata[4],$data_vildata[5],$data_vildata[6],$data_vildata[7],$data_vildata[8],$data_vildata[9]\n";
					for ($i = 1; $i <= $data_no; $i++) {
						print OUT "$data_player[$i]\n";
					}
					close(OUT);
					&msg_write(0, 1, 31,"�u<b>$in{'TXTNAME'}</b>����v�����ւ���Ă��܂����B");
					$wk_entryflg = 1;
				}
			}
			# Print HTML document
			&disp_head1;
			print "<TR><TD>\n";
			if($wk_entryflg == 1){
				print "�A�i�^��$data_no�l�ڂ̑����Ƃ��ēo�^���������܂����B\n";
				$in{'COMMAND'} = 'LOGIN';
				$in{'CMBPLAYER'} = $data_no;
			}elsif($wk_entryflg == 2){
				print "�\\���󂠂�܂���B���ɃQ�[�����J�n���Ă��܂��B\n";
			}elsif($wk_entryflg == 3){
				print "�\\���󂠂�܂���B���ɂQ�Q���o�^����Ă��܂��B\n";
			}else{
				print "���͍��ڂ�����������܂���B\n";
			}
			print "</TD></TR>\n";
		}
		#--------------------------------------------------------------------- ���O�C������
		if ($in{'COMMAND'} eq 'LOGIN') {
			$wk_loginflg = 0;
			$wk_count = 0;
			$user_no = 1;
			if ($in{'CMBPLAYER'} == 0){
				#���l�̑��փ��O�C������
				$wk_loginflg = 1;
				$sys_loginflg = '2';
				$sys_plyerno = 60;
			}elsif ($in{'CMBPLAYER'} <= 23){
				#�v���C���[�̑��փ��O�C������
				open(IN, $file_pdata);
				while (<IN>) {
					$wk_count++;
					$value = $_;
					$value =~ s/\n//g;
					@wk_player = split(/,/, $value);
					if ($wk_count > 1){
						if ($wk_player[0] == $in{'CMBPLAYER'}){
							if ($wk_player[8] eq $m{name}){
								$wk_loginflg = 1;
								$sys_loginflg = '2';
								$sys_plyerno = $in{'CMBPLAYER'};
							}else{
								$wk_loginflg = 9;
							}
						}
					}
				}
				close(IN);
			}elsif ($in{'CMBPLAYER'} == 99){
				#���֊Ǘ��҃��O�C��
				open(IN, $file_pdata);
				while (<IN>) {
					$wk_count++;
					$value = $_;
					$value =~ s/\n//g;
					@wk_player = split(/,/, $value);
					if ($wk_count == 1){
						$user_no = @wk_player[7];
					}
				}
				close(IN);
				
				&sysadoin;
				if ($m{name} eq $sys_ID[$user_no]) {
					$wk_loginflg = 1;
					$sys_loginflg = '2';
					$sys_plyerno = 50;
				}else{
					$wk_loginflg = 9;
				}
			}
			# Print HTML document
			if($wk_loginflg != 1){
				&disp_head1;
				if ($user_no == 0){
					print "$data_vildata[7]���ݒ肳��Ă��܂���B\n";
				}
				print "�p�X���[�h������������܂���B\n";
			}
		}
		#--------------------------------------------------------------------- ���O�{��
		if ($in{'COMMAND'} eq 'LOGVIEW') {
			$sys_loginflg = '2';
			$sys_plyerno = 60;
			$sys_logviewflg = 1;
		}
	}
	#=================================================================== ���O�C���n�j
	if ($sys_loginflg eq '2') {

		# ���݂̏�Ԃ��m�F
		open(IN, $file_pdata);
		$wk_count = 0;
		while (<IN>) {
			$value = $_;
			$value =~ s/\n//g;
			$wk_count++;
			if ($wk_count == 1){
				@data_vildata = split(/,/, $value);
			}else{
				@wk_player = split(/,/, $value);
				for ($i = 0; $i <= 11; $i++) {
					$data_player[$wk_count-1][$i] = $wk_player[$i];
				}
			}
		}
		close(IN);
		
		$wk_txtmsg1 = '';
		$wk_txtmsg2 = '';
		$wk_txtmsglen = 0;
		if ($in{'comment'} ne '') {
#			$in{'comment'} =~ s/\r*\x00/\x00/g;
#			$in{'comment'} =~ s/\n*\x00//g;
			$in{'comment'} =~ s/,//g;
			$wk_txtmsg1 = $in{'comment'};
			$wk_txtmsg2 = $in{'comment'};
			$wk_txtmsg2 =~ s/[\n\r]/<br>/g;
			$wk_txtmsglen = length($in{'comment'});
		}

		$data_player[$sys_plyerno][10] = $date;

		#2�d���e�h�~
		if ($data_vildata[6] == $in{'FORMID'}) {
			$in{'COMMAND'} = '';
		}
		$data_vildata[6] = $in{'FORMID'};
		
		#=================================================================== �J�n�O
		if($data_vildata[0]==0){
			#--------------------------------------------------------------------- �J�n
			if (($in{'COMMAND'} eq 'START' || $in{'COMMAND'} eq 'STARTF') && $data_vildata[1] >= 8) {
				#WRITE
				for ($i = 1; $i <= 23; $i++) {
					$wk_charactor[$i] = 'HUM';
				}
				$wk_charactor[2] = 'WLF';
				$wk_charactor[3] = 'WLF';
				$wk_charactor[4] = 'URA';
				if($data_vildata[1] >= 16){
					$wk_charactor[5] = 'WLF';
				}
				if($data_vildata[1] >= 9){
					$wk_charactor[6] = 'NEC';
				}
				if($data_vildata[1] >= 10){
					$wk_charactor[7] = 'MAD';
				}
				if($data_vildata[1] >= 11){
					$wk_charactor[8] = 'BGD';
				}
				if($data_vildata[1] >= 13){
					$wk_charactor[9] = 'FRE';
					$wk_charactor[10] = 'FRE';
				}
				if($data_vildata[1] >= 20){
					$wk_charactor[19] = 'WLF';
					$wk_charactor[20] = 'ROL';
				}
				if($data_vildata[1] >= 15 && $in{'COMMAND'} eq 'STARTF'){
					$wk_charactor[11] = 'FOX';
				}
				for ($i = 2; $i <= $data_vildata[1]; $i++) {
					$wk_rnd = int(rand($data_vildata[1] - $i + 1)) + 1;
					$data_player[$i][3] = $wk_charactor[$wk_rnd];
					for ($i2 = $wk_rnd; $i2 <= $data_vildata[1]; $i2++) {
						$wk_charactor[$i2] = $wk_charactor[$i2+1];
					}
				}
				$data_vildata[0] = 1;
				$data_vildata[2] = 1;
				$data_vildata[3] = 2;
				$data_vildata[4] = 0;
				$data_vildata[9] = $time;
	
				# Print HTML document
				&msg_write(1, 50, 32,"<FONT size=\"+1\">�P���ڂ̖�ƂȂ�܂����B</FONT>");
			}
			#--------------------------------------------------------------------- ���b�Z�[�W
			if (($in{'COMMAND'} eq 'MSG' || $in{'COMMAND'} eq 'MSG2' || $in{'COMMAND'} eq 'MSG3') && $wk_txtmsg1 ne '') {
				$wk_fonttag1 = "";
				$wk_fonttag2 = "";

				# [ msg write ]
				if ($in{'COMMAND'} eq 'MSG2'){
					$wk_fonttag1 = "<FONT size=\"+1\">";
					$wk_fonttag2 = "</FONT>";
				}
				if ($in{'COMMAND'} eq 'MSG3'){
					$wk_fonttag1 = "<FONT size=\"-1\">";
					$wk_fonttag2 = "</FONT>";
				}
				&msg_write(0, 1, $sys_plyerno, $wk_fonttag1.$wk_txtmsg2.$wk_fonttag2);
			}
			#--------------------------------------------------------------------- ���O�ύX
			if ($in{'COMMAND'} eq 'NAMECHG' && $wk_txtmsg1 ne '') {
				if ($wk_txtmsglen <= 20){
					$data_player[$sys_plyerno][7] = $wk_txtmsg1;
				}
			}
			#--------------------------------------------------------------------- �����ύX
			if ($in{'COMMAND'} eq 'VILNAME' && $wk_txtmsg1 ne '') {
				if ($wk_txtmsglen <= 16){
					$data_vildata[5] = $wk_txtmsg1;
				}
			}
			#--------------------------------------------------------------------- ���[���ύX
			if ($in{'COMMAND'} eq 'VILRULE' && $wk_txtmsg1 ne '') {
				if ($wk_txtmsglen =~ /^[0-9]$/){
					$rule_number = int($wk_txtmsg1);
					$data_vildata[8] = $rule_number if ($rule_number >= 0 && $rule_number < @limit_times);
				}
			}
			#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
			if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
				# [ msg write ]
				&msg_write(0, 1, 23, $wk_txtmsg2);
			}
			#--------------------------------------------------------------------- ���l�o�^��������
			if ($in{'COMMAND'} eq 'PLEYERDEL') {
				open(IN, $file_pdata);
				$wk_count = 0;
				while (<IN>) {
					$value = $_;
					$value =~ s/\n//g;
					$wk_count++;
					if ($wk_count == 1){
						@data_vildata = split(/,/, $value);
					}else{
						@wk_player = split(/,/, $value);
						if ($in{'CMBPLAYER'} == $wk_player[0]){
							#�폜���鑺�l�̍s���΂�
							$wk_CMBPLAYER = $data_player[$in{'CMBPLAYER'}][7];
							$wk_count--;
						}else{
							$data_player[$wk_count-1][0] = $wk_count - 1;
							for ($i = 1; $i <= 11; $i++) {
								 $data_player[$wk_count-1][$i] = $wk_player[$i];
							}
						}
					}
				}
				close(IN);
				#���l�̐l������l���炷
				$data_vildata[1] = $data_vildata[1] - 1;
				&data_write;
				&msg_write($data_vildata[2], 2, 34,"<b>$wk_CMBPLAYER</b>�����<FONT color=\"#ff0000\">���l�̓o�^�𖕏�����܂����B</FONT>");
				&msg_write($data_vildata[2], 2, 34,"<b><FONT color=\"#ff0000\">�f�[�^���ύX���ꂽ�̂őS��������x���O�C�����Ȃ����Ă��������B</FONT>");
			}
		}
		#=================================================================== �n�m�o�k�`�x�I
		if($data_vildata[0]==1){# �Q�[�����t���O
			if($data_vildata[8] != 0){
				$data_vildata[4] += $time - $data_vildata[9];
				$data_vildata[9] = $time;
			}
			#--------------------------------------------------------------------- [ �� ]
			if($data_vildata[3] == 1){# ��
				if($data_vildata[8] == 1){
					if($data_vildata[4] >= $limit_times[$data_vildata[8]][0]){
						$data_vildata[4] = 0;
						$data_vildata[3] = 3
					}
				}
				#--------------------------------------------------------------------- ���b�Z�[�W
				if (($in{'COMMAND'} eq 'MSG' || $in{'COMMAND'} eq 'MSG2' || $in{'COMMAND'} eq 'MSG3') && $wk_txtmsg1 ne '' && $data_vildata[4] < $limit_times[$data_vildata[8]][0]) {
					if($data_vildata[8] == 0){
						if ($wk_txtmsglen <= 100){
							$data_vildata[4] += 15;
						}elsif ($wk_txtmsglen <= 200){
							$data_vildata[4] += 30;
						}elsif ($wk_txtmsglen <= 300){
							$data_vildata[4] += 45;
						}elsif ($wk_txtmsglen <= 400){
							$data_vildata[4] += 60;
						}elsif ($wk_txtmsglen <= 500){
							$data_vildata[4] += 75;
						}elsif ($wk_txtmsglen <= 600){
							$data_vildata[4] += 90;
						}elsif ($wk_txtmsglen <= 700){
							$data_vildata[4] += 105;
						}else{
							$data_vildata[4] += 120;
						}
						if ($data_vildata[4] >= $limit_times[0][0]){
							$data_vildata[4] = $limit_times[0][0];
						}
					}

					$wk_fonttag1 = "";
					$wk_fonttag2 = "";
					# [ msg write ]
					if ($in{'COMMAND'} eq 'MSG2'){
						$wk_fonttag1 = "<FONT size=\"+1\">";
						$wk_fonttag2 = "</FONT>";
					}
					if ($in{'COMMAND'} eq 'MSG3'){
						$wk_fonttag1 = "<FONT size=\"-1\">";
						$wk_fonttag2 = "</FONT>";
					}
					&msg_write($data_vildata[2], 1, $sys_plyerno, $wk_fonttag1.$wk_txtmsg2.$wk_fonttag2);
				}
				#--------------------------------------------------------------------- �� �b
				if ($in{'COMMAND'} eq 'MSG0' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 1, 23, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'MSGM0'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, 23, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- ����
				if ($in{'COMMAND'} eq 'SILENT') {
					$data_player[$sys_plyerno][9] = 1;
					# ����
					$wk_cnt_live	= 0;
					$wk_cnt_silent = 0;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if ($data_player[$i][1] eq 'A'){
							$wk_cnt_live++;
							if ($data_player[$i][9] == 1) {
								$wk_cnt_silent++;
							}
						}
					}
					# ���� ����
					if(int($wk_cnt_live / 2) < $wk_cnt_silent){
						$data_vildata[4] += 60;
						if ($data_vildata[4] >= $limit_times[$data_vildata[8]][0]){
							$data_vildata[4] = $limit_times[$data_vildata[8]][0];
						}
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							$data_player[$i][9] = 0;
						}
						&msg_write($data_vildata[2], 1, 24, '�u�E�E�E�E�E�E�B�v�P���Ԃقǂ̒��ق��������B');
					}
				}
				#--------------------------------------------------------------------- ���[
				if (($in{'COMMAND'} eq 'VOTE' && $data_player[$sys_plyerno][2] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') || $in{'COMMAND'} eq 'VOTECHK') {
					if ($in{'COMMAND'} eq 'VOTE'){
						$data_player[$sys_plyerno][2] = $in{'CMBPLAYER'};
					}
					# ���[����
					$wk_voteflg = 1;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						$wk_votecount[$i] = 0;
					}
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if ($data_player[$i][2] != 0 && $data_player[$i][1] eq 'A'){
							$wk_votecount[$data_player[$i][2]]++;
						}
						if ($data_player[$i][2] == 0 && $data_player[$i][1] eq 'A') {
							$wk_voteflg = 0;
						}
					}

					if ($wk_voteflg == 1){
						$wk_topvote = 1;
						$wk_votetable = "<TABLE>";
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][1] eq 'A'){
								$wk_votetable = $wk_votetable."<TR><TD><b>$data_player[$i][7]</b>����</TD><TD>$wk_votecount[$i] �[</TD><TD>���[�� �� <b>$data_player[$data_player[$i][2]][7]</b>����</TD></TR>";
								if ($wk_votecount[$wk_topvote] < $wk_votecount[$i]){
									$wk_topvote = $i;
								}
							}
						}
						$wk_votetable = $wk_votetable."</TABLE>";
						&msg_write($data_vildata[2], 2, 0,"$wk_votetable");
						&msg_write($data_vildata[2], 2, 0,"<BR><FONT size=\"+1\">$data_vildata[2]���� ���[���ʁB</FONT>");
						$wk_topvotecheck = 0;
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($wk_votecount[$wk_topvote] == $wk_votecount[$i]){
								$wk_topvotecheck++;
							}
						}
						if ($wk_topvotecheck == 1){
							# ���[�I���A��Ԃ̐l�����Y����
							$data_vildata[3] = 2;
							$data_vildata[4] = 24;
							$data_vildata[9] = $time;
							$data_player[$wk_topvote][1] = 'D';
							# �L���̓��A��
							if ($data_player[$wk_topvote][3] eq 'ROL') {
								#�����Ă���l�����l�I��  *����ׂ���Ȃ��ˁH
								for ($i = 1; $i <= $data_vildata[1]; $i++) {
									 if ($data_player[$i][1] eq 'A') {
										 $wk_targezibaku = $i;
									 }
								}
								$data_player[$wk_targezibaku][1] = 'D';
							}else{
								$wk_targezibaku = 99;
							}
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								$data_player[$i][2] = 0;
								$data_player[$i][9] = 0;
								if ($data_player[$i][3] eq 'NEC' && $data_player[$i][1] eq 'A' && $data_vildata[2]>=2) {
									$data_player[$i][4] = $wk_topvote;
								}
								if ($data_player[$i][3] eq 'URA') {
									$data_player[$i][4] = 0;
								}
							}
							if ($data_vildata[0] == 1) {
								&msg_write($data_vildata[2], 2, 33,"<b>$data_player[$wk_topvote][7]</b>����͑������c�̌���<FONT color=\"#ff0000\">���Y����܂����E�E�E�B</FONT>");
								if ($wk_targezibaku != 99) {
									&msg_write($data_vildata[2], 2, 35,"<b>$data_player[$wk_targezibaku][7]</b>����͔L���ɓ��A��ɂ����<FONT color=\"#ff0000\">���S���܂����E�E�E�B</FONT>");
								}
							}
							
							# [ �������� ]
							&sub_judge;
							
							if ($data_vildata[0] == 1) {
								&msg_write($data_vildata[2], 50, 32,"<FONT size=\"+1\">$data_vildata[2]���ڂ̖�ƂȂ�܂����B</FONT>");
							}
						}else{
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								$data_player[$i][2] = 0;
							}
							&msg_write($data_vildata[2], 2, 31,"<FONT size=\"+1\">�ē��[�ƂȂ�܂����B</FONT>");
						}
					}
				}
				#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'SHOCK' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$in{'CMBPLAYER'}][1] = 'D';
					&msg_write($data_vildata[2], 1, 34,"<b>$data_player[$in{'CMBPLAYER'}][7]</b>����͓s���ɂ��<FONT color=\"#ff0000\">�ˑR�����܂����E�E�E�B</FONT>");
				}
				#--------------------------------------------------------------------- �ē��[
				if ($in{'COMMAND'} eq 'REVOTE') {
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						$data_player[$i][2] = 0;
					}
					$data_vildata[4] = 0;
					&msg_write($data_vildata[2], 2, 31,"<FONT size=\"+1\">�ē��[�ƂȂ�܂����B</FONT>");
				}
			}
			#--------------------------------------------------------------------- [ �� ���[�҂� ]
			if($data_vildata[3] == 3){# ��
				if($data_vildata[8] == 1){
					if($data_vildata[4] >= $limit_times[$data_vildata[8]][2]){
						$data_vildata[4] = 0;
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][1] eq 'A' && $data_player[$i][2] == 0) {
								$data_player[$i][1] = 'D';
								&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$i][7]</b>����͓s���ɂ��<FONT color=\"#ff0000\">�ˑR�����܂����E�E�E�B</FONT>");
							}
						}
						$in{'COMMAND'} = 'VOTECHK';
					}
				}
				#--------------------------------------------------------------------- �� �b
				if ($in{'COMMAND'} eq 'MSG0' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 1, 23, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'MSGM0'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, 23, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- ���[
				if (($in{'COMMAND'} eq 'VOTE' && $data_player[$sys_plyerno][2] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') || $in{'COMMAND'} eq 'VOTECHK') {
					if ($in{'COMMAND'} eq 'VOTE'){
						$data_player[$sys_plyerno][2] = $in{'CMBPLAYER'};
					}
					# ���[����
					$wk_voteflg = 1;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						$wk_votecount[$i] = 0;
					}
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if ($data_player[$i][2] != 0 && $data_player[$i][1] eq 'A'){
							$wk_votecount[$data_player[$i][2]]++;
						}
						if ($data_player[$i][2] == 0 && $data_player[$i][1] eq 'A') {
							$wk_voteflg = 0;
						}
					}

					if ($wk_voteflg == 1){
						$wk_topvote = 1;
						$wk_votetable = "<TABLE>";
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][1] eq 'A'){
								$wk_votetable = $wk_votetable."<TR><TD><b>$data_player[$i][7]</b>����</TD><TD>$wk_votecount[$i] �[</TD><TD>���[�� �� <b>$data_player[$data_player[$i][2]][7]</b>����</TD></TR>";
								if ($wk_votecount[$wk_topvote] < $wk_votecount[$i]){
									$wk_topvote = $i;
								}
							}
						}
						$wk_votetable = $wk_votetable."</TABLE>";
						&msg_write($data_vildata[2], 2, 0,"$wk_votetable");
						&msg_write($data_vildata[2], 2, 0,"<BR><FONT size=\"+1\">$data_vildata[2]���� ���[���ʁB</FONT>");
						$wk_topvotecheck = 0;
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($wk_votecount[$wk_topvote] == $wk_votecount[$i]){
								$wk_topvotecheck++;
							}
						}
						if ($wk_topvotecheck == 1){
							# ���[�I���A��Ԃ̐l�����Y����
							$data_vildata[3] = 2;
							$data_vildata[4] = 24;
							$data_vildata[9] = $time;
							$data_player[$wk_topvote][1] = 'D';
							# �L���̓��A��
							if ($data_player[$wk_topvote][3] eq 'ROL') {
								#�����Ă���l�����l�I��  *����ׂ���Ȃ��ˁH
								for ($i = 1; $i <= $data_vildata[1]; $i++) {
									 if ($data_player[$i][1] eq 'A') {
										 $wk_targezibaku = $i;
									 }
								}
								$data_player[$wk_targezibaku][1] = 'D';
							}else{
								$wk_targezibaku = 99;
							}
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								$data_player[$i][2] = 0;
								$data_player[$i][9] = 0;
								if ($data_player[$i][3] eq 'NEC' && $data_player[$i][1] eq 'A' && $data_vildata[2]>=2) {
									$data_player[$i][4] = $wk_topvote;
								}
								if ($data_player[$i][3] eq 'URA') {
									$data_player[$i][4] = 0;
								}
							}
							if ($data_vildata[0] == 1) {
								&msg_write($data_vildata[2], 2, 33,"<b>$data_player[$wk_topvote][7]</b>����͑������c�̌���<FONT color=\"#ff0000\">���Y����܂����E�E�E�B</FONT>");
								if ($wk_targezibaku != 99) {
									&msg_write($data_vildata[2], 2, 35,"<b>$data_player[$wk_targezibaku][7]</b>����͔L���ɓ��A��ɂ����<FONT color=\"#ff0000\">���S���܂����E�E�E�B</FONT>");
								}
							}
							
							# [ �������� ]
							&sub_judge;
							
							if ($data_vildata[0] == 1) {
								&msg_write($data_vildata[2], 50, 32,"<FONT size=\"+1\">$data_vildata[2]���ڂ̖�ƂȂ�܂����B</FONT>");
							}
						}else{
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								$data_player[$i][2] = 0;
							}
							$data_vildata[4] = 0;
							&msg_write($data_vildata[2], 2, 31,"<FONT size=\"+1\">�ē��[�ƂȂ�܂����B</FONT>");
						}
					}
				}
				#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'SHOCK' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$in{'CMBPLAYER'}][1] = 'D';
					&msg_write($data_vildata[2], 1, 34,"<b>$data_player[$in{'CMBPLAYER'}][7]</b>����͓s���ɂ��<FONT color=\"#ff0000\">�ˑR�����܂����E�E�E�B</FONT>");
				}
				#--------------------------------------------------------------------- �ē��[
				if ($in{'COMMAND'} eq 'REVOTE') {
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						$data_player[$i][2] = 0;
					}
					$data_vildata[4] = 0;
					&msg_write($data_vildata[2], 2, 31,"<FONT size=\"+1\">�ē��[�ƂȂ�܂����B</FONT>");
				}
			}
			#--------------------------------------------------------------------- [ �� ]
			if($data_vildata[3] == 2){# ��̎��Ԓ���
				if($data_vildata[8] == 1){
					if($data_vildata[4] >= $limit_times[$data_vildata[8]][1]){
						$data_vildata[4] = 0;
						$data_vildata[3] = 4;
					}
				}
				#-------------------------- ���i��
				if ($in{'COMMAND'} eq 'MSGWLF' && $wk_txtmsg1 ne '' && $data_vildata[4] < $limit_times[$data_vildata[8]][1]) {
					if($data_vildata[8] == 0){
						if ($wk_txtmsglen <= 100){
							$data_vildata[4] += 15;
						}elsif ($wk_txtmsglen <= 200){
							$data_vildata[4] += 30;
						}elsif ($wk_txtmsglen <= 300){
							$data_vildata[4] += 45;
						}else{
							$data_vildata[4] += 60;
						}
						if ($data_vildata[4] >= $limit_times[0][0]){
							$data_vildata[4] = $limit_times[0][0];
						}
					}
					# [ msg write ]
					&msg_write($data_vildata[2], 3, $sys_plyerno, $wk_txtmsg2);
				}
				#-------------------------- �E�Q�\��
				if($data_vildata[2] >= 2){
					if ($in{'COMMAND'} eq 'KILL' && $data_player[$in{'CMBPLAYER'}][3] ne 'WLF' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][3] eq 'WLF') {
								$data_player[$i][4] = $in{'CMBPLAYER'};
							}
						}
						&msg_write($data_vildata[2], 11, 42,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>�����_���܂��B");
					}
				}else{
					if ($in{'COMMAND'} eq 'KILL' && $data_player[$in{'CMBPLAYER'}][3] ne 'WLF' && $data_player[$in{'CMBPLAYER'}][1] eq 'A' && $in{'CMBPLAYER'} == 1) {
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][3] eq 'WLF') {
								$data_player[$i][4] = $in{'CMBPLAYER'};
							}
						}
						&msg_write($data_vildata[2], 11, 42,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>�����_���܂��B");
					}
				}
				#-------------------------- �肢�t
				if ($in{'COMMAND'} eq 'FORTUNE' && $data_player[$sys_plyerno][4] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$sys_plyerno][4] = $in{'CMBPLAYER'};
					&msg_write($data_vildata[2], 12, 43,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>�����肢�܂��B");
				}
				#-------------------------- ��l
				if ($in{'COMMAND'} eq 'GUARD' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$sys_plyerno][4] = $in{'CMBPLAYER'};
					&msg_write($data_vildata[2], 13, 44,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>�������q���܂��B");
				}
				
				#--------------------------- �Ƃ茾
				if ($in{'COMMAND'} eq 'MSG1' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 5, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------- �� �b
				if ($in{'COMMAND'} eq 'MSG0' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 2, 23, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'MSGM0'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, 23, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- ��I������
				if ($in{'COMMAND'} ne '') {
					$wk_nightend = 1;
					$wk_targetwlf = 0;
					$wk_targetura = 0;
					$wk_targetbgd = 0;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if ($data_player[$i][1] eq 'A') {
							if ($data_player[$i][3] eq 'WLF'){
								$wk_targetwlf = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
							if ($data_player[$i][3] eq 'URA') {
								$wk_targetura = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
							if ($data_player[$i][3] eq 'BGD' && $data_vildata[2] >= 2) {
								$wk_targetbgd = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
						}
					}
					if ($wk_nightend == 1) {
						# ��q�Ȃ��ŗd�ǈȊO�Ȃ�l�T�ɎE�Q�����
						if ($wk_targetwlf != $wk_targetbgd && $data_player[$wk_targetwlf][3] ne 'FOX') {
							$data_player[$wk_targetwlf][1] = 'D';
							&msg_write($data_vildata[2], 4, 34,"<b>$data_player[$wk_targetwlf][7]</b>����͗���<FONT color=\"#ff0000\">���c�Ȏp�Ŕ������ꂽ�E�E�E�B</FONT>");
						}
						# �d�ǂ��肢���ꂽ������
						if ($data_player[$wk_targetura][3] eq 'FOX') {
							$data_player[$wk_targetura][1] = 'D';
							&msg_write($data_vildata[2], 4, 34,"<b>$data_player[$wk_targetura][7]</b>����͗���<FONT color=\"#ff0000\">���c�Ȏp�Ŕ������ꂽ�E�E�E�B</FONT>");
						}
						#�L�����l�T�𓹘A��
						if ($wk_targetwlf != $wk_targetbgd && $data_player[$wk_targetwlf][3] eq 'ROL') {
							#�����Ă���l�T�̒������l��I�� *�킩�߂ĎI�ƈႤ
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								if ($data_player[$i][1] eq 'A'){
									if ($data_player[$i][3] eq 'WLF'){
										$wk_targezibaku = $i;
									}
								}
							}
							$data_player[$wk_targezibaku][1] = 'D';
							&msg_write($data_vildata[2], 4, 35,"<b>$data_player[$wk_targezibaku][7]</b>����͗���<FONT color=\"#ff0000\">���c�Ȏp�Ŕ������ꂽ�E�E�E�B</FONT>");
						}
						# [ �������� ]
						&sub_judge;
						
						if ($data_vildata[0] == 1) {
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								if ($data_player[$i][3] eq 'WLF') {
									$data_player[$i][4] = 0;
								}
								if ($data_player[$i][3] eq 'BGD') {
									$data_player[$i][4] = 0;
								}
							}
							$data_vildata[2]++;
							$data_vildata[3] = 1;
							$data_vildata[4] = 0;
							$data_vildata[9] = $time;
							&msg_write($data_vildata[2], 50, 32,"<FONT size=\"+1\">$data_vildata[2]���ڂ̒��ƂȂ�܂����B</FONT>");
						}
					}
				}
				#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'SHOCK' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$in{'CMBPLAYER'}][1] = 'D';
					&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$in{'CMBPLAYER'}][7]</b>����͓s���ɂ��<FONT color=\"#ff0000\">�ˑR�����܂����E�E�E�B</FONT>");
				}
			}
			
			#--------------------------------------------------------------------- [ �� �\�͎��s�҂�]
			if($data_vildata[3] == 4){# ��̎��Ԓ���
				if($data_vildata[8] == 1){
					if($data_vildata[4] >= $limit_times[$data_vildata[8]][1]){
						$data_vildata[4] = 0;
						$kill_wlf = 1;
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][1] eq 'A') {
								if ($data_player[$i][3] eq 'WLF'){
									if ($data_player[$i][4] == 0 && $kill_wlf) {
										$data_player[$i][1] = 'D';
										&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$i][7]</b>����͓s���ɂ��<FONT color=\"#ff0000\">�ˑR�����܂����E�E�E�B</FONT>");
									}
									$kill_wlf = 0;
								}
								if ($data_player[$i][3] eq 'URA') {
									if ($data_player[$i][4] == 0) {
										$data_player[$i][1] = 'D';
										&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$i][7]</b>����͓s���ɂ��<FONT color=\"#ff0000\">�ˑR�����܂����E�E�E�B</FONT>");
									}
								}
								if ($data_player[$i][3] eq 'BGD' && $data_vildata[2] >= 2) {
									if ($data_player[$i][4] == 0) {
										$data_player[$i][1] = 'D';
										&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$i][7]</b>����͓s���ɂ��<FONT color=\"#ff0000\">�ˑR�����܂����E�E�E�B</FONT>");
									}
								}
							}
						}
					}
				}
				#-------------------------- �E�Q�\��
				if($data_vildata[2] >= 2){
					if ($in{'COMMAND'} eq 'KILL' && $data_player[$in{'CMBPLAYER'}][3] ne 'WLF' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][3] eq 'WLF') {
								$data_player[$i][4] = $in{'CMBPLAYER'};
							}
						}
						&msg_write($data_vildata[2], 11, 42,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>�����_���܂��B");
					}
				}else{
					if ($in{'COMMAND'} eq 'KILL' && $data_player[$in{'CMBPLAYER'}][3] ne 'WLF' && $data_player[$in{'CMBPLAYER'}][1] eq 'A' && $in{'CMBPLAYER'} == 1) {
						for ($i = 1; $i <= $data_vildata[1]; $i++) {
							if ($data_player[$i][3] eq 'WLF') {
								$data_player[$i][4] = $in{'CMBPLAYER'};
							}
						}
						&msg_write($data_vildata[2], 11, 42,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>�����_���܂��B");
					}
				}
				#-------------------------- �肢�t
				if ($in{'COMMAND'} eq 'FORTUNE' && $data_player[$sys_plyerno][4] == 0 && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$sys_plyerno][4] = $in{'CMBPLAYER'};
					&msg_write($data_vildata[2], 12, 43,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>�����肢�܂��B");
				}
				#-------------------------- ��l
				if ($in{'COMMAND'} eq 'GUARD' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$sys_plyerno][4] = $in{'CMBPLAYER'};
					&msg_write($data_vildata[2], 13, 44,"<b>".$data_player[$in{'CMBPLAYER'}][7]."</b>�������q���܂��B");
				}
				
				#--------------------------- �Ƃ茾
				if ($in{'COMMAND'} eq 'MSG1' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 5, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------- �� �b
				if ($in{'COMMAND'} eq 'MSG0' && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, $sys_plyerno, $wk_txtmsg2);
				}
				#--------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write($data_vildata[2], 2, 23, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'MSGM0'  && $wk_txtmsg1 ne '') {
					# [ msg write ]
					&msg_write(99, 1, 23, $wk_txtmsg2);
				}
				#--------------------------------------------------------------------- ��I������
				if ($in{'COMMAND'} ne '') {
					$wk_nightend = 1;
					$wk_targetwlf = 0;
					$wk_targetura = 0;
					$wk_targetbgd = 0;
					for ($i = 1; $i <= $data_vildata[1]; $i++) {
						if ($data_player[$i][1] eq 'A') {
							if ($data_player[$i][3] eq 'WLF'){
								$wk_targetwlf = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
							if ($data_player[$i][3] eq 'URA') {
								$wk_targetura = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
							if ($data_player[$i][3] eq 'BGD' && $data_vildata[2] >= 2) {
								$wk_targetbgd = $data_player[$i][4];
								if ($data_player[$i][4] == 0) {
									$wk_nightend = 0;
								}
							}
						}
					}
					if ($wk_nightend == 1) {
						# ��q�Ȃ��ŗd�ǈȊO�Ȃ�l�T�ɎE�Q�����
						if ($wk_targetwlf != $wk_targetbgd && $data_player[$wk_targetwlf][3] ne 'FOX') {
							$data_player[$wk_targetwlf][1] = 'D';
							&msg_write($data_vildata[2], 4, 34,"<b>$data_player[$wk_targetwlf][7]</b>����͗���<FONT color=\"#ff0000\">���c�Ȏp�Ŕ������ꂽ�E�E�E�B</FONT>");
						}
						# �d�ǂ��肢���ꂽ������
						if ($data_player[$wk_targetura][3] eq 'FOX') {
							$data_player[$wk_targetura][1] = 'D';
							&msg_write($data_vildata[2], 4, 34,"<b>$data_player[$wk_targetura][7]</b>����͗���<FONT color=\"#ff0000\">���c�Ȏp�Ŕ������ꂽ�E�E�E�B</FONT>");
						}
						#�L�����l�T�𓹘A��
						if ($wk_targetwlf != $wk_targetbgd && $data_player[$wk_targetwlf][3] eq 'ROL') {
							#�����Ă���l�T�̒������l��I�� *�킩�߂ĎI�ƈႤ
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								if ($data_player[$i][1] eq 'A'){
									if ($data_player[$i][3] eq 'WLF'){
										$wk_targezibaku = $i;
									}
								}
							}
							$data_player[$wk_targezibaku][1] = 'D';
							&msg_write($data_vildata[2], 4, 35,"<b>$data_player[$wk_targezibaku][7]</b>����͗���<FONT color=\"#ff0000\">���c�Ȏp�Ŕ������ꂽ�E�E�E�B</FONT>");
						}
						# [ �������� ]
						&sub_judge;
						
						if ($data_vildata[0] == 1) {
							for ($i = 1; $i <= $data_vildata[1]; $i++) {
								if ($data_player[$i][3] eq 'WLF') {
									$data_player[$i][4] = 0;
								}
								if ($data_player[$i][3] eq 'BGD') {
									$data_player[$i][4] = 0;
								}
							}
							$data_vildata[2]++;
							$data_vildata[3] = 1;
							$data_vildata[4] = 0;
							$data_vildata[9] = $time;
							&msg_write($data_vildata[2], 50, 32,"<FONT size=\"+1\">$data_vildata[2]���ڂ̒��ƂȂ�܂����B</FONT>");
						}
					}
				}
				#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
				if ($in{'COMMAND'} eq 'SHOCK' && $data_player[$in{'CMBPLAYER'}][1] eq 'A') {
					$data_player[$in{'CMBPLAYER'}][1] = 'D';
					&msg_write($data_vildata[2], 2, 34,"<b>$data_player[$in{'CMBPLAYER'}][7]</b>����͓s���ɂ��<FONT color=\"#ff0000\">�ˑR�����܂����E�E�E�B</FONT>");
				}
			}
		}
		#=================================================================== �Q�[���I��
		if($data_vildata[0]==2){
			#--------------------------------------------------------------------- ���b�Z�[�W
			if (($in{'COMMAND'} eq 'MSG' || $in{'COMMAND'} eq 'MSG2' || $in{'COMMAND'} eq 'MSG3') && $wk_txtmsg1 ne '') {
				$wk_fonttag1 = "";
				$wk_fonttag2 = "";
				# [ msg write ]
				if ($in{'COMMAND'} eq 'MSG2'){
					$wk_fonttag1 = "<FONT size=\"+1\">";
					$wk_fonttag2 = "</FONT>";
				}
				if ($in{'COMMAND'} eq 'MSG3'){
					$wk_fonttag1 = "<FONT size=\"-1\">";
					$wk_fonttag2 = "</FONT>";
				}
				&msg_write($data_vildata[2], 1, $sys_plyerno, $wk_fonttag1.$wk_txtmsg2.$wk_fonttag2);
			}
			#--------------------------------------------------------------------- �Ǘ��҃��b�Z�[�W
			if ($in{'COMMAND'} eq 'MSGM'  && $wk_txtmsg1 ne '') {
				# [ msg write ]
				&msg_write($data_vildata[2], 50, 23,$wk_txtmsg2);
			}
		}

		# 0:GAMESTART , 1:PLAYERNO , 2:DATE , 3:FAZE , 4:TIME , 5:FORMID , 7:�Ǘ��҂h�c
		# 0:NO , 1:ALIVE/DEAD , 2:VOTE , 3:JOB , 4:JOBwk , 5:wk1 , 6:wk2 , 7:PASSWORD , 8:NAME , 9:PROFILE 
		
		# [ HEAD ]
		&disp_head2;

		# [ PLAYER LIST ]
		&disp_players;

		# [ MY DATA ]
		&disp_mydata;
		
		if ($sys_logviewflg != 1 || $sys_storytype != "2"){
			print "<TR><TD class=\"CLSTD01\">�� �o����</TD></TR>\n";
			if($data_vildata[0]!=2){
			print "<TR><TD ><OPTION value=\"\"><INPUT type=\"submit\" value=\"�X�V\"></TD></TR>\n";
			}
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

		
		#�f�[�^��������
		if($sys_plyerno <= 50){
			&data_write;
		}
	}
	
	print "</TD></TR>\n";
	print "<TR><TD>\n";
	print "<INPUT type=\"hidden\" name=\"TXTPNO\" value=\"$sys_plyerno\">";
	print "<INPUT type=\"hidden\" name=\"VILLAGENO\" value=\"$sys_village\">";
	print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"2\">";
	$wk_rnd = int(rand(1000000)) + 1;
	print "<INPUT type=\"hidden\" name=\"FORMID\" value=\"$wk_rnd\">";
	print "</TD></TR>\n";
}
# ***************************************************************** ���O�C���Ȃ�
else{
	&disp_head1;
	#���[�U�[�h�c�̑��݌���
	&sysadoin;
	$user_no = 0;
	for ($i = 1; $i <= $sys_ID_COUNT; $i++) {# �Ǘ����[�U�[�`�F�b�N
		if ($m{name} eq $sys_ID[$i]) {
			$user_no = $i;
		}
	}
	
	if($user_no == 0 && $in{'TXTPASS'} eq $pass){# �V�K�Ǘ����[�U�[
		open(IN, $sys_path_bak);
		$wk_count_s = 1;
		$sys_ID_COUNT = 0;
		while (<IN>) {
			$value = $_;
			$value =~ s/\n//g;
			
			@wk_player = split(/,/, $value);
			$sys_ID[$wk_count_s] = $wk_player[0];
			$sys_pass[$wk_count_s] = $wk_player[1];
			$sys_name[$wk_count_s] = $wk_player[2];
			$wk_count_s++;
			$sys_ID_COUNT++;
			}
		close(IN);
		
		$sys_ID[$wk_count_s] = $m{name};
		$sys_pass[$wk_count_s] = $m{pass};
		$sys_name[$wk_count_s] = $m{name};
		
		open(OUT, "> ".$sys_path_bak);
		for(1..$wk_count_s){
			print OUT "$sys_ID[$_],$sys_pass[$_],$sys_name[$_]\n";
		}
		close(OUT);
		$user_no = $wk_count_s;
		$in{'TXTPASS'} = $sys_pass[$user_no];
	}
	
	if ($in{'TXTPASS'} eq $sys_pass[$user_no] && $user_no != 0) {
		if ($in{'COMMAND'} eq 'NEWVILLAGE') {
			#�V�K�쐬�������̏����t�@�C���֏�������
			#�Ō�̑��ԍ����擾����
			opendir(INDIR, $dat_dir) || die $!;
			@files = sort readdir(INDIR);
			closedir(INDIR);
			foreach (@files){
			if(/dat_buu(.*)\.(dat)$/){
				$filename = $_;
				if(open(IN, $dat_dir.$filename)){
				  @wk_vildata = split(/,/,<IN>);
				  #�t�@�C�������瑺�ԍ����擾
				  @wk_filename = unpack 'a7a6a4', $filename; # unpack
				  $wk_fileno = $wk_filename[1];
				  
				  close(IN);
				  }
				}
			}
			$wk_fileno++;
			$wk_txtmsg1 = '';
			$wk_txtmsglen = 0;
			if ($in{'TXTMURA'} ne '') {
				$in{'TXTMURA'} =~ s/\r*$//g;
				$in{'TXTMURA'} =~ s/\n//g;
				$in{'TXTMURA'} =~ s/,//g;
				$wk_txtmsg1 = $in{'TXTMURA'};
				$wk_txtmsg2 = $in{'TXTMURA'};
				$wk_txtmsg2 =~ s/\r/<BR>/g;
				$wk_txtmsglen = length($in{'TXTMURA'});
			}
			#�U���ɕ␳
			$cnt = sprintf("%06d",$wk_fileno);
			#�f�[�^�t�@�C�������O�t�@�C���֏�������
			$file_pdata = $dat_path.$cnt.".dat";
			$file_log   = $log_path.$cnt.".dat";
			@data_vildata = (0,1,0,1,0,'');
			if ($wk_txtmsglen <= 16){
				$data_vildata[5] = $wk_txtmsg1;
			}
			$data_vildata[7] = $user_no;
			$data_vildata[8] = 1;
			$data_vildata[9] = $time;
			#���̍쐬�Ɠ����ɏ����]���҂��쐬����
			$data_player[1][0] =  1;
			$data_player[1][1] =  'A';
			$data_player[1][2] =  0;
			$data_player[1][3] =  'NON';
			$data_player[1][4] =  0;
			$data_player[1][5] =  '-';
			$data_player[1][6] =  '#DDDDDD';
			$data_player[1][7] =  '�����]����';
			$data_player[1][8] =  '�Ǘ���';
			$data_player[1][9] =  0;
			$data_player[1][10] =  $date;
			$data_player[1][11] =  26;# icon
			
			&data_write;
			open(OUT, "> ".$file_log);
			close(OUT);
		
			print "<TR><TD align=\"center\">�V�K�ɍ쐬���܂����B</TD></TR>\n";
		} elsif ($in{'COMMAND'} eq 'DELVILLAGE') {
			$wak_village =  sprintf("%06d",$sys_village);
			open(IN, $dat_path.$wak_village.".dat");
			@wk_vildata = split(/,/,<IN>);
			close(IN);
			if ($wk_vildata[0] == 2) {# �I�����Ă鑺
				#�o�b�N�A�b�v�ԍ����擾
				if( open( FH, "douke/count.dat" ) ){
					$cnt = <FH>;
					close(FH);
					#�J�E���g�A�b�v
					$cnt++;
					#�J�E���^��������
					if( open( FH, ">douke/count.dat" ) ){
						print FH $cnt;
						close(FH);
					} else {
						print "�t�@�C���������I�[�v���Ɏ��s���܂����B\n";
					}
					#�U���ɕ␳
					$cnt = sprintf("%06d",$cnt);
				} else {
					print "�t�@�C���ǂݍ��I�[�v���Ɏ��s���܂����B\n";
				}
				#�v���C���[�f�[�^���o�b�N�A�b�v
				$file_pdata = $dat_path.$wak_village.".dat";
				$file_bakup = $dat_path_bak.$cnt.".bak";
				$ret = rename  $file_pdata , $file_bakup;
				if ($ret == 0) {
					printf "�t�@�C�����ύX�Ɏ��s(%s => %s)\n", $file_pdata, $file_bakup;
					printf "�G���[(%d:%s)\n", $!, $!;
				}
				#���O�f�[�^���o�b�N�A�b�v
				$file_log	= $log_path.$wak_village.".dat";
				$file_bakup = $log_path_bak.$cnt.".bak";
				$ret = rename  $file_log , $file_bakup;
				if ($ret == 0) {
					printf "�t�@�C�����ύX�Ɏ��s(%s => %s)\n", $file_pdata, $file_bakup;
					printf "�G���[(%d:%s)\n", $!, $!;
				}
				print "<TR><TD align=\"center\">�� $sys_village�Ԃ��폜���܂����B</TD></TR>\n";
			} else {
				print "<TR><TD align=\"center\">�Q�[�����I�����Ă���폜���Ă��������B</TD></TR>\n";
			}
		} elsif ($in{'COMMAND'} eq 'ENDVILLAGE') {
			open(IN, $file_pdata);
			$wk_count = 0;
			while (<IN>) {
				$value = $_;
				$value =~ s/\n//g;
				$wk_count++;
				if ($wk_count == 1){
					@data_vildata = split(/,/, $value);
				}else{
					@wk_player = split(/,/, $value);
					for ($i = 0; $i <= 11; $i++) {
						$data_player[$wk_count-1][$i] = $wk_player[$i];
					}
					}
			}
			close(IN);
			
			$data_vildata[0] = 2;
			&data_write;
			print "<TR><TD align=\"center\">�� $sys_village�ԃQ�[���������I�����܂����B</TD></TR>\n";
		}
		&disp_admin;
	} else {
		if ($in{'COMMAND'} eq 'ENTER') {
			&disp_login;
		}else{
			if ($in{subf} eq "room") {
				&disp_room;
			}
			elsif ($in{subf} eq "entry") {
				&disp_entry;
			}
			elsif ($in{subf} eq "log") {
				&disp_logview;
			}
			elsif ($in{subf} eq "master") {
				&disp_admin;
			}
			else {
				print "<TR><TD align=\"center\">���������������ǂ����B</TD></TR>\n";
			}
		}
	}
}

# [ FOOT ]
&disp_foot;

# Lock����
rmdir($lock_path);
