require "$datadir/skill.cgi";
$is_battle = 1; # ﾊﾞﾄﾙﾌﾗｸﾞ1
#================================================
# 戦闘 Created by Merino
#================================================

#ﾈｺﾐﾐ問題
#　ﾈｺﾐﾐ相手に技を避けられるとこっちの一部の技はMP消費なしで効果が発揮される
#　逆にｾﾙﾊﾞなど相手に当たることを前提としない技は効果も発揮しない
#　そもそもﾈｺﾐﾐ避けすぎな気もする
#　諸々の問題を含め、攻撃ﾌﾗｸﾞを共用してるのがやりにくい

# 武器による優劣
my %tokkous = (
# '強い属性' => qr/弱い属性/,
	'剣' => qr/斧/,
	'斧' => qr/槍/,
	'槍' => qr/剣/,
	'炎' => qr/風|無/,
	'風' => qr/雷|無/,
	'雷' => qr/炎|無/,
	'無' => qr/剣|斧|槍/,
);

#================================================
# 使う値を Set
#================================================
my @m_skills = split /,/, $m{skills};
my @y_skills = split /,/, $y{skills};

# 画面表示やｽｷﾙで使うのでｸﾞﾛｰﾊﾞﾙ変数
$m_at = $m{at};
$y_at = $y{at};
$m_df = $m{df};
$m_mdf= $m{mdf};
$y_df = $y{df};
$y_mdf= $y{mdf};
$m_ag = $m{ag};
$y_ag = $y{ag};

if    ($guas[$m{gua}][2] =~ /無|剣|斧|槍/) { $m_df += $guas[$m{gua}][3]; }
elsif ($guas[$m{gua}][2] =~ /炎|風|雷/)    { $m_mdf+= $guas[$m{gua}][3]; }
if    ($guas[$y{gua}][2] =~ /無|剣|斧|槍/) { $y_df += $guas[$m{gua}][3]; }
elsif ($guas[$y{gua}][2] =~ /炎|風|雷/)    { $y_mdf+= $guas[$m{gua}][3]; }
# 使用するのは AT or MAT, DF or MDF のどちらか
if    ($weas[$m{wea}][2] =~ /無|剣|斧|槍/) { $m_at = $m{at}  + $weas[$m{wea}][3]; }
elsif ($weas[$m{wea}][2] =~ /炎|風|雷/)    { $m_at = $m{mat} + $weas[$m{wea}][3]; $y_df = $y_mdf; }
if    ($weas[$y{wea}][2] =~ /無|剣|斧|槍/) { $y_at = $y{at}  + $weas[$y{wea}][3]; }
elsif ($weas[$y{wea}][2] =~ /炎|風|雷/)    { $y_at = $y{mat} + $weas[$y{wea}][3]; $m_df = $m_mdf; }

$m_ag -= $guas[$m{gua}][5];
$y_ag -= $guas[$y{gua}][5];
if($guas[$m{gua}][0] ne '7'){
	$m_ag -= $weas[$m{wea}][5];
}
$m_ag = int(rand(5)) if $m_ag < 1;
$y_ag -= $weas[$y{wea}][5];
$y_ag = int(rand(5)) if $y_ag < 1;

$m_at = int($m_at * 0.5) if $m{wea} && $m{wea_c} <= 0;

if ($m{wea} && $y{wea}) {
	if (&is_tokkou($m{wea},$y{wea})){
		$m_at = int(1.5 *$m_at);
		$y_at = int(0.75*$y_at);
		$is_m_tokkou = 1;
	}
	elsif (&is_tokkou($y{wea},$m{wea})) {
		$y_at = int(1.5 *$y_at);
		$m_at = int(0.75*$m_at);
		$is_y_tokkou = 1;
	}
}
# 武器と防具の相性設定(攻撃力)
# 素手vs防具あり 0.3倍 素手vs防具なし 1.0倍
# 武器vs防具なし 1.0倍 武器vs防具属性違い 1.0倍 武器vs防具属性同じ 0.5倍
# 素手で防具持ち殴ったら下方修正同様、武器で防具なし殴ったら上方修正とかはしないの？ 素手不利で相対的に武器持ち有利とも言えるけど
if ($y{gua}) {
	if ($m{wea}) {
		if (&is_gua_valid($y{gua},$m{wea})){
			$m_at = int(0.5 *$m_at);
			$is_y_tokkou2 = 1;
		}
	} else {
		$m_at = int(0.3 *$m_at);
		$is_y_tokkou2 = 1;
	}
}
#else {
#	$m_at = int($m_at * 1.2) if $m{wea};
#}
if ($m{gua}) {
	if ($y{wea}) {
		if (&is_gua_valid($m{gua},$y{wea})){
			$y_at = int(0.5 *$y_at);
			$is_m_tokkou2 = 1;
		}
	} else {
		$y_at = int(0.3 *$y_at);
		$is_m_tokkou2 = 1;
	}
}
#else {
#	$y_at = int($y_at * 1.2) if $y{wea};
#}


#================================================
# ﾒｲﾝ動作
#================================================
&run_battle2;
#&run_battle;

&battle_menu if $m{hp} > 0 && $y{hp} > 0;


#================================================
# 実行処理
#================================================
sub run_battle2 {
	if ($cmd eq '') {
		$mes .= '戦闘ｺﾏﾝﾄﾞを選択してください<br>';
	}
	elsif ($m{turn} >= 20) { # なかなか決着つかない場合
		$mes .= '戦闘限界ﾀｰﾝを超えてしまった…これ以上は戦えません<br>';
		&lose;
	}
	else {
		# 無改造の状態と違って後攻でも先攻に先んじて効果を発揮する処理が実装された
		# したがって、先攻後攻というどちらを優先して処理するか以前に両方できるだけの処理を行う

		local $m_s = undef;
		local $pikorin;
		if (!$metal) { # ﾒﾀﾙ相手には常に攻撃で必殺技も閃かない
			$m_s = $skills[ $m_skills[ $cmd - 1 ] ] if $cmd > 0 && $guas[$m{gua}][0] ne '21'; # 1ｺﾏﾝﾄﾞ以上を入力していて狂戦士の鎧じゃなくﾒﾀﾙ相手じゃないなら必殺技
			$m_s = undef if defined($m_s) && ($weas[$m{wea}][2] ne $m_s->[2] || !&m_mp_check($m_s)); # 必殺技を選択していても属性が違ったりMPが足りないなら攻撃
	
			# 技閃いてもフラグが立たない問題対策 フラグ自体は先攻後攻関係ないので予め閃き処理を済ませばフラグ立てられる
			$pikorin = &_learning if !defined($m_s); # 攻撃で技を閃いたならば 1 が返り、閃いた技は $m_s に入る
		}

		local $y_s = $skills[ $y_skills[ int(rand(6)) - 1 ] ] if $guas[$y{gua}][0] ne '21'; # 狂戦士の鎧じゃないなら必殺技
		$y_s = undef if defined($y_s) && ($weas[$y{wea}][2] ne $y_s->[2] || !&y_mp_check($y_s)); # 必殺技を選択していても属性が違ったりMPが足りないなら攻撃

=pod
		# 攻撃フラグや防具フラグも予めここで済ませてしまいたいがイジる部分が増えるのでとりあえず現状維持
		# フラグ類をまず全部洗い出してから処理すれば変な挙動しなくなる
		# 例
		#   無効技をﾈｺﾐﾐで避けられるとMP消費せずに無効技を発揮できる
		#   ｽﾀﾝ技をﾔﾀﾉｶｶﾞﾐで返されても相手にｽﾀﾝ効果を与える
		# 戦闘は $who で自分と相手を切り替えてるのでそれ同様 $who で戦闘フラグも切り替える
		local $who = 'm';
		&m_flag2; # ${"$who"."_is_guard"} → $m_is_guard などフラグ入る
		local $who = 'y';
		$y_flag2; # ${"$who"."_is_guard"} → $y_is_guard などフラグ入る
=cut

		# 勝敗判定については未着手
		# 基本的にプレイヤー不利になっているが、先攻後攻で分けるのも良いのでは？
		if ( rand($m_ag * 3) >= rand($y_ag * 3) ) { # プレイヤー先攻
			my $v = &m_attack2;
			if ($y{hp} <= 0 && $m{hp} > 0) { # ﾘｽｸﾀﾞﾒｰｼﾞで自分がHP0になっても敵の攻撃に移る↓
				&win; # ﾌﾟﾚｲﾔｰ先攻だからまずは勝利判定だと思われる
			}
			else {
				&y_attack2;
				if    ($m{hp} <= 0) { &lose; } # さらにﾘｽｸﾀﾞﾒｰｼﾞで相手がHP0になってもすでに自分はHP0なので負ける
				elsif ($y{hp} <= 0) { &win;  }
				elsif ($m{pet}) {
					unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
						&use_pet('battle', $v);
					}
					if    ($m{hp} <= 0) { &lose; } # ﾌﾟﾚｲﾔｰ先攻だから勝利判定先にしたら？
					elsif ($y{hp} <= 0) { &win; }
				}
			}
		}
		else { # NPC先攻
			&y_attack2;
			if ($m{hp} <= 0) { # ﾘｽｸﾀﾞﾒｰｼﾞで敵がHP0になってもこっちの攻撃に移る↓
				&lose; # NPC先攻だからまずは敗北判定だと思われる
			}
			else {
				my $v = &m_attack2;
				if    ($m{hp} <= 0) { &lose;  } # さらにﾘｽｸﾀﾞﾒｰｼﾞでこっちがHP0になると負ける
				elsif ($y{hp} <= 0) { &win; }
				elsif ($m{pet}) {
					unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
						&use_pet('battle', $v);
					}
					if    ($m{hp} <= 0) { &lose; }
					elsif ($y{hp} <= 0) { &win; }
				}
			}
		}
		$m{turn}++;
	}
	$m{mp} = 0 if $m{mp} < 0;
	$y{mp} = 0 if $y{mp} < 0;
}

#=================================================
# 自分の攻撃
#=================================================
sub m_attack2 {
	&y_flag2;

	if ($pikorin) { # 従来ﾈｺﾐﾐ相手に攻撃して避けられると技を閃かなかった 閃くが当たらないに修正
		$m_mes = "閃いた!! $m_s->[1]!";
		$mes .= qq|<font color="#CCFF00">☆閃き!!$m{name}の$m_s->[1]!!</font><br>|;
	}
	if ($gua_avoid) { # 相手のﾈｺﾐﾐ判定
		$mes .= "$y{name}はひらりと身をかわした<br>";
		return;
	}

	local $who = 'm';
	my $hit_damage = $y{hp}; # 与えたダメージを持つ

	if (defined($m_s)) { # 必殺技
		if ($pikorin) { # 従来通り閃いた技はMP消費もなければ無効技などのフラグ無視
			&{ $m_s->[4] }($m_at);
		}
		else {
			$m{mp} -= $guas[$m{gua}][0] eq '6' ? int($m_s->[3] / 2) : $m_s->[3];
			$m_mes = $m_s->[5] ? "$m_s->[5]" : "$m_s->[1]!" unless $m_mes;
			$mes .= "$m{name}の$m_s->[1]!!<br>";
			if($is_guard){
				my $pre_yhp = $y{hp};
				&{ $m_s->[4] }($m_at);
				$y{hp} = $pre_yhp;
			} elsif ($gua_skill_mirror) {
				my $pre_yhp = $y{hp};
				&{ $m_s->[4] }($m_at);
				$m{hp} -= $pre_yhp - $y{hp};
				$mes .= "しかし$guas[$y{gua}][1]が技を反射し ".($pre_yhp - $y{hp})." のﾀﾞﾒｰｼﾞをうけました!!<br>";
				$y{hp} = $pre_yhp;
			} else {
				&{ $m_s->[4] }($m_at);
			}
		}
	}
	else { # 攻撃
		my $sc = 1;
		if ($guas[$m{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$m{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}
		for my $scc (1..$sc) {
			$mes .= "$m{name}の攻撃!!";
			my $kaishin_flag = $m{hp} < $m{max_hp} * 0.25 && int(rand($m{hp})) == 0; # 999->249.75 && 0〜248 1/249
			if($guas[$m{gua}][0] eq '8'){
				$kaishin_flag = int(rand($m{hp} / 10)) == 0; # 999->99.9 0〜98 1/99 なんとなく1/3ぐらいで会心でもええんでないか
			}
			my $gua_mes;
			my $m_at_bf = $m_at;
			if ($guas[$m{gua}][0] eq '10' && rand(10) < 3) {
				$gua_mes = "<br>$guas[$m{gua}][1]が駆動する!";
				$m_at = int($m_at * 1.2);
			} elsif ($guas[$m{gua}][0] eq '21') {
				$gua_mes .= "<br>$guas[$m{gua}][1]が暴\走する!";
				$m_at = int($m_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($m_at) : &_attack_normal($m_at, $y_df);
			$m_at = $m_at_bf;
			$mes .= "$gua_mes<br>";

			if ($is_counter) {
				$mes .= "攻撃を返され $v のﾀﾞﾒｰｼﾞをうけました<br>";
				$m{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "ｽﾀﾝで動けない!<br>";
			}
			else {
				$mes .= "$v のﾀﾞﾒｰｼﾞをあたえました<br>";
				if ($m{wea_c} > 0 && $scc eq '1') {
					--$m{wea_c};
					my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
					$mes .= "$wnameは壊れてしまった<br>" if $m{wea_c} == 0;
				}
				$y{hp} -= $v;
			}
		}
	}
	$hit_damage -= $y{hp};

	# 送電服は受けたダメージで回復すると思ってたけど与えたダメージで回復する 分けて書いてあることから仕様と思われる
	# ｸﾜﾊﾞﾗは消費MP半減だから無効技連打でも恩恵受けられるが、送電服は与えたダメージに依存するのでｸﾜﾊﾞﾗほど恩恵受けないと思われる
	# 高魅力がｿｰﾗﾝ撃って運が良ければｸﾜﾊﾞﾗよりも効率は良いが…20から18,15とかにするのは？
	if ($guas[$m{gua}][0] eq '13' && $hit_damage) {
		my $v = int($hit_damage / 20);
		$mes .= "あたえたﾀﾞﾒｰｼﾞから MP を $v 吸収しました<br>";
		$m{mp} += $v;
		$m{mp} = $m{max_mp} if $m{mp} > $m{max_mp};
	}

	if($gua_relief && $hit_damage){
		my $v = int($hit_damage / 10);
		$mes .= "$v のﾀﾞﾒｰｼﾞを防ぎました<br>";
		$y{hp} += $v;
	} elsif ($gua_remain && $hit_damage && $y{hp} <= 0) {
		$mes .= "$guas[$y{gua}][1]に攻撃が当たり奇跡的に致命傷をまのがれた<br>";
		$y{hp} = 1;
	} elsif ($gua_half_damage && $hit_damage) {
		$mes .= "$guas[$y{gua}][1]がﾀﾞﾒｰｼﾞを半減させました<br>";
		$y{hp} += int($hit_damage / 2);
	}

}

#=================================================
# 相手の攻撃
#=================================================
sub y_attack2 {
	&m_flag2;
	if ($metal) {
		$mes .= "$y{name}は様子を見ている";
		return;
	}
	if ($gua_avoid) { # 相手のﾈｺﾐﾐ判定
		$mes .= "$m{name}はひらりと身をかわした<br>";
		return;
	}

	local $who = 'y';
	my $hit_damage = $m{hp}; # 与えたダメージを持つ

	if (defined($y_s)) { # 必殺技
		$y{mp} -= $y_s->[3]; # NPC側でｸﾜﾊﾞﾗのお守りが機能してない 強すぎるから？
		$y_mes = $y_s->[5] ? "$y_s->[5]" : "$y_s->[1]!" unless $y_mes;
		$mes .= "$y{name}の$y_s->[1]!!<br>";

		if ($is_guard) {
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$m{hp} = $pre_mhp;
		} elsif ($gua_skill_mirror) {
#			$mes .= "$guas[$m{gua}][1]が技を反射する!!<br>";
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$y{hp} -= $pre_mhp - $m{hp};
			$mes .= "しかし$guas[$m{gua}][1]が技を反射し ".($pre_mhp - $m{hp})." のﾀﾞﾒｰｼﾞをうけました!!<br>";
			$m{hp} = $pre_mhp;
		} else {
			&{ $y_s->[4] }($y_at);
		}
	} else { # 攻撃
		my $sc = 1;
		if ($guas[$y{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$y{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}

		for my $scc (1..$sc) {
			$mes .= "$y{name}の攻撃!!";
			my $kaishin_flag = $y{hp} < $y{max_hp} * 0.25 && int(rand($y{hp})) == 0;
			if($guas[$y{gua}][0] eq '8'){
				$kaishin_flag = int(rand($y{hp} / 10)) == 0;
			}
			my $gua_mes;
			my $y_at_bf = $y_at;
			if ($guas[$y{gua}][0] eq '10' && rand(10) < 3) {
				$gua_mes .= "<br>$guas[$y{gua}][1]が駆動する!";
				$y_at = int($y_at * 1.2);
			} elsif ($guas[$y{gua}][0] eq '21') {
				$gua_mes .= "<br>$guas[$y{gua}][1]が暴\走する!";
				$y_at = int($y_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($y_at) : &_attack_normal($y_at, $m_df);
			$y_at = $y_at_bf;
			$mes .= "$gua_mes<br>";

			if ($is_counter) {
				$mes .= "攻撃を返し $v のﾀﾞﾒｰｼﾞをあたえました<br>";
				$y{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "ｽﾀﾝで動けない!<br>";
			}
			else {
				$mes .= "$v のﾀﾞﾒｰｼﾞをうけました<br>";
				$m{hp} -= $v;
			}
		}
	}
	$hit_damage -= $m{hp};

	if ($guas[$y{gua}][0] eq '13' && $hit_damage) {
		my $v = int($hit_damage / 20);
		$mes .= "あたえたﾀﾞﾒｰｼﾞから MP を $v 吸収しました<br>";
		$y{mp} += $v;
		$y{mp} = $y{max_mp} if $y{mp} > $y{max_mp};
	}

	if($gua_relief && $hit_damage){
		my $v = int($hit_damage / 10);
		$mes .= "$v のﾀﾞﾒｰｼﾞを防ぎました<br>";
		$m{hp} += $v;
	} elsif ($gua_remain && $hit_damage && $m{hp} <= 0) {
		$mes .= "$guas[$m{gua}][1]に攻撃が当たり奇跡的に致命傷をまのがれた<br>";
		$m{hp} = 1;
	} elsif ($gua_half_damage && $hit_damage) {
		$mes .= "$guas[$m{gua}][1]がﾀﾞﾒｰｼﾞを半減させました<br>";
		$m{hp} += int($hit_damage / 2);
	}
}

#=================================================
# 自分の攻撃ﾌﾗｸﾞ
#=================================================
sub m_flag2 {
	&init_battle_flags;
	return if ($guas[$m{gua}][0] eq '21') && !$pikorin; # 狂戦士の鎧は攻撃強制 閃いてるなら狂戦士の鎧でも必殺技

	&{ $m_s->[6] } if defined($m_s); # 必殺技

	# 防具の特殊フラグ
	if ($m{gua}) {
		my $m_g = $guas[ $m{gua} ];
		&{ $m_g->[6] };
	}
}

#=================================================
# 相手の攻撃ﾌﾗｸﾞ
#=================================================
sub y_flag2 {
	&init_battle_flags;
	return if $guas[$y{gua}][0] eq '21'; # 狂戦士の鎧は攻撃強制
	return if $metal;

	&{ $y_s->[6] } if defined($y_s); # 必殺技

	# 防具の特殊フラグ
	if ($y{gua}) {
		my $y_g = $guas[ $y{gua} ];
		&{ $y_g->[6] };
	}
}


#=================================================
# 攻撃ﾌﾗｸﾞの初期化
#=================================================
sub init_battle_flags {
	$is_guard = 0; # HPダメージ"必殺技"の無効フラグ
	$is_guard_s = 0; # なんのフラグか分からん
	$gua_relief = 0; # HPダメージの軽減フラグ
	$gua_remain = 0; # HP0の回避フラグ
	$gua_half_damage = 0; # HPダメージの半減フラグ
	$gua_skill_mirror = 0; # "必殺技"の反射フラグ
	$gua_avoid = 0; # 行動の無効フラグ
}

sub run_battle {
=pod
	if ($m{name} eq 'nanamie' || $m{name} eq '') {
		$m{mp} = 999;
		$m{ag} = 548;
		$y{mp} = 999;
		$m{act} = 0;
		$mes .= "m{wea} : $m{wea}, y{wea} : $y{wea}<br>";
		$mes .= "m{gua} : $m{gua}, y{gua} : $y{gua}<br>";
		$mes .= "skill_0 : $y_skills[0], skill_1 : $y_skills[1], skill_2 : $y_skills[2], skill_3 : $y_skills[3], skill_4 : $y_skills[4], skill_-1 : $y_skills[-1]<br><br>";
	}
=cut
	if ($cmd eq '') {
		$mes .= '戦闘ｺﾏﾝﾄﾞを選択してください<br>';
	}
	elsif ($m{turn} >= 20) { # なかなか決着つかない場合
		$mes .= '戦闘限界ﾀｰﾝを超えてしまった…これ以上は戦えません<br>';
		&lose;
	}
	elsif ( rand($m_ag * 3) >= rand($y_ag * 3) ) {
		my $y_rand = int(rand(6))-1;
		# 技は5つだけど、5番目の技が選ばれる確率が高い(1/6, 1/6, 1/6, 1/6, 1/3)
		# プレイヤーの攻撃コマンド分のズレ修正をコピペした結果確率の偏りが生じる不具合かと思ったが、
		# 技を5つすべて埋めてない場合には攻撃になる確率を上げるようにする意図があるのかも
		# なので、技が全部埋まってるならば1/5ずつ、技が埋まってないなら従来通り攻撃を高め
		# こんぐらいは裏技的なこととしてスルーでも良いかも？
#		my $y_rand = @y_skills >= 5 ? int(rand(5)) : int(rand(6))-1 ; # (-1, 0, 1, 2, 3, 4) -1番目の要素はケツなので 4 と同じ
		$is_guard = 0;
		$is_guard_s = 0;
		$gua_relief = 0;
		$gua_remain = 0;
		$gua_half_damage = 0;
		$gua_skill_mirror = 0;
		$gua_avoid = 0;
		&y_flag($y_rand);
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$mes .= "y_rand : $y_rand<br>";
			$mes .= "y_flag<br>";
			$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
			$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
		}
=cut
		my $v = &m_attack;
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$mes .= "m_attack<br>";
			$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
			$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
		}
=cut
		if ($y{hp} <= 0 && $m{hp} > 0) {
			&win;
		}
		else {
			$is_guard = 0;
			$gua_relief = 0;
			$gua_remain = 0;
			$gua_half_damage = 0;
			$gua_skill_mirror = 0;
			$gua_avoid = 0;
			&m_flag;
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "m_flag<br>";
				$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
				$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br>";
			}
=cut
			&y_attack($y_rand);
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "y_attack<br>";
				$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
				$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br><br>";
				$m{hp} = 1 if $m{hp} < 1;
			}
=cut
			if    ($m{hp} <= 0) { &lose; }
			elsif ($y{hp} <= 0) { &win;  }
			elsif ($m{pet}) {
				unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
					&use_pet('battle', $v);
				}
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	else {
		my $y_rand = int(rand(6))-1;
		$is_guard = 0;
		$is_guard_s = 0;
		$gua_relief = 0;
		$gua_remain = 0;
		$gua_half_damage = 0;
		$gua_skill_mirror = 0;
		$gua_avoid = 0;
		&m_flag;
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$mes .= "y_rand : $y_rand<br>";
			$mes .= "m_flag<br>";
			$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
			$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br>";
		}
=cut
		&y_attack($y_rand);
=pod
		if ($m{name} eq 'nanamie' || $m{name} eq '') {
			$m{hp} = 1 if $m{hp} < 1;
			$mes .= "y_attack<br>";
			$mes .= "m_is_guard : $is_guard, m_is_guard_s : $is_guard_s, m_gua_relief : $gua_relief, m_gua_remain : $gua_remain<br>";
			$mes .= "m_gua_half_damage : $gua_half_damage, m_gua_skill_mirror : $gua_skill_mirror, m_gua_avoid : $gua_avoid<br><br>";
		}
=cut
		if ($m{hp} <= 0) {
			&lose;
		}
		else {
			$is_guard = 0;
			$gua_relief = 0;
			$gua_remain = 0;
			$gua_half_damage = 0;
			$gua_skill_mirror = 0;
			$gua_avoid = 0;
			&y_flag($y_rand);
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "y_flag<br>";
				$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
				$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
			}
=cut
			my $v = &m_attack;
=pod
			if ($m{name} eq 'nanamie' || $m{name} eq '') {
				$mes .= "m_attack<br>";
				$mes .= "y_is_guard : $is_guard, y_is_guard_s : $is_guard_s, y_gua_relief : $gua_relief, y_gua_remain : $gua_remain<br>";
				$mes .= "y_gua_half_damage : $gua_half_damage, y_gua_skill_mirror : $gua_skill_mirror, y_gua_avoid : $gua_avoid<br><br>";
			}
=cut
			if    ($m{hp} <= 0) { &lose;  }
			elsif ($y{hp} <= 0) { &win; }
			elsif ($m{pet}) {
				unless($boss && ($m{pet} eq '122' || $m{pet} eq '123' || $m{pet} eq '124')){
					&use_pet('battle', $v);
				}
				if    ($m{hp} <= 0) { &lose; }
				elsif ($y{hp} <= 0) { &win; }
			}
		}
		$m{turn}++;
	}
	
	$m{mp} = 0 if $m{mp} <= 0;
	$y{mp} = 0 if $y{mp} <= 0;
}


#=================================================
# 自分の攻撃
#=================================================
sub m_attack {
	if ($gua_avoid) {
		$mes .= "$y{name}はひらりと身をかわした<br>";
		return;
	}
	
	my $m_s = $skills[ $m_skills[$cmd-1] ];
	
	if ($guas[$m{gua}][0] eq '21') {
		$m_s = undef;
	}
	
	my $guard_pre_hp = $y{hp};
	
	# 必殺技 正常なｺﾏﾝﾄﾞか # 属性が装備しているものと同じか # MPがあるか # メタル相手じゃないか
	if ($cmd > 0 && defined($m_s) && $weas[$m{wea}][2] eq $m_s->[2] && &m_mp_check($m_s) && !$metal) {
		if($guas[$m{gua}][0] eq '6'){
			$m{mp} -= int($m_s->[3] / 2);
		}else{
			$m{mp} -= $m_s->[3];
		}
		$m_mes = $m_s->[5] ? "$m_s->[5]" : "$m_s->[1]!" unless $m_mes;
		$mes .= "$m{name}の$m_s->[1]!!<br>";
		local $who = 'm';
		if($is_guard){
			my $pre_yhp = $y{hp};
			&{ $m_s->[4] }($m_at);
			$y{hp} = $pre_yhp;
		} elsif ($gua_skill_mirror) {
			$mes .= "$guas[$y{gua}][1]が技を反射する!!<br>";
			my $pre_yhp = $y{hp};
			&{ $m_s->[4] }($m_at);
			$m{hp} -= $pre_yhp - $y{hp};
			$y{hp} = $pre_yhp;
		} else {
			&{ $m_s->[4] }($m_at);
		}
	}
	# ﾋﾟｺﾘﾝ! 習得技5未満 かつ 武器ﾚﾍﾞﾙ かつ 相手の強さ普通以上↑ 
	elsif (@m_skills < 5 && $m{wea_lv} >= int(rand(300)) && &st_lv > 0 && !$metal) {
		local $who = 'm';
		&_pikorin;
	}
	else { # 攻撃
		my $sc = 1;
		if ($guas[$m{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$m{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}
		for my $scc (1..$sc) {
			$mes .= "$m{name}の攻撃!!";
			my $kaishin_flag = $m{hp} < $m{max_hp} * 0.25 && int(rand($m{hp})) == 0;
			if($guas[$m{gua}][0] eq '8'){
				$kaishin_flag = int(rand($m{hp} / 10)) == 0;
			}
			my $m_at_bf = $m_at;
			if ($guas[$m{gua}][0] eq '10' && rand(10) < 3) {
				$mes .= "<br>$guas[$m{gua}][1]が駆動する!";
				$m_at = int($m_at * 1.2);
			} elsif ($guas[$m{gua}][0] eq '21') {
				$mes .= "<br>$guas[$m{gua}][1]が暴\走する!";
				$m_at = int($m_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($m_at) : &_attack_normal($m_at, $y_df);
			$m_at = $m_at_bf;
			
			if ($is_counter) {
				$mes .= "<br>攻撃を返され $v のﾀﾞﾒｰｼﾞをうけました<br>";
				$m{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "<br>ｽﾀﾝで動けない!<br>";
			}
			else {
				$mes .= "<br>$v のﾀﾞﾒｰｼﾞをあたえました<br>";
				if ($m{wea_c} > 0 && $scc eq '1') {
					--$m{wea_c};
					my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
					$mes .= "$wnameは壊れてしまった<br>" if $m{wea_c} == 0;
				}
				$y{hp} -= $v;
			}
		}
	}
	$guard_pre_hp -= $y{hp};

	if ($guas[$m{gua}][0] eq '13' && $guard_pre_hp) {
		$mes .= "<br>ダメージをMP".int($guard_pre_hp / 20)."として吸収した<br>";
		$m{mp} += int($guard_pre_hp / 20);
		if ($m{mp} > $m{max_mp}) {
			$m{mp} = $m{max_mp};
		}
	}
	
	if($gua_relief && $guard_pre_hp){
		my $v = int($guard_pre_hp / 10);
		$mes .= "<br>$v のﾀﾞﾒｰｼﾞを防ぎました<br>";
		$y{hp} += $v;
	} elsif ($gua_remain && $guard_pre_hp && $y{hp} <= 0) {
		$mes .= "<br>ﾛｹｯﾄﾍﾟﾝﾀﾞﾝﾄに攻撃が当たり奇跡的に致命傷をまのがれた<br>";
		$y{hp} = 1;
	} elsif ($gua_half_damage && $guard_pre_hp) {
		$mes .= "<br>ダメージを半減させた<br>";
		$y{hp} += int($guard_pre_hp / 2);
	}
	
}
#=================================================
# 相手の攻撃
#=================================================
sub y_attack {
	my $y_s = $skills[ $y_skills[ $_[0] ] ];
	
	if ($guas[$y{gua}][0] eq '21') {
		$y_s = undef;
	}
	if ($metal) {
		$mes .= "$y{name}は様子を見ている";
		return;
	}
	
	if ($gua_avoid) {
		$mes .= "$m{name}はひらりと身をかわした<br>";
		return;
	}
	
	my $guard_pre_hp = $m{hp};
	# 必殺技 正常なｺﾏﾝﾄﾞか # 属性が装備しているものと同じか # MPがあるか
	if (defined($y_s) && $weas[$y{wea}][2] eq $y_s->[2] && &y_mp_check($y_s)) {
		$y{mp} -= $y_s->[3];
		$y_mes = $y_s->[5] ? "$y_s->[5]" : "$y_s->[1]!" unless $y_mes;
		$mes .= "$y{name}の$y_s->[1]!!<br>";

		local $who = 'y';
		if ($is_guard) {
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$m{hp} = $pre_mhp;
		} elsif ($gua_skill_mirror) {
			$mes .= "$guas[$m{gua}][1]が技を反射する!!<br>";
			my $pre_mhp = $m{hp};
			&{ $y_s->[4] }($y_at);
			$y{hp} -= $pre_mhp - $m{hp};
			$m{hp} = $pre_mhp;
		} else {
			&{ $y_s->[4] }($y_at);
		}
	} else {
		my $sc = 1;
		if ($guas[$y{gua}][0] eq '1' && rand(3) < 1) {
			$sc = 2;
		} elsif ($guas[$y{gua}][0] eq '15') {
			$sc = 1 + int(rand(4));
		}

		for my $scc (1..$sc) {
			$mes .= "$y{name}の攻撃!!";
			my $kaishin_flag = $y{hp} < $y{max_hp} * 0.25 && int(rand($y{hp})) == 0;
			if($guas[$y{gua}][0] eq '8'){
				$kaishin_flag = int(rand($y{hp} / 10)) == 0;
			}
			my $y_at_bf = $y_at;
			if ($guas[$y{gua}][0] eq '10' && rand(10) < 3) {
				$mes .= "<br>$guas[$y{gua}][1]が駆動する!";
				$y_at = int($y_at * 1.2);
			} elsif ($guas[$y{gua}][0] eq '21') {
				$mes .= "<br>$guas[$y{gua}][1]が暴\走する!";
				$y_at = int($y_at * 1.5);
			}
			my $v = $kaishin_flag ? &_attack_kaishin($y_at) : &_attack_normal($y_at, $m_df);
			$y_at = $y_at_bf;

			if ($is_counter) {
				$mes .= "<br>攻撃を返し $v のﾀﾞﾒｰｼﾞをあたえました<br>";
				$y{hp} -= $v;
			}
			elsif ($is_stanch) {
				$mes .= "<br>ｽﾀﾝで動けない!<br>";
			}
			else {
				$mes .= "<br>$v のﾀﾞﾒｰｼﾞをうけました<br>";
				$m{hp} -= $v;
			}
		}
	}
	$guard_pre_hp -= $m{hp};

	if ($guas[$y{gua}][0] eq '13' && $guard_pre_hp) {
		$mes .= "<br>ダメージをMPとして吸収した<br>";
		$y{mp} += int($guard_pre_hp / 20);
		if ($y{mp} > $y{max_mp}) {
			$y{mp} = $y{max_mp};
		}
	}
	
	if($gua_relief && $guard_pre_hp){
		my $v = int($guard_pre_hp / 10);
		$mes .= "<br>$v のﾀﾞﾒｰｼﾞを防ぎました<br>";
		$m{hp} += $v;
	} elsif ($gua_remain && $guard_pre_hp && $m{hp} <= 0) {
		$mes .= "<br>$guas[$m{gua}][1]に攻撃が当たり奇跡的に致命傷をまのがれた<br>";
		$m{hp} = 1;
	} elsif ($gua_half_damage && $guard_pre_hp) {
		$mes .= "<br>ダメージを半減させた<br>";
		$m{hp} += int($guard_pre_hp / 2);
	}
}

#=================================================
# 自分の攻撃ﾌﾗｸﾞ
#=================================================
sub m_flag {
	if ($guas[$m{gua}][0] eq '21') {
		return;
	}
	my $m_s = $skills[ $m_skills[$cmd-1] ];
	
	# 必殺技 正常なｺﾏﾝﾄﾞか # 属性が装備しているものと同じか # MPがあるか
	if ($cmd > 0 && defined($m_s) && $weas[$m{wea}][2] eq $m_s->[2] && &m_mp_check($m_s)) {
		&{ $m_s->[6] };
	}
	# 防具の特殊フラグ
	if ($m{gua}) {
		my $m_g = $guas[ $m{gua} ];
		&{ $m_g->[6] };
	}
}
#=================================================
# 相手の攻撃ﾌﾗｸﾞ
#=================================================
sub y_flag {
	if ($guas[$y{gua}][0] eq '21') {
		return;
	}
	my $y_s = $skills[ $y_skills[ $_[0] ] ];
	if ($metal) {
		return;
	}
	
	# 必殺技 正常なｺﾏﾝﾄﾞか # 属性が装備しているものと同じか # MPがあるか
	if (defined($y_s) && $weas[$y{wea}][2] eq $y_s->[2] && &y_mp_check($y_s)) {
		&{ $y_s->[6] };
	}
	# 防具の特殊フラグ
	if ($y{gua}) {
		my $y_g = $guas[ $y{gua} ];
		&{ $y_g->[6] };
	}
}

#=================================================
# 会心、通常攻撃
#=================================================
sub _attack_kaishin {
	my $at = shift;
	$mes .= '<b>会心の一撃!!</b>';
	return int($at * (rand(0.4)+0.8) );
}
sub _attack_normal {
	my($at, $df) = @_;
	my $v = int( ($at * 0.5 - $df * 0.3) * (rand(0.3)+ 0.9) );
	   $v = int(rand(5)+1) if $v < 5;
	return $v;
}
#=================================================
# 新技習得(すでに覚えている技でも発動) 習得で1、未習得で0
#=================================================
sub _learning {
	if (@m_skills < 5 && $m{wea_lv} >= int(rand(300)) && &st_lv > 0) {
		# 覚えられる属性のものを全て@linesに入れる
		my @lines = ();
		for my $i (1 .. $#skills) {
			push @lines, $i if $weas[$m{wea}][2] eq $skills[$i][2];
		}

		if (@lines) {
			my $no = $lines[int(rand(@lines))];
			# 覚えていない技なら追加
			my $is_learning = 1;
			for my $m_skill (@m_skills) {
				if ($m_skill eq $no) {
					$is_learning = 0;
					last;
				}
			}
			$m{skills} .= "$no," if $is_learning;
			$m_s = $skills[ $no ];
			return 1;
		}
		else { # 例外処理：覚えられるものがない
			$m_mes = '閃めきそうで閃けない…';
		}
	}
	return 0;
}

sub _pikorin {
	# 覚えられる属性のものを全て@linesに入れる
	my @lines = ();
	for my $i (1 .. $#skills) {
		push @lines, $i if $weas[$m{wea}][2] eq $skills[$i][2];
	}
	
	if (@lines) {
		my $no = $lines[int(rand(@lines))];
		$m_mes = "閃いた!! $skills[$no][1]!";
		# 覚えていない技なら追加
		my $is_learning = 1;
		for my $m_skill (@m_skills) {
			if ($m_skill eq $no) {
				$is_learning = 0;
				last;
			}
		}
		$m{skills} .= "$no," if $is_learning;
		$mes .= qq|<font color="#CCFF00">☆閃き!!$m{name}の$skills[ $no ][1]!!</font><br>|;
		$skills[ $no ][4]->($m_at);
	}
	else { # 例外処理：覚えられるものがない
		$m_mes = '閃めきそうで閃けない…';
	}
}


#=================================================
# 戦闘用メニュー
#=================================================
sub battle_menu {
	if($is_smart){
		$menu_cmd .= qq|<table boder=0 cols=5 width=90 height=90>|;

		$menu_cmd .= qq|<tr><td><form method="$method" action="$script">|;
		$menu_cmd .= qq|<input type="submit" value="攻撃" class="button1s"><input type="hidden" name="cmd" value="0">|;
		$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$menu_cmd .= qq|</form>|;
		$menu_cmd .= qq|</td>|;

		for my $i (1 .. $#m_skills+1) {
			if($i % 5 == 0){
				$menu_cmd .= qq|<tr>|;
			}
#			next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
			next unless &m_mp_check($skills[ $m_skills[$i-1] ]);
			next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
			my $mline;
			if(length($skills[ $m_skills[$i-1] ][1])>20){
				$mline = substr($skills[ $m_skills[$i-1] ][1],0,10) . "\n" . substr($skills[ $m_skills[$i-1] ][1],10,10). "\n" . substr($skills[ $m_skills[$i-1] ][1],20);
			}elsif(length($skills[ $m_skills[$i-1] ][1])>10) {
				$mline = substr($skills[ $m_skills[$i-1] ][1],0,10) . "\n" . substr($skills[ $m_skills[$i-1] ][1],10);
			}else{
				$mline = $skills[ $m_skills[$i-1] ][1];
			}
			$menu_cmd .= qq|<td><form method="$method" action="$script">|;
			$menu_cmd .= qq|<input type="submit" value="$mline" class="button1s"><input type="hidden" name="cmd" value="$i">|;
			$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$menu_cmd .= qq|</form>|;
			$menu_cmd .= qq|</td>|;
			if($i % 5 == 4){
				$menu_cmd .= qq|</tr>|;
			}
		}
		if($#m_skills % 5 != 3){
			$menu_cmd .= qq|</tr>|;
		}
		$menu_cmd .= qq|</table>|;
	}else{
		$menu_cmd  = qq|<form method="$method" action="$script"><select name="cmd" class="menu1">|;
		$menu_cmd .= qq|<option value="0">攻撃</option>|;
		for my $i (1 .. $#m_skills+1) {
#			next if $m{mp} < $skills[ $m_skills[$i-1] ][3];
			next unless &m_mp_check($skills[ $m_skills[$i-1] ]);
			next if $weas[$m{wea}][2] ne $skills[ $m_skills[$i-1] ][2];
			$menu_cmd .= qq|<option value="$i"> $skills[ $m_skills[$i-1] ][1]</option>|;
		}
		$menu_cmd .= qq|</select><br><input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$menu_cmd .= qq|<input type="submit" value="決 定" class="button1"></form>|;
	}
}


#=================================================
# 勝利
#=================================================
sub win {
	$m{hp} = 0 if $m{hp} < 0;
	$y{hp} = 0;
	$m{turn} = 0;
	$mes .= "$y{name}を倒しました<br>";

	$m_mes = $m{mes_win}  unless $m_mes;
	$y_mes = $y{mes_lose} unless $y_mes;
	
	if ($w{world} eq $#world_states-4) {
		require './lib/fate.cgi';
		&super_attack('battle');
	}

	$result = 'win';
}

#=================================================
# 敗北
#=================================================
sub lose {
	if ($m{name} eq 'nanamie' || $m{name} eq 'QE') {
#		&win;
#		return;
	}

	$m{hp} = 0;
	$y{hp} = 0 if $y{hp} < 0;
	$m{turn} = 0;
	$mes .= "$m{name}はやられてしまった…<br>";

	$m_mes = $m{mes_lose} unless $m_mes;
	$y_mes = $y{mes_win}  unless $y_mes;

	$result = 'lose';
}


#=================================================
# 武器により特攻がつくかどうか
#=================================================
sub is_tokkou {
	my($wea1, $wea2) = @_;
	return defined $tokkous{ $weas[$wea1][2] } && $weas[$wea2][2] =~ /$tokkous{ $weas[$wea1][2] }/ ? 1 : 0;
}

#=================================================
# 防具が有効かどうか
#=================================================
sub is_gua_valid {
	my($gua, $wea) = @_;
	return $guas[$gua][2] eq $weas[$wea][2];
}

#=================================================
# MPがあるかどうか
#=================================================
sub m_mp_check {
	my $m_s = shift;
	return ($m{mp} >= $m_s->[3] || ($guas[$m{gua}][0] eq '6' && $m{mp} >= int($m_s->[3] / 2)));
}
sub y_mp_check {
	my $y_s = shift;
	return ($y{mp} >= $y_s->[3] || ($guas[$y{gua}][0] eq '6' && $y{mp} >= int($y_s->[3] / 2)));
}



1; # 削除不可
