#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ���E��\�� Created by nanamie
#================================================

@world_summaries = (
	# ���a
	'�I����Ԃ�������蒷���ł��B<br>'.
	'�ȉ��ȗ�',
	# �ɉh
	'�ꕔ�̍s���ɑ΂��Č��J�����Ⴆ�܂��B<br>'.
	'�ȉ��ȗ�',
	# �v��
	'�v��',
	# ���D
	'���D',
	# �\�N
	'�\�N',
	# ����
	'����',
	# ����
	'����',
	# �S��
	'�S��',
	# �s��
	'�s��',
	# ��]
	'�푈�������ɕ����t���O�������܂���B<br>'.
	'�I���ƈႢ�����A���ꍑ�͂𒴂�����ʏ�ʂ蓝��ł��܂��B<br>'.
	'�ȉ��ȗ�',
	# �[��
	'�[��',
	# �ċ�
	'�ċ�',
	# ��N
	'��N',
	# �I��
	'�I��',
	# ��E�E
	'��E�E',
	# ����
	'����',
	# ����
	'����',
	# ����
	'����',
	# �E��
	'�E��',
	# ��
	'��',
	# �ԉ�
	'�ԉ�',
	# �ّ�
	'�ّ�',
	# �p�Y
	'�p�Y',
	# �O���u
	'�O���ɕ�����ē��������܂��B<br>'.
	'�ȉ��ȗ�',
	# �s��ՓV
	'�񍑂ɕ�����ē��������܂��B<br>'.
	'�ȉ��ȗ�',
	# ����
	'�v���C���[�����������̍��ɔ�΂��ꂻ�ꂼ�ꓝ�������܂��B<br>'.
	'�ȉ��ȗ�',
	# �Í�
	'���󍑂�NPC���Ƃɕ�����ē��������܂��B<br>'.
	'�ȉ��ȗ�'
);

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
		print qq|<input type="submit" value="�߂�" class="button1"></form>|;
	}
	else {
		print qq|<form action="$script_index">|;
		print qq|<input type="submit" value="�s�n�o" class="button1"></form>|;
	}

	print "<h1>$world_states[$in{world}]</h1>";
	print "<p>�N�����������l����񂩂ˁ`</p>";
	print "$world_states[$in{world}]�́A$world_summaries[$in{world}]";
}