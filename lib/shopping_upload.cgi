#================================================
# upload picture
#================================================
sub begin {
	$mes .= "�߂�܂�";
	$m{pet} = 168;
	&refresh;
	&n_menu;
}

sub tp_1  {
	$mes .= "�߂�܂�";
	$m{pet} = 168;
	&refresh;
	&n_menu;
}

sub tp_100 {
	$m{tp} = 200;
	$mes .= '�َ����̔��p��<br>';
	$mes .= '�T�C�Y����(15KB�܂�)<br>';
	&menu('��߂�','�َ�������G��]��');
}

sub tp_200 {
	return if &is_ng_cmd(1);

	if ($cmd eq '1'){
	   $m{tp} = 300;
	   &{ 'tp_'. $m{tp} };
	}
	else
	{
		&refresh;
		&n_menu;
	}
}

sub tp_300 {
$layout = 2;
	$mes .= "<br>";
	$mes .= qq|<form action="upload.cgi" method="$method" enctype="multipart/form-data">|;
	$mes .= qq|<input type=file name="upfile">|;
	$mes .= qq|<input type=submit name=sub value="�ِ��E����]��">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|</form>|;
}

sub tp_400 {
#	&remove_pet if !-f "$userdir/$in{id}/upload_token.cgi";
	&remove_pet;
	&refresh;
	&n_menu;
}

1;