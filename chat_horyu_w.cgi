#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/_comment_tag.cgi';
#=================================================
# �����ē��_���X������
#=================================================
use File::Copy;

&get_data;

$this_title  = "�����ċc��쐬";
$this_list   = "$logdir/chat_horyu_list";
$save_list   = "$logdir/chat_horyu_list_s";
$this_dir    = "$logdir/kaizou";
$save_dir    = "$logdir/kaizou2";
$this_script = 'chat_horyu_w.cgi';
$this_return = 'chat_horyu_w';

@deletable_member = ($admin_name, $admin_sub_name);

# �ő���Đ�(���p)
$max_comment = 2000;

#=================================================
&run;
&footer;
exit;

#=================================================
sub run {

	&write_comment if ($in{mode} eq "write" && $in{target} eq "new" && $in{comment});
	&del_comment if ($in{mode} eq "write" && $in{target} ne "new" && &delete_check);

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;

	my $rows = $is_mobile ? 2 : 5;
	print qq|<form method="$method" action="$this_script"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1"></textarea><br>|;
	print qq|<input type="hidden" name="limit" value="365">|;
#	print qq|<select name="limit">|;
#	print qq|<option value="1">�������</option>|;
#	print qq|<option value="3">�����O��</option>|;
#	print qq|<option value="7" selected>��������</option>|;
#	print qq|<option value="365" selected>��������</option>|;
#	print qq|</select>|;
	print qq|<input type="submit" value="�쐬" class="button_s"><br>|;
	print qq|<input type="radio" name="target" value="new" checked>�c����쐬<br><hr size="5"><br>|;
	print qq|<input type="checkbox" name="save" value="1" checked>�I���c�Ă�ۑ�<br>|;
	
	open my $fh, "< $this_list.cgi" or &error("$this_list.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
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
		if($limit > $time){
			print qq|������]�� $goodn �l:$bgood �������Ύ� $badn �l:$bbad\n|;
		}else{
			if($goodn > $badn){
				print qq|<font size="5"><font color="blue">������]�� $goodn �l:$bgood</font> �������Ύ� $badn �l:$bbad ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
			}elsif($goodn < $badn){
				print qq|<font size="5">������]�� $goodn �l:$bgood <font color="red">�������Ύ� $badn �l:$bbad</font> ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
			}else{
				print qq|<font size="5"><font color="yellow">������]�� $goodn �l:$bgood �������Ύ� $badn �l:$bbad</font> ���̋c��͊��Ԃ��߂��Ă܂�</font><br>\n|;
			}
		}
		print qq|<input type="radio" name="target" value="$line">���̋c�������<br>|;
		 $linet = <$fh2>;
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bid) = split /<>/, $linet;
		$bname .= "[$bshogo]" if $bshogo;
		$bicon = qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>|;
		if ($hidden) {
			$bname = "����";
			$bicon = $default_icon;
			$bcountry = 0;
		}
		$bcomment = &comment_change($bcomment, 1);
		print qq|<font color="$cs{color}[$bcountry]">$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
		close $fh2;
		print qq|<hr size="5">\n|;
	}
	close $fh;
	print qq|</form>|;
}

#=================================================
# �������ݏ���
#=================================================
sub write_comment {
	&error('�{���ɉ���������Ă��܂���') if $in{comment} eq '';
	&error("�{�����������܂�(���p$max_comment�����܂�)") if length $in{comment} > $max_comment;
	my $max = 1;
	open my $fh, "< $this_list.cgi" or &error("$this_list.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
		chomp($line);
		if($line > $max){
			$max = $line;
		}
	}
	close $fh;
	my $target = $max+1;

	open my $fhw, ">> $this_list.cgi" or &error("$this_list.cgi ̧�ق��J���܂���");
	print $fhw "$target\n";
	close $fhw;

	open my $fh2, "> $this_dir/$target.cgi" or &error("$this_dir/$target.cgi ̧�ق��J���܂���");

	# ����ݸ
	$in{comment} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;#"
	
	my $limit = $in{limit} * 24 * 3600;
	my $limit_time = $time + $limit;
	my ($lmin, $lhour, $lday, $lmon) = (localtime($limit_time))[1, 2, 3, 4];
	$lmon += 1;
	if ($in{limit} <= 7) {
		$in{comment} .= "<br>�c�_����:$lmon��$lday��$lhour��$lmin��";
	}

	print $fh2 "<><>$limit_time<>0<>\n";
	print $fh2 "$time<>$date<>$m{name}�����o<br>�c��<>0<><>$addr<>$in{comment}<>$m{icon}<>\n";
	close $fh2;

	$in{comment} = "$m{name}���񂪉����Ă��쐬���܂���<hr>�y�����Ă��瑗�M�z";
	my $mname = $m{name};
	$m{name} = '�V�X�e��';
	my $mcountry = $m{country};
	$m{country} = 0;
	my $micon = $m{icon};
	$m{icon} = '';
	my $mshogo = $m{shogo};
	$m{shogo} = '';
	&send_group('all');

	$in{comment} = "";
	$m{name} = $mname;
	$m{country} = $mcountry;
	$m{icon} = $micon;
	$m{shogo} = $mshogo;

	return 1;
}

#=================================================
# �c�����
#=================================================
sub del_comment {
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

	if($in{save}){
		open my $fh2, ">> $save_list.cgi" or &error("$save_list.cgi ̧�ق��J���܂���");
		print $fh2 "$in{target}\n";
		close $fh2;
		copy("$this_dir/$in{target}.cgi", "$save_dir/$in{target}.cgi");
		&doubled_save_clean;
	}
	
	unlink "$this_dir/$in{target}.cgi" or &error("$this_dir/$in{target}.cgi ̧�ق��폜�ł��܂���");

	return 1;
}

#=================================================
# �ۑ����X�g�C��
#=================================================
sub doubled_save_clean {
	my @lines;
	my %sames = ();
	open my $fh, "+< $save_list.cgi" or &error("$save_list.cgi ̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		chomp($line);
		next if $sames{$line}++;
		push @lines, "$line\n";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}

#=================================================
# �폜�҃`�F�b�N
#=================================================
sub delete_check {
	for my $name (@deletable_member){
		if($name eq $m{name}){
			return 1;
		}
	}
	return 0;
}

