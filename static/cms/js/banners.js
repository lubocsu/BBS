//添加轮播图
$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var name_ipt = $("input[name='name']");
        var image_ipt = $("input[name='image_b']");
        var link_ipt = $("input[name='link_url']");
        var priority_ipt = $("input[name='priority']");
        var name = name_ipt.val();
        var image_b= image_ipt.val();
        var link_url=link_ipt.val();
        var priority = priority_ipt.val();
        var SubmitType = self.attr('data-type');
        var BannerId = self.attr('data-id');
        var url ='';
        if(!name || !image_b || !link_url || !priority){
            swal({
                          type: 'warning',
                          title:"提示",
                          text:'请输入完整的轮播图数据'
                });
            return;
        }
        if(SubmitType=='update'){
            url = '/cms/ubanner/';
        }else {
            url ='/cms/abanner/';
        }
        zzajax.post({
            'url':url,
            'data':{
                'name':name,
                'image_b':image_b,
                'link_url':link_url,
                'priority':priority,
                'banner_id':BannerId
            },
            'success':function (data) {
                dialog.modal("hide");
                if (data['code'] == 200){
                    //重新加载页面
                    window.location.reload();
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

//编辑轮播图
$(function () {
   $(".edit-banner-btn").click(function (event) {
       var self =$(this);
       event.preventDefault();
       var dialog = $("#banner-dialog");
       dialog.modal("show");

       var tr = self.parent().parent();
       var name = tr.attr("data-name");
       var image_b = tr.attr("data-image");
       var link_url = tr.attr("data-link");
       var priority = tr.attr("data-priority");

        var name_ipt = dialog.find("input[name='name']");
        var image_ipt = dialog.find("input[name='image_b']");
        var link_ipt = dialog.find("input[name='link_url']");
        var priority_ipt = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");

        name_ipt.val(name);
        image_ipt.val(image_b);
        link_ipt.val(link_url);
        priority_ipt.val(+priority);
        console.log(typeof priority);
        saveBtn.attr('data-type','update');
        saveBtn.attr('data-id',tr.attr('data-id'));

   });
});

//删除轮播图
$(function () {
   $(".delete-banner-btn").click(function (event) {
       var self = $(this);
       var tr = self.parent().parent();
       var banner_id = tr.attr("data-id");
       swal({
              title: '确定要删掉吗?',
              text: "",
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              cancelButtonText:'取消',
              confirmButtonText: '确定!'
            }).then((result) => {
              if (result.value) {
                  zzajax.post({
           'url':'/cms/dbanner/',
           'data':{
               'banner_id':banner_id
           },
           'success':function (data) {
               if (data['code']==200){
                   window.location.reload()
               }else {
                   swal({
                          type: 'warning',
                          title:"提示",
                          text:''+data['message']
                    })
               }
           }
       });
              }
        })

   })
});

// 七牛上传图片
$(function () {
       zzqiniu.setUp({
           'domain':'http://pc5nfgg9w.bkt.clouddn.com/',
            'browse_btn':'upload-btn',
            'uptoken_url':'/c/uptoken/',
            'success':function (up,file,info) {
                var image_ipt = $("input[name='image_b']");
                image_ipt.val(file.name)
            }
       })
});