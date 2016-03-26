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
        MahjongPlayerInfo = definition();
    }

})(function(){// ���ۂ̒�`���s���֐�
    'use strict';

    var MahjongPlayerInfo = {};

    MahjongPlayerInfo.game_ = null;
    MahjongPlayerInfo.setGame = function(game) {
        MahjongPlayerInfo.game_ = game;
    };
    // �v���C���[���̃N���X�{��
    MahjongPlayerInfo.PlayerInfo = Class.create({
        // �R���X�g���N�^
        initialize: function() {
            this.playerName = "player";
            this.point = 25000;
            this.position = 0;// 0:�� 1:�E 2:�� 3:��
            this.infoLabel = new Label();
            this.infoLabel.font = "8px cursive";
        },
        
        // �v���C���[�̈ʒu��ݒ肷��֐��Bpublic
        setPosition: function(position) {
            this.position = position;
        },
        
        // �v���C���[����ݒ肷��֐��Bpublic
        setPlayerName: function(playerName) {
            this.playerName = playerName;
        },
        
        // �v���C���[���̃Q�b�^�[�Bpublic
        getPlayerName: function() {
            return this.playerName;
        },
        
        // �����_��ݒ肷��֐��Bpublic
        setPoint: function(point) {
            this.point = point;
        },
        
        // �����_�𑝌�����֐��Bpublic
        pointAdd: function(point) {
            this.point += point;
        },
        
        // ��ڲ԰����\��������֐��Bpublic
        show: function() {
            var entityWidth = MahjongPlayerInfo.game_.width * 0.23;
            var entityHeight = MahjongPlayerInfo.game_.height * 0.03;
            var posX = MahjongPlayerInfo.game_.width * 0.35;
            var posY = MahjongPlayerInfo.game_.height * 0.6;
            var rotate = 0;
            if (this.position === 1) {
                posX = MahjongPlayerInfo.game_.width * 0.49;
                posY = MahjongPlayerInfo.game_.height * 0.51;
                rotate = 270;
            } else if (this.position === 2) {
                posX = MahjongPlayerInfo.game_.width * 0.4;
                posY = MahjongPlayerInfo.game_.height * 0.37;
                rotate = 180;
            } else if (this.position === 3) {
                posX = MahjongPlayerInfo.game_.width * 0.25;
                posY = MahjongPlayerInfo.game_.height * 0.46;
                rotate = 90;
            }
            this.infoLabel.text = this.playerName + ":" + this.point;
            this.infoLabel.x = posX;
            this.infoLabel.y = posY;
            this.infoLabel.width = entityWidth;
            this.infoLabel.height = entityHeight;
            this.infoLabel.backgroundColor = 'white';
            this.infoLabel.rotation = rotate;
            MahjongPlayerInfo.game_.rootScene.addChild(this.infoLabel);
        }
    });
    
    // ���W���[���̃G�N�X�|�[�g
    return MahjongPlayerInfo;
});
