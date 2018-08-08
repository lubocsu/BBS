$(function () {
   var ue = UE.getEditor("editor",{
        "serverUrl":'/ueditor/upload/',
       "toolbars":[
           [
               'undo', //撤销
               'redo', //重做
               'bold', //加粗
               'italic', //斜体
               'source', //源代码
               'blockquote', //引用
               'insertcode', //代码语言
               'selectall', //全选
               'fontfamily', //字体
               'fontsize', //字号
               'simpleupload', //单图上传
               'emotion', //表情
           ]
       ]
    });
   window.ue =ue;
});
$(function () {
   $('#comment-btn').click(function (event) {
       event.preventDefault();
       var loginTag = $("#login-tag").attr('data-is-login');
       if (!loginTag){
           window.location='/signin/';
       }else {
            var content =window.ue.getContent();
            var post_id = $("#post-content").attr("data-id");
            zzajax.post({
                'url':'/acomment/',
                'data':{
                    'content':content,
                    'post_id':post_id
                },
                'success':function (data) {
                    if (data['code']==200){
                        window.location.reload();
                    }
                    else {
                         swal({
                          type: 'warning',
                          title:"提示",
                          text:''+data['message']
                    })
                    }
                }
            })
       }

   })
});