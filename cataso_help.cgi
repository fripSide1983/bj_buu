#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';

sub header2 {
	print qq|Content-type: text/html; charset=shift_jis\n\n|;
	
print << "HTML";
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<link rel="stylesheet" href="$htmldir/css/cataso.css?$jstime" />
<title>HELP</title>
</head>
<body>
HTML
}

sub run {
	print qq|<ul>|;
	print qq|<li>�u/reset�v:���Z�b�g</li>|;
	print qq|<li>���[���F�����_��10�_�ɂȂ菟���錾������Ώ���</li>|;
	print qq|<li>�_���F<ul><li>�ƁF1��1�_</li><li>�X�F1��2�_</li><li>�����i��M�����ň�Ԓ�������������l�j�F2�_</li><li>�R�m���i�R�m�J�[�h����ԑ����g�����l�j�F2�_</li><li>���_�J�[�h�F1��1�_</li></ul></li>|;
	print qq|<li>�����͍�����<span class="sand">�y</span><span class="wool">�r</span><span class="iron">�S</span><span class="wheat">��</span><span class="tree">��</span></li>|;
	print qq|<li>�X��:<span class="sand">�y1</span><span class="tree">��1</span></li>|;
	print qq|<li>�ƁF<span class="sand">�y1</span><span class="wool">�r1</span><span class="wheat">��1</span><span class="tree">��1</span></li>|;
	print qq|<li>�X�F<span class="iron">�S3</span><span class="wheat">��2</span></li>|;
	print qq|<li>�J�[�h�F<span class="wool">�r1</span><span class="iron">�S1</span><span class="wheat">��1</span></li>|;
	print qq|</ul>|;
}

sub footer2 {
	print qq|</body></html>|;
}

&header2;
&run;
&footer2;
exit;
