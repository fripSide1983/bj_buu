#================================================
# �����ݸ� Created by Merino
#================================================

# �ƭ� ���ǉ�/�ύX/�폜/���בւ��\
my @menus = (
	['�߂�', 		'main'],
	['�����߰��',	'shopping2'],
	['���l�̂��X',	'shopping_akindo'],
	['���̉攌��',	'shopping_akindo_picture'],
	['�ޯ�ϰ���',	'shopping_akindo_book'],
	['���l�̋�s',	'shopping_akindo_bank'],
	['��@����',	'shopping_akindo_casino'],
	['�����݉��',	'shopping_auction'],
	['�ެݸ�����',	'shopping_junk_shop'],
	['��ĉ�',	'shopping_breeder'],
	['�����޶޽',	'shopping_casino'],
	['���Ɍ�����',	'shopping_casino_exchange'],
	['���Z��',		'shopping_colosseum'],
	['���\���a�@',	'shopping_hospital'],
);

if (&on_december) {
	push @menus, ['�N�����o', 'shopping_december'];
}
#================================================
sub begin {
	$mes .= '�ǂ��ɍs���܂���?<br>';
	&menu(map { $_->[0] } @menus);
}
sub tp_1  { &b_menu(@menus); }



1; # �폜�s��
