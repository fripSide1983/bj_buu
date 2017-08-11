#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require './lib/_use_pet_log.cgi';
#=================================================
# ���ߔp�l�ݷݸ� Created by nanamie
#=================================================

my $max_ranking = 10;

#=================================================
&decode;
&header;
&read_cs;

$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @country_pets;
require './lib/_use_pet_log.cgi' if $rank_status[$in{no}][0] eq 'use_pet';
my $type = $country_pets[$in{no}] > 0 ? "$in{no}" : ''; # ̧�ٖ��̌ꖖ���߯Ĕԍ��ƈ�v���Ȃ� 0�`n

my $this_file = "$logdir/use_pet_ranking_${type}.cgi";
my $use_pet_ranking_cycle_day = 1;

#unless (-f "$this_file") {
#	open my $fh1, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
#	close $fh1;
#	chmod $chmod, $this_file;
#}

&update_use_pet_ranking if -M $this_file > $use_pet_ranking_cycle_day;
#&update_use_pet_ranking; #�����ɍX�V�������ꍇ�͂����̃R�����g�A�E�g���O���i�������������d���Ȃ�̂ő��₩�ɖ߂����Ɓj
&run;
&footer;
exit;


#=================================================
# �ݷݸމ��
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="�s�n�o" class="button1"></form>|;
	for my $i (0 .. $#country_pets) {
		print $i eq $in{no} ? qq|$pets[$country_pets[$i]][1] / | : qq|<a href="?no=$i">$pets[$country_pets[$i]][1]</a> / |;
	}
	print qq|<a href="player_ranking.cgi?no=0">�p�l�ݷݸ�</a> / |;

	print qq|<h1>$country_pets[$in{no}][1]�p�l�ݷݸ�</h1>|;
	print qq|<div class="mes"><ul><li>�ݷݸނ�$use_pet_ranking_cycle_day�����Ƃ�ؾ�Ă���X�V����܂�</ul></div><br>|;

	print qq|<table class="table1" cellpadding="2"><tr><th>����</th><th>���l</th><th>���O</th><th>������</th></tr>| unless $is_mobile;

	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	my $pre_number = 0;
	my $d_rank;
	while ($line = <$fh>) {
		my($number,$name,$country) = split /<>/, $line;
		my $player_id =  unpack 'H*', $name;
		if($rank_status[$in{no}][0] eq 'rank'){
			my $tempn = $number;
			my $sran = 0;
			while ($tempn =~ /��/){
				$tempn =~ s/��//;
				$sran++;
			}
			if($sran){
				$d_rank = $rank if ($pre_number != $sran);
				$pre_number = $sran;
			}else {
				$d_rank = $rank if ($pre_number ne $number);
				$pre_number = $number;
			}
		}else {
			$d_rank = $rank if ($pre_number != $number);
			$pre_number = $number;
		}
		print $is_mobile     ? qq|<hr><b>$d_rank</b>��/$number/<a href="./profile.cgi?id=$player_id&country=$country">$name</a>/$cs{name}[$country]/\n|
			: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank��</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]<br></td></tr>\n|
			:  qq|<tr class="stripe1"><th>$d_rank��</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$country">$name</a></td><td>$cs{name}[$country]<br></td></tr>\n|
			;
		++$rank;
	}
	close $fh;

	print qq|</table>| unless $is_mobile;
}

#=================================================
# �p�l�ݷݸނ��X�V
#=================================================
sub update_use_pet_ranking  {
	my %sames = ();
	my @line = ();
	my @p_ranks = ();

	for my $country (0 .. $w{country}) {
		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgi̧�ق��J���܂���");
		while (my $player = <$cfh>) {
			$player =~ tr/\x0D\x0A//d;
			next if ++$sames{$player} > 1;
			my $player_id = unpack 'H*', $player;
			my $c = &read_use_pet_log($player_id, $country_pets[$in{no}]);

			# �ݷݸނ����܂��Ă��čŉ��ʂ�菬��������ݸ�݂���󂪂Ȃ�
			next if (@p_ranks > $max_ranking) && ($p_ranks[$#p_ranks][1] >= $c);

			if (0 < $c) {
				# �e��ڲ԰��}����Ă��Ȃ����ݸ�t�����A�ݸ�O�ɂȂ������ʂ͍폜
				my $is_insert = 0; # �}�����Ă��邩
				my @count = (1, 0); # ����, �ʉߐ�
				my ($prev_rank, $prev_value) = (0, 0); # 1��ʂ̏��ʂƒl
				for my $i (0 .. @p_ranks) {
					# �}����Ă���ڲ԰��傫�����ɕ��ׂ�
					# �����ɏ��ʂ��v�Z����̂ő}���͈��̂�
					if ($c >= $p_ranks[$i][0] && !$is_insert) {
						splice(@p_ranks, $i, 0, [$c, $player]);
						$is_insert = 1;
					}

					# �ݷݸނ���o����ڲ԰�����O
					# �����ʂ�����̂�1�l�ł͂Ȃ��S���폜
					$count[1] = $prev_value == $p_ranks[$i][0] ? $count[1]+1 : 0;
					my $rank = $count[0] - $count[1]; # �� - �_�u�萔 = ����
					if ($rank > $prev_rank && $prev_rank >= $max_ranking) {
						splice(@p_ranks, $i, 1) while $p_ranks[$i][1];
						last; # �S���폜�����̂Ŏ��̗v�f�͂Ȃ�
					}

					# ���̗v�f���ݸ�O���ǂ������肷��̂ɏ��ʂƒl���K�v
					($prev_rank, $prev_value) = ($rank, $p_ranks[$i][0]);
					$count[0]++;
				}
			}
		}
		close $cfh;
	}

	# ���`�{�����̃_�~�[�폜
	for my $rank (0 .. $#p_ranks - 1) {
		push(@line, "$p_ranks[$rank][0]<>$p_ranks[$rank][1]<>\n");
	}
	undef(@p_ranks);

	open my $fh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @line;
	close $fh;
}
