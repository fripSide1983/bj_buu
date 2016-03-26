#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# �����ݷݸ� Created by Merino
#=================================================

# �\���������(./log/�ɂ������)�@���ǉ�/�ύX/�폜/���בւ��\
my @files = (
#	['����',		'۸�̧�ٖ�(shop_list_xxxx���̕���)'],
	['���l�̂��X',	'',			'��'],
	['���̉攌��',	'picture',	'��'],
	['�ޯ�ϰ���',	'book',		'��'],
	['���l�̋�s',	'bank',		'��'],
);

# �Œ���K�v�Ȕ��㐔(���l�̂��X�̂�)
my $min_sale_c = 5;


#=================================================
&decode;
&header;
&read_cs;

$in{no} ||= 0;
$in{no} = 0 if $in{no} >= @files;
my $type = $files[$in{no}][1] ? "_$files[$in{no}][1]" : '';
my $flag_file = "$logdir/sales_ranking${type}_cycle_flag.cgi";
my $this_file = "$logdir/shop_list${type}.cgi";

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
		print $i eq $in{no} ? qq|$files[$i][0] / | : qq|<a href="?no=$i">$files[$i][0]</a> / |;
	}
	print qq|<a href="casino_ranking.cgi">��@����</a> / |;
	print qq|<h1>$files[$in{no}][0]�����ݷݸ�</h1>|;
	print qq|<div class="mes"><ul><li>�ݷݸނƊe���X�̔�����Ɣ��㐔�́A$sales_ranking_cycle_day�����Ƃ�ؾ�Ă���X�V����܂�|;

	if ($files[$in{no}][1] eq 'bank') {
		print "<li>�X�V�����ݸނŎ葱�񐔂� 0 ��̋�s�͓|�Y�ƂȂ�܂�";
		print "<li>�X�V�����ݸނő��a���z�� 100�� G�����̋�s�͓|�Y�ƂȂ�܂�";
		print qq|<li>���̍X�V���ԁF$month��$mday��$hour��$min��</ul></div><br>|;
		print qq|<table class="table1" cellpadding="2"><tr><th>����</th><th>���v</th><th>�葱��</th><th>��s��</th><th>�o�c��</th><th>ү����</th></tr>| unless $is_mobile;
	}
	else {
		if ($files[$in{no}][1] eq '') {
			print qq|<li>�X�V�����ݸނŔ��㐔�� $min_sale_c�����̂��X�͕X�ƂȂ�܂�|;
		}
		else {
			print qq|<li>�X�V�����ݸނŔ������ 0 G�̂��X�͕X�ƂȂ�܂�|;
		}
		print qq|<li>���̍X�V���ԁF$month��$mday��$hour��$min��</ul></div><br>|;
		print qq|<table class="table1" cellpadding="2"><tr><th>����</th><th>�����</th><th>���㐔</th><th>�X��</th><th>�X��</th><th>ү����</th></tr>| unless $is_mobile;
	}
	
	my $rank = 1;
	open my $fh, "< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	while ($line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money) = split /<>/, $line;
		print $is_mobile     ? qq|<hr><b>$rank</b>��/$sale_money G/$sale_c$files[$in{no}][2]/$shop_name/$name/$message/\n|
			: $rank % 2 == 0 ? qq|<tr><th>$rank��</th><td align="right">$sale_money G</td><td align="right">$sale_c$files[$in{no}][2]</td><td>$shop_name</td><td>$name</td><td>$message<br></td></tr>\n|
			:  qq|<tr class="stripe1"><th>$rank��</th><td align="right">$sale_money G</td><td align="right">$sale_c$files[$in{no}][2]</td><td>$shop_name</td><td>$name</td><td>$message<br></td></tr>\n|
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
	my %sames = ();
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($shop_name, $name, $message, $sale_c, $sale_money, $display, $guild_number) = split /<>/, $line;
		$display = '' if $display ne '1';
		# �޸ނł��X����ɂȂ��Ă�����̂�����
		next if ++$sames{$name} > 1;

		my $id = unpack 'H*', $name;
		next unless -f "$userdir/$id/shop${type}.cgi";
		
		open my $fh2, "+< $userdir/$id/shop_sale${type}.cgi";
		eval { flock $fh2, 2; };
		my $line2 = <$fh2>;
		my($m_sale_c, $m_sale_money, $m_update_t) = split /<>/, $line2;
		
		# ���l�̋�s�A���a������
		if ($files[$in{no}][1] eq 'bank' && &is_the_end("$userdir/$id/shop${type}.cgi") ) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			&write_send_news("<b>$name�̌o�c����$shop_name�͑��a���z��100�������̂��ߓ|�Y���܂���</b>", 1, $name);
			open my $fh, ">> $userdir/$id/ex_c.cgi";
			print $fh "ceo_c<>1<>\n";
			close $fh;
		}
		# ������� 0G �Ȃ�폜
		elsif ($m_sale_money <= 0 && $m_update_t < $time - 24 * 3600 && !($files[$in{no}][1] eq '' && $guild_number)) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			
			if ($files[$in{no}][1] eq 'bank') {
				&write_send_news("<b>$name�̌o�c����$shop_name�͌o�c�j�]�̂��ߓ|�Y���܂���</b>", 1, $name);
			}
			else {
				&write_send_news("<b>$name�̌o�c����$shop_name�͌o�c�j�]�̂��ߕX���܂���</b>", 1, $name);
			}
			open my $fh, ">> $userdir/$id/ex_c.cgi";
			print $fh "ceo_c<>1<>\n";
			close $fh;
		}
		# ���l�̂��X�͍Œ���K�v�Ȕ��㐔���`�F�b�N
		elsif ($files[$in{no}][1] eq '' && $m_sale_c < $min_sale_c && $m_update_t < $time - 24 * 3600) {
			close $fh2;
			unlink "$userdir/$id/shop${type}.cgi";
			unlink "$userdir/$id/shop_sale${type}.cgi";
			&write_send_news("<b>$name�̌o�c����$shop_name�͌o�c�j�]�̂��ߕX���܂���</b>", 1, $name);
			open my $fh, ">> $userdir/$id/ex_c.cgi";
			print $fh "ceo_c<>1<>\n";
			close $fh;
		}
		else {
			seek  $fh2, 0, 0,;
			truncate $fh2, 0;
			print $fh2 "0<>0<>$time<>";
			close $fh2;
			
			push @lines, "$shop_name<>$name<>$message<>$m_sale_c<>$m_sale_money<>$display<>$guild_number<>\n";
		}
	}
	@lines = map{ $_->[0] } sort { $b->[4] <=> $a->[4] } map { [$_, split /<>/] } @lines;
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	# �X�V�����׸�̧�ق��X�V
	open my $fh9, "> $flag_file";
	close $fh9;
}

sub is_the_end {
	my $bank_file = shift;
	
	my $sum_money = 0;
	open my $fh, "< $bank_file" or &error("$bank_filȩ�ق��ǂݍ��߂܂���");
	my $head_line = <$fh>;
	while (my $line = <$fh>) {
		my($year, $name, $money) = split /<>/, $line;
		$sum_money += $money;
	}
	close $fh;
	
	return $sum_money < 1000000 ? 1 : 0;
}



