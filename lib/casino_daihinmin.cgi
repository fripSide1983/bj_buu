#================================================
# ��n��
#================================================
=pod
�u�I�[��[�����Ư�Ͻ��]�F�قƂ�Ǔǂ߂ˁ[�ł����ǂ��[���Ɨ���ǂ��������A�m���ɎQ��������肪�������� (�C��s�s�ٲ� : 9/1 23:19)
�u�I�[��[�����Ư�Ͻ��]�F�v���t��������3 �l�������ƌ��̕��̃v���C���[��10�����u��������H(�ˁ[���H) (�C��s�s�ٲ� : 9/1 23:15)
�u�I�[��[�����Ư�Ͻ��]�F�v���t��������2 ���f���ꂽ�v���C��10�����u�Ń��Z�b�g�������ĂȂ��� (�C��s�s�ٲ� : 9/1 23:13)
�u�I�[��[�����Ư�Ͻ��]�F�v���t��������1 �v���C���ɖ��Q���҂��e�ɂȂ�{�^���������Ƃ��̃����o�[�t�@�C������ (�C��s�s�ٲ� : 9/1 23:12)
1<>1504707895<>�u�I�[��,�����r�g�m,���N�K�C��,����,<>�����r�g�m:0:32,8;���N�K�C��:0:15,41,43,34,36,37;����:1:27,5,31,44,10,23,49,11,26,53;<>0<>���N�K�C��<>16<><><>2<>1<><>

play card get
game data open
pass or play check
pass
field refresh check
turn change1
turn change2
header 1<>1504793392<>�ԂԂ�,����,���޽,�����r�g�m,su-,<>���޽:1:3,29,17,19,20,47,9,36,54;�����r�g�m:0:16,18,11;su-:1:15,8,13,53;�ԂԂ�:0:1,42,43,31,45,46,10,12,38;����:1:2,41,32,37,25,39;<>0<>su-<><><><><><><> 
=cut

require './lib/_casino_funcs.cgi';

$header_size = 7; # ��n���p��ͯ�ް���� �e�A��̶��ށA���ҁA�����o���E�K�i�̔���A�X�[�g����A�v���A�C���o
($_leader, $_field_card, $_winner, $_bind_m, $_bind_s, $_revo, $_back) = ($_header_size .. $_header_size + $header_size - 1); # ͯ�ް�z��̲��ޯ��
$coin_lack = 0; # 0 ��݂�ڰĂɑ���Ȃ��ƎQ���ł��Ȃ� 1 ��݂�ڰĂɑ���Ȃ��Ă��Q���ł���
$min_entry = 2; # �Œ�2�l
$max_entry = 8; # �ō�8�l

my @nums = ('3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'Jo'); # �Ⴂ��
my @suits = $is_mobile ? ('S', 'H', 'C', 'D', '') : ('&#9824;', '&#9825;', '&#9827;', '&#9826;', '');

my @rates = (0, 100, 1000, 3000, 10000, 30000);

sub run {

	&_default_run;
}

#================================================
# �ްщ�ʂɕ\���������̒�`
#================================================
sub show_game_info { # �e���ޯĊz�Ȃǂ̕\�� �Q���҂��O�ɕ\�������
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|�e:$head[$_leader] ڰ�:$head[$_rate]|;
}
#sub show_start_info { } # ��W���̹ްтɎQ�����Ă�����ڲ԰�ɕ\����������� _start_game_form �̏�ɕ\������� ��`���ĂȂ��Ă�����ɖ��Ȃ�
sub show_started_game { # �n�܂��Ă���ްт̕\�� �Q���҂������łȂ����� is_member �Ŕ��ʂ��؂�ւ���
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	my @members = &get_members($head[$_participants]);
	my @winners = &get_members($head[$_winner]);
	print "<br>";
	for my $i (1 .. @members) {
		print "$i�� $winners[$i-1],";
	}
	&show_status(@head);
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants], $head[$_field_card], $head[$_winner]) if &is_member($head[$_participants], "$m{name}"); # �ްтɎQ�����Ă���
}
#sub show_tale_info { # ��`���ĂȂ��Ă�����ɖ��Ȃ�
#	my ($m_turn, $m_value, $m_stock, @head) = @_;
#	&show_status($head[$_participants_datas]) if $head[$_participants];
#}

=pod
#================================================
# �e�ɂȂ�̫��
#================================================
sub participants_form {
	# ���ɖ��̏���
	print qq|<form method="$method" action="$this_script" name="form">|;
	print "���[�g�F".&create_select_menu("rate", @rates);
	print &create_submit("leader", "�e�ɂȂ�");
	print qq|</form>|;
}

#================================================
# �e�ɂȂ鏈��
#================================================
sub leader {
	&_participate(0, 0, '');
}
=cut
#================================================
# �Q������̫��
#================================================
sub participate_form {
	my ($leader) = @_;
	my $button = $leader ? "�Q������" : "�e�ɂȂ�";
	# ���ɖ��̏���
	print qq|<form method="$method" action="$this_script" name="form">|;
	print "���[�g�F".&create_select_menu("rate", 0, @rates) unless $leader;
	print &create_submit("participate", "$button");
	print qq|</form>|;
}

#================================================
# �Q�����鏈�� ڰĂ̂��߂��ݸ����
#================================================
sub participate {
	&_participate($rates[$in{rate}], 0, '');
}

#================================================
# �J�n���鏈�� ���ۂ̃t�@�C������� _casino_funcs.cgi _start_game
#================================================
sub start_game {
	my ($fh, $head_line, $ref_members, $ref_game_members) = @_;
	my @head = split /<>/, $$head_line; # ͯ�ް
	my @participants = &get_members($head[$_participants]);
	my $is_start = 0;
	# ���ɖ��̏���
	my @cards;
	my $leader_i = 0; # �޲Ԃ�3�������Ă���Q���҂̲��ޯ��

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # �Q���҂��K�v�\���A�ްъJ�n�O�Ȃ�
		($is_start, $head[$_state], $head[$_lastupdate], $head[$_field_card]) = (1, 1, $time, '');
		# ���ɖ��̏���
		my $size = @participants;
		my @deck = &shuffled_deck($size);
		my $i = 0;
		while (@deck) {
			my $c = shift @deck;
			$leader_i = $i if $c == 40; # �޲Ԃ�3
			push @{$cards[$i]}, $c;
			$i = $#participants <= $i ? 0 : $i + 1;
		}
	}
	my $c = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			# ���ɖ��̏���
			@{$cards[$c]} = sort { $a <=> $b } @{$cards[$c]};
			${"card_$_"} = '' for (0 .. 13);
			for my $i (0 .. $#{$cards[$c]}) {
				my $j = ${$cards[$c]}[$i];
				if ($j == 53 || $j == 54) { # ���ނ��ݸ���ɿ�� �ݸ���ɕϐ��Ɋi�[���Ō��1�Ɍ���
					${"card_13"} .= "$j,";
				}
				else {
					${"card_".($j-1)%13} .= "$j,";
				}
			}
			$mstock .= ${"card_$_"} for (0 .. 13); # 1�Ɍ���
			($mtime, $mturn) = ($time, 2);
			if ($leader_i == $c) { # �޲Ԃ�3�������Ă���Q���҂���ԂɈړ�
				$head[$_leader] = $mname;
			}
			$c++;

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
	$head[$_participants] = &change_turn($head[$_participants]) for (0 .. $leader_i-1);

	$$head_line = &h_to_s(@head);
}

#================================================
# ��ڲ��̫�� ��{���ɖ��ɊہX����������K�v������
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants, $field_cards, $pass) = @_;
	my @hand_cards = split /,/, $m_stock;
	my @participants = &get_members($participants);

	if ($participants[0] eq $m{name}) {
		my $is_joker = 0;
		print "<br>��D�F".@hand_cards."��<br>";
		print qq|<form method="$method" action="$this_script" name="form">|;
		unless (0 < $m_value && 0 < $pass) {
			for my $hand_card (@hand_cards) {
				my ($num, $suit) = &get_card($hand_card);
				$is_joker = 1 if $num == 13;
				print &create_check_box("card_$hand_card", "$hand_card", "$suits[$suit]$nums[$num] ���o��<br>");
			}
			if ($field_cards eq '' && $is_joker) { # ��D���Ȃ��A��D�ɼޮ���������Ƃ�
				print &create_radio_button('joker', 1, '�������o��');
				print ' ';
				print &create_radio_button('joker', 2, '�K�i�o��<br>');
			}
		}
		print &create_submit("play", "���ނ��o��");
		print qq|</form>|;
	}
	else {
		my @cards = ();
		print qq|<br>$participants[0]���v�l���ł�<br>|;
		for my $hand_card (@hand_cards) {
			my ($num, $suit) = &get_card($hand_card);
			push @cards, "$suits[$suit]$nums[$num]";
		}
		print "��D�F".@hand_cards."�� ".&create_select_menu("card", 0, @cards);
		print "<br>";
	}
}

#================================================
# ��ڲ�̏���
#================================================
sub play {
	my @members = ();
	my $result_mes = '';
	my $winner = '';
	my $is_reset = 0;

	# ���ɖ��̏���
	$mes .= "play card get<br>";
	my @play_cards = ();
	my $is_joker = 0;
	for my $i (1 .. 54) {
		if ($in{"card_$i"}) {
			$is_joker++ if $i == 53 || $i == 54;
			push @play_cards, $in{"card_$i"} ;
		}
	}

	# ��̋����I���� ̧�ٵ���݂��� while ٰ�߂̊Ԃ��S�b�\�������Ă�
	# �����������݂Ńt�@�C������ꂽ�Ƃ��t�@�C���̒��g��ǂݎ��Ȃ��������H
	# �ł����̒��x�ł���Ȃ��ƂɂȂ�Ȃ獑�t�@�C�������ƃ��o���͂�
	# play card get game data open field refresh check header <><><><><><><><><><><><>

	my ($is_playable, $play_mes, $is_sequence, $is_double) = (0, '', 0, 0);
	my $is_pass = 0;
	my ($is_eight_cut, $is_s3_cut, $is_pass_cut) = (0, 0, 0);

	$mes .= "game data open<br>";
	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ͯ�ް
	my @participants = &get_members($head[$_participants]);
	my @winners = &get_members($head[$_winner]);
	my %pass_datas = (); # �Q���҂̃p�X��������
	my $is_my_turn = $head[$_state] && $participants[0] eq $m{name} && 2 <= $m{c_turn}; # �J�n���Ă���ްтɎQ�����Ă��Ď��������
	while (my $line = <$fh>) { # �S��ڲ԰�ް����ォ�瑖��
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_my_turn && $mname eq $m{name}) {
			$head[$_lastupdate] = $time;
			$mtime = $time;

			$mes .= "pass or play check<br>";
			unless (@play_cards) { # �p�X
				$mes .= "pass<br>";
				$mvalue = 1;
				$is_pass = 1;
			}
			else { # �J�[�h���o���Ă���
				$mes .= "play card check<br>";
				# �o�������ނ��ׂĂ���D�ɂ��邩 ���؂�Ȃ���݂�ύX���Ȃ����ނ��o���āu�߂�v�����A�ēx���o�������؂�Ȃ���݂�ύX���Ȃ����ނ��ēx�o����i�������ނ����X�o���邾���Ŏ��Q�͂Ȃ��j
				my $eq_num = 0;
				my @hand_cards = split /,/, $mstock;
				for my $hand_card (@hand_cards) {
					for my $play_card (@play_cards) {
						$eq_num ++ if $hand_card == $play_card;
					}
				}
				unless ($eq_num == @play_cards) { # �o�������ނ���D�ɂȂ�������X���[
					$mes .= '<p>�s������ ��D�ɂȂ����ނ��o�����Ƃ��Ă��܂�</p>';
#					$pass_datas{$mname} = $mvalue if 1 < $mturn; # �Q���҂��߽���̎擾
#					$is_reset++ if 1 < $mturn && 1 < $mvalue;
					push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
					next;
				}

				my $play_cards = join(",", @play_cards);

				# �o�����J�[�h��ٰقɑ����Ă��邩
				$mes .= "playable check<br>";
				($is_playable, $result_mes, $is_sequence, $is_double) = &is_playable($play_cards, $head[$_field_card], $head[$_bind_m], $head[$_bind_s], $head[$_revo]);

				$mes .= "joker check<br>";
				# �ޮ������܂�2���ȏ�̶���
				if ($head[$_field_card] eq '' && 1 < @play_cards && $is_joker) {
					$is_joker = $in{joker}; # 1 �������o�� 2 �K�i�o��
					unless ($is_joker) {
						$mes .= '<p>ٰوᔽ �ޮ������o���Ƃ��͖���錾���Ă�������</p>';
						($is_playable, $result_mes) = (0, '');
					}
				}

				if ($is_playable) { # �o�������ނ�ُٰ�F�߂��Ă���
					$mes .= "playable ok<br>";

					$mes .= "multi or sequence check<br>";
					# �������o���E�K�i�o���̔���ݒ�
					if ($head[$_field_card] eq '' && 1 < @play_cards) { # ����ɂ̂ݕ������Ȃǂ̔��蔭��
						if ($is_joker) {
							$mes .= "is_joker $is_joker is_sequence $is_sequence is_double $is_double";
							$head[$_bind_m] = $is_joker; # 1 �������o�� 2 �K�i�o��
						}
						else {
							$head[$_bind_m] = 1 if $is_double; # �������o��;
							$head[$_bind_m] = 2 if $is_sequence; # �K�i�o��
						}
					}

					$mes .= "revolution check<br>";
					# �v���ݒ� �������o���Ŋv�� �K�i�ł͔������Ȃ�
 					if (3 < @play_cards && $head[$_bind_m] == 1 && !$is_sequence) {
						$head[$_revo] = !$head[$_revo];
						$result_mes .= '<br>�v�����N�����܂���';
					}

					$mes .= "suit check<br>";
					# ��Ĕ���̐ݒ� �ޮ������܂܂�Ă��Ȃ���D������A�o�������ނɂ�ޮ������܂܂�Ă��Ȃ��Ȃ甛������
					if ($head[$_bind_s] eq '' && $head[$_field_card] && $head[$_field_card] !~ /53/ && $head[$_field_card] !~ /54/ && $is_joker == 0) {
						my $is_suit_lock = 1;
						my @suit_lock = ();
						my @field_cards = split /,/, $head[$_field_card];
						for my $i (0 .. $#play_cards) { # �o�������ނƏ�̶��ނ��ׂĂ𑖍� �o�������ނƏ�D�̐��͓���
							my @suit = ( (&get_card($play_cards[$i]))[1], (&get_card($field_cards[$i]))[1] );
							if ($suit[0] == $suit[1]) { # �o�������ނƏ�̶��ނ̽�Ă�����
								$suit_lock[$suit[0]] = 1;
							}
							else {
								$is_suit_lock = 0;
								last; # ��Ă��Ⴄ���_��ۯ�����Ȃ����Ƃ��m��
							}
						}
						if ($is_suit_lock) {
							$head[$_bind_s] = 0; # ������
							$head[$_bind_s] |= $suit_lock[$_] << $_ for (0 .. 3);
							$result_mes .= '<br>��Ĕ��肪�������܂���';
						}
					}

					$mes .= "eight cut check<br>";
					# ���؂�
					if ($head[$_bind_m] != 2 || $is_double && !$is_sequence) {
						for my $play_card (@play_cards) {
							unless ($play_card == 53 || $play_card == 54) {
								$is_eight_cut = 1 if ($play_card-1) % 13 == 5; # 1�`52 �̒l���� -1 �������̂� 13 �Ŋ������]�肪 0�`12 �ɂȂ�
							}
						}
					}

					$mes .= "s3 check<br>";
					# �X�y3�Ԃ�
					$is_s3_cut = 1 if (@play_cards == 1 && $play_cards[0] == 1 && ($head[$_field_card] == 53 || $head[$_field_card] == 54));

					$mes .= "new hand create<br>";
					my @new_hand_cards = ();
					for my $hand_card (@hand_cards) {
						my $is_eq = 0;
						for my $play_card (@play_cards) {
							if ($hand_card == $play_card) {
								$is_eq = 1;
								last;
							}
						}
						push @new_hand_cards, $hand_card unless $is_eq;
					}
					$mvalue = 0;
					$mstock = join(",", @new_hand_cards);
					$head[$_field_card] = $play_cards;

					$mes .= "win check<br>";
					unless ($mstock) {
						my $is_find = 0;
						if ($is_eight_cut || # ���؂�オ��
							$is_s3_cut || # ���3�Ԃ��オ��
							($is_double && (($head[$_field_card]-1) % 13) == 0) || # �v������ ���3 ��
							($is_double && (($head[$_field_card]-1) % 13) == 12) || # ��v������ ���2 ��
							(@play_cards == 1 && ( # �o�������ނ�1������
							($head[$_revo] && (($head[$_field_card]-1) % 13) == 0) || # �v������ 3 ��
							(!$head[$_revo] && (($head[$_field_card]-1) % 13) == 12) || # ��v������ 2 ��
							$head[$_field_card] eq '53' || $head[$_field_card] eq '54') ) ) { # �ޮ���
							$mes .= "taboo win<br>";
							for my $i (0 .. @participants-1) {
								unless ($winners[$#participants-$i] || $is_find) {
									$winners[$#participants-$i] = $m{name};
									$is_find = 1;
								}
							}
							$result_mes .= "<br>�֎~�オ��";
							$is_eight_cut = $is_s3_cut = 0;
						}
						else {
							$mes .= "win<br>";
							for my $i (0 .. $#participants) {
								unless ($winners[$i] || $is_find) {
									$winners[$i] = $m{name};
									$is_find = 1;
								}
							}
							$result_mes .= "<br>�オ��";
						}
						$head[$_winner] = join(",", @winners);
						$winner = $m{name};
						$mvalue = 2;
					}
				}
			}
		}
		if ($is_my_turn) {
			$pass_datas{$mname} = $mvalue if 1 < $mturn; # �Q���҂��߽���̎擾
			$is_reset++ if 1 < $mturn && 1 < $mvalue; # �Q���҂��オ��
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	$mes .= "field refresh check<br>";
	if ($is_my_turn && ($is_playable || $is_pass || $is_eight_cut || $is_s3_cut)) {
		my $pass_num = 0;
		my @next_num = (0, 0);
		my $refresh_num = 0;
		my $is_find = 0;
		unless ($is_eight_cut || $is_s3_cut) {
			$mes .= "turn change1<br>";
			for my $i (0 .. $#participants) {
				if ($next_num[0] == 0 && $participants[$i] ne $m{name} && $pass_datas{$participants[$i]} == 0) { # �߽�����Ă��Ȃ����߂���ڲ԰
					$next_num[0] = $i;
					$is_find = 1; # �߽�����Ă��Ȃ���ڲ԰����������
				}
				elsif ($pass_datas{$participants[$i]} == 1) { # �߽�����Ă�����ڲ԰
					$next_num[1] = $i if $next_num[1] == 0 && $participants[$i] ne $m{name}; # �߽�����Ă��钼�߂���ڲ԰
					$pass_num++;
				}
				elsif ($participants[$i] ne $m{name} && $pass_datas{$participants[$i]} == 2) { # �オ���Ă�����ڲ԰
					$refresh_num++;
				}
			}
		}

		$result_mes .= '�p�X' if $is_pass;
		if ($is_eight_cut || $is_s3_cut || ($is_find && @participants == ($pass_num+$refresh_num+1)) || (!$is_find && @participants == ($pass_num+$refresh_num))) { 
			$mes .= "turn change2<br>";
			($head[$_field_card], $head[$_bind_m], $head[$_bind_s]) = ('', '', '');
			$result_mes .= '<br>���؂�' if $is_eight_cut;
			$result_mes .= '<br>�X�y3�Ԃ�' if $is_s3_cut;
			$result_mes .= ' ��𗬂��܂���';
			for my $i (0 .. $#members) {
				my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $members[$i];
				next if $mturn < 2 || 1 < $mvalue;
				$members[$i] = "$mtime<>$mname<>$maddr<>$mturn<>0<>$mstock<>\n";
			}
		}

		# �߽�����Ă��Ȃ���ڲ԰������Ȃ璼�߂��߽�����Ă��Ȃ���ڲ԰�����
		# �S�����߽���Ă���Ȃ璼�߂��߽�����Ă�����ڲ԰�����
		$head[$_participants] = &change_turn($head[$_participants]) for (1 .. $next_num[!$is_find]) unless $is_eight_cut || $is_s3_cut; # ��ݏI�� 1��݂ŕ�����s������悤�ȹްтȂ���ı�Ă��A�ŏI�I�ȍs���Ŏ��s
	}

	my $penalty_coin = 0;
	my $size2 = @participants;
	$mes .= "if init_header is_my_turn $is_my_turn && is_reset $is_reset == participants $size2<br>";
	if ($is_my_turn && $winner eq $m{name} && ($is_playable || $is_pass) && $is_reset == @participants) { # �኱�s�K�v�Ȋ��������邯�ǂƂɂ����I������������
		$mes .= "reset1<br>";
		$penalty_coin = $head[$_rate];
		&init_header(\@head);
		&reset_members(\@members);
	}
	else { $is_reset = 0; }

	my $header = &h_to_s(@head);
	$mes .= "header $header<br>";
	unshift @members, $header; # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	# �I������
	if ($is_reset) {
		$mes .= "reset2<br>";
		my $winner_mes = '';
		my $loser_mes = '';
		my $move_c = 2 <= (@winners / 2) ? 2 : 1; # 4�l�ȏ�ź�݂̈ړ���2��N���� ��x��<->��n�� �x��<->�n�� 3�l�ȉ��ł� ��x��<->��n�� ��1��
		for my $i (0 .. $#winners) {
			if ($winners[$i] eq $m{name}) {
				$m{c_turn} = 0;
				&write_user;
			}
			else {
		 		&regist_you_data($winners[$i], 'c_turn', '0');
			}

			if ($i < $move_c) {
				&coin_move($penalty_coin / (1 + $i), $winners[$i], 1);
				$winner_mes .= "$winners[$i] �� ".($penalty_coin / (1 + $i))." ��ݓ��܂���<br>";

				&coin_move(-1 * $penalty_coin / (1 + $i), $winners[$#winners-$i], 1);
				$loser_mes = "$winners[$#winners-$i] �� ".($penalty_coin / (1 + $i))." ��ݕ����܂���<br>" . $loser_mes;
			}
			elsif ($i < @winners-$move_c) {
				$winner_mes .= "$winners[$i] �� 0 ��ݓ��܂���<br>";
			}
		}
		&system_comment("$winner_mes$loser_mes");
	}

	return $result_mes; # ��ڲ�̕�
}

sub show_status {
	my @head = @_;

	my @field_cards = split /,/, $head[$_field_card];
	my $field_num = @field_cards;

	print "<br>��ԁF";

	if ($head[$_revo]) {
		print "�v�� ";
	}

	# �������E�K�i�o������\��
	if ($field_num) {
		if ($head[$_bind_m] == 2) {
			print "$field_num���K�i����";
		}
		else {
			print "$field_num������";
		}
	}

	# ��Ĕ���\��
	if ($head[$_bind_s]) {
		print " ��Ĕ���(";
		my @suit_lock = ();
		for my $i (0 .. 3) {
			push @suit_lock, $suits[$i] if 1 & ($head[$_bind_s] >> $i);
		}
		print join " ", @suit_lock;
		print ")";
	}

	print "<br>��D�F";
	for my $i (0 .. $#field_cards) {
		my ($num, $suit) = &get_card($field_cards[$i]);
		print " " if $i != 0;
		print "$suits[$suit]$nums[$num]";
	}

	print "<br>��D�F";
	my @participants_datas = split /;/, $head[$_participants_datas];
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		my @hand_cards = split /,/, $datas[2];
		my $size = @hand_cards;
		print "$datas[0]�F$size�� ";
		print " ";
	}
}

sub shuffled_deck {
	my $participants = shift;
	my $size = 51; # ���ޖ��� 54�� Joker 2���L
	my @deck;

	@deck[$_] = $_+1 for (0 .. $size);
	for my $i (0 .. $size) {
		my $j = int(rand($i + 1)); # ���񂷂�x�ɗ����͈͂��L����
		my $temp = $deck[$i];
		$deck[$i] = $deck[$j];
		$deck[$j] = $temp;
	}

	# ��ײ��޶��� �Q���ґS����������D�����ɂȂ�悤�ɒ���
	my $blind_num = 54 % $participants;
	shift(@deck) for (0 .. $blind_num-1);
	splice(@deck, int(rand(@deck)), 0, "$_") for (53 .. 54); # �ޮ����͏��O�Ώۂ���O���

	return @deck;
}

sub get_card {
	my $card = shift;
	my ($num, $suit) = ('', '');
	if ($card == 53 || $card == 54) {
		($num, $suit) = (13, 4);
	}
	else {
		$num = ($card-1) % 13; # 1�`52 �̒l���� -1 �������̂� 13 �Ŋ������]�肪 0�`12 �ɂȂ�
		$suit = int(($card-1)/13); # 0��߰�� 1ʰ� 2���� 3�޲�
	}
	return ($num, $suit);
}

sub is_playable {
	my ($play_cards, $field_cards, $bind_m, $bind_s, $revo) = @_;
	my @play_cards = split /,/, $play_cards; # �o��������
	my @field_cards = split /,/, $field_cards; # ��̶���
	unless (@field_cards == 0 || @play_cards == @field_cards) { # ���ނ̖����������Ă��Ȃ�
		$mes .= '<p>ٰوᔽ �o���J�[�h��'. @field_cards .'���ɂ��Ă�������</p>';
		return (0, '');
	}

	my @play_card_datas = (); # �o�������ނ̏ڍ� [0]1���ڂ��ݸ [1]1���ڂ̽�� [2]2���ڂ��ݸ [3]2���ڂ̽�� ...
	($play_card_datas[$_*2], $play_card_datas[$_*2+1]) = &get_card($play_cards[$_]) for (0 .. $#play_cards);
	my @field_card_datas = (); # ��̶��ނ̏ڍ� [0]1���ڂ��ݸ [1]1���ڂ̽�� [2]2���ڂ��ݸ [3]2���ڂ̽�� ...
	($field_card_datas[$_*2], $field_card_datas[$_*2+1]) = &get_card($field_cards[$_]) for (0 .. $#field_cards);

	# �������� �v���֌W�Ȃ��ޮ����͏�ɍŋ����¼ޮ����ɑ΂��Ăͽ��3���ł�����
	my @num = ($play_card_datas[0], $field_card_datas[0]);
	unless ($revo) { # ��v����
		$num[0] = 14 if @play_cards == 1 && $play_card_datas[0] == 0 && $play_card_datas[1] == 0 && $field_card_datas[0] == 13; # ���3
	}
	else { # �v����
		$num[0] = -2 if @play_cards == 1 && $play_card_datas[0] == 0 && $play_card_datas[1] == 0 && $field_card_datas[0] == 13; # ���3
		$num[0] = -1 if $play_card_datas[0] == 13; # ��D�̼ޮ���
		$num[1] = -1 if $field_card_datas[0] == 13; # ��̼ޮ���
=pod
		my $is_joker = 0;
		for my $i (0 .. $#play_cards) {
			if ($play_card_datas[($#play_cards-$i)*2] == 13) {
				$is_joker = 1;
				next;
			}
			else {
				if ($is_joker) {
					$num[0] = $play_card_datas[($#play_cards-$i)*2] + 1;
				}
				else {
					$num[0] = $play_card_datas[($#play_cards-$i)*2];
				}
				last;
			}
		}
		$mes .= "joker" if $is_joker;
		$is_joker = 0;
		for my $i (0 .. $#field_cards) {
			if ($field_card_datas[($#field_cards-$i)*2] == 13) {
				$is_joker = 1;
				next;
			}
			else {
				if ($is_joker) {
					$num[1] = $field_card_datas[($#field_cards-$i)*2] + 1;
				}
				else {
					$num[1] = $field_card_datas[($#field_cards-$i)*2];
				}
				last;
			}
		}
=cut
	}

	if (0 < @field_cards && $num[$revo] <= $num[!$revo]) { # �v�����͔�r�Ώۂ����ւ��� $revo �Ž���
		$mes .= '<p>ٰوᔽ ��D��苭�����ނ��o���Ă�������</p>';
		return (0, '');
	}

	# ���3�Ԃ��ͽ�Ĕ��薳��
	if (!(@play_cards == 1 && $play_card_datas[0] == 0 && $play_card_datas[1] == 0 && $field_card_datas[0] == 13) && $bind_s) {
		my $play_suits = 0;
		my @play_suits = ();
		$play_suits[$play_card_datas[$_*2+1]] = 1 for (0 .. $#play_cards); # �o�������ނ��ׂĂ̽�Ă��擾
		$play_suits |= $play_suits[$_] << $_ for (0 .. 3); # ��ď����r�b�g�t���O�ɕϊ�
		unless ($bind_s == $play_suits) { # ����̃r�b�g�t���O�Ɠ���ł͂Ȃ�
			my $suit_xmatch = $bind_s ^ $play_suits;
			my $xmatch_num = 0;
			$xmatch_num += 1 & ($suit_xmatch >> $_) for (0 .. 3);

			my $joker_num = 0;
			for my $i (0 .. $#play_cards) {
				$joker_num++ if $play_card_datas[$i*2] == 13; # �ޮ����̖������擾
			}

			unless (($xmatch_num - $joker_num) == 0) { # ��ĈႢ�̐��Ƽޮ����̖�������������Ȃ��Ȃ罰Ă��ᔽ
				$mes .= '<p>ٰوᔽ ��D�Ɠ�����Ă̶��ނ��o���Ă�������</p>';
				return (0, '');
			}
		}
	}

	my @is_sequence = (); # [0] �o�������ނ��K�i�� [1] ��̶��ނ��K�i��
	my @is_double = (); # [0] �o�������ނ�����وȏォ [1] ��̶��ނ�����وȏォ
	if (1 < @play_cards) { # ���ʕ������E�K�i����
		$is_sequence[0] = &is_sequence(@play_card_datas); # �K�i����
		$is_double[0] = &is_double(@play_card_datas); # ���ʎD����������
		unless ($is_sequence[0] || $is_double[0]) {
			$mes .= '<p>ٰوᔽ �������o���Ƃ��͓��ʂő����邩�K�i�ɂ��Ă�������</p>';
			return (0, '');
		}
	}
	if (0 < @field_cards && (($bind_m == 1 && !$is_double[0]) || ($bind_m == 2 && !$is_sequence[0])) ) {
		if ($bind_m == 1) {
			$mes .= (0, '<p>ٰوᔽ �o���J�[�h��'. @field_cards .'���ɂ��Ă�������</p>');
		}
		else {
			$mes .= (0, '<p>ٰوᔽ �o���J�[�h���K�i�ɂ��Ă�������</p>');
		}
		return (0, '');
	}

	my $result_mes = '';
	$result_mes .= "$suits[$play_card_datas[$_*2+1]]$nums[$play_card_datas[$_*2]] " for (0 .. $#play_cards);
	$result_mes .= "���o���܂���";

	return (1, $result_mes, $is_sequence[0], $is_double[0]);
}

sub is_sequence {
	my @card_datas = @_;
	my $size = @card_datas / 2;
	my $is_sequence = 0;

	if (2 < $size) { # 3���ȏォ��K�i ����Ȃ�
		my ($is_suit, $is_joker) = (1, 0);
		my ($max, $min) = ($card_datas[0*2], $card_datas[1*2]); # 1���ڂ�2���ڂ������l��
		my @suit = ();
		$suit[0] = $card_datas[0*2+1]; # 1���ڂ̃X�[�g���擾
		for my $i (0 .. $size - 1) { # �ő�l�ƍŒ�l�̎擾
			$suit[1] = $card_datas[$i*2+1];
			$is_joker++ if $suit[1] == 4;
			if ($is_joker < 1 && $suit[0] != $suit[1]) {
				$is_suit = 0;
				last;
			}
			next if $is_joker; # �ޮ����͍ő�l�Ƃ��Đ����Ȃ�
			$max = $card_datas[$i*2] if $max < $card_datas[$i*2];
			$min = $card_datas[$i*2] if $card_datas[$i*2] < $min;
		}

		# �D 4�� 0��ޮ����Ƃ��� 0�`2 �ɂȂ�
		# 4007 = 7 - 4 + 1 = 4
		# 4060 = 6 - 4 + 1 = 3
		# 4500 = 5 - 4 + 1 = 2
		# �D 5�� 0��ޮ����Ƃ���
		# 45008 = 8 - 4 + 1 = 5
		# 45070 = 7 - 4 + 1 = 4
		# 45600 = 6 - 4 + 1 = 3
		my $diff = ($max - $min + 1);
		if ($is_joker < 2) { # �ޮ�����1���ȉ��܂܂��K�i
			if ($is_joker) {							# �ޮ�����1���܂܂��K�i�Ȃ�΁A
				my $diff2 = $size - $diff;			# ���ޖ������� (�ō��l - �Œ�l + 1) �������� 0 �` 1 �ɂȂ�
				$is_sequence = (($diff2 == 0 || $diff2 == 1) && $is_suit); # �i�ō��ʂ�Joker�ő�ւ���� 1�A���ʂ��� 0�j
			}
			else { # �ޮ������܂܂�Ȃ��K�i
				$is_sequence = ($diff == $size && $is_suit); # (�ō��l - �Œ�l + 1) == �o�������� && �X�[�g�����Ă�
			}
		}
		else { # �ޮ�����2���܂܂��K�i
			if ($size == 3) { $is_sequence = 1; } # �ޮ����ȊO��1�������Ȃ��K�i
			else {											# �ޮ�����2���܂܂��4���ȏ�̊K�i�Ȃ�΁A
				my $diff2 = $size - $diff;				 # �o�������ޖ������� (�ō��l - �Œ�l + 1) �������� 0 �` 2 �ɂȂ�
				$is_sequence = ((-1 < $diff2 && $diff2 < 3) && $is_suit); # �i�ō��ʂ�Joker�ő�ւ���� 2�A���ʂɂȂ�ɂ� 1�A0 �ƂȂ�j
			}
		}
	}
	return $is_sequence;
}

sub is_double {
	my @card_datas = @_;
	my $size = @card_datas / 2;
	my $is_double = 1;
	my @num = ($card_datas[0*2], '');
	for my $i (0 .. $size - 1) {
		$num[1] = $card_datas[$i*2];
		if ($num[1] != 13 && $num[0] != $num[1]) {
			$is_double = 0;
			last;
		}
	}
	return $is_double;
}

1;#�폜�s��
