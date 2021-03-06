#! /usr/bin/perl 
# 进行分段统计
# 输入 stat.pl 起始值 终点值 每段大小 字段位置

my ($start, $end, $each_len, $field) = @ARGV;

while (<STDIN>) {
	chomp;
	split /\t/;

	$data = $_[$field-1];
	$idx = int(($data - $start) / $each_len);

	$info{$idx} ++;
}

for ($i=0; $i<($end-$start)/$each_len; $i++) {
	$s = $start + $i*$each_len;
	$e = $start + ($i+1)*$each_len;
	$ifo = 0;
	$ifo = $info{$i} if exists $info{$i};
	print "[$s,$e)\t$ifo\n";
}
