#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require "./lib/move_player.cgi";
my $this_script = 'admin_country.cgi';
#=================================================
# ���f�[�^�쐬/�ǉ�/���� Created by Merino
#=================================================

# ���܂����ŏo�͂����f�[�^
# ��NPC���ׂ����ݒ肵�����ꍇ�́A�쐬���ꂽ�u./data/npc_war_��No.cgi�v���������Ă�
my @countries = (qw/�R���z�[�Y�A�M ���� �S������ �܏� �ϑԐa�m���c �C��s�s�ٲ� �����ƃp���h�� ��޽�A�� �ڼޱ���� ��޽�ر�A�� �׷����� ������ى��� ��ް����� �ު���݉��� ��ݼޑ卑 ���ޘA�� ��݉��� ذ�ު���� ��މ��� �ر����/);
my @colors    = (qw/#006699 #0066CC #009999 #6600FF #0099CC #00CC99 #666699 #6699CC #3399CC #00CC00 #33CC33 #990000 #993333 #996633 #CC9966 #99CC66 #999999 #CC0000 #CC9900 #CC0099 #9900CC #CC3366/);
my @npcs = (
	['�ٳި��c��(NPC)',	'�̧�ٌR�t(NPC)',	'�ؽ���R(NPC)',		'��ď��R(NPC)',		'����ݑ���(NPC)'],
	['��ި�݋�(NPC)',	'���ްٌR�t(NPC)',	'��ļ�ݏ��R(NPC)',	'���ޏ��R(NPC)',	'�ٰ�ޑ���(NPC)'],
	['�ص�ݍc��(NPC)',	'���޽ČR�t(NPC)',	'�ص����R(NPC)',	'����R(NPC)',		'���ޑ���(NPC)'],
	['��ڰݍc��(NPC)',	'�è�R�t(NPC)',		'���ި�����R(NPC)',	'ذ�ާ����R(NPC)',	'�Я�ޑ���(NPC)'],
	['�ص�ݍc��(NPC)',	'���޽ČR�t(NPC)',	'�ص����R(NPC)',	'����R(NPC)',		'���ޑ���(NPC)'],
	['���ݔ���(NPC)',	'��ČR�t(NPC)',		'��̫��ޏ��R(NPC)',	'���ݏ��R(NPC)',	'����ޑ���(NPC)'],
	['�ڵ���׍c��(NPC)','ϯ���R�t(NPC)',	'�я��R(NPC)',		'нè����R(NPC)',	'а����(NPC)'],
	['��è�c�q(NPC)',	'è�ް�R�t(NPC)',	'ٰ�����R(NPC)',	'�Ӱ�����R(NPC)',	'���ذ����(NPC)'],
	['�ު���t��(NPC)',	'�ެ���R�t(NPC)',	'�ޮټު���R(NPC)',	'�ުư���R(NPC)',	'�ޮݑ���(NPC)'],
	['�ظ����(NPC)',	'��ذ�R�t(NPC)',	'��ި���R(NPC)',	'�ذ���R(NPC)',		'�ذ����(NPC)'],
	['�ު���ލc��(NPC)','ϼ���R�t(NPC)',	'�ޮ������R(NPC)',	'ϲ�ُ��R(NPC)',	'���ݑ���(NPC)'],
	['��ذ�c��(NPC)',	'�όR�t(NPC)',		'��ި�ݏ��R(NPC)',	'���ޱ���R(NPC)',	'��ő���(NPC)'],
	['�޼�ٍc��(NPC)',	'ϰ��R�t(NPC)',		'���׏��R(NPC)',	'���ް���R(NPC)',	'�߯������(NPC)'],
);
my %npc_statuss = (
	max_hp => [999, 500, 250, 150, 100],
	max_mp => [999, 300, 100, 100, 50],
	at     => [700, 400, 200, 100, 50],
	df     => [500, 300, 200, 100, 50],
	mat    => [700, 400, 200, 100, 50],
	mdf    => [500, 300, 200, 100, 50],
	ag     => [800, 500, 200, 100, 50],
	cha    => [800, 500, 200, 100, 50],
	lea    => [500, 350, 150, 80,  40],
	rank   => [$#ranks, $#ranks-2, 8, 5, 3],
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


#=================================================
# ���C������
#=================================================
&header;
&decode;
&error('�߽ܰ�ނ��Ⴂ�܂�') unless $in{pass} eq $admin_pass;
&header_admin;

if    ($in{mode} eq 'now_country')     { &now_country;     }
elsif ($in{mode} eq 'add_country')     { &admin_add_country;     }
elsif ($in{mode} eq 'delete_country')  { &admin_delete_country;  }
elsif ($in{mode} eq 'restore_country') { &restore_country; }
elsif ($in{mode} eq 'modify_country') { &modify_country; }
elsif ($in{mode} eq 'change_year')     { &admin_change_year;     }
elsif ($in{step}) { &{ 'step_' . $in{step} }; }
else { &step_1; }
&footer;
exit;



#=================================================
# header+
#=================================================
sub header_admin {
	print <<"EOM";
	<table border="0"><tr><td>
		<form action="$script_index">
			<input type="submit" value="�s�n�o" class="button1">
		</form>
	</td><td>
		<form method="$method" action="admin.cgi">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="��ڲ԰�Ǘ�" class="button1">
		</form>
	</td><td>
		<form method="$method" action="$this_script">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="���Ǘ�" class="button1">
		</form>
	</td><td>
		<form method="$method" action="$this_script">
			<input type="hidden" name="mode" value="now_country">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="���݂̍��f�[�^" class="button1">
		</form>
	</td></tr></table>
EOM
}


#=================================================
# ���݂̍��f�[�^
#=================================================
sub now_country {
print qq|<p>���݂̍��f�[�^</p>|;
	&read_cs;
	&countries_html;
}


#=================================================
# Step1
#=================================================
sub step_1 {
	print <<"EOM";
	<br>
	<div class="mes">
		<ul>
			<li>���E�̍��̐��Ǝn�܂�̔N�Ə����͂��Ă��������B
			<li>����r���ő��₵���茸�炵���肷�邱�Ƃ͉\\�ł��B
			<li>���ɂ�����肪�Ȃ��ꍇ����̫�Ă̂܂܂�OK�ł��B
			<li>���̐��͂P�����炢����ł����₷���Ƃ��\\�ł��B
			<li>���̐��ɂ���Փx���ς���Ă���̂ŁA�ɒ[�ɑ���/���Ȃ��ꍇ�� ./lib/reset.cgi �œ�Փx�ݒ��ς��邱�Ƃ𐄏����܂��B
		</ul>
	</div>
	<br>
	<form method="$method" action="$this_script">
		<input type="text" name="country" value="6" class="text_box_s" style="text-align: right">��<br>
		<input type="text" name="year"    value="1" class="text_box_s" style="text-align: right">�N<br>
		<select name="world">
EOM
		for my $i (0 .. $#world_states) {
			my $selected = $in{world} == $i ? " selected=\"selected\"" : "";
			print qq|<option value="$i" label="$world_states[$i]"$selected>$world_states[$i]</option>|;
		}
	print <<"EOM";
		</select>�<br>
		<input type="hidden" name="step" value="2">
		<input type="hidden" name="pass" value="$in{pass}">
		<p><input type="submit" value="����" class="button_s"></p>
	</form>
EOM
	if (-s "$logdir/countries.cgi") {
		print <<"EOM";
	<br><br><hr>
	<br>
	<div class="mes">
	�N��ύX����<br>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="change_year">
		<input type="hidden" name="pass" value="$in{pass}">
		<input type="text" name="year" value="1" class="text_box_s" style="text-align: right">�N<br>
		<p><input type="submit" value="�ύX" class="button1"></p>
	</form>
	</div>
	<br>
	<div class="mes">
	����ǉ�����<br>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="add_country">
		<input type="hidden" name="pass" value="$in{pass}">
		�����F<input type="text" name="add_name"  class="text_box1"><br>
		���F�F<input type="text" name="add_color" class="text_box1"><br>
		<p><input type="submit" value="�ǉ�" class="button1"></p>
	</form>
	</div>
	<br>
	<div class="mes">
	�����폜(��Ԍ��̍����炵���폜�ł��܂���)<br>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="delete_country">
		<input type="hidden" name="pass" value="$in{pass}">
		<p><input type="submit" value="�폜" class="button1"></p>
	</form>
	</div>
	<br>
	<div class="mes">
	�����C��<br>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="modify_country">
		<input type="hidden" name="pass" value="$in{pass}">
		<p><input type="submit" value="�C��" class="button1"></p>
	</form>
	</div>
	<br>
EOM
	}
	
	&backup if $is_backup_countries && -d "backup";
}
#=================================================
# Step2
#=================================================
sub step_2 {
	print <<"EOM";
	<p>�S$in{country}�J���B$in{year}�N�ڂ�$world_states[$in{world}]����n�܂�</p>
	<p>���̖��O�ƐF�����߂Ă�������</p>
	<form method="$method" action="$this_script">
		<input type="hidden" name="year" value="$in{year}">
		<input type="hidden" name="world" value="$in{world}">
		<input type="hidden" name="step" value="2">
		<input type="hidden" name="country" value="$in{country}">
		<input type="hidden" name="omakase" value="1">
		<input type="hidden" name="pass" value="$in{pass}">
		<input type="submit" value="���܂���" class="button1">
	</form>
	<form method="$method" action="$this_script">
EOM
	for my $i (1 .. $in{country}) {
		my $country = '';
		my $color   = '';
		
		if ( $in{omakase} && defined($countries[0]) && defined($colors[0]) ) {
			my $v  = int(rand(@countries));
			my $vv = int(rand(@colors));
			$country = splice(@countries, $v, 1);
			$color   = splice(@colors, $vv, 1);
		}

		print qq|���̖��O�F <input type="text" name="name_$i" class="text_box1" value="$country">|;
		print qq|�@���̐F�F <input type="text" name="color_$i" class="text_box1" value="$color" style="color: #333; background-color: $color;"><br>|;
	}
	
	print <<"EOM";
		<input type="hidden" name="year" value="$in{year}">
		<input type="hidden" name="world" value="$in{world}">
		<input type="hidden" name="country" value="$in{country}">
		<input type="hidden" name="pass" value="$in{pass}">
		<input type="hidden" name="step" value="3">
		<p><input type="submit" value="����" class="button_s"></p>
	</form>
EOM
}
#=================================================
# Step3
#=================================================
sub step_3 {
	%w = ();
	%cs = ();
	
	$in{year} = 1 if $in{year} < 0;
	--$in{year};
print "$w{country}<br>" if $config_test;
	
	$w{country} = $in{country};
print "$w{country}<br>" if $config_test;
	$w{year}    = $in{year};
	$w{world}   = $in{world};
	$w{playing} = 0;

	for my $i (1 .. $in{country}) {
		&error('���O���F�����L���̍�������܂�') if !$in{"name_$i"} || !$in{"color_$i"};
		
		$cs{name}[$i]     = $in{"name_$i"};
		$cs{color}[$i]    = $in{"color_$i"};
		$cs{member}[$i]   = 0;
		$cs{win_c}[$i]    = 0;
		$cs{tax}[$i]      = 30;
		
		# ̧�قȂǍ쐬
		mkdir "$logdir/$i" or &error("$logdir/$i ̫��ނ����܂���ł���") unless -d "$logdir/$i";
		for my $file_name (qw/bbs bbs_log bbs_member depot_log depot_b depot_b_log leader member patrol prison prison_member prisoner violator/) {
			my $output_file = "$logdir/$i/$file_name.cgi";
#			next if -f $output_file;
			open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
			close $fh;
			chmod $chmod, $output_file;
		}
		# ���ɂ�1�s�ڂ��ݒ�Ȃ̂ŗ\�ߏ�������ł����Ȃ��ƍ��ɂɂԂ�����1�ڂ̃A�C�e�����������Ă��܂�
		my $output_file = "$logdir/$i/depot.cgi";
		open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
		print $fh "1<>1<>1����Lv1�ȏオ���p�ł��܂�<>\n";
		close $fh;
		chmod $chmod, $output_file;
		
		&add_npc_data($i);
		
		mkdir "$logdir/union" or &error("$logdir/union ̫��ނ����܂���ł���") unless -d "$logdir/union";
		
		# create union file
		for my $j ($i+1 .. $in{country}) {
			my $file_name = "$logdir/union/${i}_${j}";
#			next if -f "$file_name.cgi";
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
		
		open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ̧�ق����܂���");
		close $fh_h;
	}
	
	$w{player} = 0;
	opendir my $dh, "$userdir" or &error('հ�ް̫��ނ��J���܂���');
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /\./;
		next if $file_name =~ /backup/;
		++$w{player};
	}
	closedir $dh;
	
	require './lib/reset.cgi';
	&reset;
	&begin_common_world;

	&write_cs;
	&create_countries_mes;

	print qq|<p>�ȉ��̂悤�ȍ��f�[�^���쐬���܂���!</p>|;
	&countries_html;
}


#=================================================
# ���ꗗ�\��
#=================================================
sub countries_html {
	print qq|<table class="table1">|;

	print qq|<tr><th>$e2j{name}</th>|;
	print qq|<td align="center" style="color: #333; background-color: $cs{color}[$_];">$cs{name}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;

	for my $k (qw/strong food money soldier tax/) {
		print qq|<tr><th>$e2j{$k}</th>|;
		for my $i (1 .. $w{country}) {
			print qq|<td align="right">$cs{$k}[$i]</td>|;
		}
		print qq|</tr>\n|;
	}

	print qq|<tr><th>$e2j{state}</th>|;
	print qq|<td align="center">$country_states[ $cs{state}[$_] ]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;

	print qq|</table>|;
}


#=================================================
# NPC���쐬
#=================================================
sub add_npc_data {
	my $country = shift;
	my $v     = int(rand(@npcs));
	my $names = splice(@npcs, $v, 1);
	my @names = @{ $names };
	
	my $line = qq|\@npcs = (\n|;
	
	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$names[$i]',\n|;
		
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
# ���̕��j̧�ٍ쐬
#=================================================
sub create_countries_mes {
	open my $fh, "> $logdir/countries_mes.cgi";
	for my $i (0 .. $in{country}) {
		print $fh "<><>\n";
	}
	close $fh;
}

#=================================================
# �N��ύX
#=================================================
sub admin_change_year {
	&read_cs;
	$w{year} = $in{year}-1;
	&write_cs;

	require "./lib/reset.cgi";
	&reset;

	print qq|<p>�ȉ��̂悤�ȍ��f�[�^�ŔN��$w{year}�ɂ��܂���!</p>|;
	&countries_html;
}

#=================================================
# ����ǉ�
#=================================================
sub admin_add_country {
	&read_cs;
	&error('���O���F�����L���ł�') if !$in{"add_name"} || !$in{"add_color"};

	++$w{country};
	
	my $i = $w{country};

	# ̧�قȂǍ쐬���Ă��܂�
	mkdir "$logdir/$i" or &error("$logdir/$i ̫��ނ����܂���ł���") unless -d "$logdir/$i";
	for my $file_name (qw/bbs bbs_log bbs_member depot depot_log leader member patrol prison prison_member prisoner violator/) {
		my $output_file = "$logdir/$i/$file_name.cgi";
#		next if -f $output_file;
		open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
		close $fh;
		chmod $chmod, $output_file;
	}
	
	&add_npc_data($i);
	
	# create union file
	for my $j (1 .. $i-1) {
		my $file_name = "$logdir/union/${j}_${i}";
#		next if -f "$file_name.cgi";
		open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ̧�ق����܂���");
		close $fh;
		chmod $chmod, "$file_name.cgi";
		
		open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ̧�ق����܂���");
		close $fh2;
		chmod $chmod, "${file_name}_log.cgi";
		
		open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ̧�ق����܂���");
		close $fh3;
		chmod $chmod, "${file_name}_member.cgi";

		$w{ "f_${j}_${i}" } = int(rand(50)+10);
		$w{ "p_${j}_${i}" } = 0;
	}
	
	open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ̧�ق����܂���");
	print $fh_h "�������c$date ���̓��ɉ��x�����O�C������ƍX�V����܂�";
	close $fh_h;
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
	my $ave_c = int($w{player} / $country);
	$cs{name}[$i]     = $in{"add_name"};
	$cs{color}[$i]    = $in{"add_color"};
	$cs{member}[$i]   = 0;
	$cs{win_c}[$i]    = 0;
	$cs{tax}[$i]      = 30;
	$cs{strong}[$i]   = int(rand(6)  + 7) * 1000;
	$cs{food}[$i]     = int(rand(10) + 3) * 1000;
	$cs{money}[$i]    = int(rand(10) + 3) * 1000;
	$cs{soldier}[$i]  = int(rand(10) + 3) * 1000;
	$cs{state}[$i]    = rand(2) > 1 ? 0 : int(rand(@country_states));
	$cs{capacity}[$i] = $ave_c;
	$cs{is_die}[$i]   = 0;
	
	&write_cs;
	
	open my $fh9, ">> $logdir/countries_mes.cgi";
	print $fh9 "<><>\n";
	close $fh9;
	
	print qq|<p>����ǉ����܂���</p>|;
	&countries_html;
}

#=================================================
# ���𕜌�
#=================================================
sub restore_country {
	my @lines = ();
	open my $fh, "< ./backup/$in{file_name}" or &error("./backup/$in{file_name}̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	close $fh;
	
	open my $fh2, "> $logdir/countries.cgi" or &error("$logdir/countries.cgi̧�ق��J���܂���");
	print $fh2 @lines;
	close $fh2;
	
	print qq|<p>���ް��𕜌����܂���</p>|;
	
	&read_cs;
	&countries_html;
}

#=================================================
# �����폜
#=================================================
sub admin_delete_country {
	&read_cs;
	
	my @lines = &get_country_members($w{country});
	for my $line (@lines) {
		$line =~ tr/\x0D\x0A//d;
		&move_player($line, $w{country}, 0);
		&regist_you_data($line, 'country', 0);
	}
	--$w{country};
	&write_cs;
	
	print qq|<p>$cs{name}[$w{country}+1]���폜���܂���</p>|;
	&countries_html;
}


#=================================================
# �ޯ�����̫��
#=================================================
sub backup {
	my %files = ();
	opendir my $dh, "backup" or &error("backup̫��ނ��J���܂���");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /index.html/;
		
		my $file_time = (stat "./backup/$file_name")[9];
		$files{$file_time} = $file_name;
	}
	closedir $dh;

	print qq|<form method="$method" action="$this_script">|;
	print qq|<div class="mes">�ޯ����߂��畜��<br>|;
	print qq|<select name="file_name" class="select1">|;
	
	for my $k (sort { $b <=> $a } keys %files) {
		my($hour, $day, $month) = (localtime($k))[2,3,4];
		++$month;
		print qq|<option value="$files{$k}">$month��$day��$hour:00</option>|;
	}
	print qq|</select><br>|;
	print qq|<input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="mode" value="restore_country">|;
	print qq|<p><input type="submit" value="����" class="button1"></p></form></div>|;
}

#=================================================
# �C��
#=================================================
sub modify_country {
	&read_cs;

	if ($in{execute}) {
		for my $i (1..$w{country}) {
			$cs{color}[$i] = $in{"color_" . $i};
			$cs{name}[$i] = $in{"name_" . $i};
			for my $k (qw/strong food money soldier tax state/) {
				$cs{$k}[$i] = $in{$k . "_" . $i};
				if ($cs{$k}[$i] =~ /[^0-9]/ || $cs{$k}[$i] < 0) {
					$cs{$k}[$i] = 0;
				}
			}
		}
		&write_cs;
	}
	
	print <<"EOM";
	<p>���̏������߂Ă�������</p>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="modify_country">
		<input type="hidden" name="execute" value="1">
		<input type="hidden" name="pass" value="$in{pass}">
EOM
	print qq|<table class="table1">|;

	print qq|<tr><th>�F</th>|;
	for my $i (1 .. $w{country}) {
		print qq|<td align="center" style="color: #333; background-color: $cs{color}[$i];"><input type="text" name="color_${i}" value="$cs{color}[$i]"/></td>|;
	}
	print qq|</tr>\n|;

	print qq|<tr><th>$e2j{name}</th>|;
	for my $i (1 .. $w{country}) {
		print qq|<td align="center" style="color: #333; background-color: $cs{color}[$i];"><input type="text" name="name_${i}" value="$cs{name}[$i]"/></td>|;
	}
	print qq|</tr>\n|;

	for my $k (qw/strong food money soldier tax/) {
		print qq|<tr><th>$e2j{$k}</th>|;
		for my $i (1 .. $w{country}) {
			print qq|<td align="right"><input type="text" name="${k}_${i}" value="$cs{$k}[$i]"/></td>|;
		}
		print qq|</tr>\n|;
	}

	print qq|<tr><th>$e2j{state}</th>|;
	for my $i (1 .. $w{country}) {
		print qq|<td align="right">|;
		print qq|<select name="state_${i}">|;
		for my $j (0..$#country_states) {
			my $selected = $cs{state}[$i] eq $j ? ' selected' : '';
			print qq|<option value="$j"$selected>$country_states[$j]</option>|;
		}
		print qq|</select>|;
		print qq|</td>|;
	}
	print qq|</tr>\n|;

	print qq|</table>|;	
	print <<"EOM";
		<p><input type="submit" value="�C��" class="button_s"></p>
	</form>
EOM
}

