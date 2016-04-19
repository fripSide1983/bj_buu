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
	# ���ꎞworld�Ɗ����؂ꎞreset�ő΂ɂ���������������҂̉�ʂɂ��\�����邽�ߒf�O
	# �����ɂ����铝�ꎞ�̕����� _war_result.cgi ������������

	# �Ղ����ɓ���
	if (&is_festival_world) {
		if ($w{world} eq $#world_states-1) { # ����
			$migrate_type = &festival_type('konran', 0);
		}
		elsif ($w{world} eq $#world_states-2) { # �s��ՓV
			$migrate_type = &festival_type('kouhaku', 0);
			$w{country} -= 2;
		}
		elsif ($w{world} eq $#world_states-3) { # �O���u
			$migrate_type = &festival_type('sangokusi', 0);
			$w{country} -= 3;
		}
		&player_migrate($migrate_type);
	}

	$mes .= "���Ȃ��͂��̐��E�ɉ������߂܂���?<br>";
	&menu('�F���]�ނ���','��]','��]','���a');
	$m{tp} += 10;
}

sub tp_110 {
	my $old_world = $w{world};

	&show_desire unless $w{year} =~ /5$/;
	if ($w{year} =~ /9$/) { # �Ղ��J�n��
		my $year = $w{year} + 1;
		if ($year % 40 == 0) { # �s��ՓV
			&write_world_news("<i>$m{name}�̊肢�͋󂵂����E�͓�ɕ�����܂���</i>");
		}
		elsif ($year % 40 == 20) { # �O���u
			&write_world_news("<i>$m{name}�̊肢���󂵂����􂵂����E�𓝈ꂷ�ׂ��O�����䓪���܂���</i>");
		}
		elsif ($year % 40 == 10) { # �ّ�
			&write_world_news("<i>$m{name}�̊肢���󂵂����E�������������Ƃ�</i>");
		}
		else { # ����
			&write_world_news("<i>$m{name}�̊肢�͋󂵂����E�͍����Ɋׂ�܂���</i>");
		}
	}
	elsif (!$w{year} =~ /5$/) {# �����J�n���ł͂Ȃ�
		my @new_worlds;
		if ($cmd eq '1') {# ��]
			@new_worlds = (1,2,3,4,5,6,7,17,18,19,20);
		}
		elsif ($cmd eq '2') {# ��]
			@new_worlds = (8,9,10,11,12,13,14,15,16);
		}
		elsif ($cmd eq '3') {# ���a
			@new_worlds = (0);
		}
		else {
			@new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
		}
		my @next_worlds = &unique_worlds(@new_worlds);
		$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
		$w{world_sub} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];

		# �����̂���܂�Ȃ��̂�
		if ($w{world} eq $old_world) {
			$w{world} = int(rand($#world_states-5));
			++$w{world} if $w{world} eq $old_world;
			$w{world} = int(rand(10)) if $w{world} >= $#world_states-5;
			&write_world_news("<i>���E�� $world_states[$old_world] �ƂȂ�܁c���� $world_states[$w{world}]�ƂȂ�܂���</i>");
		}
		else {
			if ($w{world} eq '0') {# ���a
				&write_world_news("<i>���E�� $world_states[$w{world}] �ɂȂ�܂���</i>");
			}
			elsif ($w{world} eq '18') {# �E��
				&write_world_news("<i>���E�� $world_states[$w{world}] �Ƃ����ӂ���(���Ȃ����ϊ��ł��Ȃ�)�ɂȂ�܂���</i>");
			}
			else {
				&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
			}
		}
		$w{game_lv} = int($w{game_lv} * 0.7) if $w{world} eq '15' || $w{world} eq '17';
	}# else {# �����J�n���ł͂Ȃ�

	require './lib/reset.cgi';
	&reset; # �����܂ō������ꎞ�̏���

	my $migrate_type = 0;
	# ���E� �����˓�
	if ($w{year} =~ /6$/) { # �Í��E�p�Y
		&show_desire;
		&write_world_news("<i>$m{name}�̊肢�͂���������܂���</i>");
	}
	elsif ($w{year} =~ /0$/) {
		require './lib/_festival_world.cgi';
		$migrate_type = &opening_festival;
		&wt_c_reset;
	}

#	unshift @old_worlds, $w{world};
	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgi���J���܂���");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$w{world}<>$nline\n";
	close $fh;

#	my $migrate_type = 0;
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
#	elsif (&is_festival_world) {# �Ղ��Ȃ��
#		if ($w{world} eq $#world_states-1) { # ����
#			$migrate_type = &festival_type('konran', 1);
#		}
#		elsif ($w{world} eq $#world_states-2) { # �s��ՓV
#			$w{game_lv} = 99;
#			$migrate_type = &add_festival_country('kouhaku');
#		}
#		elsif ($w{world} eq $#world_states-3) { # �O���u
#			$w{game_lv} = 99;
#			$migrate_type = &add_festival_country('sangokusi');
#		}
#		elsif ($w{world} eq $#world_states-4) { # �p�Y
#			$w{game_lv} += 20;
#			for my $i (1 .. $w{country}) {
#				$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
#			}
#		}
#		elsif ($w{world} eq $#world_states-5) { # �ّ�
#			$migrate_type = &festival_type('sessoku', 1);
#		}
#	}

	$w{game_lv} = 0;
	&refresh;
	&n_menu;
	&write_cs;

#	require "./lib/reset.cgi";
#	&player_migrate($migrate_type);
	&player_migrate($migrate_type) if &is_festival_world;
}

# �v���C���[�̖]�݂�\������
sub show_desire {
	if ($cmd eq '1') {# ��]
		&mes_and_world_news("<b>���E�Ɋ�]��]�݂܂���</b>", 1);
	}
	elsif ($cmd eq '2') {# ��]
		&mes_and_world_news("<b>���E�ɐ�]��]�݂܂���</b>", 1);
	}
	elsif ($cmd eq '3') {# ���a
		&mes_and_world_news("<b>���E�ɕ��a��]�݂܂���</b>", 1);
	}
	else {
		&mes_and_world_news('<b>���E�ɂ݂Ȃ��]�ނ��̂�]�݂܂���</b>', 1);
	}
}

1; # �폜�s��