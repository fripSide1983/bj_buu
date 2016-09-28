#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#=================================================
# ����
#=================================================
my $this_script = 'shop_big_data.cgi';
my $csv_script = 'shop_big_data_csv.cgi';
my $update_day = 2 * 3600;

#=================================================
&decode;
&header;

my ($kind, $no) = split /_/, $in{item}; 
$kind ||= 1;
$no ||= 1;
$kind = 1 if $kind < 1 || $kind > 4;

my $this_file = "$htmldir/item_${kind}_${no}.html";
my $html_file = "html/item_${kind}_${no}.html";

if (-e $this_file) {
	if ((stat $filename)[9] + $update_day < $time) {
		&create_sale_data_chart($kind, $no);
	}
} else {
	&create_sale_data_chart($kind, $no);
}
&run;
&footer;
exit;

#=================================================
# �ݷݸމ��
#=================================================
sub run {
	print qq|<form action="$script_index"><input type="submit" value="�s�n�o" class="button1"></form>|;
	print qq|<form action="$csv_script"><input type="submit" value="�S�f�[�^CSV�擾" class="button1"></form>|;
	print qq|<hr>���,�A�C�e���ԍ�,�A�C�e���ϐ�1,�A�C�e���ϐ�2,�l�i,���(1:���l�̂��X,2:������,3:�����ݑ���,4:�ެݸ�����,5:�j����),���ԁiUNIX���ԁj,�A�C�e����<hr>|;

	if (-e $this_file) {
		print qq|<a href="$html_file" target="_blank">����</a>|;
	} else {
		print qq|�Q�l�f�[�^������܂���B|;
	}
	print qq|<hr>|;
	print qq|<form action="$this_script">|;
	print qq|<select name="item">|;
	for $i (1..$#weas) {
		if ($i ne '0') {
			print qq|<option value="1_$i">[$weas[$i][2]]$weas[$i][1]</option>|;
		}
	}
	print qq|</select>|;
	print qq|<input type="submit" value="����" class="button1">|;
	print qq|</form>|;
	
	print qq|<form action="$this_script">|;
	print qq|<select name="item">|;
	for $i (1..$#eggs) {
		if ($i ne '53') {
			print qq|<option value="2_$i">$eggs[$i][1]</option>|;
		}
	}
	print qq|</select>|;
	print qq|<input type="submit" value="��" class="button1">|;
	print qq|</form>|;
	
	print qq|<form action="$this_script">|;
	print qq|<select name="item">|;
	for $i (1..$#pets) {
		if ($i ne '180' && $i ne '181' && $pets[$i][0] > 0) {
			print qq|<option value="3_$i">$pets[$i][1]</option>|;
		}
	}
	print qq|</select>|;
	print qq|<input type="submit" value="�߯�" class="button1">|;
	print qq|</form>|;
	
	print qq|<form action="$this_script">|;
	print qq|<select name="item">|;
	for $i (1..$#guas) {
		if ($guas[$i][1] !~ /������/) {
			print qq|<option value="4_$i">[$guas[$i][2]]$guas[$i][1]</option>|;
		}
	}
	print qq|</select>|;
	print qq|<input type="submit" value="�h��" class="button1">|;
	print qq|</form>|;

}
