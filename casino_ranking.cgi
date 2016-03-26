#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# �����ݷݸ� 
#=================================================

# �\���������(./log/�ɂ������)�@���ǉ�/�ύX/�폜/���בւ��\
my @files = (
#	['����',		'۸�̧�ٖ�(shop_list_xxxx���̕���)'],
	['���l�̂��X',	'',			'��'],
	['���̉攌��',	'picture',	'��'],
	['�ޯ�ϰ���',	'book',		'��'],
	['���l�̋�s',	'bank',		'��'],
);

# �Œ���K�v�Ȕ��㐔
my $min_sale_c = 20;

# ��[��
my $treasury_base = 100000;

#=================================================
&decode;
&header;
&read_cs;

my $type = '_casino';
my $flag_file = "$logdir/sales_ranking_casino_cycle_flag.cgi";
my $this_file = "$logdir/shop_list_casino.cgi";

&update_sales_ranking if -M $flag_file > $sales_ranking_cycle_day;
&run;
&footer;
exit;

#=================================================
# �ݷݸމ��
#=================================================
sub run {
	my $flag_time = (stat $flag_file)[9];
	my($min, $hour, $mday, $month) = ( localtime( $flag_time + $sales_ranking_cycle_day * 24 * 3600) )[1..4];
	++$month;

	print qq|<form action="$script_index"><input type="submit" value="�s�n�o" class="button1"></form>|;
	for my $i (0 .. $#files) {
		print qq|<a href="sales_ranking.cgi?no=$i">$files[$i][0]</a> / |;
	}
	print qq|��@���� / |;
	print qq|<h1>��@���ɔ����ݷݸ�</h1>|;
	print qq|<div class="mes"><ul><li>�ݷݸނƊe���X�̔�����Ɣ��㐔�́A$sales_ranking_cycle_day�����Ƃ�ؾ�Ă���X�V����܂�|;

	print qq|<li>�X�V�����ݸނŃv���C�񐔐��� $min_sale_c�����̂��X�͕X�ƂȂ�܂�|;
	print qq|<li>���̍X�V���ԁF$month��$mday��$hour��$min��</ul></div><br>|;
	print qq|<table class="table1" cellpadding="2"><tr><th>����</th><th>�����</th><th>���㐔</th><th>�X��</th><th>�X��</th><th>ү����</th></tr>| unless $is_mobile;
	
	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	while ($line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		print $is_mobile     ? qq|<hr><b>$rank</b>��/$sale_money ���/$sale_c ��/$shop_name/$name/$message/\n|
			: $rank % 2 == 0 ? qq|<tr><th>$rank��</th><td align="right">$sale_money ���</td><td align="right">$sale_c ��</td><td>$shop_name</td><td>$name</td><td>$message<br></td></tr>\n|
			:  qq|<tr class="stripe1"><th>$rank��</th><td align="right">$sale_money ���</td><td align="right">$sale_c ��</td><td>$shop_name</td><td>$name</td><td>$message<br></td></tr>\n|
			;
		++$rank;
	}
	close $fh;
	
	print qq|</table>| unless $is_mobile;
}

#=================================================
# �����ݷݸނ��X�V
#=================================================
sub update_sales_ranking  {
	# �X�V�����׸�̧�ق��X�V
	open my $fh9, "> $flag_file";
	close $fh9;
	
	my %sames = ();
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		# �޸ނł��X����ɂȂ��Ă�����̂�����
		next if ++$sames{$name} > 1;

		my $id = unpack 'H*', $name;
		next unless -f "$userdir/$id/shop${type}.cgi";
		
		open my $fh2, "+< $userdir/$id/casino_pool.cgi";
		eval { flock $fh2, 2; };
		my $line2 = <$fh2>;
		my($pool, $this_term_gain, $slot_runs) = split /<>/, $line2;
		
		# �l�C�`�F�b�N
		if ($slot_runs <= $min_sale_c) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			
			&write_send_news("<b>$name�̌o�c����$shop_name�͌o�c�j�]�̂��ߕX���܂���</b>", 1, $name);
		} else {
			seek  $fh2, 0, 0,;
			truncate $fh2, 0;
			print $fh2 "$pool<>0<>0<>";
			close $fh2;
			
			push @lines, "$shop_name<>$name<>$message<>$slot_runs<>$this_term_gain<>\n";
		}
	}
	@lines = map{ $_->[0] } sort { $b->[4] <=> $a->[4] } map { [$_, split /<>/] } @lines;
	
	$top_name = '';
	$treasury = 0;
	for my $line (@lines) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		if ($top_name eq '') {
			$top_name = $name;
		} else {
			my $id = unpack 'H*', $name;
			open my $fh2, "+< $userdir/$id/casino_pool.cgi";
			eval { flock $fh2, 2; };
			my $line2 = <$fh2>;
			my($pool, $this_term_gain, $slot_runs) = split /<>/, $line2;
			$treasury_s = $treasury_base + int($pool * 0.01);
			if ($pool > $treasury_s) {
				$treasury += $treasury_s;
				$pool -= $treasury_s;
			} else {
				$treasury += $pool;
				$pool = 0;
			}
			
			seek  $fh2, 0, 0,;
			truncate $fh2, 0;
			print $fh2 "$pool<>0<>0<>";
			close $fh2;
		}
	}
	my $id = unpack 'H*', $top_name;
	open my $fh2, "+< $userdir/$id/casino_pool.cgi";
	eval { flock $fh2, 2; };
	my $line2 = <$fh2>;
	my($pool, $this_term_gain, $slot_runs) = split /<>/, $line2;
	
	$pool += $treasury;
	
	seek  $fh2, 0, 0,;
	truncate $fh2, 0;
	print $fh2 "$pool<>0<>0<>";
	close $fh2;
	
	
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
}