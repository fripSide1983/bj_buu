#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#use Time::HiRes qw(gettimeofday tv_interval);
#=================================================
# �p�l�ݷݸ� Created by oiiiuiiii
#=================================================

my @rank_status = (
#�ϐ�,�\����,�Œ�l
	['strong','�D����',500],
	['gou','���D',3000],
	['cho','����',3000],
	['sen','���]',3000],
	['nou','�_��',50000],
	['sho','����',50000],
	['hei','����',50000],
	['sal','����',10000],
);


#=================================================
&decode;
&header;
&read_cs;

$in{no} ||= 0;
$in{no} = int($in{no});
$in{no} = 0 if $in{no} > $w{country};
my $this_file = "$logdir/year_player_ranking_country_$in{no}.cgi";

my $max_ranking = $in{rank_num} ? $in{rank_num} : ($in{no} == 0 ? 3 : 10);

&update_player_ranking if $in{renew};
#&update_player_ranking; #�����ɍX�V�������ꍇ�͂����̃R�����g�A�E�g���O���i�������������d���Ȃ�̂ő��₩�ɖ߂����Ɓj
&run;
&footer;
exit;


#=================================================
# �ݷݸމ��
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="�s�n�o" class="button1"></form>|;
	for my $i (0 .. $w{country}) {
		print $i eq $in{no} ? qq|<font color="$cs{color}[$i]">$cs{name}[$i]</font> / | : qq|<a href="?no=$i">$cs{name}[$i]</a> / |;
	}
	unless(-f "$this_file"){
		open my $fh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
		print $fh "1";
		close $fh;
	}
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	my $year = <$fh>;
	close $fh;
	&update_player_ranking if ($w{year} > $year+1);

	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	my $year = <$fh>;
	for my $no (0..$#rank_status){
		my $rank = 1;
		print qq|<h1>$year�N$rank_status[$no][1]�N���ݷݸ�</h1>|;

		print qq|<table class="table1" cellpadding="2"><tr><th>����</th><th>���l</th><th>���O</th><th>������</th></tr>| unless $is_mobile;
	
		my $pre_number = 0;
		my $d_rank;
		while ($line = <$fh>) {
			my($number,$name) = split /<>/, $line;
			last if($number == 0);
			my $id_name = $name;
			if($rank_status[$no][0] eq 'strong'){
				$id_name =~ s/ .*?����ł��D��//;
			}
			my $player_id =  unpack 'H*', $id_name;
			$d_rank = $rank if ($pre_number != $number);
			$pre_number = $number;
			print $is_mobile     ? qq|<hr><b>$d_rank</b>��/$number/<a href="./profile.cgi?id=$player_id&country=$in{no}">$name</a>/$cs{name}[$in{no}]/\n|
				: $rank % 2 == 0 ? qq|<tr></td><th>$d_rank��</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$in{no}">$name</a></td><td>$cs{name}[$in{no}]<br></td></tr>\n|
				:  qq|<tr class="stripe1"><th>$d_rank��</th><td align="right">$number</td><td><a href="./profile.cgi?id=$player_id&country=$in{no}">$name</a></td><td>$cs{name}[$in{no}]<br></td></tr>\n|
				;
			++$rank;
		}
		print qq|</table>| unless $is_mobile;
	}
	close $fh;
}

#=================================================
# �p�l�ݷݸނ��X�V
#=================================================
sub update_player_ranking  {
#	my $t0 = [gettimeofday];
	my @line = ();
	my $last_year = $w{year} - 1;
	push @line, "$last_year\n";
	$country = $in{no};

	my @p_ranks = ();
	for my $no (0 .. $#rank_status) {
		push(@{$p_ranks[$no]}, [0, 0]);
	}

	my %sames = ();
	open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgi̧�ق��J���܂���");
	while (my $player = <$cfh>) {
		$player =~ tr/\x0D\x0A//d;
		next if ++$sames{$player} > 1;
		my $player_id = unpack 'H*', $player;
		unless (-f "$userdir/$player_id/year_ranking.cgi") {
			next;
		}

		open my $fh, "< $userdir/$player_id/year_ranking.cgi" or &error("year_ranking.cgi̧�ق��J���܂���");
		while (my $line = <$fh>) {
			next if index($line, "year;$last_year", 0) < 0; # �O�N�ȊO�̃f�[�^�͖��Ӗ��Ȃ̂ŉ�͂��Ȃ�

			# �O�N�̈�N�ݷݸ��ް��̎��o��
			my %ydata;
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				$ydata{$k} = $v;
			}

			for my $no (0 .. $#rank_status) {
				my $status = $rank_status[$no][0];
				next if $ydata{$status} < $rank_status[$no][2];
				# �ݷݸނ����܂��Ă��čŉ��ʂ�菬��������ݸ�݂���󂪂Ȃ�
				next if ($#{$p_ranks[$no]} >= $max_ranking) && ($p_ranks[$no][$#{$p_ranks[$no]}-1][0] > $ydata{$status});

				my $from = '';
				if ($status eq 'strong') {
					my $strong_c;
					my $strong_v = 0;
					for my $from_c (1 .. $w{country}){
						if($strong_v < $ydata{"strong_".$from_c}){
							$strong_v = $ydata{"strong_".$from_c};
							$strong_c = $from_c;
						}
					}
					$from = " $cs{name}[$strong_c]����ł��D��";
				}

				# �e��ڲ԰��}����Ă��Ȃ����ݸ�t�����A�ݸ�O�ɂȂ������ʂ͍폜
				my $is_insert = 0; # �}�����Ă��邩
				my @count = (1, 0); # ����, �ʉߐ�
				my ($prev_rank, $prev_value) = (0, 0); # 1��ʂ̏��ʂƒl
				for my $j (0 .. $#{$p_ranks[$no]}) {
					# �}����Ă���ڲ԰��傫�����ɕ��ׂ�
					# �����ɏ��ʂ��v�Z����̂ő}���͈��̂�
					if ($ydata{$status} > $p_ranks[$no][$j][0] && !$is_insert) {
						splice(@{$p_ranks[$no]}, $j, 0, [$ydata{$status}, $player.$from]);
						$is_insert = 1;
					}
	
					# �ݷݸނ���o����ڲ԰�����O
					# �����ʂ�����̂�1�l�ł͂Ȃ��S���폜
					$count[1] = $prev_value == $p_ranks[$no][$j][0] ? $count[1]+1 : 0;
					my $rank = $count[0] - $count[1]; # �� - �_�u�萔 = ����
					if ($rank > $prev_rank && $prev_rank >= $max_ranking) {
						splice(@{$p_ranks[$no]}, $j, 1) while $p_ranks[$no][$j][0];
						last; # �S���폜�����̂Ŏ��̗v�f�͂Ȃ�
					}
	
					# ���̗v�f���ݸ�O���ǂ������肷��̂ɏ��ʂƒl���K�v
					($prev_rank, $prev_value) = ($rank, $p_ranks[$no][$j][0]);
					$count[0]++;
				}
=pod
				# �ݷݸނɎ������ް���}����āA�ݸ�O�ɏo���ް����폜
				# ���ʂ̍l���͂��Ȃ��Ă�������ł�
				for my $rank (0 .. $#{$p_ranks[$no]}) {
					if ($ydata{$status} > $p_ranks[$no][$rank][0]) {
						splice(@{$p_ranks[$no]}, $rank, 0, [$ydata{$status}, "$player$from"]);
						splice(@{$p_ranks[$no]}, $#{$p_ranks[$no]}-1, 1) if $#{$p_ranks[$no]} > $max_ranking; # ��а�ް���1���邩��$#
						last;
					}
				}
=cut
			}
		}
		close $fh;
	}
	close $cfh;

	# �e���ݷݸނ�10�ʈȓ�����ڲ԰��ǉ�
	for my $no (0 .. $#rank_status) {
		for my $rank (0 .. $#{$p_ranks[$no]}-1) {
			push(@line, "$p_ranks[$no][$rank][0]<>$p_ranks[$no][$rank][1]<>\n");
		}
		push @line, "0<><>\n";
	}
	undef(@p_ranks);

	open my $fh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
	print $fh @line;
	close $fh;

#	my $timer = tv_interval($t0);
#	print "$timer ms<br>";
}
