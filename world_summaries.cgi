#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ¢EīØ\¦ Created by nanamie
#================================================


@world_summaries = (
	# ½a
	'½a', 'Éh','v½','ŖD','\N','¬×','©','SĒ','s','ā]','[£','ÄÖ','ļN','Ią','åEE','Ą','½¼','ŗ','E°','ä','ŌĪ','Ł¬','pY','Ou','säÕV','¬',   'Ć');

#================================================
&decode;
&header;
&run;
&footer;
exit;

#================================================
sub run {
	$in{world} ||= 0;
	$in{world} = 0 if $in{world} >= @world_states;

	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="ßé" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index">|;
		print qq|<input type="submit" value="sno" class="button1"></form>|;
	}

	print qq|<h1>$world_states[$in{world}]</h1><hr>|;
	print "»ŻĢ¢EīØĶ $world_states[$in{world}] Å·B<br>";
	print "$world_summaries[$in{world}]";
}