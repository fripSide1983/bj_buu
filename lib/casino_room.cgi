#!/usr/local/bin/perl --
require 'config.cgi';
require 'lib/_write_tag.cgi';
&get_data;

$this_title  = "tobaku��";
$this_file   = "$logdir/casino_room";
$this_script = 'casino_room.cgi';

#=================================================
&run;
&footer;
exit;

# �A���������݋֎~����(�b)
$bad_time = 5;

# �ő�۸ޕۑ�����
$max_log = 60;

# �ő���Đ�(���p)
$max_comment = 200;

# ���ް�ɕ\������鎞��(�b)
$limit_member_time = 60 * 5;

#================================================
sub run {
    &write_comment if ($in{mode} eq "write") && $in{comment};
    my ($member_c, $member) = &get_member;

    print qq|<form method="$method" action="$script">|;
    print
        qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
    print qq|<input type="submit" value="�߂�" class="button1"></form>|;
    print qq|<h2>$this_title</h2>|;
    &print_state;
    &print_buttons;
    print qq|<form method="$method" action="$this_script" name="form">|;
    print
        qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
    print
        qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
    print qq|<input type="submit" value="����" class="button_s"><br>|;

    print qq|</form><font size="2">$member_c�l:$member</font><hr>|;

    open my $fh, "< $this_file.cgi"
        or &error("$this_file.cgi ̧�ق��J���܂���");
    while (my $line = <$fh>) {
        my ($btime, $bdate, $bname, $bcountry, $bshogo, $baddr, $bcomment,
            $bicon)
            = split /<>/, $line;
        $bname .= "[$bshogo]" if $bshogo;
        print
            qq|$bname�F$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
    }
    close $fh;
}

#================================================
# chat�pheader
#================================================
sub header {
    print qq|Content-type: text/html; charset=shift_jis\n\n|;
    print qq|<html><head>|;
    print qq|<meta http-equiv="Cache-Control" content="no-cache">|;
    print qq|<title>$title</title>|;

    if ($is_mobile) {
        print qq|</head><body $body><a name="top"></a>|;
    }
    else {
        print <<"EOM";
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<link rel="stylesheet" type="text/css" href="$htmldir/bj.css">

<script language="JavaScript">
<!--
function textset(text){
	document.form.comment.value = document.form.comment.value + text;
}
function textfocus() {
	document.form.comment.focus();
	return true;
}
-->
</script>
</head>
<body $body onLoad="return textfocus()">
EOM
    }
}

#=================================================
# �������ݏ���
#=================================================
sub write_comment {
    &error('�{���ɉ���������Ă��܂���') if $in{comment} eq '';
    &error("�{�����������܂�(���p$max_comment�����܂�)")
        if length $in{comment} > $max_comment;

    my @lines = ();
    open my $fh, "+< $this_file.cgi"
        or &error("$this_file.cgi ̧�ق��J���܂���");
    eval { flock $fh, 2; };

	my $mname;
	($mname, $in{comment}) = &write_change($m{name}, $in{comment}, 1);
	
    my $head_line = <$fh>;
    my ($htime, $hname, $hcomment) = (split /<>/, $head_line)[0, 2, 6];
    my ($btime, $bdate, $bname, $bcountry, $bshogo, $baddr, $bcomment, $bicon)
        = split /<>/, $line;
    return 0 if $in{comment} eq $hcomment;
    if ($hname eq $m{name} && $htime + $bad_time > $time) {
        &error(
            "�A�����e�͋֎~���Ă��܂��B<br>���΂炭�҂��Ă��珑������ł�������"
        );
    }
    push @lines, $head_line;

    while (my $line = <$fh>) {
        push @lines, $line;
        last if @lines >= $max_log - 1;
    }
	my $mshogo = length($m{shogo}) > 16 ? substr($m{shogo}, 0, 16) : $m{shogo};
    unshift @lines, "$time<>$date<>$mname<>$m{country}<>$mshogo<>$addr<>$in{comment}<>$m{icon}<>\n";
    seek $fh, 0, 0;
    truncate $fh, 0;
    print $fh @lines;
    close $fh;
    return 1;
}

#=================================================
# ���ް�擾
#=================================================
sub get_member {
    my $is_find = 0;
    my $member  = '';
    my @members = ();
    my %sames   = ();

    open my $fh, "+< ${this_file}_member.cgi"
        or &error('���ް̧�ق��J���܂���');
    eval { flock $fh, 2; };
    while (my $line = <$fh>) {
        my ($mtime, $mname, $maddr) = split /<>/, $line;
        next if $time - $limit_member_time > $mtime;
        next if $sames{$mname}++;                      # �����l�Ȃ玟

        if ($mname eq $m{name}) {
            push @members, "$time<>$m{name}<>$addr<>\n";
            $is_find = 1;
        }
        else {
            push @members, $line;
        }
        $member .= "$mname,";
    }
    unless ($is_find) {
        push @members, "$time<>$m{name}<>$addr<>\n";
        $member .= "$m{name},";
    }
    seek $fh, 0, 0;
    truncate $fh, 0;
    print $fh @members;
    close $fh;

    my $member_c = @members;

    return ($member_c, $member);
}

sub print_state {

}

sub print_buttons {

}

1;    # �폜�s��
