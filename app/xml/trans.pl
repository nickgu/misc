#! /usr/bin/perl 

use Encode;

while (<STDIN>) {
	print encode("utf-8", decode("gbk", $_));
}
