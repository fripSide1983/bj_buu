#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require './lib/bbs2.cgi';
#=================================================
# ��`�p�f���� Created by Merino
#=================================================
&get_data;

$this_title  = "�L���Ŕ�";
$this_file   = "$logdir/bbs_ad2";
$this_script = 'bbs_ad2.cgi';
$this_sub_title = "�A�C�e���̌�����W�Ȃ�";

#=================================================
&run;
&footer;
exit;
