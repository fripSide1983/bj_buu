#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# ���ʌf���� Created by Merino
#=================================================
&get_data;
&error("$cs{name}[$w{country}]�̕��͓���܂���") unless $m{country};
&error("$cs{name}[$w{country}]�̕��͓���܂���") if $m{country} eq $w{country};
&error("NPC���Ɠ����̍��͕���R�m�c�{���ɂ͓���܂���") if $w{"p_$m{country}_$w{country}"} eq '1';
&error("�S�����͕���R�m�c�{���ɂ͓���܂���") if $m{lib} eq 'prison';

$this_title  = "����R�m�c�{��";
$this_file   = "$logdir/bbs_vs_npc";
$this_script = 'bbs_vs_npc.cgi';
$this_sub_title = "��NPC���R";

#=================================================
&run;
&footer;
exit;
