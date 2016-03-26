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
	my @p_ranks = (1,'','');
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
			
			my %p;
			my %pb = &get_you_datas($player_id, 1);
			
			open my $fh, "< $userdir/$player_id/year_ranking.cgi" or &error("year_ranking.cgi̧�ق��J���܂���");
			while (my $line = <$fh>) {
				my %ydata;
				for my $hash (split /<>/, $line) {
					my($k, $v) = split /;/, $hash;
					$ydata{$k} = $v;
					if($k eq 'year'){
						if($v != $last_year){
							next;
						}
					}
				}
				if($ydata{year} == $last_year){
					if($status eq 'mil_sum'){
						$ydata{$status} = $ydata{gou};
						if($ydata{cho} > $ydata{$status}){
							$ydata{$status} = $ydata{cho};
						}
						if($ydata{sen} > $ydata{$status}){
							$ydata{$status} = $ydata{sen};
						}
					}
					if($ydata{$status}){
						$p{$status} = $ydata{$status};
						$p{name} = $pb{name};
						if($status eq 'strong'){
							my $strong_c;
							my $strong_v = 0;
							for my $from_c (1 .. $w{country}){
								if($strong_v < $ydata{"strong_$from_c"}){
									$strong_v = $ydata{"strong_$from_c"};
									$strong_c = $from_c;
								}
							}
							$p{name} .= " $cs{name}[$strong_c]����ł��D��";
						}
						if($status eq 'win'){
							if($ydata{war} > 20){
								$p{$status} = 100 * $ydata{$status} / $ydata{war};
							}else{
								$p{$status} = 0;
							}
						}
						$p{country} = $pb{country};
					}
				}
			}
			close $fh;
			
			next if $p{$status} < $rank_min;
			
			my @datas = ();
			my @rdata = ();
			my $i = 1;
			
			while ($i <= $max_ranking){
				$rdata[0] = shift @p_ranks;
				$rdata[1] = shift @p_ranks;
				$rdata[2] = shift @p_ranks;
				if ($rdata[0] <= $p{$status}) {
					push @datas, $p{$status}, $p{name}, $p{country};
					push @datas, $rdata[0], $rdata[1], $rdata[2] unless $i >= $max_ranking && $p{$status} != $rdata[0];
					$i++;
					my $last_number = $datas[-3];
					while($i <= $max_ranking || $last_number == $p_ranks[0]){
						my $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						$last_number = $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						last if $cash eq '';
						$i++;
					}
				}else {
					push @datas, $rdata[0], $rdata[1], $rdata[2];
					$i++;
				}
				last if $rdata[1] eq '';
			}
			@p_ranks = ();
			push @p_ranks, @datas;
		}
		close $cfh;
	}
	my $no1_flag = 1;
	my $no1_value = 0;
	while ($p_ranks[1] ne '') {
		my @data;
		for my $j (0..2){
			$data[$j] = shift @p_ranks;
		}
		if(($no1_flag == 1 || $data[0] == $no1_value) && $status ne 'sal'){
			my $no1_name = $data[1];
			$no1_name =~ tr/\x0D\x0A//d;
			$no1_name =~ s/\s.*?����ł��D��$//;
			my $n_id = unpack 'H*', $no1_name;
			open my $ufh, ">> $userdir/$n_id/ex_c.cgi";
			print $ufh "no1_c<>1<>\n";
			close $ufh;
			
			if ($no1_flag) {
				$no1_flag = 0;
				$no1_value = $data[0];
			}
		}
		if($status eq 'rank'){
			$data[1] =~ tr/\x0D\x0A//d;
			my $player_id = unpack 'H*', $data[1];
			my %p = &get_you_datas($player_id, 1);
			my $rank_name = $ranks[$p{rank}];
			if ($p{super_rank}){
				$rank_name = '';
				$rank_name .= '��' for 1 .. $p{super_rank};
				$rank_name .= $p{rank_name};
			}
			push @line, "$rank_name<>$data[1]<>$data[2]\n";
		}else {
			push @line, "$data[0]<>$data[1]<>$data[2]\n";
		}
	}

	open my $fh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @line;
	close $fh;
}

