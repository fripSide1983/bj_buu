sub run {
	my ($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|$member_c �l���{����|;
	print qq|<CENTER>\n|;
	print qq|<TABLE cellspacing="4" border="1">\n|;
	print qq|  <TBODY>\n|;
	print qq|    <TR>\n|;
	print qq|      <TD colspan="2" align="center"><FONT size="+3">�u���͐l�T�Ȃ��H�v</FONT></TD>\n|;
	print qq|    </TR>\n|;
	print qq|    <TR>\n|;
	print qq|      <TD colspan="2" height="5" bgcolor="#333333"></TD>\n|;
	print qq|    </TR>\n|;
	print qq|    <TR>\n|;
	print qq|      <TD align="center" rowspan="2" valign="top">\n|;
	print qq|      <TABLE cellpadding="4" cellspacing="1" bgcolor="#333333">\n|;
	print qq|        <TBODY>\n|;
	print qq|          <TR>\n|;
	print qq|            <TD align="center"><B>menu</B></TD>\n|;
	print qq|          </TR>\n|;
	print qq|          <TR>\n|;
	print qq|            <TD bgcolor="#ffffff" align="center"><A href="rule.htm"><B>���[��������</B></A><BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <A href="jinro_buu.cgi?subf=entry&id=$id&pass=$pass" target="_top"><B>�����o�^</B><BR>\n|;
	print qq|            �i�v���C���[�o�^�j</A><BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <A href="jinro_buu.cgi?subf=room&id=$id&pass=$pass"><B>���ɍs��</B><BR>\n|;
	print qq|            �i���O�C���j</A><BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <A href="jinro_buu.cgi?subf=log&id=$id&pass=$pass"><B>�ߋ��̋L�^</B><BR>\n|;
	print qq|            �i���O�Q�Ɓj</A><BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <A href="log_buu.cgi?id=$id&pass=$pass"><B>�ߋ��̋L�^</B><BR>\n|;
	print qq|            �i�폜�Q�Ɓj</A><BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <BR>\n|;
	print qq|            <A href="jinro_buu.cgi?subf=master&id=$id&pass=$pass">���̍쐬/�폜<BR>\n|;
	print qq|            </A></TD>\n|;
	print qq|          </TR>\n|;
	print qq|        </TBODY>\n|;
	print qq|      </TABLE>\n|;
	print qq|      </TD>\n|;
	print qq|      <TD><B>���Q�[���̊J�n���@</B></TD>\n|;
	print qq|    </TR>\n|;
	print qq|    <TR>\n|;
	print qq|      <TD valign="top">�P�D���̃��j���[����u�����o�^�v��I��œo�^��ʂɂ����e���ڂ���͂��ēo�^�������Ă��������B<BR>\n|;
	print qq|      �����łɃQ�[�����J�n����Ă���ꍇ�A������22������ꍇ�͓o�^�ł��܂���B<BR>\n|;
	print qq|      �Q�D���̃��j���[����u���ɍs���v��I�����܂��B<BR>\n|;
	print qq|      �R�D���ɓ���܂��B<BR>\n|;
	print qq|      �S�D�l��������Ă��ǏW�����ƊǗ��҂����f����ƃQ�[�����J�n���܂�<BR>\n|;
	print qq|      �@�@����܂ł͓K���ɎG�k���Ă��Ă�������<BR>\n|;
	print qq|      �T�D�Ǘ��҂��Q�[���J�n��錾���܂��B<BR>\n|;
	print qq|      �@�@�Q�[�����J�n�����Ǝ����I�Ɋe���ɖ�ڂ�����U���܂��B<BR>\n|;
	print qq|      <BR>\n|;
	print qq|      </TD>\n|;
	print qq|    </TR>\n|;
	print qq|  </TBODY>\n|;
	print qq|</TABLE>\n|;
	print qq|</CENTER>\n|;
	print qq|</BODY>\n|;
	print qq|</HTML>\n|;
}

sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	push @members, "<>\n";
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr, $mturn, $mvalue) = split /<>/, $line;
		if ($time - $limit_member_time > $mtime) {
			next;
		}
		next if $sames{$mname}++; # �����l�Ȃ玟
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
			$is_find = 1;
		}
		else {
			push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>\n";
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>$m{c_turn}<>$m{c_value}<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members - 1;

	return ($member_c, $member);
}

1;