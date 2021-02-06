from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import math

region_hk = [
    ["Chai_wan", 100404],
    ["Heng_fa_chuen", 100407],
    ["Shau_kei_wan", 100406],
    ["Sai_wan_ho_tai_koo", 100405],
    ["Quarry_bay", 100403],
    ["North_point_fortress_hill", 100401],
    ["Braemar_hill_north_point_mid_level", 100402],
    ["Jardines_lookout_tai_hang", 100201],
    ["Happy_valley_mid_level_east", 100202],
    ["Wan_chai_causeway_bay", 100203],
    ["Tin_hau", 100204],
    ["Central_mid_level_admiralty", 100101],
    ["Sheung_wan_central", 100104],
    ["Hong_kong_west", 100102],
    ["Western_mid_levels", 100103],
    ["The_peak", 100105],
    ["Residence_bel_air_pokfulam", 100303],
    ["Ap_lei_chau", 100305],
    ["Aberdeen_wong_chuk_hang", 100304],
    ["Repulse_bay_shou_son_hill", 100301],
    ["Tai_tam_shek_o", 100306],
    ["Stanley", 100302]
]

region_kowloon = [
    ["Tsim_sha_tsui", 200501],
    ["Kowloon_station", 200504],
    ["Yau_ma_tei", 200507],
    ["Kingspark", 200503],
    ["Mongkok", 200502],
    ["Tai_kok_tsui", 200506],
    ["Olympic", 200505],
    ["Lai_chi_kok", 200601],
    ["Mei_foo", 200604],
    ["Cheung_sha_wan_sham_shui_po", 200602],
    ["Yau_yat_tsuen", 200603],
    ["Kowloon_tong_beacon_hill", 200903],
    ["Ho_man_tin", 200902],
    ["Hung_hum", 200901],
    ["To_kwa_wan", 200904],
    ["Kai_tak", 200906],
    ["Kowloon_city", 200905],
    ["Wong_tai_sin_lok_fu", 200801],
    ["Diamond_hill_san_po_kong_ngau_chi_wan", 200802],
    ["Kowloon_bay", 200701],
    ["Kwun_tong", 200703],
    ["Lam_tin_yau_tong", 200702],
    ["Lohas_park", 201005],
    ["Tiu_keng_leng", 201004],
    ["Hang_hau", 201001],
    ["Po_lam_tseung_kwan_o_station", 201002]
]

region_new_territory = [
    ["Sai_kung_clear_water_bay", 301003],
    ["Shatin", 301702],
    ["Kau_to_shan_fotan", 301701],
    ["Ma_on_shan", 301703],
    ["Tai_po", 301601],
    ["North", 301502],
    ["Sheung_shui_fanling", 301501],
    ["Hung_shui_kiu", 301403]
    ["Fairview_palm_springs_the_vineyard", 301404],
    ["Tin_shui_wai", 301401],
    ["Yuen_long", 301402],
    ["Tuen_mun", 301301],
    ["Tsuen_wan", 301101],
    ["Sham_tseng", 301102],
    ["Ma_wan", 301103],
    ["Kwai_chung", 301201],
    ["Tsing_yi", 301202],
    ["Discovery_bay", 301802],
    ["Tung_chung", 301803],
    ["Lan_tau_island", 301801]
]

url = "https://data.midland.com.hk/search/v1/transactions?"

headers = {
    'Host': 'data.midland.com.hk',
    'Origin': 'https://www.midland.com.hk',
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJndWlkIjoibXItMjAyMS0wMS0wNy1IR0dISy15QlFtYWZRM1hvYjZuMWJ2M2xsa0prVGk4aW9Yd3REOGp6VzBDYTZkLVNZQ0M3M2VYNXJwZUtNYWQzNll1T0RXei1JSSIsImlhdCI6MTYxMDAxMjA2MCwiaXNzIjoiZGF0YS5taWRsYW5kLmNvbS5oayJ9.cCMBWDgWiYriWQqcbnvjjV4c7GaleBcA5rQ9a6alKsSgEwOlCX--fwSt2WsPSHMhNMPVqL58t_zqodmntNOKqZiV4baYXyxpj8AdSL4KufmB5xatdIFKY02mSm-4prcUzBDpNTv0u26hrMQP5wJxx1L4Sag_jx0llqU7WSGKXPKUXHopNvoPb0M05MnjWSnh537yOWRfeWSLmtIdAOWtk3BdlTs8drfuzF969e5dyMCOMSqgz9yOY9liDQfehQsN-9sZSNEU1nyR4EsGW8Nn4yjtppEu9FuYAzrrz2X2NJMO2oagQvsNJoqWw83ktPpf4Tpike5bWkdFCS6g-bz7IMN7X4hslcYd8wmzkIg7Ga5HWqzLU5Ns-1fVkXbulI2HvH109Cn9KlLSPp4Ya2ZCVt5ey5DRMkvQ3jxzJv05CoCfmWVKvxrbOma65t7TPmdYX0OgGH4tl9QRwJZrEoWh7st99cAabs4SKdYO1eKydugP6LXN33fnjayUEH4ouciv0QMRyjocPgGYZSVTBCmS_ks1YHmUB7nm6XzkuuLtzmvBo-PsGTcvfNIIZuonkz4fdTJfZniaU9g-Yp5Ike7517scMLMQLmCJVfDjqbDJ3GQnT_uPEBEiKLpq1in3-xh_o-a0w8wXbmlpJQ488cI67ulc3G8558W9357U1ZbXRvg',
    'Referer': 'https://www.midland.com.hk',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

params = {
    'hash': 'true',
    'lang': 'en',
    'currency': 'HKD',
    'unit': 'feet',
    'search_behavior': 'normal',
    'dist_ids': '100404',
    'tx_type': 'S',
    'tx_date': '3year',
    'page': '1',
    'limit': '50',
}


def get_property_list(region_list, reg_period):

    params['tx_date'] = reg_period

    for region in region_list:
        file_name = region[0] + ".csv"

        print(file_name)

        params['dist_ids'] = region[1]

        req = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(req.content, 'html.parser')
        json_data = json.loads(soup.text)

        total_no = json_data["count"]
        print(total_no)

        property_list = []
        total_page_no = math.ceil(total_no/50)
        page = 1

        while(page < (total_page_no+1)):
            print(page)

            params['page'] = page
            req = requests.get(url, headers=headers, params=params)
            soup = BeautifulSoup(req.content, 'html.parser')
            json_data = json.loads(soup.text)
            items = json_data["result"]

            for item in items:
                item_list = []

                #region
                item_list.append(item['region']['name'])
                #subregion
                item_list.append(item['subregion']['name'])
                #district
                item_list.append(item['district']['name'])
                #estate
                item_list.append(item['estate']['name'])
                #building
                try:
                    item_list.append(item['building']['name'])
                except:
                    item_list.append(None)
                #first_op_date
                item_list.append(item['building']['first_op_date'][:10])
                #floor_level
                try:
                    item_list.append(item['floor_level']['id'])
                except:
                    item_list.append(None)
                #bedroom
                item_list.append(item['bedroom'])
                #sitting_room
                item_list.append(item['sitting_room'])
                #floor
                try:
                    item_list.append(item['floor'])
                except:
                    item_list.append(None)
                #flat
                item_list.append(item['flat'])
                #area
                item_list.append(item['area'])
                #net_area
                item_list.append(item['net_area'])
                #price
                item_list.append(item['price'])
                #tx_date
                item_list.append(item['tx_date'][:10])
                #last_tx_date
                item_list.append(item['last_tx_date'][:10])
                #last_price
                item_list.append(item['last_price'])
                #gain
                item_list.append(item['gain'])
                #lat
                try:
                    item_list.append(item['location']['lat'])
                except:
                    item_list.append(None)
                #lon
                try:
                    item_list.append(item['location']['lon'])
                except:
                    item_list.append(None)

                property_list.append(item_list)

            page += 1

        dataFrame = pd.DataFrame(data=property_list)
        dataFrame.columns = ['region', 'subregion', 'district', 'estate', 'building', 'first_op_date',
                             'floor_level', 'bedroom', 'sitting_room', 'floor', 'flat', 'area', 'net_area',
                             'price', 'tx_date', 'last_tx_date', 'last_price', 'gain', 'lat', 'lon']
        dataFrame.to_csv(file_name)

# get_property_list(region_list, reg_period (30days, 90days, 180days, 1year, 3year))
get_property_list(region_hk, '30days')
get_property_list(region_kowloon, '30days')
get_property_list(region_new_territory, '30days')
