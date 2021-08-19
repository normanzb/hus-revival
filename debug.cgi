#!/usr/bin/perl

$dir=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
$dir=~ s/\\/\//g;
if ($dir eq ""){$dir=".";}

require "$dir/setup.pl";
require "$dir/config.cgi";
require "$dir/b_lib.cgi";
print "Pragma: no-cache\n";
print "Cache-Control: no-cache\n";
print "Content-type: text/html;charset=$pcharset\n\n";
&sys_time;
&r_cookies;
print <<EOF;
过期时间 $expire_date <br />
COOKIES $contents_cookies
EOF
