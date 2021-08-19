//New win
function Messagebox(href){
	window.open(href,'Messagebox','width=180,height=100,left=200,top=200,resizable=0,scrollbars=no');
}
function Newpage(href){
	window.open(href,'Messagebox','width=280,height=400,left=200,top=200,resizable=0,scrollbars=no');
}
//UBB
var Quote = 0;
var Bold  = 0;
var Italic = 0;
var Underline = 0;
var Code = 0;
var text_enter_bold	="请输入文字";
var text_enter_url      = "请输入连接地址";
var text_enter_urltitle      = "请输入连接文字";
var text_enter_image    = "请输入图片地址";
var text_enter_colorcode    = "请输入颜色代码";
var text_enter_colorfont    = "请输入文字";
var error_no_url        = "您必须输入地址";
var error_no_urltitle        = "您必须输入连接文字";
var error_no_col        = "您必须输入各项参数!";
var error_no_title      = "您必须输入主页标题";
var enter_no_colorcode    = "必须输入颜色代码";
var enter_no_colorfont    = "必须输入文字";
var error_no_bold	= "必须输入文字";
function textiWrite(NewCode) {
document.log_form.content.value+=NewCode;
document.log_form.content.focus();
return;
}
function link() {
var FoundErrors = '';
var enterURL   = prompt(text_enter_url, "http://");
var enterURLTITLE   = prompt(text_enter_urltitle, "");
if (!enterURL)    {
FoundErrors += "\n" + error_no_url;
}
if (!enterURLTITLE)    {
FoundErrors += "\n" + error_no_urltitle;
}
if (FoundErrors)  {
alert("错误!"+FoundErrors);
return;
}
var ToAdd = "[url="+enterURL+"]"+enterURLTITLE;
document.log_form.content.value+=ToAdd;
document.log_form.content.value+="[/url]";
document.log_form.content.focus();
}
function image() {
var FoundErrors = '';
var enterURL   = prompt(text_enter_image, "http://");
if (!enterURL) {
FoundErrors += "\n" + error_no_url;
}
if (FoundErrors) {
alert("错误!"+FoundErrors);
return;
}
var ToAdd = "[img]"+enterURL;
document.log_form.content.value+=ToAdd;
document.log_form.content.value+="[/img]";
document.log_form.content.focus();
}

function color() {
var entercolorcode   = prompt(text_enter_colorcode, "RED");
var entercolorfont   = prompt(text_enter_colorfont, "");
var ToAdd = "[color="+entercolorcode+"]"+entercolorfont;
document.log_form.content.value+=ToAdd;
document.log_form.content.value+="[/color]";
document.log_form.content.focus();
}

function frame() {
var enterframesrc   = prompt("请输入连接的网页地址", "");
var ToAdd = "[frame="+ enterframesrc +"]";
document.log_form.content.value+=ToAdd;
document.log_form.content.focus();
}

function html() {
var ToAdd = "[html]请在这里输入HTML代码";
document.log_form.content.value+=ToAdd;
document.log_form.content.value+="[/html]";
document.log_form.content.focus();
}

function quicksubmit(){
	if (event.keyCode==13 && event.ctrlKey){
		//判断是不是CTRL+ENTER
		document.log_form.submit();}
	if (event.keyCode==83 && event.altKey){
		//判断是不是ALT+S
		document.log_form.submit();}
}

function bold(){
var FoundErrors = '';
var TEXT_BOLD   = prompt(text_enter_bold, "");
if (!TEXT_BOLD) {
FoundErrors += "\n" + error_no_bold;
}
if (FoundErrors) {
alert("错误!"+FoundErrors);
return;
}
var ToAdd = "[b]"+TEXT_BOLD;
document.log_form.content.value+=ToAdd;
document.log_form.content.value+="[/b]";
document.log_form.content.focus();
}

function em(code){
document.log_form.content.value+="[em"+code+"]";
}