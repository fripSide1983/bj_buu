#!/usr/local/bin/perl --
require 'config.cgi';
#require './lib/chat.cgi';
require './lib/bbs.cgi';
#=================================================
# €ΚΑ¬―Δ Created by Merino
#=================================================
&get_data;

$this_file   = "$logdir/chat_admin";
$this_title  = "^cc_κ";
$this_script = 'chat_admin.cgi';

#&header2;
#=================================================
&run;
&footer;
exit;
