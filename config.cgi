require './lib/system.cgi';
#================================================
$VERSION = '2.71';
# ��{�ݒ� Created by Merino
#================================================
# ���ݒ�Ǘ�����URL
# http://������URL/bj/admin_country.cgi?pass=�Ǘ����߽ܰ��
#
# ��ڲ԰�Ǘ�����URL
# http://������URL/bj/admin.cgi?pass=�Ǘ����߽ܰ��
# 
# ���u������URL�v�Ƃ͂���CGI��ݒu�����ꏊ�܂ł̱��ڽ
#================================================

# ����ݽ�\��(��) �ʏ�ғ����́u0�v
$mente_min = 0;

# �Ǘ��߽ܰ��(�K���Ȕ��p�p�����ɕK���ύX���Ă�������)
require './admin_password.cgi';

# �Ǘ��l��ڲ԰��
$admin_name = '����';

# gzip���k�]��(�킩��Ȃ��E�g��Ȃ��ꍇ�͋� '' )
$gzip = '';

# �g�ы@��ɂ��PNG����\���Ȃ̂�
# ����JPEG�o�͐ݒ�(0:PNG or JPEG, 1:JPEG�̂�) 
$is_force_jpeg = 0;

# ----------------------------
# ����
$title = 'Blind Justice';

# ���ى摜(�K�v�Ȃ��ꍇ�́u''�v)
$title_img = './html/title.jpg';

# �߂��URL
$home = 'http://buu.pandora.nu/';

# �嗤�̖��O
$world_name = 'ո�����';

# ----------------------------
# �ő�o�^�l��
$max_entry = 400;

# �ő�۸޲ݐl��
$max_login = 300;

# �ő���ڲ�l��
$max_playing = 250;

# Top��۸޲�ؽĂɕ\�����鎞��(��)
$login_min = 20;

# ----------------------------
# �@�픻�ʂɂ���߰�ނ̐؂�ւ�(0:PC�g�є��ʁA1:PC�ł��g�щ��)
# �g�ѐ�p�߰�ނɂ���ꍇ��g�щ�ʂ��m�F����ꍇ�ȂǂɁu1�v
$is_mobile = 0;
$is_smart = 0;

# �g�їpbody���
$body = 'bgcolor="#000000" text="#CCCCCC" link="#3366FF" vlink="#CC00FF" alink="#663333"';

# ----------------------------
# ��̫�Ă̱��݉摜(icon̫��ނ̒���̧�ٖ� ��> '000.gif' )
# ���݂��g��Ȃ��ꍇ�͋�('')
$default_icon = '000.gif';

# �����폜����(��)�B���̓��ɂ��𒴂��Ă�۸޲݂��Ȃ�հ�ް�͍폜
$auto_delete_day = 30;

# �����ݷݸލX�V����(��)�B�������ݸނŔ��� 0 G�̂��X�͍폜
$sales_ranking_cycle_day = 15;

# ��{�S������(��) Game Standard Wait Time
$GWT = 20;

# ���^�����炦��Ԋu(��)
$salary_hour = 6;

# �N��C������(�ްѓ��ł̔N)
$reset_ceo_cycle_year = 3;

# ��\�C������(�ްѓ��ł̔N)
$reset_daihyo_cycle_year = 5;

# ----------------------------
# �E���ɕ\������钘��\���BHTML��ގg�p�\(�u$copyright = <<"EOM";�v�`�uEOM�v�̊ԂɋL�q)
$copyright = <<"EOM";
<!-- �������� -->



<!-- �����܂� -->
EOM

# ----------------------------
# �ߋ��̉h���A�������A�莆��BBS�Ȃǂ̊�{�ݒ�(���ݒ�ύX���Ȃ��ꍇ�͈ȉ����ް��ƂȂ�)
# ----------------------------
# �ő�۸ޕۑ�����
$max_log = 50;

# ----------------------------
# �莆��BBS�Ȃǂ̊�{�ݒ�(���ݒ�ύX���Ȃ��ꍇ�͈ȉ����ް��ƂȂ�)
# ----------------------------
# �A���������݋֎~����(�b)
$bad_time    = 30;

# �ő���Đ�(���p)
$max_comment = 2000;

# ���ʂɐݒ�ύX������ꍇ�́A���������O�ɕϐ��̒l��ς���Ηǂ�(blog.cgi�ȂǎQ��)


# ----------------------------
# ���ق��Ȃ��ꍇ(���L)
$non_title = '����';

# �G�̍ő及����
$max_my_picture = 15;

# �{�̍ő及����
$max_my_book = 30;


#================================================
# ����/�r�炵�΍��ݒ�
#================================================
# �������ێ҂ւ̃��b�Z�[�W
$deny_message = '���Ȃ���IP���ڽ�ͱ����������������Ă��܂�';

# ��������ؽāu '�֎~IP���ڽ�܂���νĖ�', �v
# ���ؽ�(*)�őO����v(��> '*.proxy',)�A�����v(��> '127.0.0.*',)
@deny_lists = (
	'*.anonymizer.com',
	'p*-ipngn100105matuyama.ehime.ocn.ne.jp',
	'',
);


#================================================
# �e�t�@�C���ݒ�
#================================================
$userdir  = './user';
$icondir  = './icon';
$logdir   = './log';
$datadir  = './data';
$htmldir  = './html';

$script       = 'bj.cgi';
$script_index = 'index.cgi';

$method = 'POST';
$chmod  = 0666;


#================================================
# �g�ђ[�����ʏ���
#================================================
$agent = $ENV{HTTP_USER_AGENT};
if ($is_mobile
	|| $agent =~ /DoCoMo/  # DoCoMo
	|| $agent =~ /KDDI|UP\.Browser/  # Ez
	|| $agent =~ /J-PHONE|Vodafone|SoftBank/  # SoftBank
#	|| $agent =~ /DDIPOCKET|WILLCOM/  # AIR-HDGE PHONE
#	|| $agent =~ /ASTEL/  # �h�b�gi�[��
	|| $ENV{HTTP_X_JPHONE_MSNAME}) {
		$is_mobile = 1;
		$method  = 'GET';

		if ($ENV{HTTP_X_DCMGUID}) {
			$agent = '�ő̎��ʔԍ�'.$ENV{HTTP_X_DCMGUID}.'�@'.$agent;
		}
		elsif ($ENV{HTTP_X_UP_SUBNO}) {
			$agent = '�ő̎��ʔԍ�'.$ENV{HTTP_X_UP_SUBNO}.'�@'.$agent;
		}
		
		# ----------------------------
		# �g�ю��̖߂��URL
		$home = 'http://buu.pandora.nu';
	
		# �籲�݂��g�p���Ă���ꍇ�̱��ݻ��ޒ���
		$mobile_icon_size = q|width="25px" height="25px"|;
}

if ($is_smart
	|| $agent =~ /iPhone/i  # iPhone
	|| $agent =~ /Android/i  # Android
	) {
		$is_smart = 1;
		
		# �籲�݂��g�p���Ă���ꍇ�̱��ݻ��ޒ���
		$mobile_icon_size = q|width="25px" height="25px"|;
}


#================================================
# javascript�t�@�C���X�V�ϐ�
#================================================
$jstime = '201510311654';
1; # �폜�s��
