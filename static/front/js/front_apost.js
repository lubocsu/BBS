$(function () {
    var ue = UE.getEditor("editor",{
        "serverUrl":'/ueditor/upload/'
    });
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var title_inp = $('input[name="title"]');
        var boardSelect = $('select[name="board_id"]');

        var title = title_inp.val();
        var board_id = boardSelect.val();
        var content = ue.getContent();

        zzajax.post({
            'url':'/apost/',
            'data':{
                'title':title,
                'board_id':board_id,
                'content':content
            },
            'success':function (data) {
                if (data['code']==200){
                    // swal({
                    //   title: '帖子发表成功！',
                    //   text: '',
                    //   type: 'warning',
                    //   showCancelButton: true,
                    //   confirmButtonColor: '#3085d6',
                    //   cancelButtonColor: '#d33',
                    //   confirmButtonText: '再发一篇',
                    //   cancelButtonText: '回到首页',
                    //   confirmButtonClass: 'btn btn-success',
                    //   cancelButtonClass: 'btn btn-danger',
                    //   buttonsStyling: false
                    // }).then(function() {
                    //   // title_inp.val('');
                    //   // ue.setContent('');
                    //   window.location = '/'
                    // }, function(dismiss) {
                    //   // dismiss的值可以是'cancel', 'overlay',
                    //   // 'close', 'timer'
                    //   if (dismiss == 'cancel') {
                    //    // window.location = '/'
                    //       title_inp.val('');
                    //       ue.setContent('');
                    //   }
                    // })
                    const swalWithBootstrapButtons = swal.mixin({
                          confirmButtonClass: 'btn btn-success',
                          cancelButtonClass: 'btn btn-danger',
                          buttonsStyling: false,
                        });

                        swalWithBootstrapButtons({
                          title: '发布成功',
                          text: "",
                          type: 'success',
                          showCancelButton: true,
                          confirmButtonText: '再发一篇',
                          cancelButtonText: '回到首页',
                          reverseButtons: true
                        }).then((result) => {
                          if (result.value) {

                              title_inp.val('');
                              ue.setContent('');

                          } else if (
                            // Read more about handling dismissals
                            result.dismiss === swal.DismissReason.cancel
                          ) {

                              window.location = '/';

                          }
                        })


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