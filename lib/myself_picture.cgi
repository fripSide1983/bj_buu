#================================================
# �����̍�i(�G) Created by Merino
#================================================

# ��i�Ɏg��������̫���(book,etc,music,picture)
$goods_dir = 'picture';

# ��i�̎��(img,html,cgi)
$goods_type = 'img';

# ��i�̖���
$goods_name = '�G';

# �����ł���ő吔
$max_goods = $max_my_picture + $m{sedai} * 3;

# ��`��p
$need_ad_money = 500;

# ����ɑ���Ƃ��̎萔��(����)
$need_send_money = 500;

# ����ɑ���Ƃ��̎萔��(����)
$need_send_money_other = 3000;

# ���X���ݔ�p
$build_money = 100000;

# ���X�ɂ�����ő吔
$max_shop_item = 15;



#================================================
# ��Őݒ肵�����̂�����CGI�ɓn��
require "./lib/_myself_goods.cgi";



1; # �폜�s��
