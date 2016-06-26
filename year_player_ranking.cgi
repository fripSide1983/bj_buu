#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';

use File::Copy;
#=================================================
# ��N�ݷݸ� Created by oiiiuiiii
#=================================================

my @rank_status = (
#�ϐ�,�\����,�Œ�l
    ['strong','�D����',5000],
    ['nou','�_��',100000],
    ['sho','����',100000],
    ['hei','����',100000],
    ['gou','���D',30000],
    ['cho','����',30000],
    ['sen','���]',30000],
    ['gou_t','���D(�݌v)',3000],
    ['cho_t','����(�݌v)',3000],
    ['sen_t','���](�݌v)',3000],
    ['gik','�U�v',50],
    ['res','�~�o',3],
    ['esc','�E��',3],
    ['tei','��@',30],
    ['win','�����i20��ȏ�j',50],
    ['stop','���',5],
    ['pro','�F�D',10],
    ['sal','����',10000],
    ['dai','���{',5],
#    ['mil_sum','�R��',1],
);


#=================================================
&decode;
&header;
&read_cs;

my $max_ranking = $in{rank_num} ? $in{rank_num} : 10;

$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @rank_status;
my $type = $rank_status[$in{no}][0] ? "_$rank_status[$in{no}][0]" : '';

my $this_file = "$logdir/year_player_ranking${type}.cgi";

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
	for my $i (0 .. $#rank_status) {
		print $i eq $in{no} ? qq|$rank_status[$i][1] / | : qq|<a href="?no=$i">$rank_status[$i][1]</a> / |;
	}
	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	my $year = <$fh>;
	close $fh;
	&update_player_ranking if ($w{year} > $year+1);

	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	my $year = <$fh>;
	print qq|<h1>$year�N$rank_status[$in{no}][1]�N���ݷݸ�</h1>|;
	print qq|<div class="mes"><ul><li>�ݷݸނ͖��N���Ƃ�ؾ�Ă���X�V����܂�</ul></div><br>|;

	print qq|<table class="table1" cellpadding="2"><tr><th>����</th><th>���l</th><th>���O</th><th>������</th></tr>| unless $is_mobile;
	
	my $pre_number = 0;
	my $d_rank;
	while ($line = <$fh>) {
		my($number,$name,$country) = split /<>/, $line;
		$id_name = $name;
		if($rank_status[$in{no}][0] eq 'strong'){
			$id_name =~ s/ .*?����ł��D��//g;
		}
		my $player_id =  unpack 'H*', $id_name;
		$d_rank = $rank if ($pre_number != $number);
		$pre_number = $number;
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
sub update_player_ranking  {
	for my $i(1..10){
		my $to_file_name;
		my $old_year = 10 - $i;
		my $old_file_name = $this_file;
		$old_file_name =~ s/\.cgi//;
		$to_file_name = $old_file_name;
		$old_file_name .= "_" . $old_year . ".cgi";
		if($old_year == 0){
			$old_file_name = $this_file;
		}
		my $to_year = $old_year + 1;
		$to_file_name .= "_" . $to_year . ".cgi";
		if(-f "$old_file_name"){
			if($old_year == 9){
				unlink $old_file_name;
			}else{
				move $old_file_name, $to_file_name;
			}
		}
	}

	my %sames = ();
	my @line = ();
	my @p_ranks = ();
	my $status = $rank_status[$in{no}][0];
	my $rank_min = $rank_status[$in{no}][2];
	
	my $last_year = $w{year} - 1;
	push @line, "$last_year\n";

	for my $country (0 .. $w{country}) {
		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgi̧�ق��J���܂���");
		while (my $player = <$cfh>) {
			$player =~ tr/\x0D\x0A//d;
			next if ++$sames{$player} > 1;
			my $player_id = unpack 'H*', $player;
			unless (-f "$userdir/$player_id/year_ranking.cgi") {
				next;
			}

			my $p_status = 0;
			open my $fh, "< $userdir/$player_id/year_ranking.cgi" or &error("year_ranking.cgi̧�ق��J���܂���");
			while (my $line = <$fh>) {
				next if (index($line, "year;$last_year", 0) < 0) || # �O�N�ȊO�̃f�[�^�͖��Ӗ��Ȃ̂ŉ�͂��Ȃ�
							(index($line, $status, 0) < 0); # �Q�Ɛ�f�[�^�������Ȃ��l�܂ŉ�͂��Ă����Ӗ�

				# �O�N�̈�N�ݷݸ��ް��̎��o��
				my %ydata;
				for my $hash (split /<>/, $line) {
					my($k, $v) = split /;/, $hash;
					$ydata{$k} = $v;
				}

				if ($status eq 'mil_sum') {
					$ydata{$status} = $ydata{gou};
					if($ydata{cho} > $ydata{$status}){
						$ydata{$status} = $ydata{cho};
					}
					if($ydata{sen} > $ydata{$status}){
						$ydata{$status} = $ydata{sen};
					}
				}
				elsif ($status eq 'strong') {
					my $strong_c;
					my $strong_v = 0;
					for my $from_c (1 .. $w{country}){
						if($strong_v < $ydata{"strong_".$from_c}){
							$strong_v = $ydata{"strong_".$from_c};
							$strong_c = $from_c;
						}
					}
					$player .= " $cs{name}[$strong_c]����ł��D��";
				}
				elsif ($status eq 'win') {
					$ydata{$status} = $ydata{war} > 20 ? 100 * $ydata{$status} / $ydata{war} : 0;
				}
				$p_status = $ydata{$status};
			}
			close $fh;
			next if $p_status < $rank_min;
			push @p_ranks, [$p_status, $player, $country]; # �ݸ����ڲ԰�̒ǉ�
		}
		close $cfh;
	}

	# �ݸ����ڲ԰�̂�����ʎ҂𔲂��o����1�ʂ̃v���C���[��No.1�n���t�^
	# �������̂��߂� sort ���g���ĂȂ�����0.08�b���炢���������Ȃ��c���̃f�[�^���傫����Ό��ʂ��肻��
	my $count = 0;
	my $old_max_value = 0;
	my @ranking = (0, 0); # ����, �_�u��
	while ($max_ranking > $ranking[0]) {
		last unless @p_ranks;

		# sort �̑���Ƀg�b�v�����������o��
		my $max_value = 0;
		my $max_index = 0;
		for my $index (0 .. $#p_ranks) {
			if ($p_ranks[$index][0] > $max_value) {
				$max_value = $p_ranks[$index][0];
				$max_index = $index;
			}
		}

		# 2�ʈȉ�����ʂƓ������l�Ȃ�_�u���������A�Ⴄ�Ȃ�_�u�������Z�b�g
		$ranking[1] = $old_max_value > $max_value ? 0 : $ranking[1]+1 if $count > 0;
		$ranking[0] = $count+1 - $ranking[1]; # (�C���f�b�N�X+1) - �_�u���� = ����

		# �����ݷݸވȊO��1�ʂ̃v���C���[�� No.1 �n���t�^
		if ($status ne 'sal' && $ranking[0] == 1) {
			my $no1_name = $p_ranks[$max_index][1];
			$no1_name =~ s/\s.*?����ł��D��$//;
			my $n_id = unpack 'H*', $no1_name;
			open my $ufh, ">> $userdir/$n_id/ex_c.cgi";
			print $ufh "no1_c<>1<>\n";
			close $ufh;
		}

		push(@line, join('<>', @{splice(@p_ranks, $max_index, 1)})."\n");
		$count++;
		$old_max_value = $max_value;
	}

=pod
	if (@p_ranks) {
		# sort��1�s�ɂł��邯�ǔz��̑S�v�f�𑀍삹�����ݸ�݂�����ڲ԰�������߯����遪�̕�������
		@p_ranks = sort {$b->[0] <=> $a->[0]} @p_ranks;

		# �ݷݸ��ް��̏������ݏ���
		my @ranking = (0, 0); # ����, �_�u��
		for my $count (0 .. $#p_ranks) {
			# 2�ʈȉ�����ʂƓ������l�Ȃ�_�u���������A�Ⴄ�Ȃ�_�u�������Z�b�g
			$ranking[1] = $p_ranks[$count-1][0] > $p_ranks[$count][0] ? 0 : $ranking[1]+1 if $count > 0;
			$ranking[0] = $count+1 - $ranking[1]; # (�C���f�b�N�X+1) - �_�u���� = ����

			# �����ݷݸވȊO��1�ʂ̃v���C���[�� No.1 �n���t�^
			if ($status ne 'sal' && $ranking[0] == 1) {
				my $no1_name = $p_ranks[0][1];
				$no1_name =~ s/\s.*?����ł��D��$//;
				my $n_id = unpack 'H*', $no1_name;
				open my $ufh, ">> $userdir/$n_id/ex_c.cgi";
				print $ufh "no1_c<>1<>\n";
				close $ufh;
			}

			push @line, "$p_ranks[$count][0]<>$p_ranks[$count][1]<>$p_ranks[$count][2]\n";
			last if $ranking[0] >= $max_ranking; # ���ʂ� $max_ranking �ȏ�ɂȂ����炨�I��
		}
	}
=cut
	open my $fh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");
	print $fh @line;
	close $fh;
}

