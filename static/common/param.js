var zzparam = {
    setParam: function (href,key,value) {
        //重新加载整个界面
        var isReplaced = false;
        var urlArray = href.split('?');
        if(urlArray.length > 1){
            var queryArray = urlArray[1].split('&');
            for(var i=0;i<queryArray.length;i++){
                var paramsArray = queryArray[i].split('=');
                if(paramsArray[0] == key){
                    paramsArray[1] = value;
                    queryArray[i] = paramsArray.join('=');
                    isReplaced = true;
                    break;
                }
            }
            if(!isReplaced){
                var params = {};
                params[key] = value;
                if(urlArray.length > 1){
                    href = href + '&' + $.params(params);
                }else{
                    href = href +'?'+$.params(params);
                }
            }else {
                var params = queryArray.join('&');
                urlArray[1] = params;
                href = urlArray.join('?');
            }
        }else {
            var param = {};
            param[key] = value;
            if(urlArray.length > 1){
                href = href + '&' + $.param(param);
            }else {
                href = href + '?' + $.param(param);
            }
        }
        return href;
    }
};