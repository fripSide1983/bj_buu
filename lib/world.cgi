sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
require './lib/_world_reset.cgi';
#================================================
# ���E� Created by Merino
#================================================

#================================================
# �I�����
#================================================
sub tp_100 {
	$mes .= "���Ȃ��͂��̐��E�ɉ������߂܂���?<br>";
	&menu('�F���]�ނ���','��]','��]','���a');
	$m{tp} += 10;
}

sub tp_110 {
	my $old_world = $w{world};

	my @new_worlds;
	if ($cmd eq '1') { # ��]
		&mes_and_world_news("<b>���E�Ɋ�]��]�݂܂���</b>", 1);
		@new_worlds = (1,2,3,4,5,6,7,17,18,19,20);
	}
	elsif ($cmd eq '2') { # ��]
		&mes_and_world_news("<b>���E�ɐ�]��]�݂܂���</b>", 1);
		@new_worlds = (8,9,10,11,12,13,14,15,16);
	}
	elsif ($cmd eq '3') { # ���a
		&mes_and_world_news("<b>���E�ɕ��a��]�݂܂���</b>", 1);
		@new_worlds = (0);
	}
	else {
		&mes_and_world_news('<b>���E�ɂ݂Ȃ��]�ނ��̂�]�݂܂���</b>', 1);
		@new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
	}

	my @next_worlds = &unique_worlds(@new_worlds);
	$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
	$w{world_sub} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];

	# �����Í���
	if ($old_world eq $#world_states) {
		$w{world} = $#world_states;
		&write_world_news("<i>$m{name}�̊肢�͂���������܂���</i>");
	}
	# �����V���b�t��
	elsif ($old_world eq $#world_states-1) {
		$w{world} = $#world_states-1;
		&write_world_news("<i>$m{name}�̊肢�͋󂵂����E�͍����Ɋׂ�܂���</i>");
	}
	# �����g��
	elsif ($old_world eq $#world_states-2) {
		$w{world} = $#world_states-2;
		&write_world_news("<i>$m{name}�̊肢�͋󂵂����E�͓�ɕ�����܂���</i>");
	}
	# �����O��
	elsif ($old_world eq $#world_states-3) {
		$w{world} = $#world_states-3;
		&write_world_news("<i>$m{name}�̊肢���󂵂����􂵂����E�𓝈ꂷ�ׂ��O�����䓪���܂���</i>");
	}
	# �����p�Y
	elsif ($old_world eq $#world_states-4) {
		$w{world} = $#world_states-4;
		&write_world_news("<i>$m{name}�̊肢�͋󂵂����E�͉p�Y���`�������o������ɂȂ�܂���</i>");
	}
	# �����ّ�
	elsif ($old_world eq $#world_states-5) {
		$w{world} = $#world_states-5;
		&write_world_news("<i>$m{name}�̊肢���󂵂����E�������������Ƃ�</i>");
	}
	# �����̂���܂�Ȃ��̂�
	elsif ($w{world} eq $old_world) {
		$w{world} = int(rand(@world_states-3));
		++$w{world} if $w{world} eq $old_world;
		$w{world} = int(rand(10)) if $w{world} > $#world_states-3;
		&write_world_news("<i>���E�� $world_states[$old_world] �ƂȂ�܁c���� $world_states[$w{world}]�ƂȂ�܂���</i>");
	}
	else {
		if ($w{world} eq '0') { # ���a
			&write_world_news("<i>���E�� $world_states[$w{world}] �ɂȂ�܂���</i>");
		}elsif ($w{world} eq '18') { # �E��
			&write_world_news("<i>���E�� $world_states[$w{world}] �Ƃ����ӂ���(���Ȃ����ϊ��ł��Ȃ�)�ɂȂ�܂���</i>");
		}else{
			&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
		}
	}	
	unshift @old_worlds, $w{world};
	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgi���J���܂���");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$nline\n";
	close $fh;
	
	my $migrate_type = 0;
	if ($w{world} eq '0') { # ���a
		$w{reset_time} += 3600 * 12;
	}
	elsif ($w{world} eq '6') { # ����
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			push @win_cs, [$i, $cs{win_c}[$i]];
		}
		@win_cs = sort { $b->[1] <=> $a->[1] } @win_cs;
		
		# ��̏ꍇ�͈�ԍ��͏���
		shift @win_cs if @win_cs % 2 == 1;
		
		my $half_c = int(@win_cs*0.5-1);
		for my $i (0 .. $half_c) {
			my $c_c = &union($win_cs[$i][0],$win_cs[$#win_cs-$i][0]);
			$w{'p_'.$c_c} = 1;
		}
	}
	elsif ($w{world} eq '18') { # �E��
		$w{reset_time} = $time;
		for my $i (1 .. $w{country}) {
			$cs{food}[$i]     = int(rand(300)) * 1000;
			$cs{money}[$i]    = int(rand(300)) * 1000;
			$cs{soldier}[$i]  = int(rand(300)) * 1000;
		}
	}
	elsif (&is_festival_world($w{world})) {
		&write_world_news("�Ղ��˓�");
		if ($w{world} eq $#world_states-4) { # �p�Y
			$w{game_lv} += 20;
			for my $i (1 .. $w{country}) {
				$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
			}
		}
		elsif ($w{world} eq $#world_states-2) { # �s��ՓV
			$w{game_lv} = 99;
			$migrate_type = add_festival_country('kouhaku');
#			$w{country} += 2;
#			my $max_c = int($w{player} / 2) + 3;
#			for my $i ($w{country}-1..$w{country}){
#				mkdir "$logdir/$i" or &error("$logdir/$i ̫��ނ����܂���ł���") unless -d "$logdir/$i";
#				for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
#					my $output_file = "$logdir/$i/$file_name.cgi";
#					next if -f $output_file;
#					open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
#					close $fh;
#					chmod $chmod, $output_file;
#				}
#				for my $file_name (qw/leader member/) {
#					my $output_file = "$logdir/$i/$file_name.cgi";
#					open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
#					close $fh;
#					chmod $chmod, $output_file;
#				}
#				&add_npc_data($i);
#				# create union file
#				for my $j (1 .. $i-1) {
#					my $file_name = "$logdir/union/${j}_${i}";
#					$w{ "f_${j}_${i}" } = -99;
#					$w{ "p_${j}_${i}" } = 2;
#					next if -f "$file_name.cgi";
#					open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ̧�ق����܂���");
#					close $fh;
#					chmod $chmod, "$file_name.cgi";
#					open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ̧�ق����܂���");
#					close $fh2;
#					chmod $chmod, "${file_name}_log.cgi";
#					open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ̧�ق����܂���");
#					close $fh3;
#					chmod $chmod, "${file_name}_member.cgi";
#				}
#				unless (-f "$htmldir/$i.html") {
#					open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ̧�ق����܂���");
#					close $fh_h;
#				}
#				$cs{name}[$i]     = $i == $w{country} ? "�����̂��̗�":"���̂��̎R";
#				$cs{color}[$i]    = $i == $w{country} ? '#ff0000':'#ffffff';
#				$cs{member}[$i]   = 0;
#				$cs{win_c}[$i]    = 999;
#				$cs{tax}[$i]      = 99;
#				$cs{strong}[$i]   = 75000;
#				$cs{food}[$i]     = 0;
#				$cs{money}[$i]    = 0;
#				$cs{soldier}[$i]  = 0;
#				$cs{state}[$i]    = 0;
#				$cs{capacity}[$i] = $max_c;
#				$cs{is_die}[$i]   = 0;
#				my @lines = &get_countries_mes();
#				if ($w{country} > @lines - 2) {
#					open my $fh9, ">> $logdir/countries_mes.cgi";
#					print $fh9 "<>$default_icon<>\n";
#					print $fh9 "<>$default_icon<>\n";
#					close $fh9;
#				}
#			}
#			$migrate_type = festival_type('kouhaku', 1);
#			
#			for my $i (1 .. $w{country}-2) {
#				$cs{strong}[$i]   = 0;
#				$cs{food}[$i]     = 0;
#				$cs{money}[$i]    = 0;
#				$cs{soldier}[$i]  = 0;
#				$cs{state}[$i]    = 0;
#				$cs{capacity}[$i] = 0;
#				$cs{is_die}[$i]   = 1;
#	
#				for my $j ($i+1 .. $w{country}-2) {
#					$w{ "f_${i}_${j}" } = -99;
#					$w{ "p_${i}_${j}" } = 2;
#				}
#	
#				$cs{old_ceo}[$i] = $cs{ceo}[$i];
#				$cs{ceo}[$i] = '';
#				
#				open my $fh, "> $logdir/$i/leader.cgi";
#				close $fh;
#			}
		}
		elsif ($w{world} eq $#world_states-3) { # �O���u
			$w{game_lv} = 99;
			$migrate_type = add_festival_country('sangokusi');
#			$w{country} += 3;
#			my $max_c = int($w{player} / 3) + 3;
#			for my $i ($w{country}-2..$w{country}){
#				mkdir "$logdir/$i" or &error("$logdir/$i ̫��ނ����܂���ł���") unless -d "$logdir/$i";
#				for my $file_name (qw/bbs bbs_log bbs_member depot depot_log patrol prison prison_member prisoner violator old_member/) {
#					my $output_file = "$logdir/$i/$file_name.cgi";
#					next if -f $output_file;
#					open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
#					close $fh;
#					chmod $chmod, $output_file;
#				}
#				for my $file_name (qw/leader member/) {
#					my $output_file = "$logdir/$i/$file_name.cgi";
#					open my $fh, "> $output_file" or &error("$output_file ̧�ق����܂���ł���");
#					close $fh;
#					chmod $chmod, $output_file;
#				}
#				&add_npc_data($i);
#				# create union file
#				for my $j (1 .. $i-1) {
#					my $file_name = "$logdir/union/${j}_${i}";
#					$w{ "f_${j}_${i}" } = -99;
#					$w{ "p_${j}_${i}" } = 2;
#					next if -f "$file_name.cgi";
#					open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ̧�ق����܂���");
#					close $fh;
#					chmod $chmod, "$file_name.cgi";
#					open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ̧�ق����܂���");
#					close $fh2;
#					chmod $chmod, "${file_name}_log.cgi";
#					open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ̧�ق����܂���");
#					close $fh3;
#					chmod $chmod, "${file_name}_member.cgi";
#				}
#				unless (-f "$htmldir/$i.html") {
#					open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ̧�ق����܂���");
#					close $fh_h;
#				}
#				$cs{name}[$i]     = $i == $w{country}-2 ? '�':
#									$i == $w{country}-1 ? '��':
#														'�';
#				$cs{color}[$i]    = $i == $w{country}-2 ? '#4444ff':
#									$i == $w{country}-1 ? '#ff4444':
#														'#44ff44';
#				$cs{member}[$i]   = 0;
#				$cs{win_c}[$i]    = 999;
#				$cs{tax}[$i]      = 99;
#				$cs{strong}[$i]   = 50000;
#				$cs{food}[$i]     = 0;
#				$cs{money}[$i]    = 0;
#				$cs{soldier}[$i]  = 0;
#				$cs{state}[$i]    = 0;
#				$cs{capacity}[$i] = $max_c;
#				$cs{is_die}[$i]   = 0;
#				my @lines = &get_countries_mes();
#				if ($w{country} > @lines - 3) {
#					open my $fh9, ">> $logdir/countries_mes.cgi";
#					print $fh9 "<>$default_icon<>\n";
#					print $fh9 "<>$default_icon<>\n";
#					print $fh9 "<>$default_icon<>\n";
#					close $fh9;
#				}
#			}
#			$migrate_type = festival_type('sangokusi', 1);
#			for my $i (1 .. $w{country}-3) {
#				$cs{strong}[$i]   = 0;
#				$cs{food}[$i]     = 0;
#				$cs{money}[$i]    = 0;
#				$cs{soldier}[$i]  = 0;
#				$cs{state}[$i]    = 0;
#				$cs{capacity}[$i] = 0;
#				$cs{is_die}[$i]   = 1;
#	
#				for my $j ($i+1 .. $w{country}-2) {
#					$w{ "f_${i}_${j}" } = -99;
#					$w{ "p_${i}_${j}" } = 2;
#				}
#	
#				$cs{old_ceo}[$i] = $cs{ceo}[$i];
#				$cs{ceo}[$i] = '';
#				
#				open my $fh, "> $logdir/$i/leader.cgi";
#				close $fh;
#			}
		}
		elsif ($w{world} eq $#world_states-5) { # �ّ�
			$migrate_type = festival_type('sessoku', 1);
		}
		elsif ($w{world} eq $#world_states-1) { # ����
			$migrate_type = festival_type('konran', 1);
		}
	}
	
	$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.7):$w{game_lv};
	
	&refresh;
	&n_menu;
	&write_cs;
	
	require "./lib/reset.cgi";
	&player_migrate($migrate_type);
}

1; # �폜�s��
