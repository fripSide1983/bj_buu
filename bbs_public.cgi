#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/bbs.cgi';
#=================================================
# ���ʌf���� Created by Merino
#=================================================
&get_data;

$this_title  = "$title�f����";
$this_file   = "$logdir/bbs_public";
$this_script = 'bbs_public.cgi';
$this_sub_title = qq|<br>�������݌����̂���l�����������߂܂���B<br>�o�O�񍐂�<a href="letter.cgi?id=$id&pass=$pass&send_name=������������">������</a>��<br>���A�͌𗬂�|;
@writer_member = ($admin_name, $admin_sub_name, $admin_support_name);

#=================================================
&run;
&footer;
exit;
