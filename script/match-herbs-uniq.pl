#!usr/bin/perl -w
use strict;

unless(@ARGV==3)
{
    die "perl $0 <uniq_list> <database_title> <OUT>\n";
}

open IN1, "$ARGV[0]" or die;
open IN2, "$ARGV[1]" or die;
open OUT, ">$ARGV[2]" or die;

my (@tmp1,@tmp2,@k1,@k2,@k3,@k4);
my ($i,$j);

while(<IN1>)
{
    chomp;
    @tmp1=split;
    push @k1,$tmp1[0];
}

while(<IN2>)
{
    chomp;
    @tmp2=split;
    push @k2,$tmp2[0];
    push @k3,$tmp2[1];
}

for($i=0;$i<@k1;$i++)
{
    for($j=0;$j<@k2;$j++)
    {
        if($k1[$i] eq $k3[$j])
        {
            print OUT "$k2[$j]\t$k1[$i]\n";
        }
    }
}
