#!/usr/local/bin/perl --
require 'config.cgi';
require "$datadir/profile.cgi";
#================================================
# 戦歴表示 Created by Merino
#================================================
&decode;
&header;
&header_profile;
&run;
&footer;
exit;
#================================================
sub run {
	open my $fh, "< $userdir/$in{id}/memory.cgi" or &error("$userdir/$in{id}/memory.cgiﾌｧｲﾙが読み込めません");
	print qq|<li>$_</li><hr size="1">\n| while <$fh>;
	close $fh;
}
