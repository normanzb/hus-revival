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
########################
$action=$FORM{'action'};
$usrid=$FORM{'usrid'};
$usrpwd=$FORM{'usrpwd'};
if ($usrid =~ /\.cgi/ or $usrid =~ /\0/){&B_ERROR("你的尝试没有成功，如果发现BUG请联系Norman Shinn。");}
$content=$FORM{'content'};
$aboutimage=$FORM{'aboutimage'};
$imgw=$FORM{'imgw'};
$imgh=$FORM{'imgh'};
$title=$FORM{'title'};
$abouturl=$FORM{'abouturl'};
$class=$FORM{'class'};
$input_class_name=$FORM{'class_name'};
$input_class_scription=$FORM{'class_scription'};
$classid=$FORM{'classid'};
$logid_from=$FORM{'logid_from'};
$usr_right=$FORM{'usr_right'};
$usrcon=$FORM{'usrcon'};
$usrcard=$FORM{'usrcard'};
$usrqq=$FORM{'usrqq'};
$usrmail=$FORM{'usrmail'};
$petname=$FORM{'petname'};
$viewtype=$FORM{'viewtype'};
$Rcounter=$FORM{'Rcounter'};
$templetename=$FORM{'t_title'};
$h_code=$FORM{'H_code'};
$b_code=$FORM{'B_code'};
$f_code=$FORM{'F_code'};
$urlautodetect=$FORM{'urlautodetect'};
####################################
if ($action eq "") {&mainpage;}
if ($action eq "login") {&login;}
if ($action eq "editor") {&editor;}
if ($action eq "inout") {&inout;}
if ($action eq "new_log") {&new_log;}
if ($action eq "user") {&user;}
if ($action eq "class") {&create_class_page;}
if ($action eq "create_class") {&create_class;}
if ($action eq "delete_class") {&delete_class;}
if ($action eq "templete") {&templete;}
if ($action eq "blog") {&blog;}
if ($action eq "upfile") {&upfile;}
if ($action eq "del_log") {&del_log;}
if ($action eq "userform") {&userform;}
if ($action eq "newid") {&newid;}
if ($action eq "coverform") {&userform;}
if ($action eq "coverid") {&newid;}
if ($action eq "replymanager") {&replymanager;}
if ($action eq "delreply") {&delreply;}
if ($action eq "templete_save") {&templete_save;}
if ($action eq "templete_open") {&templete;}
if ($action eq "uploadpage") {&uploadpage;}
if ($action eq "Javawrite") {&pri_Javawrite;}
if ($action eq "delid") {&delid;}
if ($action eq "settop") {&settop;}
if ($action eq "setdown") {&setdown;}

################################
#■ Revival 版本内容开始
#■ 登录
sub login
{
&chk;
&r_usrdata;
if ($usrid ne $db_usrid){$panel_name="发生错误";&B_ERROR("你的用户数据可能出现异常错误，请联系 $admin_connect 。");}
if ($usrpwd ne $db_usrpwd){$panel_name="发生错误";&B_ERROR("密码错误！请检查密码后再登录！");}
$usrpwd_crypted=crypt($usrpwd,Mt);
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
&w_cookies;
$panel_name="登录成功";
#<div style="float:left;margin-left:10px;">
#	<img src="./b_img/icon_data.gif" onclick="javascript:init_datamanager();" style="cursor:hand;" alt="数据管理" /><br />
#	数据管理
#</div>
$LoginHTML=<<EOF;
欢迎使用HUS，请选择：<br />
<br />
<div style="float:left;margin-left:0px;">
	<img src="./b_img/icon_blog.gif" onclick="javascript:init_Editor();" style="cursor:hand;" alt="编写日志" /><br />
	编写日志
</div>
<div style="float:left;margin-left:10px;">
	<img src="./b_img/icon_user.gif" onclick="javascript:init_usermanager();" style="cursor:hand;" alt="用户管理" /><br />
	用户管理
</div>
<div style="float:left;margin-left:10px;">
	<img src="./b_img/icon_temp.gif" onclick="javascript:init_templete();" style="cursor:hand;" alt="编辑模板" /><br />
	编辑模板
</div>
<script language="javascript">
function init_Editor(){
Editor=window.open('./blog_manager.cgi?action=editor', 'Editor', 'width=480,height=500,left=300,top=50,resizable=0,scrollbars=no');
}
function init_datamanager(){
window.alert('该功能暂未开发')
}
function init_usermanager(){
window.open('./blog_manager.cgi?action=user', 'user');
}
function init_templete(){
window.open('./blog_manager.cgi?action=templete', 'templete');
}
</script>
<br /><br /><br /><br />
EOF
&LoginHTML($LoginHTML);
}

#■ 登录登出页面
sub inout{
&r_cookies;
if ($usrid eq "")
{
&mainpage;
}
else{
&c_cookies;
$panel_name="安全登出";
&B_ERROR("<center><br>你已经安全退出<br>&nbsp;</center>");
}
}

#■ 主页面
sub mainpage {
	if ($action eq "" or $action eq "inout"){
$panel_name="用户登录";
}
$LoginFORM=<<EOF;
		<img src="./editorfiles/logo.gif" align="left" /><strong>HUS Reviv\@l</strong><br /><font size=1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;version $ver</font>
		<br /><FORM title=login action=blog_manager.cgi method=post>
		I　D：<INPUT class="textbox" TYPE="text" VALUE="" NAME="usrid" maxlength="10" /><br />
		密码：<INPUT class="textbox" TYPE="password" VALUE="" NAME="usrpwd" maxlength="20" /><br /><br />
			<INPUT type="hidden" value="login" name="action" /><INPUT type="submit" value="确定" /> &nbsp;<INPUT type="reset" value="取消" />&nbsp; <a href="http://bynorman.51z.cn">获得HUS Reviv\@l 的拷贝</a>
    	</form>
EOF
&LoginHTML($LoginFORM);
}

#■ 页面框架
sub LoginHTML{
&phtml;
print <<EOF;
<html>
<head>
	<style>
	\@import url(./editorfiles/style.css);
	</style>
			<script language="javascript">
			m_x=0;
			m_y=0;
			Moving=0;
			function getPos(){
			m_x=event.x;
			m_y=event.y;
			}
			function setPos(){
			if (Moving == 1){
			CenterLogin.style.left=m_x-180;
			CenterLogin.style.top=m_y-8;
			setTimeout("setPos()",1);
			}
			}
			function StartDrag(){
			Moving=1;
			setPos();
			}
			function StopDrag(){
			Moving=0;
			}
			</script>
</head>
<body onmousemove="getPos();">
	<div id="CenterLogin">
		<div id="title" onmousedown="StartDrag()" onmouseup="StopDrag()" onselectstart="return false;">
		<strong>$panel_name &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</strong>
		</div>
		<div id="Loginbottom">
		$_[0]
		</div>
	</div>
</body>
</html>
EOF
}

#■ 内容编辑页面
sub editor{
&r_cookies;
&chk_full;
if ($action eq "editor"){
$panel_name="日志编辑";
}
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
if ($logid_from ne ""){
&r_blog_log;
}
if ($logid_from ne "" and $db_admin eq "2" and $AUTHORID{1} ne $usrid){$panel_name="发生错误";&B_ERROR("该日志不是你发表的，你的权限不够!");}
&phtml;
print <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="gb2312">
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" /> 
<meta http-equiv="Content-Language" content="gb2312" />
<meta http-equiv="pragma" CONTENT="no-cache"> 
<meta http-equiv="Cache-Control" CONTENT="no-cache, must-revalidate"> 
<meta name="Copyright" content="2004-2005 by norman shinn(许宏宇) http://pfgroup.yeah.net" /> 
<head>
<title>HUS Reviv\@l $ver</title>
<style>
\@import url(./editorfiles/style.css);
</style>
</head>
<body>

<div id="Menu">
<div id="husicon">
<img src="./editorfiles/husicon.gif" align=button />
</div>
<div id="buttons" name="buttons" class="buttons_out" onmouseover="stylechange('buttons','over',this);showlayer('layer_files')" onmouseout="stylechange('buttons','out',this)" onclick="detectclick();stylechange('buttons','click',this);showlayer('layer_files')">
日志(<u>L</u>)
</div>
<div id="buttons" name="buttons" class="buttons_out" onmouseover="stylechange('buttons','over',this);showlayer('layer_fav')" onmouseout="stylechange('buttons','out',this)" onclick="detectclick();stylechange('buttons','click',this);showlayer('layer_fav')">
窗口(<u>W</u>)
</div>
<div id="buttons" name="buttons" class="buttons_out" onmouseover="stylechange('buttons','over',this);showlayer('layer_help')" onmouseout="stylechange('buttons','out',this)" onclick="detectclick();stylechange('buttons','click',this);showlayer('layer_help')">
帮助(<u>H</u>)
</div>
</div>
<div id="control" onclick="detectclick(true)">
<button class="sbtn_over" onclick="Newdocument()"; title="New 新建">
<img src="./editorfiles/new.gif" />
</button>
<button class="sbtn_over" onclick="Opendocument()"; title="Open 打开">
<img src="./editorfiles/open.gif" />
</button>
<button class="sbtn_over" onclick="Savedocument()"; title="Save 保存">
<img src="./editorfiles/save.gif" />
</button>
<img src="./editorfiles/vline.gif" />
<button class="sbtn_over" onclick="ForeColor()"; title="Color 颜色">
<img src="./editorfiles/color.gif" />
</button>
<button class="sbtn_over" onclick="Editor.document.execCommand('Bold')"; title="Bold 粗体">
<strong>B</strong>
</button>
<button class="sbtn_over" onclick="Editor.document.execCommand('italic')"; title="Italic 斜体">
<i>I</i>
</button>
<button class="sbtn_over" onclick="Editor.document.execCommand('Underline')"; title="Underline 下划线">
<u>U</u>
</button>
<button class="sbtn_over" onclick="CreateLink();"; title="Link 超链接">
<img src="./editorfiles/link.gif" />
</button>
<button class="sbtn_over" onclick="InsertImage();"; title="Image 图片">
<img src="./editorfiles/img.gif" />
</button>
<button class="sbtn_over" onclick="InsertField()"; title="Code 代码">
<span style="font:7px tahoma;">Code</span>
</button>
<img src="./editorfiles/vline.gif" />
<button class="sbtn_over" onclick="InsertCutoff()"; title="Cutoff 切断">
<img src="./editorfiles/cutoff.gif" />
</button>
<button class="sbtn_over" onclick="InsertHideMark()"; title="Hide 隐藏">
<img src="./editorfiles/hide.gif" />
</button>
<br />
标题：<input class="text" type="text" name="i_title" value="$TITLE{1}" />
类别：<select name="i_classid" style="border:1px solid #000000;">
EOF
&r_blog_class;
if ($logid_from ne ""){
print "<option value=\"$CLASSID{1}\">不改变类</option>";
$CONTENT{1} =~ s/<br><br>\[script=\S+?\].+?\[\/script\]//isg;
}
$i=0;
while ($i <= $blog_class_maxid){
print "<option value=\"$i\">$CLASS_ATTRIB_NAME{$i}</option>";
$i++;
}
$CONTENT{1}=~ s/\"/\\\"/g;
$CONTENT{1}=~ s/\r\n//g;
$CONTENT{1}=~ s/\n\r//g;
$CONTENT{1}=~ s/[\n|\r]//g;
print <<EOF;
	<script language="javascript">
	function frame_init(){
	frames('Editor').document.body.innerHTML="$CONTENT{1}";
	}
	</script>
EOF
print <<EOF;
</select>
<br />
<iframe id="Editor" name="Editor" src="./editorfiles/mainpage.htm" frameborder="0" onclick="detectclick(true)" onload="frame_init();">
</iframe>
</div>
<div id="detectarea" onclick="detectclick(true)">

</div>
<div class="layer" id="layer_files">
<div id="Menulist" name="Menulist" class="Menulist_out" onmouseover="stylechange('Menulist','over',this)" onmouseout="stylechange('Menulist','out',this)" onclick="detectclick();stylechange('Menulist','click',this);Newdocument();">
新建(<u>N</u>) Ctrl+N
</div>
<div id="Menulist" name="Menulist" class="Menulist_out" onmouseover="stylechange('Menulist','over',this)" onmouseout="stylechange('Menulist','out',this)" onclick="detectclick();stylechange('Menulist','click',this);Opendocument();">
打开...(<u>O</u>) Ctrl+O
</div>
<div id="Menulist" name="Menulist" class="Menulist_out" onmouseover="stylechange('Menulist','over',this)" onmouseout="stylechange('Menulist','out',this)" onclick="detectclick();stylechange('Menulist','click',this);Savedocument();">
保存(<u>S</u>) Ctrl+S
</div>
<hr width=90%>
<div id="Menulist" name="Menulist" class="Menulist_out" onmouseover="stylechange('Menulist','over',this)" onmouseout="stylechange('Menulist','out',this)" onclick="detectclick();stylechange('Menulist','click',this);window.close();">
离开(<u>X</u>) Ctrl+X
</div>
</div>

<div class="layer" id="layer_fav">
<div id="Menulist" name="Menulist" class="Menulist_out" onmouseover="stylechange('Menulist','over',this)" onmouseout="stylechange('Menulist','out',this)" onclick="detectclick();stylechange('Menulist','click',this);Emotion=window.showModelessDialog('./editorfiles/em.htm',Editor,'dialogLeft:40px;dialogTop:40px;help:no;status:no;dialogHeight:360px;dialogWidth:240px;scroll:no;')">
表情(<u>E</u>)
</div>
<div id="Menulist" name="Menulist" class="Menulist_out" onmouseover="stylechange('Menulist','over',this)" onmouseout="stylechange('Menulist','out',this)" onclick="detectclick();stylechange('Menulist','click',this);UpfilePage=window.showModelessDialog('./blog_manager.cgi?action=upfile',Editor,'dialogLeft:40px;dialogTop:400px;help:no;status:no;dialogHeight:140px;dialogWidth:240px;scroll:no;')">
上传(<u>U</u>)
</div>
<div id="Menulist" name="Menulist" class="Menulist_out" onmouseover="stylechange('Menulist','over',this)" onmouseout="stylechange('Menulist','out',this)" onclick="detectclick();stylechange('Menulist','click',this);ClassPage=window.showModelessDialog('./blog_manager.cgi?action=class',window,'dialogLeft:40px;dialogTop:540px;help:no;status:no;dialogHeight:200px;dialogWidth:240px;scroll:no;')">
分类(<u>C</u>)
</div>
</div>

<div class="layer" id="layer_help">
<div id="Menulist" name="Menulist" class="Menulist_out" onmouseover="stylechange('Menulist','over',this)" onmouseout="stylechange('Menulist','out',this)" onclick="detectclick();stylechange('Menulist','click',this);window.open('http://update.bynorman.51z.cn','browser','width=280,height=400,scrollbar=auto,statusbar=no,')">
HUS Update
</div>
<div id="Menulist" name="Menulist" class="Menulist_out" onmouseover="stylechange('Menulist','over',this)" onmouseout="stylechange('Menulist','out',this)" onclick="detectclick();stylechange('Menulist','click',this);alert('作者:Norman Shinn(许宏宇)\\r\\n主页:http://pfgroup.yeah.net\\r\\nＱＱ:1984518\\r\\n版本:$ver')">
关于 HUS Reviv\@l
</div>
</div>
<script language="javascript">
//基本信息
husversion="$ver";
//菜单Function
clicked=0;//判断是否点击
function stylechange(obj,act,src){
btn=document.getElementsByName(obj);
if (act == 'over'){unact='out';}
if (act == 'over' && clicked == 1){unact='out';act='click';}
if (act == 'out'){unact='out';}
if (act == 'click'){unact='out';}
i=0;
while (i < btn.length){
btn.item(i).className=obj + '_' + unact;
i++;
}
src.className=obj + '_' + act;
}
function detectclick(sw){
if (clicked == 1){
clicked=0;
i=0;
while (i < document.all.length){
if (document.all.item(i).className == "layer"){
document.all.item(i).style.display="none";}
i++;
}
}else{
if (sw != true){
clicked=1;}
}
}
function showlayer(src){

if (clicked == 1){
i=0;
while (i < document.all.length){
if (document.all.item(i).className == "layer"){
document.all.item(i).style.display="none";}
i++;
}
document.all(src).style.display="block";
}
}

function Debug(){
alert(Test);
}
//文档操作
function Newdocument(){
	if (Editor.document.body.innerHTML != ""){
	yesorno=window.showModalDialog('./editorfiles/yesorno.htm','是否忽略原日志内容<br />并编辑新日志?<br /><br />',"dialogheight:100px;dialogwidth:180px;resizable:no;help:no;status:no;scroll:no;");	
	}
	else{
	yesorno=1;
	}
	if (yesorno == 1){
	location.reload('./blog_manager.cgi?action=editor');
	}
}
function Opendocument(path){
	path="";
	Rurl=window.showModalDialog('./editorfiles/filedialog.htm',window,"dialogheight:200px;dialogwidth:380px;resizable:no;help:no;status:no;scroll:no;");
	if (Rurl){
		if (Editor.document.body.innerHTML != ""){
		yesorno=window.showModalDialog('./editorfiles/yesorno.htm','是否忽略原日志内容<br />并编辑新日志?<br /><br />',"dialogheight:100px;dialogwidth:180px;resizable:no;help:no;status:no;scroll:no;");	
		}
		else{yesorno=1;}
		if (yesorno==1){
		window.open(path + Rurl,'_self');
		}
	}
}
function Savedocument(){
	if (i_title.value == ""){
	alert("标题为空，请填写标题！");
	}else{
	log_form.title.value=i_title.value;
	log_form.classid.value=i_classid.value;
	log_form.content.value=Editor.document.body.innerHTML;
	window.open('about:blank','Messagebox','width=180,height=100,left=200,top=200,resizable=0,scrollbars=no');
	log_form.submit();
	}
}
//Toolbar代码:
function CreateLink(){
Editor.document.body.focus();
Editor.document.execCommand('CreateLink');
}
function InsertImage(){
Editor.document.body.focus();
showModalDialog("./editorfiles/insert_image.html",Editor.document, "dialogheight:200px;dialogwidth:430px;resizable:no;help:no;status:no;scroll:no;");
}
function InsertField(){
Editor.document.body.focus();
Editor.document.execCommand('InsertFieldset');
}
function InsertCutoff(){
Editor.document.body.focus();
Editor.document.selection.createRange().pasteHTML('[CutOffHere]');
}
function InsertHideMark(){
var userselect = showModalDialog("./editorfiles/select_user.html", window, "dialogheight:80px;dialogwidth:120px;resizable: no; help: no; status: no; scroll: no;");
Editor.document.body.focus();
if (userselect != -2){
	if (userselect == 0){
	Editor.document.selection.createRange().pasteHTML('[HideMark]');
	}
	if (userselect == -1){
	Editor.document.selection.createRange().pasteHTML('[HideObject:guest]');
	}
}


}
function ForeColor(){
	Editor.document.body.focus();
	var oldcolor = _dec_to_rgb(document.all['Editor'].contentWindow.document.queryCommandValue('ForeColor'));
    var newcolor = showModalDialog("./editorfiles/select_color.html", oldcolor, "dialogheight:216px;resizable: no; help: no; status: no; scroll: no;");

    if (newcolor != null) {document.all['Editor'].contentWindow.document.execCommand('ForeColor', false, "#"+newcolor); }
}
function _dec_to_rgb(value) {
  var hex_string = "";
  for (var hexpair = 0; hexpair < 3; hexpair++) {
    var myByte = value & 0xFF;            // get low byte
    value >>= 8;                        // drop low byte
    var nybble2 = myByte & 0x0F;          // get low nybble (4 bits)
    var nybble1 = (myByte >> 4) & 0x0F;   // get high nybble
    hex_string += nybble1.toString(16); // convert nybble to hex
    hex_string += nybble2.toString(16); // convert nybble to hex
  }
  return hex_string.toUpperCase();
}
</script>
<div id="HideFORM">
	<FORM action="blog_manager.cgi" method="post" name="log_form" target="Messagebox">
	<input type="hidden" name="title" />
	<input type="hidden" name="classid" />
	<input type="hidden" name="content" />
	<input type="hidden" name="urlautodetect" value="1" />
	<input type="hidden" name="action" value="new_log" />
	<input type="hidden" name="logid_from" value="$logid_from" />
	</FORM>
</div>
</body>
</html>
EOF
}

#■ 类创建页面
sub create_class_page{
&r_cookies;
&chk_full;
if ($action eq "class"){
$panel_name="类管理";
}
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
&framet;
&get_Javawrite;
print <<EOF;
<iframe id="classframe" name="classframe" frameborder="0" src="./blog_manager.cgi?action=Javawrite" scrolling="no">
</iframe>
&nbsp; <img class="Imgbtn" src="./editorfiles/newclass.gif" align="absmiddle" onclick="Newclass();" border="0" alt="新建分类" />&nbsp; <img class="Imgbtn" src="./editorfiles/delclass.gif" align="absmiddle" border="0" onclick="Delclass()" alt="删除分类" /> &nbsp;<a href="#" onmouseover="checkgoValue();u_Scroller();" onmouseout="checkgoValue();"><font face="webdings">5</font></a> &nbsp;<a href="#" onmouseover="checkgoValue();d_Scroller();" onmouseout="checkgoValue();"><font face="webdings">6</font></a>
<script language="javascript">
go=0;
i=-1;
j=1;
function checkgoValue(){
if (go==0){
go=1;
}else{
go=0;
}
}
function u_Scroller(src){
	if (go == 1){
	classframe.scrollBy(0,i);
	setTimeout('u_Scroller();',10);
	}
	}
function d_Scroller(){
	if (go == 1){
	classframe.scrollBy(0,j);
	setTimeout('d_Scroller();',10);
	}
	}
function Newclass(){
sw_refresh=window.showModalDialog('./editorfiles/newclass.htm',window,'dialogwidth:280px;dialogheight:50px;resizable:no;help:no;status:no;scroll:no;');
if (sw_refresh == 1){
document.frames('classframe').location.reload('./blog_manager.cgi?action=Javawrite');//('./blog_manager.cgi?action=Javawrite','classframe');
}
}
function Delclass(){
	if (classsubmit.classid.value != ""){
	window.open('about:blank','Messagebox','width=180,height=100,left=200,top=200,resizable=0,scrollbars=no');
	classsubmit.submit();
	}
	else{
	alert('你未选择要删除的分类');
	}
}
</script>
<div id="hideFORM">
	<form name="classsubmit" action="blog_manager.cgi" method="post" target="Messagebox">
	<input type="hidden" value="" name="classid" /><input type="hidden" value="delete_class" name="action" />
	</form>
</div>
EOF
&frameb;
}

sub get_Javawrite(){
$Javawrite=<<EOF;
<html>
	<head>
	<style>
	td{font:9pt tahoma,宋体;}
	\@import url(./editorfiles/style_b.css);
	</style>
	<meta http-equiv="pragma" CONTENT="no-cache"> 
	<meta http-equiv="Cache-Control" CONTENT="no-cache, must-revalidate"> 
	</head>
	<body leftmargin="0" topmargin="0" style="background-color:#D4D0C8;">
<table border=0 width=236 bgcolor="#D4D0C8" cellspacing="0">

EOF
&r_blog_class;
$i=0;
$ScriptC_length=$blog_class_maxid+1;
$ScriptC="parent.dialogArguments.document.getElementsByName('i_classid').item(0).length=$ScriptC_length;";
while ($i <= $blog_class_maxid){
$ScriptC=<<EOF;
$ScriptC
parent.dialogArguments.document.getElementsByName('i_classid').item(0).options[$i].text='$CLASS_ATTRIB_NAME{$i}';
parent.dialogArguments.document.getElementsByName('i_classid').item(0).options[$i].value='$i';
EOF
$Javawrite=<<EOF;
	$Javawrite
	<tr id="class_elements" name="class_elements" class="class_normal" onclick="selectobj(this,'$i');">
	<td width=10 style="border-bottom:1px dotted #000000;">
	[$i]
	</td><td width="20%" style="border-bottom:1px dotted #000000;">
	$CLASS_ATTRIB_NAME{$i}
	</td><td width="80%" style="border-bottom:1px dotted #000000;">
	$CLASS_ATTRIB_SCRIPTION{$i}
	</td></tr>
EOF
$i++;
}
$Javawrite=<<EOF;
$Javawrite
</tr>
</table>
	<script language="javascript">
	CE=document.getElementsByName('class_elements');
	function selectobj(src,classid){
	i=0;
	while(i < CE.length){
		CE.item(i).className="class_normal";
		i++;
		}
		src.className="class_selected";
		parent.classsubmit.classid.value=classid;
	}
	$ScriptC
	</script>
	</html>
EOF
$Javawrite=~ s/\n\r//g;
$Javawrite=~ s/\n//g;
$Javawrite=~ s/\r//g;
}

sub pri_Javawrite(){
&phtml;
&get_Javawrite();
print "$Javawrite";
}

#■ 创建类
sub create_class{
&r_cookies;
&chk_full;
if ($action eq "create_class"){
$panel_name="已创建类";
}
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
&w_blog_class;
&B_ERROR("完成创建!<script>opener.windclose();</script>");
}

#■ 删除类
sub delete_class{
&r_cookies;
&chk_full;
if ($action eq "delete_class"){
$panel_name="已删除类";
}
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
&c_blog_class;
&B_ERROR("完成删除。<script>opener.window.open('./blog_manager.cgi?action=Javawrite','classframe');</script>");
}

#■ 新LOG页面
sub new_log{
&r_cookies;
&chk_full;
if ($action eq "new_log"){
$panel_name="建立日志";
}
if ($action eq "del_log"){
$panel_name="删除日志";
&r_blog_log;
if ($logid_from ne "" and $db_admin eq "2" and $AUTHORID{1} ne $usrid){$panel_name="发生错误";&B_ERROR("该日志不是你发表的，你的权限不够!");}
}
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
if ($content eq ""){$panel_name="发生错误";&B_ERROR("内容为空!");}
if ($title eq ""){$panel_name="发生错误";&B_ERROR("标题为空!");}
&sys_time;
&sys_translate("HTML");
&w_blog_log;
&B_ERROR("$panel_name完成<script>opener.log_form.logid_from.value='$maxlog';</script>");
}

#■ templete创建页面
sub templete{
&r_cookies;
&chk_full;
if ($action eq "templete"){
$panel_name="模版设计";
$textarea_disabled="disabled";
}
if ($action eq "templete_open"){
$panel_name="模版设计";
$textarea_disabled="";
open(TFILE,"$dir/$blogdata/tpl_$templetename\_h.cgi");
$h_code=<TFILE>;
close(TFILE);
open(TFILE,"$dir/$blogdata/tpl_$templetename\_b.cgi");
$b_code=<TFILE>;
close(TFILE);
open(TFILE,"$dir/$blogdata/tpl_$templetename\_f.cgi");
$f_code=<TFILE>;
close(TFILE);
}
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
&framet;
print <<EOF;
<form action="blog_manager.cgi" method=post Name="templete">
	<script language="javascript">
	dialogArguments=0;
	var cansave=0;
	function GetFileName(){
	filename=prompt('请输入模版名','');
	document.templete.t_title.value=filename;
	cansave=1;
	filebox.style.visibility='hidden';
	templete.H_code.disabled=false;
	templete.H_code.value='';
	templete.B_code.disabled=false;
	templete.B_code.value='';
	templete.F_code.disabled=false;
	templete.F_code.value='';

	}
	function ShowFileBox(){
	filebox.style.visibility='visible';
	}
	function HideFileBox(){
	filebox.style.visibility='hidden';
	}
	function OpenFile(filename){
	document.templete.t_title.value=filename;
	document.templete.action.value="templete_open";
	templete.submit();
	}
	function SaveFile(filename){
		if (document.templete.t_title.value != ""){
			document.templete.action.value="templete_save";
			templete.submit();
		}
	}
	</script>
	
<TABLE cellSpacing=0 cellPadding=0 width=500 background="" border=0 align=center>
	<tr><td>
	<img src="./b_img/editor_new.gif" border=0 align=absmiddle onclick="GetFileName()"> <img src="./b_img/editor_save.gif" border=0 align=absmiddle onclick="SaveFile()"> <img src="./b_img/editor_open.gif" border=0 onclick="ShowFileBox()" align=absmiddle> 
	&nbsp; 模版：<input type="text" name="t_title" value="$templetename" readonly style="border:0px solid #000000;background:#eeeeee"><input NAME="action" type=hidden name="action" value="templete_save"><br>
	</td></tr>
	</table>
	<br>
<TABLE cellSpacing=0 cellPadding=0 width="60%" background="" border=0 align=center>
  <TBODY>
  <TR>
    <TD 
    style="BORDER-RIGHT: #076394 1px solid; BORDER-TOP: #076394 1px solid; BORDER-LEFT: #076394 1px solid; BORDER-BOTTOM: #076394 1px solid" 
    background="" bgColor=#366594><FONT style="BACKGROUND-COLOR: #366594" 
      color=#ffffff>&nbsp;<STRONG>头</STRONG>_部</FONT></TD>
    <TD 
    style="BORDER-RIGHT: #076394 1px solid; BORDER-TOP: #076394 1px solid; BORDER-LEFT: #076394 1px solid; BORDER-BOTTOM: #076394 1px solid" 
    width=400 background="" bgColor=#ffffff rowSpan=2><TEXTAREA style="BORDER-RIGHT: #000000 0px solid; BORDER-TOP: #000000 0px solid; BORDER-LEFT: #000000 0px solid; WIDTH: 400px; BORDER-BOTTOM: #000000 0px solid; HEIGHT: 323px" name=H_code rows=11 cols=43 $textarea_disabled>$h_code</TEXTAREA> 
    </TD></TR>
  <TR>
    <TD 
    style="BORDER-RIGHT: #076394 1px solid; PADDING-RIGHT: 10px; BORDER-TOP: #076394 1px solid; PADDING-LEFT: 10px; PADDING-BOTTOM: 10px; BORDER-LEFT: #076394 1px solid; PADDING-TOP: 10px; BORDER-BOTTOM: #076394 1px solid" 
    background="" bgColor=#b7cedf>
      <P><STRONG>模版头部设计_</STRONG><BR><BR><STRONG>位置：</STRONG>网页上方的导航条及左侧的功能条<BR><STRONG>标签：</STRONG>
      <DIV 
      style="PADDING-RIGHT: 20px; PADDING-LEFT: 20px; PADDING-BOTTOM: 4px; PADDING-TOP: 4px">&lt;ControlPanel&gt;<BR>显示登录<BR>&lt;calendar&gt;<BR>显示日历<BR>&lt;pagehref&gt; 
      <BR>显示翻页连接<BR>&lt;classline&gt;<BR>显示分类连接<BR>&lt;reply_index&gt;<BR>显示最新回复<br />&lt;blogstat&gt;显示日志状态</DIV>
      <P></P></TD></TR></TBODY></TABLE><br>
      	  
      	  <TABLE cellSpacing=0 cellPadding=0 width="60%" background="" border=0 align=center>
  <TBODY>
  <TR>
    <TD 
    style="BORDER-RIGHT: #ffc0cb 1px solid; BORDER-TOP: #ffc0cb 1px solid; BORDER-LEFT: #ffc0cb 1px solid; BORDER-BOTTOM: #ffc0cb 1px solid" 
    background="" bgColor=#ffc0cb><FONT 
      color=#ffffff>&nbsp;<STRONG>中</STRONG>_部</FONT></TD>
    <TD 
    style="BORDER-RIGHT: #ffc0cb 1px solid; BORDER-TOP: #ffc0cb 1px solid; BORDER-LEFT: #ffc0cb 1px solid; BORDER-BOTTOM: #ffc0cb 1px solid" 
    vAlign=top width=400 background="" bgColor=#ffffff rowSpan=2><TEXTAREA style="BORDER-RIGHT: #000000 0px solid; BORDER-TOP: #000000 0px solid; BORDER-LEFT: #000000 0px solid; WIDTH: 400px; BORDER-BOTTOM: #000000 0px solid; HEIGHT: 404px" name=B_code rows=15 cols=43 $textarea_disabled>$b_code</TEXTAREA> 
    </TD></TR>
  <TR>
    <TD 
    style="BORDER-RIGHT: #ffc0cb 1px solid; PADDING-RIGHT: 10px; BORDER-TOP: #ffc0cb 1px solid; PADDING-LEFT: 10px; PADDING-BOTTOM: 10px; BORDER-LEFT: #ffc0cb 1px solid; PADDING-TOP: 10px; BORDER-BOTTOM: #ffc0cb 1px solid" 
    vAlign=top background="" bgColor=#fff5f4>
      <P><STRONG>模版中部设计_</STRONG><BR><BR><STRONG>位置：</STRONG>网页中部显示日志内容的表格<BR><STRONG>标签：</STRONG>
      <DIV 
      style="PADDING-RIGHT: 20px; PADDING-LEFT: 20px; PADDING-BOTTOM: 4px; PADDING-TOP: 4px">&lt;log_title&gt;<br />显示日志标题<br />&lt;class_name&gt;<br />
      显示类名<BR>&lt;class_script&gt;<BR>显示类描述<BR>&lt;content&gt;<BR>显示日志内容<BR>&lt;usrid&gt;<BR>发表人<BR>&lt;create_time&gt;<BR>发布时间<BR>&lt;logid_cgi&gt;<BR>日志ID(文件号)<BR>&lt;abouturl&gt;<BR>相关网址<BR>&lt;aboutimage&gt;<BR>相关图片</DIV>
      <P></P></TD></TR></TBODY></TABLE><br>
      	  
      	  <TABLE cellSpacing=0 cellPadding=0 width="60%" background="" border=0 align=center>
   <TBODY>
  <TR>
    <TD 
    style="BORDER-RIGHT: #a8cf56 1px solid; BORDER-TOP: #a8cf56 1px solid; BORDER-LEFT: #a8cf56 1px solid; BORDER-BOTTOM: #a8cf56 1px solid" 
    background="" bgColor=#a8cf56 height=10><FONT 
      color=#ffffff>&nbsp;<STRONG>尾</STRONG>_部</FONT></TD>
    <TD 
    style="BORDER-RIGHT: #a8cf56 1px solid; BORDER-TOP: #a8cf56 1px solid; BORDER-LEFT: #a8cf56 1px solid; BORDER-BOTTOM: #a8cf56 1px solid" 
    vAlign=top width=400 background="" bgColor=#ffffff rowSpan=2><TEXTAREA style="BORDER-RIGHT: #000000 0px solid; BORDER-TOP: #000000 0px solid; BORDER-LEFT: #000000 0px solid; WIDTH: 400px; BORDER-BOTTOM: #000000 0px solid; HEIGHT: 264px" name=F_code rows=7 cols=43 $textarea_disabled>$f_code</TEXTAREA> 
    </TD></TR>
  <TR>
    <TD 
    style="BORDER-RIGHT: #a8cf56 1px solid; PADDING-RIGHT: 10px; BORDER-TOP: #a8cf56 1px solid; PADDING-LEFT: 10px; PADDING-BOTTOM: 10px; BORDER-LEFT: #a8cf56 1px solid; PADDING-TOP: 10px; BORDER-BOTTOM: #a8cf56 1px solid" 
    vAlign=top background="" bgColor=#f1f8e4>
      <P><STRONG>模版尾部设计_</STRONG><BR><BR><STRONG>位置：</STRONG>显示网页底部版权信息等<BR><STRONG>标签：</STRONG> 

      <DIV 
      style="PADDING-RIGHT: 20px; PADDING-LEFT: 20px; PADDING-BOTTOM: 4px; PADDING-TOP: 4px">&lt;pagehref&gt;<BR>翻页连接<BR>&lt;usagetime&gt;<br />程序耗时显示<br />
      </DIV>
      <HR width="100%" color=#c0c0c0 SIZE=1>
      请务必保留“Program Presented by <A href="http://pfgroup.yeah.net">Norm\@n 
      sh!nn</A>”<BR>字样。</TD></TR></TBODY></TABLE>
      	  <div id=filebox style="visibility:hidden;POSITION: absolute;LEFT: 300px;TOP:150px;">
      	  <table  cellSpacing=0 cellPadding=0 width=500 style="border:1px solid #000000"><tr><td bgcolor=#aaaaaa height=24> &nbsp;选择文件</td></tr>
      	  	  <tr><td bgcolor=#eeeeee> &nbsp;
EOF
opendir(BLOGDIR,"$dir/$blogdata/");
while ($dir_name = readdir(BLOGDIR))
{
	if ($dir_name =~ /tpl_(.*)_h.cgi/){
	print "<a href=\"#\" onclick=\"OpenFile('$1')\">$1</a>&nbsp;";
	}
}

closedir(BLOGDIR);
print "</td></tr><tr><td align=right>[<a href=\"#\" onclick=\"HideFileBox()\">取消</a>]</td></tr></table></div>";
&frameb;

}

#■ templete页面保存
sub templete_save{
&r_cookies;
&chk_full;
if ($action eq "templete_save"){
$panel_name="储存完毕";
}
if ($db_admin ne "6"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
$h_code=~ s/\n//g;
$b_code=~ s/\n//g;
$f_code=~ s/\n//g;
open(TFILE,">$dir/$blogdata/tpl_$templetename\_h.cgi");
print TFILE"$h_code";
close(TFILE);
open(TFILE,">$dir/$blogdata/tpl_$templetename\_b.cgi");
print TFILE"$b_code";
close(TFILE);
open(TFILE,">$dir/$blogdata/tpl_$templetename\_f.cgi");
print TFILE"$f_code";
close(TFILE);
&framet;
print<<EOF;
	<script language="javascript">
	dialogArguments=0;
	</script>
	<center>模板更新完成！</center>
EOF
&frameb;
}

#■ BLOG管理页面
sub blog{
&r_cookies;
&chk_full;
if ($action eq "blog"){
$panel_name="日志管理";
}
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
&framet;
print <<EOF;
<table border=0 width=100%>
EOF
&r_blog_log;
&pagehref;
print "<tr><td colspan=4>$pagehref</td></tr>";
$i=0;
while($i++ < $log_count){
print <<EOF;
<tr><td style="border-bottom:1px dashed #000000;" width=70%>$TITLE{$i}</td><td><a href="#" onclick="parent.CloseandReturn('./blog_manager.cgi?action=editor&logid_from=$BLOG_LOGID{$i}');">编辑&nbsp;<a href="./blog_manager.cgi?action=del_log&logid_from=$BLOG_LOGID{$i}">删除</a>&nbsp;<a href="./blog_manager.cgi?action=replymanager&logid_from=$BLOG_LOGID{$i}">评论管理</a></a></td></tr>
EOF
}
print <<EOF;
</table>
EOF
&frameb;
}

#■ 数据管理页
sub upfile{
&r_cookies;
&chk_full;
if ($action eq "upfile"){
$panel_name="文件上传";
}
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
&framet;
print <<EOF;
<iframe id="dataframe" frameborder="0" src="about:blank" scrolling="no">
</iframe>
<script>
function writeHTML(){
dataframe.document.write('<html><body bgcolor="#D4D0C8" leftmargin="0" topmargin="0"><form name="upfileform" method="POST" action="upfile.cgi" ENCTYPE="multipart/form-data"><input type="file" name="upfile"><br><input type="button" value="上载" onclick="upfileform.submit();this.disabled=true;this.value=\\'上载中...\\'"></form></body></html>');
}
writeHTML();
</script>
EOF
&frameb;
}

#■ 用户管理页面
sub user{
&r_cookies;
&chk_full;
if ($action eq "user"){
$panel_name="用户管理";
}
if ($db_admin ne "6"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}

&framet;
print <<EOF;
<script>
	dialogArguments=0;
</script>
<center>
	<TABLE WIDTH=100%><tr><td bgcolor=#dedede colspan=4 height=20><a href="./blog_manager.cgi?action=userform">&nbsp;添加新用户</a></td></tr></TABLE>
	<TABLE cellSpacing=0 cellPadding=0 width=500 border=0>
    <TBODY>
    <TR>
    <TD background="" bgColor=#daebfe STYLE="border:1px solid #076394">&nbsp;<b>用户列表</b><br>&nbsp;&nbsp;
EOF
opendir(USRDIR,"$dir/$userdata");
while ($dir_name = readdir(USRDIR))
{
	if ($dir_name ne "." and $dir_name ne ".."){
	print "<a href=\"./blog_manager.cgi?action=coverform&usrid=$dir_name\">$dir_name</a>&nbsp;";
	}
}

closedir(USRDIR);
print <<EOF;
</TD></TR></TBODY></TABLE>
</center>
EOF
&frameb;
}

#■ 用户添加页面
sub userform{
$usridbak=$usrid;
&r_cookies;
&r_usrdata;
if ($action eq "userform"){
$panel_name="用户添加";
}
if ($action eq "coverform"){
$panel_name="编辑用户";
&chk_full;
	if ($usrid ne $usridbak and $db_admin ne "6"){&B_ERROR("你没有权限。");}
}
if ($db_admin eq "6"){
	$userform_html_add="<input type=\"radio\" name=\"usr_right\" value=\"6\">管理员 <input type=\"radio\" name=\"usr_right\" value=\"2\">更新成员 <input type=\"radio\"  name=\"usr_right\" value=\"0\">普通会员 <br /><input type=\"button\" value=\"删除\" name=\"\" onclick=\"Messagebox('./blog_manager.cgi?action=delid&usrid=' + document.userform.usrid.value)\" />";
	}
if ($action eq "userform"){$action_value="newid";}else{$action_value="coverid";}
$usrid=$usridbak;
&r_usrdata;
&framet;
print <<EOF;
<script>
	dialogArguments=0;
</script>
<CENTER><TABLE>
	<TR>
	<FORM id="userform" name="userform" action="./blog_manager.cgi" method=post><TD>
I &nbsp;D ：<INPUT id="usrid" style="WIDTH: 63px; HEIGHT: 19px" size="8" name="usrid" value="$db_usrid" />「登入用的帐户」<BR><BR>
密码：<INPUT style="WIDTH: 63px; HEIGHT: 19px" size="8" name="usrpwd" value="$db_usrpwd" type="password" />「别告诉别人哦」<BR><BR>
确认：<INPUT style="WIDTH: 63px; HEIGHT: 19px" size="8" name="usrcon" value="$db_usrpwd" type="password" />「重新输一遍密码」<BR><BR>
证件：<INPUT style="WIDTH: 63px; HEIGHT: 19px" size="8" name="usrcard" value="$db_usrcard" maxLength="18" />「你的身份证号码」<BR><BR>
Q Q ：<INPUT style="WIDTH: 63px; HEIGHT: 19px" size="8" name="usrqq" value="$db_usrqq" /><BR>
Mail &nbsp;：<INPUT style="WIDTH: 63px; HEIGHT: 19px" size="8" name="usrmail" value="$db_usrmail" /><BR>
<input type="hidden" name="action" value="$action_value" /><input type="submit" value="提交" /> $userform_html_add
      	  </TD></FORM></TR></TABLE>
      </CENTER>
EOF
&frameb;
}

#■ 删除日志
sub del_log{
if ($logid_from eq ""){$panel_name="发生错误";&B_ERROR("该日志为空，无法删除！");}
$content="[none]";
$title="[no data]";
$classid="-1";
&new_log;
}

#■ 用户添加页面
sub newid{
if ($action ne "newid"){
	$usridbak=$usrid;
	$usrpwdbak=$usrpwd;
	&r_cookies;
	&r_usrdata;
	if ($usrid ne "" and $usrid ne $usridbak and $db_admin ne "6" and $action ne "newid" or ($usrid eq "" and $action ne "newid")){
		&chk_full;
		$panel_name="发生错误";
		&B_ERROR("你的权限不够!");
	}
	if ($usridbak eq $usrid){$usr_right=$db_admin;}
	if ($action eq "userform"){
	$panel_name="用户管理";
	}
	if ($usridbak eq $usrid){$sw_cookies="1";}else{$sw_cookies="0";}
	$usrid=$usridbak;
	$usrpwd=$usrpwdbak;
}else{
	if ($db_admin ne "6" and $usr_right ne ""){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
	if ($usr_right eq ""){$usr_right="0";}
	$sw_cookies="1";
	$reloadcode="<script language=\"javascript\">opener.location.reload();</script>";
}
$usrid=~tr/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/;
$usrid=~s/\s//ig;
if ($usrid eq "" or $usrpwd eq ""){$panel_name="发生错误";&B_ERROR('<br><strong>I D和密码不可以为空！<br></strong>');}
if (-e "$dir/$userdata/$usrid/info.cgi" and $action eq "newid"){$panel_name="发生错误";&B_ERROR('<br><strong>该I D已经注册！<br>请更换I D重试！<br></strong>');}
if (length($usrpwd) > 20 or length($usrpwd) < 5){$panel_name="发生错误";&B_ERROR('<br><strong>密码长度不合法！<br>密码必须5-10个字符！<br></strong>');}
if ($usrpwd ne $usrcon){$usrpwd="";$usrcon="";$panel_name="发生错误";&B_ERROR('<br><strong>两次密码输入有错！<br>请重新输入密码！</strong><br>');}
if ($usrmail !~ /\@.*\./){$panel_name="发生错误";&B_ERROR('<br><strong>E-mail格式非法！<br>请重新输入E-mail！</strong><br>');}
if ($usrqq =~ /\D/){$panel_name="发生错误";&B_ERROR('<br><strong>QQ号中有非法字符！<br>请重新输入QQ！</strong><br>');}
if (length($usrcard) != 18 and length($usrcard) != 15){$panel_name="发生错误";&B_ERROR('<br><strong>身份证长度不合法！<br>请重新输入身份证！</strong><br>');}
if ($usrcard =~ /\D/){$panel_name="发生错误";&B_ERROR('<br><strong>身份证中有非法字符！<br>请重新输入身份证！</strong><br>');}
$admin=$usr_right;
&w_usrdata;
$usrpwd_crypted=crypt($usrpwd,Mt);
if ($sw_cookies eq "1"){&w_cookies;}
$panel_name="注册完成";
&B_ERROR("<br>编辑完成！$reloadcode");
}

#■ 删除ID
sub delid{
$delusrid=$usrid;
&r_cookies;
&r_usrdata;
&chk_full;
if ($db_admin ne "6"){&B_ERROR("你没有权限删除用户。");}
unlink("$dir/$userdata/$delusrid/info.cgi");
rmdir("$dir/$userdata/$delusrid");
$panel_name="注册完成";
&B_ERROR("删除完成。");
}

#■ 评论管理
sub replymanager{
&r_cookies;
&chk_full;
if ($action eq "replymanager"){
$panel_name="评论管理";
}
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}
&framet;

$BLOG_LOGID{1}=$logid_from;
$i=1;
&r_reply;
print <<EOF;
<div style="width:372px;height:140px;overflow:auto;">
EOF
$i=1;
while ($Reply_Contentz{$i} ne ""){
print <<EOF;
		<div class="reply"><b>$Reply_Name{$i}：</b><br><br>&nbsp; &nbsp; $Reply_Contentz{$i}<br><br>
		&nbsp; [<a href="./blog_manager.cgi?action=delreply&logid_from=$logid_from&Rcounter=$i">删除</a>]
		</div>
EOF
$i++;
}
print "</table></div>";
&frameb;
}

#■ 评论删除
sub delreply{
&r_cookies;
&chk_full;
if ($action eq "delreply"){
$panel_name="删除评论";
}
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}

$logfile=$logid_from;
&w_reply;
&B_ERROR("评论已经删除！");
}

#■ 上传页 
sub uploadpage{
&r_cookies;
&chk_full;
if ($db_admin ne "6" and $db_admin ne "2"){$panel_name="发生错误";&B_ERROR("你的权限不够!");}

&phtml;
print <<EOF;
<html>
<head>
<style>
.textbox{font:9pt tahoma,宋体;background:;border:1px solid #000000;background-image:URL(./b_img/bg_button.gif);width:150 px;height:20 px;}
</style>
</head>
<body topMargin="0" leftMargin="0" bgcolor="#eeeeee">
<form method="post" action="upfile.cgi" ENCTYPE="multipart/form-data">
<input class="textbox" type="file" name="upfile"> <input type="submit" value="上载"><input type="hidden" name="editorup" value="1">
</form>
</body>
</html>
EOF
}

#■ 置顶
sub settop{
&r_cookies;
$chk_result=&chk_full("background");
if ($db_admin eq "6" and $chk_result eq 0) {
&addOnTop($logid_from);
&B_ERROR("已经置顶文章。<script>opener.location.reload('./blog.cgi?');</script>");
}else{
&B_ERROR("你没有权限。");
}
}

#■ 解除置顶
sub setdown{
&r_cookies;
$chk_result=&chk_full("background");
if ($db_admin eq "6" and $chk_result eq 0) {
&delOnTop($logid_from);
&B_ERROR("已经解除置顶文章。<script>opener.location.reload('./blog.cgi?');</script>");
}else{
&B_ERROR("你没有权限。");
}
}
###############
#■ Revival 版本内容结束