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
        MahjongTehai = definition();
    }

})(function(){// ���ۂ̒�`���s���֐�
    'use strict';
    
    var MahjongTehai = {};
    
    MahjongTehai.game_ = null;
    MahjongTehai.setGame = function(game) {
        MahjongTehai.game_ = game;
    };
    // ���v�E�ʎq��\���C���i�[�N���X
    MahjongTehai.Naki = Class.create({
        // �R���X�g���N�^
        initialize: function() {
            this.paiNaki = MahjongPai.Pai();
            this.pai1 = MahjongPai.Pai();
            this.pai2 = MahjongPai.Pai();
            this.kanFlag = 0;// 0:�|���E�`�[ 1:���� 2:�Þ� -1:�ʑO�ʎq
            this.nakiFrom = 3;// 3:��� 2:�Ζ� 1:����
        },
        
        // ���v�𕶎��񂩂�ݒ肷��֐��Bpublic
        setNaki: function(str) {
            var split_str = str.split('');
            if (split_str[0] == '-') {
                if (split_str[split_str.length - 1] == '-') {
                    // �Ζʃ|��
                    this.pai1.setFrame(split_str[1] + split_str[2]);
                    this.paiNaki.setFrame(split_str[3] + split_str[4]);
                    this.pai2.setFrame(split_str[5] + split_str[6]);
                    if (split_str.length === 10) {
                        this.kanFlag = 1;
                    }
                    this.nakiFrom = 2;
                } else {
                    // ��ƃ|���`�[
                    this.paiNaki.setFrame(split_str[1] + split_str[2]);
                    this.pai1.setFrame(split_str[3] + split_str[4]);
                    this.pai2.setFrame(split_str[5] + split_str[6]);
                    if (split_str.length === 9) {
                        this.kanFlag = 1;
                    }
                    this.nakiFrom = 3;
                }
            } else {
                if (split_str[split_str.length - 1] === '-') {
                    // ���ƃ|��
                    this.pai1.setFrame(split_str[0] + split_str[1]);
                    this.pai2.setFrame(split_str[2] + split_str[3]);
                    this.paiNaki.setFrame(split_str[4] + split_str[5]);
                    if (split_str.length === 9) {
                        this.kanFlag = 1;
                    }
                    this.nakiFrom = 1;
                } else {
                    // �Þ�
                    this.paiNaki.setFrame(split_str[0] + split_str[1]);
                    this.pai1.setFrame(split_str[2] + split_str[3]);
                    this.pai2.setFrame(split_str[4] + split_str[5]);
                    this.kanFlag = 2;
                    this.nakiFrom = 0;
                }
            }
        },
        
        // �ʎq�𕶎��񂩂�ݒ肷��֐��Bpublic
        setMentsu: function(str) {
            var split_str = str.split('');
            this.paiNaki.setFrame(split_str[0] + split_str[1]);
            this.pai1.setFrame(split_str[2] + split_str[3]);
            this.pai2.setFrame(split_str[4] + split_str[5]);
            this.kanFlag = -1;
        },
        
        // �ǂݍ��݉\�ȕ�����ɕϊ�����֐��Bpublic
        toString: function() {
            var retStr = "";
            if (this.kanFlag === 2) {
                for (var i = 0; i < 4; i++) {
                    retStr += this.paiNaki.str;
                }
            } else {
                if (this.kanFlag !== -1) {
                    if (this.nakiFrom === 2 || this.nakiFrom === 3) {
                        retStr += "-";
                    }
                }
                retStr += this.paiNaki.str + this.pai1.str + this.pai2.str;
                if (this.kanFlag === 1) {
                    retStr += this.paiNaki.str;
                }
                if (this.kanFlag !== -1) {
                    if (this.nakiFrom === 1 || this.nakiFrom === 2) {
                        retStr += "-";
                    }
                }
            }
            return retStr;
        },
        
        // ���֐��̂��ߐF�X���肷��֐��B���q�Bpublic
        isShuntsu: function() {
            return (this.pai1.str !== this.pai2.str);
        },
        
        // ���֐��̂��ߐF�X���肷��֐��B���q�Bpublic
        isKotsu: function() {
            return (this.pai1.str === this.pai2.str);
        },
        
        // ���֐��̂��ߐF�X���肷��֐��B�|���Bpublic
        isPon: function() {
            return (this.isKotsu() && this.kanFlag === 0);
        },
        
        // ���֐��̂��ߐF�X���肷��֐��B�Í��Bpublic
        isAnko: function() {
            return (this.isKotsu() && this.kanFlag === -1);
        },
        
        // ���֐��̂��ߐF�X���肷��֐��B���ȁBpublic
        isMinkan: function() {
            return (this.isKotsu() && this.kanFlag === 1);
        },
        
        // ���֐��̂��ߐF�X���肷��֐��B�ÞȁBpublic
        isAnkan: function() {
            return (this.isKotsu() && this.kanFlag === 2);
        },
        
        // ���֐��̂��ߐF�X���肷��֐��B���v���܂ނ��Bpublic
        isIku: function() {
            if (this.pai1.isIku()) {
                return true;
            }
            if (this.pai2.isIku()) {
                return true;
            }
            if (this.paiNaki.isIku()) {
                return true;
            }
            
            return false;
        },
        
        // ���֐��̂��ߐF�X���肷��֐��B���v���Bpublic
        isTsu: function() {
            var type = this.pai1.str.substr(0, 1);
            if (type === 'z') {
                return true;
            }
            type = this.pai2.str.substr(0, 1);
            if (type === 'z') {
                return true;
            }
            type = this.paiNaki.str.substr(0, 1);
            if (type === 'z') {
                return true;
            }
            
            return false;
        },
        
        // ���֐��̂��ߐF�X���肷��֐��B��㎚�v���܂ނ��Bpublic
        isYaochu: function() {
            return (this.isIku() || this.isTsu());
        }
    });
    // ��v��ʎq���Ƃɕ����ĕێ�����_���Ȃǂ̌v�Z�p�C���i�[�N���X�B
    MahjongTehai.MentsuSeparatedTehai = Class.create({
        // �R���X�g���N�^
        initialize: function() {
            this.mentsu = [];
            this.janto = MahjongPai.Pai();
            this.finishShape = 0;// 0:���� 1:�V���{ 2:�ƒ� 3:�Ӓ� 4:�P�R
            this.tehai = null;// �V�a���̃t���O��ۑ����邽�߂Ɏ�v�N���X������
        },
        
        // ��v��ݒ肷��֐��Bpublic
        setTehai: function(tehai) {
            this.tehai = tehai;
            for (var i = 0; i < this.tehai.naki.length; i++) {
                this.addMentsu(this.tehai.naki[i]);
            }
        },
        
        // �ʎq��ǉ�����֐��Bpublic
        addMentsu: function(naki) {
            this.mentsu.push(naki);
        },
        
        // ������ݒ肷��֐��Bpublic
        setJanto: function(str) {
            this.janto.setFrame(str);
        },
        
        // �オ�肪����ݒ肷��֐��Bpublic
        setFinishShape: function(shape) {
            this.finishShape = shape;
        }, 
        
        // �ʎq�̃Q�b�^�[�Bpublic
        getMentsu: function(index) {
            if (index >= 0 && index < this.mentsu.length) {
                return this.mentsu[index];
            }
            return null;
        },
        
        // ���q�𐔂���֐��Bpublic
        countShuntsu: function() {
            var count = 0;
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].isShuntsu()) {
                    count++;
                }
            }
            return count;
        },
        
        // ���q�𐔂���֐��Bpublic
        countKotsu: function() {
            var count = 0;
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].isKotsu()) {
                    count++;
                }
            }
            return count;
        },
        
        // �ʎq��4���邩���ׂ�֐��Bpublic
        is4Mentsu: function() {
            return ((this.countShuntsu() + this.countKotsu()) === 4);
        },
        
        // �Í��̐��𐔂���֐��Bpublic
        countAnko: function() {
            var count = 0;
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].isAnko() || this.mentsu[i].isAnkan()) {
                    count++;
                }
            }
            return count;
        },
        
        // �Ȏq�̐��𐔂���֐��Bpublic
        countKan: function() {
            var count = 0;
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].isMinkan() || this.mentsu[i].isAnkan()) {
                    count++;
                }
            }
            return count;
        },
        
        // �ʑO�����肷��֐��Bpublic
        isMenzen: function() {
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].kanFlag !== -1 && this.mentsu[i].kanFlag !== 2) {
                    return false;
                }
            }
            return true;
        },
        
        // ���̌v�Z������֐��Bpublic
        calcHu: function(ba, kaze) {
            // ���v�Z
            var hu = 20;
            if (this.janto.str === ba) {
                hu += 2;
            }
            if (this.janto.str === kaze) {
                hu += 2;
            }
            if (this.finishShape === 2 || this.finishShape === 3 || this.finishShape === 4) {
                hu += 2;
            }
            for (var i = 0; i < this.mentsu.length; i++) {
                var addHu = 0;
                if (this.mentsu[i].isPon()) {
                    addHu = 2;
                } else if (this.mentsu[i].isAnko()) {
                    if (this.finishShape === 1 && this.mentsu[i].pai1.str === this.tehai.lastAddPai.str) {
                        addHu = 2;
                    } else {
                        addHu = 4;
                    }
                } else if (this.mentsu[i].isMinkan()) {
                    addHu = 8;
                } else if (this.mentsu[i].isAnkan()) {
                    addHu = 16;
                }
                if (this.mentsu[i].isYaochu()) {
                    addHu *= 2;
                }
                hu += addHu;
            }

            if (hu % 10 > 0) {
                hu += 10 - (hu % 10);
            }
            return hu;
        },
        
        // �ʐ����v�Z����֐��Bpublic
        calcFan: function(ba, kaze) {
            // �ʌv�Z
            var fan = 0;
            var yaku = '';
            var yakuList = [];
            for (var ruleI = 0; ruleI < MahjongTehai.Rule.ruleSize(); ruleI++) {
                var rule = MahjongTehai.Rule.getRule(ruleI);
                var result = rule(this, ba, kaze);
                if (result[0] > 0) {
                    yakuList.push(result);
                }
            }
            var isYakuman = false;
            for (var yakuI = 0; yakuI < yakuList.length; yakuI++) {
                if (yakuList[yakuI][0] >= 13) {
                    isYakuman = true;
                }
            }
            for (var yakumanI = 0; yakumanI < yakuList.length; yakumanI++) {
                if (!isYakuman || yakuList[yakumanI][0] >= 13) {
                    fan += yakuList[yakumanI][0];
                    yaku += yakuList[yakumanI][1] + ',';
                }
            }
            // �h�����Z
            if (fan > 0) {
                var doraNum = 0;
                var hist = this.tehai.toHistogramAll();
                var doras = this.tehai.getDoras();
                for (var doraI = 0; doraI < doras.length; doraI++) {
                    var doraHyouji = doras[doraI];
                    var doraStr = MahjongPai.getDoraNextStr(doraHyouji);
                    doraNum += hist[MahjongPai.strToNum(doraStr)];
                }
                if (doraNum > 0) {
                    fan += doraNum;
                    yaku += '�h��' + doraNum + ',';
                }
            }
            return [fan, yaku];
        },
        
        // �_�����v�Z����֐��Bpublic
        calcPoint: function(ba, kaze) {
            var hu = this.calcHu(ba, kaze);
            var fan = this.calcFan(ba, kaze);
            return MahjongTehai.calcPointFromHuAndFan(hu, fan, this.tehai.isTsumo(), kaze === 'z1');
        },
        
        // �����Ɠ����C���X�^���X��Ԃ��֐��Bpublic
        clone: function() {
            var ret = MahjongTehai.MentsuSeparatedTehai();
            ret.setTehai(this.tehai);
            for (var i = 0; i < this.mentsu.length; i++) {
                if (this.mentsu[i].kanFlag === -1) {
                    var mentsu = MahjongTehai.Naki();
                    mentsu.setMentsu(this.mentsu[i].toString());
                    ret.mentsu.push(mentsu);
                }
            }
            ret.janto.setFrame(this.janto.str);
            ret.finishShape = this.finishShape;            
            return ret;
        }
    });
    // ��v�̃N���X�{��
    MahjongTehai.Tehai = Class.create({
        // �R���X�g���N�^
        initialize: function() {
            this.tehai = [];
            this.naki = [];
            this.position = 0;// 0:�� 1:�E 2:�� 3:��
            this.mine = 1;
            this.tsumoFlag = false;
            this.chankanFlag = false;
            this.tenhoFlag = false;
            this.chihoFlag = false;
            this.reachFlag = false;
            this.doubleReachFlag = false;
            this.ippatsuFlag = false;
            this.rinshanFlag = false;
            this.haiteiFlag = false;
            this.doras = [];
            this.agariHai = null;
            this.lastAddPai = null;
            this.selected = null;
        },
        
        // �����Ɠ����C���X�^���X��Ԃ��֐��Bpublic
        clone: function() {
            var ret = MahjongTehai.Tehai();
            ret.setAll(this.toString());
            ret.position = this.position;
            ret.mine = this.mine;
            ret.tsumoFlag = this.tsumoFlag;
            ret.chankanFlag = this.chankanFlag;
            ret.tenhoFlag = this.tenhoFlag;
            ret.chihoFlag = this.chihoFlag;
            ret.reachFlag = this.reachFlag;
            ret.doubleReachFlag = this.doubleReachFlag;
            ret.ippatsuFlag = this.ippatsuFlag;
            ret.rinshanFlag = this.rinshanFlag;
            ret.haiteiFlag = this.haiteiFlag;
            ret.doras = this.doras;
            ret.lastAddPai = this.lastAddPai;
            ret.selected = this.selected;
            
            return ret;
        },
        
        // �ʒu��ݒ肷��֐��Bpublic
        setPosition: function(position) {
            this.position = position;
        },
        
        // �ΐ�p�����̎�v���ǂ�����ݒ肷��֐��Bpublic
        setMine: function(mine) {
            this.mine = mine;
        },
        
        // ��v��ǂݍ��ފ֐��B
        setTehai: function(str) {
            var split_str = str.split('');
            this.tehai = [];
            var i = 0;
            while (i < split_str.length) {
                if (split_str[i] === ' ') {
                    break;
                }
                var pai = MahjongPai.Pai();
                pai.setFrame(split_str[i] + split_str[i + 1]);
                this.tehai.push(pai);
                i += 2;
            }
        },
        
        setSelected: function(selecting) {
            this.selected = selecting;
        },
        
        // ���v���܂ߎ�v��ǂݍ��ފ֐��Bpublic
        setAll: function(str) {
            this.naki = [];
            var split_str = str.split(' ');
            for (var i = 0; i < split_str.length; i++) {
                if (i === 0) {
                    this.setTehai(split_str[i]);
                } else {
                    var huro = MahjongTehai.Naki();
                    huro.setNaki(split_str[i]);
                    this.naki.push(huro);
                }
            }
        },
        
        // ��v�ɒǉ�����֐��B������MahjongPai.Pai�Bpublic
        add: function(pai) {
            this.tehai.push(pai);
            if (this.lastAddPai === null) {
                this.lastAddPai = MahjongPai.Pai();
            }
            this.lastAddPai.setFrame(pai.str);
            this.setIds();
            this.refresh();
        },
        
        // �`�[�����Ƃ��ɌĂԊ֐��B�����̓`�[�����v�ƃ`�[�����`�Bpublic
        chi: function(pai, type) {
            var pai1Str = pai.getType() + (pai.getNum() - 1);
            var pai2Str = pai.getType() + (pai.getNum() + 1);
            if (type === -1) {
                pai1Str = pai.getType() + (pai.getNum() - 2);
                pai2Str = pai.getType() + (pai.getNum() - 1);
            } else if (type === 1) {
                pai1Str = pai.getType() + (pai.getNum() + 1);
                pai2Str = pai.getType() + (pai.getNum() + 2);
            }
            var hist = this.toHistogram();
            if (hist[MahjongPai.strToNum(pai1Str)] > 0 && hist[MahjongPai.strToNum(pai2Str)] > 0) {
                for (var i1 = 0; i1 < this.tehai.length; i1++) {
                    if (this.tehai[i1].str === pai1Str) {
                        this.tehai.splice(i1, 1);
                        break;
                    }
                }
                for (var i2 = 0; i2 < this.tehai.length; i2++) {
                    if (this.tehai[i2].str === pai2Str) {
                        this.tehai.splice(i2, 1);
                        break;
                    }
                }
                var naki = MahjongTehai.Naki();
                naki.setNaki('-' + pai.str + pai1Str + pai2Str);
                this.naki.push(naki);
                this.refresh();
                return true;
            }
            return false;
        },
        
        // �|�������Ƃ��ɌĂԊ֐��B�����̓|�������v�ƃ|�����������Bpublic
        pon: function(pai, from) {
            var hist = this.toHistogram();
            if (hist[MahjongPai.strToNum(pai.str)] >= 2) {
                for (var i1 = 0; i1 < this.tehai.length; i1++) {
                    if (this.tehai[i1].str === pai.str) {
                        this.tehai.splice(i1, 1);
                        break;
                    }
                }
                for (var i2 = 0; i2 < this.tehai.length; i2++) {
                    if (this.tehai[i2].str === pai.str) {
                        this.tehai.splice(i2, 1);
                        break;
                    }
                }
                var naki = MahjongTehai.Naki();
                var nakiStr = pai.str + pai.str + pai.str;
                if (from === 3) {
                    nakiStr = '-' + nakiStr;
                } else if (from === 2) {
                    nakiStr = '-' + nakiStr + '-';
                } else if (from === 1) {
                    nakiStr = nakiStr + '-';
                }
                naki.setNaki(nakiStr);
                this.naki.push(naki);
                this.refresh();
                return true;
            }
            return false;
        },
        
        // ���Ȃ����Ƃ��ɌĂԊ֐��B�����͖��Ȃ����v�Ɩ��Ȃ��������Bpublic
        minkan: function(pai, from) {
            var hist = this.toHistogram();
            if (hist[MahjongPai.strToNum(pai.str)] >= 3) {
                for (var i1 = 0; i1 < this.tehai.length; i1++) {
                    if (this.tehai[i1].str === pai.str) {
                        this.tehai.splice(i1, 1);
                        break;
                    }
                }
                for (var i2 = 0; i2 < this.tehai.length; i2++) {
                    if (this.tehai[i2].str === pai.str) {
                        this.tehai.splice(i2, 1);
                        break;
                    }
                }
                for (var i3 = 0; i3 < this.tehai.length; i3++) {
                    if (this.tehai[i3].str === pai.str) {
                        this.tehai.splice(i3, 1);
                        break;
                    }
                }
                var naki = MahjongTehai.Naki();
                var nakiStr = pai.str + pai.str + pai.str + pai.str;
                if (from === 3) {
                    nakiStr = '-' + nakiStr;
                } else if (from === 2) {
                    nakiStr = '-' + nakiStr + '-';
                } else if (from === 1) {
                    nakiStr = nakiStr + '-';
                }
                naki.setNaki(nakiStr);
                this.naki.push(naki);
                return true;
            }
            return false;
        },
        
        // �ÞȂ����Ƃ��ɌĂԊ֐��B�����͈ÞȂ����v�Bpublic
        ankan: function(pai) {
            var hist = this.toHistogram();
            if (hist[MahjongPai.strToNum(pai.str)] === 4) {
                for (var i1 = 0; i1 < this.tehai.length; i1++) {
                    if (this.tehai[i1].str === pai.str) {
                        this.tehai.splice(i1, 1);
                        break;
                    }
                }
                for (var i2 = 0; i2 < this.tehai.length; i2++) {
                    if (this.tehai[i2].str === pai.str) {
                        this.tehai.splice(i2, 1);
                        break;
                    }
                }
                for (var i3 = 0; i3 < this.tehai.length; i3++) {
                    if (this.tehai[i3].str === pai.str) {
                        this.tehai.splice(i3, 1);
                        break;
                    }
                }
                for (var i4 = 0; i4 < this.tehai.length; i4++) {
                    if (this.tehai[i4].str === pai.str) {
                        this.tehai.splice(i4, 1);
                        break;
                    }
                }
                var naki = MahjongTehai.Naki();
                var nakiStr = pai.str + pai.str + pai.str + pai.str;
                naki.setNaki(nakiStr);
                this.naki.push(naki);
                return true;
            }
            return false;
        },
        
        // ���Ȃ����Ƃ��ɌĂԊ֐��B�����͉��Ȃ����v�Bpublic
        kakan: function(pai) {
            var nakiIndex = -1;
            for (var nakiI = 0; nakiI < this.naki.length; nakiI++) {
                if (this.naki[nakiI].pai1.str === pai.str && this.naki[nakiI].isPon()) {
                    nakiIndex = nakiI;
                    break;
                }
            }
            var tehaiIndex = -1;
            for (var tehaiI = 0; tehaiI < this.tehai.length; tehaiI++) {
                if (this.tehai[tehaiI].str === pai.str) {
                    tehaiIndex = tehaiI;
                    break;
                }
            }
            if (nakiIndex !== -1 && tehaiIndex !== -1) {
                this.tehai.splice(tehaiIndex, 1);
                this.naki[nakiIndex].kanFlag = 1;
                return true;
            }
            return false;
        },
        
        // �ÞȂ������͉��Ȃł��邩�ǂ����Ԃ��֐��Bpublic
        getKanable: function() {
            var kanable = [];
            var hist = this.toHistogram();
            for (var ankanI = 0; ankanI < 34; ankanI++) {
                if (hist[ankanI] === 4) {
                    var ankanPai = MahjongPai.Pai();
                    ankanPai.setFrame(MahjongPai.numToStr(ankanI));
                    kanable.push(ankanPai);
                }
            }
            for (var kakanI = 0; kakanI < this.naki.length; kakanI++) {
                var naki = this.naki[kakanI];
                if (naki.isPon() && hist[MahjongPai.strToNum(naki.pai1.str)] === 1) {
                    var kakanPai = MahjongPai.Pai();
                    kakanPai.setFrame(naki.pai1.str);
                    kanable.push(kakanPai);
                }
            }
            return kanable;
        },
        
        // �v��؂�֐��B�����͎�v�̃C���f�b�N�X�Bpublic
        drop: function(index) {
            if (this.tehai.length % 3 !== 2) {
                return null;
            }
            if (index >= 0 && index < this.tehai.length) {
                var pai = this.tehai[index];
                this.tehai.splice(index, 1);
                
                this.sort();
                this.refresh();

                return pai;
            }
            return null;
        },
        
        // ��v��ǂݍ��݉\�ȕ�����ɕϊ�����֐��Bpublic
        toString: function(forceShow) {
            var retStr = "";
            for (var tehaiI = 0; tehaiI < this.tehai.length; tehaiI++) {
                if (forceShow || this.mine === 1) {
                    retStr += this.tehai[tehaiI].str;
                }
            }
            for (var nakiI = 0; nakiI < this.naki.length; nakiI++) {
                retStr += " ";
                retStr += this.naki[nakiI].toString();
            }
            
            return retStr;
        },
        
        // ��v���q�X�g�O�����ɕϊ�����֐��Bpublic
        toHistogram: function() {
            var hist = [];
            for (var initI = 0; initI < 34; initI++) {
                hist.push(0);
            }
            for (var tehaiI = 0; tehaiI < this.tehai.length; tehaiI++) {
                var str = this.tehai[tehaiI].str;
                hist[MahjongPai.strToNum(str)]++;
            }
            return hist;
        },
        
        // ���v���܂ߎ�v���q�X�g�O�����ɕϊ�����֐��Bpublic
        toHistogramAll: function() {
            var hist = [];
            for (var initI = 0; initI < 34; initI++) {
                hist.push(0);
            }
            for (var tehaiI = 0; tehaiI < this.tehai.length; tehaiI++) {
                var str = this.tehai[tehaiI].str;
                hist[MahjongPai.strToNum(str)]++;
            }
            for (var nakiI = 0; nakiI < this.naki.length; nakiI++) {
                var naki = this.naki[nakiI];
                hist[MahjongPai.strToNum(naki.pai1.str)]++;
                hist[MahjongPai.strToNum(naki.pai2.str)]++;
                hist[MahjongPai.strToNum(naki.paiNaki.str)]++;
                if (naki.kanFlag > 0) {
                    hist[MahjongPai.strToNum(naki.paiNaki.str)]++;
                }
            }
            return hist;
        },
        
        // ���v����֐��Bpublic
        sort: function() {
            this.tehai.sort(
                function(a, b) {
                    var aType = a.str.substr(0, 1); 
                    var aNum = parseInt(a.str.substr(1, 1), 10);
                    if (aType == 'm') {
                        aNum += 10;
                    } else if(aType === 's') {
                        aNum += 20;
                    } else if(aType === 'p') {
                        aNum += 30;
                    } else if(aType === 'z') {
                        aNum += 40;
                    }
                    var bType = b.str.substr(0, 1); 
                    var bNum = parseInt(b.str.substr(1, 1), 10);
                    if (bType == 'm') {
                        bNum += 10;
                    } else if(bType === 's') {
                        bNum += 20;
                    } else if(bType === 'p') {
                        bNum += 30;
                    } else if(bType === 'z') {
                        bNum += 40;
                    }
                    if (aNum < bNum) {
                        return -1;
                    } else if(aNum > bNum) {
                        return 1;
                    } else {
                        return 0;
                    }
                }
            );
            
            this.setIds();
        },
        
        // ��v���ׂĂɃ^�b�`�����Ƃ��̃��X�i�[��ݒ肷��֐��Bpublic
        setIds: function() {
            for (var i = 0; i < this.tehai.length; i++) {
                var pai = this.tehai[i];
                pai.setId(i);
            }
        },
        
        // ��v�̍ĕ`��t���O�𗧂Ă�֐��B
        refresh: function() {
            var e = new enchant.Event("refreshRequire");
            MahjongTehai.game_.dispatchEvent(e);
        },
        
        // ��v��\������֐��Bpublic
        show: function() {
            this.showCore(MahjongTehai.game_.rootScene, this.mine);
        },
        
        // ���ʕ\�����Ɏ�v��\������֐��Bpublic
        showResult: function(scene, tenpai) {
            this.showCore(scene, tenpai);
        },
        
        // ��v�̕\���p�����֐��B
        showCore: function(scene, showFlag) {
            var beginPosX = 0.11 * MahjongTehai.game_.width;
            var beginPosY = 0.87 * MahjongTehai.game_.height;
            var beginPosNakiX = MahjongTehai.game_.width - MahjongPai.sizeX;
            var beginPosNakiY = 0.87 * MahjongTehai.game_.height;
            var directXX = 1;
            var directXY = 0;
            var directYX = 0;
            var directYY = 1;
            var rotate = 0;
            if (this.position === 1) {
                beginPosX = 0.89 * MahjongTehai.game_.width;
                beginPosY = 0.78 * MahjongTehai.game_.height;
                beginPosNakiX = 0.89 * MahjongTehai.game_.width;
                beginPosNakiY = 0;
                directXX = 0;
                directXY = -1;
                directYX = 1;
                directYY = 0;
                rotate = 270;
            } else if (this.position === 2) {
                beginPosX = 0.78 * MahjongTehai.game_.width;
                beginPosY = 0;
                beginPosNakiX = 0;
                beginPosNakiY = 0;
                directXX = -1;
                directXY = 0;
                directYX = 0;
                directYY = -1;
                rotate = 180;
            } else if (this.position === 3) {
                beginPosX = 0;
                beginPosY = 0.11 * MahjongTehai.game_.height;
                beginPosNakiX = 0;
                beginPosNakiY = MahjongTehai.game_.height - MahjongPai.sizeY;
                directXX = 0;
                directXY = 1;
                directYX = -1;
                directYY = 0;
                rotate = 90;
            }
            var posX = beginPosX;
            var posY = beginPosY;
            for (var tehaiI = 0; tehaiI < this.tehai.length; tehaiI++) {
                var paiTehai = this.tehai[tehaiI];
                paiTehai.x = posX;
                paiTehai.y = posY;
                if (this.position == 0 && tehaiI === this.selected) {
                    paiTehai.y -= MahjongPai.sizeY * 0.1;
                }
                paiTehai.rotation = rotate;
                if (!showFlag) {
                    paiTehai.setUra(true);
                }
                scene.addChild(paiTehai);
                posX += directXX * MahjongPai.sizeX;
                posY += directXY * MahjongPai.sizeX;
            }
            posX = beginPosNakiX;
            posY = beginPosNakiY;
            for (var nakiI = this.naki.length - 1; nakiI >= 0; nakiI--) {
                var huro = this.naki[nakiI];
                if (huro.kanFlag !== 2) {
                    if (huro.nakiFrom === 1) {
                        var paiNaki1 = huro.paiNaki;
                        paiNaki1.x = posX + 
                                    directYX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki1.y = posY +
                                    directYY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki1.rotation = rotate - 90;
                        scene.addChild(paiNaki1);
                        if (huro.kanFlag === 1) {
                            var paiKan1 = MahjongPai.Pai();
                            paiKan1.setFrame(huro.paiNaki.str);
                            paiKan1.x = posX +
                                        directYX * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                        directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan1.y = posY+
                                        directYY * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                        directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan1.rotation = rotate - 90;
                            scene.addChild(paiKan1);
                        }
                        posX += -1 * directXX * MahjongPai.sizeY;
                        posY += -1 * directXY * MahjongPai.sizeY;
                        
                        var pai11 = huro.pai1;
                        pai11.x = posX;
                        pai11.y = posY;
                        pai11.rotation = rotate;
                        scene.addChild(pai11);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
        
                        var pai21 = huro.pai2;
                        pai21.x = posX;
                        pai21.y = posY;
                        pai21.rotation = rotate;
                        scene.addChild(pai21);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
                    } else if (huro.nakiFrom === 2) {
                        var pai12 = huro.pai1;
                        pai12.x = posX;
                        pai12.y = posY;
                        pai12.rotation = rotate;
                        scene.addChild(pai12);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
        
                        var paiNaki2 = huro.paiNaki;
                        paiNaki2.x = posX + 
                                    directYX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki2.y = posY +
                                    directYY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki2.rotation = rotate - 90;
                        scene.addChild(paiNaki2);
                        if (huro.kanFlag === 1) {
                            var paiKan2 = MahjongPai.Pai();
                            paiKan2.setFrame(huro.paiNaki.str);
                            paiKan2.x = posX + 
                                    directYX * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                    directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan2.y = posY +
                                    directYY * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                    directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan2.rotation = rotate - 90;
                            scene.addChild(paiKan2);
                        }
                        posX += -1 * directXX * MahjongPai.sizeY;
                        posY += -1 * directXY * MahjongPai.sizeY;
                        
                        var pai22 = huro.pai2;
                        pai22.x = posX;
                        pai22.y = posY;
                        pai22.rotation = rotate;
                        scene.addChild(pai22);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
        
                    } else {
                        var pai13 = huro.pai1;
                        pai13.x = posX;
                        pai13.y = posY;
                        pai13.rotation = rotate;
                        scene.addChild(pai13);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
        
                        var pai23 = huro.pai2;
                        pai23.x = posX;
                        pai23.y = posY;
                        pai23.rotation = rotate;
                        scene.addChild(pai23);
                        posX += -1 * directXX * MahjongPai.sizeX;
                        posY += -1 * directXY * MahjongPai.sizeX;
        
                        var paiNaki3 = huro.paiNaki;
                        paiNaki3.x = posX +
                                    directYX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki3.y = posY +
                                    directYY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2 -
                                    directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                        paiNaki3.rotation = rotate - 90;
                        scene.addChild(paiNaki3);
                        if (huro.kanFlag === 1) {
                            var paiKan3 = MahjongPai.Pai();
                            paiKan3.setFrame(huro.paiNaki.str);
                            paiKan3.x = posX +
                                    directYX * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                    directXX * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan3.y = posY +
                                    directYY * (MahjongPai.sizeY - MahjongPai.sizeX * 3) / 2 -
                                    directXY * (MahjongPai.sizeY - MahjongPai.sizeX) / 2;
                            paiKan3.rotation = rotate - 90;
                            scene.addChild(paiKan3);
                        }
                        posX += -1 * directXX * MahjongPai.sizeY;
                        posY += -1 * directXY * MahjongPai.sizeY;
                    }
                } else {
                    var minimize = 0.75;
                    // �Þ�
                    var pai1an = MahjongPai.Pai();
                    pai1an.setFrame("u0");
                    pai1an.x = posX;
                    pai1an.y = posY;
                    pai1an.rotation = rotate;
                    pai1an.scaleX = MahjongPai.scale * minimize;
                    pai1an.scaleY = MahjongPai.scale * minimize;
                    scene.addChild(pai1an);
                    posX += -1 * directXX * MahjongPai.sizeX * minimize;
                    posY += -1 * directXY * MahjongPai.sizeX * minimize;
                    
                    var pai2an = MahjongPai.Pai();
                    pai2an.setFrame(huro.paiNaki.str);
                    pai2an.x = posX;
                    pai2an.y = posY;
                    pai2an.rotation = rotate;
                    pai2an.scaleX = MahjongPai.scale * minimize;
                    pai2an.scaleY = MahjongPai.scale * minimize;
                    scene.addChild(pai2an);
                    posX += -1 * directXX * MahjongPai.sizeX * minimize;
                    posY += -1 * directXY * MahjongPai.sizeX * minimize;
                    
                    var pai3an = MahjongPai.Pai();
                    pai3an.setFrame(huro.paiNaki.str);
                    pai3an.x = posX;
                    pai3an.y = posY;
                    pai3an.rotation = rotate;
                    pai3an.scaleX = MahjongPai.scale * minimize;
                    pai3an.scaleY = MahjongPai.scale * minimize;
                    scene.addChild(pai3an);
                    posX += -1 * directXX * MahjongPai.sizeX * minimize;
                    posY += -1 * directXY * MahjongPai.sizeX * minimize;
                    
                    var pai4an = MahjongPai.Pai();
                    pai4an.setFrame("u0");
                    pai4an.x = posX;
                    pai4an.y = posY;
                    pai4an.rotation = rotate;
                    pai4an.scaleX = MahjongPai.scale * minimize;
                    pai4an.scaleY = MahjongPai.scale * minimize;
                    scene.addChild(pai4an);
                    posX += -1 * directXX * MahjongPai.sizeX * minimize;
                    posY += -1 * directXY * MahjongPai.sizeX * minimize;
                }
            }
        },
        
        // ��v�̃V�����e�������v�Z����֐��Bpublic
        calcShanten: function() {
            var c = this.calcChitoitsuShanten();
            var k = this.calcKokushiShanten();
            var b = this.calcBaseShanten();
            var min = 13;
            if (c < min) {
                min = c;
            }
            if (k < min) {
                min = k;
            }
            if (b < min) {
                min = b;
            }
            
            return min;
        },
        
        // ���Ύq�܂ŉ��V�����e�����v�Z����֐��Bpublic
        calcChitoitsuShanten: function() {
            if (this.naki.length > 0) {
                return 13;
            }
            var hist = this.toHistogram();
            var toitsu = 0;
            var seed = 0;
            for (var i = 0; i < 34; i++) {
                if (hist[i] > 0) {
                    seed++;
                }
                if (hist[i] >= 2) {
                    toitsu++;
                }
            }
            if (seed > 7) {
                seed = 7;
            }
            hist = null;
            return (13 - toitsu - seed);
        },
        
        // ���m���o�܂ŉ��V�����e�����v�Z����֐��Bpublic
        calcKokushiShanten: function() {
            if (this.naki.length > 0) {
                return 13;
            }
            var hist = this.toHistogram();
            var yaochu = 0;
            var janto = 0;
            var yaochuIndex = [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33];
            for (var i = 0; i < yaochuIndex.length; i++) {
                var num = hist[yaochuIndex[i]];
                if (num > 0) {
                    yaochu++;
                }
                if (janto === 0 && num >= 2) {
                    janto++;
                }
            }
            hist = null;
            yaochuIndex = null;
            return (13 - yaochu - janto);
        },
        
        
        // 4�ʎq1�����P�܂ŉ��V�����e�����v�Z����֐��Bpublic
        calcBaseShanten: function() {
            var hist = this.toHistogram();
            
            // �Ǘ��v����
            for (var aloneI = 0; aloneI < hist.length; aloneI++) {
                if (hist[aloneI] == 1) {
                    if (aloneI >= 27) {
                            hist[aloneI] = 0;
                    } else {
                        var num = (aloneI % 9) + 1;
                        if (num === 1) {
                            if (hist[aloneI + 1] + hist[aloneI + 2] === 0) {
                                hist[aloneI] = 0;
                            }
                        } else if (num === 9) {
                            if (hist[aloneI - 2] + hist[aloneI - 1] === 0) {
                                hist[aloneI] = 0;
                            }
                        } else if (num === 2) {
                            if (hist[aloneI - 1] + hist[aloneI + 1] + hist[aloneI + 2] === 0) {
                                hist[aloneI] = 0;
                            }
                        } else if (num === 8) {
                            if (hist[aloneI - 2] + hist[aloneI - 1] + hist[aloneI + 1] === 0) {
                                hist[aloneI] = 0;
                            }
                        } else {
                            if (hist[aloneI - 2] + hist[aloneI - 1] + hist[aloneI + 1] + hist[aloneI + 2] === 0) {
                                hist[aloneI] = 0;
                            }
                        }
                    }
                }
            }
            
            var tatsuCalc = function (h, index) {
                while (h[index] === 0) {
                    index++;
                }
                if (index >= h.length) {
                    return 0;
                }
                // �Ύq
                if (h[index] >= 2) {
                    h[index] -= 2;
                    return (tatsuCalc(h, index) + 1);
                }
                
                // ���v�͏��q�̓��q�͎��Ȃ�
                if (index >= 27) {
                    return tatsuCalc(h, index + 1);
                }
                var num = (index % 9) + 1;
                // �Ӓ��A����
                if (num < 9) {
                    if (h[index + 1] > 0) {
                        h[index]--;
                        h[index + 1]--;
                        return (tatsuCalc(h, index) + 1);
                    }
                }
                
                // �ƒ�
                if (num < 8) {
                    if (h[index + 2] > 0) {
                        h[index]--;
                        h[index + 2]--;
                        return (tatsuCalc(h, index) + 1);
                    }
                }
                return tatsuCalc(h, index + 1);
            };
            
            var mentsuCalc = function(h, index, mentsu) {
                while (h[index] === 0) {
                    index++;
                }
                if (index >= h.length) {
                    var tatsu = tatsuCalc(h, 0);
                    if (mentsu + tatsu > 4) {
                        tatsu = 4 - mentsu;
                    }
                    return (8 - mentsu * 2 - tatsu);
                }
                if (index >= 27) {
                    // ���v�͍��q�̂�
                    if(h[index] >= 3) {
                        h[index] -= 3;
                        return mentsuCalc(h, index + 1, mentsu + 1);
                    }
                } else {
                    // ���v�͏��q�ƍ��q���l��
                    var num = (index % 9) + 1;
                    var skipClone = h.concat();
                    var shanten = mentsuCalc(skipClone, index + 1, mentsu);
                    skipClone = null;
                    if (num < 8 && h[index + 1] > 0 && h[index + 2] > 0) {
                        // ���q������ꍇ
                        if (h[index] >= 3) {
                            // ���q�����q���Ƃ��ꍇ
                            var shuntsuClone = h.concat();
                            shuntsuClone[index]--;
                            shuntsuClone[index + 1]--;
                            shuntsuClone[index + 2]--;
                            var shuntsuShanten2 = mentsuCalc(shuntsuClone, index, mentsu + 1);
                            var kotsuClone = h.concat();
                            kotsuClone[index] -= 3;
                            var kotsuShanten2 = mentsuCalc(kotsuClone, index, mentsu + 1);
                            if (shanten === undefined || shuntsuShanten2 < shanten) {
                                shanten = shuntsuShanten2;
                            }
                            if (shanten === undefined || kotsuShanten2 < shanten) {
                                shanten = kotsuShanten2;
                            }
                            shuntsuClone = null;
                            kotsuClone = null;
                        } else {
                            // ���q�̂ݎ���ꍇ
                            h[index]--;
                            h[index + 1]--;
                            h[index + 2]--;
                            var shuntsuShanten1 = mentsuCalc(h, index, mentsu + 1);
                            if (shanten === undefined || shuntsuShanten1 < shanten) {
                                shanten = shuntsuShanten1;
                            }
                        }
                    } else {
                        if (h[index] >= 3) {
                            // ���q�̂ݎ���ꍇ
                            h[index] -= 3;
                            var kotsuShanten1 = mentsuCalc(h, index, mentsu + 1);
                            if (shanten === undefined || kotsuShanten1 < shanten) {
                                shanten = kotsuShanten1;
                            }
                        }
                    }
                    return shanten;
                }
                return mentsuCalc(h, index + 1, mentsu);
            };
            
            var cloneHist = hist.concat();
            var min = mentsuCalc(cloneHist, 0, this.naki.length);
            for (var histI = 0; histI < 34; histI++) {
                if (hist[histI] >= 2) {
                    cloneHist = hist.concat();
                    cloneHist[histI] -= 2;
                    var shanten = mentsuCalc(cloneHist, 0, this.naki.length) - 1;
                    if (min > shanten) {
                        min = shanten;
                    }
                }
            }
            cloneHist = null;
            hist = null;
            tatsuCalc = null;
            mentsuCalc = null;
            return min;
        },
        
        // ���v���̑҂��v���v�Z����֐��Bpublic
        getMachi: function() {
            if (this.calcShanten() === 0) {
                return this.getYuko();
            }
            return null;
        },
        
        // �L���v��Ԃ��֐��Bpublic
        getYuko: function() {
            if (this.isTsumoban()) {
                var yukohais = [];
                var nowShanten = this.calcShanten();
                for (var i = 0; i < 34; i++) {
                    var pai = MahjongPai.Pai();
                    pai.setFrame(MahjongPai.numToStr(i));
                    var cloneTehai = this.clone();
                    cloneTehai.add(pai);
                    if (cloneTehai.calcShanten() === nowShanten - 1) {
                        yukohais.push(pai);
                    }
                    cloneTehai = null;
                    pai = null;
                }
                return yukohais;
            }
            return null;
        },
        
        // �c���Ԃ����肷��֐��Bpublic
        isTsumoban: function() {
            return (this.tehai.length % 3 === 1);
        },
        
        // �؂�Ԃ����肷��֐��Bpublic
        isKiriban: function() {
            return (this.tehai.length % 3 === 2);
        },
        
        // ���v�����肷��֐��Bpublic
        isShoupai: function() {
            return (this.tehai.length % 3 === 0);
        },
        
        //�c���t���O�𗧂Ă�֐��Bpublic
        setTsumo: function(flag) {
            this.tsumoFlag = flag;
        },
        
        //�c���t���̃Q�b�^�[�Bpublic
        isTsumo: function() {
            return this.tsumoFlag;
        },
        
        // ���ȃt���O�𗧂Ă�֐��Bpublic
        setChankan: function(flag) {
            this.chankanFlag = flag;
        },
        
        // ���ȃt���O�̃Q�b�^�[�Bpublic
        isChankan: function() {
            return this.chankanFlag;
        },
        
        // �V�a�t���O�𗧂Ă�֐��Bpublic
        setTenho: function(flag) {
            this.tenhoFlag = flag;
        },
        
        // �V�a�t���O�̃Q�b�^�[�Bpublic
        isTenho: function() {
            return this.tenhoFlag;
        },
        
        // �n�a�t���O�𗧂Ă�֐��Bpublic
        setChiho: function(flag) {
            this.chihoFlag = flag;
        },
        
        // �n�a�t���O�̃Q�b�^�[�Bpublic
        isChiho: function() {
            return this.chihoFlag;
        },
        
        // �����t���O�𗧂Ă�֐��Bpublic
        setReach: function(flag) {
            this.reachFlag = flag;
        },
        
        // �����t���O�̃Q�b�^�[�Bpublic
        isReach: function() {
            return this.reachFlag;
        },
        
        // �_�u�������t���O�𗧂Ă�֐��Bpublic
        setDoubleReach: function(flag) {
            this.doubleReachFlag = flag;
            if (flag) {
                this.reachFlag = true;
            }
        },
        
        // �_�u�������t���O�̃Q�b�^�[�Bpublic
        isDoubleReach: function() {
            return this.doubleReachFlag;
        },
        
        // �ꔭ�t���O�𗧂Ă�֐��Bpublic
        setIppatsu: function(flag) {
            this.ippatsuFlag = flag;
        },
        
        // �ꔭ�t���O�̃Q�b�^�[�Bpublic
        isIppatsu: function() {
            return this.ippatsuFlag;
        },
        
        // ���t���O�𗧂Ă�֐��Bpublic
        setRinshan: function(flag) {
            this.rinshanFlag = flag;
        },
        
        // ���t���O�̃Q�b�^�[�Bpublic
        isRinshan: function() {
            return this.rinshanFlag;
        },
        
        // �C��t���O�𗧂Ă�֐��Bpublic
        setHaitei: function(flag) {
            this.haiteiFlag = flag;
        },
        
        // �C��t���O�̃Q�b�^�[�Bpublic
        isHaitei: function() {
            return this.haiteiFlag;
        },
        
        // �h����ݒ肷��֐��Bpublic
        setDoras: function(doras) {
            this.doras = doras;
        },
        
        // �h���̃Q�b�^�[�Bpublic
        getDoras: function() {
            return this.doras;
        },
        
        // �_�����v�Z����֐��Bpublic
        calcPoint: function(ba, kaze) {
            this.sort();
            if (this.calcShanten() === -1) {
                if (this.calcChitoitsuShanten() === -1 && !this.isRyanpeikou()) {
                    var splitMentsu = MahjongTehai.MentsuSeparatedTehai();
                    splitMentsu.setTehai(this);
                    var fan = splitMentsu.calcFan(ba, kaze);
                    return MahjongTehai.calcPointFromHuAndFan(25, [2 + fan[0], '���Ύq,' + fan[1]], this.isTsumo(), kaze === 'z1');
                } else if (this.calcKokushiShanten() === -1) {
                    return MahjongTehai.calcPointFromHuAndFan(20, [13, '���m���o'], this.isTsumo(), kaze === 'z1');
                } else {
                    var maxPoint = [0, 0, '�`�����{', ''];
                    var splitMentsuList = this.splitMentsu();
                    for (var i = 0; i < splitMentsuList.length; i++) {
                        var point = splitMentsuList[i].calcPoint(ba, kaze, this.isTsumo(), kaze === 'z1');
                        if (maxPoint[1] < point[1]) {
                            maxPoint = point;
                        }
                    }
                    return maxPoint;
                }
            }
            return [0, 0, '�`�����{', ''];
        },
        
        // ��v��ʎq���Ƃɕ�����֐��B
        splitMentsu: function() {
            var list = [];
            var hist = this.toHistogram();
            var splitTehai = MahjongTehai.MentsuSeparatedTehai();
            splitTehai.setTehai(this);
            var cloneHist = null;
            
            var removeMentsu = function(l, h, s) {
                var restFind = false;
                for (var i = 0; i < 34; i++) {
                    var removed = false;
                    if (h[i] > 0) {
                        restFind = true;
                        var num = (i % 9) + 1;
                        if (i < 27) {
                            // ���v�̏ꍇ���q������
                            if (num <= 7) {
                                if (h[i] > 0 && h[i + 1] > 0 && h[i + 2] > 0) {
                                    var shuntsuHist = h.concat();
                                    var shuntsuSplitTehai = s.clone();
                                    shuntsuHist[i]--;
                                    shuntsuHist[i + 1]--;
                                    shuntsuHist[i + 2]--;
                                    var shuntsu = MahjongTehai.Naki();
                                    shuntsu.setMentsu(MahjongPai.numToStr(i) + MahjongPai.numToStr(i + 1) + MahjongPai.numToStr(i + 2));
                                    shuntsuSplitTehai.addMentsu(shuntsu);
                                    removeMentsu(l, shuntsuHist, shuntsuSplitTehai);
                                    
                                    shuntsuHist = null;
                                    shuntsuSplitTehai = null;
                                    shuntsu = null;
                                    
                                    removed = true;
                                }
                            }
                        }
                        if (h[i] >= 3) {
                            var kotsuHist = h.concat();
                            var kotsuSplitTehai = s.clone();
                            kotsuHist[i] -= 3;
                            var kotsu = MahjongTehai.Naki();
                            kotsu.setMentsu(MahjongPai.numToStr(i) + MahjongPai.numToStr(i) + MahjongPai.numToStr(i));
                            kotsuSplitTehai.addMentsu(kotsu);
                            removeMentsu(l, kotsuHist, kotsuSplitTehai);
                            
                            kotsuHist = null;
                            kotsuSplitTehai = null;
                            kotsu = null;
                            
                            removed = true;
                        }
                    }
                    if (removed) {
                        break;
                    }
                }
                if (!restFind) {
                    l.push(s);
                }
            };
            
            var machiSet = function(list, finishPai) {
                var machiList = [];
                for (var i = 0; i < list.length; i++) {
                    var s = list[i];
                    for (var ryanmenJ = 0; ryanmenJ < s.mentsu.length; ryanmenJ++) {
                        var mentsuRyanmen = s.getMentsu(ryanmenJ);
                        if (mentsuRyanmen.kanFlag === -1 && mentsuRyanmen.isShuntsu()) {
                            if (mentsuRyanmen.paiNaki.str === finishPai.str && finishPai.getNum() !== 7) {
                                var sRyanmen7 = s.clone();
                                sRyanmen7.setFinishShape(0);
                                machiList.push(sRyanmen7);
                                break;
                            } else if (mentsuRyanmen.pai2.str === finishPai.str && finishPai.getNum() !== 3) {
                                var sRyanmen3 = s.clone();
                                sRyanmen3.setFinishShape(0);
                                machiList.push(sRyanmen3);
                                break;
                            }
                        }
                    }
                    for (var shaboJ = 0; shaboJ < s.mentsu.length; shaboJ++) {
                        var mentsuShabo = s.getMentsu(shaboJ);
                        if (mentsuShabo.kanFlag === -1 && mentsuShabo.isKotsu()) {
                            if (mentsuShabo.paiNaki.str === finishPai.str) {
                                var sShabo = s.clone();
                                sShabo.setFinishShape(1);
                                machiList.push(sShabo);
                                break;
                            }
                        }
                    }
                    for (var kanchanJ = 0; kanchanJ < s.mentsu.length; kanchanJ++) {
                        var mentsuKanchan = s.getMentsu(kanchanJ);
                        if (mentsuKanchan.kanFlag === -1 && mentsuKanchan.isShuntsu()) {
                            if (mentsuKanchan.pai1.str === finishPai.str) {
                                var sKanchan = s.clone();
                                sKanchan.setFinishShape(2);
                                machiList.push(sKanchan);
                                break;
                            }
                        }
                    }
                    for (var penchanJ = 0; penchanJ < s.mentsu.length; penchanJ++) {
                        var mentsuPenchan = s.getMentsu(penchanJ);
                        if (mentsuPenchan.kanFlag === -1 && mentsuPenchan.isShuntsu()) {
                            if (mentsuPenchan.paiNaki.str === finishPai.str && finishPai.getNum() === 7) {
                                var sPenchan7 = s.clone();
                                sPenchan7.setFinishShape(3);
                                machiList.push(sPenchan7);
                                break;
                            } else if (mentsuPenchan.pai2.str === finishPai.str && finishPai.getNum() === 3) {
                                var sPenchan3 = s.clone();
                                sPenchan3.setFinishShape(3);
                                machiList.push(sPenchan3);
                                break;
                            }
                        }
                    }
                    if (s.janto.str === finishPai.str) {
                        var sTanki = s.clone();
                        sTanki.setFinishShape(4);
                        machiList.push(sTanki);
                    }
                }
                return machiList;
            };
            
            for (var i = 0; i < 34; i++) {
                if (hist[i] >= 2) {
                    cloneHist = hist.concat();
                    cloneHist[i] -= 2;
                    splitTehai.setJanto(MahjongPai.numToStr(i));
                    removeMentsu(list, cloneHist, splitTehai);
                }
            }
            list = machiSet(list, this.lastAddPai);
            
            hist = null;
            cloneHist = null;
            return list;
        },
        
        // ��u�����ǂ������肷��֐��Bpublic
        isRyanpeikou: function() {
            // ��u�������͎��Ύq�Əd�Ȃ�̂œ��ʂɔ���
            if (this.calcChitoitsuShanten() === -1 || (this.calcBaseShanten() === -1)) {
                var hist = this.toHistogram();
                var peikou = 0;
                for (var manzuI = 0; manzuI < 7; manzuI++) {
                    if (hist[manzuI] >= 2 && hist[manzuI + 1] >= 2 && hist[manzuI + 2] >= 2) {
                        hist[manzuI] -= 2;
                        hist[manzuI + 1] -= 2;
                        hist[manzuI + 2] -= 2;
                        peikou++;
                    }
                    if (hist[manzuI] >= 2 && hist[manzuI + 1] >= 2 && hist[manzuI + 2] >= 2) {
                        hist[manzuI] -= 2;
                        hist[manzuI + 1] -= 2;
                        hist[manzuI + 2] -= 2;
                        peikou++;
                    }
                }
                for (var sozuI = 9; sozuI < 16; sozuI++) {
                    if (hist[sozuI] >= 2 && hist[sozuI + 1] >= 2 && hist[sozuI + 2] >= 2) {
                        hist[sozuI] -= 2;
                        hist[sozuI + 1] -= 2;
                        hist[sozuI + 2] -= 2;
                        peikou++;
                    }
                    if (hist[sozuI] >= 2 && hist[sozuI + 1] >= 2 && hist[sozuI + 2] >= 2) {
                        hist[sozuI] -= 2;
                        hist[sozuI + 1] -= 2;
                        hist[sozuI + 2] -= 2;
                        peikou++;
                    }
                }
                for (var pinzuI = 18; pinzuI < 15; pinzuI++) {
                    if (hist[pinzuI] >= 2 && hist[pinzuI + 1] >= 2 && hist[pinzuI + 2] >= 2) {
                        hist[pinzuI] -= 2;
                        hist[pinzuI + 1] -= 2;
                        hist[pinzuI + 2] -= 2;
                        peikou++;
                    }
                    if (hist[pinzuI] >= 2 && hist[pinzuI + 1] >= 2 && hist[pinzuI + 2] >= 2) {
                        hist[pinzuI] -= 2;
                        hist[pinzuI + 1] -= 2;
                        hist[pinzuI + 2] -= 2;
                        peikou++;
                    }
                }
                hist = null;
                if (peikou >= 2) {
                    return true;
                }
            }
            return false;
        }
    });
    
    // ���̃N���X
    MahjongTehai.Rule = {};
    
    // ����̖�
    MahjongTehai.Rule.rules = [
        // �|���̑������ɔ���
        // ��
        // �V�a
        function(tehai, ba, kaze) {
            if (tehai.tehai.isTenho()) {
                return [13, '�V�a'];
            }
            return [0, ''];
        },
        // �n�a
        function(tehai, ba, kaze) {
            if (tehai.tehai.isChiho()) {
                return [13, '�n�a'];
            }
            return [0, ''];
        },
        // �l�Í�
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                if (tehai.countAnko() == 4) {
                    if (tehai.finishShape === 1 && tehai.tehai.isTsumo()) {
                        return [13, '�l�Í�'];
                    } else if (tehai.finishShape === 4) {
                        return [26, '�l�Í��P�R'];
                    }
                }
            }
            return [0, ''];
        },
        // ��O��
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var sangenCount = 0;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (mentsu.pai1.str === 'z5') {
                        sangenCount++;
                    }
                    if (mentsu.pai1.str === 'z6') {
                        sangenCount++;
                    }
                    if (mentsu.pai1.str === 'z7') {
                        sangenCount++;
                    }
                    mentsu = null;
                }
                if (sangenCount == 3) {
                    return [13, '��O��'];
                }
            }
            return [0, ''];
        },
        // ����F
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            for (var i = 0; i < hist.length; i++) {
                if (i < 27 && hist[i] > 0) {
                    return [0, ''];
                }
            }
            return [13, '����F'];
        },
        // ���l��
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var kazeCount = 0;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (mentsu.pai1.str === 'z1') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z2') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z3') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z4') {
                        kazeCount++;
                    }
                    mentsu = null;
                }
                if (kazeCount == 3 && (tehai.janto.str === 'z1' || tehai.janto.str === 'z2' || tehai.janto.str === 'z3' || tehai.janto.str === 'z4')) {
                    return [13, '���l��'];
                }
            }
            return [0, ''];
        },
        // ��l��
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var kazeCount = 0;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (mentsu.pai1.str === 'z1') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z2') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z3') {
                        kazeCount++;
                    }
                    if (mentsu.pai1.str === 'z4') {
                        kazeCount++;
                    }
                    mentsu = null;
                }
                if (kazeCount == 4) {
                    return [26, '��l��'];
                }
            }
            return [0, ''];
        },
        // �Έ�F
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            for (var i = 0; i < hist.length; i++) {
                if (hist[i] > 0) {
                    if (!(i === 10 || i === 11 || i === 12 || i === 14 || i === 16 || i === 32)) {
                        return [0, ''];
                    }
                }
            }
            return [13, '�Έ�F'];
        },
        // ���V��
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var onlyIku = true;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (mentsu.isShuntsu()) {
                        mentsu = null;
                        return [0, ''];
                    }
                    if (!mentsu.isIku()) {
                        mentsu = null;
                        return [0, ''];
                    }
                    mentsu = null;
                }
                var jantoType = tehai.janto.str.substr(0, 1);
                var jantoNum = parseInt(tehai.janto.str.substr(1, 1), 10);
                if (jantoType === 'z') {
                    return [0, ''];
                }
                if (jantoNum !== 1 && jantoNum !== 9) {
                    return [0, ''];
                }
                return [13, '���V��'];
            }
            return [0, ''];
        },
        // �l�Ȏq
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                if (tehai.countKan() === 4) {
                    return [13, '�l�Ȏq'];
                }
            }
            return [0, ''];
        },
        // ��@��
        function(tehai, ba, kaze) {
            if (tehai.isMenzen()) {
                var hist = tehai.tehai.toHistogramAll();
                for (var i = 0; i < 3; i++) {
                    if (hist[i * 9] >= 3 &&
                        hist[i * 9 + 1] >= 1 &&
                        hist[i * 9 + 2] >= 1 &&
                        hist[i * 9 + 3] >= 1 &&
                        hist[i * 9 + 4] >= 1 &&
                        hist[i * 9 + 5] >= 1 &&
                        hist[i * 9 + 6] >= 1 &&
                        hist[i * 9 + 7] >= 1 &&
                        hist[i * 9 + 8] >= 3) {
                        return [13, '��@��'];
                    }
                }
            }
            return [0, ''];
        },
        
        // �Z��
        // ����F
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            var mHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var sHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var pHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var zHist = [0, 0, 0, 0, 0, 0, 0];
            for (var histSplitI = 0; histSplitI < 34; histSplitI++) {
                if (histSplitI < 9) {
                    mHist[histSplitI] = hist[histSplitI];
                } else if (histSplitI < 18) {
                    sHist[histSplitI - 9] = hist[histSplitI];
                } else if (histSplitI < 27) {
                    pHist[histSplitI - 18] = hist[histSplitI];
                } else if (histSplitI < 34) {
                    zHist[histSplitI - 27] = hist[histSplitI];
                }
            }
            var suColors = 0;
            for (var manzuI = 0; manzuI < 9; manzuI++) {
                if(mHist[manzuI] > 0) {
                    suColors++;
                    break;
                }
            }
            for (var sozuI = 0; sozuI < 9; sozuI++) {
                if(sHist[sozuI] > 0) {
                    suColors++;
                    break;
                }
            }
            for (var pinzuI = 0; pinzuI < 9; pinzuI++) {
                if(pHist[pinzuI] > 0) {
                    suColors++;
                    break;
                }
            }
            var hasTsu = false;
            for (var tsuI = 0; tsuI < 7; tsuI++) {
                if(zHist[tsuI] > 0) {
                    hasTsu = true;
                    break;
                }
            }
            if (suColors === 1 && !hasTsu) {
                if (tehai.isMenzen()) {
                    return [6, '����F'];
                } else {
                    return [5, '����F'];
                }
            }
            return [0, ''];
        },
        
        // �O��
        // ����F
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            var mHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var sHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var pHist = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            var zHist = [0, 0, 0, 0, 0, 0, 0];
            for (var histSplitI = 0; histSplitI < 34; histSplitI++) {
                if (histSplitI < 9) {
                    mHist[histSplitI] = hist[histSplitI];
                } else if (histSplitI < 18) {
                    sHist[histSplitI - 9] = hist[histSplitI];
                } else if (histSplitI < 27) {
                    pHist[histSplitI - 18] = hist[histSplitI];
                } else if (histSplitI < 34) {
                    zHist[histSplitI - 27] = hist[histSplitI];
                }
            }
            var suColors = 0;
            for (var manzuI = 0; manzuI < 9; manzuI++) {
                if(mHist[manzuI] > 0) {
                    suColors++;
                    break;
                }
            }
            for (var sozuI = 0; sozuI < 9; sozuI++) {
                if(sHist[sozuI] > 0) {
                    suColors++;
                    break;
                }
            }
            for (var pinzuI = 0; pinzuI < 9; pinzuI++) {
                if(pHist[pinzuI] > 0) {
                    suColors++;
                    break;
                }
            }
            var hasTsu = false;
            for (var tsuI = 0; tsuI < 7; tsuI++) {
                if(zHist[tsuI] > 0) {
                    hasTsu = true;
                    break;
                }
            }
            if (suColors === 1 && hasTsu) {
                if (tehai.isMenzen()) {
                    return [3, '����F'];
                } else {
                    return [2, '����F'];
                }
            }
            return [0, ''];
        },
        // ���S��?��
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (!mentsu.isIku()) {
                        mentsu = null;
                        return [0, ''];
                    }
                    mentsu = null;
                }
                var jantoType = tehai.janto.str.substr(0, 1);
                var jantoNum = parseInt(tehai.janto.str.substr(1, 1), 10);
                if (jantoType === 'z') {
                    return [0, ''];
                }
                if (jantoNum !== 1 && jantoNum !== 9) {
                    return [0, ''];
                }
                if (tehai.isMenzen()) {
                    return [3, '���S��?��'];
                } else {
                    return [2, '���S��?��'];
                }
            }
            return [0, ''];
        },
        // ��u��
        function(tehai, ba, kaze) {
            if(tehai.tehai.isRyanpeikou()){
                return [3, '��u��'];
            }
            return [0, ''];
        },
        
        // ����
        // �O�F����
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var shuntsuMinPaiHist = [];
                for (var initI = 0; initI < 34; initI++) {
                    shuntsuMinPaiHist.push(0);
                }
                for (var mentsuI = 0; mentsuI < tehai.mentsu.length; mentsuI++) {
                    if (tehai.mentsu[mentsuI].isShuntsu()) {
                        var pai1Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai1.str);
                        var pai2Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai2.str);
                        var paiNakiNum = MahjongPai.strToNum(tehai.mentsu[mentsuI].paiNaki.str);
                        
                        var minPaiNum = pai1Num;
                        if (pai2Num < minPaiNum) {
                            minPaiNum = pai2Num;
                        }
                        if (paiNakiNum < minPaiNum) {
                            minPaiNum = paiNakiNum;
                        }
                        
                        shuntsuMinPaiHist[minPaiNum]++;
                    }
                }
                for (var countI = 0; countI < 9; countI++) {
                    if (shuntsuMinPaiHist[countI] > 0 &&
                        shuntsuMinPaiHist[countI + 9] > 0 &&
                        shuntsuMinPaiHist[countI + 18] > 0) {
                        if (tehai.isMenzen()) {
                            return [2, '�O�F����'];
                        } else {
                            return [1, '�O�F����'];
                        }
                    }
                }
            }
            return [0, ''];
        },
        // ��C�ʊ�
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var shuntsuMinPaiHist = [];
                for (var initI = 0; initI < 34; initI++) {
                    shuntsuMinPaiHist.push(0);
                }
                for (var mentsuI = 0; mentsuI < tehai.mentsu.length; mentsuI++) {
                    if (tehai.mentsu[mentsuI].isShuntsu()) {
                        var pai1Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai1.str);
                        var pai2Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai2.str);
                        var paiNakiNum = MahjongPai.strToNum(tehai.mentsu[mentsuI].paiNaki.str);
                        
                        var minPaiNum = pai1Num;
                        if (pai2Num < minPaiNum) {
                            minPaiNum = pai2Num;
                        }
                        if (paiNakiNum < minPaiNum) {
                            minPaiNum = paiNakiNum;
                        }
                        
                        shuntsuMinPaiHist[minPaiNum]++;
                    }
                }
                for (var countI = 0; countI < 3; countI++) {
                    if (shuntsuMinPaiHist[countI * 9] > 0 &&
                        shuntsuMinPaiHist[countI * 9 + 3] > 0 &&
                        shuntsuMinPaiHist[countI * 9 + 6] > 0) {
                        if (tehai.isMenzen()) {
                            return [2, '��C�ʊ�'];
                        } else {
                            return [1, '��C�ʊ�'];
                        }
                    }
                }
            }
            return [0, ''];
        },
        // ���S��?��
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var hasTsu = false;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (!mentsu.isYaochu()) {
                        mentsu = null;
                        return [0, ''];
                    } else if (mentsu.isTsu()) {
                        hasTsu = true;
                    }
                    mentsu = null;
                }
                var jantoType = tehai.janto.str.substr(0, 1);
                var jantoNum = parseInt(tehai.janto.str.substr(1, 1), 10);
                
                if (jantoType !== 'z' && jantoNum !== 1 && jantoNum !== 9) {
                    return [0, ''];
                }
                if (tehai.countKotsu() === 4) {
                    return [0, ''];
                }
                
                
                if (hasTsu || jantoType === 'z') {
                    if (tehai.isMenzen()) {
                        return [2, '���S��?��'];
                    } else {
                        return [1, '���S��?��'];
                    }
                }
            }
            return [0, ''];
        },
        // �΁X�a
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                if (tehai.countKotsu() === 4) {
                    return [2, '�΁X�a'];
                }
            }
            return [0, ''];
        },
        // �O�Í�
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                if (tehai.countAnko() == 3) {
                    if (tehai.finishShape === 1) {
                        if (tehai.tehai.isTsumo()) {
                            return [2, '�O�Í�'];
                        }
                    } else {
                        return [2, '�O�Í�'];
                    }
                }
            }
            return [0, ''];
        },
        // ���V��
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            for (var i = 0; i < 34; i++) {
                if (hist[i] > 0) {
                    if (i > 0 && i < 8) {
                        return [0, ''];
                    }
                    if (i > 9 && i < 17) {
                        return [0, ''];
                    }
                    if (i > 18 && i < 26) {
                        return [0, ''];
                    }
                }
            }
            return [2, '���V��'];
        },
        // �O�F����
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var kotsuMinPaiHist = [];
                for (var initI = 0; initI < 34; initI++) {
                    kotsuMinPaiHist.push(0);
                }
                for (var mentsuI = 0; mentsuI < tehai.mentsu.length; mentsuI++) {
                    if (tehai.mentsu[mentsuI].isKotsu()) {
                        var pai1Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai1.str);
                        
                        kotsuMinPaiHist[pai1Num]++;
                    }
                }
                for (var countI = 0; countI < 9; countI++) {
                    if (kotsuMinPaiHist[countI] > 0 &&
                        kotsuMinPaiHist[countI + 9] > 0 &&
                        kotsuMinPaiHist[countI + 18] > 0) {
                        return [2, '�O�F����'];
                    }
                }
            }
            return [0, ''];
        },
        // �O�Ȏq
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                if (tehai.countKan() === 3) {
                    return [2, '�O�Ȏq'];
                }
            }
            return [0, ''];
        },
        // ���O��
        function(tehai, ba, kaze) {
            if(tehai.is4Mentsu()){
                var sangenCount = 0;
                for (var i = 0; i < 4; i++) {
                    var mentsu = tehai.getMentsu(i);
                    if (mentsu.pai1.str === 'z5') {
                        sangenCount++;
                    }
                    if (mentsu.pai1.str === 'z6') {
                        sangenCount++;
                    }
                    if (mentsu.pai1.str === 'z7') {
                        sangenCount++;
                    }
                    mentsu = null;
                }
                if (sangenCount == 2 && MahjongPai.strToNum(tehai.janto.str) >= 31) {
                    return [2, '���O��'];
                }
            }
            return [0, ''];
        },
        // �_�u������
        function(tehai, ba, kaze) {
            if (tehai.tehai.isDoubleReach()) {
                return [2, '�_�u������'];
            }
            return [0, ''];
        },
        
        // ����
        // ����
        function(tehai, ba, kaze) {
            if (tehai.tehai.isReach() && !tehai.tehai.isDoubleReach()) {
                return [1, '����'];
            }
            return [0, ''];
        },
        // �ꔭ
        function(tehai, ba, kaze) {
            if (tehai.tehai.isIppatsu()) {
                return [1, '�ꔭ'];
            }
            return [0, ''];
        },
        // ��O�����̘a
        function(tehai, ba, kaze) {
            if (tehai.isMenzen() && tehai.tehai.isTsumo()) {
                return [1, '��O�����̘a'];
            }
            return [0, ''];
        },
        // �f?��
        function(tehai, ba, kaze) {
            var hist = tehai.tehai.toHistogramAll();
            for (var i = 0; i < 34; i++) {
                if (hist[i] > 0) {
                    if (i === 0 || i === 8) {
                        return [0, ''];
                    }
                    if (i === 9 || i === 17) {
                        return [0, ''];
                    }
                    if (i === 18 || i === 26) {
                        return [0, ''];
                    }
                    if (i >= 27) {
                        return [0, ''];
                    }
                }
            }
            return [1, '�f?��'];
        },
        // ���a
        function(tehai, ba, kaze) {
            if (!tehai.is4Mentsu()) {
                return [0, ''];
            }
            for (var i = 0; i < 4; i++) {
                var mentsu = tehai.getMentsu(i);
                if (!mentsu.isShuntsu()) {
                    return [0, ''];
                }
                mentsu = null;
            }
            var jantoType = tehai.janto.str.substr(0, 1);
            var jantoNum = parseInt(tehai.janto.str.substr(1, 1), 10);
            if (jantoType === 'z') {
                if (jantoNum >= 5) {
                    return [0, ''];
                } else {
                    if (tehai.janto.str === ba || tehai.janto.str === kaze) {
                        return [0, ''];
                    }
                }
            }
            if (tehai.finishShape !== 0) {
                return [0, ''];
            }
            return [1, '���a'];
        },
        // ��u��
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu() && !tehai.tehai.isRyanpeikou()) {
                var shuntsuMinPaiHist = [];
                for (var initI = 0; initI < 34; initI++) {
                    shuntsuMinPaiHist.push(0);
                }
                for (var mentsuI = 0; mentsuI < tehai.mentsu.length; mentsuI++) {
                    if (tehai.mentsu[mentsuI].isShuntsu()) {
                        var pai1Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai1.str);
                        var pai2Num = MahjongPai.strToNum(tehai.mentsu[mentsuI].pai2.str);
                        var paiNakiNum = MahjongPai.strToNum(tehai.mentsu[mentsuI].paiNaki.str);
                        
                        var minPaiNum = pai1Num;
                        if (pai2Num < minPaiNum) {
                            minPaiNum = pai2Num;
                        }
                        if (paiNakiNum < minPaiNum) {
                            minPaiNum = paiNakiNum;
                        }
                        
                        shuntsuMinPaiHist[minPaiNum]++;
                    }
                }
                for (var countI = 0; countI < 34; countI++) {
                    if (shuntsuMinPaiHist[countI] >= 2) {
                        if (tehai.isMenzen()) {
                            return [1, '��u��'];
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // �����v
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu()) {
                for (var i = 0; i < tehai.mentsu.length; i++) {
                    if (tehai.mentsu[i].isKotsu()) {
                        if (tehai.mentsu[i].pai1.str === ba) {
                            return [1, '�ꕗ'];      
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // �啗�v
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu()) {
                for (var i = 0; i < tehai.mentsu.length; i++) {
                    if (tehai.mentsu[i].isKotsu()) {
                        if (tehai.mentsu[i].pai1.str === kaze) {
                            return [1, '����'];      
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // ��
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu()) {
                for (var i = 0; i < tehai.mentsu.length; i++) {
                    if (tehai.mentsu[i].isKotsu()) {
                        if (tehai.mentsu[i].pai1.str === 'z5') {
                            return [1, '��'];      
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // �
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu()) {
                for (var i = 0; i < tehai.mentsu.length; i++) {
                    if (tehai.mentsu[i].isKotsu()) {
                        if (tehai.mentsu[i].pai1.str === 'z6') {
                            return [1, '�'];      
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // ��
        function(tehai, ba, kaze) {
            if (tehai.is4Mentsu()) {
                for (var i = 0; i < tehai.mentsu.length; i++) {
                    if (tehai.mentsu[i].isKotsu()) {
                        if (tehai.mentsu[i].pai1.str === 'z7') {
                            return [1, '��'];      
                        }
                    }
                }
            }
            return [0, ''];      
        },
        // ���J��
        function(tehai, ba, kaze) {
            if (tehai.tehai.isRinshan() && tehai.tehai.isTsumo()) {
                return [1, '���J��'];
            }
            return [0, ''];
        },
        // ����
        function(tehai, ba, kaze) {
            if (tehai.tehai.isChankan()) {
                return [1, '����'];
            }
            return [0, ''];
        },
        // �C��̌�
        function(tehai, ba, kaze) {
            if (tehai.tehai.isHaitei() && tehai.tehai.isTsumo()) {
                return [1, '�C��̌�'];
            }
            return [0, ''];
        },
        // �͒ꝝ��
        function(tehai, ba, kaze) {
            if (tehai.tehai.isHaitei() && !tehai.tehai.isTsumo()) {
                return [1, '�͒ꝝ��'];
            }
            return [0, ''];
        },
    ];
    
    MahjongTehai.Rule.ruleSize = function() {
        return MahjongTehai.Rule.rules.length;
    };
    
    // ���̃Q�b�^�[ �Bpublic
    MahjongTehai.Rule.getRule = function(index) {
        if (index < 0 || index >= MahjongTehai.Rule.rules.length) {
            var voidFunc = function(tehai) {
                return [0, ''];
            };
            return voidFunc;
        }
        return MahjongTehai.Rule.rules[index];
    };
    
    // �Ǝ�����ǉ�����ۂɎg���֐��Bpublic
    MahjongTehai.Rule.addRule = function(rule) {
        MahjongTehai.Rule.rules.push(rule);
    };
    
    // ���_�v�Z������T�u�֐��B
    MahjongTehai.calcPointFromHuAndFan = function(hu, fan, tsumoFlag, oyaFlag) {
        var huFanStr = hu + '��' + fan[0] + '��';
        if (fan[0] === 0) {
            return [0, 0, '�𖳂�', ''];
        }
        var basePoint = hu * 2 * 2;
        for (var i = 0; i < fan[0]; i++) {
            basePoint *= 2;
        }
        if (basePoint >= 2000) {
            if (fan[0] >= 13) {
                var yakumanDoubled = parseInt(fan[0] / 13);
                basePoint = 8000 * yakumanDoubled;
                if (yakumanDoubled == 1) {
                    huFanStr = '��';
                } else if (yakumanDoubled == 2) {
                    huFanStr = '�_�u����';
                } else if (yakumanDoubled == 3) {
                    huFanStr = '�g���v����';
                } else {
                    huFanStr = yakumanDoubled + '�{��';
                }
            } else if (fan[0] >= 11) {
                basePoint = 6000;
                huFanStr += '�O�{��';
            } else if (fan[0] >= 8) {
                basePoint = 4000;
                huFanStr += '�{��';
            } else if (fan[0] >= 6) {
                basePoint = 3000;
                huFanStr += '����';
            } else {
                basePoint = 2000;
                huFanStr += '����';
            }
        }
        if (tsumoFlag) {
            var oyaPoint = basePoint * 2;
            if (oyaPoint % 100 > 0) {
                oyaPoint = oyaPoint + 100 - (oyaPoint % 100);
            }
            var koPoint = basePoint;
            if (koPoint % 100 > 0) {
                koPoint = koPoint + 100 - (koPoint % 100);
            }
            if (oyaFlag) {
                return [oyaPoint, oyaPoint, fan[1], huFanStr];
            }
            return [koPoint, oyaPoint, fan[1], huFanStr];
        } else {
            var ronPoint = basePoint;
            if (oyaFlag) {
                ronPoint *= 6;
            } else {
                ronPoint *= 4;
            }
            if (ronPoint % 100 > 0) {
                ronPoint = ronPoint + 100 - (ronPoint % 100);
            }
            return [0, ronPoint, fan[1], huFanStr];
        }
    };
    
    return MahjongTehai;
});