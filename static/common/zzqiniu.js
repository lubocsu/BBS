'use strict';
var zzqiniu = {
        'setUp':function (args) {
            var domain = args['domain'];
            var parmas = {
                browse_button:args['browse_btn'],
                runtimes:'html5,flash,html4',
                max_file_size : '500mb',
                dragdrop:false,
                chunk_size:'4mb',
                uptoken_url:args['uptoken_url'],
                domain: domain,
                get_new_uptoken: false,
                auto_start: true,
                unique_names: true,
                multi_selection:false,
                filters:{
                    mime_type:[
                        {title : "Video files", extensions : "flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,m4v,mp4"},
                        {title : "Image files", extensions : "jpg,gif,png"}], // 限定jpg,gif,png后缀上传,限定flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,m4v,mp4后缀格式上传
            },
                log_level:5,
                init:{
                    'FileUploaded':function (up,file,info) {
                        if(args['success']){
                            var success = args['success'];
                            file.name = domain + file.target_name;
                            success(up,file,info);
                        }
                    },
                     'Error': function(up, err, errTip) {
                      //上传出错时,处理相关的事情
                         if(args['error']){
                             var error = args['error'];
                             error(up,err,errTip)
                         }
                    },
                    'UploadProgress':function (up,file) {
                        if(args['progress']){
                            args['progress'](up,file);
                        }
                    },
                    'FilesAdded':function (up,file) {
                        if(args['fileadded']){
                            args['fileadded'](up,file);
                        }
                    },
                    'UploadComplete':function () {
                        if(args['complete']){
                            args['complete'](up,file);
                        }
                    },
                }
            };
            //把args中的参数放到params中去
            for (var key in args){
                parmas[key] = args[key];
            }
            var uploader = Qiniu.uploader(parmas);
            return uploader;

        }
};