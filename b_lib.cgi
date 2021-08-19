#■ Blog数据版本
$blogdata_version="1";
#■ Blog数据目录
$blogdata="blogdata";

#■ BLOG上部分HTML
sub framet{
	&phtml;
print <<EOF;
<html>
<head>
<meta http-equiv="pragma" content="no-cache"> 
<meta http-equiv="Cache-Control" content="no-cache, must-revalidate"> 
<style>
\@import url('./editorfiles/style_b.css');
</style>
<title>$panel_name</title>
<script language="javascript" src="./jscript.js">
</script>
</head>
<body>
<div id="dialogtitle">
<strong><img class="Imgbtn" src="./editorfiles/dot.gif" align="absmiddle" /> $panel_name</strong> <font face="webdings">6</font>
</div>
<div class="dialog" style="height:400px;Padding-top:12px;">
EOF
}

#■ BLOG下部分HTML
sub frameb{
$copyright="<font size=1>Powered by <a href=\"http://pfgroup.yeah.net\">HUS Reviv\@l[$ver]</a></font><br /> $copyright";
print <<EOF;
</div>
<script language="javascript">
if (dialogArguments){Rvalue=dialogArguments;}
function returnEValue(arg_1,arg2){
$_[0];
}
</script>
</body>
</html>
EOF
}

#■ 写入新LOG
sub w_blog_log{
&r_blog_log;
if ($logid_from <= 0){
$maxlog++;
open(MAXLOG,">$dir/$blogdata/maxlog.cgi");
print MAXLOG"$maxlog";
close(MAXLOG);
}
else{
$i=1;
$maxlog=$logid_from;
$BLOG_LOGID{$i}=$maxlog;
&r_reply;
$content="$content<br><br>[script=$script_font_color]Edited by $usrid in $create_time [/script]";
$create_time=$CREATE_TIME{1};
$usrid=$AUTHORID{1};
}
open(LOG,">$dir/$blogdata/log_$maxlog.cgi");
print LOG"$blogdata_version|$usrid|$classid|$title|$content|$abouturl|$aboutimage|$imgw|$imgh|$create_time|\n";
$i=1;
while($Reply_Contentz{$i} ne ""){
		print LOG"$Reply_Name{$i}|$Reply_Contentz{$i}|\n";
		$i++;
}
close(LOG);
}

#■ 读入新LOG
sub r_blog_log{
open(MAXLOG,"$dir/$blogdata/maxlog.cgi");
$maxlog=<MAXLOG>;
close(MAXLOG);
if ($logid_from eq "" or $logid_from > $maxlog){$logid_cgi=$maxlog;$logid_from="-1";}
else{
$logid_cgi=$logid_from;
}
if ($viewtype eq ""){
$viewtype="next";
}
if ($viewtype eq "next"){
	$i=0;
	if ($i < $log_count and $logid_cgi > 0){$while_sw=1;}
}else{
	$i=$log_count+1;
	if ($i > 1 and $logid_cgi < $maxlog){$while_sw=1;}
}
$nodata=0;
while($while_sw){
if ($viewtype eq "next"){
$i++;
}else{
$i--;
}
$DB{$i}=$i;
open(LOG,"$dir/$blogdata/log_$logid_cgi.cgi");
@BLOG_LOGs=<LOG>;
$BLOG_LOG{$i}=$BLOG_LOGs[0];
close(LOG);
$BLOG_REPLYCOUNT{$i}=@BLOG_LOGs;
$BLOG_REPLYCOUNT{$i}--;
$BLOG_LOGID{$i}=$logid_cgi;
($DB_BLOGDATA_VERSION{$i},$AUTHORID{$i},$CLASSID{$i},$TITLE{$i},$CONTENT{$i},$ABOUTURL{$i},$ABOUTIMAGE{$i},$IMGW{$i},$IMGH{$i},$CREATE_TIME{$i},$blank)=split(/\|/,$BLOG_LOG{$i});
if ($action ne "viewclass" and $action ne "search" and ($TITLE{$i} eq "[no data]" or $TITLE{$i} eq "")){
if ($viewtype eq "next"){
$i--;
}else{
$i++;
}
}
	if ($action eq "viewclass"){
		&blog_action_viewclass;
	}
	if ($action eq "search"){
		&blog_action_search;
	}
	if ($action eq "viewdata"){
		&blog_action_viewdata;
	}
	if ($nodata == $logid_from or $nodata == $maxlog){
	$AUTHORID{$i}="";
	$CLASSID{$i}="";
	$TITLE{$i}="";
	$CONTENT{$i}="";
	$CREATE_TIME{$i}="";
	}
	if ($viewtype eq "next"){
	$logid_cgi--;
	if ($i < $log_count and $logid_cgi > 0){$while_sw=1;}else{$while_sw=0;}
	}else{
	$logid_cgi++;
	if ($i > 1 and $logid_cgi <= $maxlog){$while_sw=1;}else{$while_sw=0;}
	}
}
$i--;
if ($action eq "viewclass" and $CLASSID{$i} != $classid){
$AUTHORID{$i}="";
$CLASSID{$i}="";
$TITLE{$i}="";
$CONTENT{$i}="";
$CREATE_TIME{$i}="";
}
}
sub blog_action_viewclass{
if ($action eq "viewclass" and $classid ne "" and $CLASSID{$i} != $classid and $logid_cgi > 1){
	if ($viewtype eq "next"){
	$i--;
	}else{
	$i++;
	}
$nodata++;
}
if ($action eq "viewclass" and $CLASSID{$i} != $classid){
$AUTHORID{$i}="";
$CLASSID{$i}="";
$TITLE{$i}="";
$CONTENT{$i}="";
$CREATE_TIME{$i}="";
}
}
sub blog_action_search{
unless ($CONTENT{$i} =~ /$keyword/ or $logid_cgi <= 1){
if ($viewtype eq "next"){
$i--;
}else{
$i++;
}
$nodata++;
}
unless ($CONTENT{$i} =~ /$keyword/){
$AUTHORID{$i}="";
$CLASSID{$i}="";
$TITLE{$i}="";
$CONTENT{$i}="";
$CREATE_TIME{$i}="";
}
}
sub blog_action_viewdata{
$gmt_year=$view_year;
$gmt_mon=$view_mon;
$gmt_day=$view_day;
&sys_translate;
if ($view_day eq ""){
$create_time =~ s/日//isg;
}
unless ($CREATE_TIME{$i} =~ /$create_time/ or $logid_cgi <= 1){
if ($viewtype eq "next"){
$i--;
}else{
$i++;
}
$nodata++;
}
unless ($CREATE_TIME{$i} =~ /$create_time/){
$AUTHORID{$i}="";
$CLASSID{$i}="";
$TITLE{$i}="";
$CONTENT{$i}="";
$CREATE_TIME{$i}="";
}
}

#■ 读取类
sub r_blog_class{
unless (-e "$dir/$blogdata/class.cgi"){
open(CLASS,">$dir/$blogdata/class.cgi");
close(CLASS);
}
open(CLASS,"$dir/$blogdata/class.cgi");
$blog_class_firstline=<CLASS>;
close(CLASS);

if ($blog_class_firstline eq ""){
$CLASS_ATTRIB_NAME{'0'}="未分类";
$CLASS_ATTRIB_SCRIPTION{'0'}="无内容";
$blog_class_maxid="-1";
}
else{
open(CLASS,"$dir/$blogdata/class.cgi");
@blog_class_attrib=<CLASS>;
$blog_class_firstline=$blog_class_attrib[0];

($blog_class_maxid, $ignore, $ignore)=split(/\|/,$blog_class_firstline);

close(CLASS);
foreach $blog_class_attrib (@blog_class_attrib){
($db_classid ,$db_class_name ,$db_class_scription)=split(/\|/,$blog_class_attrib);
$CLASS_ATTRIB_NAME{$db_classid}=$db_class_name;
$CLASS_ATTRIB_SCRIPTION{$db_classid}=$db_class_scription;
	}
}
}

#■ 添加类
sub w_blog_class{
&r_blog_class;
$classid=1+$blog_class_maxid;
open(CLASS,">$dir/$blogdata/class.cgi");
print CLASS"$classid|$input_class_name|$input_class_scription|\n";
$i=$classid-1;

while ($i >= 0){+
print CLASS"$blog_class_attrib[$i]";
$i--;
}
close(CLASS);
}

#■ 删除类
sub c_blog_class{
$delclassid=$classid;
&r_blog_class;
open(CLASS,">$dir/$blogdata/class.cgi");
close(CLASS);
$blog_class_id=$blog_class_maxid + 1;
open(CLASS,">>$dir/$blogdata/class.cgi");
while (--$blog_class_maxid >= 0){
	$blog_class_id--;
if ($delclassid == $blog_class_id){
	$blog_class_id--;
	print CLASS"$blog_class_maxid|$CLASS_ATTRIB_NAME{$blog_class_id}|$CLASS_ATTRIB_SCRIPTION{$blog_class_id}|\n";

	}
else{
	print CLASS"$blog_class_maxid|$CLASS_ATTRIB_NAME{$blog_class_id}|$CLASS_ATTRIB_SCRIPTION{$blog_class_id}|\n";
	}
}
close(CLASS);
}

#■ 模版读取
sub DrawControlPanel{
&r_cookies;
$jscode=<<EOF;
<script language="javascript" src="./jscript.js">
</script>
EOF
$chk_result=&chk_full("background");
if ($usrid eq "" or $chk_result){
return <<EOF;
$jscode
<div id="LoginForm_div">
<form id="Lform" name="Lform" action="blog.cgi" method="post">
<div id="LoginForm_title"><img src="./b_img/control.gif" /></div>
用户：<input class="textbox" type="text" value="" name="usrid" /><br />
密码：<input class="textbox" type="password" value="" name="usrpwd" /><br />
<input class="button" type="button" value="登录" onclick="Messagebox('./blog.cgi?action=logout&usrid=' + document.Lform.usrid.value + '&usrpwd=' + document.Lform.usrpwd.value);" />
<input class="button" type="reset" value="注册" onclick="Newpage('./blog_manager.cgi?action=userform');" />
</form>
</div>
EOF
}
else{
if ($db_admin eq "6" or $db_admin eq "2"){
$adminbtns="<div class=\"Controlbtns\" onclick=\"window.open('./blog_manager.cgi?action=editor','Editor', 'width=480,height=500,left=300,top=50,resizable=0,status=no,help=no,scrollbar=no');\"><img src=\"./b_img/new.gif\" /></div>"
}
return <<EOF;
$jscode
<div id="LoginForm_div">
<div id="LoginForm_title"><img src="./b_img/control.gif" /></div>
$adminbtns
<div class="Controlbtns" onclick="Newpage('./blog_manager.cgi?action=coverform&usrid=$usrid');"><img src="./b_img/profile.gif" /></div> <div class="Controlbtns" onclick="Messagebox('./blog.cgi?action=logout');"><img src="./b_img/exit.gif" /></div>
<div class="clearline"></div>
</div>
EOF
}
}
sub r_blog_templete_h{
&setBlogStat;
&getBlogStat;
if ($templete_name eq ""){$templete_name="default";}
open(TEMPLETE,"$dir/$blogdata/tpl_$templete_name\_h.cgi");
$blog_templete_head=<TEMPLETE>;
close(TEMPLETE);
&pagehref;
&Calendar;
$blog_templete_head=~ s/<calendar>/$calendar/g;
$blog_templete_head=~ s/<pagehref>/$pagehref/g;
unless ($templete_name =~ /rss/){
$blog_templete_head=~ s/<\/head>/<script>qlog=0<\/script><\/head>/ig;
}else{
$blog_templete_head=~ s/<rss:creator>/$blog_creator/ig;
$blog_templete_head=~ s/<rss:right>/by $blog_creator/ig;
$blog_templete_head=~ s/<rss:name>/$blog_name/ig;
$blog_templete_head=~ s/<rss:mail>/$admin_connect/ig;
$blog_templete_head=~ s/<rss:link>/http:\/\/$domain$path/ig;
$blog_templete_head=~ s/<rss:date>/$blog_date/ig;
$blog_templete_head=~ s/<rss:charset>/$pcharset/ig;
}
$classline="";
&r_blog_class;
$i=0;
while($i <= $blog_class_maxid){
$classline="$classline<div class=\"blog_navbtns\" onclick=\"openclass('./blog.cgi?action=viewclass&classid=$i&t=$templete_name');\" alt=\"$CLASS_ATTRIB_SCRIPTION{$i}\">$CLASS_ATTRIB_NAME{$i}</div>";
$i++;
}
&r_replyindex;
$DrawControlPanel=&DrawControlPanel;
$blog_templete_head=~ s/<ControlPanel>/$DrawControlPanel/g;
$blog_templete_head=~ s/<classline>/$classline/g;
$blog_templete_head=~ s/<reply_index>/$reply_index/g;
$blog_templete_head=~ s/<blogstat>/日志总数:$maxlog<br \/>最高页访问:$totalpage<br \/>最高IP访问:$totalip<br \/>今日页访问:$daypage<br \/>今日IP访问:$dayip/g;

if ($templete_name =~ /rss/){
print "Content-type: text/xml;charset=$pcharset\n\n";
}else{
if ($config_charset < 3){
$pcharset="utf-8";}else{$pcharset="gb2312";}
&phtml;
}
$Convert_string=$blog_templete_head;
&Char_Convert;
$blog_templete_head=$Convert_string;
print "$blog_templete_head";
}
sub r_blog_templete_b{
if ($templete_name eq ""){$templete_name="default";}
open(TEMPLETE,"$dir/$blogdata/tpl_$templete_name\_b.cgi");
$blog_templete_body=<TEMPLETE>;
close(TEMPLETE);
&sys_transubb;
$blog_templete_body=~ s/<log_title>/$TITLE{$i}/g;
&r_blog_class;
$blog_templete_body=~ s/<class_name>/$CLASS_ATTRIB_NAME{$CLASSID{$i}}/g;
$blog_templete_body=~ s/<class_script>/$CLASS_ATTRIB_SCRIPTION{$CLASSID{$i}}/g;
$blog_templete_body=~ s/<content>/$CONTENT{$i}/g;
$blog_templete_body=~ s/<usrid>/$AUTHORID{$i}/g;
$blog_templete_body=~ s/<create_time>/$CREATE_TIME{$i}/g;
$blog_templete_body=~ s/<logid_cgi>/$BLOG_LOGID{$i}/g;
$blog_templete_body=~ s/<rss:link>/http:\/\/$domain$path\lblog.cgi?action=omode&amp;logid_from=$BLOG_LOGID{$i}/g;
if ($ABOUTURL{$i} ne ""){
$blog_templete_body=~ s/<abouturl>/相关网址：<a href="$ABOUTURL{$i}">$ABOUTURL{$i}<\/a>/g;}
if ($ABOUTIMAGE{$i} ne ""){
	if ($IMGW{$i} ne "" and $IMGH{$i} ne ""){
		$IMGW{$i}="width=$IMGW{$i}";
		$IMGH{$i}="width=$IMGH{$i}";
	}
	$blog_templete_body=~ s/<aboutimage>/相关图片：<img src="$ABOUTIMAGE{$i}" border=0 $IMGH{$i} $IMGW{$i}>/g;
	}
if ($TITLE{$i} ne "" and $CONTENT{$i} ne "" and $TITLE{$i} ne "[no data]"){
		$Convert_string=$blog_templete_body;
		&Char_Convert;
		$blog_templete_body=$Convert_string;
print "$blog_templete_body";
}
}
sub r_blog_templete_b_sp{
$blog_templete_body="<a href=\"#\" onclick=\"window.open('./blog.cgi?action=omode_sp&logid_from=$BLOG_LOGID{$i}','_blank','height=400, width=769, top=0, left=0, toolbar=no, menubar=no, scrollbars=yes, resizable=yes,location=no, status=no')\">$TITLE{$i}</a>[$CREATE_TIME{$i}]<br>";
	if ($TITLE{$i} ne "" and $CONTENT{$i} ne "" and $TITLE{$i} ne "[no data]"){
		$Convert_string=$blog_templete_body;
		&Char_Convert;
		$blog_templete_body=$Convert_string;
		print "$blog_templete_body";
	}
}
sub r_blog_templete_f{
if ($templete_name eq ""){$templete_name="default";}
open(TEMPLETE,"$dir/$blogdata/tpl_$templete_name\_f.cgi");
$blog_templete_foot=<TEMPLETE>;
close(TEMPLETE);
&pagehref;
@usagetime=times;
$blog_templete_foot=~ s/<pagehref>/$pagehref$pagejump/g;
$blog_templete_foot=~ s/<usagetime>/用户时间：$usagetime[0] 系统时间：$usagetime[1]/g;
		$Convert_string=$blog_templete_foot;
		&Char_Convert;
		$blog_templete_foot=$Convert_string;
print "$blog_templete_foot";
}

#■ 页面转换代码生成
sub pagehref{
if ($action eq "blog"){
	$script_file="blog_manager.cgi?action=blog&";
	}
	elsif ($action eq "search"){
	$script_file="blog.cgi?action=search";
	}
	elsif ($action eq "viewdata"){
	$script_file="blog.cgi?action=viewdata";
	}
	else{
	$script_file="blog.cgi?";
	}
if ($action eq "viewclass" and $classid ne ""){
$pagehref_add="&action=viewclass&classid=$classid&t=$templete_name";
}elsif ($action eq "search"){
$pagehref_add="&keyword=$keyword&t=$templete_name";
}elsif ($action eq "viewdata"){
$pagehref_add="&view_year=$gmt_year&view_mon=$gmt_mon&view_day=$view_day&t=$templete_name";
}
if ($logid_from eq "" or $logid_from >= $maxlog or $logid_from < 1){
	$logid_from=$maxlog;
	$logid_next=$BLOG_LOGID{5}-1;
	if ($logid_next < $log_count){$logid_next=$log_count;}
	$pagehref="<a href=\"./$script_file&logid_from=$logid_next$pagehref_add&viewtype=next&t=$templete_name\"><img src=\"./b_img/arrow_nex.gif\" border=\"0\" align=\"absmiddle\" /></a>";
}
else{
	if ($viewtype eq "next"){
	$logid_prev=$BLOG_LOGID{1}+1;
	$logid_next=$BLOG_LOGID{5}-1;
	if ($logid_next-5 < 1){$logid_prev=1;}
	}
	else {
	$logid_prev=$BLOG_LOGID{1}+1;
	$logid_next=$BLOG_LOGID{5}-1;
	if ($logid_prev+5 >$maxlog){$logid_prev=$maxlog-4;}
	}
	if ($logid_prev > $maxlog){$logid_prev=$maxlog;}
	if ($logid_next < $log_count){$logid_next=$log_count;}

$pagehref="<a href=\"./$script_file&logid_from=$logid_prev$pagehref_add&viewtype=prev&t=$templete_name\"><img src=\"./b_img/arrow_pre.gif\" border=\"0\" align=\"absmiddle\" /></a> <a href=\"./$script_file&logid_from=$logid_next$pagehref_add&viewtype=next&t=$templete_name\"><img src=\"./b_img/arrow_nex.gif\" border=\"0\" align=\"absmiddle\" /></a>";
}
$pagejump= <<EOF;
&nbsp;跳到第 <input id="pagejump" type="text" value="" name="pagejump" style="width:40px;height:16px;font:7pt tahoma;" style="background-color:#eeeeee;border:1px solid #000000;" /> 条记录<span onmouseover="this.style.cursor='hand';" onmouseout="this.style.cursor='default';" onclick="window.open('./blog.cgi?t=$templete_name&logid_from='+ document.all.pagejump.value,'_self')"><font face="webdings">5</font></span>
EOF

}

#■ 基本代码转换
sub sys_translate{
$realyear=$gmt_year+1900;
$realmon=$gmt_mon+1;
$dateset=~ s/YYYY/$realyear/g;
$dateset=~ s/MM/$realmon/g;
$dateset=~ s/DD/$gmt_day/g;
$create_time=$dateset;

if ($_[0] eq "UBB" or $_[0] eq ""){
$content =~ s/>/&gt;/g;
$content =~ s/</&lt;/g;
$content =~ s/ /&nbsp;/g;
$content =~ s/\r\n/<br>/g;
if ($urlautodetect eq "1"){
	$content =~ s/([^=|\]])(http|ftp|https)(\S+?)(\.aspx|\.asp|\.jsp|\.js|\.php|\.pl|\.cgi|\.html|\.htm|\.cn|\.uk|\.jp|\.tw|\.kr|\.com|\.net|\.org|\.edu|\.biz|\.name|\.info)/$1\[url\]$2$3$4\[\/url\]/isg;
	}
}
if ($_[0] eq "HTML"){
$content =~ s/<img\s([^o])/<img onload="chk_width(this)" $1/ig;
$content =~ s/\.\.\/b_img\/emotion\//\.\/b_img\/emotion\//g;
$content =~ s/\r\n//g;
}

}

#■ UBB代码转换
sub sys_transubb{
$CONTENT{$i} =~ s/\[img\](http|https|ftp)(\S+?)\[\/img\]/<img src="$1$2" border=0 onload="chk_width(this)" alt="点击新窗口打开" onclick="window.open('$1$2')" onmouseover="this.style.cursor='hand'">/isg;
$CONTENT{$i} =~ s/\[url=(http|https|ftp)(\S+?)\](.+?)\[\/url\]/<a href="$1$2" target=_blank>$3<\/a>/isg;
$CONTENT{$i} =~ s/\[url\](http|https|ftp)(\S+?)\[\/url\]/<a href="$1$2" target=_blank>$1$2<\/a>/isg;
$CONTENT{$i} =~ s/\[color=(\S+?)\](.+?)\[\/color\]/<font color="$1">$2<\/font>/isg;
$CONTENT{$i} =~ s/\[script=(\S+?)\](.+?)\[\/script\]/<font color="$1">$2<\/font>/isg;
$CONTENT{$i} =~ s/\[frame=(http|https|ftp)(\S+?)\]/<iframe width=100% src="$1$2" height=100% frameborder='0' style='border:1px dotted #999999;margin-top:4px;margin-bottom:4px'><\/iframe>/isg;
$CONTENT{$i} =~ s/\[b\](\S+?)\[\/b\]/<b>$1<\/b>/isg;
$CONTENT{$i} =~ s/\[em([0-9]|)([0-9])\]/<img src=".\/b_img\/emotion\/$1$2.gif" border=0>/isg;
$CONTENT{$i} =~ s/\[quote\]&lt;STRONG&gt;(.+?：)&lt;\/STRONG&gt;&lt;BR&gt;(.+?)\[\/quote\]/<div class="code">$1$2<\/div>/ig;
}

#■ 出错页面
sub B_ERROR{
&phtml;
print<<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="gb2312">
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" /> 
<meta http-equiv="Content-Language" content="gb2312" />
<meta name="Copyright" content="2004-2005 by norman shinn(许宏宇) http://pfgroup.yeah.net" /> 
<head>
	<title>$panel_name</title>
	<style>
	\@import url(./editorfiles/style_b.css);
	</style>
</head>
<body>
	<div class="messagebox">
	$_[0]
	</div>
	<script language="javascript">
	function CloseInTime(){
	window.close();
	}
	setTimeout('CloseInTime();',1500);
	</script>
</body>
</html>
EOF
exit;
}

#■ 日历显示
sub Calendar{
if ($action eq "viewdata" and $view_year ne "" and $view_mon ne ""){
&sys_sec4gmt($view_year,$view_mon,$view_day);
&sys_time;
}
else{
&sys_time;
&sys_sec4gmt($gmt_year,$gmt_mon,$gmt_day);
}

&sys_translate;
$prev_year=$gmt_year-1;
$next_year=$gmt_year+1;
$prev_mon=$gmt_mon-1;
if ($prev_mon <0){$prev_mon=0;}
$next_mon=$gmt_mon+1;
if ($next_mon >11){$next_mon=11;}
$calendar=<<EOF;
<TABLE cellSpacing="0" cellPadding="0" width="90%" background="" border="0" style="filter:alpha(opacity=$alpha_calendar,finishOpacity=100,style=1,startX=0,startY=0,finishX=0,finishY=0,add=0,direction=45,strength=10);">
  <TBODY>
  <TR>
    <TD align="center"><a href="./blog.cgi?action=viewdata&view_year=$prev_year&view_mon=$gmt_mon&t=$templete_name"><font face="webdings">3</font></a> $realyear 年<a href="./blog.cgi?action=viewdata&view_year=$next_year&view_mon=$gmt_mon&t=$templete_name"><font face="webdings">4</font></a></TD><TD align="center"><a href="./blog.cgi?action=viewdata&view_year=$gmt_year&view_mon=$prev_mon&t=$templete_name"><font face="webdings">3</font></a> $realmon 月<a href="./blog.cgi?action=viewdata&view_year=$gmt_year&view_mon=$next_mon&t=$templete_name"><font face="webdings">4</font></a></TD></TR>
  <TR>
    <TD colspan="2">
    <TABLE cellSpacing="2" cellPadding="0" width="180" background="" border="0" align="center">
  <TBODY>
  <TR>
    <TD bgcolor="#dddddd" width="25" align="center">Sun</TD>
    <TD bgcolor="#dddddd" width="25" align="center">Mon</TD>
    <TD bgcolor="#dddddd" width="25" align="center">Tue</TD>
    <TD bgcolor="#dddddd" width="25" align="center">Wed</TD>
    <TD bgcolor="#dddddd" width="25" align="center">Thu</TD>
    <TD bgcolor="#dddddd" width="25" align="center">Fri</TD>
    <TD bgcolor="#dddddd" width="25" align="center">Sat</TD></TR>
    <TR>
EOF

$temp_day=$gmt_day;
$temp_wday=$gmt_wday;
while ($temp_day >= 1){
if ($temp_wday > 0){$temp_wday--;}
	else{$temp_wday=6;}
$temp_day--;
}

$prevmonthday=$monthday["$realmon-1"]-$temp_wday-1;
$i=0;
while ($i <= $temp_wday){
	$calendar="$calendar<td bgcolor=#eeeeee><font color=#cccccc>$prevmonthday</font></td>";
	$prevmonthday++;
	$i++;
}

$i=1;
$j=$temp_wday;
while ($i <= $monthday[$realmon]){
	if ($i == $gmt_day){$calendad_bgcolor="#cccccc"}else{$calendad_bgcolor="#eeeeee"}
	if ($j < 6){$calendar="$calendar<td bgcolor=$calendad_bgcolor align=center><a href=\"./blog.cgi?action=viewdata&view_year=$gmt_year&view_mon=$gmt_mon&view_day=$i&t=$templete_name\"><font color=#000000>$i</font></a></td>";$i++;$j++;}
		else{	$calendar="$calendar</TR><TR>";$j=-1;}

}
$i=1;
while ($j < 7){
	if ($j < 6){$calendar="$calendar<td bgcolor=#eeeeee align=center><font color=#cccccc>$i</font></td>";$i++;$j++;}
		else{	$calendar="$calendar</TR>";$j++;}
		}
$calendar=<<EOF;
	$calendar
	</TR>
   	</TBODY></TABLE>
    </TD></TR></TBODY></TABLE>
EOF

}

#■ 添加文章评论
sub w_reply{
	if ($Rcounter eq ""){
	open (LOG,">>$dir/$blogdata/log_$logfile.cgi");
	print LOG"$readername|$Reply_Content|\n";
	close(LOG);
	&reply_makeindex;
	}
	else{
	$BLOG_LOGID{1}=$logfile;
	$i=1;
	&r_reply;
	open (LOG,">$dir/$blogdata/log_$logfile.cgi");
	print LOG"$replymess[0]";
	$i=1;
	while($Reply_Contentz{$i} ne ""){
		if ($i eq $Rcounter and $action eq "delreply"){
		print LOG"[no data]|[none]|\n";
		}else{
		print LOG"$Reply_Name{$i}|$Reply_Contentz{$i}|\n";
		}
		$i++;
	}
	close(LOG);
	}
}

#■ 读取文章评论
sub r_reply{
open (LOG,"$dir/$blogdata/log_$BLOG_LOGID{$i}.cgi");
@replymess=<LOG>;
close(LOG);
$i=0;
foreach $replymess(@replymess){
	($readername,$Reply_Content,$blank)=split(/\|/,$replymess);
	$Reply_Name{$i}=$readername;
	$Reply_Contentz{$i}=$Reply_Content;
	$i++;
	}
}

#■ 创建评论索引
sub reply_makeindex{
unless (-e "$dir/$blogdata/replyind.cgi"){
open (INDEX,">$dir/$blogdata/replyind.cgi");
close(INDEX);
}
&r_replyindex;

	open (INDEX,">$dir/$blogdata/replyind.cgi");
	$Reply_Content_sub=$Reply_Content;
	$Reply_Content_sub=~ s/<br>//ig;
	$Reply_Content_sub=~ s/&lt;strong&gt;//ig;
	$Reply_Content_sub=~ s/&lt;\/strong&gt;//ig;
	$Reply_Content_sub=~ s/&lt;br&gt;//ig;
	$Reply_Content_sub=~ s/</&lt;/g;
	$Reply_Content_sub=~ s/</&gt;/g;
	$Reply_Content_sub=~ s/\[quote\]/&gt;/g;
	$Reply_Content_sub=~ s/\[\/quote\]//g;
	if (length($Reply_Content_sub) > 30){
	@R_text=split(//,$Reply_Content_sub);
	$i=0;
	$Reply_Content_sub="";
	while ($i < 24){
	$Reply_Content_sub="$Reply_Content_sub$R_text[$i]";
	$i++;
	}
	#$Reply_Content_sub=substr($Reply_Content_sub,0,24);
	$Reply_Content_sub="$Reply_Content_sub...";
	}
	print INDEX"1|$Reply_Content_sub|$logfile|\n";
	$i=2;
	while ($i <= 10) {
		print INDEX"$i|$INDEX_CONTENT{$i-1}|$INDEX_LOGFILE{$i-1}|\n";
		$i++;
		}
	close(INDEX);
}

#■ 读取评论索引
sub r_replyindex{
open (INDEX,"$dir/$blogdata/replyind.cgi");
@replyind=<INDEX>;
close(INDEX);
foreach $replyind(@replyind){
	($index_counter,$index_content,$index_logfile,$blank)=split(/\|/, $replyind);
	$INDEX_CONTENT{$index_counter}=$index_content;
	$INDEX_LOGFILE{$index_counter}=$index_logfile;
	}
	$reply_index="";
	$i=1;
	while ($i <= 10){
		$reply_index="$reply_index<a href=\"./blog.cgi?action=omode&logid_from=$INDEX_LOGFILE{$i}&t=$templete_name\" target=\"_self\">$INDEX_CONTENT{$i}</a><br>";
		$i++;
	}
}

#■ 页面统计
sub setBlogStat{
&sys_time;
unless(-e "$dir/$blogdata/blogstat.cgi"){
	&LOCK;
	open(BS,">$dir/$blogdata/blogstat.cgi");
	print BS"$gmt_day|1|1|1|1";
	close(BS);
	open(BS,">$dir/$blogdata/viewerlist.cgi");
	print BS"$ENV{'REMOTE_ADDR'}\n";
	close(BS);
	&UNLOCK;
	}
	else{
	&getBlogStat;
	if ($bs_day ne $gmt_day){
		$bs_day=$gmt_day;
		$totalpage++;
		$totalip++;
		$daypage=1;	
		$dayip=1;
		&LOCK;
		open(BS,">$dir/$blogdata/viewerlist.cgi");
		print BS"$ENV{'REMOTE_ADDR'}\n";
		close(BS);
		rename("$dir/$blogdata/rlist.txt","$dir/$blogdata/rlist_.txt");
		&UNLOCK;
		}
		else{
		$totalpage++;
		$daypage++;
		&LOCK;
		open(VIEW,"$dir/$blogdata/viewerlist.cgi");
		@viewerip=<VIEW>;
		close(VIEW);
		&UNLOCK;
		$i=0;
		$iprecord=0;
		while($viewerip[$i] ne ""){
			if ($viewerip[$i] =~ /$ENV{'REMOTE_ADDR'}/){
			$iprecord=1;
			}
			$i++;
			}
		if ($iprecord != 1){
		$totalip++;
		$dayip++;
		&LOCK;
		open(BS,">>$dir/$blogdata/viewerlist.cgi");
		print BS"$ENV{'REMOTE_ADDR'}\n";
		close(BS);
		&UNLOCK;
		}
		}
	&LOCK;
	open(BS,">$dir/$blogdata/blogstat.cgi");
	print BS"$bs_day|$totalpage|$totalip|$daypage|$dayip";
	close(BS);
	
	open(TMP,">>$dir/$blogdata/rlist.txt");
	print TMP"|$ENV{'HTTP_REFERER'}|$ENV{'REMOTE_ADDR'}|\r\n";
	close(TMP);
	&UNLOCK;
	}
}
sub getBlogStat{
	&LOCK;
	open(BS,"$dir/$blogdata/blogstat.cgi");
	$bs=<BS>;
	close(BS);
	&UNLOCK;
	($bs_day, $totalpage, $totalip, $daypage, $dayip)=split(/\|/,$bs);
}

#■ 置顶功能
sub addOnTop{
open(TOP,"$dir/$blogdata/ontop.cgi");
@TOP=<TOP>;
close(TOP);
$i=0;
$toprecord=0;
while($TOP[$i] ne ""){
	if ($_[0] == $TOP[$i]){$toprecord=1;}
	$i++;
	}
if ($toprecord eq 0){
	open(TOP,">>$dir/$blogdata/ontop.cgi");
	print TOP"$_[0]\n";
	close(TOP);
	}
}

sub Cutoff_page{
$Cutoff_content=$_[0];
if ($cutoff eq "1"){
	if (length($Cutoff_content) > $cutoff_length || $Cutoff_content =~ /\[CutOffHere\]/){
	$p_cutoff_ok=1;
	if ($Cutoff_content =~ /\[CutOffHere\]/){
		$Cutoff_content = substr($Cutoff_content,0,index($Cutoff_content,"[CutOffHere]"));
		}
		else{
		$content_left=substr($Cutoff_content,$cutoff_length,length($Cutoff_content)-$cutoff_length);
		($content_left)=split(/\<br \/>|<\/p>|<br>/i,$content_left);
		$Cutoff_content=substr($Cutoff_content,0,$cutoff_length);
		$Cutoff_content="$Cutoff_content$content_left";
		}
	$Cutoff_content="$Cutoff_content&nbsp; <br><br><br><span style=\"logbottom\">［<a href=\"./blog.cgi?action=omode&logid_from=$BLOG_LOGID{$i}&t=$templete_name\">查看全文</a>］</span>";}
}
return $Cutoff_content;
}

sub getOnTop{
open(TOP,"$dir/$blogdata/ontop.cgi");
@TOP=<TOP>;
close(TOP);
$z=0;
while($TOP[$z] ne ""){
	$TOP[$z] =~ s/\n//g;
	open(LOG,"$dir/$blogdata/log_$TOP[$z].cgi");
	$top_log=<LOG>;
	$t=$z+1;
	($blank,$authorid,$classid,$title,$content,$abouturl,$aboutimage,$imgw,$imgh,$create_time,$blank)=split(/\|/,$top_log);
	close(LOG);
if ($db_admin eq "6"){
	$setdown_sw="[<a href=\"#\" onclick=\"Messagebox('./blog_manager.cgi?action=setdown&logid_from=$TOP[$z]');\">解锁</a>]";
	}
	$content=&Cutoff_page($content);
	$outPut=<<EOF;
	$outPut
	<div class="OnTop_title"> <span class="blog_class">置顶</span> $title $setdown_sw</div>
	<div class="OnTop_content">$content</div>
EOF
	$z++;
	}
}

sub delOnTop{
open(TOP,"$dir/$blogdata/ontop.cgi");
@TOP=<TOP>;
close(TOP);
open(TOP,">$dir/$blogdata/ontop.cgi");
$z=0;
while ($TOP[$z] ne ""){
	if ("$_[0]\n" ne $TOP[$z]){
		print TOP"$TOP[$z]";
		}
	$z++;
	}
close(TOP);
}

1;