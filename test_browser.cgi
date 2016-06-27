#!/usr/local/bin/perl --

package test_browser;
use CGI::Carp;
use CGI;

#�t���[�����[�N�̃��[�g
my $framework_root = "./TestFramework";
#�t���[�����[�N�����̃X�N���v�g�t�H���_
my $test_root = "Scripts";
#�e�X�g�����s����cgi
my $test_runner = "test_runner.cgi";
#�Z�[�u�����[�h�̕ۑ���f�B���N�g��
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
        <li><a href="#tab_manual">�蓮</a></li>
        <li><a href="#tab_script">�X�N���v�g</a></li>
        <li><a href="#tab_saveload">�Z�[�u�����[�h</a></li>
   	</ul>|;
	&generate_saveload_tab;
	&generate_script_tab;
	&generate_manual_tab;
	print qq|</div>|;


}

#�Z�[�u�����[�h�p�̃^�u
sub generate_saveload_tab{

	print qq|<div id="tab_saveload">|;

	print qq|<div align="center">|;
	print qq|<form action="$test_runner" method="post">|;
	print qq|<input type="hidden" name="mode" value="save">|;
	print qq|<input type="hidden" name="dir_to_save" value="$dir_to_save">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_wide" name="submit" value="�Z�[�u">|;
	print qq|</form>|;
	print qq|<form action="$test_runner" method="post">|;
	print qq|<input type="hidden" name="mode" value="load">|;
	print qq|<input type="hidden" name="dir_to_save" value="$dir_to_save">|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="submit" class="sbt_wide" name="submit" value="���[�h">|;
	print qq|</form>|;
	print qq|</div>|;

	print qq|</div>|;
}

#�X�N���v�g�p�̃^�u
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
	print qq|<ul>���ꂼ��̃X�N���v�g�̎��s�O���TestFramework/save�ɑޔ������ĕ�������f�B���N�g��|;
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

	#���j���[����
	print qq|<div class="clearfix">|;
	print qq|<ul id="menu" class="menu_wide">|;
	print qq|  <li id="player_controller">PlayerController|;
	print qq|    <ul>|; 
	print qq|    	<li id="access_data">access_data</li>|; 
	print qq|    	<li id="create_player">create_player</li>|; 
	print qq|    	<li id="action_shikan_player">action_shikan_player</li>|; 
	print qq|    	<li id="remove_player">remove_player</li>|; 
	print qq|    	<li id="refresh_player">refresh_player</li>|; 
	print qq|    </ul>|; 
	print qq|  </li>|;
	print qq|  <li id="country_controller">CountryController|;
	print qq|    <ul>|; 
	print qq|    	<li id="access_data">access_data</li>|; 
	print qq|    	<li id="admin_add_country">admin_add_country</li>|; 
	print qq|    	<li id="admin_reset_countries">admin_reset_countries</li>|; 
	print qq|    	<li id="action_stand_candidate">action_stand_candidate</li>|; 
	print qq|    	<li id="action_vote">action_vote</li>|; 
	print qq|    </ul>|; 
	print qq|  </li>|;
	print qq|  <li id="world_controller">WorldController|;
	print qq|    <ul>|; 
	print qq|    	<li id="access_data">access_data</li>|; 
	print qq|    	<li id="evoke_disaster">evoke_disaster</li>|; 
	print qq|    </ul>|; 
	print qq|  </li>|;
	print qq|  <li id="war_controller">WarController|;
	print qq|    <ul>|; 
	print qq|    	<li id="action_set_war">action_set_war</li>|; 
	print qq|    	<li id="action_encount">action_encount</li>|; 
	print qq|    	<li id="action_step_war">action_step_war</li>|; 
	print qq|    	<li id="action_complete_war">action_complete_war</li>|; 
	print qq|    	<li id="action_win_war">action_win_war</li>|; 
	print qq|    	<li id="action_lose_war">action_lose_war</li>|; 
	print qq|    	<li id="action_draw_war_turn">action_draw_war_turn</li>|; 
	print qq|    	<li id="action_draw_war_kaimetu">action_draw_war_kaimetu</li>|; 
	print qq|    	<li id="action_after_war">action_after_war</li>|; 
	print qq|    </ul>|; 
	print qq|  </li>|;

	print qq|</ul>|;


	
	#���ꂼ��̃��j���[�̓��̓t�H�[��
	print qq|<form id="menu_form" action="$test_runner" method="post">|;
	print qq|<div id="menu_input_form" class="menu_form_class">|;
	print qq|</div>|;
	print qq|<input type="hidden" name="pass" value="|;
	print $q->param("pass");
	print qq|">|;
	print qq|<input type="hidden" name="mode" value="manual">|;
	print qq|<input type="submit" class="sbt_1" class="menu_form_class" name="submit" value="���s">|;
	print qq|</form>|;
	print qq|</div>|;#menu_top

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

	#�w�b�_
	print $q->header( -charset => 'Shift_JIS');
	print $q->start_html(
		-title => "�e�X�g�t���[�����[�N",
		-script=> [
				{-type => 'text/javascript',
				 -src  => "http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"},
				{-type => 'text/javascript',
				 -src  => "http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"},
				{-type => 'text/javascript',
				 -src  => "$framework_root/HTML/js/test_gui.js"},
				{-type => 'text/javascript',
				 -src  => "$framework_root/HTML/js/test_browser_menu.js"}
			  ],
		-style=> [
				{-src  => "http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/redmond/jquery-ui.css"},
				{-src  => "$framework_root/HTML/test_browser.css"}
			 ]	

	);
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
