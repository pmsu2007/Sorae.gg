// coloring card! win -> royalblue, lose -> crimson
const CHAMP_URL ="https://ddragon.leagueoflegends.com/cdn/12.3.1/img/champion/";
const SPELL_URL ="https://ddragon.leagueoflegends.com/cdn/12.3.1/img/spell/";
const SPELL_DICT = {
'21': 'SummonerBarrier',
'1': 'SummonerBoost',
'14': 'SummonerDot',
'3': 'SummonerExhaust',
'4': 'SummonerFlash',
'6': 'SummonerHaste',
'7': 'SummonerHeal',
'13': 'SummonerMana',
'30': 'SummonerPoroRecall',
'31': 'SummonerPoroThrow',
'11': 'SummonerSmite',
'39': 'SummonerSnowURFSnowball_Mark',
'32': 'SummonerSnowball',
'12': 'SummonerTeleport',
'54': 'Summoner_UltBookPlaceholder',
'55': 'Summoner_UltBookSmitePlaceholder',
}

/*
룬 정보
8000 : 정밀 (2)
8100 : 지배 (0)
8200 : 마법 (4)
8300 : 영감 (1)
8400 : 결의 (3)
*/

const RUNE_DICT = {
    '8000':2,
    '8100':0,
    '8200':4,
    '8300':1,
    '8400':3, 
}

var ITEM_DATA;
var SPELL_DATA;
var RUNE_DATA;

fetch(STATIC_URL + 'js/item.json')
.then (response => response.json())
.then(
    data => ITEM_DATA = data
)
fetch(STATIC_URL + 'js/summoner.json')
.then (response => response.json())
.then(
    data => SPELL_DATA = data
)
fetch(STATIC_URL + 'js/runesReforged.json')
.then (response => response.json())
.then(
    data => RUNE_DATA = data
)


const cards = document.querySelectorAll('.card');
const detailContainer = document.querySelector('.detail-container');
const records = document.querySelector('.record');


[...cards].forEach(card => {
    if (card.dataset.result == 'True') {
        card.classList.add('card-win');
    } else {
        card.classList.add('card-lose');
    }
});


const getDetail = function(matchID, matchTime) {
    url = '/detail/' + '?matchID=' +  matchID

    const MATCH_MIN =  matchTime / 60;
    
    fetch(url)
    .then(res => res.json())
    .then(
        json => {
            detailContainer.innerHTML = json.data;
        }
    )
    .then (
        () => {
            detailContainer.dataset.matchId = matchID;
            const gameDuration = detailContainer.querySelector('.game-duration');
            let durMin = parseInt(MATCH_MIN);
            let durSec = matchTime - durMin * 60;
            gameDuration.textContent = durMin + '분 ' + durSec + '초';
            detailContainer.querySelectorAll('.game-result').forEach( elem => {
                if (elem.textContent === "승리") elem.style.color = "royalblue";
                else elem.style.color = "crimson";
            })
        })
    .then (
        // set champion image
        () => {
            const championImg = detailContainer.querySelectorAll('.img-level img');
            championImg.forEach(img => {
                img.src = STATIC_URL + 'images/champion/' + img.alt +'.png';
            });
        }
    )
    .then (
        // spell manipulation
        () => {
            const spells = detailContainer.querySelectorAll('.spell');
            spells.forEach(spell => {
                const spellName = SPELL_DICT[spell.dataset.id];
                spell.src = SPELL_URL + spellName  + '.png';
                // spell tooltip
                spell.dataset.tippyContent = '<tooltipName>' + SPELL_DATA['data'][spellName]['name'] + '</tooltipName>' 
                + '<br><br>'
                + SPELL_DATA['data'][spellName]['description'];
            })
        }
    )
    .then (
        // rune manipulation
        () => {
            // sub rune setting
            const subRunes = detailContainer.querySelectorAll('.s-rune');
            subRunes.forEach(rune => {
                rune.src = STATIC_URL + 'images/' + RUNE_DATA[RUNE_DICT[rune.dataset.id]].icon;
                rune.dataset.tippyContent = '<tooltipName>' + RUNE_DATA[RUNE_DICT[rune.dataset.id]].name + '</tooltipName>' + '<br><br>';
                // sub rune1, sub rune2 tooltip setting
                const slots = RUNE_DATA[RUNE_DICT[rune.dataset.id]].slots;
                let rune1Complete = false;
                let rune2Complete = false;
                slots.forEach(slot => {
                    slot.runes.forEach(r => {
                        if (r.id == rune.dataset.rune1) {
                            rune.dataset.tippyContent += '<tooltipName>' + r.name + '</tooltipName>'
                            + '<br>' + r.shortDesc + '<br><br>';
                            rune1Complete = true;
                        } else if (r.id == rune.dataset.rune2) {
                            rune.dataset.tippyContent += '<tooltipName>' + r.name + '</tooltipName>'
                            + '<br>' + r.shortDesc +'<br><br>';
                            rune2Complete = true;
                        }
                        if (rune1Complete && rune2Complete){
                            rune.dataset.tippyContent = rune.dataset.tippyContent.slice(0, -4);
                            return false;
                        }
                    })
                    if (rune1Complete && rune2Complete) return false;
                })
            })
            // primary rune setting
            const primaryRunes = detailContainer.querySelectorAll('.p-rune');
            primaryRunes.forEach(rune => {
                for (let i = 0; i < 5; i++) {
                const slot = RUNE_DATA[i].slots[0].runes;
                slot.forEach(r => {
                    if (r.id == rune.dataset.id) {
                        rune.src = STATIC_URL + 'images/' + r.icon;
                        // primary rune tooltip
                        rune.dataset.tippyContent = '<tooltipName>' + r.name + '</tooltipName>'
                        + '<br><br>' + r.shortDesc + r.longDesc;
                        return false;
                    }
                })
            }
            })
        }
    )
    .then (            
        // KDA manipulation
        () => {

            const redTeam = document.querySelector('.red-team');
            const blueTeam = document.querySelector('.blue-team');
            
            blueTotalKill = 0;
            redTotalKill = 0;

            blueTeam.querySelectorAll('.kda-num').forEach(elem => {
                let kda = elem.nextElementSibling.firstElementChild.textContent.split('/');
                blueTotalKill += parseInt(kda[0]);
                let kdaNum = (parseInt(kda[0]) + parseInt(kda[2])) / parseInt(kda[1]);
                if (kdaNum !== Infinity && !isNaN(kdaNum)) {
                kdaNum = kdaNum.toFixed(2);
                elem.textContent = kdaNum + ':1';
                if (kdaNum >= 5) elem.classList.add('highlight2');
                else if (kdaNum >= 4) elem.classList.add('highlight3');
                else if (kdaNum >= 3) elem.classList.add('highlight4');
                else if (kdaNum < 2) elem.classList.add('highlight5'); 
                } else if (isNaN(kdaNum)) {
                    elem.textContent = '0.00:1';
                    elem.classList.add('highlight5');
                } else {
                    elem.textContent = 'Perfect';
                    elem.classList.add('highlight1');
                }
            })
            redTeam.querySelectorAll('.kda-num').forEach(elem => {
                let kda = elem.nextElementSibling.firstElementChild.textContent.split('/');
                redTotalKill += parseInt(kda[0]);
                let kdaNum = (parseInt(kda[0]) + parseInt(kda[2])) / parseInt(kda[1]);
                if (kdaNum !== Infinity && !isNaN(kdaNum)) {
                    kdaNum = kdaNum.toFixed(2);
                    elem.textContent = kdaNum + ':1';
                    if (kdaNum >= 5) elem.classList.add('highlight2');
                    else if (kdaNum >= 4) elem.classList.add('highlight3');
                    else if (kdaNum >= 3) elem.classList.add('highlight4');
                    else elem.classList.add('highlight5'); 
                    } else if (isNaN(kdaNum)) {
                        elem.textContent = '0.00:1';
                        elem.classList.add('highlight5');
                    } else {
                        elem.textContent = 'Perfect';
                        elem.classList.add('highlight1');
                    } 
            })
            blueTeam.querySelectorAll('.kda-detail').forEach(elem => {
                let kda = elem.firstElementChild.textContent.split('/');
                let killParticipation = blueTotalKill != 0 ? Math.round(100 * (parseInt(kda[0]) + parseInt(kda[2])) / blueTotalKill) : 0;
                killPartElem = elem.firstElementChild.nextElementSibling;
                killPartElem.textContent = '(' + killParticipation + '%)';
                if (killParticipation >= 80) killPartElem.classList.add('highlight1');
                else if (killParticipation >= 70) killPartElem.classList.add('highlight2');
                else if (killParticipation >= 60) killPartElem.classList.add('highlight4');
                else if (killParticipation < 50) killPartElem.classList.add('highlight5');
            })
            redTeam.querySelectorAll('.kda-detail').forEach(elem => {
                let kda = elem.firstElementChild.textContent.split('/');
                let killParticipation = redTotalKill != 0 ? Math.round(100 * (parseInt(kda[0]) + parseInt(kda[2])) / redTotalKill) : 0;
                killPartElem = elem.firstElementChild.nextElementSibling;
                killPartElem.textContent = '(' + killParticipation + '%)';
                if (killParticipation >= 80) killPartElem.classList.add('highlight1');
                else if (killParticipation >= 70) killPartElem.classList.add('highlight2');
                else if (killParticipation >= 60) killPartElem.classList.add('highlight4');
                else if (killParticipation < 50) killPartElem.classList.add('highlight5');
            })
        })
    .then (
        // damage manipulation
        () => {
            let damages = detailContainer.querySelectorAll('.damage-info');
            damages = [...damages];
            damages.sort((a, b) => {
                let aDamage = parseInt(a.firstElementChild.dataset.val);
                let bDamage = parseInt(b.firstElementChild.dataset.val);
                return bDamage - aDamage;
            })
            let counter = 1;
            let maximumDamage = parseInt(damages[0].firstElementChild.dataset.val);
            damages.forEach(elem => {
                // 등수 표시 및 그래프
                elem.firstElementChild.nextElementSibling.textContent = counter + '등';
                counter++;
                let damageRatio = parseInt(parseInt(elem.firstElementChild.dataset.val) / maximumDamage * 100);
                const fill = elem.querySelector('.fill');
                fill.style.width = damageRatio.toString() + '%';
                
            })
            for (let i = 1; i <= 3; i++) {
                // 1 ~ 3등 강조
                damages[i - 1].classList.add('highlight' + i);
            }

        }
    )
    .then (
        // vision score manipulation
        () => {
            const visions = detailContainer.querySelectorAll('.vision-info');
            visions.forEach(elem => {
                const visionScore = parseInt(elem.firstElementChild.textContent);
                let visionPerMin = visionScore / MATCH_MIN;
                visionPerMin = visionPerMin.toFixed(2);
                const visionPerMinElem = elem.firstElementChild.nextElementSibling;
                visionPerMinElem.textContent = visionPerMin + ' vision/분';

                if (visionPerMin >= 3) visionPerMinElem.classList.add('highlight1');
                else if (visionPerMin >= 2.5) visionPerMinElem.classList.add('highlight2');
                else if (visionPerMin >= 2) visionPerMinElem.classList.add('highlight3');
                else if (visionPerMin >= 1.5) visionPerMinElem.classList.add('highlight4');
                else if (visionPerMin < 1) visionPerMinElem.classList.add('highlight5');
            })
        }
    )
    .then (
        // cs manipulation 
        () => {
            const csElems = detailContainer.querySelectorAll('.cs-info');
            csElems.forEach(elem => {
                const cs = parseInt(elem.firstElementChild.textContent);
                let csPerMin = cs / MATCH_MIN;
                csPerMin = csPerMin.toFixed(1);
                const csPerMinElem = elem.firstElementChild.nextElementSibling;
                csPerMinElem.textContent = csPerMin + 'cs/분';

                if (csPerMin >= 9) csPerMinElem.classList.add('highlight1');
                else if (csPerMin >= 8) csPerMinElem.classList.add('highlight3');
                else if (csPerMin >= 7) csPerMinElem.classList.add('highlight4');
                else if (csPerMin < 6) csPerMinElem.classList.add('highlight5');
            })
        }
    )
    .then (
        // item tooltip
        () => {
            itemImgs = detailContainer.querySelectorAll('.items img');
            itemImgs.forEach(item => {
                item.dataset.tippyContent = '<tooltipName>' + ITEM_DATA['data'][item.dataset.id]['name'] + '</tooltipName>'
                +'<br><br>'
                + ITEM_DATA['data'][item.dataset.id]['description']
                + ITEM_DATA['data'][item.dataset.id]['plaintext']
            })
        }
    )
    .then (
        // 팀내 왕관 씌우기 kda, 딜량, 시야점수
        () => {
            // 킬관여 왕관
            // blue team
            const blueTeam = detailContainer.querySelector('.blue-team');
            let kdaInfos = blueTeam.querySelectorAll('.kda-info');
            kdaInfos = [...kdaInfos];
            kdaInfos.sort((a, b) => {
                let aKP = parseInt(a.querySelector('.kill-participation').textContent.slice(1, -2));  
                let bKP = parseInt(b.querySelector('.kill-participation').textContent.slice(1, -2));
                return bKP - aKP;
            })
            let maxKP =  parseInt(kdaInfos[0].querySelector('.kill-participation').textContent.slice(1, -2));
            let blackCrown = kdaInfos[0].querySelector('.black-crown');
            blackCrown.style.display = 'inline';
            blackCrown.dataset.tippyContent += '팀내 최다 킬관여<br>'
            let idx = 1;
            while (idx < kdaInfos.length) {
                let curKP = parseInt(kdaInfos[idx].querySelector('.kill-participation').textContent.slice(1, -2));
                if (maxKP !== curKP) break;
                blackCrown = kdaInfos[idx].querySelector('.black-crown');
                blackCrown.style.display = 'inline';
                blackCrown.dataset.tippyContent += '팀내 최다 킬관여<br>'
                idx++;
            }

            // red team
            const redTeam = detailContainer.querySelector('.red-team');
            kdaInfos = redTeam.querySelectorAll('.kda-info');
            kdaInfos = [...kdaInfos];
            kdaInfos.sort((a, b) => {
                let aKP = parseInt(a.querySelector('.kill-participation').textContent.slice(1, -2));  
                let bKP = parseInt(b.querySelector('.kill-participation').textContent.slice(1, -2));
                return bKP - aKP;
            })
            maxKP =  parseInt(kdaInfos[0].querySelector('.kill-participation').textContent.slice(1, -2));
            blackCrown = kdaInfos[0].querySelector('.black-crown');
            blackCrown.style.display = 'inline';
            blackCrown.dataset.tippyContent += '팀내 최다 킬관여<br>'
            idx = 1;
            while (idx < kdaInfos.length) {
                let curKP = parseInt(kdaInfos[idx].querySelector('.kill-participation').textContent.slice(1, -2));
                if (maxKP !== curKP) break;
                blackCrown = kdaInfos[idx].querySelector('.black-crown');
                blackCrown.style.display = 'inline';
                blackCrown.dataset.tippyContent += '팀내 최다 킬관여<br>'
                idx++;
            }

            // 딜량 왕관

            // blue team
            let damageInfos = blueTeam.querySelectorAll('.damage-info');
            damageInfos = [...damageInfos];
            damageInfos.sort((a, b) => {
                let aDamage = parseInt(a.firstElementChild.dataset.val);  
                let bDamage = parseInt(b.firstElementChild.dataset.val); 
                return bDamage - aDamage;
            })
            let maxDamage = parseInt(damageInfos[0].firstElementChild.dataset.val);
            blackCrown = damageInfos[0].querySelector('.black-crown');
            blackCrown.style.display = 'inline';
            blackCrown.dataset.tippyContent += '팀내 최다 딜량<br>';
            idx = 1;
            while (idx < damageInfos.length) {
                let curDamage = parseInt(damageInfos[idx].firstElementChild.dataset.val);
                if (maxDamage !== curDamage) break;
                blackCrown = damageInfos[idx].querySelector('.black-crown');
                blackCrown.style.display = 'inline';
                blackCrown.dataset.tippyContent += '팀내 최다 딜량<br>';
                idx++;
            }

            // red team
            damageInfos = redTeam.querySelectorAll('.damage-info');
            damageInfos = [...damageInfos];
            damageInfos.sort((a, b) => {
                let aDamage = parseInt(a.firstElementChild.dataset.val);  
                let bDamage = parseInt(b.firstElementChild.dataset.val); 
                return bDamage - aDamage;
            })
            maxDamage = parseInt(damageInfos[0].firstElementChild.dataset.val);
            blackCrown = damageInfos[0].querySelector('.black-crown');
            blackCrown.style.display = 'inline';
            blackCrown.dataset.tippyContent += '팀내 최다 딜량<br>';
            idx = 1;
            while (idx < damageInfos.length) {
                let curDamage = parseInt(damageInfos[idx].firstElementChild.dataset.val);
                if (maxDamage !== curDamage) break;
                blackCrown = damageInfos[idx].querySelector('.black-crown');
                blackCrown.style.display = 'inline';
                blackCrown.dataset.tippyContent += '팀내 최다 딜량<br>';
                idx++;
            }

            // 시야 점수 왕관

            // blue team
            let visionInfos = blueTeam.querySelectorAll('.vision-info');
            visionInfos = [...visionInfos];
            visionInfos.sort((a, b) => {
                let aVS = parseInt(a.firstElementChild.textContent);
                let bVS = parseInt(b.firstElementChild.textContent);
                return bVS - aVS;
            })
            let maxVS = parseInt(visionInfos[0].firstElementChild.textContent);
            blackCrown = visionInfos[0].querySelector('.black-crown');
            blackCrown.style.display = 'inline';
            blackCrown.dataset.tippyContent += '팀내 최다 시야점수<br>';
            idx = 1;
            while (idx < visionInfos.length) {
                let curVS = parseInt(visionInfos[idx].firstElementChild.textContent);
                if (maxVS !== curVS) break;
                blackCrown = visionInfos[idx].querySelector('.black-crown');
                blackCrown.style.display = 'inline';
                blackCrown.dataset.tippyContent += '팀내 최다 시야점수<br>';
                idx++;
            }

            // red team
            visionInfos = redTeam.querySelectorAll('.vision-info');
            visionInfos = [...visionInfos];
            visionInfos.sort((a, b) => {
                let aVS = parseInt(a.firstElementChild.textContent);
                let bVS = parseInt(b.firstElementChild.textContent);
                return bVS - aVS;
            })
            maxVS = parseInt(visionInfos[0].firstElementChild.textContent);
            blackCrown = visionInfos[0].querySelector('.black-crown');
            blackCrown.style.display = 'inline';
            blackCrown.dataset.tippyContent += '팀내 최다 시야점수<br>';
            idx = 1;
            while (idx < visionInfos.length) {
                let curVS = parseInt(visionInfos[idx].firstElementChild.textContent);
                if (maxVS !== curVS) break;
                blackCrown = visionInfos[idx].querySelector('.black-crown');
                blackCrown.style.display = 'inline';
                blackCrown.dataset.tippyContent += '팀내 최다 시야점수<br>';
                idx++;
            }

            // CS 왕관

            // blue team
            let csInfos = blueTeam.querySelectorAll('.cs-info');
            csInfos = [...csInfos];
            csInfos.sort((a, b) =>  {
                let aCS = parseInt(a.firstElementChild.textContent);
                let bCS = parseInt(b.firstElementChild.textContent);
                return bCS - aCS;
            })
            let maxCS = parseInt(csInfos[0].firstElementChild.textContent);
            blackCrown = csInfos[0].querySelector('.black-crown');
            blackCrown.style.display = 'inline';
            blackCrown.dataset.tippyContent += '팀내 최다 CS<br>';
            idx = 1;
            while (idx < csInfos.length) {
                let curCS = parseInt(csInfos[idx].firstElementChild.textContent);
                if (maxCS !== curCS) break;
                blackCrown = csInfos[idx].querySelector('.black-crown');
                blackCrown.style.display = 'inline';
                blackCrown.dataset.tippyContent += '팀내 최다 CS<br>';
                idx++;
            }

            // red team
            csInfos = redTeam.querySelectorAll('.cs-info');
            csInfos = [...csInfos];
            csInfos.sort((a, b) =>  {
                let aCS = parseInt(a.firstElementChild.textContent);
                let bCS = parseInt(b.firstElementChild.textContent);
                return bCS - aCS;
            })
            maxCS = parseInt(csInfos[0].firstElementChild.textContent);
            blackCrown = csInfos[0].querySelector('.black-crown');
            blackCrown.style.display = 'inline';
            blackCrown.dataset.tippyContent += '팀내 최다 CS<br>';
            idx = 1;
            while (idx < csInfos.length) {
                let curCS = parseInt(csInfos[idx].firstElementChild.textContent);
                if (maxCS !== curCS) break;
                blackCrown = csInfos[idx].querySelector('.black-crown');
                blackCrown.style.display = 'inline';
                blackCrown.dataset.tippyContent += '팀내 최다 CS<br>';
                idx++;
            }
        }
    )
    .then (
        // tooltip on
        () => {
            $(function () {
                $(".tooltip-div").tooltip();
            });
            const config = {
                arrow: true,
                flipOnUpdate: true,
                interactive: false,
                boundary: 'viewport',
                // popperOptions: {
                //    placement: 'auto'
                // },
                placement: 'auto',
                theme: 'light-border',
                zIndex: 999999
            };
            
            tippy('[data-tippy-content]', config);
        }
        
    )
    .catch(
        function(error) {
            alert('세부전적 불러오기에 실패했습니다.')
            console.log(error);
        }
    )
    


}



records.addEventListener('click', function (e) {
    let card = e.target.closest('.card');
    if (!card) return;
    if (!records.contains(card)) return;

    if (card.dataset.matchId == detailContainer.dataset.matchId &&
        detailContainer.style.display == 'block') {
        detailContainer.style.display = 'none';
        return;
    } else if (detailContainer.style.display == 'block') {
        detailContainer.display == 'block';
    } else {
        detailContainer.style.display = 'block';
    }

    getDetail(card.dataset['matchId'], card.dataset['matchTime']);
    
});


// tooltip initial

$(function () {
    $(".tooltip-div").tooltip();
});

