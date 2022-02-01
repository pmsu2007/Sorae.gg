from django import template
from datetime import datetime

register = template.Library()

# champion name english to koeran

ENG_TO_KOR = {"Aatrox":"아트록스","Ahri":"아리","Akali":"아칼리","Akshan":"아크샨","Alistar":"알리스타","Amumu":"아무무","Anivia":"애니비아","Annie":"애니","Aphelios":"아펠리오스","Ashe":"애쉬","AurelionSol":"아우렐리온 솔","Azir":"아지르","Bard":"바드","Blitzcrank":"블리츠크랭크","Brand":"브랜드","Braum":"브라움","Caitlyn":"케이틀린","Camille":"카밀","Cassiopeia":"카시오페아","Chogath":"초가스","Corki":"코르키","Darius":"다리우스","Diana":"다이애나","Draven":"드레이븐","DrMundo":"문도 박사","Ekko":"에코","Elise":"엘리스","Evelynn":"이블린","Ezreal":"이즈리얼","Fiddlesticks":"피들스틱","Fiora":"피오라","Fizz":"피즈","Galio":"갈리오","Gangplank":"갱플랭크","Garen":"가렌","Gnar":"나르","Gragas":"그라가스","Graves":"그레이브즈","Gwen":"그웬","Hecarim":"헤카림","Heimerdinger":"하이머딩거","Illaoi":"일라오이","Irelia":"이렐리아","Ivern":"아이번","Janna":"잔나","JarvanIV":"자르반 4세","Jax":"잭스","Jayce":"제이스","Jhin":"진","Jinx":"징크스","Kaisa":"카이사","Kalista":"칼리스타","Karma":"카르마","Karthus":"카서스","Kassadin":"카사딘","Katarina":"카타리나","Kayle":"케일","Kayn":"케인","Kennen":"케넨","Khazix":"카직스","Kindred":"킨드레드","Kled":"클레드","KogMaw":"코그모","Leblanc":"르블랑","LeeSin":"리 신","Leona":"레오나","Lillia":"릴리아","Lissandra":"리산드라","Lucian":"루시안","Lulu":"룰루","Lux":"럭스","Malphite":"말파이트","Malzahar":"말자하","Maokai":"마오카이","MasterYi":"마스터 이","MissFortune":"미스 포츈","MonkeyKing":"오공","Mordekaiser":"모데카이저","Morgana":"모르가나","Nami":"나미","Nasus":"나서스","Nautilus":"노틸러스","Neeko":"니코","Nidalee":"니달리","Nocturne":"녹턴","Nunu":"누누와 윌럼프","Olaf":"올라프","Orianna":"오리아나","Ornn":"오른","Pantheon":"판테온","Poppy":"뽀삐","Pyke":"파이크","Qiyana":"키아나","Quinn":"퀸","Rakan":"라칸","Rammus":"람머스","RekSai":"렉사이","Rell":"렐","Renekton":"레넥톤","Rengar":"렝가","Riven":"리븐","Rumble":"럼블","Ryze":"라이즈","Samira":"사미라","Sejuani":"세주아니","Senna":"세나","Seraphine":"세라핀","Sett":"세트","Shaco":"샤코","Shen":"쉔","Shyvana":"쉬바나","Singed":"신지드","Sion":"사이온","Sivir":"시비르","Skarner":"스카너","Sona":"소나","Soraka":"소라카","Swain":"스웨인","Sylas":"사일러스","Syndra":"신드라","TahmKench":"탐 켄치","Taliyah":"탈리야","Talon":"탈론","Taric":"타릭","Teemo":"티모","Thresh":"쓰레쉬","Tristana":"트리스타나","Trundle":"트런들","Tryndamere":"트린다미어","TwistedFate":"트위스티드 페이트","Twitch":"트위치","Udyr":"우디르","Urgot":"우르곳","Varus":"바루스","Vayne":"베인","Veigar":"베이가","Velkoz":"벨코즈","Vex":"벡스","Vi":"바이","Viego":"비에고","Viktor":"빅토르","Vladimir":"블라디미르","Volibear":"볼리베어","Warwick":"워윅","Xayah":"자야","Xerath":"제라스","XinZhao":"신 짜오","Yasuo":"야스오","Yone":"요네","Yorick":"요릭","Yuumi":"유미","Zac":"자크","Zed":"제드",'Zeri':'제리',"Ziggs":"직스","Zilean":"질리언","Zoe":"조이","Zyra":"자이라",}

# match type dict
MATCH_TYPE = {
    '420':{
        'type':'솔로랭크',
        'map':'소환사의 협곡'
    },
    '430':{
        'type':'일반',
        'map':'소환사의 협곡'
    },
    '440':{
        'type':'자유랭크',
        'map':'소환사의 협곡'
    },
    '450':{
        'type':'칼바람',
        'map':'자유랭크'
    },
    '900':{
        'type':'URF',
        'map':'소환사의 협곡'
    }
}

# special match name
SPECIAL_NAME = "URF"

@register.filter
def eng_to_kor(val):
    return ENG_TO_KOR[val]

@register.filter
def sec_to_min(val):
    val = round(val/60)
    return val

@register.filter
def det_win_lose(val):
    if val:
        return '승리'
    else:
        return '패배'

@register.filter
def det_game_type(val):
    return MATCH_TYPE[str(val)]['type']

@register.filter
def unix_to_date(val):
    val += 3600 * 1000 * 9
    date = datetime.fromtimestamp(int(val)/1000)
    month = date.month
    day = date.day
    return str(month) + '/' + str(day)

@register.filter
def unix_to_full_date(val):
    val += 3600 * 1000 * 9
    date = datetime.fromtimestamp(int(val)/1000)
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute

    return str(year) + '년 ' + str(month) + '월 ' + str(day) + '일 ' + str(hour) + '시 ' \
        + str(minute) + '분'
