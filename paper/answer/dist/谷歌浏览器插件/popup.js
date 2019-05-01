var gb = {
    enabled: true,
    searchUrl: true
};

function enableToggle() {
    gb.enabled = !gb.enabled;

    chrome.storage.sync.set({
        'enabled': gb.enabled
    }, function() {});

    updateHtml();
}
function enableUrlBtn() {
    gb.searchUrl = !gb.searchUrl;

    chrome.storage.sync.set({
        'searchUrl': gb.searchUrl
    }, function() {});

    updateHtml();
}

function updateHtml() {
    document.getElementById('enableBtn').className = gb.enabled ?
            'enabled' : 'disabled';
    document.getElementById('enableVal').innerHTML = gb.enabled ? '已' : '未';
    document.getElementById('selectBtn').className = gb.searchUrl ?
            'enabled' : 'disabled';
    document.getElementById('selectBtn').innerHTML = gb.searchUrl ? '百度' : '复制';
    chrome.browserAction.setIcon({
        path: 'handian48' + (gb.enabled ? '' : '-disabled') + '.png'
    });
}

window.onload = function() {
    var check = document.getElementById('enableBtn');
    check.addEventListener('click', enableToggle, false);
    var check = document.getElementById('selectBtn');
    check.addEventListener('click', enableUrlBtn, false);
    
    chrome.storage.sync.get('enabled', function(result) {
        gb.enabled = result.enabled;
        updateHtml();
    });
    chrome.storage.sync.get('searchUrl', function(result) {
        gb.searchUrl = result.searchUrl;
        updateHtml();
    });
}
