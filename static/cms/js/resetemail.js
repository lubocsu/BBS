$(function () {
    $('#send_e').click(function (event) {
        event.preventDefault();
        var email= $("input[name=email]").val();
        if(!email){
            swal({
                          type: 'warning',
                          title:"提示",
                          text:'请输入邮箱'
                    });
             return;
        }
        zzajax.get({
            'url':'/cms/email_captcha/',
            'data':{
                'email':email
            },
            'success':function (data) {
                if(data['code'] == 200){
                     swal({
                          position: 'top-end',
                          type: 'success',
                          title: '邮件发送成功，注意查收',
                          showConfirmButton: false,
                          timer: 1500
                    })
                }
                else {
                    swal({
                          type: 'warning',
                          title:"提示",
                          text:''+data['message']
                    })
                }
            },
            'fail':function (error) {
                 swal(
                          'The Internet?',
                          'That thing is still around?',
                          'question'
                        )
            }
        });
    });
});

$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var email_1 = $("input[name='email']");
        var captcha_1 = $("input[name='captcha']");
        var email = email_1.val();
        var captcha = captcha_1.val();
        zzajax.post({
            'url':'/cms/resetemail/',
            'data':{
                'email':email,
                'captcha':captcha
            },
            'success':function (data) {
                if (data['code']==200){
                    swal({
                          position: 'top-end',
                          type: 'success',
                          title: '恭喜，邮件修改成功！',
                          showConfirmButton: false,
                          timer: 1500
                    })
                }
                else {
                    swal({
                          type: 'warning',
                          title:"提示",
                          text:''+data['message']
                    })
                }
            },
            'fail':function (error) {
                swal(
                          'The Internet?',
                          'That thing is still around?',
                          'question'
                        )
            }
        });
    });
});