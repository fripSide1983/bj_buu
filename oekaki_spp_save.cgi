#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';

use CGI;
#================================================
# ���G�`���ۑ�(url_save) Powered by nanamie
#================================================

$cgi = CGI->new;

# ���e�ł���ő廲��
$max_data_size = 5000;

#================================================
&save_img();
exit;

#================================================
sub save_img {
	my $file = $cgi->param("file");
	
	my $fid = $cgi->param("id");
	my $fpass = $cgi->param("pass");
	
	my $image_type = $file eq '_temp.jpeg' ? "jpeg" : "png";
	
	&error_oekaki("no user dir") unless -d "$userdir/$fid";
	my %datas = &get_you_datas($fid, 1);
	&error_oekaki("wrong password") unless $datas{pass} eq $fpass;
	
	# �t�@�C���쐬���o�C�i���f�[�^�ǂݏ������t�@�C���T�C�Y��0�o�C�g�Ȃ�폜
	# �X�}�[�g����Ȃ��̂Ńt�@�C���T�C�Y�擾��1�o�C�g�ȏ�Ȃ�t�@�C���쐬�Ə������݂ɂ�����
	open my $fh, "> $userdir/$fid/picture/_$time.$image_type" or &error_oekaki("save failed");
	binmode $fh;
	my $file_size = 0;
	my $read_size = read($file, $buffer, 1024);
	while ($read_size) {
		$file_size += $read_size;
		print $fh $buffer;
		$read_size = read($file, $buffer, 1024);
	}
	close $fh;
	close $file;
	if ($file_size == 0) {
		unlink "$userdir/$fid/picture/_$time.$image_type";
		&error_oekaki("save failed\nyour web browser is not supported");
	}
	
	print "Content-type: text/plain\n\n";
}

#================================================
# ���G�`�����ɴװ�o��
sub error_oekaki {
	my $error_message = shift;
	print "Content-type: text/plain\n\nerror\n";
	print "$error_message\n";
	exit;
}

