#!/usr/local/bin/perl --
require 'config.cgi';
#================================================
# ƭ���\�� Created by Merino
#================================================

# �\���������(./log/�ɂ������)�@�ǉ��폜���בւ��\
my @files = (
#	['����',		'۸�̧�ٖ�'],
	['�ߋ��̉h��',	'world_news',		],
	['���E�',	'world_big_news',	],
	['�������',	'send_news',		],
	['���Z��̋O��','colosseum_news',	],
	['�V����۸�',	'blog_news',		],
	['�V��G��',	'picture_news',		],
	['�V��{',		'book_news',		],
);

#================================================
&decode;
&header;
&run;
&footer;
exit;

#================================================
sub run {
	$in{no} ||= 0;
	$in{no} = 0 if $in{no} >= @files;
	
	if ($in{id} && $in{pass}) {
		print qq|<form method="$method" action="$script">|;
		print qq|<input type="hidden" name="id" value="$in{id}"><input type="hidden" name="pass" value="$in{pass}">|;
		print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index">|;
		print qq|<input type="submit" value="�s�n�o" class="button1"></form>|;
	}
	
	for my $i (0 .. $#files) {
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$files[$i][0]</a> / |;
	}
	print qq|<a href="./amida.cgi?id=$in{id}&pass=$in{pass}">���޸��</a> / |;

	print qq|<hr><h1>$files[$in{no}][0]</h1><hr>|;
	print qq|<font size="1">���摜���\\������Ă��Ȃ����̂́A���̐l��ϲ�߸������Ȃ��Ȃ������̂ł�</font><br>| if $files[$in{no}][1] eq 'picture_news';
	
	open my $fh, "< $logdir/$files[$in{no}][1].cgi" or &error("$logdir/$files[$in{no}][1].cgi̧�ق��ǂݍ��߂܂���");
	print qq|<li>$_</li><hr size="1">\n| while <$fh>;
	close $fh;
}
