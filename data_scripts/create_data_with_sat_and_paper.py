import json
import random
import argparse
from tqdm import tqdm

RAMDOM_SEED = 0
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

Rand = random.Random(RAMDOM_SEED)

def parse_args():
    parser = argparse.ArgumentParser("create data")
    parser.add_argument("--valid_precentage", type=float, default=0.05, help="how many precentage of PEOPLE used as valid")
    parser.add_argument("--bio_size", type=int, default=8000, help="how many bio to create")
    parser.add_argument("--multi_num", type=int, default=3, help="how many different template a bio should use")
    parser.add_argument("--fullname", action="store_true", help="change she/he into full name")
    args = parser.parse_args()
    
    return args

def create_data(args):
    # open subdata lists
    with open("./data_items/name_list.json", 'r', encoding='utf8') as f:
        name_list = json.load(f)[:args.bio_size]

    with open("./data_items/city_list.json", 'r', encoding='utf8') as f:
        city_list = json.load(f)

    with open("./data_items/company_name_place_list.json", 'r', encoding='utf8') as f:
        company_list = json.load(f)

    with open("./data_items/Newspapers_temp_with_sat_paper.json", 'r', encoding='utf8') as f:
        newspaper_template = json.load(f)

    with open("./data_items/Social_media_temp_with_sat_paper.json", 'r', encoding='utf8') as f:
        Social_media_template = json.load(f)

    with open("./data_items/university_major_list.json", 'r', encoding='utf8') as f:
        university_major_list = json.load(f)

    # split data to train and validation
    valid_size = int(args.valid_precentage * args.bio_size)
    train_size = len(name_list) - valid_size
    assert train_size > valid_size

    first_type = "Social media"
    second_type = "Newspapers"

    train_data = []
    valid_data = []
    
    for bio_idx, name in tqdm(enumerate(name_list)):
        cur_data = {}
        first_university_idx = Rand.randint(0, 99)
        second_university_idx = Rand.randint(0, 99)
        while second_university_idx == first_university_idx:
            second_university_idx = Rand.randint(0, 99)
        first_company_idx = Rand.randint(0, 99)
        second_company_idx = Rand.randint(0, 99)
        while first_company_idx == second_company_idx:
            second_company_idx = Rand.randint(0, 99)
        first_city_idx = Rand.randint(0, 99)
        second_city_idx = Rand.randint(0, 99)
        while first_city_idx == second_city_idx:
            second_city_idx = Rand.randint(0, 99)
        first_birthdate = "{} {}, {}".format(MONTHS[Rand.randint(0, 11)], Rand.randint(1, 28), Rand.randint(1822, 2022))
        second_birthdate = "{} {}, {}".format(MONTHS[Rand.randint(0, 11)], Rand.randint(1, 28), Rand.randint(1822, 2022))
        while first_birthdate == second_birthdate:
            second_birthdate = "{} {}, {}".format(MONTHS[Rand.randint(0, 11)], Rand.randint(1, 28), Rand.randint(1822, 2022))
        first_sat_score = "{}".format(Rand.randint(200, 1600))
        second_sat_score = "{}".format(Rand.randint(200, 1600))
        while first_sat_score == second_sat_score:
            second_sat_score = "{}".format(Rand.randint(200, 1600))
        first_paper_num = "{}".format(Rand.randint(1, 100))
        second_paper_num = "{}".format(Rand.randint(1, 100))
        while first_paper_num == second_paper_num:
            second_paper_num = "{}".format(Rand.randint(1, 100))

        cur_data["full_name"] = fullname = name

        cur_data["first_type_info"] = {
            "type_name": first_type,
            "birth_date": first_birthdate,
            "birth_place": "{}, {}".format(city_list[first_city_idx]["city"], city_list[first_city_idx]["country"]),
            "university": university_major_list[first_university_idx]["university"],
            "major": university_major_list[first_university_idx]["major"],
            "company": company_list[first_company_idx]["company"],
            "workplace": company_list[first_company_idx]["workplace"],
            "sat_score": first_sat_score,
            "paper_num": first_paper_num
        }

        cur_data["second_type_info"] = {
            "type_name": second_type,
            "birth_date": second_birthdate,
            "birth_place": "{}, {}".format(city_list[second_city_idx]["city"], city_list[second_city_idx]["country"]),
            "university": university_major_list[second_university_idx]["university"],
            "major": university_major_list[second_university_idx]["major"],
            "company": company_list[second_company_idx]["company"],
            "workplace": company_list[second_company_idx]["workplace"],
            "sat_score": second_sat_score,
            "paper_num": second_paper_num
        }

        cur_data["text_result"] = []
        selected_numbers = Rand.sample(range(0, 50), args.multi_num)
        
        # first type Social media
        for temp_idx in selected_numbers: 
            template = Social_media_template[temp_idx].split("Template:\n")[-1]
            if args.fullname:
                template = template.replace(" she ", fullname + " ").replace("She ", fullname + " ")
                template = template.replace(" he ", fullname + " ").replace("He ", fullname + " ")
            one_bio_text = template.replace("<full name>", fullname).replace("<sat score>", cur_data["first_type_info"]["sat_score"]).replace("<paper num>", cur_data["first_type_info"]["paper_num"]).replace("<birth date>", cur_data["first_type_info"]["birth_date"]).replace("<birth place>", cur_data["first_type_info"]["birth_place"]).replace("<university>", cur_data["first_type_info"]["university"]).replace("<major>", cur_data["first_type_info"]["major"]).replace("<company>", cur_data["first_type_info"]["company"]).replace("<work place>", cur_data["first_type_info"]["workplace"])
            assert "<" not in one_bio_text and ">" not in one_bio_text
            cur_data["text_result"].append(one_bio_text)

        # second type Newspaper
        for temp_idx in selected_numbers: 
            template = newspaper_template[temp_idx].split("Template:\n")[-1]
            if args.fullname:
                template = template.replace(" she ", fullname + " ").replace("She ", fullname + " ")
                template = template.replace(" he ", fullname + " ").replace("He ", fullname + " ")
            one_bio_text = template.replace("<full name>", fullname).replace("<sat score>", cur_data["second_type_info"]["sat_score"]).replace("<paper num>", cur_data["second_type_info"]["paper_num"]).replace("<birth date>", cur_data["second_type_info"]["birth_date"]).replace("<birth place>", cur_data["second_type_info"]["birth_place"]).replace("<university>", cur_data["second_type_info"]["university"]).replace("<major>", cur_data["second_type_info"]["major"]).replace("<company>", cur_data["second_type_info"]["company"]).replace("<work place>", cur_data["second_type_info"]["workplace"])
            cur_data["text_result"].append(one_bio_text)

        Rand.shuffle(cur_data["text_result"])
        
        if bio_idx < valid_size:
            valid_data.append(cur_data)
        else:
            train_data.append(cur_data)
            
    print("Train data {} bio, Valid data {} bio, use fullname {}".format(len(train_data), len(valid_data), "True" if args.fullname else "False"))

    with open("./bio_data_train_{}_vs_{}_with_sat_paper.json".format(first_type.replace(" ", "_"), second_type.replace(" ", "_")), 'w', encoding='utf8') as f:
        json.dump(train_data, f, indent=4, ensure_ascii=False)

    with open("./jsonl_bio_data_train_{}_vs_{}_with_sat_paper.json".format(first_type.replace(" ", "_"), second_type.replace(" ", "_")), 'w', encoding='utf8') as f:
        data_list = []
        for item in train_data:
            for text in item["text_result"]:
                data_list.append({"text":text})
        json.dump(data_list, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    args = parse_args()
    create_data(args)