//�蓮�^�u�̃��j���[�̃z�o�[�E�N���b�N�C�x���g�n���h��


/* �C���v�b�g�t�H�[���e���v���[�g */

//�e�L�X�g�̐���
function make_description(description){
	var ret = "<p class=\"menu_input_description\">";
	ret += description;
	ret += "</p>";
	return ret;
};

//�t�@�C���̎w��
function make_input_file(file_name){
	var ret = "<input type=\"hidden\" name=\"file\" value=\"";
	ret += file_name;
	ret += "\">";
	return ret;
};

//�e�L�X�g�{�b�N�X�̍쐬
function make_textbox(name, opt_default_value){
	var ret = opt_default_value === undefined ?
		"<input class=\"menu_input_text\" type=\"text\" name=\""
		:"<input class=\"menu_input_text\" type=\"text\" value=" + opt_default_value + " name=\"";
	ret += name;
	ret += "\">";
	return ret;
};

//�Z���N�g�{�b�N�X�̍쐬
function make_selectbox(name, array_option, first_value){

	var ret = "<select name=\"" + name + "\">";
	var value = first_value;
	var key;
	for (key in array_option){
		ret += "<option value = \"" + value + "\">";
		ret += array_option[key];
		ret += "</option>";
		value ++;
	}
	ret += "</select>";
	return ret;
};

//���j���[�̃w�b�_�[�t�b�^�[
var menu_header = "<div id=\"menu_input_form\" class=\"menu_form_class\">";
var menu_footer = "</div>";


//PlayerController
$(function(){
    $("#player_controller").hover(function(){ 
            $("#msg_window").find("p").text("�v���C���[�̐�����m���A�폜");
        });
});

//PlayerController::access_data
$(function(){
    $("#access_data", "#player_controller").on({
	"click": function(e){ 
		$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +make_description("�f�[�^��")
			   +make_textbox("value2")
			   +make_description("�V�����l")
			   +make_textbox("value3")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/PlayerController/access_data.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("�v���C���[��user.cgi�ɒ��ڃA�N�Z�X���Ēl�̐ݒ�/�擾���s��");
		$("#msg_window").find("p").append("<br>$m{data_name}�𑀍삷�铮��");
		$("#msg_window").find("p").append("<br>�u���E�U�łł͐V�����l��get_value��ݒ肷��ƌ��݂̒l���擾���ăG���[�Ƃ��ďo�͂���");
	}
   });
});

//PlayerController::create_player
$(function(){
    $("#create_player", "#player_controller").on({
	"click": function(){ 

		var sex = ["�j��", "����"];
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +make_description("�p�X���[�h")
			   +make_textbox("value2")
			   +make_description("����")
			   +make_selectbox("value3", sex, 1)
			   +make_description("�h�o�A�h���X(�u���E�U�ł͒������B�f�t�H���g�l�̂܂܎g����)")
			   +make_textbox("value4", "1.1.1.1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/PlayerController/create_player.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("login.cgi����V�K�v���C���[���쐬");

	}
   });
});


//PlayerController::action_shikan_player
$(function(){
    $("#action_shikan_player", "#player_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +make_description("�m�����鍑�̃C���f�b�N�X")
			   +make_textbox("value2")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/PlayerController/action_shikan_player.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("���C����ʁ�����񁨎m������m������");
		$("#msg_window").find("p").append("���Q�̏ꍇ�͎m�����鍑�ɍ��̑���+1���w�肷��");

	}
   });
});

//PlayerController::remove_player
$(function(){
    $("#remove_player", "#player_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/PlayerController/remove_player.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("�v���C���[���폜����");

	}
   });
});

//PlayerController::refresh_player
$(function(){
    $("#refresh_player", "#player_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/PlayerController/refresh_player.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("�v���C���[��tp,lib,turn����ɂ���(&refresh����)");
	}
   });
});

//CountryController
$(function(){
    $("#country_controller").hover(function(){ 
            $("#msg_window").find("p").text("���Ɋւ���R���g���[���[");
        });
});

//CountryController::access_data
$(function(){
    $("#access_data", "#country_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("���̃C���f�b�N�X")
			   +make_textbox("value1")
			   +make_description("�f�[�^��")
			   +make_textbox("value2")
			   +make_description("�V�����l")
			   +make_textbox("value3")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/CountryController/access_data.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("countries.cgi�ɒ��ڃA�N�Z�X���č��̒l��ݒ�/�擾����");
		$("#msg_window").find("p").append("<br>�V�����l��get_value��ݒ肷��ƌ��݂̒l���擾���ăG���[�Ƃ��ďo�͂���");

	}
   });
});

//CountryController::admin_reset_countries
$(function(){
    $("#admin_reset_countries", "#country_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�X�^�[�g����N�x")
			   +make_textbox("value1", "1")
			   +make_description("���E�")
			   +make_textbox("value2", "1")
			   +make_description("���̐�")
			   +make_textbox("value3", "6")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/CountryController/admin_reset_countries.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("admin.cgi�̂��܂������쐬���Ăѐ��E�����Z�b�g����");

	}
   });
});

//CountryController::admin_add_country
$(function(){
    $("#admin_add_country", "#country_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�V��������")
			   +make_textbox("value1")
			   +make_description("�V�������̐F")
			   +make_textbox("value2", "#ff0000")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/CountryController/admin_add_country.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("admin.cgi�o�R�ŐV��������ǉ�����");

	}
   });
});

//CountryController::action_stand_candidate
$(function(){
    $("#action_stand_candidate", "#country_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/CountryController/action_stand_candidate.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("����񁨌N�哊�[������₩�痧��₷��");

	}
   });
});

//CountryController::action_vote
$(function(){
    $("#action_vote", "#country_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +make_description("���Җ�")
			   +make_textbox("value2")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/CountryController/action_vote.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("����񁨌N�哊�[�����[���瓊�[����");

	}
   });
});

//WorldController
$(function(){
    $("#world_controller").hover(function(){ 
            $("#msg_window").find("p").text("���E�ݒ�̃R���g���[���[");
        });
});

//WorldController::access_data
$(function(){
    $("#access_data", "#world_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�f�[�^��")
			   +make_textbox("value1")
			   +make_description("�V�����l")
			   +make_textbox("value2")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WorldController/access_data.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("countries.cgi�ɒ��ڃA�N�Z�X���Ēl��ݒ�/�擾����");
		$("#msg_window").find("p").append("<br>$w{data_name}�𑀍삷��̂Ɠ���");
		$("#msg_window").find("p").append("<br>�V�����l��get_value��ݒ肷��ƌ��݂̒l���擾���ăG���[�Ƃ��ďo�͂���");

	}
   });
});

//WorldController::evoke_disaster
$(function(){
    $("#evoke_disaster", "#world_controller").on({
	"click": function(){ 
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("more�X�C�b�`")
			   +make_textbox("value1", 0)
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WorldController/evoke_disaster.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("�ЊQ���N�����B");

	}
   });
});

//WarController
$(function(){
    $("#war_controller").hover(function(){ 
            $("#msg_window").find("p").text("�푈�֘A�̃R���g���[���[");
        });
});

//WarController::action_set_war
$(function(){
    $("#action_set_war", "#war_controller").on({
	"click": function(){ 

		var array = ["����", "�ʏ�", "����"];
        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +make_description("�Ώۍ��C���f�b�N�X")
			   +make_textbox("value2")
			   +make_description("�K��")
			   +make_selectbox("value3", array, 1)
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_set_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("���j���[�̐푈���K�͑I�������I���ŏo������v���C���[������G�~�����[�g����");
		$("#msg_window").find("p").append("<br>���������$m{lib}��war�ɂȂ�A$m{wt}�ɑҋ@���Ԃ��ݒ肳���B");

	}
   });
});

//WarController::action_encount
$(function(){
    $("#action_encount", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_encount.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("action_set_war�ŏo��������Ԃ��璅�e����B");
		$("#msg_window").find("p").append("<br>�ҋ@���Ԓ��ɂ͒��e�o���Ȃ��B�i$m{wt}��0�łȂ��Ȃ玸�s����)");
		$("#msg_window").find("p").append("<br>�ΐ푊��͒��e��Ɍ��肵�A$y{}����Q�Ƃł���B");

	}
   });
});

//WarController::action_step_war
$(function(){
    $("#action_step_war", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_step_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("�푈�Ő퓬���s��");
		$("#msg_window").find("p").append("<br>���e�O�ɌĂׂΎ��s����");

	}
   });
});


//WarController::action_win_war
$(function(){
    $("#action_win_war", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_win_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("����̕��͂��O�ɁA�����̕��͂��P���ɂ��Đ퓬���s����������");
		$("#msg_window").find("p").append("<br>���e�O�ɌĂׂΎ��s����");

	}
   });
});

//WarController::action_win_war
$(function(){
    $("#action_lose_war", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_lose_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("�����̕��͂��O�ɁA����̕��͂��P���ɂ��Đ퓬���s���s�k����");
		$("#msg_window").find("p").append("<br>���e�O�ɌĂׂΎ��s����");

	}
   });
});

//WarController::action_draw_war_turn
$(function(){
    $("#action_draw_war_turn", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_draw_war_turn.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("turn���O�ɐݒ肵�Ă���퓬���s�����������ɂ���");
		$("#msg_window").find("p").append("<br>���e�O�ɌĂׂΎ��s����");

	}
   });
});

//WarController::action_draw_war_kaimetu
$(function(){
    $("#action_draw_war_kaimetu", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_draw_war_kaimetu.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("���݂��̕��͂��O�ɐݒ肵�Ă���퓬���s�����������ɂ���");
		$("#msg_window").find("p").append("<br>���e�O�ɌĂׂΎ��s����");

	}
   });
});

//WarController::action_complete_war
$(function(){
    $("#action_complete_war", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_complete_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("����񂯂���Œ肵�Č�������܂Ő퓬����");
		$("#msg_window").find("p").append("<br>���e�O�ɌĂׂΎ��s����");

	}
   });
});

//WarController::action_after_war
$(function(){
    $("#action_after_war", "#war_controller").on({
	"click": function(){ 

        	$("#menu_input_form").replaceWith(
			    menu_header 
			   +make_description("�v���C���[��")
			   +make_textbox("value1")
			   +make_description("�I����")
			   +make_textbox("value2")
			   +menu_footer
			   +make_input_file("TestFramework/ScriptsManual/WarController/action_after_war.pm")
		);
	},
	"mouseover": function(){
		$("#msg_window").find("p").text("�����ɑI��������������");

	}
   });
});


