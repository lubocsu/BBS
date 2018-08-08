$(function () {
     var url = window.location.href;
    if(url.indexOf('?st=2') >= 0){
        var profileLi = $('.post-group-head');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children().eq(1).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('?st=3') >= 0){
        var profileLi = $('.post-group-head');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children().eq(2).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('?st=4') >= 0){
        var profileLi = $('.post-group-head');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children().eq(3).addClass('active').siblings().removeClass('active');
    } else if (url.indexOf('?st=4') < 0) {
        var profileLi = $('.post-group-head');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children().eq(0).addClass('active').siblings().removeClass('active');
    }
});