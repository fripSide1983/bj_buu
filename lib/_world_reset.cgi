#================================================
# ���E��⍑�ް���ؾ�ĂŎg���郂�W���[��
# �Ղ��Ɋւ�����̂��������S�̓I�ɂ����ƃV���v���ɂł������Ȃ̂� _world_reset �Ƃ��Ă���
# world reset vs_npc ���g�� add_npc_data �͂���ɊO���ɒu���������ǂ�����
#================================================

#================================================
# ��ȌĂяo����
# ./lib/world.cgi
# ./lib/reset.cgi
#================================================

#================================================
# ��S��
#================================================

# ���N�̏���X�g��n���ƒ���11�N�̏�Əd��������̂����O��������X�g���Ԃ��Ă���
sub unique_worlds {
	my @new_worlds = @_;
	open my $fh, "< $logdir/world_log.cgi" or &error("$logdir/world_log.cgi���J���܂���");
	my @old_worlds = split /<>/, <$fh>;
	close $fh;
	my @next_worlds;
	for my $new_v (@new_worlds){
		my $old_year = 0;
		my $old_flag = 0;
		for my $o (@old_worlds){
			last if $old_year > 10;
			if ($new_v == $o){
				$old_flag = 1;
				last;
			}
			$old_year++;
		}
		push @next_worlds, $new_v unless $old_flag;
	}
	return @next_worlds;
}

#================================================
# ���� �Í����܂ލՂ��̈�
#================================================

# �n���ꂽ��i���o�[��n���Ɠ��������f���ĕԂ�
sub is_special_world {
	my $world_no = shift;
	return $world_no < $#world_states-5 ? 0 : 1;
}

# �Ղ��̊J�n�ƏI���ɕR�Â��̂� 1 ���󂯂�
use constant FESTIVAL_TYPE => {
	'kouhaku' => 1,
	'sangokusi' => 3,
	'konran' => 5,
	'sessoku' => 7,
	'dokuritu' => 9
};

# �Ղ��̖��̂ƁA�J�n���Ȃ� 1 �I���� �Ȃ� 0 ���w�肷��
sub festival_type {
	my ($festival_name, $is_start) = @_;
	return FESTIVAL_TYPE->{$festival_name} + $is_start;
}

sub add_npc_data {
	my $country = shift;
	
	my %npc_statuss = (
		max_hp => [999, 600, 400, 300, 99],
		max_mp => [999, 500, 200, 100, 99],
		at     => [999, 400, 300, 200, 99],
		df     => [999, 300, 200, 100, 99],
		mat    => [999, 400, 300, 200, 99],
		mdf    => [999, 300, 200, 100, 99],
		ag     => [999, 500, 300, 200, 99],
		cha    => [999, 400, 300, 200, 99],
		lea    => [666, 400, 250, 150, 99],
		rank   => [$#ranks, $#ranks-2, 10, 7, 4],
	);
	my @npc_weas = (
	#	[0]����[1]����No	[2]�K�E�Z
		['��', [0],			[61..65],],
		['��', [1 .. 5],	[1 .. 5],],
		['��', [6 ..10],	[11..15],],
		['��', [11..15],	[21..25],],
		['��', [16..20],	[31..35],],
		['��', [21..25],	[41..45],],
		['��', [26..30],	[51..55],],
	);
	my $line = qq|\@npcs = (\n|;
	my @npc_names = (qw/vipqiv(NPC) kirito(NPC) �T�̉ƒ��w(NPC) pigure(NPC) �E�F��(NPC) vipqiv(NPC) DT(NPC) �n��(NPC) �A�V�����C(NPC) �S�~�N�Y(NPC)/);

	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$npc_names[$i]',\n|;
		
		for my $k (qw/max_hp max_mp at df mat mdf ag cha lea rank/) {
			$line .= qq|\t\t$k\t\t=> $npc_statuss{$k}[$i],\n|;
		}
		
		my $kind = int(rand(@npc_weas));
		my @weas = @{ $npc_weas[$kind][1] };
		my $wea  = $npc_weas[$kind][1]->[int(rand(@weas))];
		$line .= qq|\t\twea\t\t=> $wea,\n|;

		my $skills = join ',', @{ $npc_weas[$kind][2] };
		$line .= qq|\t\tskills\t\t=> '$skills',\n\t},\n|;
	}
	$line .= qq|);\n\n1;\n|;
	
	open my $fh, "> $datadir/npc_war_$country.cgi";
	print $fh $line;
	close $fh;
}

1;