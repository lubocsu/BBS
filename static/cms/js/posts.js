//帖子加精与取消
$(function () {
   $(".highlight-btn").click(function () {
       var self = $(this);
       var tr = self.parent().parent();
       var post_id = tr.attr("data-id");
       var highlight = parseInt(tr.attr("data-highlight"));
       var url ="";
       if(highlight){
           url = "/cms/uhpost/";
       }else {
           url = "/cms/hpost/";
       }
       zzajax.post({
           'url':url,
           'data':{
               'post_id':post_id
           },
           'success':function (data) {
               if(data['code']==200){
                   swal({
                          position: 'top-end',
                          type: 'success',
                          title: '操作成功！',
                          showConfirmButton: false,
                          timer: 1500
                    });
                   setTimeout(function () {
                       window.location.reload();
                   },1500);
               }else {
                    swal({
                          type: 'warning',
                          title:"提示",
                          text:''+data['message']
                    })
                }
               }
       })
   });
});
//移除帖子
$(function () {
   $('.delete-btn').click(function () {
       var self = $(this);
       var tr = self.parent().parent();
       var post_id = tr.attr('data-id');
       zzajax.post({
           'url':'/cms/dposts/',
           'data':{
               'post_id':post_id
           },
           'success':function (data) {
               if(data['code']==200){
                   swal({
                          position: 'top-end',
                          type: 'success',
                          title: '操作成功！',
                          showConfirmButton: false,
                          timer: 1000
                    });
                   setTimeout(function () {
                       window.location.reload();
                   },2000);
               }else {
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