function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const renewBtn = document.querySelector('.renewBtn');
let isRenewing = false;
renewBtn.addEventListener('click', function(e) {
    if (isRenewing) return; // if profile is renewing then return
    isRenewing = true;
    
    // activate loader and hide text
    renewBtn.firstElementChild.textContent = '';
    let loader = document.querySelector('.spinner-border');
    loader.style.display = "";

    xhr = new XMLHttpRequest();
    xhr.onload = function(e) {
        isRenewing = false;
        if(xhr.status === 200) {
            const res = JSON.parse(xhr.response);
            
            if (res.status == 200) {
                // success
                // window.location.reload();
                alert("프로필 갱신을 완료했습니다.");
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
    xhr.open('POST', './');
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    const summonerName = document.querySelector('.summonerName').textContent;
    const data = {'userName': summonerName};
    xhr.send(JSON.stringify(data));
});