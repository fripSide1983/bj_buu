package situation1;

#コントローラーで使う定数
use TestFramework::Controller::ControllerConst;

sub refresh{

	require $ControllerConst::player_controller;
	require $ControllerConst::country_controller;
	my $pc = PlayerController->new();
	my $cc = CountryController->new();

	#国をデフォルトでリセット（6ヵ国、１年目、平和）
	$cc->admin_reset_countries();

	#プレイヤーキャラクタ
	my $common_passward = "situation1";
	#名前はsituation1country1male
	my $players = [
		{ name=>"s1c1m", sex=>1,  country=>1},
		{ name=>"s1c1f", sex=>2,  country=>1},
		{ name=>"s1c2m", sex=>1,  country=>2},
		{ name=>"s1c2f", sex=>2,  country=>2},
		{ name=>"s1c3m", sex=>1,  country=>3},
		{ name=>"s1c3f", sex=>2,  country=>3},
		{ name=>"s1c4m", sex=>1,  country=>4},
		{ name=>"s1c4f", sex=>2,  country=>4},
		{ name=>"s1c5m", sex=>1,  country=>5},
		{ name=>"s1c5f", sex=>2,  country=>5},
		{ name=>"s1c6m", sex=>1,  country=>6},
		{ name=>"s1c6f", sex=>2,  country=>6}
	];


	#キャラクタ生成
	for my $player (@$players){
		$pc->create_player($player->{name}, $common_passward, $player->{sex});
	}

	#国設定
	for my $i (1 .. 6){
		$cc->access_data($i, "capacity", 2);
		$cc->access_data($i, "food", 999999);
		$cc->access_data($i, "money", 999999);
		$cc->access_data($i, "soldier", 999999);
	}

	#士官
	for my $player (@$players){
		$pc->action_shikan_player($player->{name}, $player->{country});
	}

	#セーブ
	require  $ControllerConst::situation_loader;
	SituationLoader::save_situation("situation1");
}


1;
