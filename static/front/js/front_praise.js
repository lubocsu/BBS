/* @author:Romey
	 * 动态点赞
	 * 此效果包含css3，部分浏览器不兼容（如：IE10以下的版本）
	*/
	$(function(){
		$("#praise").click(function(){
			var praise_img = $("#praise-img");
			var text_box = $("#add-num");
			var praise_txt = $("#praise-txt");
			var num=parseInt(praise_txt.text());
			if(praise_img.attr("src") == ("/static/images/yizan.png")||praise_img.attr("src") ==("http://127.0.0.1:5000/static/images/yizan.png") ){

				var post_id=$('.praise').attr("data-id");
				var fuser_id = $('.praise').attr("data-fuser");
				zzajax.post({
					'url':'/c_praise/',
					'data':{
						'post_id':post_id,
						'fuser_id':fuser_id
					},
					'success':function (data) {
						if (data['code']==200){
							$('#praise-img').attr("src","http://127.0.0.1:5000/static/images/zan.png");
							praise_txt.removeClass("hover");
							text_box.show().html("<em class='add-animation'>-1</em>");
							$(".add-animation").removeClass("hover");
							num -=1;
							praise_txt.text(num);
						} else {
							swal({
								  type: 'warning',
								  title:"提示",
								  text:''+data['message']
							})
						}
                    }
				})

			}else{
				var post_id=$('.praise').attr("data-id");
				var fuser_id = $('.praise').attr("data-fuser");
				zzajax.post({
					'url':'/praise/',
					'data':{
						'post_id':post_id,
						'fuser_id':fuser_id
					},
					'success':function (data) {
						if (data['code']==200){
							$('#praise-img').attr("src","http://127.0.0.1:5000/static/images/yizan.png");
							praise_txt.addClass("hover");
							text_box.show().html("<em class='add-animation'>+1</em>");
							$(".add-animation").addClass("hover");
							num +=1;
							praise_txt.text(num);
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
		});
	});