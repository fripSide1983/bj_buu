#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# �����f���� Created by Merino
#=================================================
&get_data;
&error("$cs{name}[0]�̕��͂����p�ł��܂���") if $m{country} eq '0';
&error("���̍��Ɠ�����g��ł��܂���") unless $union;
&error("�S�����͓�����c���ɂ͓���܂���") if $m{lib} eq 'prison';
my $u = &union($m{country}, $union);

$this_title  = "$cs{name}[$m{country}]+$cs{name}[$union] ������c��";
$this_file   = "$logdir/union/$u";
$this_script = 'bbs_union.cgi';

#=================================================
&run;
&footer;
exit;
