#!/usr/local/bin/perl --
################################################
# test_browser.cgi����Ăяo�����e�X�g���s����
################################################
use CGI;
$CGI::LIST_CONTEXT_WARN = 0;
use CGI::Carp;
require "./TestFramework/TestInterface.cgi";
require "./TestFramework/TestResultBrowser.cgi";

#�t���[�����[�N�̃��[�g
my $framework_root ="./TestFramework";
#���ʏo�͗p��HTML
my $output_html = "./TestFramework/result.html";
#�߂��
my $back_to = "test_browser.cgi";

my $q = new CGI;

&init;
&run;
&end;

#������
sub init{


	#�w�b�_
	print qq|
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja-JP" xml:lang="ja-JP">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>����</title>
<link rel="stylesheet" href="$framework_root/HTML/test_browser.css">
</head>
<body>|;

	#�F��
	unless(&_is_valid_passward){
		print qq|<div id="msg_window"><p class="msg_class">invalid pass</p></div><br>|;
		print $q->end_html;
		exit;
	}
}

#���[�h�ʂɏ������s
sub run{

	my $mode = $q->param('mode');
	
	if($mode eq "save"){
		&_run_save;
	}
	elsif($mode eq "load"){
		&_run_load;
	}
	elsif($mode eq "script"){
		&_run_script;
	}
	elsif($mode eq "manual"){
		&_run_manual;
	}
}

#�Z�[�u���[�h
sub _run_save{

	#�ݒ���
	my $dir_to_save = $q->param('dir_to_save');
	unless($dir_to_save){
		print qq|dir_to_save���^�����Ă��Ȃ�<br>|;
		return;
	}

	#�e�X�g�C���^�[�t�F�[�X�N���X����
	my $result = TestResultBrowser->new($output_html);
	my $test_interface = TestInterface->new($result);

	#�Z�[�u
	$test_interface->add_save_dir("./data");
	$test_interface->add_save_dir("./log");
	$test_interface->add_save_dir("./html");
	$test_interface->add_save_dir("./user");
	$test_interface->save_data($dir_to_save);
	print qq|<div id="msg_window"><p class="msg_class">data, log, html, user�f�B���N�g����$dir_to_save�ɃZ�[�u����</p></div><br>|;
}

#���[�h���[�h
sub _run_load{

	#�ݒ���
	my $dir_to_save = $q->param('dir_to_save');
	unless($dir_to_save){
		print qq|dir_to_save���^�����Ă��Ȃ�<br>|;
		return;
	}

	#�e�X�g�C���^�[�t�F�[�X�N���X����
	my $result = TestResultBrowser->new($output_html);
	my $test_interface = TestInterface->new($result);

	#���[�h
	$test_interface->add_save_dir("./data");
	$test_interface->add_save_dir("./log");
	$test_interface->add_save_dir("./html");
	$test_interface->add_save_dir("./user");
	$test_interface->restore_data($dir_to_save);
	print qq|<div id="msg_window"><p class="msg_class">data, log, html, user�f�B���N�g����$dir_to_save�Ƀ��[�h����</p></div><br>|;
}

#�X�N���v�g���[�h
sub _run_script{

	#�ݒ���
	my @files = $q->param('file');
	unless(@files){
		print qq|<div id="msg_window"><p class="msg_class">�X�N���v�g���I������Ă��Ȃ�</p></div><br>|;
		return;
	}
	my @settings_save= $q->param('setting_save');

	#�e�X�g�C���^�[�t�F�[�X�N���X����
	my $result = TestResultBrowser->new($output_html);
	my $test_interface = TestInterface->new($result);
	
	#�ޔ��f�B���N�g���ݒ�
	for my $setting_save (@settings_save){
		$test_interface->add_save_dir($setting_save);
	}
	
	#�e�X�g���s
	$test_interface->run_all_tests(@files);
	
	#�e�X�g���ʂ��o��
	$test_interface->output_result();
	
	#����
	$test_interface->restore_data();

}

#�}�j���A�����[�h
sub _run_manual{
	print qq|<div id="msg_window"><p class="msg_class">�J����</p></div><br>|;
}

#�I������
sub end{

	#�߂�{�^������
	print qq|<form action="$back_to" method="post">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_1" name="submit" value="�߂�">|;
	print qq|</form>|;

	#�I��
	print $q->end_html();
	exit;

}

#�p�X���[�h�`�F�b�N
sub _is_valid_passward{

	require "./TestFramework/testframework_passward.pm";
	if($q->param('pass') ne $testframework_passward::passward){
		return 0;
	}
	return 1;
}
