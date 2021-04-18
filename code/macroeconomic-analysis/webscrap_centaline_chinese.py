from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import math
import time

region_hk = [
    ["Kennedy_town_sai_ying_pun", ["19-HMA111", "19-HMA047", "19-HMA056", "19-HMA012"]],
    ["Bel_air_sasson", ["19-HMA063"]],
    ["South_horizon", ["19-HMA200"]],
    ["Aberdeen_ap_lei_chau", ["19-HMA155", "19-HMA127", "19-HMA045", "19-HMA093", "19-HMA151", "19-HMA082", "19-HMA122"]],
    ["Mid_level_west", ["19-HMA028", "19-HMA053"]],
    ["Peak_south", ["19-HMA025", "19-HMA141", "19-HMA121", "19-HMA118", "19-HMA123", "19-HMA105", "19-HMA064", "19-HMA018", "19-HMA048", "19-HMA132"]],
    ["Mid_level_central", ["19-HMA076", "19-HMA026"]],
    ["Happy_valley_mid_level_east", ["19-HMA130", "19-HMA070", "19-HMA071", "19-HMA126"]],
    ["Wanchai_causeway_bay", ["19-HMA160", "19-HMA144"]],
    ["North_point", ["19-HMA041", "19-HMA032", "19-HMA014"]],
    ["Mid_level_north_point", ["19-HMA042"]],
    ["Quarry_bay_kornhill", ["19-HMA110", "19-HMA113"]],
    ["Taikoo_shing", ["19-HMA034"]],
    ["Sai_wan_ho", ["19-HMA057", "19-HMA195"]],
    ["Shau_kei_wan_chai_wan", ["19-HMA163", "19-HMA094", "19-HMA020"]],
    ["Heng_fa_chuen", ["19-HMA061"]],
]

region_kowloon = [
    ["Olympic_station", ["19-HMA134"]],
    ["Kowloon_station", ["19-HMA003"]],
    ["Mongkok_yaumatei", ["19-HMA074", "19-HMA068", "19-HMA015", "19-HMA033"]],
    ["Tsimshatsui_jordan", ["19-HMA172", "19-HMA052", "19-HMA059"]],
    ["Lai_chi_kok", ["19-HMA043"]],
    ["Nam_cheong", ["19-HMA081"]],
    ["Ho_man_tin_kings_park", ["19-HMA065", "19-HMA058"]],
    ["To_kwa_wan", ["19-HMA013", "19-HMA108"]],
    ["Whampoa_laguna_verde", ["19-HMA133", "19-HMA095"]],
    ["Tseung_kwan_o", ["19-HMA148", "19-HMA112", "19-HMA060", "19-HMA159", "19-HMA114"]],
    ["Meifoo_wonderland", ["19-HMA128", "19-HMA099", "19-HMA098", "19-HMA092", "19-HMA089"]],
    ["Cheung_sha_wan_sham_shui_po", ["19-HMA171", "19-HMA049", "19-HMA077"]],
    ["Yau_yat_chuen", ["19-HMA010"]],
    ["Kowloon_tong", ["19-HMA152", "19-HMA004"]],
    ["Lam_tin_yau_tong", ["19-HMA156", "19-HMA075"]],
    ["Kowloon_bay_ngau_chi_wan", ["19-HMA005", "19-HMA040"]],
    ["Kwun_tong", ["19-HMA161", "19-HMA051"]],
    ["Diamond_hill_wong_tai_sin", ["19-HMA147", "19-HMA131", "19-HMA066", "19-HMA135", "19-HMA137", "19-HMA162", "19-HMA002", "19-HMA115", "19-HMA039"]],
    ["Hung_hum", ["19-HMA090", "19-HMA091"]],
    ["Kai_tak", ["19-HMA117"]],
]

region_new_east = [
    ["Sai_kung", ["19-HMA055", "19-HMA046", "19-HMA054", "19-HMA119", "19-HMA017"]],
    ["Tai_wai", ["19-HMA188"]],
    ["Shatin", ["19-HMA170", "19-HMA106", "19-HMA062", "19-HMA176", "19-HMA021"]],
    ["Fotan_shatin_kau_to_shan", ["19-HMA187", "19-HMA001"]],
    ["Ma_on_shan", ["19-HMA107"]],
    ["Tai_po_mid_level_hong_lok_yuen", ["19-HMA177", "19-HMA180", "19-HMA169"]],
    ["Tai_po", ["19-HMA184", "19-HMA182", "19-HMA185", "19-HMA181"]],
    ["Sheung_shui_fanling_kwu_tung", ["19-HMA179", "19-HMA168", "19-HMA166", "19-HMA165", "19-HMA164", "19-HMA189"]],
]

region_new_west = [
    ["Discovery_bay_other_islands", ["19-HMA125", "19-HMA019", "19-HMA078", "19-HMA067", "19-HMA178"]],
    ["Fairview_park_palm_spring_the_vineyard", ["19-HMA150", "19-HMA136"]],
    ["Yuen_long", ["19-HMA085", "19-HMA084", "19-HMA191", "19-HMA087", "19-HMA083", "19-HMA190", "19-HMA030", "19-HMA029", "19-HMA009", "19-HMA008", "19-HMA007", "19-HMA006", "19-HMA149"]],
    ["Tuen_mun", ["19-HMA138", "19-HMA139", "19-HMA037", "19-HMA038", "19-HMA153", "19-HMA036", "19-HMA035", "19-HMA050", "19-HMA157", "19-HMA086"]],
    ["Tin_shui_wai", ["19-HMA031"] ],
    ["Tsuen_wan_belvedere_garden", ["19-HMA016", "19-HMA143", "19-HMA103", "19-HMA104", "19-HMA193", "19-HMA100", "19-HMA101", "19-HMA102", "19-HMA158"]],
    ["Kwai_chung", ["19-HMA140", "19-HMA192"] ],
    ["Tsing_yi", ["19-HMA079"]],
    ["Ma_wan_park_island", ["19-HMA109"]],
    ["Tung_chung_islands", ["19-HMA174", "19-HMA183"]],
    ["Sham_tseng_castle_peak_road", ["19-HMA023", "19-HMA116", "19-HMA011", "19-HMA073", "19-HMA120", "19-HMA080"]],
]

url = "https://hk.centanet.com/findproperty/api/Transaction/Search"

headers = {
    'Host': 'hk.centanet.com',
    'Origin': 'https://hk.centanet.com',
    'Referer': 'https://hk.centanet.com/findproperty/list/transaction?q=vVw54ms7VkOTQQdKanf3VA',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Content-Length': '191',
    'Connection': 'keep-alive',
}

data = {
    "day": "Day1095",
    "mtrs": [],
    "offset": 0,
    "order": "desc",
    "pageSource": "search",
    "postType": "Sale",
    "primarySchoolNets": [],
    "size": 15,
    "sort": "InsOrRegDate",
    "typeCodes": []
}


def get_property_list(region_name, region_list, reg_period):

    data['day'] = reg_period

    for region in region_list:
        file_name = "centaline_chinese/" + region_name + "/" + region[0] + ".csv"
        print("File name: ", file_name)

        # open file to be updated
        original_df = pd.read_csv(file_name, index_col=0)
        last_updated_date = original_df["regDate"].iloc[1]
        print("Last updated date: ", last_updated_date)

        data['typeCodes'] = region[1]

        req = requests.post(url, headers=headers, data=json.dumps(data))
        soup = BeautifulSoup(req.content, 'html.parser')
        # time to load the data
        time.sleep(1)
        json_data = json.loads(soup.text)

        total_no = json_data["count"]
        print("Total no. of records: ",total_no)

        property_list = []
        no = 0

        while(no < (total_no+1)):
            print("no: ", no)

            try:
                data['offset'] = no
                req = requests.post(url, headers=headers, data=json.dumps(data))
                soup = BeautifulSoup(req.content, 'html.parser')
                # time to load the data
                time.sleep(1)
                json_data = json.loads(soup.text)
                items = json_data["data"]
            except:
                print("failed to fetch data")
                no += 15
                continue

            for item in items:
                try:
                    reg_date = item['regDate'][:10]
                except:
                    reg_date = item['insDate'][:10]

                if reg_date == last_updated_date:
                    break

                item_list = []

                #region
                try:
                    item_list.append(item['scope']['terr'])
                except:
                    item_list.append(None)
                #district
                try:
                    item_list.append(item['districtName'])
                except:
                    item_list.append(None)
                #estate
                try:
                    item_list.append(item['estateName'])
                except:
                    item_list.append(None)
                #building
                try:
                    item_list.append(item['buildingName'])
                except:
                    item_list.append(None)
                #address
                try:
                    item_list.append(item['address'])
                except:
                    item_list.append(None)
                #floor
                try:
                    item_list.append(item['yAxis'])
                except:
                    item_list.append(None)
                #flat
                try:
                    item_list.append(item['xAxis'])
                except:
                    item_list.append(None)
                #transaction price
                try:
                    item_list.append(item['transactionPrice'])
                except:
                    item_list.append(None)
                #gross area
                try:
                    item_list.append(item['gArea'])
                except:
                    item_list.append(None)
                #gross area unit price
                try:
                    item_list.append(item['gUnitPrice'])
                except:
                    item_list.append(None)
                #net area
                try:
                    item_list.append(item['nArea'])
                except:
                    item_list.append(None)
                #net area unit price
                try:
                    item_list.append(item['nUnitPrice'])
                except:
                    item_list.append(None)
                #reg date
                item_list.append(reg_date)
                #bedroom count
                try:
                    item_list.append(item['bedroomCount'])
                except:
                    item_list.append(None)

                property_list.append(item_list)

            else:
                no += 15
                continue
            break

        if len(property_list) > 1:
            dataFrame = pd.DataFrame(data=property_list)
            dataFrame.columns = ['region', 'district', 'estate', 'building', 'address',
                                 'floor', 'flat', 'price', 'grossArea', 'upGrossArea', 'saleableArea',
                                 'upSaleableArea', 'regDate', 'bedroom']
            dataFrame = dataFrame.append(original_df, ignore_index=True)
            dataFrame.to_csv(file_name, encoding='utf_8_sig')
            print("updated")
        else:
            print("up to date")
        print("---------------------------------------")

# get_property_list(region_name, region_list, reg_period (Day30, Day90, Day180, Day365, Day1095))
get_property_list("hk_island", region_hk, 'Day30')
get_property_list("kowloon", region_kowloon, 'Day30')
get_property_list("new_east", region_new_east, 'Day30')
get_property_list("new_west", region_new_west, 'Day30')