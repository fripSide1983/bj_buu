sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
require './lib/reset.cgi';
#require './lib/_world_reset.cgi';
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
	if (&is_special_world) { # �����̊J�n��
		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # �p�Y
			&write_world_news("<i>$m{name}�̊肢�͋󂵂����E�͉p�Y���`�������o������ɂȂ�܂���</i>");
		}
		elsif ($w{year} =~ /6$/) { # �Í�
			&write_world_news("<i>$m{name}�̊肢�͂���������܂���</i>");
		}
		elsif ($w{year} % 40 == 0) { # �s��ՓV
			&write_world_news("<i>$m{name}�̊肢�͋󂵂����E�͓�ɕ�����܂���</i>");
		}
		elsif ($w{year} % 40 == 20) { # �O���u
			&write_world_news("<i>$m{name}�̊肢���󂵂����􂵂����E�𓝈ꂷ�ׂ��O�����䓪���܂���</i>");
		}
		elsif ($w{year} % 40 == 10) { # �ّ�
			&write_world_news("<i>$m{name}�̊肢���󂵂����E�������������Ƃ�</i>");
		}
		else { # ����
			&write_world_news("<i>$m{name}�̊肢�͋󂵂����E�͍����Ɋׂ�܂���</i>");
		}
	}
	else { # �����ȊO�̊J�n��
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

		($w{world}, $w{world_sub}) = &choice_unique_world(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);

#		my @next_worlds = &unique_worlds(@new_worlds);
#		$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
#		$w{world_sub} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];

		# �����̂���܂�Ȃ��̂�
		if ($w{world} eq $old_world) {
			$w{world} = int(rand($#world_states-5));
			++$w{world} if $w{world} eq $old_world;
			$w{world} = int(rand(10)) if $w{world} >= $#world_states-5;
			&write_world_news("<i>���E�� $world_states[$old_world] �ƂȂ�܁c���� $world_states[$w{world}]�ƂȂ�܂���</i>");
		}
		&begin_common_world;
#		$w{game_lv} = int($w{game_lv} * 0.7) if $w{world} eq '15' || $w{world} eq '17';
	}# else { # �����ȊO�̊J�n��
	&add_world_log($w{world});
#	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgi���J���܂���");
#	my $saved_w = 0;
#	$nline = "";
#	for my $old_w (@old_worlds){
#		next if $old_w =~ /[^0-9]/;
#		$nline .= "$old_w<>";
#		last if $saved_w > 15;
#		$saved_w++;
#	}
#	print $fh "$w{world}<>$nline\n";
#	close $fh;

#	$w{game_lv} = 0;
	&refresh;
	&n_menu;
	&write_cs;
}

1; # �폜�s��