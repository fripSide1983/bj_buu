# �Ղ��̊J�n�ƏI���ɕR�Â��̂� 1 ���󂯂�
use constant FESTIVAL_TYPE => {
	'kouhaku' => 1,
	'sanngokushi' => 3,
	'konnrann' => 5,
	'sessoku' => 7,
	'dokuritsu' => 9
};

# �Ղ��̖��̂ƁA�J�n���Ȃ� 1 �I���� �Ȃ� 0���w�肷��
sub festival_type {
	my ($festival_name, $is_start) = @_;
	return FESTIVAL_TYPE->{$festival_name} + $is_start;
}

1;
