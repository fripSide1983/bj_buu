#================================================
# �ݒ�ύX
#================================================

#=================================================
sub begin {
	$layout = 2;
	if ($m{tp} > 1) {
		$mes .= '���ɉ������܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= '�l�ݒ��ύX���܂�<br>';
	}

	$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="cmd" value="1">|;
	$mes .= '�����̎��V���b�t�������H<br>';
	$mes .= $m{shuffle} ? qq|<input type="radio" name="shuffle" value="0">�͂� <input type="radio" name="shuffle" value="1" checked>������ <br>|:
						qq|<input type="radio" name="shuffle" value="0" checked>�͂� <input type="radio" name="shuffle" value="1">������<br>|;

	$mes .= '�ΐl���ɂ�\������H<br>';
	$mes .= $m{disp_casino} ? qq|<input type="radio" name="disp_casino" value="1" checked>�͂� <input type="radio" name="disp_casino" value="0">������<br>|:
						qq|<input type="radio" name="disp_casino" value="1">�͂� <input type="radio" name="disp_casino" value="0" checked>������<br>|;

	$mes .= '�𗬍L���JAVA�\���ɂ���H<br>';
	$mes .= $m{chat_java} ? qq|<input type="radio" name="chat_java" value="1" checked>�͂� <input type="radio" name="chat_java" value="0">������<br>|:
						qq|<input type="radio" name="chat_java" value="1">�͂� <input type="radio" name="chat_java" value="0" checked>������<br>|;

	$mes .= 'TOP��\������H<br>';
	$mes .= $m{disp_top} ? qq|<input type="radio" name="disp_top" value="1" checked>�͂� <input type="radio" name="disp_top" value="0">������<br>|:
						qq|<input type="radio" name="disp_top" value="1">�͂� <input type="radio" name="disp_top" value="0" checked>������<br>|;

	$mes .= '�ߋ��̉h����\������H<br>';
	$mes .= $m{disp_news} ? qq|<input type="radio" name="disp_news" value="1" checked>�͂� <input type="radio" name="disp_news" value="0">������<br>|:
						qq|<input type="radio" name="disp_news" value="1">�͂� <input type="radio" name="disp_news" value="0" checked>������<br>|;

	$mes .= '�𗬍L���\������H<br>';
	$mes .= $m{disp_chat} ? qq|<input type="radio" name="disp_chat" value="1" checked>�͂� <input type="radio" name="disp_chat" value="0">������<br>|:
						qq|<input type="radio" name="disp_chat" value="1">�͂� <input type="radio" name="disp_chat" value="0" checked>������<br>|;

	$mes .= '��`����\������H<br>';
	$mes .= $m{disp_ad} ? qq|<input type="radio" name="disp_ad" value="1" checked>�͂� <input type="radio" name="disp_ad" value="0">������<br>|:
						qq|<input type="radio" name="disp_ad" value="1">�͂� <input type="radio" name="disp_ad" value="0" checked>������<br>|;

	$mes .= '��\�]�c���\������H<br>';
	$mes .= $m{disp_daihyo} ? qq|<input type="radio" name="disp_daihyo" value="1" checked>�͂� <input type="radio" name="disp_daihyo" value="0">������<br>|:
						qq|<input type="radio" name="disp_daihyo" value="1">�͂� <input type="radio" name="disp_daihyo" value="0" checked>������<br>|;

	$mes .= '�����������Ŏ󂯎��H<br>';
	$mes .= $m{salary_switch} ? qq|<input type="radio" name="salary_switch" value="0">�͂� <input type="radio" name="salary_switch" value="1" checked>������<br>|:
						qq|<input type="radio" name="salary_switch" value="0" checked>�͂� <input type="radio" name="salary_switch" value="1">������<br>|;

	$mes .= '�{�X�������H<br>';
	$mes .= $m{no_boss} ? qq|<input type="radio" name="no_boss" value="1" checked>�͂� <input type="radio" name="no_boss" value="0">������<br>|:
						qq|<input type="radio" name="no_boss" value="1">�͂� <input type="radio" name="no_boss" value="0" checked>������<br>|;

	$mes .= '�z���X�C�b�`������H<br>';
	$mes .= $m{incubation_switch} ? qq|<input type="radio" name="incubation_switch" value="1" checked>�͂� <input type="radio" name="incubation_switch" value="0">������<br>|:
						qq|<input type="radio" name="incubation_switch" value="1">�͂� <input type="radio" name="incubation_switch" value="0" checked>������<br>|;

	$mes .= '�K�`�����̎c�莞�Ԃ�\������H<br>';
	$mes .= $m{disp_gacha_time} ? qq|<input type="radio" name="disp_gacha_time" value="1" checked>�͂� <input type="radio" name="disp_gacha_time" value="0">������<br>|:
						qq|<input type="radio" name="disp_gacha_time" value="1">�͂� <input type="radio" name="disp_gacha_time" value="0" checked>������<br>|;

	$mes .= '�u���b�N���X�g��L���ɂ���H<br>';
	$mes .= $m{valid_blacklist} ? qq|<input type="radio" name="valid_blacklist" value="1" checked>�͂� <input type="radio" name="valid_blacklist" value="0">������<br>|:
						qq|<input type="radio" name="valid_blacklist" value="1">�͂� <input type="radio" name="valid_blacklist" value="0" checked>������<br>|;

	$mes .= '�푈�Őw�`��I�ԁH<br>';
	$mes .= $m{war_select_switch} ? qq|<input type="radio" name="war_select_switch" value="1" checked>�͂� <input type="radio" name="war_select_switch" value="0">������<br>|:
						qq|<input type="radio" name="war_select_switch" value="1">�͂� <input type="radio" name="war_select_switch" value="0" checked>������<br>|;

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="�ύX" class="button1"></form>|;
		
	&menu('��߂�');
}
sub tp_1 {
	return if &is_ng_cmd(1);
	
	$m{tp} = 100;
	&{ 'tp_' .$m{tp} };
}


#=================================================
# �ύX
#=================================================
sub tp_100 {
	$m{shuffle} = $in{shuffle};	
	$m{disp_casino} = $in{disp_casino};
	$m{chat_java} = $in{chat_java};
	$m{disp_top} = $in{disp_top};
	$m{disp_news} = $in{disp_news};
	$m{disp_chat} = $in{disp_chat};
	$m{disp_ad} = $in{disp_ad};
	$m{disp_daihyo} = $in{disp_daihyo};
	$m{salary_switch} = $in{salary_switch};
	$m{no_boss} = $in{no_boss};
	$m{incubation_switch} = $in{incubation_switch};
	$m{disp_gacha_time} = $in{disp_gacha_time};
	$m{valid_blacklist} = $in{valid_blacklist};
	$m{war_select_switch} = $in{war_select_switch};

	&begin;
}

1; # �폜�s��
