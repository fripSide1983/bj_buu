#!/usr/local/bin/perl --
use CGI::Carp qw(fatalsToBrowser);
require 'config.cgi';
require 'config_game.cgi';
#================================================
# Ҳ�CGI Created by Merino
#================================================
&get_data;
&error("��������ݽ���ł��B���΂炭���҂���������(�� $mente_min ����)") if ($mente_min);
&before_bj;
if ($m{wt} > 0) { # �S������
	if ($is_mobile) {
		my $next_time_mes = sprintf("���ɍs���ł���܂� %d��%02d�b<br>", int($m{wt} / 60), int($m{wt} % 60) );
		$mes .= &disp_now();
		$mes .= $next_time_mes;
	}
	elsif($is_smart) {
		my $next_time_mes = sprintf("%d��%02d�b", int($m{wt} / 60), int($m{wt} % 60) );
		my $reset_rest = int($w{reset_time} - $time);
		my $nokori_time = $m{next_salary} - $time;
		my $nokori_time_mes = sprintf("��<b>%d</b>��<b>%02d</b>����", $nokori_time / 3600, $nokori_time % 3600 / 60);
		$mes .= &disp_now();
		$mes .= qq|\n���ɍs���ł���܂� <span id="nokori_time">$next_time_mes</span>\n|;
		$mes .= qq|<script type="text/javascript"><!--\n nokori_time($m{wt}, $reset_rest);\n// --></script>\n|;
		$mes .= qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
		$mes .= qq|�G��[�O��F<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> �A��<b>$m{renzoku_c}</b>��]<br>| if $m{renzoku_c};
		$mes .= qq|���̋����܂� $nokori_time_mes|;
	}
	else{
		my $head_mes = '';
		if (-f "$userdir/$id/letter_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC66">�莆���͂��Ă��܂�</font><br>|;
		}
		if (-f "$userdir/$id/depot_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC00">�a���菊�ɉו����͂��Ă��܂�</font><br>|;
		}
		if (-f "$userdir/$id/goods_flag.cgi") {
			$main_screen .= qq|<font color="#FFCC99">ϲٰтɉו����͂��Ă��܂�</font><br>|;
		}
		my $next_time_mes = sprintf("%d��%02d�b", int($m{wt} / 60), int($m{wt} % 60) );
		my $reset_rest = int($w{reset_time} - $time);
		my $nokori_time = $m{next_salary} - $time;
		my $nokori_time_mes = sprintf("��<b>%d</b>��<b>%02d</b>����", $nokori_time / 3600, $nokori_time % 3600 / 60);

		$main_screen .= &disp_now();

		$main_screen .= qq|\n���ɍs���ł���܂� <span id="nokori_time">$next_time_mes</span>\n|;
		$main_screen .= qq|<script type="text/javascript"><!--\n nokori_time($m{wt}, $reset_rest);\n// --></script>\n|;
		$main_screen .= qq|<noscript>$next_time_mes</noscript>\n<br>\n|;
		$main_screen .= qq|�G��[�O��F<font color="$cs{color}[$m{renzoku}]">$cs{name}[$m{renzoku}]</font> �A��<b>$m{renzoku_c}</b>��]<br>| if $m{renzoku_c};
		$main_screen .= qq|���̋����܂� $nokori_time_mes|;
	}
	&n_menu;
	$menu_cmd .= qq|<form method="$method" action="bj_rest_shop.cgi">|;
	$menu_cmd .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$menu_cmd .= $is_mobile ? qq|<input type="submit" value="�X�ɍs��" class="button1" accesskey="#"><input type="hidden" name="guid" value="ON"></form>|: qq|<input type="submit" value="�X�ɍs��" class="button1"><input type="hidden" name="guid" value="ON"></form>|;

}
else {
	if (-f "./lib/$m{lib}.cgi") { # lib �Ăяo��
		if ($m{tp} eq '1' && $cmd eq '0') { # begin�ƭ���0(��߂�)��I������ݾ�
			if ($m{lib} =~ /shopping_/) {
				require './lib/shopping.cgi';
				&refresh;
				$m{lib} = 'shopping';
			}
			else {
				$mes .= '��߂܂���<br>';
				require './lib/main.cgi';
				&refresh;
			}
		}
		else {
			require "./lib/$m{lib}.cgi";
		}
	}
	else { # ��̫��lib �Ăяo��
		require './lib/main.cgi';
	}
	
	if ($m{tp}) { # lib ����
		&{ 'tp_'.$m{tp} } if &is_satisfy; # is_satisfy��1(true)�Ȃ珈������
	}
	else { # begin �ƭ�
		$m{tp} = 1;
		&begin;
	}
}

&auto_heal unless $is_battle;
$is_mobile ? require './lib/template_mobile_base.cgi' :
	$is_smart ? require './lib/template_smart_base.cgi' : require './lib/template_pc_base.cgi';
&write_user;
&footer;
# ------------------
# ���Ԃɂ���
sub auto_heal {
	my $v = $time - $m{ltime}; 
	$v = &use_pet('heal_up', $v);
	$v = int( $v / $heal_time ); 
	$m{hp} += $v;
	$m{mp} += int($v * 0.8);
	$m{hp} = $m{max_hp} if $m{hp} > $m{max_hp};
	$m{mp} = $m{max_mp} if $m{mp} > $m{max_mp};
}

sub disp_now {
	my $state = "���̑�";
	if($m{lib} eq 'domestic'){
		if($m{tp} eq '110'){
			if($m{turn} eq '1'){
				$state = "���K��";
			}elsif($m{turn} eq '3'){
				$state = "��K��";
			}else{
				$state = "���K��";
			}
			$state .= "�_�ƒ��ł�";
		}elsif($m{tp} eq '210'){
			if($m{turn} eq '1'){
				$state = "���K��";
			}elsif($m{turn} eq '3'){
				$state = "��K��";
			}else{
				$state = "���K��";
			}
			$state .= "���ƒ��ł�";
		}elsif($m{tp} eq '310'){
			if($m{turn} eq '1'){
				$state = "���K��";
			}elsif($m{turn} eq '3'){
				$state = "��K��";
			}else{
				$state = "���K��";
			}
			$state .= "�������ł�";
		}elsif($m{tp} eq '410'){
			if($m{turn} eq '1'){
				$state = "���K��";
			}elsif($m{turn} eq '3'){
				$state = "��K��";
			}elsif($m{turn} eq '5'){
				$state = "���K��";
			}else{
				$state = "���K��";
			}
			$state .= "�����������ł�";
		}
	}elsif($m{lib} eq 'military'){
		$state = "$cs{name}[$y{country}]�ֈړ����ł�";
		if($m{tp} eq '110'){
			$state .= "(���D)";
		}elsif($m{tp} eq '210'){
			$state .= "(����)";
		}elsif($m{tp} eq '310'){
			$state .= "(���])";
		}elsif($m{tp} eq '410'){
			$state .= "(��@)";
		}elsif($m{tp} eq '510'){
			$state .= "(�U�v)";
		}elsif($m{tp} eq '610'){
			if($m{value} eq 'military_ambush'){
				$state = "�R��";
			}else{
				$state = "�i�R";
			}
			$state .= "�҂��������ł�";
		}elsif($m{tp} eq '710'){
			$state .= "(�������D)";
		}elsif($m{tp} eq '810'){
			$state .= "(��������)";
		}elsif($m{tp} eq '910'){
			$state .= "(�������])";
		}
	}elsif($m{lib} eq 'prison'){
		$state = "$cs{name}[$y{country}]�̘S���ŗH���ł�";
	}elsif($m{lib} eq 'promise'){
		$state = "$cs{name}[$y{country}]�ֈړ����ł�";
		if($m{tp} eq '110'){
			$state .= "(�F�D)";
		}elsif($m{tp} eq '210'){
			$state .= "(���)";
		}elsif($m{tp} eq '310'){
			$state .= "(���z��)";
		}elsif($m{tp} eq '410'){
			$state .= "(��������)";
		}elsif($m{tp} eq '510'){
			$state .= "(�����j��)";
		}elsif($m{tp} eq '610'){
			$state = "�������ֈړ����ł�(�H���A��)";
		}elsif($m{tp} eq '710'){
			$state = "�������ֈړ����ł�(�����A��)";
		}elsif($m{tp} eq '810'){
			$state = "�������ֈړ����ł�(���m�A��)";
		}
	}elsif($m{lib} eq 'war'){
		$state = "$cs{name}[$y{country}]�ֈړ����ł�";
		if($m{value} eq '0.5'){
			$state .= "(�����i�R)";
		}elsif($m{value} eq '1'){
			$state .= "(�i�R)";
		}elsif($m{value} eq '1.5'){
			$state .= "(��������)";
		}
	}
	return "$state<br>\n";
}
1; # �폜�s�� login.cgi�� bj.cgi��require���Ă���
