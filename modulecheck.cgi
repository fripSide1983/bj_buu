#! /usr/local/bin/perl -I./lib
#
# modcheck.cgi
# Perl module check program
# List all Perl modules installed in the server and display them and
# their versions
# Version numbers only display when the packages use $VERSION in it.
#
# �T�[�o�[�ɃC���X�g�[������Ă���Perl�̃��W���[�����`�F�b�N����v���O����
# modcheck.cgi���T�[�o�[�ɃC���X�g�[�����A�u���E�U�ŕ\������ƃ��W���[����
# �t�@�C�����A�p�b�P�[�W���A�o�[�W�����̃��X�g���\������܂��B
# �o�[�W�����́A$VERSION��Package���Ŏg���Ă���ꍇ�̂ݕ\������܂��B
#
# 1.001 : 2/15/08 : Added dummy mode
# 1.0 : 1/27/08 : Created
#
# http://www.hidekik.com/
# Copyright(c) 2008, Hideki Kanayama All Rights Reserved

use strict;
use CGI::Carp qw(fatalsToBrowser);
use File::Find;

# If include path name into displaying file name, set 1.
# If display only file name, set 0.
# �\���t�@�C�����Ƀp�X�����܂ޏꍇ�́A1, �t�@�C�����݂̂̏ꍇ�́A0�B
my $include_path = 0;

# �T�[�o�[�̕��S�����炷���߂Ɏ��ۂ̃��W���[�������������Ƀ_�~�[��html��\�����郂�[�h
my $dummy_mode = 0;

# �_�~�[���[�h��html�t�@�C��
my $dummy_html = "modcheck_disp.html";

if ($dummy_mode){
    print "Content-Type: text/html\n\n";
    if (open(HTML, "< $dummy_html")){
	while (<HTML>){
	    print;
	}
	close(HTML);
    } else {
	print "�_�~�[HTML�t�@�C��$dummy_html���I�[�v���ł��܂���B\n";
    }
    exit;
}

my $version = "1.0";
my $lastupdatedyear = "2008";
my $mysite = 'http://www.hidekik.com/';

print <<END;
Content-Type: text/html

<html>
<head>
<title>Perl modules</title>
</head>
<body>
<center>
<a href="modcheck.html">Back</a>
<p>
Perl Version : $]<br>
OS Version : $^O<p>
<table cols=4 width=50% border=1>
<tr>
    <th>&nbsp;</th>
<th>File name</th>
<th>Package name</th>
<th>Versoin</th>
</tr>
END

    my @modules;
my $count = 1;

find (\&wanted, @INC);


print <<END;
</table>
</center>
<div align=\"right\"><i>modcheck.cgi $version<br>Copyright(c) $lastupdatedyear, <a href=\"$mysite\" target=\"_blank\">hidekik.com</a></i></div>
<body>
</html>
END

sub wanted {
    my $pmname = $File::Find::name;
    my $pm = $_;
    if ($pmname =~ /\.pm$/){
	if (open (MOD, "< $pmname")){
	    print "<tr align=center>\n";
	    my $hit = 0;
	    my $file = $include_path ? $pmname : $pm;
	    print "<td nowrap>$count</td>\n<td nowrap>$file</td>\n";
	    while (<MOD>){
		if ($hit == 0 and /^\s*package\s+(\S+)\s*;/){
		    print "<td nowrap>$1</td>\n";
		    $hit = 1;
		} elsif ($hit and /VERSION\s*=\s*[\'\"]?\s*([\d\.\w]+)\s*[\'\"]?\s*;/){
		    print "<td nowrap>$1</td>\n";
		    last;
		}
	    }
	    close(MOD);
	    print "</tr>\n";
	}
	$count++;
    }
}

