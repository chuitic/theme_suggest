import json,requests,urllib

def lambda_handler(event, context):

    headers = {"X-Cybozu-API-Token": "OK9BrJbSD5Q9cwQXkUgDxZlue94KY1gfcJGjokNK"}
    res1 = json.loads(requests.get('https://chuitic.cybozu.com/k/v1/records.json?app=8', headers=headers).text)["records"] 
    
    user = "23415"  # 本当はボタンを押したユーザーのuser_idを入れる
    place = [i["places"]["value"][0] for i in list(filter(lambda x:x["user_id"]["value"]==user,res1))] #ユーザーが希望する場所

    place1_id = [i["user_id"]["value"] for i in list(filter(lambda x:x["places"]["value"][0]=="梅田",res1))]
    place2_id = [i["user_id"]["value"] for i in list(filter(lambda x:x["places"]["value"][0]=="十三",res1))]
    place3_id = [i["user_id"]["value"] for i in list(filter(lambda x:x["places"]["value"][0]=="心斎橋",res1))]
    place4_id = [i["user_id"]["value"] for i in list(filter(lambda x:x["places"]["value"][0]=="本町",res1))]
    place5_id = [i["user_id"]["value"] for i in list(filter(lambda x:x["places"]["value"][0]=="鶴橋",res1))]

    headers = {"X-Cybozu-API-Token": "9JncOzbEWpGyPh4pffqlFwQOnwvBFvcjhtBx04dy"}
    res2 = json.loads(requests.get("https://chuitic.cybozu.com/k/v1/records.json?app=6", headers=headers).text)["records"]
    
    match_id = []
    for i in place:
        if i == "梅田":
            match_id = match_id + place1_id
        if i == "十三":
            match_id = match_id + place2_id
        if i == "心斎橋":
            match_id = match_id + place3_id
            print(3)
        if i == "本町":
            match_id = match_id + place4_id
        if i == "鶴町":
            match_id = match_id + place5_id
    
    # print(place)
    # print(place3_id)
    match_id.remove(user) #match_idは場所でマッチした人のuser_idの配列になる
    # match_id = [i["user_id"]["value"] for i in list(filter(lambda x:x["places"]["value"][0]==place,res1))]
    
    #return place
    
    #以下マッチした組みをmatch_tableに入れる作業
    URL = "https://chuitic.cybozu.com/k/v1/record.json"
    for i in match_id[:3]:
        # PARAMS = {
        #   "app": 10,
        #   "record": {
        #     "user_id_1": {
        #       "value": user
        #     },
        #     "user_id_2": {
        #       "value": i
        #     },
        #   }
        # }
        # API_TOKEN = "ayqYnrMFHTNfMHqMUzAaa813sridMiNmHI7byMNH"
        # headers = {"X-Cybozu-API-Token": API_TOKEN, "Content-Type" : "application/json"}
        # rest = requests.post(URL, json=PARAMS, headers=headers)
        
        for j in list(filter(lambda x:x["user_id"]["value"]==i,res2)):
            name = j['name']['value']
            sex = j['sex']['value']
            job = j['job']['value']
            
            print(name,sex,job)
        #print([j["places"]["value"][0] for j in list(filter(lambda x:x["user_id"]["value"]==i,res2))])
        
        #以下マッチした相手の情報をflexmessageで送る
        #送るものとしては相手の名前と性別と仕事
        
        FLEX = {
          "type": "bubble",
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": name,
                "weight": "bold",
                "size": "xl"
              },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "性別",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 1
                      },
                      {
                        "type": "text",
                        "text": sex,
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "職業",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 1
                      },
                      {
                        "type": "text",
                        "text": job,
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                      }
                    ]
                  }
                ]
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                  "type": "uri",
                  "label": "Yes",
                  "uri": "https://linecorp.com"
                }
              },
              {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                  "type": "uri",
                  "label": "No",
                  "uri": "https://linecorp.com"
                }
              },
              {
                "type": "spacer",
                "size": "sm"
              }
            ],
            "flex": 0
          }
        }
        
        API_TOKEN = "ayqYnrMFHTNfMHqMUzAaa813sridMiNmHI7byMNH"
        headers = {"X-Cybozu-API-Token": API_TOKEN, "Content-Type" : "application/json"}
        rest = requests.post(URL, json=FLEX, headers=headers)
        
    return match_id
    
    
    

    # return json.loads(res1.text)
    #return None
    # return 'https://chuitic.cybozu.com/k/v1/records.json?app=8&'+urllib.parse.quote('query=places in ("梅田")')

