#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
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
);


#=================================================
&decode;
&header;
&read_cs;

my $max_ranking = $in{rank_num} ? $in{rank_num} : 3;

$in{no} ||= 0;
$in{no} = int($in{no});
$in{no} = 0 if $in{no} > $w{country};
my $this_file = "$logdir/year_player_ranking_country_$in{no}.cgi";

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
			$id_name = $name;
			if($rank_status[$no][0] eq 'strong'){
				$id_name =~ s/ .*?����ł��D��//g;
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

	my @line = ();
	my $last_year = $w{year} - 1;
	
	push @line, "$last_year\n";
	$country = $in{no};
	
	for my $no (0..$#rank_status){
		my %sames = ();
		my @p_ranks = (1,'');
		my $status = $rank_status[$no][0];
		my $rank_min = $rank_status[$no][2];

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
						if($v != $w{year}){
							last;
						}
					}
				}
				if($ydata{year} == $last_year){
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
				if ($rdata[0] <= $p{$status}) {
					push @datas, $p{$status}, $p{name};
					push @datas, $rdata[0], $rdata[1] unless $i >= $max_ranking && $p{$status} != $rdata[0];
					$i++;
					my $last_number = $datas[-2];
					while($i <= $max_ranking || $last_number == $p_ranks[0]){
						my $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						$last_number = $cash;
						$cash = shift @p_ranks;
						push @datas, $cash;
						last if $cash eq '';
						$i++;
					}
				}else {
					push @datas, $rdata[0], $rdata[1];
					$i++;
				}
				last if $rdata[1] eq '';
			}
			@p_ranks = ();
			push @p_ranks, @datas;
		}
		close $cfh;
		
		while ($p_ranks[1] ne '') {
			my @data;
			for my $j (0..1){
				$data[$j] = shift @p_ranks;
			}
			push @line, "$data[0]<>$data[1]<>\n";
		}
		push @line, "0<><>\n";
	}

	open my $fh, "> $this_file" or &error("$this_filȩ�ق��J���܂���");

	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @line;
	close $fh;
}

