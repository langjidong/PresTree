#!/usr/bin/perl 
use strict;
use warnings;
my $usage=<<USAGE;
usage : perl $0 <infile1> <infile2> 
USAGE
die $usage if @ARGV<2;
open IN1,$ARGV[0] || die $!;
open IN2,$ARGV[1] || die $!;
$ARGV[2] = "$ARGV[0].xls";
$ARGV[3] = $ARGV[0].".special.xls";
$ARGV[4] = $ARGV[1].".special.xls";
open OUT1,">$ARGV[2]" || die $!;
open OUT2,">$ARGV[3]" || die $!;
open OUT3,">$ARGV[4]" || die $!;
my (@input1,@input2);
while(<IN1>){
	chomp;
	my $id1 = (split('\t',$_))[0];
	push @input1,$id1;
}
while(<IN2>){
	chomp;
	my $id2 = (split('\t',$_))[0];
	push @input2,$id2;
}
my %id;
foreach(@input2){
	$id{$_} = 1;
}
my @share = grep($id{$_},@input1);
my @diff1 = grep(!$id{$_},@input1);
print OUT1 join("\n",@share),"\n";
print OUT2 join("\n",@diff1),"\n";

%id = ();
foreach(@input1){
	$id{$_} = 1;
}
my @diff2 = grep(!$id{$_},@input2);
print OUT3 join("\n",@diff2),"\n";

close IN1;
close IN2;
close OUT1;
close OUT2;
close OUT3;
