


$(function(){
	$( '#tabs' ) . tabs();
	var menu = $('div > #menu');
	menu.menu({
		position: {my: "left top", at: "right top" }
	});
});

//�ݒ�{�^���������ꂽ���̃I���N���b�N�n���h��
function OnSettingButtonClick(){
	
	var log = document.getElementById('log');

	//API�e�X�g
	if (!window.File) {
		log.innerHTML = "�u���E�U��file API�������Ȃ��B�e�X�g�o���Ȃ��B";
		return 0;
	}

	//���ԃt�@�C���ւ̏o��
	var output;

	//�I�����ꂽ�e�X�g���������ݏ���
	var checks = document.getElementsByName('file');
	document.getElementById('log').innerHTML = "�I�����ꂽ�e�X�g<br>";
	for(var i=0; i < checks.length; i++){
		if(checks[i].checked){
			log.innerHTML += checks[i].value + "<br>";
			output += "test_name<>";
			output += checks[i].value + "\n";
		}
	}

	//�I�����ꂽ�Z�b�e�B���O���������ݏ���
	log.innerHTML += "<br>�ۑ�����f�B���N�g��<br>";

	var settings_before = document.getElementsByName('setting_before');
	for(var i=0; i < settings_before.length; i++){
		if(settings_before[i].checked){
			log.innerHTML += settings_before[i].value + ": ON<br>";
			output += "save_before<>";
			output += settings_before[i].value + "\n";
		}
	}

	log.innerHTML += "<br>��������f�B���N�g��<br>";
	var settings_after  = document.getElementsByName('setting_after');
	for(var i=0; i < settings_after.length; i++){
		if(settings_after[i].checked){
			log.innerHTML += settings_after[i].value + ": ON<br>";
			output += "save_after<>";
			output += settings_after[i].value + "\n";
		}
	}

	//���ԃt�@�C���ɏo��
}


//�K�w�I�ȃ`�F�b�N�{�b�N�X�̃N���b�N�n���h��
$(function() {
       	$("#treeList input[type=checkbox]").click(function(event) {
                   var $element = $(event.target);    
                   var checked = $element.attr('checked');
           
                   $element.closest("li").find('ul li input[type=checkbox]').each(function() {
                       if (checked) {
                           $(this).attr("checked", checked);
                       }
                       else {
                           $(this).removeAttr('checked');
                       }
                   });
               });
	});

//�X�N���v�g�^�u�z�o�[���̃N���b�N�n���h��
$(function(){
    $("a[href = '#tab_script']").hover(function(){ 
            $("#msg_window").find("p").text("�X�N���v�g�����s����B");
            $("#msg_window").find("p").append("<br><br>");
            $("#msg_window").find("p").append("tests   : �e�X�g");
            $("#msg_window").find("p").append("<br>");
            $("#msg_window").find("p").append("samples : �e�X�g�ƃR���g���[���[�̃`���[�g���A��");
            $("#msg_window").find("p").append("<br>");
            $("#msg_window").find("p").append("util    : �֗��ȃX�N���v�g");


        });
});

//�Z�[�u�����[�h�^�u�z�o�[���̃N���b�N�n���h��
$(function(){
    $("a[href = '#tab_saveload']").hover(function(){ 
            $("#msg_window").find("p").text("�f�[�^��ۑ�/��������");
            $("#msg_window").find("p").append("<br>Controller�ŕύX�����\��������data, log, html, user�f�B���N�g�����Z�[�u�����[�h����");
            $("#msg_window").find("p").append("<br>�V�����Z�[�u�������܂ŕۑ����ꂽ�f�[�^�͏����Ȃ�");

        });
});

//�蓮�^�u�z�o�[���̃N���b�N�n���h��
$(function(){
    $("a[href = '#tab_manual']").hover(function(){ 
            $("#msg_window").find("p").text("�R���g���[���[���u���E�U����g�p����");
        });
});
