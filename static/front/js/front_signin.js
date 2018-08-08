$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var telephone_inp = $("input[name='telephone']");
        var password_inp = $("input[name='password']");
        var remember_inp = $("input[name='remember']");
        var telephone = telephone_inp.val();
        var password = password_inp.val();
        var remember = remember_inp.checked?1:0;

        zzajax.post({
            'url':'/signin/',
            'data':{
                'telephone':telephone,
                'password':password,
                'remember':remember
            },
            'success':function (data) {
            if(data['code']==200){
                var return_to = $('#return_to').text();
                if (return_to){
                    window.location = return_to;
                }else {
                    window.location = '/';
                }
            }else{
                swal({
                          type: 'warning',
                          title:"提示",
                          text:''+data['message']
                    })
            }
        }
        })
    })
});