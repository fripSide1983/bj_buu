#================================================
# ���ɋ��p�֐�
#================================================

use constant GAME_RESET => 1; # �ްт̍X�V���~�܂��Ă���
use constant LEAVE_PLAYER => 2; # �Q���҂���è�ނɂȂ��Ă���

$limit_think_time = 60 * 10; # 10�����u����ڲ԰���O
$limit_game_time = 60 * 20; # 30�����u�Źް�ؾ��

#================================================
# �ΐl���ɂ̊�{�I��Ҳ݉��
#================================================
sub _default_run {
#	my $_default = $_; # ���ĕ����̗L��
	$in{comment} = &{$in{mode}} if $in{mode} && $in{mode} ne 'write'; # �e����ނɑΉ�����֐��ւ�۰�ް
	&write_comment if $in{comment};

	my @datas = ();

	my($member_c, $member, @datas) = &get_member;

	if($m{c_turn} eq '0' || $m{c_turn} eq ''){
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	}

	print qq|<h2>$this_title</h2>|;
	print qq|$mes|;
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="����" class="button_s"><br>|;
	unless ($is_mobile) {
		print qq|�����۰��<select name="reload_time" class="select1"><option value="0">�Ȃ�|;
		for my $i (1 .. $#reload_times) {
			print $in{reload_time} eq $i ? qq|<option value="$i" selected>$reload_times[$i]�b| : qq|<option value="$i">$reload_times[$i]�b|;
		}
		print qq|</select>|;
	}
	print qq|</form><font size="2">$member_c�l:$member</font><br>|;

	&show_game_info(@datas);

	print qq|<hr>|;
	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my ($btime, $bdate, $bname, $bcountry, $bshogo, $baddr, $bcomment, $bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$is_mobile ? $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
}

#================================================
# ��݂̑���
#================================================
sub coin_move{
	my ($m_coin, $name, $no_system_comment) = @_;
	my $ret_v;
	
	my $player_id = unpack 'H*', $name;

	# ���݂��Ȃ��ꍇ�̓X�L�b�v
	unless (-f "$userdir/$player_id/user.cgi") {
		return $ret_v;
	}
	if($name eq $m{name}){
		if ($m{coin} + $m_coin < 0){
			$ret_v = -1 * $m{coin};
		}else {
			$ret_v = $m_coin;
		}
		
		$m{coin} += $ret_v;
		&write_user;
	}else{
		my %datas1 = &get_you_datas($name);
		my $temp = $datas1{coin} + $m_coin;

		if ($temp < 0){
			$temp = 0;
			$ret_v = -1 * $datas1{coin};
		} else {
			if ($temp > 2500000) {
				$temp = 2500000;
			}
			$ret_v = $m_coin;
		}
		&regist_you_data($name,'coin',$temp);
	}

	unless ($no_system_comment) {
		if($ret_v > 0){
			&system_comment("$name �� $ret_v ��ݓ��܂���");
		}else{
			my $temp = -1 * $ret_v;
			&system_comment("$name �� $temp ��ݕ����܂���");
		}
	}
	
	if ($m_coin < $ret_v) {
		my $diff = ($ret_v - $m_coin) * 10;
			
		my $shop_id = unpack 'H*', $name;
		my $this_pool_file = "$userdir/$shop_id/casino_pool.cgi";
		my @lines = ();
		if (-f $this_pool_file) {
			open my $fh, "+< $this_pool_file" or &error("$this_pool_file���J���܂���");
			eval { flock $fh, 2; };
			
			while (my $line = <$fh>){
				my($pool, $this_term_gain, $slot_runs) = split /<>/, $line;
				$pool -= $diff;
				push @lines, "$pool<>$this_term_gain<>$slot_runs<>\n";
				last;
			}
			
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
		}
	}
	
	return $ret_v;
}

sub bonus {
	my $name = shift;
	my $mes_as = shift;
	my $mes_news = shift;
	
	my $player_id = unpack 'H*', $name;

	# ���݂��Ȃ��ꍇ�̓X�L�b�v
	unless (-f "$userdir/$player_id/user.cgi") {
		return;
	}
	
	require "$datadir/casino_bonus.cgi";
	my $prize;
	my $item_no = int(rand($#bonus+1));
	&send_item($name,$bonus[$item_no][0],$bonus[$item_no][1],$bonus[$item_no][2],$bonus[$item_no][3], 1);
	if($bonus[$item_no][0] == 1){
		$prize .= "$weas[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 2){
		$prize .= "$eggs[$bonus[$item_no][1]][1]";
	}elsif($bonus[$item_no][0] == 3){
		$prize .= "$pets[$bonus[$item_no][1]][1]";
	}
	if ($mes_as ne '') {
		&system_comment("$name �� $mes_as �Ƃ��� $prize ���l�����܂���");
	}
	if ($mes_news ne '') {
		&write_send_news(qq|<font color="#FF0000">$name �� $mes_news</font>|);
	}
}

sub system_comment{
	my $s_mes = shift;

	my @lines = ();
	open my $fh, "+< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };

	# ����ݸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"
	my $head_line = <$fh>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		push @lines, $line;
		last if @lines >= $max_log-1;
	}
	unshift @lines, "$time<>$date<>�V�X�e�����b�Z�[�W<>0<><>$addr<>$s_mes<>$default_icon<>\n";
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#================================================
# �ΐl���Ɋ֌W�̕ϐ���������
#================================================
sub you_c_reset {
	my $name = shift;
	if ($name eq $m{name}) {
		$m{c_turn} = 0;
		$m{c_value} = 0;
		$m{c_stock} = 0;
		&write_user;
	}else {
		&regist_you_data($name,'c_turn',0);
		&regist_you_data($name,'c_value',0);
		&regist_you_data($name,'c_stock',0);
	}
}

#================================================
# �ΐl���Ɋ֌W�̕ϐ���������(����հ�ް)
#================================================
sub you_lot_c_reset {
	my @names = @_;

	my @data = (
		['c_turn', 0],
		['c_value', 0],
		['c_stock', 0],
	);

	for $name (@names) {
		if ($name eq $m{name}) {
			$m{c_turn} = $m{c_value} = $m{c_stock} = 0;
			&write_user;
		}
		else {
			&regist_you_array($datas{name}, @data);
		}
	}
}

1;#�폜�s��
