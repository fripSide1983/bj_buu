sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('��۸��Ѵװ�ُ�ȏ����ł�'); }
require './lib/reset.cgi';
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
		my $old_world = $w{world};
		my @new_worlds;
		if ($cmd eq '1') { # ��]
			@new_worlds = (1,2,3,4,5,6,7,17,18,19,20);
		}
		elsif ($cmd eq '2') { # ��]
			@new_worlds = (8,9,10,11,12,13,14,15,16);
		}
		elsif ($cmd eq '3') { # ���a
			@new_worlds[0] = 0; # (0) �ɂ���Ƌ�̔z��ɂȂ���ۂ� ���a��]�񂾎��ɏ���X�g���󈵂��ɂȂ��ē�ɂȂ�
		}
		else {
			@new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
		}
		($w{world}, $w{world_sub}) = &choice_unique_world(@new_worlds);

		# �����̂���܂�Ȃ��̂�
		if ($w{world} eq $old_world) {
			$w{world} = int(rand($#world_states-5));
			++$w{world} if $w{world} eq $old_world;
			$w{world} = int(rand(10)) if $w{world} >= $#world_states-5;
			&write_world_news("<i>���E�� $world_states[$old_world] �ƂȂ�܁c���� $world_states[$w{world}]�ƂȂ�܂���</i>");
		}
		elsif ($w{world} eq '0') { # ���a
			&write_world_news("<i>���E�� $world_states[$w{world}] �ɂȂ�܂���</i>");
		}
		elsif ($w{world} eq '18') { # �E��
			&write_world_news("<i>���E�� $world_states[$w{world}] �Ƃ����ӂ���(���Ȃ����ϊ��ł��Ȃ�)�ɂȂ�܂���</i>");
		}
		else {
			&write_world_news("<i>���E�� $world_states[$w{world}] �ƂȂ�܂���</i>");
		}
	}# else { # �����ȊO�̊J�n��
	&add_world_log($w{world});
	&begin_common_world;

	&refresh;
	&n_menu;
	&write_cs;
}

1; # �폜�s��