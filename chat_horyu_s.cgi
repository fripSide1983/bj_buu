#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/_comment_tag.cgi';
#=================================================
# �����ē��_���ۑ����O
#=================================================
&get_data;

$this_title  = "���[�ς݋c��";
$this_list   = "$logdir/chat_horyu_list_s";
$this_dir    = "$logdir/kaizou2";
$this_script = 'chat_horyu_s.cgi';

@del_member = ('����', '������������');
#=================================================
&run;
&footer;
exit;

#=================================================
sub run {
	&del_thread if ($in{mode} eq "delete" && &del_check);
	
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	open my $fh, "< $this_list.cgi" or &error("$this_list.cgi ̧�ق��J���܂���");
	my @rev_line;
	while (my $line = <$fh>) {
		unshift @rev_line, $line
	}
	for my $line (@rev_line) {
		chomp($line);
		open my $fh2, "< $this_dir/$line.cgi" or &error("$this_dir/$line.cgi ̧�ق��J���܂���");
		my $head_linet = <$fh2>;
		my ($bgood,$bbad,$limit,$hidden) = split /<>/, $head_linet;
		my @goods = split /,/, $bgood;
		my $goodn = @goods;
		my @bads = split /,/, $bbad;
		my $badn = @bads;
		if ($hidden) {
			$bgood = "����";
			$bbad = "����";
		}
		print qq|<hr size="1">|;
		if($goodn > $badn){
			print qq|<font size="5"><font color="blue">������]�� $goodn �l:$bgood</font> �������Ύ� $badn �l:$bbad ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
		}elsif($goodn < $badn){
			print qq|<font size="5">������]�� $goodn �l:$bgood <font color="red">�������Ύ� $badn �l:$bbad</font> ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
		}else{
			print qq|<font size="5"><font color="yellow">������]�� $goodn �l:$bgood �������Ύ� $badn �l:$bbad</font> ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
		}
		
		if(&del_check){
			print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="delete">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="�폜" class="button_s">|;
			print qq|<input type="hidden" name="target" value="$line"></form>|;
		}
		while (my $linet = <$fh2>) {
			my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bid) = split /<>/, $linet;
			$bname .= "[$bshogo]" if ($bshogo && $bname ne '����������@���؎I');
			$bicon = qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>|;
			if ($hidden) {
				$bname = "����";
				$bicon = $default_icon;
				$bcountry = 0;
			}
			$bcomment = &comment_change($bcomment, 1);
			print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
		}
		close $fh2;
		print qq|<hr size="5">\n|;
	}
	close $fh;
	print qq|</form>|;
}
#=================================================
# �c�����
#=================================================
sub del_thread {
	my @lines;
	my %sames = ();
	open my $fh, "+< $this_list.cgi" or &error("$this_list.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		chomp($line);
		if($line != $in{target}){
			next if $sames{$line}++;
			push @lines, "$line\n";
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	unlink "$this_dir/$in{target}.cgi" or &error("$this_dir/$in{target}.cgi ̧�ق��폜�ł��܂���");

	return 1;
}

#=================================================
# ����҃`�F�b�N
#=================================================
sub del_check {
	for my $name (@del_member){
		if($name eq $m{name}){
			return 1;
		}
	}
	return 0;
}
