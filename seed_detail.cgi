#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# �푰�ڍ�
#================================================

&decode;
&header;

my $table_class = $is_smart ? "table2" : "table1" ;

&seed_detail;

&footer;
exit;

#================================================
# �ڍ�
#================================================
sub seed_detail {
	print qq|<table class="$table_class" cellpadding="3">| unless $is_mobile;
	print qq|<tr><th>�푰��</th><th>����</th></tr>| unless $is_mobile;
	
	for my $s (keys(%seeds)) {
		next if $seeds{$s]}[0] eq '';
		
		print $is_mobile ? qq|<hr><h2>$seeds{$s]}[0]</h2><br>$seeds{$s]}[3]<br>|
			: qq|<tr><th align="left">$seeds{$s]}[0]</th></tr><tr><td>$seeds{$s]}[3]</td></tr>|;
	}
	print qq|</table>| unless $is_mobile;
}
