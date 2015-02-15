#! /usr/bin/perl

open FP, $ARGV[0] or die;
while (<FP>) {
	chomp;
	split /\t/;
	$tb{$_[0]}=1;
}
close FP;

$id=0;
if ($#ARGV == 2) {
	$id=$ARGV[2]-1;
	print STDERR "id=$id\n";
}

for ($i=1; $i<@ARGV; ++$i) { 
	open FP, $ARGV[$i] or die;
	while (<FP>) {
		chomp;
		split /\t/;
		if ( ! defined $tb{$_[$id]} )  {
			print "$_\n";
		}
	}
	close FP;
}
