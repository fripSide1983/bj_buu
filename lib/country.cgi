#================================================
# ����� Created by Merino
#================================================

# �ƭ� ���ǉ�/�ύX/�폜/���בւ��\
my @menus = (
	['��߂�',			'main'],
	['�e���̏��',		'country_info'],
	['�d��',			'country_move'],
	["$e2j{ceo}���[",	'country_leader'],
	['��\�����R��',	'country_review'],
	['��\\�҂̎d��',	'country_daihyo'], # ��\�҂̂ݕ\��
	["$e2j{ceo}�̎d��",	'country_config'], # �N��̂ݕ\��
);


#================================================
sub begin {
	my $line = &get_countries_mes($m{country}) if $m{country};
	my($country_mes, $country_mark) = split /<>/, $line;
	my @lines = &get_country_members($m{country});
	
	$mes .= qq|<font color="$cs{color}[$m{country}]">$c_m</font>|;
	$mes .= qq|<br><img src="$icondir/$country_mark">| if $country_mark;
	$mes .= qq|<br>$country_mes| if $country_mes;
	$mes .= qq|<hr size="1">�푈�F$cs{modify_war}[$m{country}] �����F$cs{modify_dom}[$m{country}] �R���F$cs{modify_mil}[$m{country}] �O���F$cs{modify_pro}[$m{country}]|;
	$mes .= qq|<hr size="1">������<br>@lines|;
	
	pop @menus unless $cs{ceo}[$m{country}] eq $m{name}; # �N��ȊO��\��
	pop @menus unless &is_daihyo; # ��\�҈ȊO��\��
	
	&menu(map{ $_->[0] }@menus);
}

sub tp_1 { &b_menu(@menus); }



1; # �폜�s��
