#�� ����Ա��ϵ��ʽ [E-mail�е�@��ǰ��Ҫ���'\'�����򽫴�����ʾ]
$admin_connect="norman_shinn\@hotmail.com";
#�� GMTʱ������
$real_hour="8";
#�� URL
$domain="";
#�� PATH
$path="";
#�� �û�����Ŀ¼
$userdata="userdata";
#�� �������ݿ�Ŀ¼
$petdata="petdata";
#�� �������ݿ�Ŀ¼
$basicdata="basicdata";
#�� Tip����Ŀ¼
$tipdata="tipdata";
#�� COOKIE����ʱ��[��]��һ���������ã�
$expire_year="0";
#�� COOKIE����ʱ��[��]��һ���������ã�
$expire_min="30";
#�� ����ҳ��ˢ��ʱ��[��]
$chat_refreshtime="20";
#�� �ж����ʱ��[��]
$action_count="3270";
#�� �ַ���
$pcharset="gb2312";
#�� ����STYLE��Ϣ
$style01="<STYLE>a{text-decoration:none;}body{font: 9pt tahoma;}td{font: 9pt;}input{border:1px #000000 dotted;background:#B8B868;}</STYLE>";

#�� lockfile��
$lockf = "$dir/dummy.txt";
#�� �ļ�����ʽ
# �� 0=no 1=symlink���� 2=mkdir���� 3=Tripod�ã�������
$lkey = 2;

##################################
###����:##########################
#####��רҵ��ʿ�����޸���������#####
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################

$usrdata_version="1";
$mantozlib_version="P6";
##################################
$copyright="<FONT face=Tahoma size=1>This system base on MANTOZ CGI LIB[$mantozlib_version] by </FONT><A href=\"http://pfgroup.yeah.net\"><FONT face=Tahoma color=#000000 size=1>Norm\@n Sh!nn</A></FONT>";#����Ȩ��HACK���ٴη��������򣬵�����������������տͻ������������ʾ��HTML�����б�����һ�У����������ΪΪ��Ȩ��

#�� ��ȫ��¼���
sub chk{
if ($usrid =~ /\.cgi/){&ERROR('<center><br><strong>I D�зǷ��ַ�<br></strong></center>');exit;}
$usrid=~tr/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/;
$petname=~tr/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/;
unless (-e "$dir/$userdata/$usrid/info.cgi"){&ERROR('<center><br><strong>�޴�I D��<br>���߲�����ʱ��<br>�����µ�¼��<br>&nbsp;</strong></center>');exit;}
if ($usrid eq "" or $usrpwd eq ""){&ERROR('<center><br><strong>I D�����벻����Ϊ�գ�<br></strong></center>');exit;}
}

#�� ��ȫ��¼��� [��ȫ��ʽ]
sub chk_full{
$usrpwd="blank";
&r_usrdata;
$db_usrpwd_crypted=crypt($db_usrpwd,Mt);
if ($_[0] eq ""){
	&chk;
	if ($usrid ne $db_usrid){&ERROR("����û����ݿ��ܳ����쳣��������ϵ $admin_connect ��");}
	if ($usrpwd_crypted ne $db_usrpwd_crypted){&ERROR("�����������������ٵ�¼��");}
	}
	elsif($_[0] eq "background"){
	if ($usrid ne $db_usrid){return 1;}
	elsif ($usrpwd_crypted ne $db_usrpwd_crypted){return 1;}else{return 0;}
	}
}

#�� GMT��ʽʱ���ȡ
sub sys_time{
if ($sec4gmt_sec eq ""){
$sec4gmt_sec=time;
}
($gmt_sec,$gmt_min,$gmt_hour,$gmt_day,$gmt_mon,$gmt_year,$gmt_wday,$gmt_yday,$gmt_isdst ) = gmtime($sec4gmt_sec);
@weekday = ("Sun","Mon","Tue","Wed","Thu","Fri","Sat");
@monthname = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");
if ($gmt_min >= 30){$expire_hour=1;$final_min=$gmt_min + $expire_min - 60;}else{$final_min=$gmt_min + $expire_min;}
$final_hour = $gmt_hour + $real_hour + $expire_hour;
if ($final_hour > 24){$final_hour=$final_hour-24;$gmt_day++;}
$expire_date = sprintf("%s\, %02d\-%s\-%04d %02d:%02d:%02d GMT",$weekday[$gmt_wday],$gmt_day,$monthname[$gmt_mon],$gmt_year + 1900 + $expire_year,$final_hour,$final_min,$gmt_sec);
}

#�� �й���½ʱ���ȡ
sub sys_time_cn{
$year_now=$gmt_year+1900;
$mon_now=$gmt_mon+1;
$day_now=$gmt_day;
$hour_now=$gmt_hour + $real_hour;
if ($hour_now > 24){
$hour_now=$hour_now-24;
$day_now++;
}
$min_now=$gmt_min;
}

#�� ����1970��1��1�տ�ʼ���ۼ���������sys_time��������ʹ��
sub sys_sec4gmt{
@monthday=(0,31,28,31,30,31,30,31,31,30,31,30,31);
unless ($sec4gmt_year % 4){
$monthday[2]=29;
}
$sec4gmt_year=$_[0];
$sec4gmt_mon=$_[1];
$sec4gmt_day=$_[2];
use integer;
$r_year_num=($sec4gmt_year-72)/4;
no integer;
$i=1;
while ($i <= ($sec4gmt_mon)){
	$sec4gmt_mday+=$monthday["$i"];
	$i++;
}
$sec4gmt_sec=60*60*24*(365*($sec4gmt_year-70)+$r_year_num+$sec4gmt_mday)+1;
}

#�� дCOOKIE��Ϣ [������phtml����֮ǰʹ��]
sub w_cookies{
&sys_time;
if ($domain eq ""){
$cookies_domain="";
}
else{
$cookies_domain="domain=$domain; path=$path;";
}
print "Set-Cookie: Manto_info=$usrid|$usrpwd_crypted|; expires=$expire_date; $cookies_domain\n";
}

#�� ��COOKIE��Ϣ [������phtml����֮ǰʹ��]
sub r_cookies{
$contents_cookies = $ENV{HTTP_COOKIE};
$contents_cookies =~ s/Manto_info=//g;
($usrid, $usrpwd_crypted, $blank)=split(/\|/,$contents_cookies);
}

#�� ��ȫ���COOKIE��Ϣ [������phtml����֮ǰʹ��]
sub c_cookies{
&sys_time;
if ($domain eq ""){
$cookies_domain="";
}
else{
$cookies_domain="domain=$domain; path=$path;";
}
print "Set-Cookie: Manto_info=||; expires=$expire_date; $cookies_domain\n";
}

#�� д�û�����
sub w_usrdata{
&LOCK;
mkdir("$dir/$userdata/$usrid",0777);
open(USRFILE,">$dir/$userdata/$usrid/info.cgi");
print USRFILE"$usrdata_version|$usrid|$petname|$usrpwd|$usrcard|$usrqq|$usrmail|$admin";
close(USRFILE);
&UNLOCK;
}

#�� ���û�����
sub r_usrdata{
&LOCK;
open(USRFILE,"$dir/$userdata/$usrid/info.cgi");
$usr_info=<USRFILE>;
close(USRFILE);
($db_usrdata_version, $db_usrid, $petname, $db_usrpwd, $db_usrcard, $db_usrqq, $db_usrmail, $db_admin)=split(/\|/,$usr_info);
&UNLOCK;
}

#�� HTML��ʽ��ʾ����
sub phtml{
print "Pragma: no-cache\n";
print "Cache-Control: no-cache\n";
print "Content-type: text/html;charset=$pcharset\n\n";
}

#�� WML��ʽ��ʾ����
sub pwml{
#print "Content-type: text/html\n\n";
print "Content-type: text/vnd.wap.wml; charset=utf-8\n\n";
#application/vnd.wap.wml
}

#�� ����ҳ����
sub ERROR {
&phtml;
print<<EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML><HEAD><TITLE></TITLE>
<STYLE>
a{text-decoration:none;}
td{font: 9pt;}
input{border:1px #000000 dotted;background:#C898D8;}
.glow{filter:glow(color=#000000, strength=0);}
.dshadow{FONT-SIZE: 9pt; FILTER: dropshadow(color=#FFFFFF,offx=1,offy=1); COLOR: #000000; FONT-FAMILY: "����"}
</STYLE>

<META http-equiv=Content-Type content="text/html; charset=gb2312">
<META content="MSHTML 6.00.2800.1106" name=GENERATOR></HEAD>
<BODY bgColor=#ffffff leftMargin=0 background="" topMargin=0>
<TABLE style="BORDER-RIGHT: #000000 1px dashed; BORDER-LEFT: #000000 1px dashed" 
cellSpacing=0 cellPadding=0 width=150 align=center background=img/lbg.gif 
border=0>
  <TBODY>
  <TR>
    <TD background="" bgColor=#ffffff><IMG height=24 alt="" hspace=0 
      src="img/manto.gif" width=60 align=absMiddle border=0>&nbsp;&nbsp; 
      <STRONG><FONT color=#ff6820>��</FONT></STRONG><FONT face=Webdings 
      color=#ff6820>a</FONT>����<STRONG><FONT 
color=#ff6820>��</FONT></STRONG></TD></TR>
		  <TR>
		  <TD>$_[0]</TD>
		  </TR>
		   <TR>
    <TD align=middle background="" bgColor=#ffffff height=12>$copyright</TD></TR></TBODY></TABLE></BODY></HTML>
EOF
exit;
}

#===========#
# �� LOCK	#
#===========#
sub LOCK {
local($retry,$mtime);
if	 (-e "$lockf") {
	$mtime = (stat($lockf))[9];
	if ($mtime < (time - 60)){&UNLOCK;}else{&ERROR("����ϵͳæ�����һ������ԡ�");}}
	if($lkey eq 1){$retry = 5;while (!symlink(".", $lockf)){if (--$retry <= 0){&ERROR("����ϵͳæ�����һ������ԡ�");}sleep(1);}}
	elsif($lkey eq 2){$retry = 5;while (!mkdir($lockf, 0755)){if (--$retry <= 0) {&ERROR("����ϵͳæ�����һ������ԡ�");}sleep(1);}}
	elsif($lkey eq 3){local($lk) = mkdir($lockf, 0755);if ($lk eq 0)			 {&ERROR("����ϵͳæ�����һ������ԡ�");}}
$lockflag=1;
}
#===========#
# �� UNLOCK	#
#===========#
sub UNLOCK {if($lkey eq 1){unlink($lockf);}elsif($lkey eq 2){rmdir($lockf);}elsif($lkey eq 3){ rmdir($lockf);}$lockflag=0;}

1;