#!/usr/local/bin/perl --
require 'config.cgi';
#================================================
# �Δ� Created by Merino
#================================================

# �\���������(./log/legend/�ɂ������)�@�ǉ��폜���בւ��\
my @files = (
#	['����',				'۸�̧�ٖ�'],
	['���̑嗤�e��',		'touitu'	],
	['���i���̏؁�',		'comp_shogo'],
	['���Ͻ��',				'comp_skill'],
	['�����Ͻ��',			'comp_wea'	],
	['��ϰϽ��',			'comp_gua'	],
	['����Ͻ��',			'comp_egg'	],
	['�߯�Ͻ��',			'comp_pet'	],
	['�����֗�㋭����',	'champ_0'	],
	['�޷�Ű��㋭����',	'champ_1'	],
	['����ݗ�㋭����',		'champ_2'	],
	['ϼ޼�ݗ�㋭����',	'champ_3'	],
	['�ټެ���㋭����',	'champ_4'	],
	['����ߵݗ�㋭����',	'champ_5'	],
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
		print qq|<form action="$script_index"><input type="submit" value="�s�n�o" class="button1"></form>|;
	}

	for my $i (0 .. $#files) {
		next unless -s "$logdir/legend/$files[$i][1].cgi";
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?id=$in{id}&pass=$in{pass}&no=$i">$files[$i][0]</a> / |;
	}

	print qq|<hr><h1>$files[$in{no}][0]</h1><hr>|;
	
	open my $fh, "< $logdir/legend/$files[$in{no}][1].cgi" or &error("$logdir/legend/$files[$in{no}][1].cgi̧�ق��ǂݍ��߂܂���");
	print qq|<li>$_</li><hr>\n| while <$fh>;
	close $fh;
}
