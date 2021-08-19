function chk_width(src){
if (qlog){
	img_width=150
}
else{
	img_width=400
}
if (src.width > img_width){
	src.style.height=img_width * src.height / src.width;
	src.style.width=img_width;
	}
}

function openclass(href){
window.open(href,'_self');
}