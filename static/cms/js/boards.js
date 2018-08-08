//添加板块
$(function () {
   $('#add_board-btn').click(function (event) {
       event.preventDefault();
       swal({
              title: '请输入模块名称',
              input: 'text',
              showCancelButton: true,
              confirmButtonText: '确定',
              cancelButtonText:'取消',
              showLoaderOnConfirm: true,
              preConfirm: function(text) {
                zzajax.post({
                  'url':'/cms/aboard/',
                  'data':{
                      'name':text
                  },
                  'success':function (data) {
                      if (data['code']==200){
                          window.location.reload();
                      }else {
                          swal({
                              type: 'warning',
                              title:"提示",
                              text:''+data['message']
                            })
                      }
                  }
              })
              },
              allowOutsideClick: false
            });
   })
});


//编辑板块
$(function () {
    $('.edit-board-btn').click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr('data-id');
        swal({
              title: '请输入新模块名称',
              input: 'text',
              showCancelButton: true,
              confirmButtonText: '确定',
              cancelButtonText:'取消',
              inputPlaceholder:name,
              showLoaderOnConfirm: true,
              preConfirm: function(text) {
                zzajax.post({
                  'url':'/cms/uboard/',
                  'data':{
                      'name':text,
                      'board_id':board_id
                  },
                  'success':function (data) {
                      if (data['code']==200){
                          window.location.reload();
                      }else {
                          swal({
                              type: 'warning',
                              title:"提示",
                              text:''+data['message']
                            })
                      }
                  }
              })
              },
              allowOutsideClick: false
            });
    })
});


//删除板块
$(function () {
   $(".delete-board-btn").click(function (event) {
       var self = $(this);
       var tr = self.parent().parent();
       var board_id = tr.attr("data-id");
       var name = tr.attr('data-name');
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
                           'url':'/cms/dboard/',
                           'data':{
                               'board_id':board_id,
                               'name':name
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