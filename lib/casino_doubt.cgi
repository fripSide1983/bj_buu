#================================================
# �޳�
#================================================
require './lib/_casino_funcs.cgi'; # ���ĎQ��

$header_size = 2; # �޳ėp��ͯ�ް���� ��݁A��D
($_turn, $_field_cards) = ($_header_size .. $_header_size + $header_size - 1); # ͯ�ް�z��̲��ޯ��
$coin_lack = 0; # 0 ��݂�ڰĂɑ���Ȃ��ƎQ���ł��Ȃ� 1 ��݂�ڰĂɑ���Ȃ��Ă��Q���ł���
$min_entry = 4; # �Œ�4�l
$max_entry = 11; # �ō�11�l

my @rates = (0, 100, 1000, 3000, 10000, 30000);

my @nums = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K');
my @suits = ('��߰��', 'ʰ�', '����', '�޲�');

sub run {
	&_default_run;
}

#================================================
# �ްщ�ʂɕ\���������̒�`
#================================================
sub show_game_info { # �e���ޯĊz�Ȃǂ̕\�� �Q���҂��O�ɕ\�������
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	print qq|ڰ�:$head[$_rate]|;
}
#sub show_start_info { } # ��W���̹ްтɎQ�����Ă�����ڲ԰�ɕ\����������� _start_game_form �̏�ɕ\������� ��`���ĂȂ��Ă�����ɖ��Ȃ�
sub show_started_game { # �n�܂��Ă���ްт̕\�� �Q���҂������łȂ����� is_member �Ŕ��ʂ��؂�ւ���
	my ($m_turn, $m_value, $m_stock, @head) = @_;
	my @field_card = split /,/, $head[$_field_cards];
	my $field_card_num = @field_card;
	print qq|<br>��D�F$field_card_num��|;
	&play_form($m_turn, $m_value, $m_stock, $head[$_participants], $head[$_field_cards]) if &is_member($head[$_participants], "$m{name}"); # �ްтɎQ�����Ă���
	&show_members_hand($head[$_participants_datas]);
}

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
	&_participate($rates[$in{rate}], '', '');
}

#================================================
# �J�n���鏈�� ���ۂ̃t�@�C������� _casino_funcs.cgi _start_game
#================================================
sub start_game {
	my ($fh, $head_line, $ref_members, $ref_game_members) = @_;
	my @head = split /<>/, $$head_line; # ͯ�ް
	my @participants = split /,/, $head[$_participants];
	my $is_start = 0;
	# ���ɖ��̏���
	my @cards;

	if ($min_entry <= @participants && @participants <= $max_entry && !$head[$_state] && &is_member($head[$_participants], "$m{name}") && $m{c_turn} == 1) { # �Q���҂��K�v�\���A�ްъJ�n�O�Ȃ�
		($is_start, $head[$_state], $head[$_lastupdate], $head[$_turn], $head[$_field_cards]) = (1, 1, $time, 0, '');
		$$head_line = &h_to_s(@head);
		# ���ɖ��̏���
		my $deck_n = @participants < 8 ? 1 : 2; # 8�l�ȏォ���ޯ�2��
		my @deck = &shuffled_deck($deck_n);
		my $i = 0;
		while (@deck) {
			push @{$cards[$i]}, shift @deck;
			$i = $#participants <= $i ? 0 : $i + 1;
		}
	}
	my $c = 0;
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_start && &is_member($head[$_participants], "$mname")) {
			# ���ɖ��̏���
			@{$cards[$c]} = sort { $a <=> $b } @{$cards[$c]};
			($mtime, $mturn, $mvalue, $mstock) = ($time, 2, '', join(",", @{$cards[$c]}));
			$c++;

			push @$ref_game_members, $mname;
		}
		push @$ref_members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}
}

#================================================
# ��ڲ��̫�� ��{���ɖ��ɊہX����������K�v������
#================================================
sub play_form {
	my ($m_turn, $m_value, $m_stock, $participants, $field_cards) = @_;
	my @hand_cards = split /,/, $m_stock;
	my @participants = &get_members($participants);

	my @cards = ();
	if ($participants[0] eq $m{name}) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		for my $hand_card (@hand_cards) {
			my ($num, $suit) = &get_card($hand_card);
			push @cards, "$suits[$suit]$nums[$num]";
		}
		print "��D�F".@hand_cards."�� ".&create_select_menu("card", 0, @cards);
		print &create_submit("play", "���ނ��o��");
		print qq|</form>|;
	}
	else {
		print qq|<br>$participants[0]���v�l���ł�<br>|;
		for my $hand_card (@hand_cards) {
			my ($num, $suit) = &get_card($hand_card);
			push @cards, "$suits[$suit]$nums[$num]";
		}
		print "��D�F".@hand_cards."�� ".&create_select_menu("card", 0, @cards);
		print "<br>";
	}

	if ($field_cards && $participants[-1] ne $m{name}) {
		print qq|<form method="$method" action="$this_script" name="form">|;
		print &create_submit("doubt", "�޳�");
		print qq|</form>|;
	}
}

#================================================
# ��ڲ�̏���
#================================================
sub play {
	my @members = ();
	my $result_mes = '';
	my $winner = '';
	my @lose_members = ();
	my $penalty_coin = 0;

	# ���ɖ��̏���
	my $play_card;

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ͯ�ް
	my @participants = split /,/, $head[$_participants];
	my $is_my_turn = $head[$_state] && &is_my_turn($head[$_participants], $m{name}) && 2 <= $m{c_turn}; # �J�n���Ă���ްтɎQ�����Ă��Ď��������
	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_my_turn && $mname eq $m{name}) {
			$head[$_lastupdate] = $time;
			$mtime = $time;

			# ���ɖ��̏���
			my @hand_cards = split /,/, $mstock;
			$play_card = splice(@hand_cards, $in{card}, 1);
			$head[$_field_cards] .= "$play_card,";
			my $num = $head[$_turn] % 13;
			$head[$_turn]++;
			$result_mes = "$nums[$num]�̶��ނ��o���܂���";
			$mstock = join(",", @hand_cards);
			unless ($mstock) {
				$winner = $mname;
				@lose_members = &get_members($head[$_participants]);
				$penalty_coin = $rate;
				$result_mes .= "<br>��D���Ȃ��Ȃ���$mname�̏����ł�";
				&init_header(\@head);
				&reset_members(\@members);
			}
			else {
				$head[$_participants] = &change_turn($head[$_participants]); # ��ݏI�� 1��݂ŕ�����s������悤�ȹްтȂ���ı�Ă��A�ŏI�I�ȍs���Ŏ��s
			}
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	unshift @members, &h_to_s(@head); # ͯ�ް
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	if ($winner) {
		my $cv = 0;
		for my $loser (@lose_members) {
			if ($loser ne $winner) {
				&regist_you_data($loser, 'c_turn', '0');
				$cv += -1 * &coin_move(-1 * $penalty_coin, $loser);
			}
		}
		&coin_move($cv, $winner);
		$m{c_turn} = 0;
		&write_user;
	}

	return $result_mes; # ��ڲ�̕�
}

sub doubt {
	my @members = ();
	my $result_mes = '';

	# ���ɖ��̏���
	my $play_card;
	my $is_doubt = 0;
	my $target_player;

	open my $fh, "+< ${this_file}_member.cgi" or &error('���ް̧�ق��J���܂���'); 
	eval { flock $fh, 2; };
	my $head_line = <$fh>;
	my @head = split /<>/, $head_line; # ͯ�ް
	my @participants = &get_members($head[$_participants]); # id�ƺ�ς̕�����𖼑O�̔z��ɕϊ�
	my @field_cards = split /,/, $head[$_field_cards];
	if (@field_cards) {
		$is_doubt = 1;
		$head[$_field_cards] = '';
		my $card_num = $nums[($head[$_turn] - 1) % 13];
		my @top_card = &get_card($field_cards[-1]);

		if ($card_num eq $nums[$top_card[0]]) {
			$result_mes = "DOUBT���s�I";
			$target_player = $m{name};
		}
		else {
			$result_mes = "DOUBT�����I";
			$target_player = $participants[-1];
		}
		$result_mes .= " $participants[-1]�̏o�������ނ�$suits[$top_card[1]]��$nums[$top_card[0]]�ł�";
	}

	while (my $line = <$fh>) {
		my ($mtime, $mname, $maddr, $mturn, $mvalue, $mstock) = split /<>/, $line;
		if ($is_doubt && $mname eq $target_player) {
			my @hand_cards = split /,/, $mstock;
			push @hand_cards, @field_cards;
			@hand_cards = sort { $a <=> $b } @hand_cards;
			$mstock = join(",", @hand_cards);
		}
		push @members, "$mtime<>$mname<>$maddr<>$mturn<>$mvalue<>$mstock<>\n";
	}

	unshift @members, &h_to_s(@head);
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	return $result_mes;
}

sub show_members_hand {
	my $participants_datas = shift;

	my @participants_datas = split /;/, $participants_datas;
	for my $i (0 .. $#participants_datas) {
		my @datas = split /:/, $participants_datas[$i];
		my @hand_cards = split /,/, $datas[2];
#		my $name = pack 'H*', $datas[0];
		my $size = @hand_cards;
		print "$datas[0]�F$size�� ";
		print "<br>" if ($i+1) % 4 == 0;
	}
}

sub shuffled_deck {
	my $deck_n = shift; # �ޯ���
	my $size = $deck_n * 52 - 1; # ���ޖ���
	my @deck;

	@deck[$_] = $_+1 for (0 .. $size);
	for my $i (0 .. $size) {
		my $j = int(rand($i + 1)); # ���񂷂�x�ɗ����͈͂��L����
		my $temp = $deck[$i];
		$deck[$i] = $deck[$j];
		$deck[$j] = $temp;
	}
	return @deck;
}

sub get_card {
	my $card = shift;
	my $num = ($card-1) % 13; # 1�`52 �̒l���� -1 �������̂� 13 �Ŋ������]�肪 0�`12 �ɂȂ�
	my $suit = int(($card-1)/13); # 0��߰�� 1ʰ� 2���� 3�޲�
	return ($num, $suit);
}

1;#�폜�s��