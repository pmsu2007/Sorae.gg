const renewBtn = document.querySelector('.renewBtn');
let isRenewing = false;
renewBtn.addEventListener('click', function(e) {
    if (isRenewing) return;
    isRenewing = true;
    
    // activate loader and hide text
    renewBtn.firstElementChild.textContent = '';
    let loader = document.querySelector('.spinner-border');
    loader.style.display = "";

    xhr = new XMLHttpRequest();
    xhr.onload = function(e) {
        isRenewing = false;
        if(xhr.status === 200) {
            const res = JSON.parse(xhr.responseText);
            if (res.status == 200) {
                // success
                window.location.reload();
            }
            else {
                alert("프로필 갱신에 실패했습니다.")
                loader.style.display = "none";
                renewBtn.firstChild.textContent= "프로필 갱신";
            }
        } else {
            alert("프로필 갱신에 실패했습니다.")
            loader.style.display = "none";
            renewBtn.firstChild.textContent= "프로필 갱신";
        }
    }

    // data transfer
    xhr.open('POST', '/renew/');
    xhr.setRequestHeader('Content-type', 'application/json');
    const summonerName = document.querySelector('.summonerName').textContent;
    const data = {'userName': summonerName};
    xhr.send(JSON.stringify(data));
});