// 点击更换图片验证码
$(function () {
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = zzparam.setParam(src,'xx',Math.random());
        self.attr('src',newsrc)
    });
});
// 短信验证码以及接口加密
$(function () {
    $('#sms-captcha-btn').click(function (envent) {
         var self = $(this); //将this表位jq对象
        envent.preventDefault();
        var telephone = $("input[name='telephone']").val();
        if(!(/^1[345879]\d{9}$/.test(telephone))){
            swal({
                          type: 'warning',
                          title:"提示",
                          text:'请输入正确的手机号码'
                    });
            return;
        }
        var timestamp = (new Date).getTime();
        var sign = md5(timestamp+telephone+'12#dfdsaddddp');
        zzajax.post({
            'url':'/c/sms_captcha/',
            'data':{
                'telephone':telephone,
                'timestamp':timestamp,
                'sign':sign
            },
            'success':function (data) {
                // console.log(data);
                if(data['code']==200){
                    swal({
                          position: 'top-end',
                          type: 'success',
                          title: '短信验证码发送成功！',
                          showConfirmButton: false,
                          timer: 1500
                    })
                    self.attr('disabled','disabled');
                    var timeCont=60;
                    var timer=setInterval(function () {
                        timeCont--;
                        self.text(timeCont);
                        if (timeCont<= 0){
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.text('发送验证码')
                        }
                    },1000);
                }else {
                    swal({
                          type: 'warning',
                          title:"提示",
                          text:''+data['message']
                    })
                }
            }
        });

    })
});

$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var telephone_inp = $("input[name='telephone']");
        var smscaptcha_inp = $("input[name='sms_captcha']");
        var username_inp = $("input[name='username']");
        var password1_inp = $("input[name='password1']");
        var password2_inp = $("input[name='password2']");
        var graph_captcha_inp = $("input[name='graph_captcha']");
        var telephone = telephone_inp.val();
        var sms_captcha = smscaptcha_inp.val();
        var username = username_inp.val();
        var password1 = password1_inp.val();
        var password2 = password2_inp.val();
        var graph_captcha = graph_captcha_inp.val();

        zzajax.post({
            'url':'/signup/',
            'data':{
                'telephone':telephone,
                'sms_captcha':sms_captcha,
                'username':username,
                'password1':password1,
                'password2':password2,
                'graph_captcha':graph_captcha
            },
            'success':function (data) {
                if(data['code']==200){
                    var return_to = $('#return_to').text();
                    if(return_to){
                        window.location = return_to;
                    }else {
                        window.location='/';
                    }
                }
                else {
                    swal({
                          type: 'warning',
                          title:"提示",
                          text:''+data['message']
                    })
                }
            },
            'fail':function () {
                 swal(
                          'The Internet?',
                          'That thing is still around?',
                          'question'
                        )
            }
        })

    })
});