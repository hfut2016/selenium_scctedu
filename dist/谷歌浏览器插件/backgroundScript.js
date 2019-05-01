// let serchNewsUrl = `https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=` ;
let nowUrl =`https://www.baidu.com/s?ie=utf-8&f=8&wd=`;
let serchPageUrl = true; 
chrome.extension.onRequest.addListener(
  function(request, sender, sendResponse) {
	console.log(request)
	chrome.storage.sync.get('searchUrl', function(result) {
		// console.log(result);
		serchPageUrl = result.searchUrl;
		})
	let responseHtml = `
	<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Document</title>
</head>
<body>
  <div class="kw" style=" text-align:left; display:flex; font-size:small;	font-weight:100;"><p id="result_kw"></p></div>
  <div class="kw" style=" text-align: left; display: flex; color:springgreen; border: 1px solid skyblue; font-size:small;	font-weight:100;"><p id="result_qs"></p></div>
  <div class="answer" style="text-align: left; color:dodgerblue; border: 1px solid skyblue;	font-weight:800; font-size:small;"></div>
</body>
</html>`
	chrome.storage.sync.get('enabled', function(result) {  
		let responseData = '';
		// console.log(result)
		if (!result.enabled){
			sendResponse({result: responseData, status:'stop'});
		} else if (serchPageUrl){
			var xhr = new XMLHttpRequest();
			xhr.open("GET", nowUrl + request.selected, true);
			xhr.onreadystatechange = function() {
				if (xhr.readyState == 4) {
					responseData = checkHtml(xhr.responseText);
					sendResponse({result: responseData, status:'search'});
					}
			}
			xhr.send();
		} else {
			var xhr = new XMLHttpRequest();
			xhr.open("GET", 'http://127.0.0.1:10086/?kw=' + request.selected, true);
			xhr.onreadystatechange = function() {
				if (xhr.readyState == 4) {
					if(xhr.status>=200&&xhr.status<300  ||  xhr.status==304){
						responseData = JSON.parse(xhr.responseText);
						myHtml = responseHtml.replace(/id="result_kw">/,`id="result_kw">${responseData.kw}`);
						myHtml = myHtml.replace(/id="result_qs">/,`id="result_qs">${responseData.question}`);
						let temp = ``
						if (responseData.answer.length > 0){
							responseData.answer.forEach(item => {
							temp = `${temp}<p>${item.option}：${item.value}</p>`;
							});
							myHtml = myHtml.replace(/font-size:small;"><\/div>/,`font-size:small;">${temp}</div>`);
						}
						console.log(responseData)
						sendResponse({result: myHtml, status:'copy'});
					} else {
						myHtml = responseHtml.replace(/id="result_kw">/,`id="result_kw">${request.selected}`);
						myHtml = myHtml.replace(/font-size:small;"><\/div>/,`font-size:larger;">请运行本地服务器程序</div>`);
						sendResponse({result: myHtml, status:'copy'});
					}
				}
			}
			xhr.send();
		}
	});
 });
 
 function checkHtml(html) {
	 // console.log(html.match(/\)\);<\/script>[\s\S\w\W\d\D]*?<body link="#0000cc">/g))
	 if (html.match(/#content_left{width:540px;padding-left:121px;padding-top:5px}/g)){
		 return html.replace(/#content_left{width:540px;padding-left:121px;padding-top:5px}/,"#content_left{width:540px;padding-left:1px;padding-top:5px}")
		 .replace(/<a href="\/" id="result_logo" onmousedown=.* alt="到百度首页" title="到百度首页"><\/a>/, myButton)
		 .replace(/\)\);<\/script>[\s\S\w\W\d\D]*?<body link="#0000cc">/, insertScript)
	 } else {
		 return html;
	 }
 }
 
 var myButton = `<p id="result_logo" onmousedown="return c({'fm':'tab','tab':'logo'})">
	<input class="index-logo-src" style="height: 40px;" id="copy-btn" type="button" value="一键复制" title="点击复制到剪贴版">
	<input class="index-logo-srcnew" type="button" value="到百度首页" title="到百度2首页"></p>`
 
 var insertScript = `));</script><script type="text/javascript" data-for="result">
	var copyToTipe = function(obj){
			if(document.getElementById("kw")){
				document.getElementById("kw").select();  
				console.log(document.execCommand("Copy")?'复制成功':'复制失败');
	}}
	var iframeLoad = function(){
		document.getElementById("copy-btn").setAttribute("onclick","copyToTipe(this)")}
	</script></head><body link="#0000cc" onload="iframeLoad()">`


