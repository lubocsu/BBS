// JavaScript Document
//
//
// 导航菜单

// $(".M1").click(function () {
//    $(".none").addClass("block");
// });

function navList(id) {
    var url = window.location.href;
    var $obj = $("#nav_dot"), $item = $("#J_nav_" + id);
    if(url.indexOf('percenter') >= 0) {
      var $div = $('#li1').children('.list-item');
        if ($div.is(":hidden")){
            $div.show();
        }
    }
    if(url.indexOf('changepwd') >= 0) {
      var $div = $('#li1').children('.list-item');
        if ($div.is(":hidden")){
            $div.show();
        }
    }
    if(url.indexOf('resetemail') >= 0) {
      var $div = $('#li1').children('.list-item');
        if ($div.is(":hidden")){
            $div.show();
        }
    }
    if(url.indexOf('posts') >= 0) {
      var $div = $('#li2').children('.list-item');
        if ($div.is(":hidden")){
            $div.show();
        }
    }
    if(url.indexOf('comments') >= 0) {
      var $div = $('#li3').children('.list-item');
        if ($div.is(":hidden")){
            $div.show();
        }
    }
    if(url.indexOf('croles') >= 0) {
      var $div = $('#li7').children('.list-item');
        if ($div.is(":hidden")){
            $div.show();
        }
    }
    if(url.indexOf('fusers') >= 0) {
      var $div = $('#li5').children('.list-item');
        if ($div.is(":hidden")){
            $div.show();
        }
    }
    if(url.indexOf('boards') >= 0) {
      var $div = $('#li4').children('.list-item');
        if ($div.is(":hidden")){
            $div.show();
        }
    }
    if(url.indexOf('cusers') >= 0) {
      var $div = $('#li6').children('.list-item');
        if ($div.is(":hidden")){
            $div.show();
        }
    }if(url.indexOf('banners') >= 0) {
      var $div = $('#li4').children('.list-item');
        if ($div.is(":hidden")){
            $div.show();
        }
    }

    $item.addClass("on").parent().removeClass("none").parent().addClass("selected");
    $obj.find("h4").hover(function () {
        $(this).addClass("hover");
    }, function () {
        $(this).removeClass("hover");
    });
    $obj.find("p").hover(function () {
        if ($(this).hasClass("on")) { return; }
        $(this).addClass("hover");
    }, function () {
        if ($(this).hasClass("on")) { return; }
        $(this).removeClass("hover");
    });
    $obj.find("h4").click(function () {
        var $div = $(this).siblings(".list-item");
        if ($(this).parent().hasClass("selected")) {
            $div.slideUp(600);
            $(this).parent().removeClass("selected");
        }
        if ($div.is(":hidden")) {
            $("#nav_dot li").find(".list-item").slideUp(600);
            $("#nav_dot li").removeClass("selected");
            $(this).parent().addClass("selected");
            $div.slideDown(600);

        } else {
            $div.slideUp(600);
        }
    });
}

/****表格隔行高亮显示*****/
window.onload=function(){
	oTable=document.getElementById("tab");//找表格
	aTr=document.getElementsByTagName("tr");//找所有的行
	for(i=0;i<aTr.length;i++){
		if(i%2==0){
			aTr[i].style.background="#fff";	
		}else{
			aTr[i].style.background="#ccc";	
		};
	};
};
