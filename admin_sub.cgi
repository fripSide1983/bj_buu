#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require './lib/move_player.cgi';
require "$datadir/skill.cgi";
my $this_script = 'admin_sub.cgi';
#=================================================
# �v���C���[�Ǘ� Created by Merino
#=================================================

# ���я���
my %e2j_sorts = (
	country	=> '����',
	name	=> '���O��',
	ldate	=> '�X�V������',
	addr	=> 'νĖ�/IP��',
	agent	=> 'UA(��׳��)',
	check	=> '���d����',
	player	=> '�v���C���[����',
);

# ��̫�Ă̕��я�
$in{sort} ||= 'addr';


#=================================================
# ���C������
#=================================================
&header;
&decode;
&error('�߽ܰ�ނ��Ⴂ�܂�') unless $in{pass} eq $admin_sub_pass;
&read_cs;

if ($in{mode} eq 'junk_sub')          { &junk_sub($in{j_del}); }
elsif ($in{mode} eq 'country_reset')     { &country_reset; }
elsif ($in{mode} eq 'boss_make')         { &boss_make; }
elsif ($in{mode} eq 'admin_repaire')     { &admin_repaire; }
elsif ($in{mode} eq 'admin_compare')   { &admin_compare; }
elsif ($in{mode} eq 'shield')   { &admin_shield; }

&top;
&footer;
exit;

#=================================================
# top
#=================================================
sub top {
	print qq|<form action="$script_index"><input type="submit" value="�s�n�o" class="button1"></form>|;

	print qq|<form action="admin_country_sub.cgi"><input type="hidden" name="pass" value="$in{pass}"><input type="submit" value="���Ǘ���" class="button1"></form>|;

	print qq|<table border="0"><tr>|;
	print qq|<td><form method="$method" action="$this_script"><input type="hidden" name="country" value=""><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="sort" value="$in{sort}"><input type="submit" value="�Sհ�ް" class="button_s"></form></td>|;
	for my $i (0 .. $w{country}) {
		print qq|<td><form method="$method" action="$this_script"><input type="hidden" name="country" value="$i"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="hidden" name="sort" value="$in{sort}"><input type="submit" value="$cs{name}[$i]" class="button_s"></form></td>|;
	}
	print qq|</tr></table>|;
	
	print qq|<table border="0"><tr>|;
	while (my($k,$v) = each %e2j_sorts) {
		print qq|<td><form method="$method" action="$this_script"><input type="hidden" name="country" value="$in{country}"><input type="hidden" name="pass" value="$in{pass}">\n|;
		print qq|<input type="hidden" name="sort" value="$k"><input type="submit" value="$v" class="button_s"></form></td>\n|;
	}
	print qq|</tr></table>|;
	
	print qq|<div class="mes">$mes</div><br>| if $mes;
	
	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="mode" value="admin_delete_user"><input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<input type="hidden" name="country" value="$in{country}"><input type="hidden" name="sort" value="$in{sort}">|;
	print qq|ؾ�ẮA��ʂɉ����\\������Ȃ��Ȃ�����ANext���[�v�ɂ͂܂�����Ԃ��C�����܂��B<br>|;
	print qq|<table class="table1"><tr>|;

	for my $k (qw/���O �ۑS �������� ̫��� �� IP���ڽ νĖ� UserAgent(��׳��) �X�V����/) {
		print qq|<th>$k</th>|;
	}
	print qq|</tr>|;
	
	# �v���C���[�����擾
	my @lines = $in{country} eq '' ? &get_all_users : &get_country_users($in{country});

	my $b_addr  = '';
	my $b_host  = '';
	my $b_agent = '';
	my $count = 0;
	my $pre_line = '';
	my $is_duplicated = 0;
	for my $line (@lines) {
		my($id, $name, $pass, $country, $addr, $host, $agent, $ldate) = split /<>/, $line;
		
		# �����z�X�g���������Ȃ�ԕ\��
		if ( ($addr eq $b_addr && $host eq $b_host && $agent eq $b_agent)
			|| ($agent eq $b_agent && ($agent =~ /DoCoMo/ || $agent =~ /KDDI|UP\.Browser/ || $agent =~ /J-PHONE|Vodafone|SoftBank/)) ) {
				unless ($is_duplicated) {
					my($pid, $pname, $ppass, $pcountry, $paddr, $phost, $pagent, $pldate) = split /<>/, $pre_line;
					print qq|<tr class="stripe2">|;
					print qq|<td>$pname</td>|;
					print qq|<td><input type="button" class="button_s" value="�ۑS" onClick="location.href='?mode=shield&shield=$id&pass=$in{pass}';"></td>|;
					print qq|<td><input type="button" class="button_s" value="��������" onClick="location.href='?sort=player&checkid=$id&pass=$in{pass}';"></td>|;
					print qq|<td>$pid</td>|;
					print qq|<td>$cs{name}[$pcountry]</td>|;
					print qq|<td>$paddr</td>|;
					print qq|<td>$phost</td>|;
					print qq|<td>$pagent</td>|;
					print qq|<td>$pldate</td></tr>|;
				}
				print qq|<tr class="stripe2">|;
				$is_duplicated = 1;
		}
		else{
			$is_duplicated = 0;
			if ($in{sort} ne 'check') {
				print ++$count % 2 == 0 ? qq|<tr class="stripe1">| : qq|<tr>|;
			}
		}
		$b_addr  = $addr;
		$b_host  = $host;
		$b_agent = $agent;
		
		if ($in{sort} ne 'check' || $is_duplicated) {
			print qq|<td>$name</td>|;
			print qq|<td><input type="button" class="button_s" value="�ۑS" onClick="location.href='?mode=shield&shield=$id&pass=$in{pass}';"></td>|;
			print qq|<td><input type="button" class="button_s" value="��������" onClick="location.href='?sort=player&checkid=$id&pass=$in{pass}';"></td>|;
			print qq|<td>$id</td>|;
			print qq|<td>$cs{name}[$country]</td>|;
			print qq|<td>$addr</td>|;
			print qq|<td>$host</td>|;
			print qq|<td>$agent</td>|;
			print qq|<td>$ldate</td></tr>|;
		}
		
		$pre_line = $line;
	}
	print qq|</table><br></form>|;
	
	print qq|<br><br><br>|;
	print qq|<div class="mes">�f�[�^�␳�F�ȉ��̏�ԂɂȂ������Ɏg�p<ul>|;
	print qq|<li>���ۂ̓o�^�l�����Ⴄ|;
	print qq|<li>�������o�[�ɈႤ���̐l�������Ă�|;
	print qq|<li>�������o�[�ɓ������O�̐l������|;
	print qq|<li>�������o�[�Ƀv���C���[�ꗗ�ɂ͑��݂��Ȃ��l������|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_repaire">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�f�[�^�␳" class="button_s"></p></form></div>|;
	
	print qq|<br><br><br>|;
	print qq|<div class="mes">�C��r�F��̍C�̃��O�C���󋵂��r����<ul>|;
	print qq|<li>���C�^�f�̂���v���C���[������ꍇ��r���܂�|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="admin_compare">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="���C��r" class="button_s"></p>|;
	print qq|<input type="text" name="comp1" value="">|;
	print qq|<input type="text" name="comp2" value=""></form></div>|;
	
	print qq|<br><br><br>|;
	print qq|<div class="mes">���A�Ď��F�ȉ��̏�ԂɂȂ������Ɏg�p<ul>|;
	print qq|<li>���C���A�^�f�̂���v���C���[������ꍇ�ɃW�����N�V���b�v�̃��O���Q�Ƃ��܂�|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="junk_sub">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="���A�Ď�" class="button_s"></p>|;
	print qq|<input type="hidden" name="j_del" value="0">|;
	print qq|</form></div>|;

	print qq|<br><br><br>|;
	print qq|<div class="mes">��ް���ޑ���F�ȉ��̏�ԂɂȂ������Ɏg�p<ul>|;
	print qq|<li>�����̌�쓮����ް���ޑ��肳��Ȃ��������i�l�ݒ�ɂ�����炸�S����ް���ޑ���ɂ��܂��j|;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="country_reset">|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="����ݑ���" class="button_s"></p></form></div>|;
	
	print qq|<br><br><br>|;
	print qq|<div class="mes">�{�X<ul>|;
	print qq|<li>���݂̃{�X<br>|;
	open my $bfh, "< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgi̧�ق�����܂���");
	my $line = <$bfh>;
	my ($bname, $bcountry, $bmax_hp, $bmax_mp, $bat, $bdf, $bmat, $bmdf, $bag, $bcha, $bwea, $bskills, $bmes_win, $bmes_lose, $bicon, $bwea_name) = split /<>/, $line;
	print qq|$bname HP:$bmax_hp MP:$bmax_mp<br>|;
	print qq|�U��:$bat ���U:$bmat<br>|;
	print qq|�h��:$bdf ���h:$bmdf<br>|;
	print qq|�f��:$bag ����:$bcha<br>|;
	print qq|����:$weas[$bwea][1]<br>|;
	print qq|�Z:|;
	my @bskill = split /,/, $bskills;
	for(@bskill){
		print qq|$skills[$_][1],|;
	}
	print qq|<br>|;
	print qq|<form method="$method" action="$this_script"><p>�V�{�X�쐬</p><input type="hidden" name="mode" value="boss_make">|;
	print qq|<p>�{�X��<input type="text" name="boss_name" class="text_box1"></p>|;
	print qq|<p>HP<input type="text" name="boss_hp" class="text_box1">MP<input type="text" name="boss_mp" class="text_box1"></p>|;
	print qq|<p>�U��<input type="text" name="boss_at" class="text_box1">���U<input type="text" name="boss_mat" class="text_box1"></p>|;
	print qq|<p>�h��<input type="text" name="boss_df" class="text_box1">���h<input type="text" name="boss_mdf" class="text_box1"></p>|;
	print qq|<p>�f��<input type="text" name="boss_ag" class="text_box1">����<input type="text" name="boss_cha" class="text_box1"></p>|;
	print qq|<p>����<select name="boss_wea" class="menu1">|;
	for(0..$#weas){
		print qq|<option value="$_">$weas[$_][1]</option>|;
	}
	print qq|<p>���햼<input type="text" name="boss_weaname" class="text_box1"></p>|;
	print qq|</select></p>|;
	for my $i (1..5){
		print qq|<p>�Z$i<select name="boss_skill$i" class="menu1">|;
		for(0..$#skills){
			print qq|<option value="$_">$skills[$_][1]</option>|;
		}
		print qq|</select></p>|;
	}
	print qq|<p>���j���b�Z�[�W<input type="text" name="boss_winmes" class="textarea1"></p>|;
	print qq|<p>�s�k���b�Z�[�W<input type="text" name="boss_losemes" class="textarea1"></p>|;
	print qq|<input type="hidden" name="pass" value="$in{pass}">|;
	print qq|<p><input type="submit" value="�V�{�X�쐬" class="button_s"></p></form></div>|;
}

#=================================================
# �����������F�����I�ɖ������ɂ���
#=================================================
sub admin_go_neverland {
	return unless $in{id};
	
	require './lib/move_player.cgi';
	local %m = &get_you_datas($in{id}, 1);
	$m{lib} = '';
	$m{wt} = $m{tp} = $m{turn} = $m{stock} = $m{value} = 0;
	$id = $in{id};
	&move_player($m{name}, $m{country}, 0);
	$m{country} = 0;

	&regist_you_data($m{name}, "random_migrate", 0);
	
	&write_user;
	
	$mes .= "$m{name}�̏�������ؾ�Ă��܂���<br>";
}


#=================================================
# �����Ƃ̃��[�U�[�f�[�^���擾
#=================================================
sub get_country_users {
	my $country = shift;
	my @lines = ();
	open my $fh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgi̧�ق��ǂݍ��߂܂���");
	while (my $name = <$fh>) {
		$name =~ tr/\x0D\x0A//d;
		
		my $id = unpack 'H*', $name;
		open my $fh2, "< $userdir/$id/user.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
		my $line_data = <$fh2>;
		my $line_info = <$fh2>;
		close $fh2;
		
		my %m = ();
		for my $hash (split /<>/, $line_data) {
			my($k, $v) = split /;/, $hash;
			next if $k =~ /^y_/;
			$m{$k} = $v;
		}
		($m{addr}, $m{host}, $m{agent}) = split /<>/, $line_info;

		my $line = "$id<>";
		for my $k (qw/name pass country addr host agent ldate/) {
			$line .= "$m{$k}<>";
		}
		push @lines, "$line\n";
	}
	close $fh;

	if    ($in{sort} eq 'name')    { @lines = map { $_->[0] } sort { $a->[2] cmp $b->[2] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'addr')    { @lines = map { $_->[0] } sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'ldate')   { @lines = map { $_->[0] } sort { $a->[8] cmp $b->[8] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'country') { @lines = map { $_->[0] } sort { $a->[4] <=> $b->[4] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'agent')   { @lines = map { $_->[0] } sort { $b->[7] cmp $a->[7] } map { [$_, split /<>/] } @lines; }
	
	return @lines;
}


#=================================================
# �S���[�U�[�̃f�[�^���擾
#=================================================
sub get_all_users {
	my @lines = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		
		open my $fh, "< $userdir/$id/user.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
		my $line_data = <$fh>;
		my $line_info = <$fh>;
		close $fh;
		
		my %m = ();
		for my $hash (split /<>/, $line_data) {
			my($k, $v) = split /;/, $hash;
			next if $k =~ /^y_/;
			$m{$k} = $v;
		}
		
		if(-f "$userdir/$id/access_log.cgi" && ($in{sort} eq 'check' || $in{sort} eq 'player')){
			open my $fh2, "< $userdir/$id/access_log.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
			while (my $line_info_add = <$fh2>){
				($m{addr}, $m{host}, $m{agent}) = split /<>/, $line_info_add;
				my $line = "$id<>";
				for my $k (qw/name pass country addr host agent ldate/) {
					$line .= "$m{$k}<>";
				}
				unless($m{host} =~ /\.trendmicro\.com$|\.sjdc$|\.iad1$/){
					push @lines, "$line\n";
				}
			}
		}else{
			($m{addr}, $m{host}, $m{agent}) = split /<>/, $line_info;
			my $line = "$id<>";
			for my $k (qw/name pass country addr host agent ldate/) {
				$line .= "$m{$k}<>";
			}
			push @lines, "$line\n";
		}
	}
	closedir $dh;
	
	if    ($in{sort} eq 'name')    { @lines = map { $_->[0] } sort { $a->[2] cmp $b->[2] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'addr')    { @lines = map { $_->[0] } sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'ldate')   { @lines = map { $_->[0] } sort { $b->[8] cmp $a->[8] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'country') { @lines = map { $_->[0] } sort { $a->[4] <=> $b->[4] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'agent')   { @lines = map { $_->[0] } sort { $b->[7] cmp $a->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'check')   { @lines = map { $_->[0] } sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }
	elsif ($in{sort} eq 'player')  { @lines = map { $_->[0] } sort { $a->[2] cmp $b->[2] ||$a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] } map { [$_, split /<>/] } @lines; }

	return @lines;
}

#=================================================
# �f�[�^�␳�F�l���⍑�����ް�Ȃǂ����������̂���U�����ɂ��Ă��珑������
#=================================================
sub admin_repaire {
	my %members = ();
	
	my $count = 0;
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);
		
		push @{ $members{$m{country}} }, "$m{name}\n";
		++$count;
	}
	closedir $dh;
	my $country = $w{world} eq $#world_states ? $w{country} - 1 :
					$w{world} eq $#world_states-2 ? 2 :
					$w{world} eq $#world_states-3 ? 3 : $w{country};
	$w{player} = $count;
	my $ave_c = int($w{player} / $country);
	
	my $all_member = 0;
	for my $i (0 .. $w{country}) {
		$mes .= "<hr>$cs{name}[$i]<br>@{ $members{$i} }<br>";
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgi̧�ق��J���܂���");
		print $fh @{ $members{$i} };
		close $fh;
		
		$cs{member}[$i] = @{ $members{$i} } || 0;
		$cs{capacity}[$i] = $w{world} eq $#world_states && $i == $w{country} ? 6:
							$w{world} eq $#world_states-2 && $i < $w{country} - 1 ? 0:
							$w{world} eq $#world_states-3 && $i < $w{country} - 2 ? 0:$ave_c;
	}
	
	&write_cs;
	$mes .= "<hr>�l���⍑�����ް̧�ق��C�����܂���<br>";
}

#=================================================
# ���A�Ď�
#=================================================
sub junk_sub {
	my $del = shift;
	open my $fh3, "+< $logdir/junk_shop_sub.cgi" or &error("$logdir/junk_shop_sub.cgi̧�ق��J���܂���");
	my @lines = <$fh3>;
	my @sell = ();
	my @buy = ();
	$mes .= qq|<table class="table1"><tr><th>�A�C�e��</th><th>���O</th><th>����/����</th><th>����</th></tr>|;
	@lines = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] || $a->[5] <=> $b->[5]}
					map { [$_, split /<>/ ] } @lines;
	for my $line (@lines){
		my($kind, $item_no, $item_c, $name, $jtime, $type) = split /<>/, $line;
		$mes .= "<td>";
		$mes .= $kind eq '1' ? $weas[$item_no][1]
			: $kind eq '2' ? $eggs[$item_no][1]
			:				$pets[$item_no][1];
		$mes .= "</td><td>$name</td>";
		$mes .= $type ? "<td>����</td>" : "<td>����</td>";
		$mes .= "<td>$jtime<br></td></tr>";
	}
	$mes .= "</table>";
	
	close $fh3;
}

#=================================================
# ��ް���ޑ���
#=================================================
sub country_reset {
	my %members = ();
	
	my $count = 0;
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		my %m = &get_you_datas($id, 1);
		
		&regist_you_data($m{name}, 'country', 0);
		for my $k (qw/war dom pro mil/) {
			&regist_you_data($name, $k."_c", $m{$k."_c_t"}+$m{$k."_c"});
		}
		&regist_you_data($m{name}, "random_migrate", 0);
		
		push @{ $members{0} }, "$m{name}\n";
		++$count;
	}
	closedir $dh;
	my $country = $w{world} eq $#world_states ? $w{country} - 1 :
					$w{world} eq $#world_states-2 ? 2 :
					$w{world} eq $#world_states-3 ? 3 : $w{country};
	$w{player} = $count;
	my $ave_c = int($w{player} / $country);
	
	my $all_member = 0;
	for my $i (0 .. $w{country}) {
		$mes .= "<hr>$cs{name}[$i]<br>@{ $members{$i} }<br>";
		open my $fh, "> $logdir/$i/member.cgi" or &error("$logdir/$i/member.cgi̧�ق��J���܂���");
		print $fh @{ $members{$i} };
		close $fh;
		
		$cs{member}[$i] = @{ $members{$i} } || 0;
		$cs{capacity}[$i] = $w{world} eq $#world_states && $i == $w{country} ? 6:
							$w{world} eq $#world_states-2 && $i < $country - 1 ? 0:
							$w{world} eq $#world_states-3 && $i < $country - 1 ? 0:$ave_c;
	}
	
	&write_cs;
	$mes .= "<hr>�S����ް���ޑ���ɂ��܂���<br>";
}

#=================================================
# ���{�X�쐬
#=================================================
sub boss_make {
	open my $bfh, "> $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgi̧�ق�����܂���");
	print $bfh "$in{boss_name}<>0<>$in{boss_hp}<>$in{boss_mp}<>$in{boss_at}<>$in{boss_df}<>$in{boss_mat}<>$in{boss_mdf}<>$in{boss_ag}<>$in{boss_cha}<>$in{boss_wea}<>$in{boss_skill1},$in{boss_skill2},$in{boss_skill3},$in{boss_skill4},$in{boss_skill5}<>$in{boss_losemes}<>$in{boss_winmes}<>$default_icon<>$in{boss_weaname}<>\n";
	close $bfh;
}

#=================================================
# ���C��r
#=================================================
sub admin_compare {
	my @lines = ();
	my @comp = ($in{comp1}, $in{comp2});
	my %addr = ();
	my %host = ();
	my %agent = ();
	my $bit = 1;
	for my $name (@comp) {
		my $id = unpack 'H*', $name;
		
		open my $fh2, "< $userdir/$id/access_log.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
		while (my $line_info_add = <$fh2>){
			my ($maddr, $mhost, $magent) = split /<>/, $line_info_add;
			if (($addr{$maddr} & $bit) == 0) {
				$addr{$maddr} |= $bit;
			}
			if (($host{$mhost} & $bit) == 0) {
				$host{$mhost} |= $bit;
			}
			if (($agent{$magent} & $bit) == 0) {
				$agent{$magent} |= $bit;
			}
		}
		$bit *= 2;
	}
	
	$mes .= qq|<table class="table1">|;
	$mes .= qq|<tr>|;
	$mes .= qq|<th>�A�h���X</th>|;
	for my $name (@comp) {
		$mes .= qq|<th>$name</th>|;
	}
	$mes .= qq|</tr>|;
	foreach my $maddr (keys(%addr)) {
		my $mes_tr = qq|<td>$maddr</td>|;
		$bit = 1;
		my $count = 0; 
		for my $name (@comp) {
			$mes_tr .= qq|<td>|;
			if ($addr{$maddr} & $bit) {
				$mes_tr .= qq|��|;
				$count++;
			}
			$mes_tr .= qq|</td>|;
			$bit *= 2;
		}
		$mes .= $count > 1 ? qq|<tr class="stripe2">| : qq|<tr>|;
		$mes .= $mes_tr;
		$mes .= qq|</tr>|;
	}
	$mes .= qq|</table>|;

	$mes .= qq|<table class="table1">|;
	$mes .= qq|<tr>|;
	$mes .= qq|<th>�z�X�g��</th>|;
	for my $name (@comp) {
		$mes .= qq|<th>$name</th>|;
	}
	$mes .= qq|</tr>|;
	foreach my $mhost (keys(%host)) {
		my $mes_tr = qq|<td>$mhost</td>|;
		$bit = 1;
		my $count = 0; 
		for my $name (@comp) {
			$mes_tr .= qq|<td>|;
			if ($host{$mhost} & $bit) {
				$mes_tr .= qq|��|;
				$count++;
			}
			$mes_tr .= qq|</td>|;
			$bit *= 2;
		}
		$mes .= $count > 1 ? qq|<tr class="stripe2">| : qq|<tr>|;
		$mes .= $mes_tr;
		$mes .= qq|</tr>|;
	}

	$mes .= qq|<table class="table1">|;
	$mes .= qq|<tr>|;
	$mes .= qq|<th>�G�[�W�F���g</th>|;
	for my $name (@comp) {
		$mes .= qq|<th>$name</th>|;
	}
	$mes .= qq|</tr>|;
	foreach my $magent (keys(%agent)) {
		my $mes_tr = qq|<td>$magent</td>|;
		$bit = 1;
		my $count = 0; 
		for my $name (@comp) {
			$mes_tr .= qq|<td>|;
			if ($agent{$magent} & $bit) {
				$mes_tr .= qq|��|;
				$count++;
			}
			$mes_tr .= qq|</td>|;
			$bit *= 2;
		}
		$mes .= $count > 1 ? qq|<tr class="stripe2">| : qq|<tr>|;
		$mes .= $mes_tr;
		$mes .= qq|</tr>|;
	}
	$mes .= qq|</table>|;
}

#=================================================
# �f�[�^�ۑS
#=================================================
sub admin_shield {
	my %s = &get_you_datas($in{shield}, 1);
	
	$mes .= "$s{name}�̃f�[�^��";
	if ($s{delete_shield}) {
		&regist_you_data($s{name}, "delete_shield", 0);
		$mes .= "�ۑS����������܂����B<br>";
	} else {
		&regist_you_data($s{name}, "delete_shield", 1);
		$mes .= "�ۑS���܂����B<br>";
	}
}


