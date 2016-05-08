require 'config_game.cgi';

sub write_change {
	my ($bname, $bcomment, $chat_flag) = @_;
	while(1){
		if($bcomment =~ /(.*)&amp;dice\((\d+)\)(.*)/){
			my $dice = int(rand($2)+1);
			$bcomment = "$1$m{name}��$2�ʃ_�C�X��U�����B�o�ڂ�$dice�I�y�_�C�X�z$3";
			if($2 >= 100 && $dice == 1){
				&dice_fumble($2);
			}
		}else{
			last;
		}
	}
	while(1){
		if($bcomment =~ /(.*)&amp;(\d+)[dD](\d+)\(\)(.*)/){
			my $dice = 0;
			my $d_num = $2;
			if ($d_num > 100) {
				$d_num = 100;
			}
			$bcomment = "$1$m{name}��$3�ʃ_�C�X��$d_num�U�����B�o�ڂ�";
			for my $i (1..$d_num){
				my $t_dice = int(rand($3)+1);
				$dice += $t_dice;
				$bcomment .= $i == 1 ? "$t_dice" : ",$t_dice";
			}
			$bcomment .= "���v$dice�I�y�_�C�X�z$4";
			if($3 ** $d_num >= 100 && $dice == $d_num){
				&dice_fumble($3, $d_num);
			}
		}else{
			last;
		}
	}
	while(1){
		if($bcomment =~ /(.*)&amp;(\d+)[dD](\d+)\((\d+)\)(.*)/){
			my $dice = $4;
			my $d_num = $2;
			if ($d_num > 100) {
				$d_num = 100;
			}
			$bcomment = "$1$m{name}��$3�ʃ_�C�X��$d_num�U�����B�o�ڂ�";
			for my $i (1..$d_num){
				my $t_dice = int(rand($3)+1);
				$dice += $t_dice;
				$bcomment .= $i == 1 ? "$t_dice" : ",$t_dice";
			}
			$bcomment .= "�I�Œ�l��$4�B���v$dice�I�y�_�C�X�z$5";
			if($3 ** $d_num >= 100 && $dice == $d_num){
				&dice_fumble($3, $d_num);;
			}
		}else{
			last;
		}
	}
	$bcomment =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"link.cgi?$2\" target=\"_blank\">$2<\/a>/g;
	#"
	if($bcomment =~ /&amp;fusianasan/){
		$bname = "$host";
		$bcomment =~ s|&amp;fusianasan||g;
	}
	if($bcomment =~ /(.*)&amp;admin_set\((.+)=(\d+)\)(.*)/){
		my $change_mes = '';
		if (&is_sabakan) {
			my $this_config = $this_file . '_config.cgi';
			my %bbs_config = ();
			$bbs_config{shogo_limit} = 16;
			if (-f $this_config) {
				open my $fhc, "< $this_config" or &error("$this_config ̧�ق��J���܂���");
				my $config_line = <$fhc>;
				for my $config_hash (split /<>/, $config_line) {
					my($k, $v) = split /;/, $config_hash;
					$bbs_config{$k} = $v;
				}
			}
			$bbs_config{$2} = $3;
			my $config_line;
			foreach my $key (keys(%bbs_config)) {
				$config_line .= "$key;$bbs_config{$key}<>";
			}
	
			open my $fhc, "> $this_config" or &error("$this_config ̧�ق��J���܂���");
			print $fhc $config_line;
			close $fhc;
			
			$change_mes = "�y�I�ǃR�}���h�z$this_config ���C�����܂��B"
		}
		$bcomment = "$1$change_mes$4";
	}
	if($bcomment =~ /&amp;img/){
		$bcomment =~ s|&amp;img|<amp_img>|;
		if($bcomment =~ /&amp;img/){
			&error('img�^�O�͈�̓��e�ɂ���܂łł�');
		}
		$bcomment =~ s|<amp_img>|&amp;img|;
	}

	return ($bname, $bcomment);
}

sub dice_fumble{
	my ($dice_size, $number) = @_;
	if($m{shogo} ne $shogos[1][0] && $m{shogo_t} ne $shogos[1][0]){
		if($number){
			$m{shogo} = "����$dice_size�ʃ_�C�X$number�U���ăt�@���u���o����";
		}else{
			$m{shogo} = "����$dice_size�ʃ_�C�X�Ńt�@���u���o����";
		}
		&write_user;
	}
}


1; # �폜�s��
