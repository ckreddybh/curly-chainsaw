use Net::SMTP;
package sendMail; 
sub send_mail {
	$smtp = Net::SMTP->new($host);
	my $host = "localhost";
	my $from_name = "CK Reddy";
	my $to = shift;
	my $from= shift;
	my $subject = shift;
	my $message = shift;
	if ($smtp) {
		my $from_name = 'CK Reddy';
		$smtp->mail("$to");
		$smtp->to("$to");
		$smtp->data();
		$smtp->datasend("To: $to\n");
		$smtp->datasend("From: $from_name <$from>\n");
		$smtp->datasend("Subject: $subject\n");
		$smtp->datasend("$message");
		$smtp->datasend("\n");
		$smtp->dataend();
		$smtp->quit;


	}
}

1;

__END__
