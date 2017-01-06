#================================================
# ����ر�
#================================================

# ����ر�Ӱ�ނ̊J�n
sub start_tutorial {
	$m{tutorial_switch} = 1;
	&read_tutorial;
}

# ����ر�Ӱ�ނ̏I��
sub stop_tutorial {
	$m{tutorial_switch} = 0;
}

# Ҳ݉�ʂɕ\�������ү����
sub show_tutorial_message {
	my $message = shift;
	$mes .= qq|<hr><font color="#99CCCC">$message</font><br>|;
}

# ���ĒB�����ɕ\�������ү����
sub success_quest_mes {
	my $message = shift;
	$tutorial_mes .= qq|<hr><font color="#99CCCC">$message</font><br>|;
}

# ���ĒB������
sub success_quest_result {
	my $k = shift;
	unless ( ($tutorial_quests{$k}[3] eq 'egg_c' && $m{egg} eq '0') || ($tutorial_quests{$k}[3] eq 'wea_lv' && (!$m{wea} || $m{wea_lv} >= 30)) ) {
		$m{$tutorial_quests{$k}[3]} += $tutorial_quests{$k}[2];
	}

	if ($tutorial_quests{$k}[3] eq 'egg_c') {
		return " $tutorial_quests{$k}[2] �̛z���l��Ⴂ�܂���";
	}
	elsif ($tutorial_quests{$k}[3] eq 'wea_lv') {
		return "�����b���Ă��炢�܂���";
	}
	elsif ($tutorial_quests{$k}[3] eq 'money') {
		return " $tutorial_quests{$k}[2] G���͂��܂���";
	}
	elsif ($tutorial_quests{$k}[3] eq 'coin') {
		return " $tutorial_quests{$k}[2] ��ݖႢ�܂���";
	}
	elsif ($tutorial_quests{$k}[3] eq 'rank_exp') {
		return " $tutorial_quests{$k}[2] �̍v���l��Ⴂ�܂���";
	}
	elsif ($tutorial_quests{$k}[3] eq 'medal') {
		return " $tutorial_quests{$k}[2] �̌M�͂������܂���";
	}
}

# �����ް�
%tutorial_quests = (
	#key								=>	[[0]No,	[1]��,	[2]��V����,																					[3]���ĕ�,									[4]��V,			[5]������
#	tutorial_to_country_1		=>	[0,		1,			sub{ my $i = 25; $m{egg_c} += $i if $m{egg}; return " $i �̛z���l��Ⴂ�܂���"; },		'��ް���ނ��獑�֎d�����Ă݂悤',	'�z���l+25',	'���ɏ������邱�Ƃŋ������Ⴆ���蓝���ɎQ��������ł��܂�'],
	tutorial_bbsc_write_1		=>	[0,		1,			25 ,		'egg_c',		'����݈ȊO�̍���c���ň��A���Ă݂悤',	'�z���l+25',		'�����������G�k�����莿��ł��܂�'],
	tutorial_junk_shop_wea_1	=>	[1,		1,			3000,		'money',		'�ެݸ����߂ŕ���𔃂��Ă݂悤',			'����+3000',		'��������Ɛ퓬�E�푈���̍U���͂��オ��܂�'],
	tutorial_junk_shop_gua_1	=>	[2,		1,			3000,		'money',		'�ެݸ����߂Ŗh��𔃂��Ă݂悤',			'����+3000',		'��������Ɛ퓬���̖h��͂��オ��A������ʂ��t���܂�'],
	tutorial_junk_shop_sell_1	=>	[3,		1,			3000,		'money',		'�ެݸ����߂ɉ����𔄂��Ă݂悤',			'����+3000',		'���������̂ͼެݸ����߂ɕ��сA�N���������Ă���܂�'],
	tutorial_5000_gacha_1		=>	[4,		1,			5,			'rank_exp',	'5000�������񂵂Ă݂悤',						'�v���l+5',			'24���Ԃ�1��񂹂�̂Ŗ����񂵂܂��傤'],
	tutorial_bank_1				=>	[5,		1,			10,		'coin',		'��s�ɂ�����a���Ă݂悤',					'���+10',			'���N���q���Ⴆ����A�����ŕ����Ă����S�ł�'],
	tutorial_hunting_1			=>	[6,		1,			10,		'coin',		'���������Ă݂悤',				'���+10',			'�����ł͂������Ⴆ�A�����E�����肷�邱�Ƃ�����܂�'],
	tutorial_highlow_1			=>	[7,		1,			1,			'wea_lv',	'���ɂ�ʲ۳�����Ă݂悤',						'��������+1',		'���߂���݂͖𗧂±��тƌ����ł��܂�'],
	tutorial_training_1			=>	[8,		1,			5000,		'money',		'�C�s�����Ă݂悤',								'����+5000',		'�Ԃ�����Ɛ키�ƋZ��M���₷���ł�'],
	tutorial_hospital_1			=>	[9,		1,			10000,	'money',		'���\���a�@�Ŏ������ĖႨ��',					'������+10000',	'HP�EMP�̎����񕜂�҂ĂȂ��ꍇ�͕a�@�ŉ񕜂ł��܂�'],
	tutorial_breeder_1			=>	[10,		1,			20,		'coin',		'��ĉ��ɗ���a���Ă݂悤',					'���+20',			'�a��������10�����ɛz���l�� +1 ����܂�'],
	tutorial_full_act_1			=>	[11,		1,			25,		'egg_c',		'��J�x�� 100 %�ȏ�ɂ��Ă݂悤',			'�z���l+25',		'��J�� 100 %�𒴂���Ɠ����ȊO�̍s������������܂�'],
	tutorial_dom_1					=>	[12,		1,			10000,	'money',		'���������Ă݂悤',								'������+10000',	'���܂�����J���񕜂������𑝂₷���Ƃ��ł��܂�'],
	tutorial_mil_1					=>	[13,		1,			5,			'rank_exp',	'�D�R�������Ă݂悤',							'�v���l+5',			'������D�����ƂœG����W�Q���Ȃ��畨���𑝂₹�܂�'],
	tutorial_gikei_1				=>	[14,		1,			10,		'coin',		'�U�v�����Ă݂悤',								'���+10',			'�G���̓����𖳌��ɂ�����A��킳���₷���Ȃ�܂�'],
	tutorial_promise1_1			=>	[15,		1,			10000,	'money',		'�F�D��������ł݂悤',						'������+10000',	'�������ێ�������A����h�����Ƃ��ł��܂�'],
	tutorial_mil_ambush_1		=>	[16,		1,			10,		'coin',		'�R���҂����������Ă݂悤',					'���+10',			'���ʂ����������̂ŐQ��O�ȂǂɎd�|���Ă����܂��傤'],
	tutorial_promise2_1			=>	[17,		1,			30000,	'money',		'����������ł݂悤',						'������+30000',	'����Ԃ��������邱�Ƃň���I�ɍU�߂���Ƃ����󋵂�h���܂�'],
	tutorial_ceo_1					=>	[18,		1,			1,			'medal',		'�N��ɗ���₵�Ă݂悤',						'�M��+1',			'�N��ɂȂ�Ɛ�p����ނ�������ꂽ��A�e��s���ɕ␳���t���܂�'],
	tutorial_job_change_1		=>	[19,		1,			20000,	'money',		'<a href="http://www43.atwiki.jp/bjkurobutasaba/pages/695.html">�E��</a>��ς��Ă݂悤',			'������+20000',		'�R�t��x��q����ʓI�Ȃ悤�ł�'],
	tutorial_lv_20_1				=>	[20,		1,			30000,	'money',		'���ق� 20 �ɂ��悤',							'������+30000',	'Lv.20�ɂȂ�ƌ����ł���悤�ɂȂ�܂�'],
	tutorial_mariage_1			=>	[21,		1,			30,		'coin',		'�������k���ɓo�^���Ă݂悤',					'�v���l+30',		'��������Ɠ]�����̃X�e������}������A����̋Z���K���ł��܂�'],
);

# ����ߐ�
# �����ް��Ɋ܂߂�Ƹ��Đ����ϓ��������ɏ��������Ȃ��Ƃ����番���Ď�����
$tutorial_quest_stamps = keys(%tutorial_quests);

# ������ް�
@tutorial_stamps = (
	#[0]No,	[1]��,	[2]��V����,																							[3]��V
	[0,		3,			sub{ &send_item($m{name}, 2, 51, 0, 0, 1); return "�޷�Ű���ނ�Ⴂ�܂���"; },	'�޷�Ű����'],
	[1,		6,			sub{ my $i = 5000; $m{money} += $i; return " $i G���͂��܂���"; },					'����+5000'],
	[2,		9,			sub{ &send_item($m{name}, 2, 25, 0, 0, 1); return "�ؽ�ٴ��ނ�Ⴂ�܂���"; },		'�ؽ�ٴ���'],
	[3,		12,		sub{ &send_item($m{name}, 2, 1, 0, 0, 1); return "����Ѵ��ނ�Ⴂ�܂���"; },		'����Ѵ���'],
	[4,		16,		sub{ my $i = 10000; $m{coin} += $i; return " $i ��ݖႢ�܂���"; },					'���+10000'],
	[5,		19,		sub{ &send_item($m{name}, 2, 19, 0, 0, 1); return "���߰���ނ�Ⴂ�܂���"; },		'���߰����'],
	[6,		22,		sub{ &send_item($m{name}, 2, 33, 0, 0, 1); return "����ݴ��ނ�Ⴂ�܂���"; },		'����ݴ���'],
);

=pod
# ���ĒB���Ɋւ���s���̐������ɌĂяo���Ɣ����B�������Ȃǂ�����Ă����
# �����ɂ͸��ķ���z��œn��
sub run_tutorial_quest {
	my @ks = @_;

	for my $k (@ks) {
		++$m{$k};
		if ($m{$k} eq $tutorial_quests{$k}[1]) {
			my $str = "��V�Ƃ���" . &{$tutorial_quests{$k}[2]};
			&success_quest_mes("���āu$tutorial_quests{$k}[3]�v��B�����܂����I<br>$str<br><br>$tutorial_quests{$k}[5]");
			++$m{tutorial_quest_stamp_c};
		}
	}

	# ����ߺ���ذ�
	if ($m{tutorial_quest_stamp_c} eq $tutorial_quest_stamps) {
		&success_quest_mes("���ׂĂ̽���߂��W�߂܂����I");
	}
}
=cut

# հ�ް������ر��ް��̓ǂݍ���
sub read_tutorial {
	&write_tutorial unless -f "$userdir/$id/tutorial.cgi"; # ������

	open my $fh, "< $userdir/$id/tutorial.cgi" or &error("���̂悤�Ȗ��O$in{login_name}����ڲ԰�����݂��܂���");
	my $line = <$fh>;
	close $fh;

	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$m{$k} = $v; # $s
	}
}

# հ�ް������ر��ް��̏�������
sub write_tutorial {
	my $line = "tutorial_quest_stamp_c;$m{tutorial_quest_stamp_c}<>"; # ����߂͸����ް��ɓ����ĂȂ��̂ŗ\�ߒ�`

	foreach my $k (keys(%tutorial_quests)) {
		$line .= "$k;$m{$k}<>";
	}

	open my $fh, "> $userdir/$id/tutorial.cgi";
	print $fh "$line\n";
	close $fh;
}

# ���Ă̒B����Ԃ̕\��
sub show_stamps {
	&read_tutorial unless $m{tutorial_switch}; # ����ر�Ӱ�ސ؂��ĂĂ����ߒ��͌����悤��

	$layout = 2;
	my $comp_par = int($m{tutorial_quest_stamp_c} / $tutorial_quest_stamps * 100);
	$mes .= "����ߒ� �s���ߗ� $comp_par%�t<br>";

 	$mes .= $is_mobile ? '<hr>�ԍ� / �B�� / ���� / ��V'
 		:qq|<table class="table1" cellpadding="3"><tr><th>�ԍ�</th><th>�B��</th><th>����</th><th>��V</th></tr>|;

	my @list = (); # �����ް���ʯ���ŏ��s���Ȃ��߁A�\���p�ɿ�Ă���
	$#list = $tutorial_quest_stamps - 1;
	foreach my $k (keys(%tutorial_quests)) {
		my ($no, $result, $quest, $str, $sub_str) = ($tutorial_quests{$k}[0]+1, '', '', '', '');
		if ($m{$k} >= $tutorial_quests{$k}[1]) {
			$result = '��';
			$quest = "<s>$tutorial_quests{$k}[4]</s>";
			$sub_str = $is_mobile ? "<br>$tutorial_quests{$k}[6]"
				: qq|<tr><td colspan="4">$tutorial_quests{$k}[6]</td></tr>|;
		}
		else {
			$result = '�~';
			$quest = "$tutorial_quests{$k}[4]";
		}
	 	$str = $is_mobile ? qq|<hr>$no / $result / $quest / $tutorial_quests{$k}[5]|
	 		: qq|<tr><td align="right">$no</td><td align="center">$result</td><td>$quest</td><td>$tutorial_quests{$k}[5]</td></tr>|;
		splice(@list, $tutorial_quests{$k}[0], 1, $str.$sub_str);
	}

	for my $i (0 .. $#list) {
		$mes .= "$list[$i]";
	}

 	$mes .= qq|</table>| unless $is_mobile;

	$mes .= "<p>����ߕ�V</p>";
 	$mes .= $is_mobile ? '<hr>�ԍ� / �B�� / ����ߐ� / ��V'
 		:qq|<table class="table1" cellpadding="3"><tr><th>�ԍ�</th><th>�B��</th><th>����ߐ�</th><th>��V</th></tr>|;

	my $no = 0;
	if ($is_mobile) {
		for my $i (0 .. $#tutorial_stamps) {
			++$no;
			my $result = '';
			$result = $m{tutorial_quest_stamp_c} >= $tutorial_stamps[$i][1] ? '��' : '�~';
		 	$mes .= "<hr>$result / $tutorial_stamps[$i][1] / $tutorial_stamps[$i][3]";
		}
	}
	else {
		for my $i (0 .. $#tutorial_stamps) {
			++$no;
			my $result = '';
			$result = $m{tutorial_quest_stamp_c} >= $tutorial_stamps[$i][1] ? '��' : '�~';
		 	$mes .= qq|<tr><td align="right">$no</td><td align="center">$result</td><td align="right">$tutorial_stamps[$i][1]</td><td>$tutorial_stamps[$i][3]</td></tr>|;
		}
	}

 	$mes .= qq|</table>| unless $is_mobile;
}

# ���B���ȏ��Ղ̸��Ă�\��
sub show_quest {
	my $str = '';
	my $min = $tutorial_quest_stamps;
	foreach my $k (keys(%tutorial_quests)) {
		if ($m{$k} < $tutorial_quests{$k}[1] && $tutorial_quests{$k}[0] < $min) {
			$min = $tutorial_quests{$k}[0];
			$str = $tutorial_quests{$k}[4];
		}
	}

	return $str;
}

1; # �폜�s��
