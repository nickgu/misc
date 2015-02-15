#!/usr/bin/perl -w
use strict;

my $size = ((@ARGV && $ARGV[0] =~ /^\d+$/) ? shift : 10);
my $lines = 0;
my @output;
srand(time ^ $$);

print STDERR "RANDOM_NUM=$size\n";

while (<STDIN>) {
	++$lines;
	if ($lines <= $size) {
		push(@output, $_);
	}
	elsif (rand($lines) < $size) {
		$output[int(rand($size))] = $_;
	}
}
print @output;
