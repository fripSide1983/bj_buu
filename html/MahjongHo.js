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
        MahjongHo = definition();
    }

})(function(){// ���ۂ̒�`���s���֐�
    'use strict';

    var MahjongHo = {};

    MahjongHo.game_ = null;
    MahjongHo.setGame = function(game) {
        MahjongHo.game_ = game;
    };
    // �͂̃N���X�{��
    MahjongHo.Ho = Class.create({
        // �R���X�g���N�^
        initialize: function() {
            this.ho = [];
            this.reachAt = null;
            this.position = 0;// 0:�� 1:�E 2:�� 3:��
            this.eaten = [];
        },
        
        // �ǂ��ɕ\������͂��ݒ肷��֐��Bpublic
        setPosition: function(position) {
            this.position = position;
        },
        
        // �͂ɔv��ǉ�����֐��B�����͕�����Ȃ̂Œ��ӁBpublic
        addHo: function(str) {
            var pai = MahjongPai.Pai();
            pai.setFrame(str);
            this.ho.push(pai);
        },
        
        // ����������֐��Bpublic
        reach: function() {
            if (this.reachAt === null) {
                if (this.ho.length > 0) {
                    this.reachAt = this.ho.length - 1;
                    this.refresh();
                }
            }
        },
        
        // ���ꂽ�Ƃ��ɌĂԊ֐��Bpublic
        eat: function() {
            if (this.ho.length > 0) {
                this.eaten.push(this.ho.length - 1);
                this.refresh();
            }
        },
        
        // �ĕ`��t���O�𗧂Ă�֐��B
        refresh: function() {
            this.show();
        },
        
        // setAll�œǂݍ��߂�`�ŉ͂̏��𕶎��񉻂���֐��Bpublic
        toString: function() {
            var retStr = "";
            for (var i = 0; i < this.ho.length; i++) {
                retStr += this.ho[i].str;
                if (i === this.reachAt) {
                    retStr += "r";
                }
                if (jQuery.inArray(i, this.eaten) === -1) {
                    retStr += "e";
                }
            }
            return retStr;
        },
        
        // �͂�\��������֐��Bpublic
        show: function() {
            this.showCore(false);
        },
        
        // �\���̓����֐��B
        showCore: function(addFlag) {
            var beginPosX = 145;
            var beginPosY = 340;
            var directXX = 1;
            var directXY = 0;
            var directYX = 0;
            var directYY = 1;
            var rotate = 0;
            if (this.position === 1) {
                beginPosX = 345;
                beginPosY = 345;
                directXX = 0;
                directXY = -1;
                directYX = 1;
                directYY = 0;
                rotate = 270;
            } else if (this.position === 2) {
                beginPosX = 355;
                beginPosY = 145;
                directXX = -1;
                directXY = 0;
                directYX = 0;
                directYY = -1;
                rotate = 180;
            } else if (this.position === 3) {
                beginPosX = 145;
                beginPosY = 135;
                directXX = 0;
                directXY = 1;
                directYX = -1;
                directYY = 0;
                rotate = 90;
            }
            var posX = beginPosX;
            var posY = beginPosY;
            var index = 0;
            var sleepPai = false;
            for (var i = 0; i < this.ho.length; i++) {
                if (i === this.reachAt) {
                    sleepPai = true;
                }
                if (jQuery.inArray(i, this.eaten) == -1) {
                    var pai = this.ho[i];
                    if (sleepPai) {
                        pai.x = posX + directYX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 + directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        pai.y = posY + directYY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 + directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        pai.rotation = rotate + 90;
                        posX += directXX * MahjongPai.sizeY;
                        posY += directXY * MahjongPai.sizeY;
                        sleepPai = false;
                    } else {
                        pai.x = posX;
                        pai.y = posY;
                        pai.rotation = rotate;
                        posX += directXX * MahjongPai.sizeX;
                        posY += directXY * MahjongPai.sizeX;
                    }
                    if (!addFlag || i === this.ho.length - 1) {
                        MahjongHo.game_.rootScene.addChild(pai);
                    }
                    index++;
                    if (index % 6 === 0 && index < 18) {
                        var row = index / 6;
                        posX = beginPosX + directYX * row * MahjongPai.sizeY;
                        posY = beginPosY + directYY * row * MahjongPai.sizeY;
                    }
                }
            }
        },
        
        // �����񂩂�͏���ǂݍ��ފ֐��Bpublic
        setAll: function(str) {
            this.ho = [];
            this.reachAt = null;
            this.eaten = [];
            var split_str = str.split('');
            var i = 0;
            while (i < split_str.length) {
                var c = split_str[i];
                if (c === 'm' || c === 's' || c === 'p' || c === 'z') {
                    var num = split_str[i + 1];
                    this.addHo(c + num);
                    i++;
                } else if (c === 'r') {
                    this.reach();
                } else if (c === 'e') {
                    this.eat();
                }
                i++;
            }
        }
    });
    
    // ���W���[���̃G�N�X�|�[�g
    return MahjongHo;
});
