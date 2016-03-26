#=================================================
# [�Í�]NPC��p��۸��� Created by Merino
#=================================================
# ���x�������l��NPC���Ɏd�����Ȃ��悤�Ɏd�����O(�l)
$max_npc_old_member = $w{player} * 0.2 > 10 ? 10: $w{player} * 0.2;
# NPC��(�擪5���͐푈�����Ƃ��ɏo������)
my @npc_names = (qw/vipqiv(NPC) kirito(NPC) �T�̉ƒ��w(NPC) pigure(NPC) �E�F��(NPC) vipqiv(NPC) DT(NPC) �n��(NPC) �A�V�����C(NPC) �S�~�N�Y(NPC)/);
#                   0             1          2           3         4
my $npc_cap = 6;# ���S��NPC���ɂ������ꍇ�� ���̐����� 0 �ɂ���
# NPC������
# �����p�ϐ�
my $ave_add = 0; # ������v�Z�̉��ʁi���₷�ƈÍ��������Ȃ�܂��B�ύX�񐄏��j
my $max_par = 0.5; # ���ʂ̍��̒���̂ǂ̂��炢�̊����Ŕ������Œ�ɂ��邩
# ����������Ƃ����ɍŒᔽ�����ɏグ������ƈÍ����l���������Ƃ��ɍŒᔽ�����ɂȂ炸�����Ȃ肷���܂��B�T�d�ɕύX�̂���
# �icf:���ʂ̍��̒����30�Ȃ�15�l����I�[�o�[�����甽�����Œ�ɂȂ�܂��j
# �R��
my $mil_over = 6; # ����ȉ��̎��̔������i����ȉ��Ŏシ����ꍇ�͏グ��B�ύX�񐄏��j
my $mil_max = 4; # �l��������Ɠ����ł��̒l�ɂȂ�i���₷�Ɛl�������Ƃ��������Ȃ�j
my $mil_min = 0.5; # �Œᔽ�����i�Í����l���������ċ�������Ƃ��͉�����j
# �푈
my $war_over = 4.5;  # ����ȉ��̎��̔������i����ȉ��Ŏシ����ꍇ�͏グ��B�ύX�񐄏��j
my $war_max = 3; # �l��������Ɠ����ł��̒l�ɂȂ�i���₷�Ɛl�������Ƃ��������Ȃ�j
my $war_min = 0.5; # �Œᔽ�����i�Í����l���������ċ�������Ƃ��͉�����j
# �v�Z��
my $ave_cap = ($w{player} / $w{country} + $ave_add) * $max_par;
my $npc_subx = ($ave_cap - $npc_cap) == 0 ? ($cs{member}[$w{country}] - $npc_cap) : ($cs{member}[$w{country}] - $npc_cap) / ($ave_cap - $npc_cap);
# �R��NPC�����̔������i�f�t�H���g��1�jcf:4���ƍ���50000�����ŏ�ɔ���,12���Ə펞����
$npc_mil = $npc_subx * (1 - $mil_max) + $mil_max;
$npc_mil = $npc_mil < $mil_min ? $mil_min:
	 $npc_mil > $mil_max ? $mil_over:
	 $npc_mil;
# �푈NPC�����̔������i�f�t�H���g��1�jcf:3���ƍ���30000�����ŏ�ɔ���,4���Ə펞����
$npc_war = $npc_subx * (1 - $war_max) + $war_max;
$npc_war = $npc_war < $war_min ? $war_min:
	 $npc_war > $war_max ? $war_over:
	 $npc_war;
	 
#=================================================
# NPC���̒ǉ�
#=================================================
sub add_npc_country {
	&write_world_news("<i>���̔e�ҒB�ɂ���ĕ��󂳂�Ă������E�̌��E����܂�A�������Ă��S�낤�Ƃ��Ă���c</i>");
	$w{game_lv} = 99;
	$w{world} = $#world_states;
	
	# NPC�̍��̖��O
	my @c_names = (qw/���񂱂� �C���̍� ���E/);
	my $npc_country_name  = $c_names[int(rand(@c_names))];
	
	# NPC�̍��F
	my $npc_country_color = '#BA55D3';
	++$w{country};
	my $i = $w{country};
	mkdir "$logdir/$i" or &error("$logdir/$i ̫��ނ����܂���ł���") unless -d "$logdir/$i";
	for my $file_name (qw/prisoner violator old_member/) {
		my $output_file = "$logdir/$i/$file_name.cgi";
		next if -f $output_file;
		open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
		close $fh;
		chmod $chmod, $output_file;
	}
	for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member leader member/) {
		my $output_file = "$logdir/$i/$file_name.cgi";
		open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
		if ($file_name eq 'depot') {
			print $fh "1<>1<><>\n";
		}
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
	$cs{name}[$i]     = $npc_country_name;
	$cs{color}[$i]    = $npc_country_color;
	$cs{member}[$i]   = 0;
	$cs{win_c}[$i]    = 999;
	$cs{tax}[$i]      = 99;
	$cs{strong}[$i]   = 99999;
	$cs{food}[$i]     = 999999;
	$cs{money}[$i]    = 999999;
	$cs{soldier}[$i]  = 999999;
	$cs{state}[$i]    = 5;
	$cs{capacity}[$i] = $npc_cap; 
	$cs{is_die}[$i]   = 0;
	$cs{modify_war}[$i]   = 5;
	$cs{modify_dom}[$i]   = 5;
	$cs{modify_mil}[$i]   = 5;
	$cs{modify_pro}[$i]   = 5;
	
	my @lines = &get_countries_mes();
	if ($w{country} > $#lines) {
		open my $fh9, ">> $logdir/countries_mes.cgi";
		print $fh9 "���J�i���l�ԋ����A�̑�i����K�Ńm�`�J���m�O�j�����X�K�ǃC�c<>diabolos.gif<>\n";
		close $fh9;
	}
}
#=================================================
# �푈NPC��ׂ��쐬
#=================================================
sub add_npc_data {
	my $country = shift;
	
	my %npc_statuss = (
		max_hp => [999, 600, 400, 300, 99],
		max_mp => [999, 500, 200, 100, 99],
		at     => [999, 400, 300, 200, 99],
		df     => [999, 300, 200, 100, 99],
		mat    => [999, 400, 300, 200, 99],
		mdf    => [999, 300, 200, 100, 99],
		ag     => [999, 500, 300, 200, 99],
		cha    => [999, 400, 300, 200, 99],
		lea    => [666, 400, 250, 150, 99],
		rank   => [$#ranks, $#ranks-2, 10, 7, 4],
	);
	my @npc_weas = (
	#	[0]����[1]����No	[2]�K�E�Z
		['��', [0],			[61..65],],
		['��', [1 .. 5],	[1 .. 5],],
		['��', [6 ..10],	[11..15],],
		['��', [11..15],	[21..25],],
		['��', [16..20],	[31..35],],
		['��', [21..25],	[41..45],],
		['��', [26..30],	[51..55],],
	);
	my $line = qq|\@npcs = (\n|;
	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$npc_names[$i]',\n|;
		
		for my $k (qw/max_hp max_mp at df mat mdf ag cha lea rank/) {
			$line .= qq|\t\t$k\t\t=> $npc_statuss{$k}[$i],\n|;
		}
		
		my $kind = int(rand(@npc_weas));
		my @weas = @{ $npc_weas[$kind][1] };
		my $wea  = $npc_weas[$kind][1]->[int(rand(@weas))];
		$line .= qq|\t\twea\t\t=> $wea,\n|;
		my $skills = join ',', @{ $npc_weas[$kind][2] };
		$line .= qq|\t\tskills\t\t=> '$skills',\n\t},\n|;
	}
	$line .= qq|);\n\n1;\n|;
	
	open my $fh, "> $datadir/npc_war_$country.cgi";
	print $fh $line;
	close $fh;
}
#=================================================
# NPC���̍폜
#=================================================
sub delete_npc_country {
	if ($is_npc_win) {
		if ($m{country} eq $w{country}) {
			$w{win_countries} = $union ? $union : '';
			$m{country} = 0;
			$cs{war}[0] = $m{name};
			if($w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/ || $w{year} =~ /06$/){
				$m{shogo}   = '���V�g��';
			}else{
				$m{shogo}   = '���G���[�g';
			}
		}
		else {
			$w{win_countries} = $m{country};
		}
		
		# ����\�҂ɓ��T
		for my $k (qw/war dom pro mil ceo/) {
			my @bonus_pets = (19, 20, 168, 187);
			next if $cs{$k}[$w{country}] eq '';
			&send_item($cs{$k}[$w{country}], 3, $bonus_pets[int(rand(@bonus_pets))], 0, 0, 1);
		}
	}
	my @names = &get_country_members($w{country});
	require "./lib/move_player.cgi";
	
	for my $name (@names) {
		$name =~ tr/\x0D\x0A//d;
		&move_player($name, $w{country}, 0);
		&regist_you_data($name, 'country', 0);
		my $n_id = unpack 'H*', $name;
		open my $efh, ">> $userdir/$n_id/ex_c.cgi";
		print $efh "fes_c<>1<>\n";
		close $efh;
		!$is_npc_win ? &regist_you_data($name, 'shogo', $shogos[1][0]) :
		$w{world} eq $#world_states ? &regist_you_data($name, 'shogo', '���V�g��') :
										&regist_you_data($name, 'shogo', '���G���[�g');
	}
	--$w{country};
	
	my @lines = ();
	open my $fh, "+< $logdir/countries_mes.cgi";
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	pop @lines if @lines > $w{country};
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}
#=================================================
# NPC���̌R�� ./lib/military.cgi�ŕp�x����
#=================================================
sub npc_military {
	my @keys = (qw/gou gou gou cho cho cho sen ds/);
	my $k = $keys[int(rand(@keys))];
	my $country = int(rand($w{country}-1)+1);
	return if $cs{is_die}[$country]; # �ŖS������͒D��Ȃ�
	require "$datadir/npc_war_$w{country}.cgi";
	&{'npc_military_'.$k}($country);
}
sub npc_military_gou { # ���D
	my $country = shift;
	my $v = &_npc_get_resource($country, 'food');
	&write_world_news("$cs{name}[$w{country}]��$npcs[int(rand(@npcs))]{name}��$cs{name}[$country]�Ɋ�P�U�������{�B$v�̕��Ƃ����D���邱�Ƃɐ������܂���");
}
sub npc_military_cho { # ����
	my $country = shift;
	my $v = &_npc_get_resource($country, 'money');
	&write_world_news("$cs{name}[$w{country}]��$npcs[int(rand(@npcs))]{name}��$cs{name}[$country]�̎������BٰĂ��h�����A$v��$e2j{money}�𗬏o�����邱�Ƃɐ������܂���");
}
sub npc_military_sen { # �R��
	my $country = shift;
	my $v = &_npc_get_resource($country, 'soldier');
	&write_world_news("$cs{name}[$w{country}]��$npcs[int(rand(@npcs))]{name}��$cs{name}[$country]��$v�̕�����]���邱�Ƃɐ���!$cs{name}[$w{country}]�̕��Ɏ�荞�݂܂���");
}
sub npc_military_ds { # Dead Soldier ����̏���
	return if $cs{soldier}[$w{country}] > 500000;
	$cs{soldier}[$w{country}] += 50000;
	&write_world_news("$cs{name}[$w{country}]��$npcs[int(rand(@npcs))]{name}�����̍���莀��̕��m���Ăъo�܂��A$cs{name}[$w{country}]�̑����m����50000�������܂���");
}
sub _npc_get_resource {
	my($country, $k) = @_;
	my $v = int(rand(15000)+15000);
	$v *= 2 if $cs{strong}[$w{country}] < 30000;
	$v = $v > $cs{$k}[$country] ? $cs{$k}[$country] : $v;
	$cs{$k}[$country]    -= $v;
	$cs{$k}[$w{country}] += $v;
	
	return $v;
}
#=================================================
# NPC���̐푈 ./lib/_war_result.cgi�ŕp�x����
#=================================================
sub npc_war {
	require "$datadir/npc_war_$w{country}.cgi";
	if ($cs{strong}[$w{country}] < 50000) {
		  rand(6)  < 1 ? &npc_use_pet_fenrir
		: rand(10) < 1 ? &npc_use_pet_prisoner
		: rand(20) < 1 ? &npc_use_pet_pesto
		: rand(15) < 1 ? &npc_use_pet_loptr
		: rand(40) < 1 ? &npc_use_pet_meteo
		:                &npc_get_strong
		;
	}
	else {
		  rand(3)  < 1 ? &npc_use_pet_fenrir
		: rand(15) < 1 ? &npc_use_pet_prisoner
		: rand(20) < 1 ? &npc_use_pet_pesto
		: rand(20) < 1 ? &npc_use_pet_loptr
		: rand(50) < 1 ? &npc_use_pet_meteo
		:                &npc_get_strong
		;
	}
}
sub npc_use_pet_fenrir { # ̪���
	return if $touitu_strong < 20000;
	$w{game_lv} += 1 if $w{game_lv} < 90;
	for my $i (1..$w{country}-1) {
		next if $cs{is_die}[$i];
		next if $cs{strong}[$i] < 1000;
		$cs{strong}[$i] -= $touitu_strong * 0.6 > $cs{strong}[$w{country}] ? int(rand(400)+400) : int(rand(200)+200);
	}
	
	$touitu_strong * 0.6 > $cs{strong}[$w{country}] ? 
		&write_world_news("$cs{name}[$w{country}]��$npcs[0]{name}�̖��_�̑M��!�e����$e2j{strong}������܂���"):
		&write_world_news("$cs{name}[$w{country}]��$npcs[4]{name}�̔j�����!�e����$e2j{strong}������܂���");
		
}
sub npc_use_pet_loptr { # ����
	$w{game_lv} -= 1 if $w{game_lv} > 80;
	&write_world_news("$cs{name}[$w{country}]�̂��񂱂Ȃ�(NPC)�̎א_�̍ق�!");
	
	my @disasters = (['���R�ЊQ','food'],['�o�ϔj�]','money'],['��n�k','soldier']);
	my $v = int(rand(@disasters));
	for my $i (1 .. $w{country}-1) {
		next if $cs{ is_die }[$i];
		$cs{ $disasters[$v][1] }[$i] = int($cs{ $disasters[$v][1] }[$i] * 0.5);
	}
	&write_world_news("<b>���E���� $disasters[$v][0] ���N����܂���</b>");
}
sub npc_use_pet_pesto { # �߽�
	$w{game_lv} -= 1 if $w{game_lv} > 75;
	for my $i (1..$w{country}) {
		$cs{state}[$i] = 5;
	}
	&write_world_news("<b>$cs{name}[$w{country}]��$npcs[int(rand(@npcs))]{name}���ғł��T���U�炵�e����$e2j{state}�� $country_states[5] �ɂȂ�܂���</b>");
}
sub npc_use_pet_meteo { # �õ
	$w{game_lv} -= 2 if $w{game_lv} > 85;
	for my $i (1..$w{country}) {
		for my $j ($i+1..$w{country}) {
			next if($w{"p_${i}_${j}"} == 1 && $j eq $w{country});
			$w{"f_${i}_${j}"}=int(rand(20));
			$w{"p_${i}_${j}"}=2;
		}
	}
	&write_world_news("<b>$cs{name}[$w{country}]��$npcs[int(rand(@npcs))]{name}���õ���������E�����J��ƂȂ�܂���</b>");
}
sub npc_use_pet_prisoner { # �S��
	$w{game_lv} -= 1 if $w{game_lv} > 85;
	my @ks = (qw/war dom pro mil ceo/);
	my $k = $ks[int(rand(@ks))];
	for my $i (1 .. $w{country}-1) {
		next if $cs{$k}[$i] eq '';
		next if $cs{$k}[$i] eq $m{name};
		
		&regist_you_data($cs{$k}[$i], 'lib', 'prison');
		&regist_you_data($cs{$k}[$i], 'tp',  100);
		&regist_you_data($cs{$k}[$i], 'y_country',  $w{country});
		
		open my $fh, ">> $logdir/$w{country}/prisoner.cgi" or &error("$logdir/$w{country}/prisoner.cgi ���J���܂���");
		print $fh "$cs{$k}[$i]<>$i<>\n";
		close $fh;
	}
	&write_world_news("<b>$cs{name}[$w{country}]��$npcs[int(rand(@npcs))]{name}���s�C���Ȍ�������e���� $e2j{$k} ��$cs{name}[$w{country}]�̘S���ɗH����܂���</b>");
}
sub npc_get_strong { # �D��
	# ����������Ȃ��Ƃ�
	for my $k (qw/food money soldier/) {
		return if $cs{$k}[$w{country}] < 100000;
	}
	
	my $country = 1;
	if ($cs{strong}[$w{country}] < 40000) { # ��ԍ��͂���������I��
		my $max_value = $cs{strong}[1];
		for my $i (2 .. $w{country}-1) {
			if ($cs{strong}[$i] > $max_value) {
				$country = $i;
				$max_value = $cs{strong}[$i];
			}
		}
	}
	else {
		$country = int(rand($w{country}-1)+1);
	}
	
	return if ($cs{is_die}[$country] && $cs{strong}[$country] < 5000);        # �ŖS������͒D��Ȃ�
	return if $cs{strong}[$country] < 1000; # ����1000�����͒D��Ȃ�
	
	# ���̍��̑���̖��O������ю擾
	my $name = '';
	open my $fh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgi̧�ق��ǂݍ��߂܂���");
	rand($.) < 1 and $name = $_ while <$fh>;
	close $fh;
	$name =~ tr/\x0D\x0A//d;
	
	my $v = int(rand(300)+300);
	$cs{strong}[$w{country}] += $v;
	$cs{strong}[$country]    -= $v;
	&write_world_news(qq|$cs{name}[$w{country}]��$npcs[int(rand(@npcs))]{name}��$cs{name}[$country]�ɐN�U�A$name�̕��������j�� <font color="#FF00FF"><b>$v</b> ��$e2j{strong}��D�����Ƃɐ���</font>�����悤�ł�|);
	$cs{is_die}[$w{country}] = 0 if $cs{is_die}[$w{country}];
}
#=================================================
# �����l�����x��NPC���Ɏd�����Ȃ��悤�ɐ���
#=================================================
sub is_move_npc_country {
	my @lines = ();
	open my $fh, "+< $logdir/$w{country}/old_member.cgi" or &error("$logdir/$w{country}/old_member.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		if ($line eq $m{name}) {
			close $fh;
			$mes .= "�ߋ���NPC���֎d�������l�́A���΂炭NPC���֎d�����邱�Ƃ͋�����܂���<br>";
			return 0;
		}
		push @lines, "$line\n";
		last if @lines+1 >= $max_npc_old_member;
	}
	unshift @lines, "$m{name}\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	if ($m{name} eq $cs{ceo}[$m{country}]) {
		$mes .= "$c_m��$e2j{ceo}�����C����K�v������܂�<br>";
		&begin;
		return 0;
	}
	
	# ��\�߲��0
	for my $k (qw/war dom mil pro/) {
		$m{$k.'_c'} = int($m{$k.'_c'} * 0);
	}
	&mes_and_world_news("�����ɍ��𔄂�n���܂���", 1);
	return 1;
}
1;
