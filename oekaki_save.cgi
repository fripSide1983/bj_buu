#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
#================================================
# ���G�`���ۑ�(url_save) Created by Merino
#================================================

# ���e�ł���ő廲��
$max_data_size = 5000;


#================================================
$ENV{REQUEST_METHOD} =~ tr/a-z/A-Z/;
&error_oekaki("POST�ȊO��ظ���ҿ��ނ͎�M�ł��܂���") unless $ENV{REQUEST_METHOD} eq 'POST';
&error_oekaki("�ް����傫�����܂�") if $ENV{CONTENT_LENGTH} > $max_data_size;

my $buf = '';
binmode STDIN;
read(STDIN, $buf, $ENV{CONTENT_LENGTH});

my $header_magic = substr($buf, 0, 1);
if ($header_magic =~ /^[SP]$/) { &save_img($buf); }
else { &error_oekaki('�Ή����Ă��Ȃ��ײ��Ăł�'); }
exit;

#================================================
sub save_img {
	my $buf = shift;
	
	my $header_length      = substr($buf, 1, 8);
	my $send_header_length = index($buf, ";", 1 + 8);
	my $send_header        = substr($buf, 1 + 8, $send_header_length - (1 + 8) );
	my $img_length         = substr($buf, 1 + 8 + $header_length, 8);
	my $img_data           = substr($buf, 1 + 8 + $header_length + 8 + 2, $img_length);
	
	my %p = ();
	for my $pair (split /&/, $send_header) {
		my($k, $v) = split /=/, $pair;
		$p{$k} = $v;
	}
	
	&error_oekaki("��ڲ԰�o�^����Ă��܂���") unless -d "$userdir/$p{id}";
	my %datas = &get_you_datas($p{id}, 1);
	&error_oekaki("��ڲ԰�߽ܰ�ނ��Ⴂ�܂�") unless $datas{pass} eq $p{pass};
	
	$p{image_type} =~ tr/A-Z/a-z/;
	&error_oekaki("PNG��JPEG�ȊO�̏o�͂͋�����Ă��܂���") unless $p{image_type} eq 'jpeg' || $p{image_type} eq 'png';
	&error_oekaki("JPEG�ȊO�̏o�͂͋�����Ă��܂���")      if $is_force_jpeg && $p{image_type} ne 'jpeg';
	
	open my $fh, "> $userdir/$p{id}/picture/_$p{time}.$p{image_type}" or &error_oekaki("�摜�̕ۑ��Ɏ��s���܂���");
	binmode $fh;
	print $fh $img_data;
	close $fh;
	
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

