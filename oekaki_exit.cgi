#!/usr/local/bin/perl --
require './lib/system.cgi';
#================================================
# ���G�`���㏈��(url_exit) Created by Merino
#================================================
&decode;

my $name = pack 'H*', $in{id};

my $image_type = -f "./user/$in{id}/picture/_$in{time}.png" ? 'png' : 'jpeg';
$mes .= qq|<img src="./user/$in{id}/picture/_$in{time}.$image_type"><br>�G��$name��ϲ�߸���ɕۑ����܂���<br>|;
require 'bj.cgi';
exit;

