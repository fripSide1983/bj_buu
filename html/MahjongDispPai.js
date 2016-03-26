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
        MahjongDispPai = definition();
    }

})(function(){// ���ۂ̒�`���s���֐�
    'use strict';

    var MahjongDispPai = {};

    MahjongDispPai.game_ = null;
    MahjongDispPai.setGame = function(game) {
        MahjongDispPai.game_ = game;
    };
    // �v�̑傫���B�摜��ς���ꍇ�͂�������ς��Ă��������B
    MahjongDispPai.sizeXBase = 50;
    MahjongDispPai.sizeYBase = 74;
    // �g�嗦
    MahjongDispPai.scale = 0.35;
    // �\�������v�̑傫��
    MahjongDispPai.sizeX = parseInt(MahjongDispPai.sizeXBase * MahjongDispPai.scale, 10);
    MahjongDispPai.sizeY = parseInt(MahjongDispPai.sizeYBase * MahjongDispPai.scale, 10);
    // �v�̃C���[�W�X�v���C�g0�Ԗڂ����A���Ń}���Y�A�\�E�Y�A�s���Y�A���v�ƂȂ�܂�
    MahjongDispPai.image_ = "http://jsrun.it/assets/m/h/9/C/mh9CL.png";
    // �v�̃N���X�̖{��
    MahjongDispPai.DispPai = Class.create(Sprite, {
        // �R���X�g���N�^�BSprite���p�����Ă��܂��B
        initialize: function() {
            Sprite.call(this, MahjongDispPai.sizeXBase, MahjongDispPai.sizeYBase);
            this.str = 'u0'; // m1�`9,s1�`9,p1�`9,z1�`7
            this.frame = 0;
            this.image = MahjongDispPai.game_.assets[MahjongDispPai.image_];
            this.scaleX = MahjongDispPai.scale;
            this.scaleY = MahjongDispPai.scale;
            this.id = -1;
            // ���\������ۂ̃t���O
            this.uraFlag = false;
            this.dispPai = true;
        },
        
        // �v���w�肷��֐��Bpublic
        setFrame: function(str) {
            this.str = str;
            if (this.uraFlag) {
                this.frame = 0;
            } else {
                this.frame = MahjongDispPai.strToNum(str) + 1;
            }
        },
        
        // �^�b�`�����Ƃ��ɃQ�[���ɃC�x���g��Ԃ��悤�ɂ���֐��Bpublic
        setId: function(id) {
            this.id = id;
            this.clearEventListener('touchstart');
            this.addEventListener('touchstart', function() {
                var e = new enchant.Event("select" + this.id);
                MahjongDispPai.game_.dispatchEvent(e);
            });
        },
        
        // ���\���ɂ��邩�ǂ�����ݒ肷��֐��B������boolean��n���Bpublic
        setUra: function(ura) {
            this.uraFlag = ura;
            this.setFrame(this.str);
        },
        
        // �v�̎�ނ��ȒP�Ɏ擾���邽�߂̊֐��B�Ԃ�l�͔v�̎�ނ�\�������Bpublic
        getType: function() {
            return this.str.substr(0, 1);
        },
        
        // �v�̎�ނ��ȒP�Ɏ擾���邽�߂̊֐��B�Ԃ�l�͔v�̎�ނ�\�����Bpublic
        getNum: function() {
            return parseInt(this.str.substr(1, 1), 10);
        },
        
        // �v�̎�ނ��ȒP�Ɏ擾���邽�߂̊֐��B���v���ǂ�����Ԃ��Bpublic
        isTsu: function() {
            return (this.getType() === 'z');
        },
        
        // �v�̎�ނ��ȒP�Ɏ擾���邽�߂̊֐��B���v���ǂ�����Ԃ��Bpublic
        isIku: function() {
            return (!this.isTsu() && (this.getNum() === 1 || this.getNum() === 9));
        },
        
        // �v�̎�ނ��ȒP�Ɏ擾���邽�߂̊֐��B��㎚�v���ǂ�����Ԃ��Bpublic
        isYaochu: function() {
            return (this.isTsu() || this.isIku());
        }
    });
    
    // ��������q�X�g�O�����ȂǂɎg�����ɕϊ�����֐��Bpublic
    MahjongDispPai.strToNum = function(str) {
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
    MahjongDispPai.numToStr = function(num) {
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
    
    // �h���\���v����h���̕������Ԃ��֐��Bpublic
    MahjongDispPai.getDoraNextStr = function(pai) {
        var type = pai.getType();
        var num = pai.getNum() + 1;
        if (type === 'z') {
            if (num === 5) {
                num = 1;
            }else if (num === 8) {
                num = 5;
            }
        } else {
            if (num === 10) {
                num = 1;
            }
        }
        return (type + num);
    };
    
    // ���W���[���̃G�N�X�|�[�g
    return MahjongDispPai;
});
