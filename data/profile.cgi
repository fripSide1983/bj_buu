#=================================================
# ���̨�ِݒ� Created by Merino
#=================================================
# ���ǉ�/�폜/�ύX/���ёւ���
# ���̨�قŕ\��������́B���̉p���͓�������Ȃ���Ή��ł��ǂ�
@profiles = (
	['name',		'���O'],
	['sex',			'����'],
	['blood',		'���t�^'],
	['birthday',	'�a����'],
	['age',			'�N��'],
	['job',			'�E��'],
	['address',		'�Z��ł��鏊'],
	['hobby',		'�'],
	['boom',		'ϲ�ް�'],
	['site',		'���һ��'],
	['dream',		'��/�ڕW'],
	['motto',		'���E�̖�'],
	['character',	'���i�E����'],
	['like',		'�D���Ȃ���'],
	['dislike',		'�����Ȃ���'],
	['login',		'۸޲ݎ���'],
	['work',		'��Ȋ���/����'],
	['ceo',			'�N��ɂȂ�����'],
	['boast',		'����'],
	['reference',	'���̻�Ă�m������������'],
	['message',		'�����ꌾ'],
);


#=================================================
# ���̨��ͯ�ް
#=================================================
sub header_profile {
	&error('���̂悤����ڲ԰�����݂��܂���') unless -d "$userdir/$in{id}";
	print qq|<form action="$script_index"><input type="submit" value="�s�n�o" class="button1"></form>|;
	if ($is_mobile) {
		print qq|<form method="$method" action="players.cgi"><input type="submit" value="��ڲ԰�ꗗ" class="button1"></form>|
	}
	else {
		print -f "$htmldir/$in{country}.html"
			? qq|<form action="$htmldir/$in{country}.html"><input type="submit" value="��ڲ԰�ꗗ" class="button1"></form>|
			: qq|<form action="$htmldir/0.html"><input type="submit" value="��ڲ԰�ꗗ" class="button1"></form>|
			;
	}
	
	my $name = pack 'H*', $in{id};
	print qq|<h1>$name$in{title}</h1>|;
	
	print qq|<a href="profile.cgi?id=$in{id}&country=$in{country}&mode=status&title=Status">�ð��</a>/|;
	print qq|<a href="profile.cgi?id=$in{id}&country=$in{country}&mode=profile&title=Profile">���̨��</a>/| if -s "$userdir/$in{id}/profile.cgi";
	print qq|<a href="blog.cgi?id=$in{id}&country=$in{country}&title=Blog">���L</a>/| if -s "$userdir/$in{id}/blog.cgi";
	print qq|<a href="memory.cgi?id=$in{id}&country=$in{country}&title=Memory">���</a>/|;
	print qq|<hr><br>|;
}


1; # �폜�s��
