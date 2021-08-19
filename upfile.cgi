#!/usr/bin/perl

$dir=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
$dir=~ s/\\/\//g;
if ($dir eq ""){$dir=".";}

require "$dir/setup.pl";
require "$dir/config.cgi";
require "$dir/b_lib.cgi";


&r_cookies;
&chk_full;

$panel_name="数据上载";
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}

use CGI;
    my $req = new CGI; 
    my $file = $req->param("upfile"); 
	my $editorup = $req->param("editorup"); 
            my $file_name = $file;
        $file_name =~ s/^.*(\\|\/)//;
        $extname = lc(substr($file_name,length($file_name) - 4,4));
if ($file eq ""){$panel_name="发生错误";&B_ERROR("数据未选择!");}
unless (-e "$dir/uploaddata/count.cgi"){
open(COUNT,">$dir/uploaddata/count.cgi");
print COUNT"0";
close(COUNT);
$count=0;
}else{
open(COUNT,"$dir/uploaddata/count.cgi");
$count=<COUNT>;
close(COUNT);
$count++;

open(COUNT,">$dir/uploaddata/count.cgi");
print COUNT"$count";
close(COUNT);
}
&sys_time;
$year_now=$gmt_year + 1900;
open (OUTFILE, ">$dir/uploaddata/$gmt_day\_$monthname[$gmt_mon]\_$year_now\_$count$extname");
            binmode(OUTFILE); 
            	            while (my $bytesread = read($file, my $buffer, 1024)) { 
                print OUTFILE $buffer;
                                			}
close (OUTFILE);
unlink("$dir/CGItemp*");
if ($extname eq ".bmp" or $extname eq ".jpg" or $extname eq ".gif" or $extname eq ".png"){
$ubbcode="\[img\]http://$domain$path\luploaddata/$gmt_day\_$monthname[$gmt_mon]\_$year_now\_$count$extname\[/img\]";
}
else{
$ubbcode="\[url=http://$domain$path\luploaddata/$gmt_day\_$monthname[$gmt_mon]\_$year_now\_$count$extname\]点击下载\[/url\]";
}

&phtml;
if ($extname =~ /\.bmp|\.jpg|\.gif|\.ico|\.png/){
$pasteHTML="<img src=\"http://$domain$path\luploaddata/$gmt_day\_$monthname[$gmt_mon]\_$year_now\_$count$extname\" border=\"0\" />";
}
else{
$pasteHTML="<a href=\"http://$domain$path\luploaddata/$gmt_day\_$monthname[$gmt_mon]\_$year_now\_$count$extname\">$file_name</a>";
}
print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="gb2312">
<style>
body{
font:9pt tahoma,宋体;
}
</style>
<body  bgcolor="#D4D0C8" leftmargin="0" topmargin="0" style="word-break:break-all;word-warp:break-word;">
$file_name已经上传到<br />
http://$domain$path\luploaddata/$gmt_day\_$monthname[$gmt_mon]\_$year_now\_$count$extname <br />
<a href="#" onclick="parent.writeHTML();">继续上载</a>
<script>
parent.Rvalue.focus();
parent.Rvalue.document.selection.createRange().pasteHTML('$pasteHTML');
</script>
</body>
</html>
EOF
	
exit;