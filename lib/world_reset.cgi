#================================================
# ���E��⍑�ް���ؾ�ĂŎg���郂�W���[��
# �Ղ��Ɋւ�����̂��������S�̓I�ɂ����ƃV���v���ɂł������Ȃ̂� world_reset �Ƃ��Ă���
#================================================

# �Ղ��̊J�n�ƏI���ɕR�Â��̂� 1 ���󂯂�
use constant FESTIVAL_TYPE => {
	'kouhaku' => 1,
	'sangokusi' => 3,
	'konran' => 5,
	'sessoku' => 7,
	'dokuritu' => 9
};

# �Ղ��̖��̂ƁA�J�n���Ȃ� 1 �I���� �Ȃ� 0 ���w�肷��
sub festival_type {
	my ($festival_name, $is_start) = @_;
	return FESTIVAL_TYPE->{$festival_name} + $is_start;
}

1;