#================================================
# �Ċ֐�
#================================================
require './lib/jcode.pl';
use File::Copy::Recursive qw(rcopy);
use File::Path;

#================================================
# �ăC�x
#================================================
sub on_summer {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($month == 7) {
		return 1;
	}
	return 0;
}
#================================================
# �N���C�x
#================================================
sub on_december {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($month == 11) {
		return 1;
	}
	return 0;
}
#================================================
# �V�t�C�x
#================================================
sub on_new_year {
	my ($sec,$min,$hour,$mday,$month,$year,$wday,$stime) = localtime($time); 
	if ($month == 0) {
		return 1;
	}
	return 0;
}
1; # �폜�s��
