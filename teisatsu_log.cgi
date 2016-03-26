#!/usr/local/bin/perl --
require 'config.cgi';
require './lib/_comment_tag.cgi';
#================================================
# �ߋ�۸މ{�� Created by Merino
#================================================
&get_data;
&error("���̍��̉ߋ�۸ނ͌���܂���")   if $in{this_file} =~ m|/(\d+)/| && $1 ne $m{country};
&error("���̍��̉ߋ�۸ނ͌���܂���")   if $in{this_file} =~ m|/(\d+?)_(\d+?)| && !($1 eq $m{country} || $2 eq $m{country});
&run;
&footer;
exit;

#================================================
sub run {
	print qq|<form method="$method" action="$in{this_script}.cgi">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	print qq|<h2>��@۸�$in{this_title}</h2><hr>|;

	unless(-f "$in{this_file}.cgi"){
		open my $fh, "> $in{this_file}.cgi" or &error("$in{this_file}.cgi ̧�ق��ǂݍ��߂܂���");
		close $fh;
	}
	open my $fh, "< $in{this_file}.cgi" or &error("$in{this_file}.cgi ̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bcomment = &comment_change($bcomment, 0);
		print qq|<font color="$cs{color}[$bcountry]">$bname <font size="1">($cs{name}[$bcountry] : $bdate)</font><br>$bcomment</font><hr size="1">\n|;
	}
	close $fh;
}

1; # �폜�s��
