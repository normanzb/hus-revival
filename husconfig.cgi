#!/usr/bin/perl
if ($ENV{'REQUEST_METHOD'} eq "POST") {
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
}
else {
$buffer = $ENV{'QUERY_STRING'};
}
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
($name, $value) = split(/=/, $pair);
$value =~ tr/+/ /;
$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$value =~ s/<!--(.|\n)*-->//g;
$value =~ s/\|/ /g;
$value =~ s/\0//g;
$FORM{$name} = $value;
push (@DELETE, $value) if ($name eq "DEL");
}
$dir=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
$dir=~ s/\\/\//g;
if ($dir eq ""){$dir=".";}
$version="SP1";
print "Content-type: text/html;charset=gb2312\n\n";
#
if ($FORM{"action"} eq ""){
print <<EOF;
<html>
	<head><title>HUS Reviv\@l $version 设置程序</title></head>
<body bgcolor="#AAAAAA">设置完成后，请删除husconfig.cgi，以避免被他人恶意利用。
	<form action="husconfig.cgi" method="post">
网站域名(Domain)：<input type="text" value="" name="domain" />例如：supermanc.51.net<br />
网站路径(Path)：<input type="text" value="" name="path" />例如：/norman/<br />
	<input type="hidden" name="action" value="yes" />
<input type="submit" style="background-color:#AAA;border-top:1px solid #EEE;border-left:1px solid #EEE;border-right:1px solid #999;border-bottom:1px solid #999;font:12px;padding:4px;color:#FFF;margin:3px;font-weight:bold;" value="确定" />
	</form>
</body>
</html>
EOF
}
else{
#################################BEGIN
open(TMP,"$dir/setup.pl")||print "Setup.pl不能打开！";
@TMP=<TMP>;
close(TMP);
foreach $TMPs(@TMP){
$TMPs =~ s/\$ver=\"2\.0.?\"/\$ver="$version"/ig;
	if ($TMPs =~ /\$config_charset/){eval($TMPs);}
}
#config.cgi
open(TMP,"$dir/config.cgi");
@TMP=<TMP>;
close(TMP);
unlink("$dir/config.cgi");
open(TMP2,">>$dir/config.cgi");
foreach $TMPs(@TMP){
$TMPs =~ s/\$domain=""/\$domain="$FORM{"domain"}"/ig;
$TMPs =~ s/\$path=""/\$path="$FORM{"path"}"/ig;
if ($config_charset eq "1"){
$TMPs =~ s/\$pcharset="gb2312"/\$pcharset="utf-8"/ig;
}
print TMP2"$TMPs";
}
close(TMP2);
#################################END
print <<EOF;
<html>
<body>
设置完毕<br />
</body>
</html>
EOF
}