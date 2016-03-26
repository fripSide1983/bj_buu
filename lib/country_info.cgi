#=================================================
# �����\�� Created by Merino
#=================================================
sub begin {
	$layout = 2;
	$mes .= "<hr>�F�D�x/���<hr>";
	if ($m{country}) {
		for my $i (1 .. $w{country}) {
			next if $m{country} eq $i;
			&_chain_promise($m{country}, $i);
		}
	}
	for my $j (1 .. $w{country}) {
		next if $m{country} eq $j;
		for my $i ($j+1 .. $w{country}) {
			next if $m{country} eq $i;
			&_chain_promise($j, $i);
		}
	}

	$mes .= "<hr>�e����\\��";
	if ($m{country}) {
		$mes .= qq|<hr><font color="$cs{color}[$m{country}]">$cs{name}[$m{country}] �l��($cs{member}[$m{country}]/$cs{capacity}[$m{country}]) ����$cs{win_c}[$m{country}]</font><br>|;
		for my $k (qw/ceo war dom pro mil/) {
			$mes .= qq|$e2j{$k}:$cs{$k}[$m{country}]<br>| if $cs{$k}[$m{country}];
		}
	}
	for my $i (1 .. $w{country}) {
		next if $m{country} eq $i;
		$mes .= qq|<hr><font color="$cs{color}[$i]">$cs{name}[$i] �l��($cs{member}[$i]/$cs{capacity}[$i]) ����$cs{win_c}[$i]</font><br>|;
		for my $k (qw/ceo war dom pro mil/) {
			$mes .= qq|$e2j{$k}:$cs{$k}[$i]<br>| if $cs{$k}[$i];
		}
	}
	
	$mes .= "<hr>���̕��j/�����";
	my @lines = &get_countries_mes();
	if ($m{country}) {
		my($country_mes, $country_mark) = split /<>/, $lines[$m{country}];
		if ($country_mes || $country_mark) {
			$mes .= qq|<hr>|;
			$mes .= qq|<img src="$icondir/$country_mark" style="vertical-align:middle;" $mobile_icon_size><font color="$cs{color}[$m{country}]">$cs{name}[$m{country}]</font><br>| if $country_mark;
			$mes .= qq|<font color="$cs{color}[$m{country}]">$country_mes</font><br>| if $country_mes;
		}
	}
	for my $i (1 .. $w{country}) {
		next if $m{country} eq $i;

		my($country_mes, $country_mark) = split /<>/, $lines[$i];
		if ($country_mes ne '' || $country_mark ne '') {
			$mes .= qq|<hr>|;
			$mes .= qq|<img src="$icondir/$country_mark" style="vertical-align:middle;" $mobile_icon_size><font color="$cs{color}[$i]">$cs{name}[$i]</font><br>| if $country_mark;
			$mes .= qq|<font color="$cs{color}[$i]">$country_mes</font><br>| if $country_mes;
		}
	}
	
	&refresh;
	$m{lib} = 'country';
	&n_menu;
}

# ------------------
sub _chain_promise {
	my($c1, $c2) = @_;
	my $c_c = &union($c1, $c2);
	my $f_c_c  = 'f_'  . $c_c;
	my $p_c_c = 'p_' . $c_c;
	my $p_state = $w{$p_c_c} eq '1' ? '����'
				: $w{$p_c_c} eq '2' ? '���'
				:                     ''
				;
	
	$mes .= qq|<font color="$cs{color}[$c1]">$cs{name}[$c1]</font>-|;
	$mes .= qq|<font color="$cs{color}[$c2]">$cs{name}[$c2]</font> $w{$f_c_c}% $p_state<br>|;
}


1; # �폜�s��
