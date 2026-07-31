#!/usr/bin/env python3
"""Generate Estonia interactive journal + sync short journal texts into day07–10.md."""
from __future__ import annotations

from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "bldh-trio"
PHOTOS = ROOT / "photos" / "bldh-trio"
OUT_HTML = CONTENT / "estonia-journal.html"

# stamp, locale, title, teaser, body, fact, photo rel (dayXX/file.jpg)
# Style: CONTENT_STYLE v1.2（資深旅遊作家；感官切入／禁導覽與流水帳／4–6 句）
CARDS: list[dict] = [
    # —— Day 7 進入愛沙尼亞（塔圖／維爾揚迪）——
    {
        "stamp": "01 · Tartu",
        "locale": "科學門口",
        "title": "AHHAA 門前的火箭",
        "teaser": "白得刺眼的火箭直直戳進藍天，尺度大到讓人先舉手擋光。AHHAA 講動手學科學，連門口都像實驗道具。跟它打聲招呼時忽然想笑……",
        "body": "白得刺眼的火箭直直戳進藍天，尺度大到讓人先舉手擋光。AHHAA 講動手學科學，連門口都像實驗道具。跟它打聲招呼時忽然想笑——一跨進愛沙尼亞，開場白居然是「發射」。",
        "fact": "地點 — AHHAA 科學中心 ／ 造形 — ESA 火箭模型",
        "photo": "day07/ahhaa-rocket-bingge.jpg",
        "day": "day07",
        "slug": "ahhaa-rocket-bingge.jpg",
        "md_title": "AHHAA 科學中心火箭",
    },
    {
        "stamp": "02 · Tartu",
        "locale": "市政廳廣場邊",
        "title": "塔圖傾斜屋",
        "teaser": "腳步在市政廳廣場邊忽然踩空似地一晃——低頭才發現，是地板在傾斜，不是自己站不穩。這棟老房子建於 1793 年……",
        "body": "腳步在市政廳廣場邊忽然踩空似地一晃——低頭才發現，是地板在傾斜，不是自己站不穩。這棟老房子建於 1793 年，一半地基疊在舊城牆石塊上，另一半卻陷進鬆軟地面，兩百多年慢慢歪出約 5.8 度，比比薩斜塔還誇張。如今裡頭是塔圖藝術博物館，踏進展廳得先讓身體重新學會平衡。站在傾斜的地板上看畫，忽然覺得連藝術也可以是歪的，才顯得真實。",
        "fact": "建於 1793 ／ 斜角約 5.8° ／ 現為塔圖藝術博物館",
        "photo": "day07/tartu-leaning-house.jpg",
        "day": "day07",
        "slug": "tartu-leaning-house.jpg",
        "md_title": "塔圖傾斜屋",
        "replace_old_slug": "tartu-town-hall-square.jpg",
    },
    {
        "stamp": "03 · Tartu",
        "locale": "噴泉上的學生",
        "title": "接吻學生噴泉",
        "teaser": "水花先濺到視線裡，撐傘銅像在粉紅市政廳前吻得理直氣壯……",
        "body": "水花先濺到視線裡，撐傘銅像在粉紅市政廳前吻得理直氣壯。Mati Karmin 1998 年放下這對日常主角，紀念的不是帝王。坐在池邊看傘沿滴水，覺得這座城把「學生」放得比冠冕還正面。",
        "fact": "雕塑 — Mati Karmin ／ 1998",
        "photo": "day07/kissing-students-fountain-bingge.jpg",
        "day": "day07",
        "slug": "kissing-students-fountain-bingge.jpg",
        "md_title": "接吻學生噴泉",
    },
    {
        "stamp": "04 · Tartu",
        "locale": "知識的門面",
        "title": "塔圖大學主樓",
        "teaser": "白色圓柱一排排托住三角山牆，國旗在屋頂輕輕揚。創校 1632 年，眼前主樓是十九世紀初古典主義重建。抬頭望柱廊時腳步自己慢了……",
        "body": "白色圓柱一排排托住三角山牆，國旗在屋頂輕輕揚。創校 1632 年，眼前主樓是十九世紀初古典主義重建。抬頭望柱廊時腳步自己慢了——書卷氣原來會從石頭裡滲出來。",
        "fact": "創校 1632 ／ 主樓建築師 — Johann Wilhelm Krause",
        "photo": "day07/tartu-university.jpg",
        "day": "day07",
        "slug": "tartu-university.jpg",
        "md_title": "塔圖大學主樓",
    },
    {
        "stamp": "05 · Tartu",
        "locale": "最高法院前",
        "title": "最高法院前的印章雕塑",
        "teaser": "兩棵樹先把畫面夾住，金屬印章斜躺在石鋪圓心，午後光在柄上跳一下。這座雕塑就在愛沙尼亞最高法院前，紀念的是塔圖大學創辦人……",
        "body": "兩棵樹先把畫面夾住，金屬印章斜躺在石鋪圓心，午後光在柄上跳一下。這座雕塑就在愛沙尼亞最高法院前，紀念的是塔圖大學創辦人——把「印記」放大成廣場上的句點。繞到正面才看清把手與圓印面，忍不住蹲低拍。原來知識也可以被鑄成一枚看得見的戳記。",
        "fact": "位置 — 愛沙尼亞最高法院前 ／ 紀念塔圖大學創辦人",
        "photo": "day07/tartu-supreme-court-seal.jpg",
        "day": "day07",
        "slug": "tartu-supreme-court-seal.jpg",
        "md_title": "最高法院前的印章雕塑",
        "replace_old_slug": "tartu-chess-pieces.jpg",
    },
    {
        "stamp": "06 · Tartu",
        "locale": "殘缺的尖拱",
        "title": "主教座堂遺址",
        "teaser": "紅磚尖拱直指天空，縫隙間長出青草，風從缺口穿堂而過。哥德大教堂沒被修回完整，卻留下可走進去的廢墟……",
        "body": "紅磚尖拱直指天空，縫隙間長出青草，風從缺口穿堂而過。哥德大教堂沒被修回完整，卻留下可走進去的廢墟。點開動畫，跟著鏡頭走進拱廊——站在廊道裡抬頭，空曠比穹頂更安靜；有些美，缺一口反而記得住。",
        "fact": "原為磚造哥德主教座堂 ／ 現為遺址公園",
        "photo": "day07/tartu-cathedral-ruins-bingge.jpg",
        "day": "day07",
        "slug": "tartu-cathedral-ruins-bingge.jpg",
        "md_title": "塔圖主教座堂遺址",
        "video": "day07/tartu-cathedral-ruins.mp4",
    },
    {
        "stamp": "07 · Tartu",
        "locale": "廢墟上的木棧",
        "title": "主教座堂塔樓廊道",
        "teaser": "木棧道架在古磚高處，尖拱門外透出綠樹，新舊之間故意留著縫……",
        "body": "木棧道架在古磚高處，尖拱門外透出綠樹，新舊之間故意留著縫。當代結構輕、可逆，不假裝自己是中世紀。背靠遺址合影時想：時間撕開的輪廓，有時比修補更誠實。",
        "fact": "當代木棧道 ／ 可逆介入古磚遺址",
        "photo": "day07/tartu-cathedral-tower-bingge.jpg",
        "day": "day07",
        "slug": "tartu-cathedral-tower-bingge.jpg",
        "md_title": "主教座堂塔樓廊道",
    },
    {
        "stamp": "08 · Tartu",
        "locale": "粉紅門面",
        "title": "塔圖市政廳",
        "teaser": "粉紅立面在傍晚光裡發亮，鐘樓與花箱並排，愛沙尼亞與歐盟旗輕輕碰一下。十八世紀末的古典主義市政廳，把廣場的臉寫得很清楚。繞完一圈還是停在它前面……",
        "body": "粉紅立面在傍晚光裡發亮，鐘樓與花箱並排，愛沙尼亞與歐盟旗輕輕碰一下。十八世紀末的古典主義市政廳，把廣場的臉寫得很清楚。繞完一圈還是停在它前面——像認出一個剛認識、卻已經很熟的朋友。",
        "fact": "十八世紀末古典主義市政廳",
        "photo": "day07/tartu-town-hall-bingge.jpg",
        "day": "day07",
        "slug": "tartu-town-hall-bingge.jpg",
        "md_title": "塔圖市政廳",
    },
    {
        "stamp": "09 · Viljandi",
        "locale": "湖畔勇氣",
        "title": "維爾揚迪湖跳台",
        "teaser": "入夜前的湖面先顫一下，有人從上層跳台躍下，水花散成一圈圈圓。上層給大人、下層給孩子，湖岸運動氣息很濃。看著圓圈一圈圈淡掉，天色也跟著軟了……",
        "body": "入夜前的湖面先顫一下，有人從上層跳台躍下，水花散成一圈圈圓。上層給大人、下層給孩子，湖岸運動氣息很濃。看著圓圈一圈圈淡掉，天色也跟著軟了——勇氣有時只需要半秒，和一聲笑。",
        "fact": "上層大人 ／ 下層兒童",
        "photo": "day07/viljandi-lake-diving-board.jpg",
        "day": "day07",
        "slug": "viljandi-lake-diving-board.jpg",
        "md_title": "維爾揚迪湖跳台",
    },
    {
        "stamp": "10 · Viljandi",
        "locale": "市長與愛犬",
        "title": "階梯口的銅像",
        "teaser": "階梯口的銅像像剛要邁步：August Maramaa 牽著狗，神情幾乎聽得見爪聲……",
        "body": "階梯口的銅像像剛要邁步：August Maramaa 牽著狗，神情幾乎聽得見爪聲。Aili Vahtrapuu 2007 年鑄下這對搭檔；據說市長任內把維爾揚迪往度假小城打磨。站在牠們前面，覺得「用心」這種東西，銅也能傳溫。",
        "fact": "雕塑家 — Aili Vahtrapuu ／ 揭幕 2007年8月3日 ／ 位置 — Trepimäe 階梯起點",
        "photo": "day07/viljandi-man-and-dog-sculpture.jpg",
        "day": "day07",
        "slug": "viljandi-man-and-dog-sculpture.jpg",
        "md_title": "市長與愛犬銅像",
    },
    {
        "stamp": "11 · Viljandi",
        "locale": "小鎮天際線",
        "title": "維爾揚迪水塔",
        "teaser": "綠頂八角木屋架在紅磚圓塔上，街樹夾道，天色開始轉淡……",
        "body": "綠頂八角木屋架在紅磚圓塔上，街樹夾道，天色開始轉淡。二十世紀初的供水設施，如今安靜站成地標。仰拍的瞬間，小鎮天際線像把一天輕輕蓋上蓋子。",
        "fact": "二十世紀初供水塔／地標",
        "photo": "day07/viljandi-water-tower.jpg",
        "day": "day07",
        "slug": "viljandi-water-tower.jpg",
        "md_title": "維爾揚迪水塔",
    },
    {
        "stamp": "12 · Viljandi",
        "locale": "貓之城",
        "title": "街頭的貓咪們",
        "teaser": "才下車就被水泥貓瞪了一眼——原來矮胖柱子是阻車樁，擋車別進行人區……",
        "body": "才下車就被水泥貓瞪了一眼——原來矮胖柱子是阻車樁，擋車別進行人區。Kristi Kangilaski 設計、Aime Kuulbusch 做出來，市徽裡也有貓的影子。轉角再撞見一隻，忍不住一路拍下去：進愛沙尼亞的第一晚，接待處居然是貓。",
        "fact": "設計 — Kristi Kangilaski ／ 雕塑 — Aime Kuulbusch",
        "photo": "day07/viljandi-cat-sculpture-bingge.jpg",
        "day": "day07",
        "slug": "viljandi-cat-sculpture-bingge.jpg",
        "md_title": "街頭的貓咪們",
    },
    # —— Day 8 ——
    {
        "stamp": "13 · Pärnu",
        "locale": "舊火車站原址",
        "title": "派爾努窄軌鐵路紀念碑",
        "teaser": "清晨街角先亮起一塊紅——窄軌蒸汽火車頭的保險槓，綠黑車身安靜停在短軌上，腳邊還蹲著白色小象……",
        "body": "清晨街角先亮起一塊紅——窄軌蒸汽火車頭的保險槓，綠黑車身安靜停在短軌上，腳邊還蹲著白色小象。這是為紀念愛沙尼亞第一條窄軌鐵路「派爾努－瓦爾加」開通 110 週年，於 2006 年立在昔日市中心客運火車站原址；現場陳列德國 O. & Koppel 工廠 1911 年製造的老式蒸汽機車，後方還有聖彼得堡 Arthur Koppel 公司 1913 年的平台貨車廂。跟小象並肩拍照的遊客與孩子一波波過來，海灣小鎮把一段鐵路記憶留在路邊——一天從「不會再開動的火車」開始，節奏反而剛剛好。",
        "fact": "2006 設立 ／ O. & Koppel 1911 蒸汽機車 ／ Arthur Koppel 1913 平台貨車廂",
        "photo": "day08/parnu-locomotive-no5.jpg",
        "day": "day08",
        "slug": "parnu-locomotive-no5.jpg",
        "md_title": "派爾努窄軌鐵路紀念碑",
    },
    {
        "stamp": "14 · Pärnu",
        "locale": "老街尖頂",
        "title": "紅頂塔樓",
        "teaser": "樹蔭一晃，灰石圓塔托起陡峭紅瓦尖頂，單車碾過石徑發出細響……",
        "body": "樹蔭一晃，灰石圓塔托起陡峭紅瓦尖頂，單車碾過石徑發出細響。藍天剛好卡在塔尖後面，像替午前按下暫停。把這轉角收進鏡頭時想：小鎮的好看，常常不在大道，在彎進去的那一下。",
        "fact": "中世紀防禦塔語彙 ／ 派爾努老街",
        "photo": "day08/parnu-street-tower.jpg",
        "day": "day08",
        "slug": "parnu-street-tower.jpg",
        "md_title": "派爾努老街紅頂塔樓",
    },
    {
        "stamp": "15 · Pärnu",
        "locale": "街角咖啡",
        "title": "Café Grand",
        "teaser": "米白陽傘先鋪出一片陰涼，奶油色牆面與紅白花壇把騎士街撐得很有禮貌；國旗輕揚，遠處教堂尖頂探進視野……",
        "body": "米白陽傘先鋪出一片陰涼，奶油色牆面與紅白花壇把騎士街撐得很有禮貌；國旗輕揚，遠處教堂尖頂探進視野。咖啡香還沒靠近，人已經被街景留住。避暑的門面原來可以這麼安靜地打招呼。",
        "fact": "騎士街一帶 ／ 避暑小鎮門面",
        "photo": "day08/parnu-cafe-grand.jpg",
        "day": "day08",
        "slug": "parnu-cafe-grand.jpg",
        "md_title": "Café Grand 街角",
    },
    {
        "stamp": "16 · Pärnu",
        "locale": "洋蔥頂",
        "title": "聖凱瑟琳塔樓",
        "teaser": "洋蔥頭尖頂與十字一層層往上疊，石砌塔身把藍天切成細長條……",
        "body": "洋蔥頭尖頂與十字一層層往上疊，石砌塔身把藍天切成細長條。樹影落在肩上，涼意比解說先到。仰拍合影時忽然覺得：信仰的輪廓，有時就是一柱垂直的光。",
        "fact": "聖凱瑟琳東正教堂塔樓",
        "photo": "day08/parnu-orthodox-tower-bingge.jpg",
        "day": "day08",
        "slug": "parnu-orthodox-tower-bingge.jpg",
        "md_title": "聖凱瑟琳東正教堂塔樓",
    },
    {
        "stamp": "17 · Pärnu",
        "locale": "黃磚與金頂",
        "title": "聖凱瑟琳東正教堂",
        "teaser": "黃磚與紅褐飾帶在陽光裡發暖，多座洋蔥頂的鍍金十字並列閃一下。圍欄尖刺細細發亮，繞到正面再開一格。同一座教堂，遠看是天際線，近看是溫度……",
        "body": "黃磚與紅褐飾帶在陽光裡發暖，多座洋蔥頂的鍍金十字並列閃一下。圍欄尖刺細細發亮，繞到正面再開一格。同一座教堂，遠看是天際線，近看是溫度——兩種距離，兩種語氣。",
        "fact": "巴洛克／古典過渡期東正教堂",
        "photo": "day08/parnu-st-catherine-church-bingge.jpg",
        "day": "day08",
        "slug": "parnu-st-catherine-church-bingge.jpg",
        "md_title": "聖凱瑟琳東正教堂",
    },
    {
        "stamp": "18 · Pärnu",
        "locale": "傳奇船長",
        "title": "基赫努船長雕像",
        "teaser": "舵輪先握住視線，銅像上的 Kihnu Jõnn 像剛從風裡走來……",
        "body": "舵輪先握住視線，銅像上的 Kihnu Jõnn 像剛從風裡走來。座銘寫他對好船的讚嘆：船行得叫海都抱怨。港邊風一吹，覺得堅毅與幽默原來可以鑄在同一雙手上。",
        "fact": "Kihnu Jõnn（Enn Uuetoa）",
        "photo": "day08/parnu-kihnu-jonn-statue.jpg",
        "day": "day08",
        "slug": "parnu-kihnu-jonn-statue.jpg",
        "md_title": "基赫努船長雕像",
    },
    {
        "stamp": "19 · Pärnu",
        "locale": "帕爾努河左岸",
        "title": "1944年大逃亡紀念碑",
        "teaser": "1944年大逃亡紀念碑（Monument to the Great Flight of 1944），由藝術家 Elo Liiv 創作，紀念 1944 年為逃離蘇聯佔領而被迫離開家園的數萬名愛沙尼亞人……",
        "body": "1944年大逃亡紀念碑（Monument to the Great Flight of 1944），由藝術家 Elo Liiv 創作，紀念 1944 年為逃離蘇聯佔領而被迫離開家園的數萬名愛沙尼亞人。雕塑由金屬網狀結構製成，描繪了兩隻手最後的觸碰，象徵著分離與告別。它位於帕爾努河（Pärnu River）左岸，靠近城市中心橋，是當年人們向西逃離的具體地點。",
        "fact": "藝術家 — Elo Liiv ／ Monument to the Great Flight of 1944 ／ 帕爾努河左岸・市中心橋附近",
        "photo": "day08/parnu-hands-sculpture-bingge.jpg",
        "day": "day08",
        "slug": "parnu-hands-sculpture-bingge.jpg",
        "md_title": "1944年大逃亡紀念碑",
    },
    {
        "stamp": "20 · Pärnu",
        "locale": "海灣一小時",
        "title": "派爾努灣遊艇",
        "teaser": "船身劃開深藍，桅杆收在一側，「JÄÄLIND」像翠鳥掠過水面；岸邊綠樹與小艇慢慢後退……",
        "body": "船身劃開深藍，桅杆收在一側，「JÄÄLIND」像翠鳥掠過水面；岸邊綠樹與小艇慢慢後退。約一小時海灣巡航，風比任何地圖都直接。陸上走了一早，終於把身體交給浪——這才像真正到了海邊。",
        "fact": "船名 JÄÄLIND（翠鳥） ／ 約 1 小時",
        "photo": "day08/parnu-yacht-jaalind.jpg",
        "day": "day08",
        "slug": "parnu-yacht-jaalind.jpg",
        "md_title": "派爾努灣遊艇",
    },
    {
        "stamp": "21 · Pärnu",
        "locale": "午餐",
        "title": "愛沙尼亞式鴨肉",
        "teaser": "烤鴨皮一裂開就冒熱氣，Saku 啤酒涼涼貼著指節；黑麵包、鮮蔬，結尾是草莓冰淇淋……",
        "body": "烤鴨皮一裂開就冒熱氣，Saku 啤酒涼涼貼著指節；黑麵包、鮮蔬，結尾是草莓冰淇淋。醬汁與麥香把度假灣的節奏先落到舌尖。吃完站起來，塔林忽然變得更近一點。",
        "fact": "愛沙尼亞式鴨肉午餐",
        "photo": "day08/estonia-duck-lunch.jpg",
        "day": "day08",
        "slug": "estonia-duck-lunch.jpg",
        "md_title": "愛沙尼亞式鴨肉午餐",
    },
    {
        "stamp": "22 · Tallinn",
        "locale": "拱門裡的晚餐",
        "title": "MOON 餐廳",
        "teaser": "石砌拱門上方「MOON RESTORAN」幾個字先亮起來，牆邊紅標寫著 Michelin，紫花盆栽夾道……",
        "body": "石砌拱門上方「MOON RESTORAN」幾個字先亮起來，牆邊紅標寫著 Michelin，紫花盆栽夾道。推門前先拍下門口，期待比菜單早一步。首都第一晚，原來從一塊招牌的光開始。",
        "fact": "Michelin 推薦 ／ 老城拱門入口",
        "photo": "day08/tallinn-moon-restoran.jpg",
        "day": "day08",
        "slug": "tallinn-moon-restoran.jpg",
        "md_title": "MOON 米其林推薦餐廳",
    },
    {
        "stamp": "23 · Tallinn",
        "locale": "第一頓",
        "title": "米其林推薦晚餐",
        "teaser": "刀尖切開酥皮白魚，外層碎裂聲比味道先到；烤南瓜石榴沙拉、蛋白霜乳霜甜點輪流上場。層次在舌尖慢慢展開。旅途的疲憊好像也被這頓餐煮軟了……",
        "body": "刀尖切開酥皮白魚，外層碎裂聲比味道先到；烤南瓜石榴沙拉、蛋白霜乳霜甜點輪流上場。層次在舌尖慢慢展開。旅途的疲憊好像也被這頓餐煮軟了——塔林的第一口夜晚，意外地安靜。",
        "fact": "MOON 晚餐",
        "photo": "day08/michelin-dinner.jpg",
        "day": "day08",
        "slug": "michelin-dinner.jpg",
        "md_title": "米其林推薦晚餐",
    },
    {
        "stamp": "24 · Tallinn",
        "locale": "廣場之狼",
        "title": "電影之狼",
        "teaser": "廣場上混凝土狼仰頭長嚎，幾何塊面把野性收成沉默的線條……",
        "body": "廣場上混凝土狼仰頭長嚎，幾何塊面把野性收成沉默的線條——Simson von Seakyl 的手筆。側身學它抬頭，對天空比一個無聲的喊。抵達首都的夜，忽然有了電影感。",
        "fact": "藝術家 — Simson von Seakyl ／ 混凝土狼雕像",
        "photo": "day08/tallinn-movie-wolf-bingge.jpg",
        "day": "day08",
        "slug": "tallinn-movie-wolf-bingge.jpg",
        "md_title": "電影之狼雕塑",
    },
    {
        "stamp": "25 · Tallinn",
        "locale": "超市小風景",
        "title": "Delice 水果車",
        "teaser": "亮黃 Delice 三輪車停在走道中央，葡萄、檸檬與水蜜桃堆成小山；同行舉起蘋果大笑……",
        "body": "亮黃 Delice 三輪車停在走道中央，葡萄、檸檬與水蜜桃堆成小山；同行舉起蘋果大笑。大景點之外，這種小東西才讓人覺得自己真的來過。旅行有時不是名勝，是一輛捨不得路過的水果車。",
        "fact": "塔林超市內水果販賣車",
        "photo": "day08/tallinn-delice-fruit-cart.jpg",
        "day": "day08",
        "slug": "tallinn-delice-fruit-cart.jpg",
        "md_title": "塔林超市水果車",
    },
]

# Continue Day 9–10 in same style (append below in generation from compact list)
DAY9 = [
    ("tallinn-viru-gate-bingge.jpg", "26 · Tallinn", "老城門檻", "維魯城門",
     "石板路高低起伏，腳底先告訴你：進來了。兩座紅瓦圓錐頂石塔夾出一道門縫，晨光從塔間漏下來。雙臂交叉在門檻前合影，忽然覺得童話不是寫出來的……",
     "石板路高低起伏，腳底先告訴你：進來了。兩座紅瓦圓錐頂石塔夾出一道門縫，晨光從塔間漏下來。雙臂交叉在門檻前合影，忽然覺得童話不是寫出來的——是踩進去的。",
     "維魯城門"),
    ("tallinn-town-hall-dragon-spout.jpg", "27 · Tallinn", "牆角之龍", "市政廳龍頭排水口",
     "牆角探出一隻戴金冠的綠銅龍，張口吐水，鐵支架托著下顎，細流聲比行人還安靜……",
     "牆角探出一隻戴金冠的綠銅龍，張口吐水，鐵支架托著下顎，細流聲比行人還安靜。中世紀連排水都做成守護獸。多看幾秒才發現：細節裡住著故事，而且不怕被淋濕。",
     "市政廳排水獸"),
    ("tallinn-holy-ghost-clock.jpg", "28 · Tallinn", "會講故事的鐘", "聖靈教堂古鐘",
     "抬頭的瞬間，金色羅馬數字先攫住視線——十七世紀的日輪鐘鑲在白牆紅瓦之間，藍白放射紋像被時間反覆擦亮過……",
     "抬頭的瞬間，金色羅馬數字先攫住視線——十七世紀的日輪鐘鑲在白牆紅瓦之間，藍白放射紋像被時間反覆擦亮過。導遊說這是老城裡「會講故事的鐘」，我半信半疑，直到晨光斜斜切過鐘面，金屬的光澤忽然活了起來。按下快門的那一刻突然明白：在塔林，連時間都捨得慢下來讓人看清楚。",
     "十七世紀日輪時鐘"),
    ("tallinn-art-nouveau-gable.jpg", "29 · Tallinn", "夾鼻眼鏡", "偷窺者",
     "抬頭先撞上灰綠飾帶與圓窗，曲線像故意跟舊城石牆唱反調。這是舊城區的 Reichmann House，Jacques Rosenbaum 於 1908 年設計……",
     "抬頭先撞上灰綠飾帶與圓窗，曲線像故意跟舊城石牆唱反調。這是舊城區的 Reichmann House（Reichmanni maja），波羅的海德國建築師 Jacques Rosenbaum 於 1908 年設計，把新藝術運動與新文藝復興、新風格主義揉在同一面牆上。正面雕塑最出名的是那位戴夾鼻眼鏡的老人——當地人叫他「偷窺者」。盯著那副鏡片看一會兒，忽然覺得這座城也會偷看路人：華麗歸華麗，幽默卻藏在牆縫裡。",
     "Reichmann House ／ Jacques Rosenbaum 1908 ／ 新藝術運動"),
    ("tallinn-blackheads-door.jpg", "30 · Tallinn", "漢薩門面", "黑人頭兄弟會大門",
     "雙獅扶盾，門楣摩爾人頭像沉著臉；綠門配紅斜紋與金花釘，漢薩商人的氣派一整面推來……",
     "雙獅扶盾，門楣摩爾人頭像沉著臉；綠門配紅斜紋與金花釘，漢薩商人的氣派一整面推來。黑人頭兄弟會的會所門面，華麗得毫不客氣。排隊拍照時想笑：原來做生意，也可以這麼隆重地敲門。",
     "黑人頭兄弟會會所"),
    ("tallinn-three-sisters-bingge.jpg", "31 · Tallinn", "三姊妹", "三姊妹之屋",
     "三棟窄瘦山牆緊緊相依，正中赭黃那棟掛著 The Three Sisters Hotel 鐵罩，像裡加「三兄弟」的遠親……",
     "三棟窄瘦山牆緊緊相依，正中赭黃那棟掛著 The Three Sisters Hotel 鐵罩，像裡加「三兄弟」的遠親。仰拍時山牆幾乎要擠進鏡頭。姊妹站在一起，比任何解說牌都好懂——親疏遠近，建築也會說。",
     "三姊妹民宅／旅館"),
    ("tallinn-town-hall-square-bingge.jpg", "32 · Tallinn", "老城心臟", "市政廳廣場尖塔",
     "細長尖塔刺進陰天，石板廣場把人聲吸成低語；老湯瑪士風向標的傳說就停在那屋頂……",
     "細長尖塔刺進陰天，石板廣場把人聲吸成低語；老湯瑪士風向標的傳說就停在那屋頂。廣場中央抬頭，尺度先把胸口填滿。波羅的海三國若只能留一座中世紀城，我會把票投給這一眼。",
     "市政廳廣場"),
    ("tallinn-maiasmokk-cafe-bingge.jpg", "33 · Tallinn", "最老咖啡館", "Maiasmokk",
     "櫥窗寫著 1864，紙雕摩天輪用湯匙排成輻條，舊城立面倒映在玻璃裡疊成雙重街景。側身一笑，甜味還沒入口。歷史有時聞起來像糖……",
     "櫥窗寫著 1864，紙雕摩天輪用湯匙排成輻條，舊城立面倒映在玻璃裡疊成雙重街景。側身一笑，甜味還沒入口。歷史有時聞起來像糖——而且不趕時間。",
     "Maiasmokk 自 1864"),
    ("tallinn-town-hall-pharmacy-bingge.jpg", "34 · Tallinn", "六百年藥房", "市政廳藥局",
     "蛇杖藥缽旁「Apteek ad. 1422」幾個字沉甸甸掛著，歐洲仍在營業的古老藥局之一。翻開架上植物圖鑑，紙頁發出細響。原來買藥也能買進時間……",
     "蛇杖藥缽旁「Apteek ad. 1422」幾個字沉甸甸掛著，歐洲仍在營業的古老藥局之一。翻開架上植物圖鑑，紙頁發出細響。原來買藥也能買進時間——六百年的處方，從指尖翻過。",
     "自 1422 年"),
    ("tallinn-victory-column.jpg", "35 · Tallinn", "自由十字", "獨立戰爭勝利紀念柱",
     "玻璃柱頂托起自由十字，藍黑白國旗在風裡排開；前景綠陶甕浮雕三獅國徽，光從柱身穿過……",
     "玻璃柱頂托起自由十字，藍黑白國旗在風裡排開；前景綠陶甕浮雕三獅國徽，光從柱身穿過。廣場忽然安靜半拍。歡笑之外，塔林也會把沉默站成一根柱。",
     "獨立戰爭勝利紀念柱"),
    ("tallinn-kiek-in-de-kok.jpg", "36 · Tallinn", "砲口風景", "窺視廚房塔",
     "鐵砲架在拱窗前，槍口外樹梢與石塔剪影一層層退開；五樓風比樓下乾脆……",
     "鐵砲架在拱窗前，槍口外樹梢與石塔剪影一層層退開；五樓風比樓下乾脆。老城屋頂像被攤在掌心。原來最好的城市景觀，有時是從砲口望出去的那一整片綠與石。",
     "Kiek in de Kök 五樓景觀"),
    ("tallinn-city-wall-towers.jpg", "37 · Tallinn", "雙塔防線", "城牆雙塔",
     "方塔與圓塔各戴紅瓦頂，風向標在陰天裡慢慢轉；草坡、石燈並列，腳步順著防禦線走……",
     "方塔與圓塔各戴紅瓦頂，風向標在陰天裡慢慢轉；草坡、石燈並列，腳步順著防禦線走。每轉一個彎，光影就換一幕。保存完整的中世紀城，讀起來不是名詞，是這種連續的轉折。",
     "塔林城牆"),
    ("tallinn-alexander-nevsky-bingge.jpg", "38 · Tallinn", "洋蔥頂", "亞歷山大涅夫斯基教堂",
     "粉紅與白石托起深色洋蔥頂，金十字在上城堡壘前發亮，十九世紀帝國風格把天際線切開另一道口。仰拍穹頂，頸子酸了一下。老城之上，還有一種信仰的輪廓……",
     "粉紅與白石托起深色洋蔥頂，金十字在上城堡壘前發亮，十九世紀帝國風格把天際線切開另一道口。仰拍穹頂，頸子酸了一下。老城之上，還有一種信仰的輪廓——對比鮮明，卻並肩站著。",
     "亞歷山大涅夫斯基教堂"),
    ("tallinn-cow-bench-bingge.jpg", "39 · Tallinn", "街邊幽默", "坐姿銅牛",
     "街邊長椅上，銅牛翹腿坐得跟人一樣自在，金屬在陰天裡帶一點冷靜的幽默。挨著牠坐下，肩並肩。照片忽然變輕……",
     "街邊長椅上，銅牛翹腿坐得跟人一樣自在，金屬在陰天裡帶一點冷靜的幽默。挨著牠坐下，肩並肩。照片忽然變輕——公共藝術最好的功能，也許是讓路人有地方笑一下。",
     "公共藝術銅牛"),
    ("tallinn-danish-king-garden-monks.jpg", "40 · Tallinn", "花園修士", "丹麥國王花園",
     "頭罩修士銅像站在石牆與卵石之間，樹影壓下來，傳說與修道院記憶鑄成沉默；丹麥旗起源的故事也在這座花園裡呼吸……",
     "頭罩修士銅像站在石牆與卵石之間，樹影壓下來，傳說與修道院記憶鑄成沉默；丹麥旗起源的故事也在這座花園裡呼吸。熱鬧廣場走完，這裡像一口井。中世紀的另一種靜，涼涼的，剛好夠喝。",
     "丹麥國王花園"),
    ("tallinn-kaarli-church.jpg", "41 · Tallinn", "雙塔剪影", "卡利教堂",
     "高處望去，雙塔並立，綠屋頂十字架微微發亮，樹冠鋪在前景像柔焦。新城與老城之間，這對尖頂成了天際線的第二句話。遠看有時比走近更像告別……",
     "高處望去，雙塔並立，綠屋頂十字架微微發亮，樹冠鋪在前景像柔焦。新城與老城之間，這對尖頂成了天際線的第二句話。遠看有時比走近更像告別——也像約定下次再來。",
     "Kaarli kirik"),
    ("tallinn-olde-hansa-exterior.jpg", "42 · Tallinn", "漢莎門面", "Olde Hansa",
     "白牆哥德字與鐵籠燈先把傍晚點亮，紋章旗垂在門邊，風一吹就沙沙響……",
     "白牆哥德字與鐵籠燈先把傍晚點亮，紋章旗垂在門邊，風一吹就沙沙響。復古餐廳的門面把時代感擺得很整齊。推門前拍下招牌：燈光一亮，今晚的故事才掀開第一頁。",
     "Olde Hansa"),
    ("tallinn-olde-hansa-interior-bingge.jpg", "43 · Tallinn", "中古裝潢", "漢莎廚房",
     "木吧台後，仿中古服飾的笑容先迎上來；壁畫、陶壺與木雕把空間鋪成漢薩商站，餐具與上菜也放慢半拍……",
     "木吧台後，仿中古服飾的笑容先迎上來；壁畫、陶壺與木雕把空間鋪成漢薩商站，餐具與上菜也放慢半拍。走進這一幕，手錶忽然多餘。旅行最奢侈的，有時是假裝活在另一個世紀。",
     "漢莎主題餐廳內裝"),
    ("tallinn-olde-hansa-meat-feast.jpg", "44 · Tallinn", "招牌肉排", "漢莎晚餐",
     "燭光先暖了桌面：肉凍、黑麵包、紅陶碗裡的肉絲與泥蓉，薄脆餅咔嚓一聲；現場音樂繞著木桌走……",
     "燭光先暖了桌面：肉凍、黑麵包、紅陶碗裡的肉絲與泥蓉，薄脆餅咔嚓一聲；現場音樂繞著木桌走。肉排上來時，刀切聲比人聲清楚。中世紀的一天，原來可以用一頓飯慢慢收掉燈。",
     "Olde Hansa 招牌肉排"),
]

DAY10 = [
    ("tallinn-open-air-thatch-roof-bingge.jpg", "45 · Tallinn", "茅草小山", "露天博物館茅草頂",
     "草香先到，茅草頂厚得誇張，層層草束堆成一座小山，屋簷陰影涼涼壓下來。傳統農舍把保暖做成看得見的厚度。伸手比著屋簷量了一下……",
     "草香先到，茅草頂厚得誇張，層層草束堆成一座小山，屋簷陰影涼涼壓下來。傳統農舍把保暖做成看得見的厚度。伸手比著屋簷量了一下——賦歸前的早晨，尺度感比鬧鐘準。",
     "露天博物館農舍"),
    ("tallinn-open-air-farmhouse-bingge.jpg", "46 · Tallinn", "原木農舍", "露天博物館農舍",
     "原木農舍一排排站在草地，陡峭茅草頂幾乎垂到門廊，松林擋在屋後發出細響。首都近郊把農村生活的尺度整排攤開。慢慢走過去拍照，想帶走一點「日常」……",
     "原木農舍一排排站在草地，陡峭茅草頂幾乎垂到門廊，松林擋在屋後發出細響。首都近郊把農村生活的尺度整排攤開。慢慢走過去拍照，想帶走一點「日常」——離開前，反而最需要這種不趕路的風景。",
     "露天博物館"),
    ("tallinn-open-air-well-sweep.jpg", "47 · Tallinn", "取水智慧", "桔槔水井",
     "苔蘚爬滿小木屋屋頂，長槓一翹就能讓木桶探井，綠草與松林把裝置襯得很安靜。舊時取水的智慧就立在草坪上。原來便利以前長這樣……",
     "苔蘚爬滿小木屋屋頂，長槓一翹就能讓木桶探井，綠草與松林把裝置襯得很安靜。舊時取水的智慧就立在草坪上。原來便利以前長這樣——費一點力，水才顯得珍貴。",
     "傳統桔槔"),
    ("tallinn-open-air-cat-bingge.jpg", "48 · Tallinn", "農場貓", "露天農場貓咪",
     "木桶托在手上，黑白貓卻在腳邊呼呼大睡，白尾尖偶爾顫一下……",
     "木桶托在手上，黑白貓卻在腳邊呼呼大睡，白尾尖偶爾顫一下。指著牠拍照，連呼吸都放輕。賦歸路上大概會記得：最後一天的輕鬆，是一隻拒絕睜眼的貓。",
     "露天農場"),
    ("tallinn-baltic-sea-bingge.jpg", "49 · Tallinn", "終於見海", "波羅的海",
     "灰色海面一直鋪到對岸吊臂，風從水面拍上來，鹹意比名字先到。旅程叫波羅的海三國，卻拖到最後一天才真正看見海。按下快門時想笑……",
     "灰色海面一直鋪到對岸吊臂，風從水面拍上來，鹹意比名字先到。旅程叫波羅的海三國，卻拖到最後一天才真正看見海。按下快門時想笑——原來這片海，也會遲到。",
     "波羅的海"),
    ("estonia-chicken-skewer-lunch.jpg", "50 · Tallinn", "賦歸午餐", "烤肉串",
     "烤雞串的焦香先竄鼻，花椰菜、櫛瓜與紅椒躺在醬汁裡，顏色比菜單誠實……",
     "烤雞串的焦香先竄鼻，花椰菜、櫛瓜與紅椒躺在醬汁裡，顏色比菜單誠實。賦歸前這一餐，味道落得很踏實。吃完拉行李箱，輪子好像也輕了一點。",
     "愛沙尼亞式烤肉串"),
    ("tallinn-balti-jaama-turg-bingge.jpg", "51 · Tallinn", "市集門口", "Balti Jaama 市場",
     "「TURG」兩個字先撞進眼，金屬球雕塑在廣場慢慢轉，光斑一晃一晃……",
     "「TURG」兩個字先撞進眼，金屬球雕塑在廣場慢慢轉，光斑一晃一晃。豎起大拇指，市場門面已經回了禮。起飛前的最後一圈，從這道旋轉的門口進去就對了。",
     "Balti Jaama Turg"),
    ("tallinn-fish-market-berries.jpg", "52 · Tallinn", "果籃顏色", "漁人市場水果攤",
     "草莓、藍莓、紅醋栗與醋栗一盒盒排開，顏色豐盛得讓人想全買，標價卻冷靜提醒現實。湊近聞一口果酸。旅程結束前，口袋裡最好還留一點甜……",
     "草莓、藍莓、紅醋栗與醋栗一盒盒排開，顏色豐盛得讓人想全買，標價卻冷靜提醒現實。湊近聞一口果酸。旅程結束前，口袋裡最好還留一點甜——貴一點，也算跟塔林道別。",
     "漁人市場"),
]


def pack_day910():
    for slug, stamp, locale, title, teaser, body, fact in DAY9:
        CARDS.append({
            "stamp": stamp, "locale": locale, "title": title,
            "teaser": teaser, "body": body, "fact": fact,
            "photo": f"day09/{slug}", "day": "day09", "slug": slug, "md_title": title,
        })
    for slug, stamp, locale, title, teaser, body, fact in DAY10:
        CARDS.append({
            "stamp": stamp, "locale": locale, "title": title,
            "teaser": teaser, "body": body, "fact": fact,
            "photo": f"day10/{slug}", "day": "day10", "slug": slug, "md_title": title,
        })


def render_html(cards: list[dict]) -> str:
    parts = []
    for c in cards:
        photo = c["photo"]
        abs_photo = PHOTOS / photo
        if not abs_photo.exists():
            # fallback for renamed seal / leaning-house aliases
            if photo.endswith("tartu-supreme-court-seal.jpg"):
                for alt in (
                    "day07/tartu-chess-pieces.jpg",
                    "day07/tartu-thumbtack-sculpture.jpg",
                ):
                    if (PHOTOS / alt).exists():
                        photo = alt
                        break
            elif photo.endswith("tartu-leaning-house.jpg"):
                if (PHOTOS / "day07/tartu-town-hall-square.jpg").exists():
                    photo = "day07/tartu-town-hall-square.jpg"
            elif photo.endswith("tartu-chess-pieces.jpg") or photo.endswith(
                "tartu-thumbtack-sculpture.jpg"
            ):
                if (PHOTOS / "day07/tartu-supreme-court-seal.jpg").exists():
                    photo = "day07/tartu-supreme-court-seal.jpg"
            elif photo.endswith("tartu-town-hall-square.jpg"):
                if (PHOTOS / "day07/tartu-leaning-house.jpg").exists():
                    photo = "day07/tartu-leaning-house.jpg"
        img = f'../photos/bldh-trio/{photo}'
        # for deploy at site root use /photos/...
        img_web = f'photos/bldh-trio/{photo}'
        parts.append(f'''  <div class="card" onclick="this.classList.toggle('open')">
    <div class="card-head">
      <span class="stamp">{html.escape(c["stamp"])}</span>
      <span class="locale">{html.escape(c["locale"])}</span>
    </div>
    <div class="card-photo" style="background-image:url('{img_web}')"></div>
    <div class="card-title">{html.escape(c["title"])}</div>
    <div class="card-teaser">{html.escape(c["teaser"])}</div>
    <div class="expand-hint"><span class="arrow">▸</span>展開全文</div>
    <div class="card-body"><div class="card-body-inner">
      {html.escape(c["body"])}
      <div class="fact">{html.escape(c["fact"])}</div>
    </div></div>
  </div>''')

    cards_html = "\n\n".join(parts)
    return f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>愛沙尼亞行紀 — 互動札記</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;600;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Noto+Sans+TC:wght@300;400;500&display=swap');
  :root{{
    --ink:#1c2b28; --parchment:#f2ede1; --moss:#3f5d4e; --moss-deep:#28392f;
    --rust:#a8623f; --line:#c9bfa8;
    --paper-shadow: 0 18px 40px -20px rgba(28,43,40,.45);
  }}
  *{{box-sizing:border-box; margin:0; padding:0;}}
  body{{
    background: radial-gradient(ellipse at top left, #3a4f45 0%, #1c2b28 55%), var(--ink);
    background-attachment:fixed; color:var(--ink);
    font-family:'Noto Sans TC', sans-serif; padding:48px 20px 120px; min-height:100vh;
  }}
  .masthead{{ max-width:760px; margin:0 auto 40px; text-align:center; color:var(--parchment); }}
  .masthead .eyebrow{{
    font-family:'Cormorant Garamond', serif; font-style:italic; letter-spacing:.35em;
    text-transform:uppercase; font-size:12px; opacity:.7; margin-bottom:14px;
  }}
  .masthead h1{{
    font-family:'Noto Serif TC', serif; font-weight:700;
    font-size:clamp(32px,6vw,52px); line-height:1.25;
  }}
  .masthead .route{{
    margin-top:16px; font-family:'Cormorant Garamond', serif; font-size:19px; opacity:.75;
  }}
  .masthead .route span{{ padding:0 10px; }}
  .masthead .note{{
    margin-top:14px; font-size:13px; opacity:.55; letter-spacing:.04em;
  }}
  .back{{
    display:inline-block; margin-bottom:18px; color:var(--parchment); opacity:.7;
    text-decoration:none; font-size:13px; letter-spacing:.08em;
  }}
  .back:hover{{ opacity:1; }}
  .deck{{ max-width:760px; margin:0 auto; display:flex; flex-direction:column; gap:36px; }}
  .card{{
    background:var(--parchment); border-radius:2px; box-shadow:var(--paper-shadow);
    position:relative; overflow:hidden; cursor:pointer;
    transition:transform .35s cubic-bezier(.2,.8,.2,1);
  }}
  .card:hover{{ transform:translateY(-4px); }}
  .card::before{{
    content:""; position:absolute; inset:10px; border:1px solid var(--line); pointer-events:none; z-index:2;
  }}
  .card-head{{
    display:flex; align-items:baseline; justify-content:space-between;
    padding:26px 30px 0; position:relative; z-index:1;
  }}
  .stamp{{
    font-family:'Cormorant Garamond', serif; font-size:13px; letter-spacing:.2em;
    text-transform:uppercase; color:var(--moss); border:1px solid var(--moss);
    border-radius:999px; padding:4px 12px;
  }}
  .locale{{
    font-family:'Cormorant Garamond', serif; font-style:italic; font-size:15px; color:var(--rust);
  }}
  .card-photo{{
    margin:16px 30px 0; height:220px; border-radius:2px;
    background-size:cover; background-position:center; position:relative; z-index:1;
  }}
  .card-title{{
    font-family:'Noto Serif TC', serif; font-weight:700; font-size:26px;
    padding:14px 30px 6px; color:var(--moss-deep); position:relative; z-index:1;
  }}
  .card-teaser{{
    padding:0 30px 18px; font-size:15px; line-height:1.9; color:#3a3530; position:relative; z-index:1;
  }}
  .expand-hint{{
    padding:0 30px 24px; font-size:12.5px; color:var(--rust); letter-spacing:.08em;
    display:flex; align-items:center; gap:6px; position:relative; z-index:1;
  }}
  .expand-hint .arrow{{ transition:transform .3s ease; display:inline-block; }}
  .card.open .expand-hint .arrow{{ transform:rotate(90deg); }}
  .card-body{{
    max-height:0; overflow:hidden; transition:max-height .5s ease;
    border-top:1px dashed var(--line); position:relative; z-index:1;
  }}
  .card.open .card-body{{ max-height:800px; }}
  .card-body-inner{{
    padding:26px 30px 32px; font-size:15.5px; line-height:2; color:#2b2620;
  }}
  .card-body-inner .fact{{
    margin-top:16px; padding-top:14px; border-top:1px dotted var(--line);
    font-family:'Cormorant Garamond', serif; font-size:15.5px; font-style:italic; color:var(--moss);
  }}
  footer{{
    max-width:760px; margin:60px auto 0; text-align:center; color:var(--parchment);
    opacity:.5; font-family:'Cormorant Garamond', serif; font-style:italic;
    font-size:13px; letter-spacing:.15em;
  }}
  @media(max-width:520px){{
    .card-head, .card-title, .card-teaser, .expand-hint, .card-body-inner, .card-photo{{ margin-left:0; margin-right:0; padding-left:22px; padding-right:22px; }}
    .card-photo{{ margin:16px 22px 0; height:180px; }}
  }}
</style>
</head>
<body>
<div class="masthead">
  <a class="back" href="trips/bldh-trio.html">← 返回波羅的海旅程</a>
  <div class="eyebrow">Journal · Eesti</div>
  <h1>石與貓的國度</h1>
  <div class="route">塔圖 <span>·</span> 維爾揚迪 <span>·</span> 派爾努 <span>·</span> 塔林</div>
  <div class="note">點卡片展開全文 · 資深旅遊作家札記（v1.2）</div>
</div>
<div class="deck">
{cards_html}
</div>
<footer>— Eesti, 2026 — · {len(cards)} 則札記</footer>
</body>
</html>
'''


def sync_markdown(cards: list[dict]) -> None:
    """Replace EE card bodies in day07–10 with short journal texts."""
    by_day: dict[str, list[dict]] = {}
    for c in cards:
        by_day.setdefault(c["day"], []).append(c)

    # day07: keep Latvia cards; replace Estonia section from AHHAA onward
    d7 = CONTENT / "day07.md"
    text = d7.read_text(encoding="utf-8")
    # split at first EE card
    marker = "### ![AHHAA"
    if marker in text:
        head = text.split(marker)[0]
    else:
        head = text
    lines = [head.rstrip(), ""]
    def card_heading(day: str, c: dict, photo: str) -> str:
        vid = c.get("video")
        suffix = f"{{video={vid}}}" if vid else ""
        return f"### ![{c['md_title']}]({day}/{photo}){suffix} {c['md_title']}"

    for c in by_day.get("day07", []):
        photo = c["slug"]
        # renamed seal sculpture aliases
        if photo in (
            "tartu-chess-pieces.jpg",
            "tartu-thumbtack-sculpture.jpg",
        ) and not (PHOTOS / "day07" / photo).exists():
            photo = "tartu-supreme-court-seal.jpg"
        elif photo == "tartu-supreme-court-seal.jpg" and not (
            PHOTOS / "day07" / photo
        ).exists():
            for alt in ("tartu-chess-pieces.jpg", "tartu-thumbtack-sculpture.jpg"):
                if (PHOTOS / "day07" / alt).exists():
                    photo = alt
                    break
        elif photo == "tartu-town-hall-square.jpg" and not (
            PHOTOS / "day07" / photo
        ).exists():
            photo = "tartu-leaning-house.jpg"
        elif photo == "tartu-leaning-house.jpg" and not (
            PHOTOS / "day07" / photo
        ).exists():
            if (PHOTOS / "day07" / "tartu-town-hall-square.jpg").exists():
                photo = "tartu-town-hall-square.jpg"
        lines.append(card_heading("day07", c, photo))
        lines.append(c["body"])
        lines.append("")
    d7.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    for day in ("day08", "day09", "day10"):
        path = CONTENT / f"{day}.md"
        raw = path.read_text(encoding="utf-8")
        # keep header through ## 古蹟
        m = re.search(r"(^# .*?\n:::meta.*?\n\n## 古蹟\n)", raw, re.S | re.M)
        if not m:
            continue
        head = m.group(1)
        parts = [head.rstrip(), ""]
        for c in by_day.get(day, []):
            parts.append(card_heading(day, c, c["slug"]))
            parts.append(c["body"])
            parts.append("")
        path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    pack_day910()
    # verify photos
    missing = []
    for c in CARDS:
        p = PHOTOS / c["photo"]
        if not p.exists() and c["photo"].endswith("tartu-supreme-court-seal.jpg"):
            for alt in (
                "day07/tartu-chess-pieces.jpg",
                "day07/tartu-thumbtack-sculpture.jpg",
            ):
                if (PHOTOS / alt).exists():
                    p = PHOTOS / alt
                    break
        if not p.exists():
            missing.append(c["photo"])
    if missing:
        print("MISSING", missing)
    OUT_HTML.write_text(render_html(CARDS), encoding="utf-8")
    sync_markdown(CARDS)
    print(f"Wrote {OUT_HTML} ({len(CARDS)} cards)")
    print("Synced day07–10.md")


if __name__ == "__main__":
    main()
