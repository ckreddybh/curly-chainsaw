#!/usr/bin/perl
use POSIX qw(strftime);
use lib "/home/ubuntu/curly-chainsaw/motilaloswal";
use Date::Simple qw(date);
use sendMail;
use strict;

$| = 1;

my $path = "/home/ubuntu/curly-chainsaw/motilaloswal";


if(scalar(@ARGV)<1)
{
	die "usage :: $0 <log path>\n";
}

my $lastline = `tail -1 $ARGV[0]`;



if($lastline eq "SCRIPT ENDED SUCCESSFULLY")
{
	open(FILE, "<$path/mail_subject_message");
	my @list = split(": ",<FILE>);
	my $subject = $list[1];
	@list = split(": ",<FILE>);
	my $message = $list[1];
	close FILE;

	sendMail::sendMimeMail('chaitu949@gmail.com,ayyappa.konala@gmail.com,setmodevamsi1117@gmail.com',$subject,$message);

}else{
	` perl /home/ubuntu/curly-chainsaw/motilaloswal/results_dates.pl /home/ubuntu/curly-chainsaw/motilaloswal/companies_to_process.txt > /home/ubuntu/curly-chainsaw/motilaloswal/results_log.log`;
}


