#================================================
# �ڐЁEհ�ް�폜�E���챲�ݍ폜 Created by Merino
#================================================
# admin.cgi�Acountry_move.cgi�Aprison.cgi�Alogin.cgi�Awar.cgi�ȂǂŎg�p
# ���ް̧�ق���ړ��B��\�Ȃ疼�O����菜��
# ������ؽĂ��ړ� or �폜���邾���Ȃ̂ŁA�ړ�����ꍇ����ڲ԰�ް���ύX���鏈�����K�v
#   ��F$m{country} = ��No; �܂��� &regist_you_data('���O', 'country', '��No');�Ȃ�


#================================================
# member.cgi��ύX����
#================================================
sub move_player {
	my($name, $from_country, $to_country) = @_;

	# �����ްؽĂ����菜���A�ړ���ɒǉ�
	my %sames = ();
	my @lines = ();
	my $is_find = 0;
	open my $fh, "+< $logdir/$from_country/member.cgi" or &error("$logdir/$from_country/member.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;

		# �������O�̐l����������ꍇ
		next if ++$sames{$line} > 1;
		
		if ($line eq $name) {
			$is_find = 1;
			next;
		}
		push @lines, "$line\n";
	}
	if ($is_find) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		--$cs{member}[$from_country];
	}
	close $fh;
	
	my $p_id = unpack 'H*', $name;
	my %datas = ();
	%datas = &get_you_datas($p_id, 1) if -f "$userdir/$p_id/user.cgi";
	
	unless ($from_country eq '0') {
		# ���[���Ă���̂������
		&check_vote(%datas) if $datas{vote};
	
		# ��\�Ҍn��菜��
		for my $key (qw/ceo war dom mil pro/) {
			if ($cs{$key}[$from_country] eq $name) {
				$cs{$key}[$from_country] = '';
				if($key ne 'ceo'){
					$m{$key.'_c'} = int($m{$key.'_c'} / 2);
					$cs{$key.'_c'}[$from_country] = 0;
				}
			}
		}
	}

	if ($to_country eq 'del') {
		&delete_user($p_id, %datas) if -d "$userdir/$p_id";
	
		&write_entry_news("$name�Ƃ����҂�����܂���");
	}
	else {
		open my $fh9, ">> $logdir/$to_country/member.cgi" or &error("$logdir/$to_country/member.cgi̧�ق��J���܂���");
		print $fh9 "$name\n";
		close $fh9;
		++$cs{member}[$to_country];
	}
#	&refresh_new_commer;
	&write_cs;
}


#================================================
# ���[���Ă����炻�̕[������
#================================================
sub check_vote {
	my %datas = @_;
	
	my @lines = ();
	open my $fh, "+< $logdir/$datas{country}/leader.cgi";
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($vname, $vote) = split /<>/, $line;
		next if $datas{name} eq $vname; # ����₵�Ă����ꍇ�͏���

		if ($datas{vote} eq $vname) { # ��[�폜
			--$vote;
			$line = "$vname<>$vote<>\n";
		}
		push @lines, $line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}


#================================================
# հ�ް�ް����폜
#================================================
sub delete_user {
	my($p_id, %datas) = @_;
	
	opendir my $dh, "$userdir/$p_id";
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		
		if (-d "$userdir/$p_id/$file_name") {
			opendir my $dh2, "$userdir/$p_id/$file_name";
			while (my $file_name2 = readdir $dh2) {
				next if $file_name2 =~ /^\./;
				unlink "$userdir/$p_id/$file_name/$file_name2";
			}
			closedir $dh2;
			
			rmdir "$userdir/$p_id/$file_name";
		}
		else {
			unlink "$userdir/$p_id/$file_name";
		}
	}
	closedir $dh;
	rmdir "$userdir/$p_id";
	--$w{player};
	
	# ���챲�ݍ폜
	unlink "$icondir/$datas{icon}" if $datas{icon} ne $default_icon && -f "$icondir/$datas{icon}";
}


1; # �폜�s��
