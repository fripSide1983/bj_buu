##########################################################################################################
# �ݒ�
##########################################################################################################
#---------------------------------------------------------------------
@limit_times = (
#	['��',	'��'	'�\�͎g�p'],
	[600,	600,	180],
	[270,	180,	180],
);

##########################################################################################################
# �T�u���[�`��
##########################################################################################################
#---------------------------------------------------------------------
sub data_write{
	open(OUT, "> ".$file_pdata);
	print OUT "$data_vildata[0],$data_vildata[1],$data_vildata[2],$data_vildata[3],$data_vildata[4],$data_vildata[5],$data_vildata[6],$data_vildata[7],$data_vildata[8],$data_vildata[9],$data_vildata[10]\n";
	for ($i9 = 1; $i9 <= $data_vildata[1]; $i9++) {
		print OUT "$data_player[$i9][0],$data_player[$i9][1],$data_player[$i9][2],$data_player[$i9][3],$data_player[$i9][4],$data_player[$i9][5],$data_player[$i9][6],$data_player[$i9][7],$data_player[$i9][8],$data_player[$i9][9],$data_player[$i9][10],$data_player[$i9][11],$data_player[$i9][12]\n";
	}
	close(OUT);
}
#---------------------------------------------------------------------
sub msg_write{
	@wk_writedata = @_;
	open(OUT, "> ".$tmp_log);
	open(IN, $file_log);
	print OUT "$wk_writedata[0],$wk_writedata[1],$wk_writedata[2],$wk_writedata[3]\n";
	while (<IN>) {
		print OUT;
	}
	close(IN);
	close(OUT);

	# Copy .tmp to .dat
	open(IN, $tmp_log);
	open(OUT, "> ".$file_log);
	$msgs = 0;
	while (<IN>) {
		# if ($msgs++ >= 2000) { last; }
		print OUT;
	}
	close(IN);
	close(OUT);
	unlink($tmp_log);
}
#---------------------------------------------------------------------
sub disp_head1{
	print "<HTML>\n";
	print "<HEAD>\n";
	print "<TITLE>$sys_title</TITLE>\n";
	print '<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">';
	print "</HEAD>\n";
	print "<BODY>\n";
	print "<FORM action=\"$cgi_path\" method=\"POST\">\n";
	print "<TABLE width=\"700\" cellspacing=\"5\"><TBODY>\n";
}
#---------------------------------------------------------------------
#  ���ɍs���i���O�C���j
#---------------------------------------------------------------------
sub disp_room{
	# Cookie�̒l�𓾂�
	&getCookie();
	$sys_default0 = $COOKIE{'SELECTROOM'};
	if ($sys_default0 eq "") {
		$sys_default0 = 0;
	}
	
	print "<TR><TD>\n";
	print "<TABLE>\n";
	#�f�[�^�t�@�C���̓��e��ǂݏo���đI�����X�g���쐬����
	print "<TR><TD>����I��</TD><TD><SELECT name=\"VILLAGENO\">\n";
	opendir(INDIR, $dat_dir) || die $!;
	@files = sort readdir(INDIR);
	closedir(INDIR);
	$wk_fileno = 1;
	foreach (@files){
		if(/dat_buu(.*)\.(dat)$/){
		$filename = $_;
		if(open(IN, $dat_dir.$filename)){
			@wk_vildata = split(/,/,<IN>);
			#�t�@�C�������瑺�ԍ����擾
			@wk_filename = unpack 'a7a6a4', $filename; # unpack
			$wk_muralist[$wk_fileno] = $wk_filename[1];
			$wk_muralist0[$wk_fileno] = $wk_vildata[0];
			$wk_muralist1[$wk_fileno] = $wk_vildata[1];
			$wk_muralist2[$wk_fileno] = $wk_vildata[2];
			$wk_muralist3[$wk_fileno] = $wk_vildata[3];
			$wk_muralist4[$wk_fileno] = $wk_vildata[4];
			$wk_muralist5[$wk_fileno] = $wk_vildata[5];
			$wk_muralist6[$wk_fileno] = $wk_vildata[6];
			$wk_muralist7[$wk_fileno] = $wk_vildata[7];
			$wk_muralist8[$wk_fileno] = $wk_vildata[8];
			$wk_muralist9[$wk_fileno] = $wk_vildata[9];
			$wk_muralist10[$wk_fileno] = $wk_vildata[10];
			print "<OPTION value=\"$wk_muralist[$wk_fileno]\" ";
			if ($sys_default0 == $wk_filename[1]) {
				print "selected";
			}
			print ">�� �Z��$wk_muralist[$wk_fileno]�� $wk_vildata[5]��</OPTION>\n";
			$wk_fileno++;
			close(IN);
		}
		}
	}
	print "  </SELECT></TD></TR>\n";
	print "<TR><TD colspan=\"2\"><INPUT type=\"submit\" value=\"���ɍs��\"></TD></TR>\n";
	#���̈ꗗ��\������
	print "<HTML>\n";
	print "<BODY>\n";
	print "<TABLE BORDER=1>\n";
	print "<TR><TH>�ԍ�</TH><TH>���̖��O</TH><TH>�l��</TH><TH>���</TH><TH>�Ǘ���</TH></TR>\n";
	for ($i = 1; $i <= $wk_fileno - 1; $i++) {
		print "<TR><TH>$wk_muralist[$i]<TH>$wk_muralist5[$i]��</TH><TH>$wk_muralist1[$i]�l</TH>";
		if ($wk_muralist0[$i]==0){
			print "<TH>�����O��</TH>";
		}
		if ($wk_muralist0[$i]==1){
			print "<TH>�Q�[���J�n</TH>";
		}
		if ($wk_muralist0[$i]==2){
			print "<TH>�Q�[���I��</TH>";
		}
		print "<TH>$sys_name[$wk_muralist7[$i]]</TH>";
		print "</TR>\n";
	}
	print "</TABLE>\n";
	print "</BODY>\n";
	print "</HTML>\n";
	
	print "</TABLE>\n";
	#print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"\">\n";
	print "<INPUT type=\"hidden\" name=\"COMMAND\" value=\"ENTER\">\n";
	print "</TD></TR>\n";
}

#---------------------------------------------------------------------
sub disp_login{
	# Cookie�̒l�𓾂�
	&getCookie();
	$sys_default1 = $COOKIE{'PLAYERNO'.$sys_village};
	if ($sys_default1 eq "") {
		$sys_default1 = 0;
	}
	$sys_default2 = $COOKIE{'PASSWORD'.$sys_village};
	
	print "<TR><TD>\n";
	print "<TABLE>\n";

	open(IN, $file_pdata);
	@wk_vildata = split(/,/, <IN>);
	print "<TR><TD>����I��</TD><TD>�� �Z��$sys_village�� $wk_vildata[5]��</TD></TR>\n";
	print "<TR><TD>���O��I��</TD><TD><SELECT name=\"CMBPLAYER\">\n";
	print "<OPTION value=\"0\">���@�l�i�ϐ�j</OPTION>\n";
	while ($value = <IN>) {
		$value =~ s/\n//g;
		@wk_player = split(/,/, $value);
		print "<OPTION value=\"$wk_player[0]\"";
		if ($sys_default1 == $wk_player[0]) {
			print " selected";
		}
		print ">$wk_player[7]</OPTION>\n";
	}
	close(IN);
	if($wk_vildata[10] != 1){
		print "<OPTION value=\"99\"";
		if ($sys_default1 == 99) {
			print " selected";
		}
		print ">�Ǘ��ҁF$sys_name[$wk_vildata[7]]</OPTION>\n";
	}
	print "</SELECT></TD></TR>\n";
	print "<TR><TD colspan=\"2\"><INPUT type=\"submit\" value=\"���ɍs��\"></TD></TR>\n";
	print "</TABLE>\n";
	print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"1\">\n";
	print "<INPUT type=\"hidden\" name=\"COMMAND\" value=\"LOGIN\">\n";
	print "<INPUT type=\"hidden\" name=\"VILLAGENO\" value=\"$sys_village\">";
	print "</TD></TR>\n";
}
#---------------------------------------------------------------------
#-  �Ǘ��҃��O�C��
#---------------------------------------------------------------------
sub disp_admin{
	print "<TR><TD>\n";
	print "<TABLE>\n";
	print "<TR><TD>����I��</TD><TD><SELECT name=\"VILLAGENO\">\n";
	$wk_fileno = 1;
	opendir(INDIR, $dat_dir) || die $!;
	@files = sort readdir(INDIR);
	closedir(INDIR);
	#$wk_fileno = 1;
	foreach (@files){
		if(/dat_buu(.*)\.(dat)$/){
		$filename = $_;
		if(open(IN, $dat_dir.$filename)){
			@wk_vildata = split(/,/,<IN>);
			
			@wk_filename = unpack 'a7a6a4', $filename; # unpack
			
			$wk_fileno = $wk_filename[1];
			
			print "<OPTION value=\"$wk_fileno\">�� �Z��$wk_fileno�� $wk_vildata[5]��</OPTION>\n";
			#$wk_fileno++;
			close(IN);
		}
		}
	}
	$wk_fileno++;
	print "  </SELECT></TD></TR>\n";
	
	print "<TR><TD>�V�KNO</TD><TD>��NO $wk_fileno</TD></TR>";
	
	print "<TR><TD>�����I��</TD><TD><SELECT name=\"COMMAND\">\n";
	print "  <OPTION value=\"NEWVILLAGE\">�����쐬</OPTION>\n";
	print "  <OPTION value=\"DELVILLAGE\">���̍폜</OPTION>\n";
	print "  <OPTION value=\"ENDVILLAGE\">�Q�[���̋����I��</OPTION>\n";
	print "</SELECT></TD></TR>\n";
	print "<TR><TD>GM</TD><TD><SELECT name=\"GM\">\n";
	print "  <OPTION value=\"ONGM\" selected>GM����</OPTION>\n";
	print "  <OPTION value=\"NOGM\">��GM</OPTION>\n";
	print "</SELECT></TD></TR>\n";
	print "<TR><TD>���̖��O(�W�����܂�)</TD><TD><INPUT size=\"20\" type=\"text\" maxlength=\"16\" name=\"TXTMURA\"></TD></TR>\n";
	print "<TR><TD>�p�X���[�h</TD><TD><INPUT type=\"hidden\" name=\"TXTPASS\" value=\"$pass\"></TD></TR>\n";
	print "<TR><TD colspan=\"2\"><INPUT type=\"submit\" value=\"�������s\"></TD></TR>\n";
	print "</TABLE>\n";
	#print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"1\">\n";
	print "</TD></TR>\n";
}
#---------------------------------------------------------------------
#  �����o�^�i�v���C���[�o�^�j
#---------------------------------------------------------------------
sub disp_entry{
	$wk_fileno = 1;
	$wk_entryflg = 0;
	opendir(INDIR, $dat_dir) || die $!;
	@files = sort readdir(INDIR);
	closedir(INDIR);
	$wk_fileno = 1;
	foreach (@files){
		if(/dat_buu(.*)\.(dat)$/){
		$filename = $_;
		if(open(IN, $dat_dir.$filename)){
			@wk_vildata = split(/,/,<IN>);
			if ($wk_vildata[0] == 0) {
				$wk_entryflg = 1;
				#�t�@�C�������瑺�ԍ����擾
				@wk_filename = unpack 'a7a6a4', $filename; # unpack
				$wk_murano[$wk_fileno] = $wk_filename[1];
				$wk_muralist5[$wk_fileno] = $wk_vildata[5];
				$wk_fileno++;
			}
			close(IN);
		}
		}
	}
	print "<TR><TD>\n";
	if ($wk_entryflg == 1) {
		# Cookie�̒l�𓾂�
		&getCookie();
		$sys_defaultMEIL = $COOKIE{'MAILADRES'};
		$sys_defaultHN = $COOKIE{'HN'};
		print "<CENTER><BR><TABLE border=\"1\" cellspacing=\"4\"><TBODY><TR><TD>";
		print "<TABLE cellpadding=\"4\"><TBODY>";
		
		print "<TR><TD align=\"center\"><B><FONT size=\"+2\">�����o�^��</FONT></B></TD></TR>\n";
		print "<TR><TD align=\"center\">��</TD></TR>\n";
		
		print "<TR><TD align=\"center\">������I�����Ă��������B</TD></TR>\n";
		print "<TR><TD align=\"center\"><SELECT name=\"VILLAGENO\">\n";
		for ($i = 1; $i <= $wk_fileno - 1; $i++) {
			print "<OPTION value=\"$wk_murano[$i]\">�� �Z��$wk_murano[$i]�� $wk_muralist5[$i]��</OPTION>\n";
		}
		print "  </SELECT></TD></TR>\n";
		print "<TR><TD align=\"center\">��</TD></TR>\n";
		
		print "<TR><TD align=\"center\"><INPUT type=\"hidden\" name=\"TXTHN\" value=\"$m{name}\"></TD></TR>\n";
		
		print "<TR><TD align=\"center\">���A�i�^�̃A�C�R����I�����Ă��������B</TD></TR>\n";
		print "<TR><TD align=\"center\"><SELECT name=\"CMBICON\">\n";
		# �A�C�R���t�@�C����ǂݍ���
		if(open(IN, $ico_path_bak)){
			while (<IN>) {
				$value = $_;
				$value =~ s/\n//g;
				@wk_icon = split(/,/, $value);
				if($wk_icon[0]==26){
					print "<OPTION value=\"$wk_icon[0]\" selected>$wk_icon[1]</OPTION>\n";
				}else{
					print "<OPTION value=\"$wk_icon[0]\">$wk_icon[1]</OPTION>\n";
				}
			}
			close(IN);
		}
		print "</SELECT></TD></TR>\n";
		#print "<TR><TD align=\"center\">��</TD></TR>\n";
		print "<TR><TD align=\"center\">��<A href='iconlist.htm' target='_blank'>�A�C�R���ꗗ</A></TD></TR>\n";
		
		print "<TR><TD align=\"center\">���A�i�^�̕\\���F��I�����Ă��������B</TD></TR>\n";
		print "<TR><TD align=\"center\"><SELECT name=\"CMBCOLOR\">\n";
		print "<OPTION value=\"1\" selected>���D lightglay</OPTION>\n";
		print "<OPTION value=\"2\">�ÊD darkglay</OPTION>\n";
		print "<OPTION value=\"3\">�� yellow</OPTION>\n";
		print "<OPTION value=\"4\">�� orange</OPTION>\n";
		print "<OPTION value=\"5\">�� red</OPTION>\n";
		print "<OPTION value=\"6\">�� lightblue</OPTION>\n";
		print "<OPTION value=\"7\">�� blue</OPTION>\n";
		print "<OPTION value=\"8\">�� green</OPTION>\n";
		print "<OPTION value=\"9\">�� purple</OPTION>\n";
		print "<OPTION value=\"10\">�� pink</OPTION>\n";
		print "</SELECT></TD></TR>\n";
		print "<TR><TD align=\"center\">��</TD></TR>\n";

		print "<TR><TD align=\"center\">���A�i�^�̑��l�Ƃ��Ă̖��O����͂��Ă��������B�i10�����j<BR>�i��F�R�c�@�l�Y�j<BR><FONT size=\"-1\">�v���C���͂��̖��O���g�p���܂��BHN���΂�Ȃ����̂��D�܂����ł��B</FONT></TD></TR>\n";
		print "<TR><TD align=\"center\"><INPUT size=\"20\" maxlength=\"10\" type=\"text\" name=\"TXTNAME\"></TD></TR>\n";
		print "<TR><TD align=\"center\">��</TD></TR>\n";

		print "<TR><TD align=\"center\">�u�������v<BR>���͑��̂��߉Ƒ��̂��߂ɂ����Ď������g�̂��߂�<BR>������������A���܂��܁A����A�Ȃ�ƂȂ��A����邩������Ȃ�<BR>�u�l�T�v�Ɛ킢�������Ƃ𐾂��܂��B</TD></TR>\n";
		print "<TR><TD align=\"center\"><INPUT type=\"submit\" value=\"���ӂ���i�o�^�j\"></TD></TR>\n";
	
		print "</TBODY></TABLE>\n";
		print "</TD></TR></TBODY></TABLE></CENTER>\n";
		print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"1\">";
		print "<INPUT type=\"hidden\" name=\"COMMAND\" value=\"ENTRY\">\n";
	} else {
		print "�؍݉\\�ȑ�������܂���ł����B";
	}
	print "</TD></TR>\n";
}
#---------------------------------------------------------------------
# �ߋ����O�\������
#---------------------------------------------------------------------
sub disp_logview{
	# Cookie�̒l�𓾂�
	&getCookie();
	$sys_default0 = $COOKIE{'SELECTROOM'};
	if ($sys_default0 eq "") {
		$sys_default0 = 0;
	}
	
	print "<TR><TD>\n";
	print "<TABLE>\n";
	
	print "<TR><TD>����I��</TD><TD><SELECT name=\"VILLAGENO\">\n";
	$wk_fileno = 1;
	opendir(INDIR, $dat_dir) || die $!;
	@files = sort readdir(INDIR);
	closedir(INDIR);
	$wk_fileno = 1;
	foreach (@files){
		if(/dat_buu(.*)\.(dat)$/){
		$filename = $_;
		if(open(IN, $dat_dir.$filename)){
			@wk_vildata = split(/,/,<IN>);
			if ($wk_vildata[0] == 2) {
				if ($sys_default0 == $wk_fileno) {
					print "selected";
				}
				#�t�@�C�������瑺�ԍ����擾
				@wk_filename = unpack 'a7a6a4', $filename; # unpack
				$wk_muralist[$wk_fileno] = $wk_filename[1];
				$wk_muralist0[$wk_fileno] = $wk_vildata[0];
				$wk_muralist1[$wk_fileno] = $wk_vildata[1];
				$wk_muralist2[$wk_fileno] = $wk_vildata[2];
				$wk_muralist3[$wk_fileno] = $wk_vildata[3];
				$wk_muralist4[$wk_fileno] = $wk_vildata[4];
				$wk_muralist5[$wk_fileno] = $wk_vildata[5];
				$wk_muralist6[$wk_fileno] = $wk_vildata[6];
				$wk_muralist7[$wk_fileno] = $wk_vildata[7];
				$wk_muralist8[$wk_fileno] = $wk_vildata[8];
				$wk_muralist9[$wk_fileno] = $wk_vildata[9];
				$wk_muralist10[$wk_fileno] = $wk_vildata[10];
				print "<OPTION value=\"$wk_muralist[$wk_fileno]\" ";
				print ">�� �Z��$wk_muralist[$wk_fileno]�� $wk_vildata[5]��</OPTION>\n";
				$wk_fileno++;
			}
			close(IN);
		}
		}
	}
	print "  </SELECT></TD></TR>\n";
	print "<TR><TD>�b��I��</TD><TD><SELECT name=\"STORYTYPE\">\n";
	print "<OPTION value=\"1\">���l�̐킢</OPTION>\n";
	print "<OPTION value=\"2\">��̒k�b</OPTION>\n";
	print "<OPTION value=\"3\" selected>�S�L�^</OPTION>\n";
	print "</SELECT></TD></TR>\n";
	print "<TR><TD colspan=\"2\"><INPUT type=\"submit\" value=\"�L�^������\"></TD></TR>\n";
	
	#���̈ꗗ��\������
	print "<HTML>\n";
	print "<BODY>\n";
	print "<TABLE BORDER=1>\n";
	print "<TR><TH>�ԍ�</TH><TH>���̖��O</TH><TH>�l��</TH><TH>�@���@�ʁ@</TH><TH>�Ǘ���</TH></TR>\n";
	for ($i = 1; $i <= $wk_fileno - 1; $i++) {
		print "<TR><TH>$wk_muralist[$i]<TH>$wk_muralist5[$i]��</TH><TH>$wk_muralist1[$i]�l</TH>";
		if ($wk_muralist8[$i]==0){
			print "<TH>������</TH>";
		}elsif ($wk_muralist8[$i]==1){
			print "<TH>���l�̏����@</TH>";
		}elsif ($wk_muralist8[$i]==2){
			print "<TH>�d�ǂ̏���</TH>";
		}elsif ($wk_muralist8[$i]==3){
			print "<TH>�l�T�̏����@</TH>";
		}elsif ($wk_muralist8[$i]==4){
			print "<TH>�d�ǂ̏���</TH>";
		}else{
			print "<TH>�@�@�@�@�@�@</TH>";
		}
		print "<TH>$sys_name[$wk_muralist7[$i]]</TH>";
		print "</TR>\n";
	}
	print "</TABLE>\n";
	print "</BODY>\n";
	print "</HTML>\n";
	
	print "</TABLE>\n";
	print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"1\">\n";
	print "<INPUT type=\"hidden\" name=\"COMMAND\" value=\"LOGVIEW\">\n";
	print "</TD></TR>\n";
}

sub disp_logview_back{
	# Cookie�̒l�𓾂�
	&getCookie();
	$sys_default0 = $COOKIE{'SELECTROOM'};
	if ($sys_default0 eq "") {
		$sys_default0 = 0;
	}
	
	print "<TR><TD>\n";
	print "<TABLE>\n";
	
	print "<TR><TD>����I��</TD><TD><SELECT name=\"VILLAGENO\">\n";
	#�o�b�N�A�b�v�ԍ����擾
	if( open( FH, "./douke/count.dat" ) ){
		$maxcnt = <FH>;
		close(FH);
		for ($i = 1; $i <= $maxcnt; $i++) {
			$cnt = sprintf("%06d",$i);
			if( open(IN, $dat_path.$cnt.".bak") ){
				@wk_vildata = split(/,/,<IN>);
				print "<OPTION value=\"$i\" ";
				if ($sys_default0 == $wk_fileno) {
					print "selected";
				}
				$wk_muralist[$i] = $i;
				$wk_muralist0[$i] = $wk_vildata[0];
				$wk_muralist1[$i] = $wk_vildata[1];
				$wk_muralist2[$i] = $wk_vildata[2];
				$wk_muralist3[$i] = $wk_vildata[3];
				$wk_muralist4[$i] = $wk_vildata[4];
				$wk_muralist5[$i] = $wk_vildata[5];
				$wk_muralist6[$i] = $wk_vildata[6];
				$wk_muralist7[$i] = $wk_vildata[7];
				$wk_muralist8[$i] = $wk_vildata[8];
				$wk_muralist9[$i] = $wk_vildata[9];
				$wk_muralist10[$i] = $wk_vildata[10];
				print ">�� �Z��$wk_fileno�� $wk_vildata[5]��</OPTION>\n";
				close(IN);
			}
		}
	} else {
		print "�t�@�C���ǂݍ��I�[�v���Ɏ��s���܂����B\n";
	}
	print "  </SELECT></TD></TR>\n";
	
	print "<TR><TD>�b��I��</TD><TD><SELECT name=\"STORYTYPE\">\n";
	print "<OPTION value=\"1\">���l�̐킢</OPTION>\n";
	print "<OPTION value=\"2\">��̒k�b</OPTION>\n";
	print "<OPTION value=\"3\" selected>�S�L�^</OPTION>\n";
	print "</SELECT></TD></TR>\n";
	
	print "<TR><TD colspan=\"2\"><INPUT type=\"submit\" value=\"�L�^������\"></TD></TR>\n";
	print "</TABLE>\n";
	print "<INPUT type=\"hidden\" name=\"TXTLOGIN\" value=\"1\">\n";
	print "<INPUT type=\"hidden\" name=\"COMMAND\" value=\"LOGVIEW\">\n";
	
	#���̈ꗗ��\������
	print "<TABLE BORDER=1>\n";
	print "<TR><TH>�ԍ�</TH><TH>���̖��O</TH><TH>�l��</TH><TH>�@���@�ʁ@</TH><TH>�Ǘ���</TH></TR>\n";
	for ($i = 1; $i <= $maxcnt; $i++) {
		print "<TR><TH>$wk_muralist[$i]<TH>$wk_muralist5[$i]��</TH><TH>$wk_muralist1[$i]�l</TH>";
		if ($wk_muralist8[$i]==0){
			print "<TH>������</TH>";
		}elsif ($wk_muralist8[$i]==1){
			print "<TH>���l�̏����@</TH>";
		}elsif ($wk_muralist8[$i]==2){
			print "<TH>�d�ς̏���</TH>";
		}elsif ($wk_muralist8[$i]==3){
			print "<TH>�l�T�̏����@</TH>";
		}elsif ($wk_muralist8[$i]==4){
			print "<TH>�d�ς̏���</TH>";
		}else{
			print "<TH>�@�@�@�@�@�@</TH>";
		}
		print "<TH>$sys_name[$wk_muralist7[$i]]</TH>";
		print "</TR>\n";
	}
	
}

#---------------------------------------------------------------------
#---------------------------------------------------------------------
sub disp_head2{
	print "<HTML>\n";
	print "<HEAD>\n";
	print '<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">';
	print "<STYLE type=\"text/css\"><!--\n";
	print "TABLE{ font-size : 11pt; }\n";
	print ".CLSTABLE{ font-size : 10pt; }\n";
	print ".CLSTABLE2{ color : #333333; }\n";
	if ($data_vildata[3] == 1 || $data_vildata[3] == 3) {
		print ".CLSTD01{ color : white; background-color : black; font-weight : bold; }\n";
	}
	if ($data_vildata[3] == 2 || $data_vildata[3] == 4) {
		print ".CLSTD01{ color : black; background-color : white; font-weight : bold; }\n";
	}
	print ".CLSTD02{ background-color : #e3e3e3; }\n";
	print "--></STYLE>\n";
	print qq|<script type="text/javascript" src="$htmldir/nokori_time.js"></script>\n|;
	print "<TITLE>$sys_title</TITLE>\n";
	print "</HEAD>\n";
	if ($data_vildata[3] == 1 || $data_vildata[3] == 3) {
		print "<BODY link=\"#FFCC00\" vlink=\"#FFCC00\" alink=\"#FFCC00\">\n";
	}
	if ($data_vildata[3] == 2 || $data_vildata[3] == 4) {
		print "<BODY bgcolor=\"#000000\" text=\"#ffffff\" link=\"#FF6600\" vlink=\"#FF6600\" alink=\"#FF6600\">\n";
	}
	print "<FORM action=\"$cgi_path\" method=\"POST\">\n";
	print "<TABLE width=\"700\" cellspacing=\"5\"><TBODY>\n";
	print "<TR><TD height=\"20\"><FONT size=\"+1\">$sys_title</FONT></TD></TR>\n";
	if($data_vildata[8] == 0){
		print "<TR><TD>�������ԂȂ�</TD></TR>\n";
	}else{
		print "<TR><TD>�������Ԃ���</TD></TR>\n";
	}
	if($data_vildata[10] == 1){
		print "<TR><TD>���̑��͉�GM�ł��B�ŏ��ɓ��������l���Q�[�����J�n���Ă��������B</TD></TR>\n";
	}
}
#---------------------------------------------------------------------
#  ��ʂ̈�ԏ�ɑ��l�̏����ꗗ�\������
#---------------------------------------------------------------------
sub disp_players{
	print "<TR><TD class=\"CLSTD01\">�� ���l����</TD></TR>\n";
	print "<TR><TD><TABLE class=\"CLSTABLE\"><TBODY>\n";
	$wk_amari = (5 - ($data_vildata[1] % 5)) % 5;
	$wk_iend  = $data_vildata[1] + $wk_amari;
	for ($i = 1; $i <= $wk_iend; $i++) {
		if ($i % 5 == 1){
			print "<TR>";
		}
		if ($i <= $data_vildata[1]){
			if ($data_player[$i][1] eq 'A'){
				#�������̃A�C�R����\��
				print "<TD valign=\"top\" bgcolor=\"$wk_color[$data_player[$i][6]]\"><IMG src=\"".$imgpath."alive".$data_player[$i][11].".gif\" title=\"$data_player[$i][7]\" alt=\"$data_player[$i][7]\" width=\"32\" height=\"32\" border=\"0\"></TD>\n";
			}
			if ($data_player[$i][1] eq 'D'){
				#���S�Ȃ̂ŕ�΂̃A�C�R����\��
				print "<TD valign=\"top\" bgcolor=\"$wk_color[$data_player[$i][6]]\"><IMG src=\"".$imgpath."grave.gif\" title=\"$data_player[$i][7]\" width=\"32\" height=\"32\" border=\"0\"></TD>\n";
			}
			print "<TD>$data_player[$i][7]<BR>";
			if ($data_vildata[0] == 2 || $data_player[$sys_plyerno][1] eq 'D' || $sys_plyerno == 50) {
				print "<b>$data_player[$i][8]</b>����<BR>";
				if ($data_player[$i][3] eq 'HUM') {
					print "[$chr_hum]";
				}
				if ($data_player[$i][3] eq 'WLF') {
					print "[$chr_wlf]";
				}
				if ($data_player[$i][3] eq 'URA') {
					print "[$chr_ura]";
				}
				if ($data_player[$i][3] eq 'NEC') {
					print "[$chr_nec]";
				}
				if ($data_player[$i][3] eq 'MAD') {
					print "[$chr_mad]";
				}
				if ($data_player[$i][3] eq 'BGD') {
					print "[$chr_bgd]";
				}
				if ($data_player[$i][3] eq 'FRE') {
					print "[$chr_fre]";
				}
				if ($data_player[$i][3] eq 'FOX') {
					print "[$chr_fox]";
				}
				if ($data_player[$i][3] eq 'ROL') {
					print "[$chr_rol]";
				}
				if ($sys_plyerno == 50) {
					if ($data_player[$i][2] != 0) {
						print "<FONT color=\"0000FF\">��</FONT>";
					}
					if ($data_player[$i][4] != 0) {
						print "<FONT color=\"00FF00\">��</FONT>";
					}
					print "<BR>$data_player[$i][10]";
				}
				print "<BR>";
			}
			if ($data_player[$i][1] eq 'A'){
				print "�i�������j</TD>\n";
			}
			if ($data_player[$i][1] eq 'D'){
				print "�i���@�S�j</TD>\n";
			}
		}else{
			print OUT "<TD></TD><TD></TD>\n";
		}
		if ($i % 5 == 0){
			print "</TR>";
		}
	}
	print "</TBODY></TABLE></TD></TR>\n";
}
#---------------------------------------------------------------------
#  ��ʂ̓�ԖڂɃL�����N�^�[�̖�ڂƏ󋵂�\������
#---------------------------------------------------------------------
sub disp_mydata{
	if($data_vildata[0] == 1 && $sys_plyerno <= 23){
		print "<TR><TD class=\"CLSTD01\">�� �A�i�^�̏��</TD></TR>\n";
		if ($data_player[$sys_plyerno][1] eq 'A') {
			print "<TR><TD><TABLE cellspacing=\"0\"><TBODY>\n";
			if ($data_player[$sys_plyerno][3] eq 'HUM') {
				print "<TR><TD><IMG src=\"".$imgpath."hum.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>�A�i�^�̖����́u$chr_hum�v�ł��B<BR>";
				print "�y�\\�́z����܂���B�������A�A�i�^�̒m�b�ƗE�C�ő����~�����Ƃ��ł���͂��ł��B</TD></TR>";
			}
			if ($data_player[$sys_plyerno][3] eq 'WLF') {
				print "<TR><TD><IMG src=\"".$imgpath."wlf.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>�A�i�^�̖����́u$chr_wlf�v�ł��B<BR>";
				print "�y�\\�́z��̊Ԃɑ��̐l�T�Ƌ��͂����l�ЂƂ�E�Q�ł��܂��B�A�i�^�͂��̋��͂ȗ͂ő��l��H���E���̂ł��B</TD></TR>";
				for ($i = 1; $i <= $data_vildata[1]; $i++) {
					if ($data_player[$i][3] eq 'WLF' && $i != $sys_plyerno) {
						print "<TR><TD colspan=\"2\">�y�\\�͔����z�ւ荂���l�T�̌����������Ԃ�<b>$data_player[$i][7]</b>����ł��B</TD></TR>";
					}
				}
				if ($data_player[$sys_plyerno][4] > 0) {
					print "<TR><TD colspan=\"2\">�y�\\�͔����z�A�i�^��<B>$data_player[$data_player[$sys_plyerno][4]][7]</B>������E��\\��ł��B</TD></TR>";
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'URA') {
				print "<TR><TD><IMG src=\"".$imgpath."ura.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>�A�i�^�̖����́u$chr_ura�v�ł��B<BR>";
				print "�y�\\�́z��̊Ԃɑ��l�ЂƂ���u�l�v���u�T�v�����ׂ邱�Ƃ��ł��܂��B�A�i�^�����l�̏����������Ă��܂��B</TD></TR>";
				if ($data_player[$sys_plyerno][4] > 0) {
					print "<TR><TD colspan=\"2\">�y�\\�͔����z�肢�̌��ʁA<B>$data_player[$data_player[$sys_plyerno][4]][7]</B>�����";
					if ($data_player[$data_player[$sys_plyerno][4]][3] eq 'WLF') {
						print "�u$chr_wlf�v�ł����B"
					}else{
						print "�u$chr_hum�v�ł����B"
					}
					print "</TD></TR>";
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'NEC') {
				print "<TR><TD><IMG src=\"".$imgpath."nec.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>�A�i�^�̖����́u$chr_nec�v�ł��B<BR>";
				print "�y�\\�́z[�Q���ڈȍ~]���̓��̃����`���҂��u�l�v���u�T�v�����ׂ邱�Ƃ��ł��܂��B�n���ł����A�i�^�̓w�͎���ő傫���v�����邱�Ƃ��s�\\�ł͂���܂���B</TD></TR>";
				if ($data_player[$sys_plyerno][4] > 0) {
					print "<TR><TD colspan=\"2\">�y�\\�͔����z�O�����Y���ꂽ<B>$data_player[$data_player[$sys_plyerno][4]][7]</B>�����";
					if ($data_player[$data_player[$sys_plyerno][4]][3] eq 'WLF') {
						print "�u$chr_wlf�v�ł����B"
					}else{
						print "�u$chr_hum�v�ł����B"
					}
					print "</TD></TR>";
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'MAD') {
				print "<TR><TD><IMG src=\"".$imgpath."mad.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>�A�i�^�̖����́u$chr_mad�v�ł��B<BR>";
				print "�y�\\�́z�l�T�̏������A�i�^�̏����ƂȂ�܂��B�A�i�^�͂ł��邩���苶���ď�����������̂ł��B�o�J�ɂȂ�B</TD></TR>";
			}
			if ($data_player[$sys_plyerno][3] eq 'BGD') {
				print "<TR><TD><IMG src=\"".$imgpath."bgd.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>�A�i�^�̖����́u$chr_bgd�v�ł��B<BR>";
				print "�y�\\�́z[�Q���ڈȍ~]��̊Ԃɑ��l�ЂƂ���w�肵�l�T�̎E�Q�����邱�Ƃ��ł��܂��B�l�T�̃R�R����ǂނ̂ł��B</TD></TR>";
				if ($data_player[$sys_plyerno][4] > 0) {
					print "<TR><TD colspan=\"2\">�y�\\�͔����z�A�i�^��<B>$data_player[$data_player[$sys_plyerno][4]][7]</B>�������q���Ă��܂��B</TD></TR>";
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'FRE') {
				print "<TR><TD><IMG src=\"".$imgpath."fre.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>�A�i�^�̖����́u$chr_fre�v�ł��B<BR>";
				print "�y�\\�́z�A�i�^�͂����ЂƂ��$chr_fre������ł��邩��m�邱�Ƃ��ł��܂��B�������Ԃ����ɔ�׉i���\\�͂ł��B�A�i�^�ɂ͐������鎞�Ԃ��^����ꂽ�̂ł��B�Y�݂Ȃ����B</TD></TR>";
				for ($i = 1; $i <= $data_vildata[1]; $i++) {
					if ($data_player[$i][3] eq 'FRE' && $i != $sys_plyerno) {
						print "<TR><TD colspan=\"2\">�y�\\�͔����z�����ЂƂ��$chr_fre��<b>$data_player[$i][7]</b>����ł��B</TD></TR>";
					}
				}
			}
			if ($data_player[$sys_plyerno][3] eq 'FOX') {
				print "<TR><TD><IMG src=\"".$imgpath."fox.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>�A�i�^�̖����́u$chr_fox�v�ł��B<BR>";
				print "�y�\\�́z�A�i�^�͐l�T�ɎE����邱�Ƃ͂���܂���B��������������Ă��܂��Ǝ���ł��܂��܂��B���l���x���A�l�T���x���A����d�ς̂��̂ɂ���̂ł��B</TD></TR>";
			}
			if ($data_player[$sys_plyerno][3] eq 'ROL') {
				print "<TR><TD><IMG src=\"".$imgpath."rol.gif\" width=\"32\" height=\"32\" border=\"0\"></TD>";
				print "<TD>�A�i�^�̖����́u$chr_rol�v�ł��B<BR>";
				print "�y�\\�́z���̑��ɏZ�ނ����̔L���ł��B���S���ɃA�i�^���E��������𓹘A��ɂ��܂��B</TD></TR>";
			}
			if ($data_player[$sys_plyerno][11] == 1) {
				print "<TR><TD colspan=\"2\">�y���@�فz�A�i�^�͑��̗l�q���f���Ȃ��璾�ق��Ă��܂��B�i�����͂ł��܂��j</TD></TR>";
			}
			if ($data_player[$sys_plyerno][2] != 0) {
				print "<TR><TD colspan=\"2\">�y���@�[�z�A�i�^��<B>$data_player[$data_player[$sys_plyerno][2]][7]</B>����ɓ��[���s���܂����B</TD></TR>";
			}
			print "</TBODY></TABLE></TD></TR>\n";
		}else{
			print "<TR><TD>�A�i�^�͑��₦�܂����E�E�E</TD></TR>\n";
		}
	}
	if($data_vildata[0] == 2 && $sys_plyerno <= 23) {
		print "<TR><TD class=\"CLSTD01\">�� �A�i�^�̏��</TD></TR>\n";
		if ($data_player[$sys_plyerno][5] eq 'W') {
			print "<TR><TD>�A�i�^��<FONT color=\"FF0000\">����</FONT>���܂����B</TD></TR>\n";
		}else{
			print "<TR><TD>�A�i�^��<FONT color=\"0000FF\">�s�k</FONT>���܂����B</TD></TR>\n";
		}
	}
}
#---------------------------------------------------------------------
#  ���݂̓����Ǝc�莞�Ԃ�\������
#---------------------------------------------------------------------
sub disp_time{
	$wk_faze[0] = '';
	$wk_faze[1] = 'sun.gif';
	$wk_faze[2] = 'moon.gif';
	if($data_vildata[3] == 1){
		$max_time = $limit_times[$data_vildata[8]][0];
	}elsif($data_vildata[3] == 2){
		$max_time = $limit_times[$data_vildata[8]][1];
	}else {
		$max_time = $limit_times[$data_vildata[8]][2];
	}
	
	$r_time = $max_time - $_[4];
	print "<IMG src=\"".$imgpath."village.gif\" width=\"32\" height=\"32\" border=\"0\"> ";
	print "<FONT size=\"+2\">�` $_[5]�� �`</FONT><BR>";
	print "<IMG src=\"".$imgpath."clock.gif\" width=\"32\" height=\"32\" border=\"0\"> ";
	if($_[2]==0){
		print "<FONT size=\"+2\">�����O��</FONT>";
	}else{
		print "<FONT size=\"+2\">$_[2]</FONT>���� ";
		# ��
		if ($_[3]==1 ||$_[3]==3){
			print "<IMG src=\"".$imgpath.$wk_faze[1]."\" border=\"0\"> ";
			if ($_[3]==1){
				$wk_min = int($r_time / 60);
				$wk_sec = $r_time - 60 * $wk_min;
				print "���v�܂ł��� <span id=\"nokori_time\"><FONT size=\"+2\">$wk_min</FONT>��";
				if($wk_sec > 0){
					print " <FONT size=\"+2\">$wk_sec</FONT>�b";
				}
				print "</span>";
				print qq|<script type="text/javascript"><!--\n nokori_time_jinro($r_time);\n// --></script>\n|;
				print qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
			}else{
				# ���[����
				$wk_nonvotecount = 0;
				for ($i = 1; $i <= $data_vildata[1]; $i++) {
					if ($data_player[$i][2] == 0 && $data_player[$i][1] eq 'A') {
						$wk_nonvotecount++;
					}
				}
				$wk_min = int($r_time / 60);
				$wk_sec = $r_time - 60 * $wk_min;
				print "���z�����̋�ɒ��݂����Ă��܂��B";
				print "���� <span id=\"nokori_time\"><FONT size=\"+2\">$wk_min</FONT>��";
				if($wk_sec > 0){
					print " <FONT size=\"+2\">$wk_sec</FONT>�b";
				}
				print "</span>�ȓ���<FONT size=\"+2\">���[</FONT>���s���Ă��������B<BR>";
				print qq|<script type="text/javascript"><!--\n nokori_time_jinro($r_time);\n// --></script>\n|;
				print qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
				print "����<FONT size=\"+2\">$wk_nonvotecount</FONT>���̓��[�҂��ƂȂ��Ă��܂��B";
			}
		}
		# ��
		if ($_[3]==2 ||$_[3]==4){
			print "<IMG src=\"".$imgpath.$wk_faze[2]."\" border=\"0\"> ";
			if ($_[3]==2){
				$wk_min = int(($max_time - $_[4]) / 60);
				$wk_sec = $max_time - 60 * $wk_min - $_[4];
				print "�閾���܂ł��� <span id=\"nokori_time\"><FONT size=\"+2\">$wk_min</FONT>��";
				if($wk_sec > 0){
					print " <FONT size=\"+2\">$wk_sec</FONT>�b";
				}
				print "</span>";
				print qq|<script type="text/javascript"><!--\n nokori_time_jinro($r_time);\n// --></script>\n|;
				print qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
			}else{
				# ���[����
				$wk_min = int(($max_time - $_[4]) / 60);
				$wk_sec = $max_time - 60 * $wk_min - $_[4];
				print "���̋󂪔��݂͂��߂Ă��܂��B";
				print "���� <span id=\"nokori_time\"><FONT size=\"+2\">$wk_min</FONT>��";
				if($wk_sec > 0){
					print " <FONT size=\"+2\">$wk_sec</FONT>�b";
				}
				print "</span>�ȓ���<FONT size=\"+2\">�\\�͑Ώ�</FONT>�����肵�Ă��������B<BR>";
				print qq|<script type="text/javascript"><!--\n nokori_time_jinro($r_time);\n// --></script>\n|;
				print qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
			}
		}
		print "<BR>\n";
	}
}
#---------------------------------------------------------------------
sub disp_msg{
	$wk_inputflg = 0;
	print "<TABLE cellpadding=\"0\"><TBODY>";
	open(IN, $file_log);
	while ($wk_inputflg == 0) {
		if ($_ = <IN>){
			$wk_msgwriteflg = 0;
			@wk_logdata = split(/,/, $_);
			# �J�n�O
			if ($data_vildata[0] == 0){
				$wk_msgwriteflg = 1;
			}
			# �Q�[�����A�I���ネ�O�C��
			if ($data_vildata[0] == 1 || ($data_vildata[0] == 2 && $sys_logviewflg == 0)){
				# ��
				if ($data_vildata[3] == 1 || $data_vildata[3] == 3){
					if ($wk_logdata[0] == $data_vildata[2] && ($wk_logdata[1] <= 2 || $wk_logdata[1] == 50)){
						$wk_msgwriteflg = 1;
					}
					if ($wk_logdata[0] == $data_vildata[2] - 1 && ($wk_logdata[1] == 2 || $wk_logdata[1] == 4)){
						$wk_msgwriteflg = 1;
					}
					if ($wk_logdata[0] <= $data_vildata[2] - 2) {
						$wk_inputflg = 9;
					}
				}
				# ��
				if ($data_vildata[3] == 2 || $data_vildata[3] == 4){
					if ($wk_logdata[0] == $data_vildata[2]){
						if ($wk_logdata[1] == 2 || $wk_logdata[1] == 50) {
							$wk_msgwriteflg = 1;
						}
						if ($wk_logdata[1] == 3) {
							if($sys_plyerno == 60){ #�ϐ�
								$wk_msgwriteflg = 2;
							}else{
								if($data_player[$sys_plyerno][3] ne 'WLF' && $data_player[$sys_plyerno][1] eq 'A') {
									$wk_msgwriteflg = 2;
								}else{
									$wk_msgwriteflg = 3;
								}
							}
						}
						if ($wk_logdata[1] == 5 && ($wk_logdata[2] == $sys_plyerno || $data_player[$sys_plyerno][1] eq 'D' || $sys_plyerno == 50)) {
							$wk_msgwriteflg = 4;
						}
						if ($wk_logdata[1] == 6 && ($data_player[$sys_plyerno][3] eq 'FRE' || $data_player[$sys_plyerno][1] eq 'D' || $sys_plyerno == 50)) {
							$wk_msgwriteflg = 5;
						}
					}
					if ($wk_logdata[0] <= $data_vildata[2] - 1) {
						$wk_inputflg = 9;
					}
				}
			}
			# ���O
			if ($data_vildata[0] == 2 && $sys_logviewflg == 1 && $sys_storytype == "1"){
				if ($wk_logdata[0] != 99){
						if ($wk_logdata[1] <= 50 && $wk_logdata[1] != 3){
						$wk_msgwriteflg = 1;
					}
					if ($wk_logdata[1] == 3) {
						$wk_msgwriteflg = 3;
					}
				}
			}
			if ($wk_msgwriteflg == 1){
				print "<TR>";
				if ($wk_logdata[2] == 0) {
					print "<TD colspan=\"2\">$wk_logdata[3]</TD>";
				}
				if ($wk_logdata[2] >= 1 && $wk_logdata[2] < 23) {
					print "<TD valign=\"top\" width=\"140\"><FONT color=\"$wk_color[$data_player[$wk_logdata[2]][6]]\">��</FONT><b>$data_player[$wk_logdata[2]][7]</b>����</TD><TD>�u".$wk_logdata[3]."�v</TD>";
				}
				if ($wk_logdata[2] == 23) {
					print "<TD valign=\"top\"><FONT color=\"FF9900\">��<b>�Q�[���}�X�^�[</b></FONT></TD><TD>�u".$wk_logdata[3]."�v</TD>";
				}
				if ($wk_logdata[2] == 24) {
					print "<TD valign=\"top\">��<b>���l�B</b></TD><TD>".$wk_logdata[3]."</TD>";
				}
				if ($wk_logdata[2] >= 31 && $wk_logdata[2] <= 50) {
					print "<TD colspan=\"2\"><IMG src=\"".$imgpath;
					if ($wk_logdata[2] == 31) {
						print "msg.gif";
					}
					if ($wk_logdata[2] == 32) {
						print "ampm.gif";
					}
					if ($wk_logdata[2] == 33) {
						print "dead1.gif";
					}
					if ($wk_logdata[2] == 34) {
						print "dead2.gif";
					}
					if ($wk_logdata[2] == 35) {
						print "dead3.gif";
					}
					if ($wk_logdata[2] == 41) {
						print "hum.gif";
					}
					if ($wk_logdata[2] == 42) {
						print "wlf.gif";
					}
					if ($wk_logdata[2] == 43) {
						print "ura.gif";
					}
					if ($wk_logdata[2] == 44) {
						print "bgd.gif";
					}
					if ($wk_logdata[2] == 35) {
						print "\" width=\"40\" height=\"40\" border=\"0\"> $wk_logdata[3]</TD>";
					}else{
						print "\" width=\"32\" height=\"32\" border=\"0\"> $wk_logdata[3]</TD>";
					}
				}
				print "</TR>";
			}
			if ($wk_msgwriteflg == 2){
				print "<TR><TD valign=\"top\">���T�̉��i��<FONT color=\"#FF0000\"></TD><TD>�u�A�I�H�[�[���E�E�E�v</FONT></TD></TR>";
			}
			if ($wk_msgwriteflg == 3){
				print "<TR><TD valign=\"top\" width=\"140\">��<b>$data_player[$wk_logdata[2]][7]</b>����̉��i��</TD><TD><FONT color=\"#FF0000\">�u".$wk_logdata[3]."�v</FONT></TD></TR>";
			}
			if ($wk_msgwriteflg == 4){
				print "<TR><TD valign=\"top\" width=\"140\">��<b>$data_player[$wk_logdata[2]][7]</b>����̓Ƃ茾</TD><TD><FONT color=\"#6666AA\">�u".$wk_logdata[3]."�v</FONT></TD></TR>";
			}
			if ($wk_msgwriteflg == 5){
				print "<TR><TD valign=\"top\" width=\"140\">��<b>$data_player[$wk_logdata[2]][7]</b>����̉�b</TD><TD><FONT color=\"#33DD33\">�u".$wk_logdata[3]."�v</FONT></TD></TR>";
			}
		}else{
			$wk_inputflg = 9;
		}
	}
	close(IN);
	print "</TBODY></TABLE>\n";
}
#---------------------------------------------------------------------
# �R�}���h�I���ƃ��b�Z�[�W���͉��
#---------------------------------------------------------------------
sub disp_command{
	if($sys_plyerno == 60){
		return();
	}
	print "<TR><TD class=\"CLSTD01\">�� �s���ݒ�</TD></TR>\n";
	print "<TR><TD>\n";
	print "<TABLE cellpadding=\"0\" cellspacing=\"0\"><TBODY>";
	print "<TR><TD>�s�����e�F</TD>";
	print "<TD><SELECT name=\"COMMAND\">";
	if ($sys_plyerno <= 23) {
		if ($data_player[$sys_plyerno][1] eq 'A' || $data_vildata[0]==2) {
			if ($data_vildata[3]==1 || $data_vildata[0]==2){
				print "<OPTION value=\"MSG\">���@�� [�������e]</OPTION>\n";
				print "<OPTION value=\"MSG2\">�������� [�������e]</OPTION>\n";
				print "<OPTION value=\"MSG3\">�キ���� [�������e]</OPTION>\n";
			}
			if ($data_vildata[0]==0) {
				print "<OPTION value=\"NAMECHG\">���O�ύX(10���ȓ�) [�������e]</OPTION>\n";
				print "<OPTION value=\"PROFILE\">�v���t�B�[���C��(40���ȓ�) [�������e]</OPTION>\n";
			}
			if ($data_vildata[0]==1) {
				if ($data_vildata[3]==2 || $data_vildata[3]==4) {
					if ($data_player[$sys_plyerno][3] eq 'WLF'){
						print "<OPTION value=\"MSGWLF\">���i�� [�������e]</OPTION>\n";
					}
					if ($data_player[$sys_plyerno][3] eq 'WLF' && $data_player[$sys_plyerno][4] == 0){
						print "<OPTION value=\"KILL\">�E�@�� [�s���Ώ�]</OPTION>\n";
					}
					if ($data_player[$sys_plyerno][3] eq 'URA' && $data_player[$sys_plyerno][4] == 0){
						print "<OPTION value=\"FORTUNE\">��@�� [�s���Ώ�]</OPTION>\n";
					}
					if ($data_player[$sys_plyerno][3] eq 'BGD' && $data_vildata[2] >= 2 && $data_player[$sys_plyerno][4] == 0){
						print "<OPTION value=\"GUARD\">��@�q [�s���Ώ�]</OPTION>\n";
					}
					if ($data_player[$sys_plyerno][3] eq 'FRE'){
						print "<OPTION value=\"MSGFRE\">��@�b [�������e]</OPTION>\n";
					}
					print "<OPTION value=\"MSG1\">�Ƃ茾 [�������e]</OPTION>\n";
				}
				if (($data_vildata[3]==1 || $data_vildata[3]==3) && $data_player[$sys_plyerno][2] == 0){
					print "<OPTION value=\"VOTE\">���@�[ [�s���Ώ�]</OPTION>\n";
				}
				if ($data_vildata[3]==1 && $data_player[$sys_plyerno][9] == 0){
					print "<OPTION value=\"SILENT\">���@��</OPTION>\n";
				}
			}
		}else{
			print "<OPTION value=\"MSG0\">��@�b [�������e]</OPTION>\n";
		}
	}
	# �Ǘ���
	if($data_vildata[10]==0){
		if ($sys_plyerno == 50) {
			print "<OPTION value=\"MSGM0\">�Ǘ��җ�@�b [�������e]</OPTION>\n";
			print "<OPTION value=\"MSGM\">�Ǘ��҃��b�Z�[�W [�������e]</OPTION>\n";
			print "<OPTION value=\"VOTECHK\">���[�W�v</OPTION>\n";
			print "<OPTION value=\"SHOCK\">�ˑR�� [�s���Ώ�]</OPTION>\n";
			print "<OPTION value=\"REVOTE\">�ē��[</OPTION>\n";
			if ($data_vildata[0]==0){
				print "<OPTION value=\"START\">�Q�[���̊J�n(�d�ǖ���)</OPTION>\n";
				print "<OPTION value=\"STARTF\">�Q�[���̊J�n(�d�ǗL��)</OPTION>\n";
				print "<OPTION value=\"STARTFF\">�Q�[���̊J�n(�d�Ǒ�����)</OPTION>\n";
				print "<OPTION value=\"PLEYERDEL\">���l�o�^�̖���</OPTION>\n";
				print "<OPTION value=\"VILNAME\">�����ύX(8���ȓ�) [�������e]</OPTION>\n";
				print "<OPTION value=\"VILRULE\">���[���ύX(����) [�������e]</OPTION>\n";
			}
		}
	}elsif($sys_plyerno == 2 && $data_vildata[0]==0){
		print "<OPTION value=\"START\">�Q�[���̊J�n(�d�ǖ���)</OPTION>\n";
		print "<OPTION value=\"STARTF\">�Q�[���̊J�n(�d�ǗL��)</OPTION>\n";
		print "<OPTION value=\"STARTFF\">�Q�[���̊J�n(�d�Ǒ�����)</OPTION>\n";
		print "<OPTION value=\"PLEYERDEL\">���l�o�^�̖���</OPTION>\n";
		print "<OPTION value=\"VILNAME\">�����ύX(8���ȓ�) [�������e]</OPTION>\n";
		print "<OPTION value=\"VILRULE\">���[���ύX(����) [�������e]</OPTION>\n";
	
	}
	print "<OPTION value=\"\">�X�@�V</OPTION>\n";
	print "</SELECT></TD>";
	print "<TD width=\"6\"></TD>";
	print "<TD>�s���ΏہF</TD>";
	print "<TD><SELECT name=\"CMBPLAYER\">";
	print "<OPTION value=\"0\">----</OPTION>\n";
	for ($i = 1; $i <= $data_vildata[1]; $i++) {
		if ($i != $sys_plyerno && $data_player[$i][1] eq 'A') {
			print "<OPTION value=\"$data_player[$i][0]\">$data_player[$i][7]</OPTION>\n";
		}
	}
	print "</SELECT></TD></TR>";
	print "</TBODY></TABLE>";
	#print "�������e�F<INPUT type=\"text\" size=\"100\" name=\"TXTMSG\"><BR>\n";
	print "<TABLE cellpadding=\"0\" cellspacing=\"0\"><TBODY><TR>";
	print "<TD valign=\"top\">�������e�F</TD><TD><TEXTAREA rows=\"3\" cols=\"70\" name=\"comment\"></TEXTAREA></TD>\n";
	print "</TR></TBODY></TABLE>";
	print "<INPUT type=\"submit\" value=\"��̓��e�ōs��\">\n";
	print "</TD></TR>\n";
}
#---------------------------------------------------------------------
sub disp_msgdead{
	$wk_writeflg = 0;
	if ($data_vildata[0] == 1 && ($data_player[$sys_plyerno][1] eq 'D' || $sys_plyerno == 50)) {
		$wk_writeflg = 1;
	}
	if ($data_vildata[0] == 2 && $sys_logviewflg == 0){
		$wk_writeflg = 1;
	}
	if ($data_vildata[0] == 2 && $sys_logviewflg == 1 && $sys_storytype == "2"){
		$wk_writeflg = 2;
	}

	if ($wk_writeflg >= 1){
		print "<TR><TD class=\"CLSTD01\">�� �H��̊�</TD></TR>\n";
		print "<TR><TD class=\"CLSTD02\">\n";
		print "<TABLE cellpadding=\"0\" class=\"CLSTABLE2\"><TBODY>";
		open(IN, $file_log);
		$wk_msgcount = 0;
		$wk_inputflg = 0;
		while ($wk_inputflg == 0) {
			if ($_ = <IN>) {
				@wk_logdata = split(/,/, $_);
				if ($wk_logdata[0] == 99){
					$wk_msgcount++;
					print "<TR>\n";
					if ($wk_logdata[2] == 23) {
						print "<TD valign=\"top\"><FONT color=\"FF6600\">��<b>�Q�[���}�X�^�[</b></FONT></TD><TD>�u".$wk_logdata[3]."�v</TD>";
					}else{
						print "<TR><TD valign=\"top\" width=\"140\"><FONT color=\"$wk_color[$data_player[$wk_logdata[2]][6]]\">��</FONT><b>$data_player[$wk_logdata[2]][7]</b>����</TD><TD>�u".$wk_logdata[3]."�v</TD></TR>";
					}
					print "</TR>\n";
				}
				if ($wk_msgcount >= 20 && $wk_writeflg == 1){
					$wk_inputflg = 9;
				}
			}else{
				$wk_inputflg = 9;
			}
		}
		close(IN);
		print "</TBODY></TABLE>\n";
		print "</TD></TR>\n";
	}
}

sub disp_msgall{
	$wk_inputflg = 0;
	print "<TABLE cellpadding=\"0\"><TBODY>";
	open(IN, $file_log);
	while ($wk_inputflg == 0) {
		if ($_ = <IN>){
			$wk_msgwriteflg = 0;
			@wk_logdata = split(/,/, $_);
			
			# ���O
			if ($data_vildata[0] == 2 && $sys_logviewflg == 1 && $sys_storytype == "3"){
				if ($wk_logdata[0] != 99){
					if ($wk_logdata[1] <= 50 && $wk_logdata[1] != 3){
						$wk_msgwriteflg = 1;
					}
					if ($wk_logdata[1] == 3) {
						$wk_msgwriteflg = 3;
					}
				}else{
					$wk_msgwriteflg = 5;
				}
			}
			if ($wk_msgwriteflg == 1){
				print "<TR>";
				if ($wk_logdata[2] == 0) {
					print "<TD colspan=\"2\">$wk_logdata[3]</TD>";
				}
				if ($wk_logdata[2] >= 1 && $wk_logdata[2] < 23) {
					if ($wk_logdata[1] == 5){
						print "<TD valign=\"top\" width=\"140\">��<b>$data_player[$wk_logdata[2]][7]</b>����̓Ƃ茾</TD><TD><FONT color=\"#6666AA\">�u".$wk_logdata[3]."�v</FONT></TD>";
					}elsif ($wk_logdata[1] == 6){
						print "<TD valign=\"top\" width=\"140\">��<b>$data_player[$wk_logdata[2]][7]</b>����̉�b</TD><TD><FONT color=\"#33DD33\">�u".$wk_logdata[3]."�v</FONT></TD>";
					}else{
						print "<TD valign=\"top\" width=\"140\"><FONT color=\"$wk_color[$data_player[$wk_logdata[2]][6]]\">��</FONT><b>$data_player[$wk_logdata[2]][7]</b>����</TD><TD>�u".$wk_logdata[3]."�v</TD>";
					}
				}
				if ($wk_logdata[2] == 23) {
					print "<TD valign=\"top\"><FONT color=\"FF9900\">��<b>�Q�[���}�X�^�[</b></FONT></TD><TD>�u".$wk_logdata[3]."�v</TD>";
				}
				if ($wk_logdata[2] == 24) {
					print "<TD valign=\"top\">��<b>���l�B</b></TD><TD>".$wk_logdata[3]."</TD>";
				}
				if ($wk_logdata[2] >= 31 && $wk_logdata[2] <= 50) {
					print "<TD colspan=\"2\"><IMG src=\"".$imgpath;
					if ($wk_logdata[2] == 31) {
						print "msg.gif";
					}
					if ($wk_logdata[2] == 32) {
						print "ampm.gif";
					}
					if ($wk_logdata[2] == 33) {
						print "dead1.gif";
					}
					if ($wk_logdata[2] == 34) {
						print "dead2.gif";
					}
					if ($wk_logdata[2] == 35) {
						print "dead3.gif";
					}
					if ($wk_logdata[2] == 41) {
						print "hum.gif";
					}
					if ($wk_logdata[2] == 42) {
						print "wlf.gif";
					}
					if ($wk_logdata[2] == 43) {
						print "ura.gif";
					}
					if ($wk_logdata[2] == 44) {
						print "bgd.gif";
					}
					if ($wk_logdata[2] == 35) {
						print "\" width=\"40\" height=\"40\" border=\"0\"> $wk_logdata[3]</TD>";
					}else{
						print "\" width=\"32\" height=\"32\" border=\"0\"> $wk_logdata[3]</TD>";
					}
				}
				print "</TR>";
			}
			if ($wk_msgwriteflg == 2){
				print "<TR><TD valign=\"top\">���T�̉��i��<FONT color=\"#FF0000\"></TD><TD>�u�A�I�H�[�[���E�E�E�v</FONT></TD></TR>";
			}
			if ($wk_msgwriteflg == 3){
				print "<TR><TD valign=\"top\" width=\"140\">��<b>$data_player[$wk_logdata[2]][7]</b>����̉��i��</TD><TD><FONT color=\"#FF0000\">�u".$wk_logdata[3]."�v</FONT></TD></TR>";
			}
			if ($wk_msgwriteflg == 5){
				print "<TR bgcolor=\"#E3E3E3\">\n";
				if ($wk_logdata[2] == 23) {
					print "<TD valign=\"top\"><FONT color=\"FF6600\">��<b>�Q�[���}�X�^�[</b></FONT></TD><TD>�u".$wk_logdata[3]."�v</TD>";
				}else{
					print "<TD valign=\"top\" width=\"140\"><FONT color=\"$wk_color[$data_player[$wk_logdata[2]][6]]\">��</FONT><b>$data_player[$wk_logdata[2]][7]</b>����</TD><TD>�u".$wk_logdata[3]."�v</TD>";
				}
				print "</TR>\n";
			}
		}else{
			$wk_inputflg = 9;
		}
	}
	close(IN);
	print "</TBODY></TABLE>\n";
}
#---------------------------------------------------------------------
sub disp_foot{
	print "<TR><TD class=\"CLSTD01\"><A href=\"$return_url\">�߂�</A></TD></TR>\n";
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print "</TBODY></TABLE></FORM></BODY>\n";
	print "</HTML>\n";
}
#---------------------------------------------------------------------
# �������ʂ�\��
#---------------------------------------------------------------------
sub sub_judge{
	$wk_alivewlf = 0;
	$wk_alivehum = 0;
	$wk_alivefox = 0;
	for ($i = 1; $i <= $data_vildata[1]; $i++) {
		if ($data_player[$i][1] eq 'A'){
			if ($data_player[$i][3] eq 'WLF'){
				$wk_alivewlf++;
			}elsif ($data_player[$i][3] eq 'FOX'){
				$wk_alivefox++;
			}else{
				$wk_alivehum++;
			}
		}
	}
	if ($wk_alivewlf == 0) {
		if ($wk_alivefox == 0) {
			$data_vildata[0] = 2;
			$data_vildata[2]++;
			$data_vildata[3] = 1;
			$data_vildata[8] = 1;
			for ($i = 1; $i <= $data_vildata[1]; $i++) {
				if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'MAD' || $data_player[$i][3] eq 'FOX'){
					$data_player[$i][5] = 'L';
				}else{
					if ($data_player[$i][1] eq 'D'){
						$data_player[$i][5] = 'W';		#���S���Ă��鑺�l������
					}else{
						$data_player[$i][5] = 'W';		#�����҂̂ݏ����҂Ƃ���
					}
				}
			}
		
			&msg_write($data_vildata[2], 1, 0,"<FONT size=\"+1\">�l�T�̌������₷�邱�Ƃɐ������܂����I</FONT>");
			&msg_write($data_vildata[2], 1, 41,"<FONT size=\"+2\" color=\"#FF6600\">�u$chr_hum�v�̏����ł��I</FONT>");
		}else{
			$data_vildata[0] = 2;
			$data_vildata[2]++;
			$data_vildata[3] = 1;
			$data_vildata[8] = 2;
			for ($i = 1; $i <= $data_vildata[1]; $i++) {
				if ($data_player[$i][3] eq 'FOX'){
					$data_player[$i][5] = 'W';
				}else{
					$data_player[$i][5] = 'L';
				}
			}
		
			&msg_write($data_vildata[2], 1, 0,"<FONT size=\"+1\">�l�T�����Ȃ��Ȃ������A��̓G�Ȃǂ������Ȃ��B</FONT>");
			&msg_write($data_vildata[2], 1, 41,"<FONT size=\"+2\" color=\"#FF6600\">�u$chr_fox�v�̏����ł��I</FONT>");
		}
	}
	if ($wk_alivewlf >= $wk_alivehum) {
		if ($wk_alivefox == 0) {
			$data_vildata[0] = 2;
			$data_vildata[2]++;
			$data_vildata[3] = 1;
			$data_vildata[8] = 3;
			for ($i = 1; $i <= $data_vildata[1]; $i++) {
				if ($data_player[$i][3] eq 'WLF' || $data_player[$i][3] eq 'MAD'){
					if ($data_player[$i][1] eq 'D'){
						$data_player[$i][5] = 'W';		#���S���Ă���l�T������
					}else{
						$data_player[$i][5] = 'W';		#�����҂̂ݏ����҂Ƃ���
					}
				}else{
					$data_player[$i][5] = 'L';
					if($data_player[$i][1] eq 'A'){
						$data_player[$i][1] = 'D';	#�s�k�������l�͐H���E����Ď��S
						&msg_write($data_vildata[2], 1, 34,"<b>$data_player[$i][7]</b>�����<FONT color=\"#ff0000\">���̂��������l�T�ɏP���ĎE���ꂽ�E�E�E�B</FONT>");
					}
				}
			}
			
			&msg_write($data_vildata[2], 1, 0,"<FONT size=\"+1\">�Ō�̈�l��H���E���Ɛl�T�B�͎��̊l�������߂đ�����ɂ����E�E�E�B</FONT>");
			&msg_write($data_vildata[2], 1, 42,"<FONT size=\"+2\" color=\"#DD0000\">�u$chr_wlf�v�̏����ł��I</FONT>");
		}else{
			$data_vildata[0] = 2;
			$data_vildata[2]++;
			$data_vildata[3] = 1;
			$data_vildata[8] = 4;
			for ($i = 1; $i <= $data_vildata[1]; $i++) {
				if ($data_player[$i][3] eq 'FOX'){
					$data_player[$i][5] = 'W';
				}else{
					$data_player[$i][5] = 'L';
				}
			}
		
			&msg_write($data_vildata[2], 1, 0,"<FONT size=\"+1\">�}�k�P�Ȑl�T�ǂ����x�����ƂȂǗe�Ղ����Ƃ��B</FONT>");
			&msg_write($data_vildata[2], 1, 41,"<FONT size=\"+2\" color=\"#FF6600\">�u$chr_fox�v�̏����ł��I</FONT>");
		}
	}
}
#---------------------------------------------------------------------
# Cookie�̒l��ǂݏo��
#
sub getCookie {
	local($xx, $name, $value);
	foreach $xx (split(/; */, $ENV{'HTTP_COOKIE'})) {
		($name, $value) = split(/=/, $xx);
		$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
		$COOKIE{$name} = $value;
	}
}

#---------------------------------------------------------------------
# Cookie�ɒl���������ނ��߂�Set-Cookie:�w�b�_�𐶐�����
#
sub setCookie {
	local($tmp, $val);
	$val = $_[1];
	$val =~ s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
	$tmp = "Set-Cookie: ";
	$tmp .= "$_[0]=$val; ";
	$tmp .= "expires=Thu, 1-Jan-2030 00:00:00 GMT;\n";
	return($tmp);
}
sub sysadoin{

	open(IN, $sys_path_bak);
	$wk_count = 1;
	$sys_ID_COUNT = 0;
	while (<IN>) {
		$value = $_;
		$value =~ s/\n//g;
		
		@wk_player = split(/,/, $value);
		$sys_ID[$wk_count] = $wk_player[0];
		$sys_pass[$wk_count] = $wk_player[1];
		$sys_name[$wk_count] = $wk_player[2];
		$wk_count++;
		$sys_ID_COUNT++;
		}
	close(IN);
}

sub randomarr{
	$size = shift;
	@rarr = (0);
	
	for my $i (1..$size){
		push @rarr, $i;
	}
	
	for my $i (1..$size){
		my $j = int(rand($size - $i) + $i);
		my $temp = $rarr[$i];
		$rarr[$i] = $rarr[$j];
		$rarr[$j] = $temp;
	}
	
	return @rarr;
}

1;