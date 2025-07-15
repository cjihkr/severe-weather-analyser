from dotenv import dotenv_values
from datetime import datetime, timedelta
from modules import weatherdata

config = dotenv_values('.env')
api_key = config['API_KEY']

gyeongsangnamdo_grids = {
    '창원시': (71, 102),
    '진주시': (77, 107),
    '통영시': (84, 87),
    '사천시': (75, 92),
    '김해시': (83, 108),
    '밀양시': (85, 108),
    '거제시': (87, 83),
    '양산시': (89, 110),
    '의령군': (74, 111),
    '함안군': (79, 103),
    '창녕군': (79, 108),
    '고성군': (87, 80),
    '하동군': (67, 96),
    '남해군': (68, 82),
    '산청군': (77, 101),
    '함양군': (74, 100),
    '거창군': (72, 94),
    '합천군': (79, 104),
}

def extract_api_response(res):
    data = {}
    for item in res:
        category = item['category']
        value = item['obsrValue']
        data[category] = float(value)
    return data

def calculate_dust_probability(vec, wsd, hour):
    if 290 <= vec <= 360: # 북서풍
        dir_score = 55
    elif 250 <= vec < 290: # 서풍
        dir_score = 37
    elif 180 <= vec < 250:
        dir_score = 18 # 남서풍
    else:
        dir_score = 5

    if wsd >= 8:
        speed_score = 35
    elif wsd >= 4:
        speed_score = 20
    elif wsd >= 2:
        speed_score = 8
    else:
        speed_score = 2

    if 9 <= hour <= 18:
        time_bonus = 10
    else:
        time_bonus = 3

    total_score = dir_score + speed_score + time_bonus
    probability = str(min(total_score, 100))

    return probability

def main():
    while True:
        region = input('황사를 예측할 지역명을 입력해 주세요. 경상남도 내 지역만 지원해요. (예: 고성군)\n지역명: ').strip()
        if region in gyeongsangnamdo_grids:
            break
        else:
            print('지역명이 잘못되었어요. 다시 입력해 주세요.')
            continue

    nx, ny = gyeongsangnamdo_grids[region]
    now = datetime.now() - timedelta(hours = 1)
    date = now.strftime('%Y%m%d')
    time = now.strftime('%H00')
    hour = int(now.strftime('%H'))

    weather = extract_api_response(weatherdata.get_ultra_srt_ncst(api_key, 1, 8, date, time, nx, ny)['response']['body']['items']['item'])
    vec = weather['VEC']
    wsd = weather['WSD']

    p = calculate_dust_probability(vec, wsd, hour)
    print('====================\n입력하신 지역의 황사 확률은 ' + p + '%예요!')

main()
