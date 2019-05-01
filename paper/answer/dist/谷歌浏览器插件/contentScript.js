
document.body.oncontextmenu = eStart => {
	return true;
	// e.preventDefault();
}

document.body.onmousedown = eStart => {
	//console.log(`划线模式`);
	document.body.onmouseup = eStop =>{
		let diffX = eStart.pageX-eStop.pageX;
		let diffY = eStart.pageY-eStop.pageY;
		// console.log(`start位置x: ${eStart.pageX-eStop.pageX}px; y: ${eStart.pageY-eStop.pageY}px \n
		// stop位置x: ${eStop.pageX}px  y: ${eStop.pageY}px`);
		if (Math.abs(diffX)>2 | Math.abs(diffY)>2){
			inserScript(eStop);
		} else if(!window.getSelection().toString()){
			removeCopy();
		}
	}
	
	return true;
	// e.preventDefault();
};

var inserScript = function(e){
	chrome.extension.sendRequest({
		selected:window.getSelection().toString()
		}, 
		function(response) {
			if (response.status === 'stop'){
				//console.log("插件未启用")
			}else if (response.status === 'copy'){
				copyPage(response,e.pageX, e.pageY);
			} else {
				baiduPage(response);
			}
	})	
}

var baiduPage = function(response){
	removeCopy();
	var iframe = document.createElement('iframe'); //动态创建框架
	iframe.setAttribute("style",`z-index:1;position: fixed;right: 0 !important; bottom: 100px !important; width: 33% !important; height: 75% !important;`);
	iframe.setAttribute("id","baidu-result");
	iframe.srcdoc=response.result;            //框架中加载的页面
	document.body.appendChild(iframe);
}

var copyPage = function(response,x,y){
	removeCopy();
	// let x = location.right < 800 ? location.right + 20 : location.left + 250;
	// let y = location.top < 200 ? location.top + 20 : location.top - 66;
	//console.log(`实际位置left: ${x}px; top: ${y}px \n光标位置left: ${location.right}px  top: ${location.top}px`);
	//console.log(`实际位置left: ${x}px; top: ${y}px \n光标位置left: ${location.x}px  top: ${location.y}px`);
	var iframe = document.createElement('iframe'); //动态创建框架
	iframe.setAttribute("style",`z-index:1;position: fixed;right: ${9}% !important; top: ${14}% !important; width: 24% !important; height: 60% `);
	iframe.setAttribute("id","baidu-result");
	iframe.setAttribute("frameborder","no");
	iframe.srcdoc=response.result;            //框架中加载的页面
	document.body.appendChild(iframe);
}

var removeCopy = function(){
	let node_data = document.getElementById("baidu-result");
		if(node_data){
			//console.log('即将移除元素',node_data.id);
			document.body.removeChild(node_data);
		};
}
