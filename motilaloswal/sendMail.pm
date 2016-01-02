use Net::SMTP;
use MIME::Lite;
package sendMail; 


sub sendMimeMail 
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

sub sendSmptMail {
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

1;

__END__
