#================================================
# �Ղ��̊J�n�E�I���Ŏg���郂�W���[��
#================================================

#================================================
# ��ȌĂяo����
# ./lib/_world_reset.cgi
# �����I�ɌĂ΂��̂ňӎ����ă��[�h����K�v�Ȃ�
#================================================

# �Ղ��̊J�n�ƏI���ɕR�Â��̂� 1 ���󂯂�
use constant FESTIVAL_TYPE => {
	'kouhaku' => 1,
	'sangokusi' => 3,
	'konran' => 5,
	'sessoku' => 7,
	'dokuritu' => 9
};
# �Ղ��̖��̂ƁA�J�n���Ȃ� 1 �I���� �Ȃ� 0 ���w�肷��
sub festival_type {
	my ($festival_name, $is_start) = @_;
	return FESTIVAL_TYPE->{$festival_name} + $is_start;
}

# �Ղ����ɒǉ�����鍑�̐��E���́E�����E���F�̒�`
use constant FESTIVAL_COUNTRY_PROPERTY => {
	'kouhaku' => [2, 75000, ["���̂��̎R", "�����̂��̗�"], ["#ffffff", "#ff0000"]],
	'sangokusi' => [3, 5, ["�", "��", "�"], ["#4444ff", "#ff4444", "#44ff44"]]
#	'sangokusi' => [3, 50000, ["�", "��", "�"], ["#4444ff", "#ff4444", "#44ff44"]]
};

# �s��ՓV����
my $country_name_hug_1 = "�����̂��̗�";
my $country_name_hug_2 = "���̂��̎R";

# �O���u����
my $country_name_san_1 = "�";
my $country_name_san_2 = "��";
my $country_name_san_3 = "�";

# �w�肳�ꂽ�Ղ��p�̍���ǉ������̏�̊J�n�t���O��Ԃ�
# �ǉ�����鍑�̏��� FESTIVAL_COUNTRY_PROPERTY �Œ�`���Ă���
sub add_festival_country {
	my $festival_name = shift;

	my $country_num = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[0];
	$w{country} += $country_num;
	my $max_c = int($w{player} / $country_num) + 3;
	for my $i ($w{country}-($country_num-1)..$w{country}){
		mkdir "$logdir/$i" or &error("$logdir/$i ̫��ނ����܂���ł���") unless -d "$logdir/$i";
		for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
			my $output_file = "$logdir/$i/$file_name.cgi";
			next if -f $output_file;
			open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
			close $fh;
			chmod $chmod, $output_file;
		}
		for my $file_name (qw/leader member/) {
			my $output_file = "$logdir/$i/$file_name.cgi";
			open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
			close $fh;
			chmod $chmod, $output_file;
		}
		&add_npc_data($i);
		# create union file
		for my $j (1 .. $i-1) {
			my $file_name = "$logdir/union/${j}_${i}";
			$w{ "f_${j}_${i}" } = -99;
			$w{ "p_${j}_${i}" } = 2;
			next if -f "$file_name.cgi";
			open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ̧�ق����܂���");
			close $fh;
			chmod $chmod, "$file_name.cgi";
			open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ̧�ق����܂���");
			close $fh2;
			chmod $chmod, "${file_name}_log.cgi";
			open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ̧�ق����܂���");
			close $fh3;
			chmod $chmod, "${file_name}_member.cgi";
		}
		unless (-f "$htmldir/$i.html") {
			open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ̧�ق����܂���");
			close $fh_h;
		}

		my $num = $i-($w{country}+1-$country_num);
		$cs{name}[$i]     = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[2][$num];
		$cs{color}[$i]    = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[3][$num];
		$cs{member}[$i]   = 0;
		$cs{win_c}[$i]    = 999;
		$cs{tax}[$i]      = 99;
		$cs{strong}[$i]   = FESTIVAL_COUNTRY_PROPERTY->{$festival_name}[1];
		$cs{food}[$i]     = 0;
		$cs{money}[$i]    = 0;
		$cs{soldier}[$i]  = 0;
		$cs{state}[$i]    = 0;
		$cs{capacity}[$i] = $max_c;
		$cs{is_die}[$i]   = 0;
		my @lines = &get_countries_mes();
		if ($w{country} > @lines - $country_num) {
			open my $fh9, ">> $logdir/countries_mes.cgi";
			print $fh9 "<>$default_icon<>\n";
			print $fh9 "<>$default_icon<>\n";
			close $fh9;
		}
	}

	for my $i (1 .. $w{country}-$country_num) {
		$cs{strong}[$i]   = 0;
		$cs{food}[$i]     = 0;
		$cs{money}[$i]    = 0;
		$cs{soldier}[$i]  = 0;
		$cs{state}[$i]    = 0;
		$cs{capacity}[$i] = 0;
		$cs{is_die}[$i]   = 1;

		for my $j ($i+1 .. $w{country}-$country_num) {
			$w{ "f_${i}_${j}" } = -99;
			$w{ "p_${i}_${j}" } = 2;
		}

		$cs{old_ceo}[$i] = $cs{ceo}[$i];
		$cs{ceo}[$i] = '';
		
		open my $fh, "> $logdir/$i/leader.cgi";
		close $fh;
	}

	return &festival_type($festival_name, 1);
}

sub player_migrate {
	my $type = shift;

	if ($type == &festival_type('kouhaku', 1)) {# �s��ՓV�ݒ�
		# �o�b�N�A�b�v�쐬
		for my $i (0 .. $w{country} - 2) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			rcopy($from, $backup);
		}
		my $from = "$logdir/countries.cgi";
		my $backup = "$logdir/countries_backup.cgi";
		rcopy($from, $backup);
		
		require "./lib/move_player.cgi";
		@sedais=([0, 0],[0, 0],[0, 0],[0, 0]);
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my $j = int(rand(2));
			my $s;
			if($m{sedai} <= 5){
				$s = 0;
			}elsif($m{sedai} <= 10){
				$s = 1;
			}elsif($m{sedai} <= 15){
				$s = 2;
			}else{
				$s = 3;
			}
			for my $cj (0..1) {
				if ($sedais[$s][$j] > $sedais[$s][$cj] + 2) {
					$j = $cj;
				}
			}
			++$sedais[$s][$j];
			&move_player($you_datas{name}, $you_datas{country}, $w{country} - $j);
			if ($you_datas{name} eq $m{name}){
				$m{country} = $w{country} - $j;
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c_t"} = $m{$k."_c"};
					$m{$k."_c"} = 0;
				}
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', $w{country} - $j);
				for my $k (qw/war dom pro mil/) {
					&regist_you_data($you_datas{name}, $k."_c_t", $you_datas{$k."_c"});
					&regist_you_data($you_datas{name}, $k."_c", 0);
				}
			}
		}
		closedir $dh;
	}
	elsif ($type == &festival_type('kouhaku', 0)) {# �s��ՓV����
		require "./lib/move_player.cgi";
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my($c1, $c2) = split /,/, $w{win_countries};
			if($c1 eq $you_datas{country} || $c2 eq $you_datas{country}){
				require './lib/shopping_offertory_box.cgi';
				for my $k (qw/war dom pro mil ceo/) {
					if ($cs{$k}[$you_datas{country}] eq $you_datas{name}) {
						&send_god_item(5, $cs{$k}[$you_datas{country}]);
					}
				}
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}else {
				&regist_you_data($you_datas{name}, 'shogo', $cs{name}[$you_datas{country}] . "(��)");
				&regist_you_data($you_datas{name},'trick_time',$time + 3600 * 24 * 3);
				&regist_you_data($you_datas{name},'shogo_t',$datas{shogo});
			}
			
			# �l�o��������
			&move_player($you_datas{name}, $you_datas{country}, 0);
			if ($you_datas{name} eq $m{name}){
				$m{country} = 0;
				$y{country} = 0;
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c"} = $m{$k."_c_t"};
					$m{$k."_c_t"} = 0;
				}
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', 0);
				&regist_you_data($you_datas{name}, 'y_country', 0);
				for my $k (qw/war dom pro mil/) {
					&regist_you_data($you_datas{name}, $k."_c", $you_datas{$k."_c_t"});
					&regist_you_data($you_datas{name}, $k."_c_t", 0);
				}
			}
		}
		closedir $dh;
		
		# ���t�H���_�폜
		for my $i ($w{country}+2, $w{country}+1) {
			my $from = "$logdir/$i";
			my $num = rmtree($from);
			
			my @lines = ();
			open my $fh, "+< $logdir/countries_mes.cgi";
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				push @lines, $line;
			}
			pop @lines while @lines > $w{country} + 1;
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
		
		$w{country} -= 2;
		
		# ���f�[�^����
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			my $num = rmtree($from);
			rcopy($backup, $from);
		}
		
		my $i = 1;
		open my $fh, "< $logdir/countries_backup.cgi" or &error("���ް����ǂݍ��߂܂���");
		my $world_line = <$fh>;
		while (my $line = <$fh>) {
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				if ($k eq 'name' || $k eq 'color' || $k eq 'win_c' || $k eq 'old_ceo' || $k eq 'ceo_continue') {
					$cs{$k}[$i] = $v;
				}
			}
			++$i;
		}
		close $fh;
	}
	elsif ($type == &festival_type('sangokusi', 1)) {# �O���u�ݒ�
		# �o�b�N�A�b�v�쐬
		for my $i (0 .. $w{country} - 3) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			rcopy($from, $backup);
		}
		my $from = "$logdir/countries.cgi";
		my $backup = "$logdir/countries_backup.cgi";
		rcopy($from, $backup);
		
		require "./lib/move_player.cgi";
		@sedais=([0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]);
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my $j = int(rand(3));
			my $s;
			if($m{sedai} <= 5){
				$s = 0;
			}elsif($m{sedai} <= 10){
				$s = 1;
			}elsif($m{sedai} <= 15){
				$s = 2;
			}else{
				$s = 3;
			}
			for my $cj (0..2) {
				if ($sedais[$s][$j] > $sedais[$s][$cj] + 2) {
					$j = $cj;
				}
			}
			++$sedais[$s][$j];
			&move_player($you_datas{name}, $you_datas{country}, $w{country} - $j);
			if ($you_datas{name} eq $m{name}){
				$m{country} = $w{country} - $j;
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c_t"} = $m{$k."_c"};
					$m{$k."_c"} = 0;
				}
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', $w{country} - $j);
				for my $k (qw/war dom pro mil/) {
					&regist_you_data($you_datas{name}, $k."_c_t", $you_datas{$k."_c"});
					&regist_you_data($you_datas{name}, $k."_c", 0);
				}
			}
		}
		closedir $dh;
	}
	elsif ($type == &festival_type('sangokusi', 0)){# �O���u����
		require "./lib/move_player.cgi";
		require "./lib/shopping_offertory_box.cgi";
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my($c1, $c2) = split /,/, $w{win_countries};
			if($c1 eq $you_datas{country} || $c2 eq $you_datas{country}){
				for my $k (qw/war dom pro mil ceo/) {
					if ($cs{$k}[$you_datas{country}] eq $you_datas{name}) {
						&send_god_item(5, $cs{$k}[$you_datas{country}]);
					}
				}
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}else {
				&regist_you_data($you_datas{name}, 'shogo', $cs{name}[$you_datas{country}] . "(��)");
				&regist_you_data($you_datas{name},'trick_time',$time + 3600 * 24 * 3);
				&regist_you_data($you_datas{name},'shogo_t',$datas{shogo});
			}
			
			# �l�o��������
			&move_player($you_datas{name}, $you_datas{country}, 0);
			if ($you_datas{name} eq $m{name}){
				$m{country} = 0;
				$y{country} = 0;
				for my $k (qw/war dom pro mil/) {
					$m{$k."_c"} = $m{$k."_c_t"};
					$m{$k."_c_t"} = 0;
				}
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', 0);
				&regist_you_data($you_datas{name}, 'y_country', 0);
				for my $k (qw/war dom pro mil/) {
					&regist_you_data($you_datas{name}, $k."_c", $you_datas{$k."_c_t"});
					&regist_you_data($you_datas{name}, $k."_c_t", 0);
				}
			}
		}
		closedir $dh;
		
		# ���t�H���_�폜
		for my $i ($w{country}+3, $w{country}+2, $w{country}+1) {
			my $from = "$logdir/$i";
			my $num = rmtree($from);
			
			my @lines = ();
			open my $fh, "+< $logdir/countries_mes.cgi";
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				push @lines, $line;
			}
			pop @lines if @lines > $w{country} + 1;
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
		
		$w{country} -= 3;
		
		# ���f�[�^����
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			my $num = rmtree($from);
			rcopy($backup, $from);
		}
		
		my $i = 1;
		open my $fh, "< $logdir/countries_backup.cgi" or &error("���ް����ǂݍ��߂܂���");
		my $world_line = <$fh>;
		while (my $line = <$fh>) {
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				if ($k eq 'name' || $k eq 'color' || $k eq 'win_c' || $k eq 'old_ceo' || $k eq 'ceo_continue') {
					$cs{$k}[$i] = $v;
				}
			}
			++$i;
		}
		close $fh;
	}
	elsif ($type == &festival_type('konran', 1) || $type == &festival_type('sessoku', 1)) {# �����ݒ�
		# ��U�l�o��������
		require "./lib/move_player.cgi";
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			next if $you_datas{shuffle};
			
			if($you_datas{name} eq $m{name}){
				&move_player($m{name}, $m{country}, 0);
				$m{country} = 0;
				&write_user;
			}
			&move_player($you_datas{name}, $you_datas{country}, 0);
			&regist_you_data($you_datas{name}, 'country', 0);
		}
		closedir $dh;
		
		# �U�蕪��
		require "./lib/move_player.cgi";
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			my $j = int(rand($w{country}) + 1);
			for my $cj (1..$w{country}) {
				if ($cs{member}[$j] > $cs{member}[$cj] + 2) {
					$j = $cj;
				}
			}
			&move_player($you_datas{name}, $you_datas{country}, $j);
			if ($you_datas{name} eq $m{name}){
				$m{country} = $j;
				&write_user;
			} else {
				&regist_you_data($you_datas{name}, 'country', $j);
			}
		}
		closedir $dh;
	}
	elsif ($type == &festival_type('konran', 0) || $type == &festival_type('sessoku', 0)) {#��������
		require "./lib/move_player.cgi";
		opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
		while (my $pid = readdir $dh) {
			next if $pid =~ /\./;
			next if $pid =~ /backup/;
			my %you_datas = &get_you_datas($pid, 1);
			
			if($you_datas{name} eq $m{name}){
				&move_player($m{name}, $m{country}, 0);
				$m{country} = 0;
				&write_user;
			}
			&move_player($you_datas{name}, $you_datas{country}, 0);
			&regist_you_data($you_datas{name}, 'country', 0);

			my($c1, $c2) = split /,/, $w{win_countries};
			if ($c1 eq $you_datas{country} || $c2 eq $you_datas{country}) {
				open my $fh, ">> $userdir/$pid/ex_c.cgi";
				print $fh "fes_c<>1<>\n";
				close $fh;
				
				&send_item($you_datas{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
			}
		}
		closedir $dh;
	}
	elsif ($type == &festival_type('dokuritu', 1)) {# �Ɨ��ݒ�
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			rcopy($from, $backup);
		}
		my $from = "$logdir/countries.cgi";
		my $backup = "$logdir/countries_backup.cgi";
		rcopy($from, $backup);
	}
	elsif ($type == &festival_type('dokuritu', 0)) {# �Ɨ�����
		require "./lib/move_player.cgi";
		for my $i (1..$w{country}) {
			my @names = &get_country_members($i);
			for my $name (@names) {
				$name =~ tr/\x0D\x0A//d;
				if($name eq $m{name}){
					&move_player($m{name}, $i, 0);
					$m{country} = 0;
					&write_user;
				}
				my %you_datas = &get_you_datas($name);
				&move_player($name, $i, 0);
				&regist_you_data($name, 'country', 0);

				my($c1, $c2) = split /,/, $w{win_countries};
				if ($c1 eq $i || $c2 eq $i) {
					require './lib/shopping_offertory_box.cgi';
					if ($cs{ceo}[$you_datas{country}] eq $you_datas{name}) {
						&send_god_item(7, $cs{ceo}[$you_datas{country}]) for (1..2);
					}
					my $n_id = unpack 'H*', $name;
					open my $fh, ">> $userdir/$n_id/ex_c.cgi";
					print $fh "fes_c<>1<>\n";
					close $fh;
					
					&send_item($name, 2, int(rand($#eggs)+1), 0, 0, 1);
				}
			}
		}
		for my $i (0 .. $w{country}) {
			my $from = "$logdir/$i";
			my $backup = $from . "_backup";
			my $num = rmtree($from);
			rcopy($backup, $from);
		}
		
		my $i = 1;
		open my $fh, "< $logdir/countries_backup.cgi" or &error("���ް����ǂݍ��߂܂���");
		my $world_line = <$fh>;
		while (my $line = <$fh>) {
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				if ($k eq 'name' || $k eq 'color' || $k eq 'win_c' || $k eq 'old_ceo' || $k eq 'ceo_continue') {
					$cs{$k}[$i] = $v;
				}
			}
			$w{country} = $i;
			++$i;
		}
		close $fh;
		
		&cs_data_repair;# ???
	}
	&cs_data_repair;
}

sub wt_c_reset {
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $pid = readdir $dh) {
		next if $pid =~ /\./;
		next if $pid =~ /backup/;
		my %you_datas = &get_you_datas($pid, 1);

		if ($you_datas{name} eq $m{name}){
			$m{wt_c_latest} = $m{wt_c};
			$m{wt_c} = 0;
			&write_user;
		} else {
			&regist_you_data($you_datas{name}, "wt_c_latest", $you_datas{wt_c});
			&regist_you_data($you_datas{name}, "wt_c", 0);
		}
	}
	closedir $dh;
}

1;