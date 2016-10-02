my $this_file = "$logdir/junk_shop.cgi";
#================================================
# �ެݸ����� Created by Merino
#=================================================

# �����Ȃ��Ƃ��̔���(����)
my @wea_nos = (1,6,11,16,21,26);
my @gua_nos = (1..15,18,21);

# ���������Ϻ�
my @gacha_eggs = (
	# �l�i,		�Ϻ�No
	# ʽ�ڴ���(2/11) �ݽ������(4/11) �޷�Ű����(3/11) ����Ѵ���(1/11) ����è����(1/11)
	[5000,	[42,42,43,43,43,43,51,51,51,1,4],		],
	# ʽ�ڴ���(5/22) �ݽ������(2/22) ����Ѵ���(1/22) ����è����(1/22)
	# ����޴���(1/22) Ѱݴ���(1/22) ̧�������(1/22) ���������(1/22) �ذ����(1/22)
	# ���ް����(1/22) �������(1/22) �ް�����(1/22) ײĴ���(1/22)
	# ����Ŵ���(1/22) ���ް����(1/22) ����ݴ���(1/22) �������(1/22)
	[20000,	[42,42,42,42,42,43,43,1,4..15,33,50],	],
	# ʽ�ڴ���(1/29) �ݽ������(1/29) ����Ѵ���(1/29) ��ذѴ���(1/29) ����è����(1/29)
	# ����޴���(1/29) Ѱݴ���(1/29) ̧�������(1/29) ���������(1/29) �ذ����(1/29)
	# ���ް����(1/29) �������(1/29) �ް�����(1/29) ײĴ���(1/29)
	# ����Ŵ���(1/29) ���ް����(1/29) ��ٴ���(1/29) ���è����(1/29)
	# ��ٴ���(1/29) ���߰����(1/29) ڲ��ް����(1/29) ڼު��޴���(1/29)
	# ���ޯĴ���(1/29) ϼޯ�����(1/29) ��ׯ�޴���(1/29) ����ݴ���(3/29) �������(1/29)
	[50000,	[42,43,1,3..24,33,33,33,50],			],
);

my @gacha_eggs2 = (
	# �l�i,		�Ϻ�No,percent
	[150000,	[[42,17], # ʽ�ڴ��� 17/100
			[52,19], # ������ 19/100
		 	[21,7], # ڼު��޴��� 7/100
			[3,29], # ��ذѴ��� 29/100
			[36,4], # ��׺�ݴ��� 4/100
			[53,11], # ȵʽ�ڴ��� 11/100
			[55,13],],		], # ����״��� 13/100
);

#	[150000,	[[42,20], # ʽ�ڴ��� 20/100
#			[52,20], # ������ 20/100
#			[16,15], # ��ٴ��� 15/100
#			[3,10], # ��ذѴ��� 10/100
#			[36,4], # ��׺�ݴ��� 4/100
#			[53,15], # ȵʽ�ڴ��� 15/100
#			[55,16],],		], # ����״��� 16/100

# ���������Ϻނ��ł���Ԋu(�b)
my $gacha_time = 24 * 60 * 60;
my $gacha_time2 = 6 * 60 * 60;

# �����l�i
my $buy_price  = 500;

# ����l�i
my $sall_price = 100;


#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ�����?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�ެݸ����߂łȂ�ł������Ȃ�ł�����<br>';
		$mes .= '���O������?<br>';
	}
	
	&menu('��߂�','����','����', '������','���z������');
}

sub tp_1 {
	return if &is_ng_cmd(1..4);
	$m{tp} = $cmd * 100;
	
	if ($cmd eq '1') {
		$mes .= "�~�����̂�����?<br>������ӂ̂��� $buy_price G�ł�����<br>";
		&menu('��߂�','����');
	}
	elsif ($cmd eq '2') {
		$mes .= "���𔄂Ă���� $sall_price G�Ŕ������<br>";
		my @menus = ('��߂�');
		push @menus, $m{wea} ? $weas[$m{wea}][1] : '';
		push @menus, $m{egg} ? $eggs[$m{egg}][1] : '';
		push @menus, $m{pet} > 0 ? "$pets[$m{pet}][1]��$m{pet_c}" : '';
		push @menus, $m{gua} ? $guas[$m{gua}][1] : '';
		&menu(@menus);
	}
	elsif ($cmd eq '3') {
		$mes .= '�^���܂��̶��������ϺށB�l�i�F�X�B�����o�邩�͂��y����<br>';
		my @menus = ('��߂�');
		for my $i (0..$#gacha_eggs) {
			push @menus, "$gacha_eggs[$i][0] G";
		}
		&menu(@menus);
	}
	elsif ($cmd eq '4') {
		$mes .= '�������د��ȶ��������ϺށB�����o�邩�͂��y����<br>';
		my @menus = ('��߂�');
		for my $i (0..$#gacha_eggs2) {
			push @menus, "$gacha_eggs2[$i][0] G";
		}
		&menu(@menus);
	}
	else {
		&begin;
	}
}

#=================================================
# ����
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);
	
	if ($m{money} < $buy_price) {
		$mes .= '���O�n�R�B����Ȃ��B�n�R�ɂȂ�����<br>';
	}
	elsif ($m{is_full}) {
		$mes .= '���O�̗a���菊���ς��B����Ȃ�<br>';
	}
	else {
		$m{money} -= $buy_price;

		if (-s $this_file) {
			my $count = 0;
			my @lines = ();
			open my $fh, "+< $this_file" or &error("$this_file ̧�ق��J���܂���");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				push @lines, $line;
				last if ++$count > 50;
			}
			my $get_line = int(rand(2)) == 0 ? shift @lines : pop @lines;
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
			
			my($kind, $item_no, $item_c) = split /<>/, $get_line;
			
			open my $fh3, ">> $logdir/junk_shop_sub.cgi" or &error("$logdir/junk_shop_sub.cgi̧�ق��J���܂���");
			print $fh3 "$kind<>$item_no<>$item_c<>$m{name}<>$time<>1<>\n";
			close $fh3;
			
			&send_item($m{name}, $kind, $item_no, $item_c);
			&sale_data_log($kind, $item_no, $item_c, 0, $buy_price, 4);

			$mes .= &get_item_name($kind, $item_no); # �A�C�e��������
			$mes .= '�𔃂��܂���<br>';
			
		}
		# �����Ȃ��ꍇ�̓f�t�H���g�A�C�e��
		else {
			if(rand(2) < 1){
				my $wea_no = $wea_nos[int(rand(@wea_nos))];
				&send_item($m{name}, 1, $wea_no, $weas[$wea_no][4]);
				$mes .= "$weas[$wea_no][1]�𔃂��܂���<br>";
			}else{
				my $gua_no = $gua_nos[int(rand(@gua_nos))];
				&send_item($m{name}, 4, $gua_no, $guas[$gua_no][4]);
				$mes .= "$guas[$gua_no][1]�𔃂��܂���<br>";
			}
		}
		$mes .= "���O�����z�A�F�B�B�������͗a���菊�ɑ�����<br>";
	}
	&begin;
}

#=================================================
# ����
#=================================================
sub tp_200 {
	if (    ($cmd eq '1' && $m{wea})
		 || ($cmd eq '2' && $m{egg})
		 || ($cmd eq '3' && $m{pet} > 0)
		 || ($cmd eq '4' && $m{gua}) ) {
			my $line;
			if ($cmd eq '1') {
				if($m{wea_name}){
					$m{wea} = 32;
					$m{wea_c} = 0;
					$m{wea_lv} = 0;
					$mes .= "������̎�𗣂ꂽ�r�[$m{wea_name}�͂�����$weas[$m{wea}][1]�ɂȂ��Ă��܂���<br>";
					$m{wea_name} = "";
				}
				$mes .= "$weas[$m{wea}][1]�𔄂�܂���<br>";
				$line = "$cmd<>$m{wea}<>$m{wea_c}<>";
				$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
			}
			elsif ($cmd eq '2') {
				$mes .= "$eggs[$m{egg}][1]�𔄂�܂���<br>";
				$line = "$cmd<>$m{egg}<>$m{egg_c}<>";
				$m{egg} = $m{egg_c} = 0;
			}
			elsif ($cmd eq '3') {
				$mes .= "$pets[$m{pet}][1]��$m{pet_c}�𔄂�܂���<br>";
				$line = "$cmd<>$m{pet}<>0<>";
				&remove_pet;
			}
			elsif ($cmd eq '4') {
				$mes .= "$guas[$m{gua}][1]�𔄂�܂���<br>";
				$line = "$cmd<>$m{gua}<>0<>";
				$m{gua} = 0;
			}
			else {
				&error('���т̎�ނ��ُ�ł�');
			}
			
			$mes .= "���O�����l�A���ǂ��B�ǂ����̎��Ă� $sall_price G���<br>";
			$m{money} += $sall_price;
#			if (rand(2) < 1) {
				open my $fh, ">> $this_file" or &error("$this_filȩ�ق��J���܂���");
				print $fh "$line\n";
				close $fh;
#			}
			open my $fh3, ">> $logdir/junk_shop_sub.cgi" or &error("$logdir/junk_shop_sub.cgi̧�ق��J���܂���");
			print $fh3 "$line$m{name}<>$time<>0<>\n";
			close $fh3;
	}
	&begin;
}

#=================================================
# ������
#=================================================
sub tp_300 {
	return if &is_ng_cmd(1..$#gacha_eggs+1);
	--$cmd;
	
	if ($m{gacha_time} > $time) {
		my $g_time = $m{gacha_time} - $time;
		my $next_gacha_time = sprintf("%02d��%02d��", int($g_time / 3600), int($g_time % 3600 / 60) );
		$mes .= "�����������߂���Ƃ��O����B���� $next_gacha_time ���炢�҂�<br>";
	}
	elsif ($m{money} >= $gacha_eggs[$cmd][0]) {
		my @egg_nos = @{ $gacha_eggs[$cmd][1] };
		my $egg_no  = $egg_nos[int(rand(@egg_nos))];
		$m{money}  -= $gacha_eggs[$cmd][0];
		
		&send_item($m{name}, 2, $egg_no, 0, 0, 1);
		$mes .= "�����������߰��<br>$eggs[$egg_no][1]���o�܂���<br>";
		
		$m{gacha_time} = $time + $gacha_time;
		if (&on_summer) {
			my $v = int(rand($gacha_eggs[$cmd][0] / 1000) + 1);
			$m{pop_vote} += $v;
			$mes .= "���[����$v�����������";
		}
	}
	else {
		$mes .= '���O�n�R�B����������ҁB�n�R�ɂȂ�����<br>';
	}

	&begin;
}

sub tp_400 {
	return if &is_ng_cmd(1..$#gacha_eggs2+1);
	--$cmd;
	
	if ($m{gacha_time2} > $time) {
		my $g_time2 = $m{gacha_time2} - $time;
		my $next_gacha_time2 = sprintf("%02d��%02d��", int($g_time2 / 3600), int($g_time2 % 3600 / 60) );
		$mes .= "�����������߂���Ƃ��O����B���� $next_gacha_time2 ���炢�҂�<br>";
	}
	elsif ($m{money} >= $gacha_eggs2[$cmd][0]) {
		my @egg_list2 = ();
		for(0..$#{$gacha_eggs2[$cmd][1]}){
			for(my $i = 0;$i < $gacha_eggs2[$cmd][1][$_][1];$i++){
				push(@egg_list2,$gacha_eggs2[$cmd][1][$_][0]);
			}
		}
		my $egg_no2  = $egg_list2[int(rand(@egg_list2))];

		$m{money}  -= $gacha_eggs2[$cmd][0];
		
		&send_item($m{name}, 2, $egg_no2, 0, 0, 1);
		$mes .= "�����������߰��<br>$eggs[$egg_no2][1]���o�܂���<br>";	
		$m{gacha_time2} = $time + $gacha_time2;
		if (&on_summer) {
			my $v = int(rand(150) + 1);
			$m{pop_vote} += $v;
			$mes .= "���[����$v�����������";
		}
	}
	else {
		$mes .= '���O�n�R�B����������ҁB�n�R�ɂȂ�����<br>';
	}

	&begin;
}

1; # �폜�s��
