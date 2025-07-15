import requests

baes_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0'

def get_ultra_srt_ncst(service_key, page_no, num_of_rows, base_date, base_time, nx, ny):
    url = baes_url + '/getUltraSrtNcst'
    params = {
        'ServiceKey': service_key,
        'pageNo': page_no,
        'numOfRows': num_of_rows,
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny,
    }

    response = requests.get(url, params = params)
    return response.json()
