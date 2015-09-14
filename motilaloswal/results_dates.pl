#!/usr/bin/perl
use POSIX qw(strftime);
use lib "/home/ckreddy/motilaloswal";
use Date::Simple qw(date);
use Net::SMTP;
use LWP::Simple;
use MIME::Lite;
use strict;
my %mon2num = qw(
		jan 01  feb 02  mar 03  apr 04  may 05  jun 06
		jul 07  aug 08  sep 09  oct 10 nov 11 dec 12
		);

my $message='';
if(scalar(@ARGV)<1)
{
	die "usage :: $0 <filename with urls>\n";
}
my $today_date = strftime "%Y-%m-%d", localtime;
my $currentdate = date($today_date);
open my $fh, "<$ARGV[0]";
if(!$fh)
{
	die "unable to open file $ARGV[0]\n";
}
while(<$fh>)
{
	my $year = strftime "%Y", localtime;
	my $url =$_; 
	$url =~ s/\/$/\/$year/g;
	$url =~ s/\n//g;
	my $company_name = '';
	if($url =~ m/http\:\/\/www\.motilaloswal\.com\/Broking\/Markets\/Corporate-Actions\/Result-Calendar\/Advance-Search\/(.*?)\//)
	{
		$company_name=$1;
		$company_name =~ s/-/ /g;
	}
	my $finaldate='';
	my @resultdatearray;
	my $resultdate;
	eval{
		if(system("curl -sS $url > /home/ckreddy/motilaloswal/usrldata.html") !=0)
		{
			die "curl not sucess";
		}

		if(system("grep 'Results' /home/ckreddy/motilaloswal/usrldata.html | grep 'Result Date' | grep -oh \"<table cellpadding='0' cellspacing='0' border='0' width='100%'><tr style='height:25px;'><td  valign='middle'  class='GridHeadL RBord' style='width:60%;'>Results.*</table>\" > /home/ckreddy/motilaloswal/table.html") !=0 )
		{
			die "grep not sucess";
		}

		open(FILE, "</home/ckreddy/motilaloswal/table.html") || die "File not found";
		my @lines = <FILE>;
		close(FILE);

		my @newlines;
		foreach(@lines) 
		{
			$_ =~ s/\<\/table\>/\<\/table\>\n/g;
			push(@newlines,$_);
		}

		open(FILE, ">/home/ckreddy/motilaloswal/table2.html") || die "File not found";
		print FILE @newlines;
		close(FILE);

		if(system("grep -oh \"<table cellpadding='0' cellspacing='0' border='0' width='100%'><tr style='height:25px;'><td  valign='middle'  class='GridHeadL RBord' style='width:60%;'>Results.*</table>\" /home/ckreddy/motilaloswal/table2.html > /home/ckreddy/motilaloswal/table.html") !=0)
		{
			die "not sucess grep 2.";
		}

		open(FILE, "</home/ckreddy/motilaloswal/table.html") || die "File not found ";
		@lines = <FILE>;
		close(FILE);

		foreach(@lines) 
		{
			$_ =~ s/<table.*?>/<table>/g;
			$_ =~ s/<td.*?>/<td>/g;
			$_ =~ s/<tr.*?>/<tr>/g;
			$_ =~ s/<a.*?>//g;
			$_ =~ s/<\/a>//g;
			push(@newlines,$_);
		}

		open(FILE, ">/home/ckreddy/motilaloswal/table32.html") || die "File not found";
		print FILE @newlines;
		close(FILE);

		if(system("tail -1 /home/ckreddy/motilaloswal/table32.html>table.html ") !=0)
		{
			die "tail not sucess";
		}

		open(FILE, "</home/ckreddy/motilaloswal/table.html") || die "File not found ";
		@lines = <FILE>;
		close(FILE);
		my $WANT = 2;
		my $count = 0;
		foreach(@lines) 
		{
			while (m/(\w+\-\w+\-\w+)<\/td>/gi) 
			{
				$resultdate =  $1 if(++$count == $WANT);
			}
		}
		@resultdatearray = split("-",$resultdate);# date , month , year
		$finaldate = $resultdatearray[2];
	};
	if($@)
	{
		warn "unable to fetch records of $company_name\n$@\n";
		next;
	}
	$finaldate = $finaldate."-".$mon2num{ lc substr($resultdatearray[1], 0, 3) }."-".$resultdatearray[0];
	eval
	{
		my $result_date = date($finaldate);
		if(!$result_date)
		{
			next;
		}
		my $num_of_days_left = $result_date - $currentdate;
		print "$company_name : $result_date : num days left : $num_of_days_left\n";
		if( $num_of_days_left < 8 && $num_of_days_left >=0)
		{
			if ($num_of_days_left > 0){
				$message = "$message<tr><td>$company_name</td><td><b>$num_of_days_left days left</b></td><td>$resultdate</td></tr>";
			}else
			{
				$message = "$message<tr><td>$company_name</td><td><b>Today</b></td></tr>";
			}

		}
	};
	if($@)
	{
		warn "unable to process date calculation \n $@\n";
		next;
	}

}

my $reportdate = strftime "%d %b %Y", localtime;
print $reportdate; 
my $subject ="Daily Results Report [$reportdate]";
my $from ='ckreddybh@gmail.com';
if($message eq '')
{
	$message = "<body><b><i>No results with in a week</i></b></body>\n";
}else
{
	$message = "<table border=\"2\"><body><tr><th><b>Company Name</th><th>Days Left</th><th>Result Date</th></b></tr>$message</body></table>";
}
sendMail('chaitu949@gmail.com,ayyappa.konala@gmail.com,setmodevamsi1117@gmail.com',$subject,$message);
#sendMail('chaitu949@gmail.com',$subject,$message);

sub send_mail {
	my $host = "localhost";
	my $smtp = Net::SMTP->new($host);
	my $to = shift;
	my $subject = shift;
	my $message = shift;
	my $cc;
	my $reply_to;
	if ($smtp) {
		my $from_name = 'CK Reddy';
		$smtp->mail("$from");
		my @toArr = split (',', $to);
		foreach(@toArr){		
			$smtp->to("$_");
		}
		$smtp->data();
		$smtp->datasend("To: $to\n");
		$smtp->datasend("From: $from_name <$from>\n");
		$smtp->datasend("Reply-To: $reply_to\n") if ($reply_to);
		$smtp->datasend("Cc: $cc\n") if ($cc);
		$smtp->datasend("Content-Type: text/html;");
		$smtp->datasend("Subject: $subject\n");
		$smtp->datasend("$message");
		$smtp->datasend("\n");
		$smtp->dataend();
		$smtp->quit;


	}
}

sub sendMail 
{
	my $mailto = shift;
	my $subject = shift;
	my $html = shift;
		my $msg  = MIME::Lite->new(
				From     => 'CKReddy@gmail.com',
				To       => $mailto,
				Type     => 'text/html',
				Subject  => $subject,
				Data     => $html,
				);

		$msg->send or die "couldn't send message to '$mailto'\n";
}
