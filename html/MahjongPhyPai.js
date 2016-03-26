enchant();

(function(definition){// ��`����֐��������ɂƂ�
    // ���[�h���ꂽ�����ɉ����ăG�N�X�|�[�g���@��ς���

    // CommonJS
    if (typeof exports === "object") {
        module.exports = definition();

    // RequireJS
    } else if (typeof define === "function" && define.amd) {
        define(definition);

    // <script>
    } else {
        MahjongPhyPai = definition();
    }

})(function(){// ���ۂ̒�`���s���֐�
    'use strict';

    var MahjongPhyPai = {};

    MahjongPhyPai.game_ = null;
    MahjongPhyPai.setGame = function(game) {
        MahjongPhyPai.game_ = game;
    };
    // �v�̑傫���B�摜��ς���ꍇ�͂�������ς��Ă��������B
    MahjongPhyPai.sizeX = 30;
    MahjongPhyPai.sizeY = 46;
    // �v�̃C���[�W�X�v���C�g0�Ԗڂ����A���Ń}���Y�A�\�E�Y�A�s���Y�A���v�ƂȂ�܂�
    MahjongPhyPai.image_ = "http://buu.pandora.nu/cgi-bin/bjtest/html/phyPai.png";
    // �v�̃N���X�̖{��
    MahjongPhyPai.PhyPai = Class.create(PhyBoxSprite, {
        // �R���X�g���N�^�BSprite���p�����Ă��܂��B
        initialize: function() {
            PhyBoxSprite.call(this, MahjongPhyPai.sizeX, MahjongPhyPai.sizeY, DYNAMIC_SPRITE, 1.0, 5.0, 0.2, true);
            this.str = 'u0'; // m1�`9,s1�`9,p1�`9,z1�`7
            this.frame = 0;
            this.image = MahjongPhyPai.game_.assets[MahjongPhyPai.image_];
            this.id = -1;
            // ���\������ۂ̃t���O
            this.uraFlag = false;
        },
        
        // �v���w�肷��֐��Bpublic
        setFrame: function(str) {
            this.str = str;
            if (this.uraFlag) {
                this.frame = 0;
            } else {
                this.frame = MahjongPhyPai.strToNum(str) + 1;
            }
        },
        
        // ID�̃Z�b�^�[�Bpublic
        setId: function(str, no) {
            this.setFrame(str);
            this.id = str + no;
            this.clearEventListener('pickup');
            this.addEventListener('pickup', function() {
                $.ajax({
                    type: 'POST',
                    url: 'chat_casino.cgi',
                    data: {
                        id: $("#id").val(),
                        pass: $("#pass").val(),
                        mode: 'tedumi',
                        arg: str + no
                    }
                });
            });
        },
        
        // �N���b�N�g���K�[�Bpublic
        ontouchstart: function() {
            var e = new enchant.Event('pickup');
            this.dispatchEvent(e);
        },
        
        // ���\���ɂ��邩�ǂ�����ݒ肷��֐��B������boolean��n���Bpublic
        setUra: function(ura) {
            this.uraFlag = ura;
            this.setFrame(this.str);
        },
        
        // ���Ԃ��֐��Bpublic
        reverse: function() {
            this.setUra(!this.uraFlag);
        },
    });    
    // ��������q�X�g�O�����ȂǂɎg�����ɕϊ�����֐��Bpublic
    MahjongPhyPai.strToNum = function(str) {
        var type = str.substr(0, 1);
        var num = parseInt(str.substr(1), 10);
        if (type === "m" && num >= 1 && num <= 9) {
            return (num - 1);
        } else if (type === "s" && num >= 1 && num <= 9) {
            return (num + 8);
        } else if (type === "p" && num >= 1 && num <= 9) {
            return (num + 17);
        } else if (type === "z" && num >= 1 && num <= 7) {
            return (num + 26);
        } else {
            return -1;
        }
    };
    
    // �q�X�g�O�����ȂǂɎg�����𕶎���ɕϊ�����֐��Bpublic
    MahjongPhyPai.numToStr = function(num) {
        var type = parseInt(num / 9, 10);
        num = (num % 9) + 1;
        if (type === 0) {
            type = 'm';
        } else if (type === 1) {
            type = 's';
        } else if (type === 2) {
            type = 'p';
        } else if (type === 3) {
            type = 'z';
        } else {
            return 'u0';
        }
        return (type + num);
    };
    // ���W���[���̃G�N�X�|�[�g
    return MahjongPhyPai;
});
