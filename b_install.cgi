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
$FORM{$name} = $value;
push (@DELETE, $value) if ($name eq "DEL");
}
####################################
$dir=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
$dir=~ s/\\/\//g;
if ($dir eq ""){$dir=".";}

require "$dir/config.cgi";
require "$dir/b_lib.cgi";
$ver="SP1";
####################################
$action=$FORM{'action'};
$new_admin=$FORM{'new_admin'};
$new_pass=$FORM{'new_pass'};
$new_qq=$FORM{'new_qq'};
$new_mail=$FORM{'new_mail'};
$log_count=$FORM{'log_count'};
$dateset=$FORM{'dateset'};
$cutoff=$FORM{'cutoff'};
$cutoff_length=$FORM{'cutoff_length'};
$script_font_color=$FORM{'script_font_color'};
$common_title_color=$FORM{'common_title_color'};
$blog_name=$FORM{'blog_name'};
$i_charset=$FORM{'i_charset'};
if ($action eq ""){&mainpage;}
if ($action eq "save_admin"){&save_admin;}
if ($action eq "save_option"){&save_option;}

sub mainpage{
if ($action eq ""){
$panel_name="��װ����";
}
&framet;

print <<EOF;
<script language="javascript">
dialogArguments=0;

function checkit(){
if (document.all.agreebox.checked == true){
document.all.blog_name.disabled = false;
document.all.new_admin.disabled = false;
document.all.new_pass.disabled  = false; 
document.all.new_qq.disabled  = false;
document.all.new_mail.disabled  = false;
document.all.new_submit.disabled = false;
}
if (document.all.agreebox.checked == false){
document.all.blog_name.disabled = true;
document.all.new_admin.disabled = true;
document.all.new_pass.disabled  = true;
document.all.new_qq.disabled  = true;
document.all.new_mail.disabled  = true;
document.all.new_submit.disabled = true;
}
}
</script>
<center>
<strong>�û�Э��:</strong>
<table cellSpacing=1 cellPadding=5 border=0 width=400 bgcolor=#183050><tr><td bgcolor=#ffffff>������<br /><br />&nbsp; &nbsp; �ó�����Norman Shinn(�����)�����������κ���δ��Norman Shinn���������޸ġ�ɾ���������йذ�Ȩ��Ϣ�������ַ������á�����ɾ���� PRESENTED BY <a href="http://pfgroup.yeah.net">Norm\@n Shinn</a> ���ı�ʶ��<br /><br />Ȩ��������<br /><br />&nbsp; &nbsp; ����ʹ����Ѱ汾HUS���û�����Ȩ�������񱣻�����İ�Ȩ�����ַ��������񱨸���ʹ�ù����з��ֵ�һ��BUG��<br /><br />����<br /><br />&nbsp; &nbsp; �����ʹ�õ�����Ѱ汾��HUS Reviv\@l�����Norman Shinn���Ը�������ճɵ�һ�����⸺���ɸ���� BUG ���ճɵ�һ����ʧ��ʹ�����Լ��е���<br />Norman Shinnֻ�ṩ�������ʹ��Ȩ��ʹ����ʹ�ø������������һ����Ϣ��������Norman Shinn��������Norman Shinn����ʹ���ߵķ��Ը���<br /><br />�����Ϣ��<br /><br />����汾��$ver<br>BLOG���ݰ汾��$blogdata_version</td></tr></table>
<input id=agreebox type=checkbox onclick="checkit()"> ��ͬ������Э�飬������ʹ��Norman Shinn����Ѱ����<br />
<br /><strong>����Ա����:</strong><br />
<br /><form action="b_install.cgi" method=post>
BLOG��:<input id=blog_name class=textbox type=text value="" name="blog_name" disabled /><br />
����ԱID:<input id=new_admin class=textbox type=text value="" name="new_admin" disabled /><br />
��������:<input id=new_pass class=textbox type=password name="new_pass" disabled /><br />
����QQ:<input id=new_qq class=textbox type=text name="new_qq" disabled /><br />
��ϵMail:<input id=new_mail class=textbox type=text name="new_mail" disabled /><br /><br />
<input id=new_submit type=submit value="����" disabled><input type="hidden" value="save_admin" name="action">
</form>
</center>
EOF
&frameb;
}

sub save_admin{
if (-e "$dir/setup.pl"){$panel_name="�Ƿ���װ";&B_ERROR("���BLOG�Ѿ���װ���ˣ������Ҫ���°�װ��<br>��ɾ��BLOGĿ¼�е�setup.pl�ļ���")}
$new_admin =~ tr/[A-Z]/[a-z]/;
$usrid=$new_admin;
$petname="Blog����Ա";
$usrpwd=$new_pass;
$usrcard="00000000000000000";
$usrqq=$new_qq;
$usrmail=$new_mail;
$admin="6";
&w_usrdata;

if ($action eq "save_admin"){
$panel_name="��װ����";
}
&framet;
print <<EOF;
<script language="javascript">
dialogArguments=0;
</script>
<center>
<strong>BLOG�������ã�</strong><br>
<form method=post action=b_install.cgi>
ÿҳ��ʾ��<input class=textbox type="text" name="log_count" value="5" /><br />
���ڸ�ʽ��<input class=textbox type="text" name="dateset" value="YYYY��MM��DD��" /><br />
�����жϣ�<input class=textbox type="checkbox" name="cutoff" value="1" checked /><br />
�ж�������<input class=textbox type="text" name="cutoff_length" value="1000" /><br />
(�ֽڳ���Ϊ0ʱ����ʾ�������ݣ�ֻ��ʾ���⡣)<br>
˵����ɫ��<input class=textbox type="text" name="script_font_color" value="cccccc" /><br />
������ɫ��<input class=textbox type="text" name="common_title_color" value="eeeeee" /><br />
�����ʽ��<input class=textbox type="radio" name="i_charset" value="1" />UTF8 (decode�������룬��Ҫ������PERL�汾5.8)<br />
 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<input class=textbox type="radio" name="i_charset" value="2" disabled="disabled" />UTF8 (ʹ��gb-uni.tab�ļ�ת����Ч�ʵ�)<br />
<input class=textbox type="radio" name="i_charset" value="3" checked="checked" />GB2312<br />
<br />
<input type=submit value="����" /><input type="hidden" name="action" value="save_option" />
<input type="hidden" name="blog_name" value="$blog_name" />
<input type="hidden" name="new_admin" value="$new_admin" />
</form>
</center>
EOF
&frameb;
}

sub save_option{
if (-e "$dir/setup.pl"){$panel_name="�Ƿ���װ";&B_ERROR("���BLOG�Ѿ���װ���ˣ������Ҫ���°�װ��<br>��ɾ��BLOGĿ¼�е�setup.pl�ļ���")}
&sys_time;
if ($cutoff ne "1"){$cutoff="0"}
		if ($i_charset eq "1"){
			$config_charset_sub=<<EOF;
\$config_charset="1";
use Encode;
no Encode;
use utf8;
no utf8;
sub Char_Convert{
				if (\$_[0] eq "true"){
				\$Convert_string=decode("UTF-8",\$Convert_string);
				\$Convert_string=encode("euc-cn",\$Convert_string);
				}else{
				\$Convert_string=decode("euc-cn",\$Convert_string,0);
				utf8::decode(\$Convert_string);
				utf8::encode(\$Convert_string);
				}
			}
EOF
			}
			elsif ($i_charset eq "2"){
			$config_charset_sub=<<EOF;
\$config_charset="2";
sub Char_Convert{}
EOF
				}
			elsif ($i_charset eq "3"){
			$config_charset_sub=<<EOF;
\$config_charset="3";
sub Char_Convert{}
EOF
				}
$option=<<EOF;
\$log_count="$log_count";
\$dateset="$dateset";
\$ver="$ver";
#�� �Ƿ�ʹ�������ж�
\$cutoff="$cutoff";
#�� �����жϵ��ֽڳ���(�ֽڳ���Ϊ0ʱ����ʾ�������ݣ�ֻ��ʾ���⡣)
\$cutoff_length="$cutoff_length";
#�� ˵���������ɫ
\$script_font_color="$script_font_color";
#�� ���۵ı���ɫ
\$common_title_color="$common_title_color";
#�� ������͸����
\$alpha_calendar="68";
#�� ��־��
\$blog_name="$blog_name";
\$blog_creator="$new_admin";
\$blog_date="$gmt_year-$gmt_mon-$gmt_day $gmt_hour:$gmt_min:$gmt_sec";
#�� �����ʽת��
$config_charset_sub

1;
EOF
open (TMP,">$dir/setup.pl");
print TMP"$option";
close(TMP);
if ($action eq "save_option"){
$panel_name="��װ���";
}
&framet;
print<<EOF;
	<script language="javascript">
	dialogArguments=0;
	</script>
EOF
print "<center>�������һ��<br /><iframe src=\"husconfig.cgi\" width=\"500\" height=\"300\" frameborder=\"0\"></center>";
&frameb;
}