my $this_file = "$logdir/offertory_box.cgi";
#================================================
# �ΑK��
#=================================================

# ���ΑK��������Ԋu�i�b�j
my $offertory_time = 24 * 60 * 60;

@buu_item = (
	#���,  �ԍ�, �ϋv�l�Ȃ�, ��, ����
	[2,54,0,0,1],# ����
	[1,33,500,0,1],# л��
	[3,125,0,0,1],# Ѱ
	[3,21,0,0,1],# ����ش�
	[3,183,0,0,1],# ���
	[3,184,0,0,20],# �ݼ�10
	[3,187,0,0,5],# �������5
);

@god_item = (
	#���,  �ԍ�, �ϋv�l�Ȃ�, ��, ����
	[2,3,999,0,10],# �z����10
	[1,32,500,30,1],# ��с�30
	[3,64,0,0,5],# �޳�5
	[3,125,0,0,1],# Ѱ
	[3,127,0,0,1],# �����
	[3,17,0,0,1],# �̧�ق����
	[3,18,0,0,1],# ж��
	[3,21,0,0,1],# ����ش�
	[2,37,999,0,5],# �z���_��5
	[3,75,0,0,5],# �����Lv4 5
	[3,143,0,0,5],# ¸��5
	[3,144,0,0,5],# �����5
	[3,132,0,0,10],# ����10
	[3,164,0,0,10],# �۽10
	[2,53,0,0,10],# ��ش���10
	[3,168,0,0,1],# �߲���
	[3,183,0,0,1],# ���
	[3,184,0,0,10],# �ݼ�10
	[3,187,0,0,3],# �������3
	[3,189,0,0,10],# Ҷ���10
	[3,190,0,0,10],# ��ּ10
);
#�͂���
@bad_item = (
	[2,22,0,0,10],# ���ޯĔ���
	[2,42,0,0,10],# ʽ�ڔ���
	[3,120,0,0,10],# ϼ޽�����
	[3,121,0,0,10],# �߲��ݔ���
	[3,176,0,0,10],# �۽����
	[3,198,0,0,10],# ��ה���
);

#���E��
my $flow_anger = 10;

#����ȉ��̗����i����v�Z�j�ȏ�ɗ݌v�z��������ƃA�C�e�������炦��
#�����Ȃ̂ő傫�߂ɐݒ肷�邱��
my $flow_total = 50000000;

# ������Ɛ_�l���{�镳�A�C�e��
my %anger_items = (
	wea => [1,6,11,16,21,26,], # ����
	egg => [22,24,42,], # �Ϻ�
	pet => [120,121,], # �߯�
	gua => [], # �h��
);

# ���A�A�C�e���i�K���Ȃ̂œK�X�ǉ����Ă��������j
my %satisfy_items = (
	wea => [5,10,15,20,25,30,31,32,], # ����
	egg => [37,38,39,40,41,45,46,47,], # �Ϻ�
	pet => [3,7,8,17,18,19,20,21,48,58,59,60,63,127,150,151,183], # �߯�
	gua => [], # �h��
);

#================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ�����?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�_�l�o�Ă��邳�[����<br>';
		$mes .= '�������<br>';
	}
	
	&menu('��߂�','���ΑK������','��������������');
}

sub tp_1 {
	return if &is_ng_cmd(1..2);
	
	if ($cmd eq '1') {
		$mes .= "<br>";
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
		$mes .= qq|<input type="radio" name="cmd" value="1">���z<input type="text" name="send_money" value="0" class="text_box1" style="text-align:right">G<br>| if $m{money} > 0;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="�����" class="button1"></p></form>|;
		$m{tp} = 100;
	}
	elsif ($cmd eq '2') {
		$mes .= "<br>";
		$mes .= qq|<form method="$method" action="$script">|;
		$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
		$mes .= qq|<input type="radio" name="cmd" value="1">[$weas[$m{wea}][2]]$weas[$m{wea}][1]��$m{wea_lv}($m{wea_c}/$weas[$m{wea}][4])<br>| if $m{wea};
		$mes .= qq|<input type="radio" name="cmd" value="2">[��]$eggs[$m{egg}][1]($m{egg_c}/$eggs[$m{egg}][2])<br>| if $m{egg};
		$mes .= qq|<input type="radio" name="cmd" value="3">[�y]$pets[$m{pet}][1]��$m{pet_c}<br>| if $m{pet};
		$mes .= qq|<input type="radio" name="cmd" value="4">[$guas[$m{gua}][2]]$guas[$m{gua}][1]<br>| if $m{gua};
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<p><input type="submit" value="����������" class="button1"></p></form>|;
		$m{tp} = 200;
	}
	else {
		&begin;
	}
}

#=================================================
# �ΑK������
#=================================================
sub tp_100 {
	return if &is_ng_cmd(1);
	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�͂܂����ꂢ�Ȑg�ɂȂ�<br>";
		&begin;
		return;
	}

	if ($m{offertory_time} > $time) {
		my $o_time = $m{offertory_time} - $time;
		my $next_offertory_time = sprintf("%02d��%02d��", int($o_time / 3600), int($o_time % 3600 / 60) );
		$mes .= "���Q�������ł����B���� $next_offertory_time �҂�<br>";
		&begin;
		return;
	}
	if ($cmd eq '1' && $in{send_money} > 0 && $in{send_money} !~ /[^0-9]/) {
		if ($m{money} >= $in{send_money}) {
			$m{offertory_time} = $time + $offertory_time;
			my $all_money = $m{money};
			$m{money} -= $in{send_money};
			if ($m{bank} ne '') {
				my $shop_id = unpack 'H*', $m{bank};
				my $save_money = 0;

				if( -f "$userdir/$shop_id/shop_bank.cgi"){
					open my $fh, "< $userdir/$shop_id/shop_bank.cgi" or &error("$userdir/$shop_id/shop_bank.cgi̧�ق��J���܂���");
					my $head_line = <$fh>;
					while (my $line = <$fh>) {
						my($year, $name, $money) = split /<>/, $line;
						if ($m{name} eq $name) {
							$save_money = $money;
							last;
						}
					}
					close $fh;
					$all_money += $save_money;
				}
			}
			my $total;
			my $anger;

			my @lines = ();
			if(-s $this_file){
				open my $ofh, "< $this_file" or &error("$this_file ̧�ق��J���܂���");
				while (my $line = <$ofh>) {
					push @lines, $line;
				}
				close $ofh;
				my $get_line = shift @lines;
				($total, $anger) = split /<>/, $get_line;
			}else {
				$total = 0;
				$anger = 0;
			}
			$total += $in{send_money};

			if($in{send_money} == $all_money){
				$total += 1000000;
			}
			if($total > int(rand($flow_total))){
				$total -= 2000000;
				$total = 0 if $total < 0;
				if (rand(10) < 1) {
					&get_god_item(7);

					$mes .= "���ؐ_<�ԁ[<br>";
					&mes_and_world_news("���ؐ_�l����A�C�e�������炢�܂���", 1);
					&send_twitter("���ؐ_�l����A�C�e�������炢�܂���", 1);
				} else {
					&get_god_item(5);

					$mes .= "�ڂ��͂����̐_�l����<br>";
					$mes .= "���������Q�肠�肪�Ƃ��B<br>";
					$mes .= "����ɃA�C�e���������<br>";
					&mes_and_world_news("�_�l����A�C�e�������炢�܂���", 1);
					&send_twitter("�_�l����A�C�e�������炢�܂���", 1);
				}
			}
			unshift @lines, "$total<>$anger";

			open my $wfh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
			print $wfh @lines;
			close $wfh;
			
			&log_errors("$in{send_money} / $all_money offertory by $m{name}");
		}
		else {
			$mes .= "����������܂���<br>";
		}
	}
	&begin;	
}

#=================================================
# ��������������
#=================================================
sub tp_200 {
	return if &is_ng_cmd(1..4);
	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�͂܂����ꂢ�Ȑg�ɂȂ�<br>";
		&begin;
		return;
	}

	if ($m{offertory_time} > $time) {
		my $o_time = $m{offertory_time} - $time;
		my $next_offertory_time = sprintf("%02d��%02d��", int($o_time / 3600), int($o_time % 3600 / 60) );
		$mes .= "���Q�������ł����B���� $next_offertory_time �҂�<br>";
		&begin;
		return;
	}
	if (($cmd eq '1' && $m{wea}) || ($cmd eq '2' && $m{egg}) || ($cmd eq '3' && $m{pet}) || ($cmd eq '4' && $m{gua})) {
		$m{offertory_time} = $time + $offertory_time;
		my $total;
		my $add_total = 20000;
		my $anger;
		my $is_anger = 0;
		my $is_satisfy = 0;
		my @kinds = ('', 'wea', 'egg', 'pet', 'gua');
		for my $anger_item (@{ $anger_items{ $kinds[$cmd] } }) {
			if ($anger_item eq $m{ $kinds[$cmd] }) {
				$is_anger = 1;
				$add_total = 10000;
			}
		}
		for my $satisfy_item (@{ $satisfy_items{ $kinds[$cmd] } }) {
			if ($satisfy_item eq $m{ $kinds[$cmd] }) {
				$is_satisfy = 1;
				$add_total = 100000;
			}
		}
		my @lines = ();
		if(-s $this_file){
			open my $ofh, "< $this_file" or &error("$this_file ̧�ق��J���܂���");
			while (my $line = <$ofh>) {
				push @lines, $line;
			}
			close $ofh;
			my $get_line = shift @lines;
			($total, $anger) = split /<>/, $get_line;
		}else {
			$total = 0;
			$anger = 0;
		}
		$total += $add_total;

		if($is_anger){
			$anger++;
			if($anger > $flow_anger){
				$anger = 0;
				if (rand(300) < 1) {
					&get_god_item(7);

					$mes .= "���ؐ_<�ԁ[<br>";
					&mes_and_world_news("���ؐ_�l����A�C�e�������炢�܂���", 1);
					&send_twitter("���ؐ_�l����A�C�e�������炢�܂���", 1);
				} else {
					&get_god_item(0);

					$mes .= "�ڂ��͂����̐_�l����I<br>";
					$mes .= "���������Q�肠�肪�Ƃ��I<br>";
					$mes .= "����ɃA�C�e��������ˁI<br>";
					&mes_and_world_news("�_�l����A�C�e�������炢�܂����H", 1);
					&send_twitter("�_�l����A�C�e�������炢�܂����H", 1);
				}
			}
		}elsif($is_satisfy){
			if($total * 2 > int(rand($flow_total))){
				$total -= 2000000;
				$total = 0 if $total < 0;
				
				if (rand(2) < 1) {
					&get_god_item(7);

					$mes .= "���ؐ_<�ԁ[<br>";
					&mes_and_world_news("���ؐ_�l����A�C�e�������炢�܂���", 1);
					&send_twitter("���ؐ_�l����A�C�e�������炢�܂���", 1);
				} else {
					&get_god_item(6);

					$mes .= "�ڂ��͂����̐_�l����<br>";
					$mes .= "���������Q�肠�肪�Ƃ��B<br>";
					$mes .= "����ɃA�C�e���������<br>";
					&mes_and_world_news("�_�l����A�C�e�������炢�܂���", 1);
					&send_twitter("�_�l����A�C�e�������炢�܂���", 1);
				}
			}
		}else{
			if($total > int(rand($flow_total))){
				$total -= 2000000;
				$total = 0 if $total < 0;
				
				if (rand(20) < 1) {
					&get_god_item(7);

					$mes .= "���ؐ_<�ԁ[<br>";
					&mes_and_world_news("���ؐ_�l����A�C�e�������炢�܂���", 1);
					&send_twitter("���ؐ_�l����A�C�e�������炢�܂���", 1);
				} else {
					&get_god_item(4);

					$mes .= "�ڂ��͂����̐_�l����<br>";
					$mes .= "���������Q�肠�肪�Ƃ��B<br>";
					$mes .= "����ɃA�C�e���������<br>";
					&mes_and_world_news("�_�l����A�C�e�������炢�܂���", 1);
					&send_twitter("�_�l����A�C�e�������炢�܂���", 1);
				}
			}
		}
		unshift @lines, "$total<>$anger";

		open my $wfh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
		print $wfh @lines;
		close $wfh;
	}	
	if ($cmd eq '1' && $m{wea}) {
		&sale_data_log(1, $m{wea}, $m{wea_c}, $m{wea_lv}, 500, 5);
		if($m{wea_name}){
			$mes .= "$m{wea_name}��_�ɕԂ��܂���";
			$m{wea_name} = "";
			&get_god_item(4);
		}
		$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
	}
	elsif ($cmd eq '2' && $m{egg}) {
		&sale_data_log(2, $m{egg}, $m{egg_c}, 0, 500, 5);
		$m{egg} = $m{egg_c} = 0;
	}
	elsif ($cmd eq '3' && $m{pet}) {
		&sale_data_log(3, $m{pet}, $m{pet_c}, 0, 500, 5);
		$m{pet} = 0;
	}
	elsif ($cmd eq '4' && $m{gua}) {
		&sale_data_log(4, $m{gua}, 0, 0, 500, 5);
		$m{gua} = 0;
	}
	&begin;	
}

sub get_god_item {
	my $type = shift;
	if ($type >= 7 && rand(3) < 1) {
		my $item_no = int(rand($#buu_item + 1));
		&send_item($m{name},$buu_item[$item_no][0],$buu_item[$item_no][1],$buu_item[$item_no][2],$buu_item[$item_no][3],1) for 1 .. $buu_item[$item_no][4];
	} elsif (rand(7) < $type) {
		my $item_no = int(rand($#god_item + 1));
		&send_item($m{name},$god_item[$item_no][0],$god_item[$item_no][1],$god_item[$item_no][2],$god_item[$item_no][3],1) for 1 .. $god_item[$item_no][4];
	} else {
		my $item_no = int(rand($#bad_item + 1));
		&send_item($m{name},$bad_item[$item_no][0],$bad_item[$item_no][1],$bad_item[$item_no][2],$bad_item[$item_no][3],1) for 1 .. $bad_item[$item_no][4];		
	}

}

sub send_god_item {
	my ($type, $send_name) = @_;
	if ($type >= 7 && rand(3) < 1) {
		my $item_no = int(rand($#buu_item + 1));
		&send_item($send_name,$buu_item[$item_no][0],$buu_item[$item_no][1],$buu_item[$item_no][2],$buu_item[$item_no][3],1) for 1 .. $buu_item[$item_no][4];
	} elsif (rand(7) < $type) {
		my $item_no = int(rand($#god_item + 1));
		&send_item($send_name,$god_item[$item_no][0],$god_item[$item_no][1],$god_item[$item_no][2],$god_item[$item_no][3],1) for 1 .. $god_item[$item_no][4];
	}else {
		my $item_no = int(rand($#bad_item + 1));
		&send_item($send_name,$bad_item[$item_no][0],$bad_item[$item_no][1],$bad_item[$item_no][2],$bad_item[$item_no][3],1) for 1 .. $bad_item[$item_no][4];		
	}

}


1; # �폜�s��
