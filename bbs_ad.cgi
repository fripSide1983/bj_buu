#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#require './lib/bbs.cgi';
require './lib/bbs2.cgi';
#=================================================
# ι`pf¦Β Created by Merino
#=================================================
&get_data;

$this_title  = "ι`ΎΒ";
#$this_file   = "$logdir/bbs_ad";
$this_file   = "$logdir/bbs_ad2";
#$this_script = 'bbs_ad.cgi';
$this_script = 'bbs_ad2.cgi';
$this_sub_title = "±²ΓΡπ·,₯θεW,¨XΜΠξΘΗ";

#=================================================
&run;
&footer;
exit;
