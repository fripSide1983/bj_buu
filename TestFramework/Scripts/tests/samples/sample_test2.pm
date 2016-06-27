#�T���v�����̂Q
#����������ɓ��삵�Ă��邩�`�F�b�N����
#�`�F�b�N���ڂP�F�������O�ƊJ�n����̂̌N��A���[�󋵃`�F�b�N
#�`�F�b�N���ڂQ�F�������O�ɓ�������Ă���v���C���[�̈ڐЃ`�F�b�N
#�`�F�b�N���ڂR�F�V���b�t���֎~�ݒ�̃��[�U�[�̓V���b�t������Ă��Ȃ���
#�T���v���̂��߂��̎O�̃`�F�b�N���ڂ��e�X�g�̏����Ƃ���

package sample_test2;

&run;

sub run{

	#�R���g���[���[�Ŏg���萔
	use TestFramework::Controller::ControllerConst;

	#�R���g���[���[
	require $ControllerConst::WorldController;
	require $ControllerConst::PlayerController;
	require $ControllerConst::CountryController;
	require $ControllerConst::WarController;
	require $ControllerConst::ItemController;
	$wc = WorldController->new();
	$pc = PlayerController->new();
	$cc = CountryController->new();
	$warc = WarController->new();
	$ic = ItemController->new();

	#�T���v�����̂P�̂悤�Ɏ����ŏ����ݒ���s�킸��
	#�������ꂽ�V�`���G�[�V�����ilog, user, html, data)�����[�h����
	#situation1�ł͂U�J���P�N�ڕ��a�A�J����
	#1�̍��ɂ́is1c1m, s1c2f)�A�Q�̍��ɂ�(s1c2m, s1c2f)�̂悤�ɒj���񖼂��ݐЂ��Ă���
	require $ControllerConst::SituationLoader;
	SituationLoader::load_situation("situation1");
	

	#######################�`�F�b�N���ڂP
	#�����O��̌N��Ɠ��[�󋵂��m�F���邽�߁A�P�̍��Ńv���C���[�𗧌�₳���ē��[���N������Ă�
	$pc->access_data("s1c1m", "money", 999999);
	$cc->action_stand_candidate("s1c1m");
	$cc->action_vote("s1c1f", "s1c1m");
	my $ceo1 = $cc->access_data(1, "ceo");
	($ceo ne "s1c1m") or die "failed to elect s1c1m as ceo";

	#######################�`�F�b�N���ڂQ
	#�Q�̍��̃v���C���[�𓊍����Ă݂�
	#ItemController����Ӽӂ�^����
	$mosimo = {type=>3, no=>177, c=>0, lv=>0};
	$ic->give_item("s1c2m", $mosimo);
	#���݂�depot����Ӽӂ�index
	my $mosimo_index = $ic->get_item_index("s1c2m", $mosimo);
	#�a�菊�������o���ő�������
	$ic->action_draw_item("s1c2m", $mosimo_index);
	#ϲٰс��y�b�g���g�p
	$ic->action_use_pet("s1c2m");
	#�����̏����߯ĂȂ炱��ŏI��肾��Ӽӂ͂��̂��ƂŃ��[�U�[���͂�v�������̂ł��̏���������
	#���[�U�[���͂�v�����邻�ꂼ����߯Ă̈�����TestFramework/Controller/Accessor/ItemAccessorSpecific/pet*.pm���Q��
	#���֓�������Ă݂�
	$ic->action_step_pet("s1c2m", 1);
	($pc->access_data("s1c2m", "lib") eq "prison") or die "failed to imprison s1c2m";

	#######################�`�F�b�N���ڂQ
	#�S�̍��̃v���C���[�̓V���b�t���֎~�ɐݒ肵�Ă���
	$pc->access_data("s1c4m", "shuffle", 1);
	$pc->access_data("s1c4f", "shuffle", 1);

	#�����J�n�������ĂԂ��߂ɍ����O�N�x�ɔN�x��ύX���Q�[�����x����ύX���āA3�̍��̃v���C���[�ɏ��������ē��ꂳ����
	#�O�̂��ߓ���n�������ׂ�
	$wc->access_data("year", 69);
	$wc->access_data("game_lv", 1);
	$wc->access_data("reset_time", 0);
	my $old_hero_c = $pc->access_data("s1c3m", "hero_c");
	$warc->action_set_war("s1c3m",1, 1);
	$pc->access_data("s1c3m", "wt", 0);
	$warc->action_encount("s1c3m");
	$warc->action_win_war("s1c3m");
	$warc->action_after_toitsu("s1c3m", 1);
	my $new_hero_c = $pc->access_data("s1c3m", "hero_c");
	($new_hero_c eq ($old_hero_c+ 1)) or die "tou_c didn't change : new_hero_c = $new_hero_c\n";

	######################�����J�n����̏󋵂��`�F�b�N����
	#�N��͉�C����Ă��邩
	for my $i (1 .. 6){
		($cc->access_data(1, "ceo") eq "") or die "ceo exists in country $i\n";
	}

	#���[�͉�������Ă��邩
	for my $player (@$Situation1::situation1_players){
		($pc->access_data($player->{name}, "vote") eq "") or die "$player->{name}'s vote is not void\n";
	}

	#�V���b�t���֎~�v���C���[�͌��̍��ɂ��邩
	($pc->access_data("s1c4m", "country") eq 4) or die "s1c4m moved\n";
	($pc->access_data("s1c4f", "country") eq 4) or die "s1c4f moved\n";

	#�������ꂽ�v���C���[���ڐЂ��Ă��邩
	#���̃`�F�b�N�͓�������Ă���v���C���[���������ɈڐЂ���1/6�̊m���Ŏ��s���Ă��܂�
	#�{���͕����l�̃v���C���[�𓊍����ă`�F�b�N���m����������ׂ�
	($pc->access_data("s1c2m", "country") ne 2) or die "s1c2m is still in the same country";

	#���̌㍬�����ɌN������ĂĂ��瓝�ꂷ��Ȃǂ��č�����̌N�哊�[�󋵂��`�F�b�N����
	#�T���v���Ƃ��Ă͏璷�Ȃ̂ł���Ńe�X�g�I���Ƃ���

}
1;
