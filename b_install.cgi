#!/usr/bin/perl
############### 下面内容请不要随便修改 ##################
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
$panel_name="安装设置";
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
<strong>用户协议:</strong>
<table cellSpacing=1 cellPadding=5 border=0 width=400 bgcolor=#183050><tr><td bgcolor=#ffffff>申明：<br /><br />&nbsp; &nbsp; 该程序由Norman Shinn(许宏宇)自主开发，任何人未经Norman Shinn允许，不得修改、删除程序中有关版权信息的所有字符和引用。不得删除“ PRESENTED BY <a href="http://pfgroup.yeah.net">Norm\@n Shinn</a> ”的标识。<br /><br />权利和义务：<br /><br />&nbsp; &nbsp; 所有使用免费版本HUS的用户都有权利和义务保护软件的版权不受侵犯，有义务报告在使用过程中发现的一切BUG。<br /><br />免责：<br /><br />&nbsp; &nbsp; 如果你使用的是免费版本的HUS Reviv\@l软件，Norman Shinn不对该软件所照成的一切问题负责，由该软件 BUG 所照成的一切损失由使用者自己承担。<br />Norman Shinn只提供该软件的使用权，使用者使用该软件所发布的一切信息均不代表Norman Shinn的立场，Norman Shinn不对使用者的发言负责。<br /><br />软件信息：<br /><br />软件版本：$ver<br>BLOG数据版本：$blogdata_version</td></tr></table>
<input id=agreebox type=checkbox onclick="checkit()"> 我同意以上协议，并决定使用Norman Shinn的免费版软件<br />
<br /><strong>管理员设置:</strong><br />
<br /><form action="b_install.cgi" method=post>
BLOG名:<input id=blog_name class=textbox type=text value="" name="blog_name" disabled /><br />
管理员ID:<input id=new_admin class=textbox type=text value="" name="new_admin" disabled /><br />
管理密码:<input id=new_pass class=textbox type=password name="new_pass" disabled /><br />
管理QQ:<input id=new_qq class=textbox type=text name="new_qq" disabled /><br />
联系Mail:<input id=new_mail class=textbox type=text name="new_mail" disabled /><br /><br />
<input id=new_submit type=submit value="决定" disabled><input type="hidden" value="save_admin" name="action">
</form>
</center>
EOF
&frameb;
}

sub save_admin{
if (-e "$dir/setup.pl"){$panel_name="非法安装";&B_ERROR("这个BLOG已经安装过了，如果需要重新安装，<br>请删除BLOG目录中的setup.pl文件。")}
$new_admin =~ tr/[A-Z]/[a-z]/;
$usrid=$new_admin;
$petname="Blog管理员";
$usrpwd=$new_pass;
$usrcard="00000000000000000";
$usrqq=$new_qq;
$usrmail=$new_mail;
$admin="6";
&w_usrdata;

if ($action eq "save_admin"){
$panel_name="安装设置";
}
&framet;
print <<EOF;
<script language="javascript">
dialogArguments=0;
</script>
<center>
<strong>BLOG基本设置：</strong><br>
<form method=post action=b_install.cgi>
每页显示：<input class=textbox type="text" name="log_count" value="5" /><br />
日期格式：<input class=textbox type="text" name="dateset" value="YYYY年MM月DD日" /><br />
文章切断：<input class=textbox type="checkbox" name="cutoff" value="1" checked /><br />
切断字数：<input class=textbox type="text" name="cutoff_length" value="1000" /><br />
(字节长度为0时不显示文章内容，只显示标题。)<br>
说明颜色：<input class=textbox type="text" name="script_font_color" value="cccccc" /><br />
标题颜色：<input class=textbox type="text" name="common_title_color" value="eeeeee" /><br />
编码格式：<input class=textbox type="radio" name="i_charset" value="1" />UTF8 (decode方法解码，需要服务器PERL版本5.8)<br />
 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<input class=textbox type="radio" name="i_charset" value="2" disabled="disabled" />UTF8 (使用gb-uni.tab文件转换，效率低)<br />
<input class=textbox type="radio" name="i_charset" value="3" checked="checked" />GB2312<br />
<br />
<input type=submit value="决定" /><input type="hidden" name="action" value="save_option" />
<input type="hidden" name="blog_name" value="$blog_name" />
<input type="hidden" name="new_admin" value="$new_admin" />
</form>
</center>
EOF
&frameb;
}

sub save_option{
if (-e "$dir/setup.pl"){$panel_name="非法安装";&B_ERROR("这个BLOG已经安装过了，如果需要重新安装，<br>请删除BLOG目录中的setup.pl文件。")}
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
#■ 是否使用文章切断
\$cutoff="$cutoff";
#■ 文章切断的字节长度(字节长度为0时不显示文章内容，只显示标题。)
\$cutoff_length="$cutoff_length";
#■ 说明字体的颜色
\$script_font_color="$script_font_color";
#■ 评论的标题色
\$common_title_color="$common_title_color";
#■ 日历的透明度
\$alpha_calendar="68";
#■ 日志名
\$blog_name="$blog_name";
\$blog_creator="$new_admin";
\$blog_date="$gmt_year-$gmt_mon-$gmt_day $gmt_hour:$gmt_min:$gmt_sec";
#■ 编码格式转换
$config_charset_sub

1;
EOF
open (TMP,">$dir/setup.pl");
print TMP"$option";
close(TMP);
if ($action eq "save_option"){
$panel_name="安装完成";
}
&framet;
print<<EOF;
	<script language="javascript">
	dialogArguments=0;
	</script>
EOF
print "<center>还差最后一步<br /><iframe src=\"husconfig.cgi\" width=\"500\" height=\"300\" frameborder=\"0\"></center>";
&frameb;
}