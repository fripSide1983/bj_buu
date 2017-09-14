#================================================
# ��ǃV�X�e�� Created by nanamie
#================================================

# require './lib/_use_pet_log.cgi';

# 23 ���ЁA�޳��A�����A�ٽ�A��޽�Aɱ�AҼ��A���ρA���āA��ށA̪��فA
# �õ�A�߽āA���̪�Aسާ�A��پށA��݁A��ӁA¸�ЁA����݁A�ٶ�A������A۽���
@country_pets = (61, 64..71, 134..145, 151..152);

#================================================
# �߯Ă̐�����۸ނ��擾
#================================================
sub read_use_pet_log {
	my ($id, $pet) = @_;
	my $this_file = "$userdir/$id/use_pet_log.cgi";
	my %pet_logs;

	unless (-f "$this_file") {
		open my $fh1, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
		close $fh1;
	}

	open my $fh2, "< $this_file" or &error("�߯Ă̐�����۸�̧�ق��J���܂���");
	my $line = <$fh2>;
	close $fh2;

	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$pet_logs{$k} = $v if !defined($pet) || $pet && $pet == $k; # �����o�O�񍐂���� !defined �������o���͂��邯�Ǘ��R�Y�ꂽ�c ����`�ł���K�v����Ȃ���悭������Ȃ�
	}

	return $pet ? $pet_logs{$pet} : %pet_logs;
}

#================================================
# �߯Ă̐�����۸ނ�ݒ�
#================================================
sub write_use_pet_log {
	my ($id, $pet) = @_;
	my $this_file = "$userdir/$id/use_pet_log.cgi";
	my %pet_logs;

	if (-f "$this_file") {
		open my $fh, "+< $this_file" or &error("$this_file ̧�ق��J���܂���");
		eval { flock $fh, 2; };
		my $line = <$fh>;

		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$pet_logs{$k} = $v;
		}

		$pet_logs{$pet}++;

		$line = '';
		for my $k (keys(%pet_logs)) {
			$line .= "$k;$pet_logs{$k}<>";
		}

		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh $line;
		close $fh;
	}
	else {
		open my $fh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
		print $fh "$pet;1<>";
		close $fh;
	}
}

#================================================
# �߯Ă̐�����۸ނ�\���i��ڲ԰�����̨�ٗp�j
#================================================
sub show_use_pet_log {
	my $id = shift;
	my %pet_logs = &read_use_pet_log($id);

	for $pet (0 .. $#pets) {
		print qq|<li>$pets[$pet][1] $pet_logs{$pet}��</li><hr size="1">\n| if defined($pet_logs{$pet});
	}
}

1;
