#!/usr/bin/perl
############### ���������벻Ҫ����޸� ##################
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
####################################
$dir=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
$dir=~ s/\\/\//g;
if ($dir eq ""){$dir=".";}

require "$dir/setup.pl";
require "$dir/config.cgi";
require "$dir/b_lib.cgi";
####################################
$action=$FORM{'action'};
$logid_from=$FORM{'logid_from'};
$classid=$FORM{'classid'};
$keyword=$FORM{'keyword'};
$view_year=$FORM{'view_year'};
$view_mon=$FORM{'view_mon'};
$view_day=$FORM{'view_day'};
$viewtype=$FORM{'viewtype'};
$logfile=$FORM{'logfile'};
$readername=$FORM{'readername'};
$Reply_Content=$FORM{'Reply_Content'};
$templete_name=$FORM{'t'};
$usrid=$FORM{'usrid'};
$usrpwd=$FORM{'usrpwd'};
$usrpwd_crypted=$FORM{'usrpwd_crypted'};
$easyreg=$FORM{'easyreg'};
####################################
if ($action eq ""){&mainpage;}
if ($action eq "viewclass"){&mainpage;}
if ($action eq "search"){&mainpage;}
if ($action eq "viewdata"){&mainpage;}
if ($action eq "unicode"){&unicode;}
if ($action eq "omode") {&omode;}
if ($action eq "omode_sp") {&omode;}
if ($action eq "reply") {&reply;}
if ($action eq "logout") {&logout;}

sub mainpage{
&r_blog_log;
&r_blog_templete_h;
unless ($templete_name =~ /rss/){
print "<script language=\"javascript\" src=\"client.js\"></script>";
&getOnTop;
}
else{
$cutoff="0";
}
$Convert_string=$outPut;
&Char_Convert;
print "$Convert_string";
$i=0;
$p_cutoff_ok=0;
while ($i++ < $log_count){
$CONTENT{$i}=&Cutoff_page($CONTENT{$i});
$CONTENT{$i} =~ s/\[CutOffHere\]//g;
if ($p_cutoff_ok ne "1"){$p_cutoff_ok="<br><br><br>";}else{$p_cutoff_ok="";}
$CONTENT{$i}="$CONTENT{$i}&nbsp; $p_cutoff_ok<span class=\"logbottom\">��<a href=\"./blog.cgi?action=omode&logid_from=$BLOG_LOGID{$i}&t=$templete_name#replythis\">���۴���($BLOG_REPLYCOUNT{$i})</a>��</span>";
&r_cookies;
$chk_result=&chk_full("background");
if ($db_admin eq "6" and $chk_result eq 0) {
$CONTENT{$i}="$CONTENT{$i}&nbsp; <span class=\"logbottom\">��<a href=\"#\" onclick=\"Messagebox('./blog_manager.cgi?action=settop&logid_from=$BLOG_LOGID{$i}')\">�ö�����</a>��</span>";
}
&hidecode;
if ($cutoff_length eq "0"){
	&r_blog_templete_b_sp;
}
else{
	&r_blog_templete_b;
	}
}
&r_blog_templete_f;
}

sub omode{
&r_blog_log;
$i=1;
&r_cookies;
$chk_result=&chk_full("background");
&hidecode;
if ($action eq "omode_sp"){
&phtml;
print <<EOF;
<html><head><title>$TITLE{$i}</title>
	<style>
	td{font:12px ����;}
	body{font:12px ����;}
	</style>
	</head><body link=#000000 alink=#000000 vlink=#000000 text=#000000 bgcolor=#ffffff>
EOF
}
else{
&r_blog_templete_h;
}
print "<script language=\"javascript\" src=\"client.js\"></script>";

if ($action eq "omode_sp"){
&sys_transubb;
print <<EOF;
<center><h1>$TITLE{$i}</h1>
		$CREATE_TIME{$i}</center><br>
	<p align=left>
	$CONTENT{$i}
	</p>
		
EOF
}
else{
	$i=1;
&r_blog_templete_b;

}
&r_reply;
$Convert_string=<<EOF;
<div class="replytable">��������</div>
EOF
&Char_Convert;
print "$Convert_string";
$i=1;
while ($Reply_Contentz{$i} ne ""){
	if ($Reply_contentz{$i} ne "[none]" and $Reply_Name{$i} ne "[no data]"){
$Convert_string=<<EOF;
<div class="replytd" id="replytd_$i" name="replytd_$i"><strong>$Reply_Name{$i}��</strong><br />$Reply_Contentz{$i}</div>
EOF
$CONTENT{$i}=$Convert_string;
&sys_transubb;
$Convert_string=<<EOF;
$CONTENT{$i}<div class="replytdcontrol"><a href="#quickreply" onclick="document.Reply_Form.Reply_Content.value='[quote]' + document.getElementsByName('replytd_$i').item(0).innerHTML + '[/quote]'"><img src="./b_img/quote.gif" border="0" style="margin-left:12px;margin-top:6px;margin-bottom:6px;cursor:hand;" /></a></div>
EOF
&Char_Convert;
print "$Convert_string";
	}
$i++;
}
if ($usrid ne ""){
	$pwdinput_name="usrpwd_crypted";
	$pwdinput_value=$usrpwd_crypted;
}
else{
	$pwdinput_name="usrpwd";
	$pwdinput_value="";
}
$Convert_string=<<EOF;
</table>
<br><br>
<div class="replytable"><a name="quickreply">��������</a></div>
	<div class="replytd">
	<form id="Reply_Form" name="Reply_Form" method="post" action="./blog.cgi" target="messagebox"><br><p align=left>
	������<input type="text" name="readername" value="$usrid" style="border:1px solid #000000;background:#dddddd;width:80px;" /> ���룺<input type="password" name="$pwdinput_name" value="$pwdinput_value" style="border:1px solid #000000;background:#dddddd;width:80px;" /> <input type="checkbox" value="1" name="easyreg" />�����ͬʱע��<br>
	���ݣ�<br>
	&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <textarea id="Reply_Content" name="Reply_Content" cols=80 rows=10 style="border:1px solid #000000;background:#dddddd;font:12px tahoma,����"></textarea></p>
	<input type=submit value="�ύ"><input type=hidden name="action" value="reply"><input type=hidden name="logfile" value="$BLOG_LOGID{1}"><br><br>
</form></div>
EOF
&Char_Convert;
print "$Convert_string";
if ($action eq "omode_sp"){
$Convert_string="</body></html>";
&Char_Convert;
print "$Convert_string";
}
else{
&r_blog_templete_f;
}
}

sub reply{
if ($readername eq ""){
&B_ERROR("���������������ˡ�");
}
if ($Reply_Content eq ""){
&B_ERROR("���������������ˡ�");
}
$Reply_Content=~ s/<IMG style="MARGIN-TOP: 6px; MARGIN-BOTTOM: 6px; MARGIN-LEFT: 12px; CURSOR: hand" src=".\/b_img\/quote.gif" border=0>//isg;
if (-e "$dir/$userdata/$readername/info.cgi"){
	if ($usrpwd eq "" and $usrpwd_crypted eq ""){
		$panel_name="��������";&B_ERROR('<br><strong>��I D�Ѿ�ע�ᣡ<br>�����I D���ԣ�<br></strong>');
	}
	else{
		$usrid=$readername;
		if ($usrpwd ne ""){
			$usrpwd_crypted=crypt($usrpwd,Mt);
		}
		&chk_full;
	}
}else{
	if ($easyreg eq "1"){
	$readername=~tr/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/;
	if ($readername eq "" or $usrpwd eq ""){$panel_name="��������";&B_ERROR('<br><strong>I D�����벻����Ϊ�գ�<br></strong>');}
	$usrid=$readername;
	$usr_right="0";
	$admin=$usr_right;
	&w_usrdata;
	$usrpwd_crypted=crypt($usrpwd,Mt);
	&w_cookies;
	}
}
$content=$Reply_Content;
&sys_translate('UBB');
$Convert_string=$content;
&Char_Convert('true');
$content=$Convert_string;
$Reply_Content=$content;
$Convert_string=$readername;
&Char_Convert('true');
$readername=$Convert_string;
&w_reply;
$logid_from=$logfile;
$panel_name="�ظ��ɹ�";
&B_ERROR('�ظ��ɹ���<script>opener.location.reload();</script>');
}

sub logout{
if ($usrid ne ""){
$usrpwd_crypted=crypt($usrpwd,Mt);
&chk_full;
&w_cookies;
$panel_name="˳����¼";
&B_ERROR("���Ѿ�˳����¼��<script>opener.location.reload('./blog.cgi?');</script>");
}
else{
&c_cookies;
$panel_name="˳���ǳ�";
&B_ERROR("���Ѿ�˳���ǳ���<script>opener.location.reload('./blog.cgi?');</script>");
}
}

sub hidecode{
if ($CONTENT{$i} =~ /\[HideMark\]/ and ($db_admin ne "6" or $chk_result ne 0) and ($usrid ne $AUTHORID{$i} or $chk_result ne 0)){$CONTENT{$i}="�Բ��𣬴���־Ϊ������־��ֻ�й���Ա�ܹ��鿴��";}
$CONTENT{$i} =~ s/\[HideMark\]//g;
if ($CONTENT{$i} =~ /\[HideObject:guest\]/ and $usrid eq ""){$CONTENT{$i}="�Բ��𣬴���־�ο���Ȩ�޲鿴��";}
$CONTENT{$i} =~ s/\[HideObject:guest\]//g;
$CONTENT{$i} =~ s/\[CutOffHere\]//g;
}

sub unicode{
&phtml;
$string="�����񾭲��������񾭲��������񾭲��������񾭲���";
$location=0;
open (TEMP,"$dir/gb-uni.tab");
@temp=<TEMP>;
close(TEMP);
$i=0;
foreach $temp(@temp){
	($left ,$right)=split(/ /,$temp);
	$right=~ s/\n//g;
	$Gb_word{$i}=$left;
	$Uni_word{$i}=$right;
	$i++;
	}
	
do{
	$word=substr($string,$location,2);
	$H_word= unpack("H*",$word); 
	$H_word=~tr/[a-z]/[A-Z]/;
	$i=0;
	while ($i < 21792 and $H_word ne $Gb_word{$i-1}){
	if ($H_word eq $Gb_word{$i}){print "&#x$Uni_word{$i};";}
	$i++;
	}
	$location=$location+2;
}while ($word ne "");

}
