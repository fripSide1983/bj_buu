#!/usr/local/bin/perl --

package test_browser;
use CGI::Carp;
use CGI;

#�t���[�����[�N�̃��[�g
my $framework_root = "./TestFramework";
#�t���[�����[�N�����̃e�X�g�t�H���_
my $test_root = "Tests";
#�e�X�g�����s����cgi
my $test_runner = "test_runner.cgi";
#�Z�[�u�����[�h�̃f�B���N�g��
my $dir_to_save = "$framework_root/save";


my $q = CGI->new();
&print_header;
&init;
&print_footer;




#������
sub init{

	#�p�X�`�F�b�N
	unless(&_is_valid_passward){
		print qq|<p>invalid passward</p>|;
		return 1;
	}

	#���b�Z�[�W�E�B���h�E
	print qq|<div id="msg_window">|;
	print qq|<p class="msg_class">�J����</p>|;
	print qq|</div>|;

	#�^�u����
 	print qq|
<div id="tabs">
	<ul>
        <li><a href="#tab_saveload">�Z�[�u�����[�h</a></li>
        <li><a href="#tab_script">�X�N���v�g</a></li>
        <li><a href="#tab_manual">�蓮</a></li>
   	</ul>|;
	&generate_saveload_tab;
	&generate_script_tab;
	&generate_manual_tab;
	print qq|</div>|;


}

#�Z�[�u�����[�h�p��tab����
sub generate_saveload_tab{

	print qq|<div id="tab_saveload">|;

	print qq|<form action="$test_runner" method="post">|;
	print qq|<input type="hidden" name="mode" value="save">|;
	print qq|<input type="hidden" name="dir_to_save" value="$dir_to_save">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_1" name="submit" value="�Z�[�u">|;
	print qq|</form>|;
	print qq|<form action="$test_runner" method="post">|;
	print qq|<input type="hidden" name="mode" value="load">|;
	print qq|<input type="hidden" name="dir_to_save" value="$dir_to_save">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_1" name="submit" value="���[�h">|;
	print qq|</form>|;

	print qq|</div>|;
}

#�X�N���v�g�p��tab����
sub generate_script_tab{

	print qq|<div id="tab_script">|;
	print qq|<form action="$test_runner" method="post">|;

	#�`�F�b�N�{�b�N�X�쐬
	print qq|<div id="treeList" class="content_box">|;
	print qq|<label>�X�N���v�g�I��</label>|;
	print qq|<ul>|;
	_load_tests($framework_root,$test_root);
	print qq|</ul>|;
	print qq|</div>|;

	#�ݒ�pdiv�쐬
	print qq|<div id="settingWindow" class="content_box">|;
	print qq|<label>�ݒ�I��</label>|;
	print qq|<ul>���ꂼ��̃e�X�g�O��TestFramework/save�ɑޔ������Ă��ꂼ��̃e�X�g��ɕ�������f�B���N�g��|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./log" checked="checked">log</label></li>|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./data" checked="checked">data</label></li>|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./html" checked="checked">html</label></li>|;
	print qq|<li><label><input type="checkbox" name="setting_save" value="./user" checked="checked">user</label></li>|;
	print qq|</ul>|;
	print qq|</div>|;
	print qq|<input type="hidden" name="mode" value="script">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_1" name="submit" value="���s">|;
	print qq|</form>|;
	print qq|</div>|;

}

#�蓮�ŃR���g���[������^�u
sub generate_manual_tab{

	print qq|<div id="tab_manual">|;
	print qq|<form action="$test_runner" method="post">|;
	print qq|<input type="hidden" name="mode" value="manual">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_1" name="submit" value="���s">|;
	print qq|</form>|;
	print qq|</div>|;
}

#�ċA�I�Ƀf�B���N�g����T�����`�F�b�N�{�b�N�X�����
sub _load_tests{

	my $parent_path = shift;
	my $this_dirname = shift;

	
	my $dir_name = $parent_path."/".$this_dirname;
	opendir(DIRHANDLE,$dir_name) or die ("$dir_name : $!");
	my @list = readdir DIRHANDLE;
	closedir(DIRHANDLE);
	my @dir_list;
	my @file_list;
	for my $name (@list){
		if(-f $parent_path."/".$this_dirname."/".$name){
			
			#cgi, pm, t�g���q�̂ݕ\��
			if($name =~ /\.cgi$|\.pm$|\.t$/){
				push(@file_list, $name);
			}
		}
		elsif(-d $parent_path."/".$this_dirname."/".$name){
			#�e�̃p�X�͖���
			unless($name =~ /\.$/){
				push(@dir_list, $name);
			}
		}
	}
	

	print qq|<li>|;
	#���g�̃`�F�b�N�{�b�N�X
	print qq|<label><input type="checkbox"><font color="red">$this_dirname</font></label>|;
	print qq|<ul>|;
	#�t�@�C���̃`�F�b�N�{�b�N�X
	for my $file(@file_list){
		print qq|<li>|;
		print qq|<label><input type="checkbox" name="file" value="$dir_name/$file">$file</label>|;
		print qq|</li>|;
	}

	#�q�f�B���N�g����
	for my $dir (@dir_list){
		_load_tests($dir_name, $dir);
	}
	print qq|</ul>|;
	print qq|</li>|;
	
}

#header
sub print_header{
	print qq|
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja-JP" xml:lang="ja-JP">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>Blind Justice �e�X�g�t���[�����[�N</title>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.19/jquery-ui.min.js"></script>
<script src="$framework_root/HTML/js/test_gui.js"></script>
<link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.19/themes/redmond/jquery-ui.css">
<link rel="stylesheet" href="$framework_root/HTML/test_browser.css">
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.19/i18n/jquery-ui-i18n.min.js"></script>
    <script>
        \$(function(){
	    \$( '#tabs' ) . tabs();
        });
    </script>
</head>
<body>|;
}

#footer
sub print_footer{

	print $q->end_html();

}


#�p�X���[�h�`�F�b�N
sub _is_valid_passward{

	require "./TestFramework/testframework_passward.pm";
	
	if($q->param("pass") ne $testframework_passward::passward){
		return 0;
	}
	return 1;
}
	
exit;
