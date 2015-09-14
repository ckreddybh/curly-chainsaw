#!/usr/bin/perl
# csv_from_table.pl
#testing pass word less push
use strict;
my $html_file = shift;
my $csv_file  = shift;
open (F_CSV, ">", $csv_file)    or  die "Failed to write to file $csv_file : $!";
open (F_HTML, "<", $html_file)  or  die "Failed to read file $html_file : $!";
while (<F_HTML>) {
# read html file line by line
    while (m#<TD>\s*(\d+)\s*</TD>\s*(</TR>)*?#gi) {
    # keep searching for numbers within TD tags, with an optional /TR tag at the end
        if (! $2) {
        # this TD is not the last TD in the TR
            print F_CSV "$1,";
              # so write comma after this number
        }
        else {
        # this is the last TD in the TR
            print F_CSV "$1\n";
              # so write newline after this number
        }
    }
}
close (F_HTML);
close (F_CSV);
