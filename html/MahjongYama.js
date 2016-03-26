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
        MahjongYama = definition();
    }

})(function(){// ���ۂ̒�`���s���֐�
    'use strict';

    var MahjongYama = {};
    
    MahjongYama.game_ = null;
    MahjongYama.setGame = function(game) {
        MahjongYama.game_ = game;
    };
    // �Q�[���I�����Ɏc��R�v��
    MahjongYama.restPais = 14;
    // �R�̃N���X�̖{��
    MahjongYama.Yama = Class.create({
        // �R���X�g���N�^
        initialize: function() {
            this.restNum = 122;
            this.kanNum = 1;
            this.dora = [];
            this.ura = MahjongPai.Pai();
            this.ura.setFrame('u0');
            this.label = new Label("�~" + this.getRest());
            this.label.color = '#FFF';
        },
        
        // �J���̐���Ԃ��֐��Bpublic
        getKanNum: function() {
            return this.kanNum;
        },
        
        // �R��ǂݍ��ފ֐��Bpublic
        setJson: function(data) {
            this.restNum = data.RestNum;
            this.kanNum = data.KanNum;
            this.dora = data.Dora;
        },
        
        // �c��c������Ԃ��֐��Bpublic
        getRest: function() {
            return this.restNum;
        },
        
        // �h��������������̔z���Ԃ��֐��Bpublic
        getDoraStrs: function() {
            return this.dora;
        },
        // �R�̏���\������֐��Bpublic
        show: function() {
            var posX = MahjongYama.game_.width * 0.38;
            var posY = MahjongYama.game_.height * 0.38;
            this.ura.x = posX;
            this.ura.y = posY;
            this.label.x = posX + MahjongPai.sizeX * 1.5;
            this.label.y = posY + MahjongPai.sizeY / 2;
            this.label.text = "�~" + this.getRest();
            MahjongYama.game_.rootScene.addChild(this.ura);
            MahjongYama.game_.rootScene.addChild(this.label);
            
            posY += MahjongPai.sizeY;
            for (var i = 0; i < this.dora.length; i++){
                var dora = MahjongPai.Pai();
                dora.setFrame(this.dora[i]);
                dora.x = posX + i * MahjongPai.sizeX;
                dora.y = posY;
                MahjongYama.game_.rootScene.addChild(dora);
            }
        }
    });
    
    return MahjongYama;
});