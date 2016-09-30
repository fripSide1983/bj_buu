require './lib/_bbs_chat.cgi';
require './lib/_comment_tag.cgi';
#================================================
# BBS Created by Merino
#================================================

# �A���������݋֎~����(�b)
$bad_time    = 10;

# �ő�۸ޕۑ�����
$max_log     = 50;

# �ő���Đ�(���p)
$max_comment = 2000;

# ���ް�ɕ\������鎞��(�b)
$limit_member_time = 60 * 4;

# �ő�ߋ�۸ޕۑ�����
$max_bbs_past_log = 50;

#================================================
sub run {

	if ($in{img}) {
		&get_img_list;
		return;
	}

	if ($in{mode} eq "write" && $in{comment}) {
		&write_comment;
		
		# �ۑ�۸ޗp
		if ($in{is_save_log}) {
			if (&is_daihyo) {
				my $sub_this_file = $this_file;
				$this_file .= "_log";
				$max_log = $max_bbs_past_log;
				&write_comment;
				$this_file = $sub_this_file;
				$mes .= "�������݂�۸ޕۑ����܂���<br>";
			}
			else {
				$mes .= "���̑�\\�҈ȊO��۸ޕۑ��͂ł��܂���<br>";
			}
		}
	}
	
	my($member_c, $member) = &get_member;

	$in{text} =~ s/&lt;_&gt;/\r\n/g;

	print qq|<form method="$metod" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>$this_title <font size="2" style="font-weight:normal;">$this_sub_title</font></h2>|;
	print qq|<p>$mes</p>| if $mes;

	print qq|<table><tr>|;
	my $this_script_p = $this_script;
	$this_script_p =~ s/\.cgi//;
	my $button = $is_smart ? button1s : button_s;
	print qq|<td><form method="$method" action="past_log.cgi"><input type="hidden" name="this_title" value="$this_title">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="this_file" value="$this_file"><input type="hidden" name="this_script" value="$this_script_p">|;
	print qq|<input type="submit" value="�ߋ�۸�" class="$button"></form></td>|;
	
	my $smart_i = 0;
	for my $i (1..$w{country}){
		next if ($i == $m{country});
		my $file_name = $this_file . "_log_" . $i;
		$smart_i++;
		if($smart_i % 4 == 0 && $is_smart){
			print qq|</tr><tr>|;
		}
		print qq|<td><form method="$method" action="teisatsu_log.cgi"><input type="hidden" name="this_title" value="$cs{name}[$i]/$this_title">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="hidden" name="this_file" value="$file_name"><input type="hidden" name="this_script" value="$this_script_p">|;
		print qq|<input type="submit" value="$cs{name}[$i]" class="$button"></form></td>|;
	}
	print qq|</tr></table>|;
	
	my $rows = $is_mobile ? 2 : 5;
	print qq|<form method="get" action="$this_script"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<textarea name="comment" cols="60" rows="$rows" wrap="soft" class="textarea1">$in{text}$in{file_name}</textarea><br>|;
	print qq|<input type="submit" value="��������" class="button_s"><input type="checkbox" name="img" value="1"/>�摜��I��|;
	print qq|�@ <input type="checkbox" name="is_save_log" value="1">۸ޕۑ�</form><br>|;
	# �������� ��������� ����c�� �������o�[��\���ɂȂ�
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		print qq|<font size="2">$member_c�l:</font><hr>|;
	}
	else {
		print qq|<font size="2">$member_c�l:$member</font><hr>|;
	}

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ̧�ق��J���܂���");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon,$bicon_pet) = split /<>/, $line;
		$bname = &name_link($bname);
		$bname .= "[$bshogo]" if $bshogo;
		$bicon = $bicon ? qq|<img src="$icondir/$bicon" style="vertical-align:middle;" $mobile_icon_size>| : '';
		$bicon_pet = $m{pet_icon_switch} && $bicon_pet ? qq| <img src="$icondir/pet/$bicon_pet" style="vertical-align:middle;" $mobile_icon_size>| : '';
		$bcomment = &comment_change($bcomment, 0);
		if ($is_mobile) {
			print qq|<div>$bicon$bicon_pet<font color="$cs{color}[$bcountry]">$bname<br>$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font></div><hr size="1">\n|;
		}
		else {
			print qq|<table border="0"><tr><td valign="top" style="padding-right: 0.5em;">$bicon$bicon_pet<br><font color="$cs{color}[$bcountry]">$bname</font></td><td valign="top"><font color="$cs{color}[$bcountry]">$bcomment <font size="1">($cs{name}[$bcountry] $bdate)</font></font><br></td></tr></table><hr size="1">\n|;
		}
	}
	close $fh;
}

sub get_img_list {

#	my ($mday, $mon, $year) = (localtime(time()))[3..5];
#	my $match_cmp = sprintf("%02d%02d",$year + 1900, $mon + 1);
	$in{comment} =~ s/<br>/<_>/g;

	print qq|<form method="$method" action="$this_script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="hidden" name="text" value="$in{comment}">|;
	print qq|<input type="submit" value="����" class="button_s"><hr>|;
	print qq|<input type="radio" name="file_name" value="" checked="checked">��߂�<hr>|;

	my $i = 0;
	my $filedat = "./../upbbs/file.dat";
	open $fh, "< $filedat" or &error("�摜���ް�̧�ق��J���܂���");
	while (my $line = <$fh>) {
		next if $line !~ /.*?$m{name}.*?(jpg|png).*?/;

		my @data = split(/\t/, $line);

		my $file_name = substr($data[5], 10);
		my $title = "";
		my $img_data = "";
		if ($data[6] =~ /^\.\/img.*?(jpg|png)$/) {
			$title = substr($data[6], 10);
		}
		else {
			$title = $data[6];
			$img_data = $data[6];
		}
		$title =~ s|(.*?)<.*|\1|g;
		$img_data =~ s|.*<!--(dsize=.*)-->.*|\1|g;

		print qq|<input type="radio" name="file_name" value="&amp;img($file_name)"><a href="./../upbbs/img-box/$file_name" target="_blank"><img src="./../upbbs/img-box/$file_name" style="vertical-align:middle;" $mobile_icon_size></a><br>$img_data<hr>|;
		$i++;
		last if $i >= 5;
	}
	close $fh;
	print qq|<input type="radio" name="file_name" value="">��߂�<hr>|;
	print qq|<input type="submit" value="����" class="button_s">|;
	print qq|</form>|;
}

1; # �폜�s��
