package FlockWrapper;
#########################################################
# flock Wrapper
# (C)2004 PANDORA C4 script by ZeRo
# http://pandora.nu admin@pandora.nu
#########################################################
#
# ����
# 	flock�λȤ�̵���Ķ���̵������flock���񤭤��ơ�
# 	mkdir symlik ��Ȥä���å���¹Ԥ���⥸�塼��
#
#	���Υ⥸�塼��ϼ�����Ǥ�ǻȤäƲ����������Υ⥸�塼���Ȥ�
#	�����ʤ�پ㡢»����ȯ�����Ƥ�⥸�塼������Ԥ���Ǥ�򤪤��ޤ���
#
# ���
#	̵������flock��close���񤭤��Ƥ�Τǡ������ǤϤ���ޤ���
#	local�ʤɤǶ˾������Ƥ���GLOB(handle)�ȶ˾������Ƥ��ʤ�GLOB��
#	���̤��Ǥ��ʤ����ᡢGLOB(handle)̾��Ʊ����Τ��٤����Ѥ��Ƥ���
#	�褦�ʥ�����ץȤˤ�Ŭ���Ƥ��ޤ��󡣤��ξ��ϡ������������ɤ�
#	�������������ᤤ�Ǥ��礦��
#
# �Ȥ���
#	use FlockWrapper ( 
#		flock   => ��å��Υ⡼��(flock mkdir symlink)��
#		           Ǥ�դΥ����ɥ�ե����,
#
#		dir     => mkdir symlink��Ȥä���å���ư�����
#				   ����Υǥ쥯�ȥ�ʥѡ��ߥå�����777�ˤ��뤳��),
#				   �ǥե���Ȥ� "." �����ȥǥ쥯�ȥ�
#
#		try     => mkdir symlink ��Ȥä���å��ǥ�å��μ���
#                  ���ߤ������ꤹ�롣
#				   �ǥե���Ȥ� 5 ��
#
#		timeout => mkdir symlink ��Ȥä���å��Ǻ���������å�
#				   ����Ū�˲������ޤǤλ��֡��á�
#				   �ǥե���Ȥ� 60 ��
#
#		close   => mkdir symlink ��Ȥä���å���flock�θƤӽФ����Ф�
#				   �ʤ�close���񤭤��뤫�ɤ����ʤ���:1, ���ʤ�:0��
#				   �ǥե���Ȥ� 1
#
#       clean   => ������ץȽ�λ���˥�å���������ʤ���:1�����ʤ�:0��
#                  �ǥե���Ȥ� 1
#
#		debug   => �ǥХå�����ν��ϡʤ���:1�����ʤ�:0��
#	);
#
# DEBUG
#	use strict;
#	use lib q(.);
#	use FlockWrapper (flock => 'mkdir', dir => './lock', clean => 0, debug => 1);
#	# ����Τ褦�˰�������ꤹ�롣
#
#	local(*IN);
#	print "handle ref: ". \*IN. "\n";
#   open(IN, "+<./lockfile") or die $!;
#	flock(IN, 2);
#	# �������ǥ�����ץȤ�λ����ȡ�dir�ǻ��ꤷ���ǥ쥯�ȥ��mkdir��
#	# ���������ǥ쥯�ȥ꤬¸�ߤ�������狼�롣
#
#	close(IN);
#	# ��������mkdir�Ǻ��������ǥ쥯�ȥ꤬�������Ƥ��ok
#
#
# ��
#	use strict;
#	use lib q(.);
#	use FlockWrapper(flock => 'mkdir', dir => './lock');
#
#	# ��������
#	local(*LOCK);
#	open(LOCK, "+<lockfile") or die $!;
#	flock(LOCK, 2);
#	#���������񤭤��ƶ���Ū��mkdir��å���¹�
#
#	��������ά������
#
#	close(LOCK);
#	# ���������񤭤��Ƥ���Τ������ǥ�å�������롣
#
######################################################

my %args = ();
my %handle = ();

my %lock = ();
$lock{mkdir}   = \&lock_mkdir;
$lock{symlink} = \&lock_symlink;

BEGIN { sub import
{
	my $pkg = shift;
	%args = @_;

	# �ѥ�᡼���ν����
	$args{dir}       = "." if !defined($args{dir});
	$args{dir}       =~ s/\/$//;
	$args{fname}     = $args{dir}. "/lockfile";
	$args{try}     ||= 10;
	$args{timeout} ||= 60;
	$args{unlocked}  = 0;
	$args{clean}     = 1 if !defined($args{clean});
	$args{close}     = 1 if !defined($args{close});
	$args{debug}   ||= 0;

	# flock �� close �Υ�åѺ���
	my $code = undef;
	if (!defined($args{flock})) {
		return;
	} elsif ($args{flock} eq 'flock') {
		return;
	} elsif (ref($args{flock}) eq 'CODE') {
		$code = $args{flock};
	} elsif (defined($lock{$args{flock}})) {
		$code = $lock{$args{flock}};
	} else {
		die "undefined lock mode.";
	}
	*CORE::GLOBAL::flock = undef;
	*CORE::GLOBAL::close = undef;
	*CORE::GLOBAL::flock = sub(*$) {
		no strict q/refs/;
		my $call = caller(0);
		my $ref = $_[0];
		$ref = \*{"${caller}::$ref"} if ref($ref) ne 'GLOB';
		print STDERR "flock:$ref\n" if $args{debug};
		$handle{$ref} = 1;
		$code->();
	};
	if ($args{close}) {
		*CORE::GLOBAL::close = sub(*) {
			no strict q/refs/;
			my $call = caller(0);
			my $ref = $_[0];
			$ref = \*{"${call}::$ref"} if ref($ref) ne 'GLOB';
			print STDERR "close:$ref\n" if $args{debug};
			if ($handle{$ref}) {
				print STDERR "unlock:$ref\n" if $args{debug};
				FlockWrapper::unlock();
				delete($handle{$ref});
			}
			return close($ref);
		};
	}
}}
END { unlock() if $args{clean}; }



sub lock_mkdir
{
	if (-e $args{fname}) {
		my $mtime = (stat($args{fname}))[9];
		unlock() if $mtime < time() - $args{timeout};
	}

	my $try = $args{try};
	while (!mkdir($args{fname}, 0755)) {
		return 0 if --$try <= 0;
		sleep(1);
	}
	return 1;
}



sub lock_symlink
{
	if (-e $args{fname}) {
		my $mtime = (stat($args{fname}))[9];
		unlock() if $mtime < time() - $args{timeout};
	}

	my $try = $args{try};
	while (!symlink(".", $args{fname})) {
		return 0 if --$try <= 0;
		sleep(1);
	}
	return 1;
}



sub unlock
{
	if ($args{flock} eq 'symlink') {
		unlink($args{fname});
		$args{unlocked} = 1;
	} elsif ($args{flock} eq 'mkdir') {
		rmdir($args{fname});
		$args{unlocked} = 1;
	}
}



1;
