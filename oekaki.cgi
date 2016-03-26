#!/usr/local/bin/perl --
require 'config.cgi';
require "$datadir/header_myroom.cgi";
#================================================
# ���G�`��CGI(PC��p) Created by Merino
#================================================
# �y������ Shi-dow�zhttp://shichan.jp/ ����
# �EPaintBBS���޳�۰�ނ��āuPaintBBS.jar�v�𓯊K�w�ɒu���Ă�
# �E�����y�C���^�[�ʏ�(sptr1114.zip)���޳�۰�ނ��āuspainter.jar�Ares(�t�H���_)�v�𓯊K�w�ɒu���Ă�

# �摜�̉���
my $image_width = 48;

# �摜�̏c��
my $image_height = 48;

# ���G�`������ ���ǉ�/�ύX/�폜/���ъ����\
# ��ԏ�̂��̂���̫�ĂɂȂ�܂�
# �g�������Ȃ����G�`���͐擪��(#������ƑI���ł��Ȃ��Ȃ�܂�)
# ------------------
# �၄Paint BBS�����ɂ������ꍇ
# ['paint_bbs',		'Paint BBS'],
# #['shi_painter',		'�����y�C���^�['],
# #['shi_painter_pro',	'�����y�C���^�[Pro'],
# ------------------
my @types = (
	# ���ٰ�ݖ�,		'����'
	['paint_bbs',		'Paint BBS'],
	['shi_painter',		'�����y�C���^�['],
	['shi_painter_pro',	'�����y�C���^�[Pro'],
);

# ��̫�Ă̏o��(0:JPEG,1:PNG)
$in{is_wish_png} ||= 0;


# ----------------------------
# �r�炵/�蔲���΍�

# �摜�쐬���̍Œᱸ��ݐ�
my $security_click = 10;

# �摜�쐬���̍Œ᎞��(�b)
my $security_timer = 20;


#================================================
&decode;
&header;
&read_user;

my $goods_c = &my_goods_count("$userdir/$id/picture");
&error("$max_my_picture�ȏ�G�����L���邱�Ƃ��ł��܂���") if $goods_c >= $max_my_picture + $m{sedai} * 3;

$in{type} ||= 0;
$in{type} = 0 if $in{type} !~ /\d/ || $in{type} < 0 || $in{type} > $#types;
my $image_size = 1;

&header_myroom;
&run;
&footer;
exit;

#================================================
sub run {
	for my $i (0..$#types) {
		print $in{type} eq $i && !$in{is_wish_png} ? qq|$types[$i][1](JPEG) / | : qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=$i&is_wish_png=0">$types[$i][1](JPEG)</a> / |;
		print $in{type} eq $i &&  $in{is_wish_png} ? qq|$types[$i][1](PNG) / | : qq|<a href="?id=$id&pass=$pass&no=$in{no}&type=$i&is_wish_png=1">$types[$i][1](PNG)</a> / |;
	}
	
	my $sub_title = '(JPEG�o��)';
	if (!$is_force_jpeg && $in{is_wish_png}) {
		$image_size = 60;
		print qq|<p>��{��PNG�ŏo�͂���܂����A���k�̊֌W�ɂ��H��JPEG�ɂȂ�ꍇ������܂��B</p>|;
		$sub_title = '(PNG�o��)';
	}
	print qq|<h3>$types[$in{type}][1] $sub_title</h3>|;

	&{ $types[$in{type}][0] };
	&_common_param;
	&read_me;
}


#================================================
# ����param
#================================================
sub _common_param {
	print <<"EOM";
	<param name="image_width" value="$image_width">
	<param name="image_height" value="$image_height">
	<param name="image_size" value="$image_size">
	<param name="image_jpeg" value="true">
	<param name="image_bkcolor" value="#ffffff">

	<param name="compress_level" value="15">
	<param name="undo" value="60">
	<param name="undo_in_mg" value="15">
	<param name="scriptable" value="true">	

	<param name="color_text"value="#505078">
	<param name="color_bk" value="#9999bb">
	<param name="color_bk2" value="#8888aa">
	<param name="color_icon" value="#ccccff">

	<param name="color_bar" value="#6f6fae">
	<param name="color_bar_hl" value="#ffffff">
	<param name="color_bar_frame_hl" value="#eeeeff">
	<param name="color_bar_frame_shadow" value="#aaaaaa">

	<param name="send_language" value="sjis">
	<param name="send_advance" value="true">
	<param name="send_header" value="id=$id&pass=$pass&time=$time;">
	<param name="send_header_image_type" value="true">

	<param name="security_click" value="$security_click">
	<param name="security_timer" value="$security_timer">
	<param name="security_url" value="$htmldir/security_url.html">
	<param name="security_post" value="false">
	<param name="url_save" value="oekaki_save.cgi">
	<param name="url_exit" value="oekaki_exit.cgi?id=$id&pass=$pass&time=$time">
</applet>
EOM
}

#================================================
# Paint BBS param
#================================================
sub paint_bbs {
	print <<"EOM";
<applet code="pbbs.PaintBBS.class" name="paintbbs" archive="PaintBBS.jar" width="90%" height="90%" align="center" MAYSCRIPT>
	<param name="bar_size" value="20">
	<param name="tool_advance" value="true">
	<param name="poo" value="false">
	
	<param name="thumbnail_width" value="100%">
	<param name="thumbnail_height" value="100%">
EOM
}


#================================================
# �����y�C���^�[ param
#================================================
sub shi_painter {
	print <<"EOM";
<applet code="c.ShiPainter.class" name="paintbbs" archive="spainter.jar,res/normal.zip" width="90%" height="90%" MAYSCRIPT>
	<param name="MAYSCRIPT" value="true">
	
	<param name="dir_resource" value="./res/">
	<param name="tt.zip" value="./res/tt.zip">
	<param name="res.zip" value="./res/res_normal.zip">
	<param name="tools" value="normal">
	<param name="layer_count" value="3">
	<param name="quality" value="1">

	<param name="tool_color_bk" value="#aabbcc">
	<param name="tool_color_button" value="#ddeeff">
	<param name="tool_color_button_hl" value="#9900ff">
	<param name="tool_color_button_dk" value="#ff0099">
	
	<param name="tool_color_button2" value="#ffffff">
	<param name="tool_color_text" value="0">
	<param name="tool_color_bar" value="#00ff00">
	<param name="tool_color_frame" value="#ff0000">
EOM
	&_common_param_shi;
}

#================================================
# �����y�C���^�[Pro param
#================================================
sub shi_painter_pro {
	print <<"EOM";
<applet code="c.ShiPainter.class" name="paintbbs" archive="spainter.jar,res/pro.zip" WIDTH="90%" height="100%">
	<param name="dir_resource" value="./res/">
	<param name="tt.zip" value="./res/tt.zip">
	<param name="res.zip" value="./res/res_pro.zip">
	<param name="tools" value="pro">
	<param name="layer_count" value="3">
	<param name="quality" value="2">
EOM
	&_common_param_shi;
}


#================================================
# �����y�C���^�[����param
#================================================
sub _common_param_shi {
	print <<"EOM";
	<param name="color_frame" value="0xff">
	<param name="color_iconselect" value="#112233">
	<param name="color_bar_shadow" value="#778899"> 

	<param name="pro_menu_color_text" value="#FFFFFF">
	<param name="pro_menu_color_off" value="#222233">
	<param name="pro_menu_color_off_hl" value="#333344">
	<param name="pro_menu_color_off_dk" value="0">
	<param name="pro_menu_color_on" value="#ff0000">
	<param name="pro_menu_color_on_hl" value="#ff8888">
	<param name="pro_menu_color_on_dk" value="#660000">
	
	<param name="bar_color_bk" value="#ffffff">
	<param name="bar_color_frame" value="#ffffff">
	<param name="bar_color_off" value="#ffffff">
	<param name="bar_color_off_hl" value="#ffffff">
	<param name="bar_color_off_dk" value="#ffffff">
	<param name="bar_color_on" value="#777777">
	<param name="bar_color_on_hl" value="#ffffff">
	<param name="bar_color_on_dk" value="#ffffff">
	<param name="bar_color_text" value="0">
	
	<!--�E�C���h�E�֌W�̐ݒ�-->
	<param name="window_color_text" value="#ff0000">
	<param name="window_color_frame" value="#ffff00">
	<param name="window_color_bk" value="#000000">
	<param name="window_color_bar" value="#777777">
	<param name="window_color_bar_hl" value="#888888">
	<param name="window_color_bar_text" value="#000000">
	
	<!--�m�F�E�C���h�E�̐ݒ�-->
	<param name="dlg_color_bk" value="#ccccff">
	<param name="dlg_color_text" value="0">
	
	<!--�A�v���b�g�̔w�i�̐ݒ�-->
	<param name=color_bk value="#9999CC">
	<param name=color_bk2 value="#888888">
	
	<!--���C���[�̃��[�^�[�J���[�̐ݒ�-->
	<param name=l_m_color value="#ffffff">
	<param name=l_m_color_text value="#0000ff">
EOM
}


sub read_me {
	print <<"EOM";
<table cellpadding="2" cellspacing="2" border="0">
<tbody>
	<tr valign="Top">
		<td valign="Top">
		
		<div class="mes">
		<div align="center">���ӎ���</div>
		<ul>
			<li>�쐬�����摜�ɂ��ẮA���쌠�E�ё������ɂ��Ė@�ߏ�̋`���ɏ]���A<br>�쐬�����v���C���[�̎��ȐӔC�ɂ����ēo�^�E�f�ڂ������̂Ƃ��܂��B
			<li>�킢���ȕ\\���A���ʓI�ȕ\\���A�c�s�I�ȕ\\���ȂǁA�����̈�ʏ펯����O�ꂽ���e�͎��l���Ă��������B
			<li>�^�}�E�X��_�b�N�A�Q�[��KH�̃L�����N�^�[�Ȃǂ͒��쌠���������̂Œ��ӁI
		</ul>
		</div><br>

		<div style="color:#00CC00">�~�X���ăy�[�W��ς�����E�C���h�E�������Ă��܂����肵���ꍇ�͗������ē����L�����o�X�̕���<br>
		�ҏW�y�[�W���J���Ȃ����Ă݂ĉ������B���͎c���Ă��܂��B<br>
		�iWinIE��l�X�P6.1�̒Z�k�N���@�\\���g���Ȃ��u���E�U�͕���Ə����܂��j<br><br></div>

			<div style="color: rgb(0,102,0); ">��{�̓���(���炭���ꂾ���͊o���Ă����������ǂ��@�\\)</div>
			
			<div style="font-size: 80%; ">
				<span style="color: rgb(80,144,120); ">&lt;��{&gt;</span><br>
				
				PaintBBS�ł͉E�N���b�N,ctrl+�N���b�N,alt+�N���b�N�͓�����������܂��B<br>
				��{�I�ɑ���͈��̃N���b�N���E�N���b�N�œ��삪�������܂��B(�x�W�G��R�s�[�g�p��������)<br>
				<br>
				
				<span style="color: rgb(80,144,120); ">&lt;�c�[���o�[&gt;</span><br>
				�c�[���o�[�̖w�ǂ̃{�^���͕�����N���b�N���ċ@�\\��؂�ւ��鎖���o���܂��B<br>
				�E�N���b�N�ŋt����B���̑��p���b�g�̐F,�}�X�N�̐F,�ꎚ�ۑ��c�[���Ɍ��݂̏�Ԃ�o�^,<BR>
				���C���\\����\\���؂�ւ����S�ĉE�N���b�N�ł��B<br>
				�t�ɃN���b�N�Ńp���b�g�̐F�ƈꎞ�ۑ��c�[���ɕۑ����Ă�������Ԃ����o���܂��B<br>
				<br>
				
				<span style="color: rgb(80,144,120); ">&lt;�L�����o�X����&gt;</span><br>
				�E�N���b�N�ŐF���X�|�C�g���܂�<br>
				�x�W�G��R�s�[���̏����̓r���ŉE�N���b�N�������ƃ��Z�b�g���܂��B
			</div>
			
			<br>
			
			<div style="color: rgb(0,102,0); ">���ꓮ��(�g���K�v�͖����������Ε֗��ȋ@�\\)</div>
				
				<div style="font-size: 80%; ">
					<span style="color: rgb(80,144,120); ">&lt;�c�[���o�[&gt;</span><br>
					
				�l��ύX����o�[�̓h���b�O���o�[�̊O�ɏo�����ꍇ�ω����ɂ₩�ɂȂ�܂��̂�<br>
				����𗘗p���čׂ����ύX���鎖���o���܂��B<br>
				�p���b�g��Shift+�N���b�N�ŐF���f�t�H���g�̏�Ԃɖ߂��܂��B<br><br>
				<span style="color: rgb(80,144,120); ">&lt;�L�[�{�[�h�̃V���[�g�J�b�g&gt;</span>
				<br>
				+�Ŋg��-�ŏk���B <br>
				Ctrl+Z��Ctrl+U�Ō��ɖ߂��ACtrl+Alt+Z��Ctrl+Y�ł�蒼���B<br>
				Esc�ŃR�s�[��x�W�G�̃��Z�b�g�B�i�E�N���b�N�ł������j <br>
				�X�y�[�X�L�[�������Ȃ���L�����o�X���h���b�O����ƃX�N���[���̎��R�ړ��B<br>
				Ctrl+Alt+�h���b�O�Ő��̕���ύX�B<br><br>
				<span style="color: rgb(80,144,120);">&lt;�R�s�[�c�[���̓���ȗ��p���@&gt;</span>
				<br>
				���C���[�Ԃ̈ړ��͌����_�ł̓R�s�[�ƃ��C���[�����݂̂ł��B�R�s�[�ł̈ړ����@�́A<br>
				�܂��ړ����������C����̒����`��I����A�ړ������������C����I����ɒʏ�̃R�s�[�̍�Ƃ�<br>
				�����܂��B�������鎖�ɂ�背�C���Ԃ̈ړ����\\�ɂȂ�܂��B<br>
				
			</div>
				<br>
			
			<div style="color: rgb(0,102,0); ">�c�[���o�[�̃{�^���Ɠ���ȋ@�\\�̊ȒP�Ȑ���</div>
			<div style="font-size: 80%; ">

			<ul type="Circle">
				<li>�y����(�ʏ�y��,���ʃy��,�e�L�X�g)<br><span style="color: #CCFFFF; ">
						���C���̃t���[���C���n�̃y���ƃe�L�X�g</span><br><br></li>
						
				<li>�y����2(�g�[��,�ڂ���,��)<br><span style="color: #CCFFFF; ">
						����Ȍ��ʂ��o���t���[���C���n�̃y��</span><br><br></li>
						
				<li>�}�`(�~�Ⓑ���`)<br><span style="color: #CCFFFF; ">
						�����`��~���̐}�`</span><br><br></li>
						
				<li>����(�R�s�[�⃌�C���[����,���]��)<br><span style="color: #CCFFFF; ">
						�R�s�[�͈�x�I����A�h���b�O���Ĉړ��A�R�s�[������c�[���ł��B</span><br><br></li>
						
				<li>�}�X�N���[�h�w��(�ʏ�,�}�X�N,�t�}�X�N�j<br><span style="color: #CCFFFF; ">
						�}�X�N�œo�^����Ă���F��`�ʕs�ɂ��܂��B�t�}�X�N�͂��̋t�B<br>
						�ʏ�Ń}�X�N�����B�܂��E�N���b�N�Ń}�X�N�J���[�̕ύX���\\�B<br><br></span></li>
						
				<li>�����S��(�����y��,�����l�p,�S����)<BR><span style="color: #CCFFFF">
						���߃��C���[��𔒂œh��ׂ����ꍇ�A���̃��C���[�������Ȃ��Ȃ�܂��̂�<BR>
						��ʃ��C���[�̐����������ɂ͂��̃c�[���ŏ����l�ɂ��ĉ������B�S�����͂��ׂĂ𓧉߃s�N�Z����������c�[���ł��B<br>
						�S�����𗘗p����ꍇ�͂��̃c�[����I����L�����o�X���N���b�N��OK�B<br><br></span></li>
						
				<li>�`�ʕ��@�̎w��B(�菑��,����,�x�W�G�Ȑ�)<br><span style="color: #CCFFFF; ">
						�y����,�`�ʋ@�\\�w��ł͂���܂���B<br>
						�܂��K�p�����̂̓t���[���C���n�̃c�[���݂̂ł��B</span><br><br></li>
						
				<li>�J���[�p���b�g�S<br><span style="color: #CCFFFF; ">
						�N���b�N�ŐF�擾�B�E�N���b�N�ŐF�̓o�^�BShift+�N���b�N�Ńf�t�H���g�l�B</span><br><br></li>
						
				<li>RGB�o�[��alpha�o�[<br><span style="color: #CCFFFF; ">
						�ׂ����F�̕ύX�Ɠ��ߓx�̕ύX�BR�͐�,G�͗�,B�͐�,A�͓��ߓx���w���܂��B<br>
						�g�[����Alpha�o�[�Œl��ύX���鎖�Ŗ��x�̕ύX���\\�ł��B</span><br><br></li>
						
				<li>�����ύX�c�[��<br><span style="color: #CCFFFF; ">
						���ʃy����I�����ɐ�����ύX�������A�f�t�H���g�̒l��alpha�l�ɑ������܂��B</span><br><br></li>
				
				<li>���ꎞ�ۑ��c�[��<br><span style="color: #CCFFFF; ">
						�N���b�N�Ńf�[�^�擾�B�E�N���b�N�Ńf�[�^�̓o�^�B(�}�X�N�l�͓o�^���܂���)</span><br><br></li>
				
				<li>���C���[�c�[��<br><span style="color: #CCFFFF; ">
				PaintBBS�͓����ȃL�����o�X��񖇏d�˂��悤�ȍ\���ɂȂ��Ă��܂��B<br>
				�܂�������ɏ����A�F�����ɕ`���ƌ��������\\�ɂȂ�c�[���ł��B<br>
				�ʏ탌�C���[�ƌ�����ނ̕��ł��̂ŉ��M�ŕ`�����悤�Ȑ����L�b�`�����߂��܂��B<br>
				�N���b�N�Ń��C���[����ւ��B�E�N���b�N�őI������Ă��郌�C���̕\\���A��\\���؂�ւ��B</span><br><br></li>	
			</ul>
			
			</div>
			<span style="color: rgb(0,102,0); ">���e�Ɋւ��āF</span>
			<div style="font-size: 80%; ">
				�G�����������瓊�e�{�^���œ��e���܂��B<br>
				�G�̓��e�����������ꍇ�͎w�肳�ꂽURL�փW�����v���܂��B<br>
				���s�����ꍇ�͎��s�����ƕ񍐂���݂̂łǂ��ɂ���т܂���B<br>
				�P�ɏd�����������ł���ꍇ�����Ԃ�u������A�ēx���e�����݂ĉ������B<br>
				���̍ۓ�d�œ��e�����ꍇ�����邩������܂��񂪁A�����<br>
				Web�T�[�o�[��CGI���̏����ł��̂ł������炸�B
			</div>
		</td>
	</tr>
</tbody>
</table>
EOM
}

