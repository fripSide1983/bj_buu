sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
#require './lib/reset.cgi';
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
#	if (&is_festival_world) {
#		if ($w{world} eq $#world_states-1) { # ����
#			$migrate_type = &festival_type('konran', 0);
#		}
#		elsif ($w{world} eq $#world_states-2) { # �s��ՓV
#			$migrate_type = &festival_type('kouhaku', 0);
#			$w{country} -= 2;
#		}
#		elsif ($w{world} eq $#world_states-3) { # �O���u
#			$migrate_type = &festival_type('sangokusi', 0);
#			$w{country} -= 3;
#		}
#		&player_migrate($migrate_type);
#	}

#	&reset;

	$mes .= "���Ȃ��͂��̐��E�ɉ������߂܂���?<br>";
	&menu('�F���]�ނ���','��]','��]','���a');
	$m{tp} += 10;
}

sub tp_110 {
	my $old_world = $w{world};

	&show_desire;
	if (&is_special_world) { # �����̊J�n��
		if ($w{year} =~ /6$/) { # �Í��E�p�Y
			&write_world_news("<i>$m{name}�̊肢�͂���������܂���</i>");
		}
		elsif ($year % 40 == 0) { # �s��ՓV
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
	else (!$w{year} =~ /5$) { # �����ȊO�̊J�n��
		my @new_worlds;
		if ($cmd eq '1') { # ��]
			@new_worlds = (1,2,3,4,5,6,7,17,18,19,20);
		}
		elsif ($cmd eq '2') { # ��]
			@new_worlds = (8,9,10,11,12,13,14,15,16);
		}
		elsif ($cmd eq '3') { # ���a
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
			if ($w{world} eq '0') { # ���a
#				Unrecognized character \x90; marked by <-- HERE after
				&write_world_news('<i>���E�� '.$world_states[$w{world}].' �ɂȂ�܂���</i>');
			}
			elsif ($w{world} eq '18') { # �E��
				&write_world_news("<i>���E�� $world_states[$w{world}] �Ƃ����ӂ���(���Ȃ����ϊ��ł��Ȃ�)�ɂȂ�܂���</i>");
			}
			else {
				&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
			}
		}
		$w{game_lv} = int($w{game_lv} * 0.7) if $w{world} eq '15' || $w{world} eq '17';
	}# else { # �����ȊO�̊J�n��

#	require './lib/reset.cgi';
#	&reset; # �����܂ō������ꎞ�̏���

#	my $migrate_type = 0;
	# ���E� �����˓�
#		&show_desire;
#	}
#	elsif ($w{year} =~ /0$/) {
#		require './lib/_festival_world.cgi';
#		$migrate_type = &opening_festival;
#		&wt_c_reset;
#	}

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
	&opening_common;
#	elsif (&is_festival_world) { # �Ղ��Ȃ��
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
#	&player_migrate($migrate_type) if &is_festival_world;
}

# �v���C���[�̖]�݂�\������
sub show_desire {
	if ($cmd eq '1') { # ��]
		&mes_and_world_news("<b>���E�Ɋ�]��]�݂܂���</b>", 1);
	}
	elsif ($cmd eq '2') { # ��]
		&mes_and_world_news("<b>���E�ɐ�]��]�݂܂���</b>", 1);
	}
	elsif ($cmd eq '3') { # ���a
		&mes_and_world_news("<b>���E�ɕ��a��]�݂܂���</b>", 1);
	}
	else {
		&mes_and_world_news('<b>���E�ɂ݂Ȃ��]�ނ��̂�]�݂܂���</b>', 1);
	}
}

1; # �폜�s��