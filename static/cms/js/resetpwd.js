$(function () {
    $("#submit").click(function (event) {
        //阻止按钮默认的提交表单事件
        event.preventDefault();
        // 查找并获取输入框的数据
        var oldp= $("input[name=oldpwd]");
        var newp= $("input[name=newpwd]");
        var newp2= $("input[name=newpwd2]");
        var oldpwd = oldp.val();
        var newpwd = newp.val();
        var newpwd2 = newp2.val();
        // 通过post请求将数据发送给后台进行验证
        zzajax.post({
            'url':'/cms/changepwd/',
            'data':{
                'oldpwd':oldpwd,
                'newpwd':newpwd,
                'newpwd2':newpwd2
            },
            'success':function (data) {
                if(data['code'] == 200){
                    swal({
                          position: 'top-end',
                          type: 'success',
                          title: '密码修改成功',
                          showConfirmButton: false,
                          timer: 1500
                    })
                }

                else {
                     console.log(data);
                    var message = data['message'];

                    swal({
                          type: 'warning',
                          title:"提示",
                          text:''+message
                    })
                    // 清空输入框
                    oldp.val('');
                    newp.val('');
                    newp2.val('');
                }
            },
            'fail':function (error) {
                // console.log(error);
                        swal(
                          'The Internet?',
                          'That thing is still around?',
                          'question'
                        )
            }
        });
    });
});