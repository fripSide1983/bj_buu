#!/usr/local/bin/perl --

require './config.cgi';
require './config_game.cgi';

# �ǂݍ��ݗe�ʂ��I�[�o�[������Ԃ� cgi-lib.pl �����[�h����Ƃ�����̃G���[�Ɋ������܂�ė�����
# �G���[�Ɋ������܂��悤�ł���Ύ����ŃG���[����������
my $maxdata    = 131072;
my $len  = $ENV{'CONTENT_LENGTH'};
my $is_error = $len > $maxdata;
if ($is_error) {
	&decode;
}
else {
	require './cgi-lib.pl';
}

my $size = 15 * 1024;

&header;
&ReadParse unless $is_error; # cgi-lib.pl �̃G���[�Ɋ������܂��悤�łȂ����
if($in{back} eq '1'){
	&read_user;
	&read_cs;
	$m{lib} = 'shopping_upload';
	$m{tp} = 100;
	&write_user;
	&error("�C���[�K���ȃA�N�Z�X�ł�");
	&footer;
} else {
	my $_time = $time;
	my $newfile = ''; # �Ȃ��� add_picture ���Ŕ��ʂł��Ȃ��̂ŊO��
	&up_read_user;
	unless ($is_error) { # cgi-lib.pl �̃G���[�Ɋ������܂��悤�łȂ����
		if (-f "$userdir/$id/upload_token.cgi") {
			if($ENV{REQUEST_METHOD} eq 'POST'){
				$newfile = &add_picture($_time); # add_picture ���Ŕ��ʂł��Ȃ��̂ŊO�ɏo��
			}
		}

		if (!-f $newfile) { # �Ȃ��� add_picture �O�Ȃ画�ʂł���
			$m{lib} = 'shopping_upload';
			$m{tp} = 100;
			&write_user;
			&error("�C���[�W�t�@�C���̍쐬�Ɏ��s���܂���");
		}
		else {
			# �߲��������������ɂ��� upload_token.cgi ���폜
			# shopping_upload.cgi $m{tp} == 400 �̎��ɂ���̧�ق��c���Ă���Ȃ玸�s���Ă�Ɣ��f�ł���
			unlink "$userdir/$id/upload_token.cgi";
			&show_picture;
			&footer;
		}
	}
}
exit;

sub add_picture {
	my $time2 = shift;
	my $ext = '';
	my $path = "$userdir/$id/picture";

	for my $tmp (@in) {
		if ($tmp =~ /(.*)Content-type:(.*)/i) {
			if ($2 =~ /image\/jpeg/i) { $ext = '.jpg'; }
			elsif ($2 =~ /image\/pjpeg/i) { $ext = '.jpg'; }
			elsif ($2 =~ /image\/gif/i) { $ext = '.gif'; }
			elsif ($2 =~ /image\/png/i) { $ext = '.png'; }
			else { $ext = 'NO'; }
		}
		elsif ($tmp =~ /(.*)filename=(.*)/i) {
			if ($2 =~ /\.jpg/i) { $ext = '.jpg'; }
			elsif ($2 =~ /\.gif/i) { $ext = '.gif'; }
			elsif ($2 =~ /\.png/i) { $ext = '.png'; }
			else { $ext = 'NO'; }
		}
	}

	my $newfile = "$path/_$time2$ext";

	if (($ext eq 'NO') || ($ext eq '') || !defined($ext)) {
		$m{lib} = 'shopping_upload';
		$m{tp} = 100;
		&write_user;
		&error('�s���Ȋg���q�ł�');
	} else {
		open my $nfh,">$newfile" or &error("�C���[�W�t�@�C�������܂���");
		binmode $nfh;
		print $nfh $in{'upfile'};
		close $nfh;

		if(-s $newfile > $size){
			unlink $newfile;
			$m{lib} = 'shopping_upload';
			$m{tp} = 100;
			&write_user;
			&error("�T�C�Y���߂ł�(15KB�܂�)");
		}
	}
	return $newfile;
}

sub show_picture{
	$layout = 2;
	my $count = 0;
	opendir my $dh, "$userdir/$id/picture" or &error("ϲ�߸�����J���܂���");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^index.html$/;
		my $file_title = &get_goods_title($file_name);
		$sub_mes .= qq|<hr><img src="$userdir/$id/picture/$file_name" style="vertical-align:middle;"> $file_title |;
		++$count;
	}
	closedir $dh;
	print qq|$sub_mes<hr>|;
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	print qq|<input type="submit" value="Next" class="button1"><input type="hidden" name="guid" value="ON"></form>|;
}

sub up_read_user {
 # Get %m %y
	%m = ();
	%y = ();
	$id   = $in{id};
	$pass = $in{pass};
	open my $fh, "< $userdir/$id/user.cgi" or &error("�v���C���[�f�[�^���ǂݍ��߂܂���");
	my $line = <$fh>;
	close $fh;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		if ($k =~ /^y_(.+)$/) {
			$y{$1} = $v;
		}else {
			$m{$k} = $v;
		}
	}
	&error('�p�X���[�h���Ⴂ�܂�') unless $m{pass} eq $pass;
	# �S�����Ԃ�����ꍇ�A�o�ߎ��ԕ����炷
	$m{wt} -= ($time - $m{ltime}) if $m{wt} > 0;
}
