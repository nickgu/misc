#! /usr/bin/perl 
# 	gusimiu@baidu.com
#
#  将一份大xml拆分成多个小xml并且生成sitemap.
#  如果每个sitemap的key也超过限制，则会生成多个sitemap	
# Usage:
# 	./split.pl <BIG_XML>
#
# NOTICE:
# 	程序最终输出的是utf8格式xml，且最后一步是调用多个进程在后台转换。所以可能
# 	存在程序结束但转换还没完成的情况。需要等待下

use Encode;

# === 设置参数 ===
#	sitemap中，对应目录的http地址 
my $url_prefix = "http://bb-rank-testc009.vm.baidu.com:8080/right-baike";

#  sitemap输出前缀, 生成的sitemap是$prefix[0-9].xml这么生成下去
my $sitemap_prefix = "right-baike-sitemap_"; 

# 输出的gb目录。默认输入的BIG_XML是gb18030格式的，没测试过输入utf8情况下是否可行
my $dir="right-baike_gb";

# 输出的utf8目录。
my $dir2="right-baike";

# 单个xml的key限制，平台限制是10M，所以注意控制在这个量级内
my $single_xml_key_limit = 5000;

# 单个sitemap内所有key的限制, 目前平台的限制是100000.
my $single_sitemap_key_limit = 90000;

# === 设置结束 ===

$sid = 0;
$kid = 0;
open OFP, ">$sitemap_prefix$sid.xml" or die;
print OFP "<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n";

$fid=0;
`rm -rf $dir`;
`mkdir $dir`;
while (<>) {
	next if /<\?*xml/;
	next if /<\/*DOCUMENT>/;

	$output .= $_;

	if (/<\/item>/) {
		$it++;	
		$kid++;
		&over if $it>$single_xml_key_limit;
	} 
}
&over;

sub over {
	print OFP 
"	<sitemap>
		<loc>$url_prefix/$fid.xml</loc>
		<lastmod>2012-12-13</lastmod>
	</sitemap>\n";	
	if ( $kid>=$single_sitemap_key_limit ) {
		$kid = 0;
		$sid ++;
		print OFP "</sitemapindex>\n";
		close OFP;
		open OFP, ">$sitemap_prefix$sid.xml" or die;
		print OFP "<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n";
	}

	open FP, ">$dir/$fid.xml" or die; 
	print FP "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n";
	print FP "<DOCUMENT>\n";
	print FP $output;
	print FP "</DOCUMENT>\n";
	close FP;

	$output = "";
	$it = 0;
	$fid++;
}

print OFP "</sitemapindex>\n";
close OFP;

`rm -rf $dir2; mkdir $dir2`;
for $fn (split /\n/, `ls $dir`) {
	print $fn."\n";
	`./trans.pl < $dir/$fn > $dir2/$fn &`;
}


