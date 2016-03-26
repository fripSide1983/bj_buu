#!/usr/local/bin/perl --
package MahjongYaku;
use strict;
use warnings;
use MahjongPai;
use MahjongYakuResult;

sub new {
	my $clazz = shift;
	my $self = {
		Yaku => sub{},
		@_
	};
	return bless $self, $clazz;
}

sub yaku {
	my $self = shift;
	if (@_) {
		$self->{Yaku} = shift;
	}
	return $self->{Yaku};
}

sub getRules {
	my @rules = ();
	
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->tehai()->tenhoFlag()) {
				$ret->fan(13);
				$ret->yaku('�V�a');
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->tehai()->chihoFlag()) {
				$ret->fan(13);
				$ret->yaku('�n�a');
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				if ($tehai->countAnko() == 4) {
					if ($tehai->finishShape() == 1 && $tehai->tehai()->tsumoFlag()) {
						$ret->fan(13);
						$ret->yaku('�l�Í�');
					} elsif ($tehai->finishShape() == 4) {
						$ret->fan(26);
						$ret->yaku('�l�Í��P�R');
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my $sangen_count = 0;
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->pai1()->str() eq 'z5') {
						$sangen_count++;
					}
					if ($mentsu->pai1()->str() eq 'z6') {
						$sangen_count++;
					}
					if ($mentsu->pai1()->str() eq 'z7') {
						$sangen_count++;
					}
				}
				if ($sangen_count == 3) {
					$ret->fan(13);
					$ret->yaku('��O��');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new(Fan => 13, Yaku => '����F');
			my @hist = $tehai->tehai()->toHistogramAll();
			for my $i (0..26) {
				if ($hist[$i] > 0) {
					$ret->fan(0);
					$ret->yaku('');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my $kaze_count = 0;
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->pai1()->str() eq 'z1') {
						$kaze_count++;
					}
					if ($mentsu->pai1()->str() eq 'z2') {
						$kaze_count++;
					}
					if ($mentsu->pai1()->str() eq 'z3') {
						$kaze_count++;
					}
					if ($mentsu->pai1()->str() eq 'z4') {
						$kaze_count++;
					}
				}
				if ($kaze_count == 3 && ($tehai->janto()->str() eq 'z1' || $tehai->janto()->str() eq 'z2' || $tehai->janto()->str() eq 'z3' || $tehai->janto()->str() eq 'z4')) {
					$ret->fan(13);
					$ret->yaku('���l��');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my $kaze_count = 0;
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->pai1()->str() eq 'z1') {
						$kaze_count++;
					}
					if ($mentsu->pai1()->str() eq 'z2') {
						$kaze_count++;
					}
					if ($mentsu->pai1()->str() eq 'z3') {
						$kaze_count++;
					}
					if ($mentsu->pai1()->str() eq 'z4') {
						$kaze_count++;
					}
				}
				if ($kaze_count == 4) {
					$ret->fan(26);
					$ret->yaku('��l��');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new(Fan => 13, Yaku => '�Έ�F');
			my @hist = $tehai->tehai()->toHistogramAll();
			for my $i (0..$#hist) {
				if ($hist[$i] > 0) {
					if (!($i == 10 || $i == 11 || $i == 12 || $i == 14 || $i == 16 || $i == 32)) {
						$ret->fan(0);
						$ret->yaku('');
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my $only_iku = 1;
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isShuntsu()) {
						$only_iku = 0;
					}
					if (!$mentsu->isIku()) {
						$only_iku = 0;
					}
				}
				if (!$tehai->janto()->isIku()) {
					$only_iku = 0;
				}
				if ($only_iku) {
					$ret->fan(13);
					$ret->yaku('���V��');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				if ($tehai->countKan() == 4) {
					$ret->fan(13);
					$ret->yaku('�l�Ȏq');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->isMenzen()) {
				my @hist = $tehai->tehai()->toHistogramAll();
				for my $i (0..2) {
					if (
						$hist[$i * 9] >= 3 &&
						$hist[$i * 9 + 1] >= 1 &&
						$hist[$i * 9 + 2] >= 1 &&
						$hist[$i * 9 + 3] >= 1 &&
						$hist[$i * 9 + 4] >= 1 &&
						$hist[$i * 9 + 5] >= 1 &&
						$hist[$i * 9 + 6] >= 1 &&
						$hist[$i * 9 + 7] >= 1 &&
						$hist[$i * 9 + 8] >= 3
					) {
						$ret->fan(13);
						$ret->yaku('��@��');
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			my @hist = $tehai->tehai()->toHistogramAll();
			for my $i (0..2) {
				my $su_count = 0;
				for my $j (0..8) {
					$su_count += $hist[$i * 9 + $j];
				}
				if ($su_count >= 14) {
					if ($tehai->isMenzen()) {
						$ret->fan(6);
					} else {
						$ret->fan(5);
					}
					$ret->yaku('����F');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			my @hist = $tehai->tehai()->toHistogramAll();
			my $tsu_count = 0;
			for my $i (27..33) {
				$tsu_count += $hist[$i];
			}
			for my $i (0..2) {
				my $su_count = 0;
				for my $j (0..8) {
					$su_count += $hist[$i * 9 + $j];
				}
				if ($tsu_count > 0 && $su_count + $tsu_count >= 14) {
					if ($tehai->isMenzen()) {
						$ret->fan(3);
					} else {
						$ret->fan(2);
					}
					$ret->yaku('����F');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my $only_iku = 1;
				my $has_shuntsu = 0;
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isShuntsu()) {
						$has_shuntsu = 1;
					}
					if (!$mentsu->isIku()) {
						$only_iku = 0;
					}
				}
				if (!$tehai->janto()->isIku()) {
					$only_iku = 0;
				}
				if ($only_iku && $has_shuntsu) {
					if ($tehai->isMenzen()) {
						$ret->fan(3);
					} else {
						$ret->fan(2);
					}
					$ret->yaku('���`����');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->tehai()->isRyanpeikou()) {
				$ret->fan(3);
				$ret->yaku('��u��');
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my @min_shuntsu_hist = ();
				for my $i (0..33) {
					push @min_shuntsu_hist, 0;
				}
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isShuntsu()) {
						$min_shuntsu_hist[MahjongPai::strToNum($mentsu->getMinPaiStr())]++;
					}
				}
				for my $i (0..8) {
					if ($min_shuntsu_hist[$i] > 0 && $min_shuntsu_hist[$i + 9] > 0 && $min_shuntsu_hist[$i + 18] > 0) {
						if ($tehai->isMenzen()) {
							$ret->fan(2);
						} else {
							$ret->fan(1);
						}
						$ret->yaku('�O�F����');
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my @min_shuntsu_hist = ();
				for my $i (0..33) {
					push @min_shuntsu_hist, 0;
				}
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isShuntsu()) {
						$min_shuntsu_hist[MahjongPai::strToNum($mentsu->getMinPaiStr())]++;
					}
				}
				for my $i (0..2) {
					if ($min_shuntsu_hist[$i * 9] > 0 && $min_shuntsu_hist[$i * 9 + 3] > 0 && $min_shuntsu_hist[$i * 9 + 6] > 0) {
						if ($tehai->isMenzen()) {
							$ret->fan(2);
						} else {
							$ret->fan(1);
						}
						$ret->yaku('��C�ʊ�');
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my $only_yaochu = 1;
				my $has_shuntsu = 0;
				my $has_tsu = 0;
				for my $mentsu (@{$tehai->mentsu()}) {
					if (!$mentsu->isYaochu()) {
						$only_yaochu = 0;
					}
					if ($mentsu->isTsu()) {
						$has_tsu = 1;
					}
					if ($mentsu->isShuntsu()) {
						$has_shuntsu = 1;
					}
				}
				if (!$tehai->janto()->isYaochu()) {
					$only_yaochu = 0;
				}
				if ($tehai->janto()->isTsu()) {
					$has_tsu = 1;
				}
				if ($only_yaochu && $has_shuntsu && $has_tsu) {
					if ($tehai->isMenzen()) {
						$ret->fan(2);
					} else {
						$ret->fan(1);
					}
					$ret->yaku('�`�����^');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				if ($tehai->countKotsu() == 4 && ($tehai->countAnko() != 4 || $tehai->finishShape() == 1)) {
					$ret->fan(2);
					$ret->yaku('�΁X�a');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				if ($tehai->countAnko() == 3) {
					if ($tehai->finishShape() == 1) {
						if ($tehai->tehai()->tsumoFlag()) {
							$ret->fan(2);
							$ret->yaku('�O�Í�');
						}
					} else {
						$ret->fan(2);
						$ret->yaku('�O�Í�');
					}
				} elsif ($tehai->countAnko() == 4 && $tehai->finishShape() == 1) {
					$ret->fan(2);
					$ret->yaku('�O�Í�');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new(Fan => 2, Yaku => '���V��');
			my @hist = $tehai->tehai()->toHistogramAll();
			for my $i (0..33) {
				if ($hist[$i] > 0) {
					if ($i > 0 && $i < 8) {
						$ret->fan(0);
						$ret->yaku('');
					}
					if ($i > 9 && $i < 17) {
						$ret->fan(0);
						$ret->yaku('');
					}
					if ($i > 18 && $i < 26) {
						$ret->fan(0);
						$ret->yaku('');
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my @min_kotsu_hist = ();
				for my $i (0..33) {
					push @min_kotsu_hist, 0;
				}
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isKotsu()) {
						$min_kotsu_hist[MahjongPai::strToNum($mentsu->getMinPaiStr())]++;
					}
				}
				for my $i (0..8) {
					if ($min_kotsu_hist[$i] > 0 && $min_kotsu_hist[$i + 9] > 0 && $min_kotsu_hist[$i + 18] > 0) {
						if ($tehai->isMenzen()) {
							$ret->fan(2);
						} else {
							$ret->fan(1);
						}
						$ret->yaku('�O�F����');
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				if ($tehai->countKan() == 3) {
					$ret->fan(2);
					$ret->yaku('�O�Ȏq');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my $sangen_count = 0;
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->pai1()->str() eq 'z5') {
						$sangen_count++;
					}
					if ($mentsu->pai1()->str() eq 'z6') {
						$sangen_count++;
					}
					if ($mentsu->pai1()->str() eq 'z7') {
						$sangen_count++;
					}
				}
				my $janto_str = $tehai->janto()->str();
				if ($sangen_count == 2 && ($janto_str eq 'z5' || $janto_str eq 'z6' || $janto_str eq 'z7')) {
					$ret->fan(2);
					$ret->yaku('���O��');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->tehai()->doubleReachFlag()) {
				$ret->fan(2);
				$ret->yaku('�_�u������');
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->tehai()->reachFlag() && !$tehai->tehai()->doubleReachFlag()) {
				$ret->fan(1);
				$ret->yaku('����');
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->tehai()->ippatsuFlag()) {
				$ret->fan(1);
				$ret->yaku('�ꔭ');
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->isMenzen() && $tehai->tehai()->tsumoFlag()) {
				$ret->fan(1);
				$ret->yaku('��O�����̘a');
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new(Fan => 1, Yaku => '�^�����I');
			my @hist = $tehai->tehai()->toHistogramAll();
			for my $i (0..33) {
				if ($hist[$i] > 0) {
					if ($i == 0 || $i == 8) {
						$ret->fan(0);
						$ret->yaku('');
					}
					if ($i == 9 || $i == 17) {
						$ret->fan(0);
						$ret->yaku('');
					}
					if ($i == 18 || $i == 26) {
						$ret->fan(0);
						$ret->yaku('');
					}
					if ($i >= 27) {
						$ret->fan(0);
						$ret->yaku('');
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new(Fan => 1, Yaku => '���a');
			if (!$tehai->is4Mentsu()) {
				$ret->fan(0);
				$ret->yaku('');
			} else {
				for my $mentsu (@{$tehai->mentsu()}) {
					if (!$mentsu->isShuntsu()) {
						$ret->fan(0);
						$ret->yaku('');
					}
				}
				my $janto_type = $tehai->janto()->getType();
				my $janto_num = $tehai->janto()->getNum();
				my $janto_str = $tehai->janto()->str();
				if ($janto_type eq 'z') {
					if ($janto_num >= 5) {
						$ret->fan(0);
						$ret->yaku('');
					} else {
						if ($janto_str eq $ba || $janto_str eq $kaze) {
							$ret->fan(0);
							$ret->yaku('');
						}
					}
				}
				if ($tehai->finishShape() != 0) {
					$ret->fan(0);
					$ret->yaku('');
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				my @min_shuntsu_hist = ();
				for my $i (0..33) {
					push @min_shuntsu_hist, 0;
				}
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isShuntsu()) {
						$min_shuntsu_hist[MahjongPai::strToNum($mentsu->getMinPaiStr())]++;
					}
				}
				for my $i (0..26) {
					if ($min_shuntsu_hist[$i] >= 2) {
						if ($tehai->isMenzen() && !$tehai->tehai()->isRyanpeikou()) {
							$ret->fan(1);
							$ret->yaku('��u��');
						}
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isKotsu()) {
						if ($mentsu->pai1()->str() eq $ba) {
							$ret->fan(1);
							$ret->yaku('�ꕗ');
						}
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isKotsu()) {
						if ($mentsu->pai1()->str() eq $kaze) {
							$ret->fan(1);
							$ret->yaku('����');
						}
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isKotsu()) {
						if ($mentsu->pai1()->str() eq 'z5') {
							$ret->fan(1);
							$ret->yaku('��');
						}
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isKotsu()) {
						if ($mentsu->pai1()->str() eq 'z6') {
							$ret->fan(1);
							$ret->yaku('�');
						}
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->is4Mentsu()) {
				for my $mentsu (@{$tehai->mentsu()}) {
					if ($mentsu->isKotsu()) {
						if ($mentsu->pai1()->str() eq 'z7') {
							$ret->fan(1);
							$ret->yaku('��');
						}
					}
				}
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->tehai()->rinshanFlag() && $tehai->tehai()->tsumoFlag()) {
				$ret->fan(1);
				$ret->yaku('���J��');
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->tehai()->chankanFlag()) {
				$ret->fan(1);
				$ret->yaku('����');
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->tehai()->haiteiFlag() && $tehai->tehai()->tsumoFlag()) {
				$ret->fan(1);
				$ret->yaku('�C��̌�');
			}
			return $ret;
		}
	);
	push @rules, MahjongYaku->new(
		Yaku => sub {
			my $tehai = shift;
			my $ba = shift;
			my $kaze = shift;
			
			my $ret = MahjongYakuResult->new();
			if ($tehai->tehai()->haiteiFlag() && !$tehai->tehai()->tsumoFlag()) {
				$ret->fan(1);
				$ret->yaku('�͒ꝝ��');
			}
			return $ret;
		}
	);
	return @rules;
}

1;