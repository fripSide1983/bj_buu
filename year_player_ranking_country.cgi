#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
use Time::HiRes qw(gettimeofday tv_interval);
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
#			my $from_c;
			if($rank_status[$no][0] eq 'strong'){
				$id_name =~ s/ .*?����ł��D��//;
#				$from_c = $name;
#				$from_c =~ s/.*?( .*?����ł��D��)/\1/g;
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
	my $t0 = [gettimeofday];

	my @line = ();
	my $last_year = $w{year} - 1;

	push @line, "$last_year\n";
	$country = $in{no};

	my %sames = ();
	my @p_ranks = ();
	for my $no (0 .. $#rank_status) {
		push(@{$p_ranks[$no]}, [0, 0]);
	}

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

				# �ݷݸނɎ������ް���}����āA�ݸ�O�ɏo���ް����폜
				my $rank_size = $#{$p_ranks[$no]};
				for my $rank (0 .. $rank_size) {
					if ($ydata{$status} > $p_ranks[$no][$rank][0]) {
						splice(@{$p_ranks[$no]}, $rank, 0, [$ydata{$status}, "$player$from"]);
						if ($#{$p_ranks[$no]} > $max_ranking) {
							splice(@{$p_ranks[$no]}, $#{$p_ranks[$no]}-1, 1);
						}
						last;
					}
				}
			}

		}
		close $fh;
	}
	close $cfh;

	for my $no (0 .. $#rank_status) {
=pod
		# �������̂��߂� sort ���g�킸�ݸ����ڲ԰�̏�ʎ҂𔲂��o��
		my $count = 0;
		my $old_max_value = 0;
		my @ranking = (0, 0); # ����, �_�u��
		while ($max_ranking > $ranking[0]) {
			last unless @{$p_ranks[$no]};
	
			# sort �̑���Ƀg�b�v�����������o��
			my $max_value = 0;
			my $max_index = 0;
			for my $index (0 .. $#{$p_ranks[$no]}) {
				if ($p_ranks[$no][$index][0] > $max_value) {
					$max_value = $p_ranks[$no][$index][0];
					$max_index = $index;
				}
			}
	
			# 2�ʈȉ�����ʂƓ������l�Ȃ�_�u���������A�Ⴄ�Ȃ�_�u�������Z�b�g
			$ranking[1] = $old_max_value > $max_value ? 0 : $ranking[1]+1 if $count > 0;
			$ranking[0] = $count+1 - $ranking[1]; # (�C���f�b�N�X+1) - �_�u���� = ����
=cut

			for my $rank (0 .. $max_ranking-1) {
				push(@line, "$p_ranks[$no][$rank][0]<>$p_ranks[$no][$rank][1]<>\n");
			}
#			push(@line, join('<>', @{splice(@{$p_ranks[$no]}, $max_index, 1)})."<>\n");
#			$count++;
#			$old_max_value = $max_value;
		}
		push @line, "0<><>\n";
	}

#	open my $fh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
#	print $fh @line;
#	close $fh;

	my $timer = tv_interval($t0);
	print "$timer ms<br>";
}
