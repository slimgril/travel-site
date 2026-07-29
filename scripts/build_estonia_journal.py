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
# Style: 壓縮四拍（當下→故事→雜記→收尾；CONTENT_STYLE v1.1）
CARDS: list[dict] = [
    # —— Day 7 進入愛沙尼亞（塔圖／維爾揚迪）——
    {
        "stamp": "01 · Tartu",
        "locale": "科學門口",
        "title": "AHHAA 門前的火箭",
        "teaser": "一跨進愛沙尼亞，塔圖科學中心門口就豎著一支白色火箭，直直指著藍天。……",
        "body": "一跨進愛沙尼亞，塔圖科學中心門口就豎著一支白色火箭，直直指著藍天。AHHAA 強調動手學科學，連入口地標都像實驗道具。舉手遮一下光，跟它打了聲招呼——還沒進門，人已經先笑了。",
        "fact": "地點 — AHHAA 科學中心 ／ 造形 — ESA 火箭模型",
        "photo": "day07/ahhaa-rocket-bingge.jpg",
        "day": "day07",
        "slug": "ahhaa-rocket-bingge.jpg",
        "md_title": "AHHAA 科學中心火箭",
    },
    {
        "stamp": "02 · Tartu",
        "locale": "大學城客廳",
        "title": "市政廳廣場",
        "teaser": "石板廣場在午後發亮，三角旗輕輕晃，咖啡座圍成一圈。這裡是塔圖的幾何中心，也是大學城的公共客廳。停下腳步讓鞋底先量尺度——……",
        "body": "石板廣場在午後發亮，三角旗輕輕晃，咖啡座圍成一圈。這裡是塔圖的幾何中心，也是大學城的公共客廳。停下腳步讓鞋底先量尺度——整座城的節奏，好像從這裡開始。",
        "fact": "位置 — 塔圖市政廳廣場",
        "photo": "day07/tartu-town-hall-square.jpg",
        "day": "day07",
        "slug": "tartu-town-hall-square.jpg",
        "md_title": "塔圖市政廳廣場",
    },
    {
        "stamp": "03 · Tartu",
        "locale": "噴泉上的學生",
        "title": "接吻學生噴泉",
        "teaser": "噴泉上，一對撐傘擁吻的銅像被水柱包圍，粉紅市政廳當背景。雕塑家 Mati Karmin 1998 年完成——……",
        "body": "噴泉上，一對撐傘擁吻的銅像被水柱包圍，粉紅市政廳當背景。雕塑家 Mati Karmin 1998 年完成——紀念的不是帝王，而是大學城的日常主角。坐在池邊看水花，覺得這座城把「學生」放得很正面。",
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
        "teaser": "白色圓柱與三角山牆撐起門面，國旗在屋頂輕揚。創校於 1632 年，眼前主樓是十九世紀初古典主義重建。抬頭望柱廊，整座城的書卷氣好像從這裡散開——……",
        "body": "白色圓柱與三角山牆撐起門面，國旗在屋頂輕揚。創校於 1632 年，眼前主樓是十九世紀初古典主義重建。抬頭望柱廊，整座城的書卷氣好像從這裡散開——走在大學城，連腳步都會不自覺放慢。",
        "fact": "創校 1632 ／ 主樓建築師 — Johann Wilhelm Krause",
        "photo": "day07/tartu-university.jpg",
        "day": "day07",
        "slug": "tartu-university.jpg",
        "md_title": "塔圖大學主樓",
    },
    {
        "stamp": "05 · Tartu",
        "locale": "棋局一隅",
        "title": "巨大的棋子",
        "teaser": "市區走著走著，忽然冒出放大版西洋棋棋子，安靜立在原地。……",
        "body": "市區走著走著，忽然冒出放大版西洋棋棋子，安靜立在原地。愛沙尼亞出過國際象棋大師，街頭出現這樣的裝置也不意外。站在棋子旁拍照，像自己也成了棋盤上一員——塔圖連街景都帶一點遊戲感。",
        "fact": "造型 — 放大版西洋棋棋子裝置 ／ 位置 — 塔圖市區",
        "photo": "day07/tartu-chess-pieces.jpg",
        "day": "day07",
        "slug": "tartu-chess-pieces.jpg",
        "md_title": "巨大的棋子",
        "replace_old_slug": "tartu-thumbtack-sculpture.jpg",
    },
    {
        "stamp": "06 · Tartu",
        "locale": "殘缺的尖拱",
        "title": "主教座堂遺址",
        "teaser": "戰後殘留的紅磚拱廊直指天空，尖拱之間長出青草。……",
        "body": "戰後殘留的紅磚拱廊直指天空，尖拱之間長出青草。這座哥德大教堂沒被修回完整，而是保留成可進入的廢墟。站在廊道裡抬頭，空曠與光反而比完整教堂更安靜——有些美，就該留缺口。",
        "fact": "原為磚造哥德主教座堂 ／ 現為遺址公園",
        "photo": "day07/tartu-cathedral-ruins-bingge.jpg",
        "day": "day07",
        "slug": "tartu-cathedral-ruins-bingge.jpg",
        "md_title": "塔圖主教座堂遺址",
    },
    {
        "stamp": "07 · Tartu",
        "locale": "廢墟上的木棧",
        "title": "主教座堂塔樓廊道",
        "teaser": "再往裡走，磚牆高處架著木棧道，尖拱門外透出綠樹。……",
        "body": "再往裡走，磚牆高處架著木棧道，尖拱門外透出綠樹。新結構故意保持輕、可逆，不假裝自己是中世紀的一部分。背靠遺址合影，把這段被時間撕開又被留下的輪廓記下來。",
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
        "teaser": "粉紅立面、鐘樓與花箱在傍晚光裡發亮，愛沙尼亞與歐盟旗並排。……",
        "body": "粉紅立面、鐘樓與花箱在傍晚光裡發亮，愛沙尼亞與歐盟旗並排。十八世紀末的古典主義市政建築，是廣場最清楚的城市名片。繞了一圈，最後還是回到這棟最像塔圖的房子前面。",
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
        "teaser": "入夜前來到湖畔：跳台上層給大人、下層給小朋友，有人正從高處躍下，水面濺起圓圈。湖岸運動氣息很濃。停下腳步看一場北歐夏夜的勇氣練習——……",
        "body": "入夜前來到湖畔：跳台上層給大人、下層給小朋友，有人正從高處躍下，水面濺起圓圈。湖岸運動氣息很濃。停下腳步看一場北歐夏夜的勇氣練習——水花一散，天色也跟著軟了。",
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
        "teaser": "市政廳旁階梯口，傳奇市長 August Maramaa 牽著狗站著，神情像下一秒就要邁步。……",
        "body": "市政廳旁階梯口，傳奇市長 August Maramaa 牽著狗站著，神情像下一秒就要邁步。雕塑家 Aili Vahtrapuu 2007 年完成；據說市長任內把維爾揚迪往度假小城打磨。站在雕像前，好像還摸得到那份用心。",
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
        "teaser": "綠頂八角木屋架在紅磚圓塔上，街樹夾道，天色開始轉淡。二十世紀初的供水設施，如今成了小鎮地標。仰拍整座水塔——……",
        "body": "綠頂八角木屋架在紅磚圓塔上，街樹夾道，天色開始轉淡。二十世紀初的供水設施，如今成了小鎮地標。仰拍整座水塔——一天的尾聲，就這樣安靜立在天際線上。",
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
        "teaser": "才踏出車子，就被路邊水泥貓逗笑了——原來這些矮胖柱子是阻車樁，擋車別開進行人區。……",
        "body": "才踏出車子，就被路邊水泥貓逗笑了——原來這些矮胖柱子是阻車樁，擋車別開進行人區。城市藝術家 Kristi Kangilaski 設計、雕塑家 Aime Kuulbusch 做出來，連市徽都看得到貓。幾乎每個轉角都能撞見一隻，忍不住一路拍下去；進愛沙尼亞的第一晚，就被貓接駕了。",
        "fact": "設計 — Kristi Kangilaski ／ 雕塑 — Aime Kuulbusch",
        "photo": "day07/viljandi-cat-sculpture-bingge.jpg",
        "day": "day07",
        "slug": "viljandi-cat-sculpture-bingge.jpg",
        "md_title": "街頭的貓咪們",
    },
    # —— Day 8 ——
    {
        "stamp": "13 · Pärnu",
        "locale": "鐵道記憶",
        "title": "派爾努蒸汽火車頭",
        "teaser": "清晨走進街角，綠黑車身、鮮紅保險槓的窄軌蒸汽火車頭 №5 安靜停在短軌上，腳邊還蹲著一座白色小象。……",
        "body": "清晨走進街角，綠黑車身、鮮紅保險槓的窄軌蒸汽火車頭 №5 安靜停在短軌上，腳邊還蹲著一座白色小象。這是度假海灣小鎮留住的一段鐵路記憶。我們先與它打個照面——一天從一座不會再開動的火車開始，節奏反而剛好。",
        "fact": "窄軌蒸汽火車頭 №5",
        "photo": "day08/parnu-locomotive-no5.jpg",
        "day": "day08",
        "slug": "parnu-locomotive-no5.jpg",
        "md_title": "派爾努蒸汽火車頭",
    },
    {
        "stamp": "14 · Pärnu",
        "locale": "老街尖頂",
        "title": "紅頂塔樓",
        "teaser": "樹蔭步道旁，白牆一側豎起灰石圓塔，塔頂是陡峭紅瓦尖頂。單車騎過石徑，藍天剛好襯著塔尖。跟著領隊慢慢走，把派爾努午前的節奏先收進鏡頭——……",
        "body": "樹蔭步道旁，白牆一側豎起灰石圓塔，塔頂是陡峭紅瓦尖頂。單車騎過石徑，藍天剛好襯著塔尖。跟著領隊慢慢走，把派爾努午前的節奏先收進鏡頭——小鎮的美，常常藏在轉角。",
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
        "teaser": "騎士街一帶，奶油色 Café Grand 撐開米白陽傘，花壇紅白相間，國旗在牆邊輕揚。遠方教堂尖頂探進視野——……",
        "body": "騎士街一帶，奶油色 Café Grand 撐開米白陽傘，花壇紅白相間，國旗在牆邊輕揚。遠方教堂尖頂探進視野——避暑小鎮的門面就長這樣。忍不住多停一眼，咖啡香還沒聞，人已經先被街景留住。",
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
        "teaser": "抬頭望見洋蔥頭尖頂與十字，石砌塔身一層層往藍天疊上去。這是派爾努的東正教地標。樹影落在肩上，我們在塔下仰拍合影——……",
        "body": "抬頭望見洋蔥頭尖頂與十字，石砌塔身一層層往藍天疊上去。這是派爾努的東正教地標。樹影落在肩上，我們在塔下仰拍合影——信仰的輪廓，先從這一柱天際線讀起。",
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
        "teaser": "整座教堂以黃磚與紅褐飾帶砌成，多座洋蔥頂鍍金十字並列，圍欄尖刺在陽光裡發亮。繞到正面再拍一張，讓濱海小鎮的信仰輪廓完整落進眼底——……",
        "body": "整座教堂以黃磚與紅褐飾帶砌成，多座洋蔥頂鍍金十字並列，圍欄尖刺在陽光裡發亮。繞到正面再拍一張，讓濱海小鎮的信仰輪廓完整落進眼底——同一座教堂，遠看與近看是兩種溫度。",
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
        "teaser": "午後走近一尊握著舵輪的銅像——基赫努傳奇船長 Kihnu Jõnn。……",
        "body": "午後走近一尊握著舵輪的銅像——基赫努傳奇船長 Kihnu Jõnn。座銘寫他對好船的讚嘆：船行得叫海都抱怨。雕塑把水手的堅毅與幽默鑄在一起。站在港邊風裡，覺得航海精神還站在這裡。",
        "fact": "Kihnu Jõnn（Enn Uuetoa）",
        "photo": "day08/parnu-kihnu-jonn-statue.jpg",
        "day": "day08",
        "slug": "parnu-kihnu-jonn-statue.jpg",
        "md_title": "基赫努船長雕像",
    },
    {
        "stamp": "19 · Pärnu",
        "locale": "河岸雙手",
        "title": "派爾努雙手雕塑",
        "teaser": "河岸步道上，兩隻巨大金屬手掌從岩石升起，指尖幾乎相觸；對岸綠屋頂民宅沿河排開。……",
        "body": "河岸步道上，兩隻巨大金屬手掌從岩石升起，指尖幾乎相觸；對岸綠屋頂民宅沿河排開。伸手比個距離，也把這組「相遇／守護」的公共藝術留在今天的灣區漫步裡——原來海邊也可以很溫柔。",
        "fact": "公共藝術 ／ 相遇與守護",
        "photo": "day08/parnu-hands-sculpture-bingge.jpg",
        "day": "day08",
        "slug": "parnu-hands-sculpture-bingge.jpg",
        "md_title": "派爾努雙手雕塑",
    },
    {
        "stamp": "20 · Pärnu",
        "locale": "海灣一小時",
        "title": "派爾努灣遊艇",
        "teaser": "登上白色帆船「JÄÄLIND」（翠鳥），桅杆收在一側，船身劃開深藍水面。……",
        "body": "登上白色帆船「JÄÄLIND」（翠鳥），桅杆收在一側，船身劃開深藍水面。約一小時海灣巡航，岸邊綠樹與小艇排成一列。風與浪把派爾努的海岸線慢慢講完——在陸地上走了一早，終於把身體交給海。",
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
        "teaser": "中午坐下：烤鴨切片粉嫩帶皮、Saku 啤酒、鮮蔬沙拉，再配黑麵包與草莓冰淇淋。醬汁溫熱、麥香清楚——……",
        "body": "中午坐下：烤鴨切片粉嫩帶皮、Saku 啤酒、鮮蔬沙拉，再配黑麵包與草莓冰淇淋。醬汁溫熱、麥香清楚——進入度假灣的節奏，先落到味覺上。這一餐吃完，下午的塔林就更有盼頭。",
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
        "teaser": "傍晚抵達塔林，石砌拱門上方掛著「MOON RESTORAN」，牆邊紅標寫著 Michelin 推薦。紫花盆栽夾道——……",
        "body": "傍晚抵達塔林，石砌拱門上方掛著「MOON RESTORAN」，牆邊紅標寫著 Michelin 推薦。紫花盆栽夾道——推門進去前，先為今晚這頓期待拍下門口。首都第一晚，從一塊招牌開始。",
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
        "teaser": "餐盤輪流上來：酥皮白魚、烤南瓜石榴沙拉，還有蛋白霜與乳霜甜點。刀切開魚肉時外酥內嫩——……",
        "body": "餐盤輪流上來：酥皮白魚、烤南瓜石榴沙拉，還有蛋白霜與乳霜甜點。刀切開魚肉時外酥內嫩——層次慢慢落在舌尖。在塔林的第一晚，這頓推薦餐把旅途的疲憊也一起煮軟了。",
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
        "teaser": "廣場上，藝術家 Simson von Seakyl 的混凝土狼仰頭長嚎，幾何塊面把野性收成雕塑。側身學它抬頭——……",
        "body": "廣場上，藝術家 Simson von Seakyl 的混凝土狼仰頭長嚎，幾何塊面把野性收成雕塑。側身學它抬頭——在塔林街頭，與這隻「電影之狼」一起對天空喊一聲。抵達首都的夜晚，忽然很有電影感。",
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
        "teaser": "超市裡停著一輛亮黃 Delice 三輪水果車，葡萄、檸檬與水蜜桃堆在後斗。同行人手裡舉著蘋果與葡萄，大家被這份可愛逗得笑出來——……",
        "body": "超市裡停著一輛亮黃 Delice 三輪水果車，葡萄、檸檬與水蜜桃堆在後斗。同行人手裡舉著蘋果與葡萄，大家被這份可愛逗得笑出來——大景點之外，這種小東西才像真正旅行過。",
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
     "清晨站在兩座紅瓦圓錐頂石塔之間，石板路在腳下高低起伏——……",
     "清晨站在兩座紅瓦圓錐頂石塔之間，石板路在腳下高低起伏——維魯城門仍是進出老城最熟悉的門面。雙臂交叉在門檻前合影，把塔林中世紀的第一道關卡先記進今天。一踏進來，整座城像童話開場。",
     "維魯城門"),
    ("tallinn-town-hall-dragon-spout.jpg", "27 · Tallinn", "牆角之龍", "市政廳龍頭排水口",
     "抬頭看見市政廳牆角探出一隻戴金冠的綠銅龍，張口吐水、鐵支架托著下顎。中世紀建築連排水都做成守護獸。忍不住多看幾秒——……",
     "抬頭看見市政廳牆角探出一隻戴金冠的綠銅龍，張口吐水、鐵支架托著下顎。中世紀建築連排水都做成守護獸。忍不住多看幾秒——原來細節裡也住著故事。",
     "市政廳排水獸"),
    ("tallinn-holy-ghost-clock.jpg", "28 · Tallinn", "會講故事的鐘", "聖靈教堂古鐘",
     "白牆紅瓦的聖靈教堂牆面，嵌著十七世紀彩色日輪時鐘：金羅馬數字、藍白放射紋。這是老城最有名的「會講故事的鐘」。晨光裡對準指針按下快門——……",
     "白牆紅瓦的聖靈教堂牆面，嵌著十七世紀彩色日輪時鐘：金羅馬數字、藍白放射紋。這是老城最有名的「會講故事的鐘」。晨光裡對準指針按下快門——時間在塔林，顯得特別好看。",
     "十七世紀日輪時鐘"),
    ("tallinn-art-nouveau-gable.jpg", "29 · Tallinn", "曲線立面", "新藝術風山牆",
     "再往上望，灰綠飾帶托起圓窗與天使浮雕，鬍鬚面具嵌在窗下。新藝術風曲線與老城石牆並存。塔林不只中世紀，連立面裝飾都捨不得略過——……",
     "再往上望，灰綠飾帶托起圓窗與天使浮雕，鬍鬚面具嵌在窗下。新藝術風曲線與老城石牆並存。塔林不只中世紀，連立面裝飾都捨不得略過——抬頭，才不會錯過整座城。",
     "新藝術風立面"),
    ("tallinn-blackheads-door.jpg", "30 · Tallinn", "漢薩門面", "黑人頭兄弟會大門",
     "石拱門上雙獅扶盾，門楣飾著摩爾人頭像；綠門配紅斜紋與金花釘。……",
     "石拱門上雙獅扶盾，門楣飾著摩爾人頭像；綠門配紅斜紋與金花釘。這是商人互助會「黑人頭兄弟會」的會所門面，漢薩時代氣派一整面推到眼前。我們在門前排隊拍照，覺得商人也活得很華麗。",
     "黑人頭兄弟會會所"),
    ("tallinn-three-sisters-bingge.jpg", "31 · Tallinn", "三姊妹", "三姊妹之屋",
     "三棟窄瘦山牆民宅緊緊相依，正中那棟漆成赭黃，鐵罩寫著 The Three Sisters Hotel。……",
     "三棟窄瘦山牆民宅緊緊相依，正中那棟漆成赭黃，鐵罩寫著 The Three Sisters Hotel。與里加「三兄弟」遙相呼應。在上城邊緣仰拍——姊妹宅邸站在一起，比任何解說牌都好懂。",
     "三姊妹民宅／旅館"),
    ("tallinn-town-hall-square-bingge.jpg", "32 · Tallinn", "老城心臟", "市政廳廣場尖塔",
     "走進石板廣場，市政廳細長尖塔刺進陰天；老湯瑪士風向標的傳說就在這座屋頂。……",
     "走進石板廣場，市政廳細長尖塔刺進陰天；老湯瑪士風向標的傳說就在這座屋頂。廣場中央抬頭，把塔林心臟的尺度先量進眼睛裡。如果波羅的海三國只能留一座中世紀城，我想我會選這裡。",
     "市政廳廣場"),
    ("tallinn-maiasmokk-cafe-bingge.jpg", "33 · Tallinn", "最老咖啡館", "Maiasmokk",
     "櫥窗寫著塔林最老咖啡館（1864），紙雕摩天輪以湯匙排成輻條；反射裡舊城立面疊進玻璃。在甜點招牌前側身一笑，也把這份老派甜味記一筆——……",
     "櫥窗寫著塔林最老咖啡館（1864），紙雕摩天輪以湯匙排成輻條；反射裡舊城立面疊進玻璃。在甜點招牌前側身一笑，也把這份老派甜味記一筆——歷史有時聞起來像糖。",
     "Maiasmokk 自 1864"),
    ("tallinn-town-hall-pharmacy-bingge.jpg", "34 · Tallinn", "六百年藥房", "市政廳藥局",
     "牆掛蛇杖藥缽與「Apteek ad. 1422」——……",
     "牆掛蛇杖藥缽與「Apteek ad. 1422」——歐洲仍在營業的最古老藥局之一。翻開架上植物圖鑑，在廣場邊讀一頁六百年的藥房故事。原來買藥也能買進時間。",
     "自 1422 年"),
    ("tallinn-victory-column.jpg", "35 · Tallinn", "自由十字", "獨立戰爭勝利紀念柱",
     "自由廣場上，玻璃柱頂托起自由十字，藍黑白國旗在風裡排開；前景綠陶甕浮雕三獅國徽。停下腳步，感受這座首都對獨立記憶的莊重——……",
     "自由廣場上，玻璃柱頂托起自由十字，藍黑白國旗在風裡排開；前景綠陶甕浮雕三獅國徽。停下腳步，感受這座首都對獨立記憶的莊重——歡笑之外，塔林也有沉默的一面。",
     "獨立戰爭勝利紀念柱"),
    ("tallinn-kiek-in-de-kok.jpg", "36 · Tallinn", "砲口風景", "窺視廚房塔",
     "登上「偷窺廚房」砲塔，鐵砲架在拱窗前，窗外樹梢外是修長石塔剪影。五樓視野把老城屋頂攤開。原來絕佳城市景觀，是從砲口望出去的那一整片綠與石——……",
     "登上「偷窺廚房」砲塔，鐵砲架在拱窗前，窗外樹梢外是修長石塔剪影。五樓視野把老城屋頂攤開。原來絕佳城市景觀，是從砲口望出去的那一整片綠與石——爬上去，才真正讀懂城牆。",
     "Kiek in de Kök 五樓景觀"),
    ("tallinn-city-wall-towers.jpg", "37 · Tallinn", "雙塔防線", "城牆雙塔",
     "城牆邊，方塔與圓塔各戴紅瓦頂，風向標在陰天裡靜靜轉；草坡與石燈並列。……",
     "城牆邊，方塔與圓塔各戴紅瓦頂，風向標在陰天裡靜靜轉；草坡與石燈並列。繞著防禦線走一圈，才明白塔林為何被稱作保存完整的中世紀城。每轉一個彎，都像走進下一幕。",
     "塔林城牆"),
    ("tallinn-alexander-nevsky-bingge.jpg", "38 · Tallinn", "洋蔥頂", "亞歷山大涅夫斯基教堂",
     "上城堡壘山前，粉紅與白石托起深色洋蔥頂與金十字。這座東正教大教堂是十九世紀帝國風格的代表。仰拍穹頂，把對比鮮明的天際線收進合影——……",
     "上城堡壘山前，粉紅與白石托起深色洋蔥頂與金十字。這座東正教大教堂是十九世紀帝國風格的代表。仰拍穹頂，把對比鮮明的天際線收進合影——老城之上，還有另一種信仰的輪廓。",
     "亞歷山大涅夫斯基教堂"),
    ("tallinn-cow-bench-bingge.jpg", "39 · Tallinn", "街邊幽默", "坐姿銅牛",
     "街邊長椅上，一尊銅牛翹腿坐得跟人一樣自在。挨著它坐下——……",
     "街邊長椅上，一尊銅牛翹腿坐得跟人一樣自在。挨著它坐下——公共藝術把幽默放進老城日常。今天的漫步多了一個笑點，照片也跟著輕了。",
     "公共藝術銅牛"),
    ("tallinn-danish-king-garden-monks.jpg", "40 · Tallinn", "花園修士", "丹麥國王花園",
     "頭罩修士銅像站在石牆與卵石之間——傳說與修道院記憶被鑄成沉默身影；這裡也以丹麥旗起源傳說聞名。……",
     "頭罩修士銅像站在石牆與卵石之間——傳說與修道院記憶被鑄成沉默身影；這裡也以丹麥旗起源傳說聞名。樹影壓下來，感受中世紀的另一種靜。熱鬧廣場走完，需要這樣一口安靜。",
     "丹麥國王花園"),
    ("tallinn-kaarli-church.jpg", "41 · Tallinn", "雙塔剪影", "卡利教堂",
     "午後從高處望去，卡利教堂兩座尖塔並立，綠屋頂十字架微微發亮；樹冠鋪在前景。新城與老城之間，這對雙塔成了天際線的第二句話——……",
     "午後從高處望去，卡利教堂兩座尖塔並立，綠屋頂十字架微微發亮；樹冠鋪在前景。新城與老城之間，這對雙塔成了天際線的第二句話——遠看，也是一種告別與再見。",
     "Kaarli kirik"),
    ("tallinn-olde-hansa-exterior.jpg", "42 · Tallinn", "漢莎門面", "Olde Hansa",
     "傍晚走近白牆哥德字與鐵籠燈，紋章旗垂在門邊。老城復古餐廳的門面已經把時代感擺好。推門進去前，先為今晚的中古宴拍下招牌——……",
     "傍晚走近白牆哥德字與鐵籠燈，紋章旗垂在門邊。老城復古餐廳的門面已經把時代感擺好。推門進去前，先為今晚的中古宴拍下招牌——燈光一亮，故事才剛開始。",
     "Olde Hansa"),
    ("tallinn-olde-hansa-interior-bingge.jpg", "43 · Tallinn", "中古裝潢", "漢莎廚房",
     "店內木吧台後，工作人員穿著仿中古服飾笑迎；壁畫、陶壺與木雕把空間鋪成漢薩商站，餐具與上菜也比照舊時。走進這一幕，時間感整個被調慢——……",
     "店內木吧台後，工作人員穿著仿中古服飾笑迎；壁畫、陶壺與木雕把空間鋪成漢薩商站，餐具與上菜也比照舊時。走進這一幕，時間感整個被調慢——旅行最奢侈的，有時是假裝活在另一個世紀。",
     "漢莎主題餐廳內裝"),
    ("tallinn-olde-hansa-meat-feast.jpg", "44 · Tallinn", "招牌肉排", "漢莎晚餐",
     "桌上擺開肉凍、黑麵包、紅陶碗裡的肉絲與泥蓉，還有薄脆餅；現場音樂輕輕繞著木桌。招牌肉排餐一份份上來——……",
     "桌上擺開肉凍、黑麵包、紅陶碗裡的肉絲與泥蓉，還有薄脆餅；現場音樂輕輕繞著木桌。招牌肉排餐一份份上來——在燭光裡，把塔林老城的這一頓吃成今天的句點。中世紀的一天，就該這樣收場。",
     "Olde Hansa 招牌肉排"),
]

DAY10 = [
    ("tallinn-open-air-thatch-roof-bingge.jpg", "45 · Tallinn", "茅草小山", "露天博物館茅草頂",
     "走進愛沙尼亞露天博物館，木屋茅草頂厚得誇張，層層草束堆成一座小山。傳統農舍把保暖做成看得見的厚度。伸手比著屋簷，忍不住抬頭量——……",
     "走進愛沙尼亞露天博物館，木屋茅草頂厚得誇張，層層草束堆成一座小山。傳統農舍把保暖做成看得見的厚度。伸手比著屋簷，忍不住抬頭量——賦歸前的早晨，先被草香留住。",
     "露天博物館農舍"),
    ("tallinn-open-air-farmhouse-bingge.jpg", "46 · Tallinn", "原木農舍", "露天博物館農舍",
     "草地上一排原木農舍，陡峭茅草頂幾乎垂到門廊，松樹林擋在屋後。首都近郊把農村生活的尺度整排攤開。我們慢慢走過去拍照——……",
     "草地上一排原木農舍，陡峭茅草頂幾乎垂到門廊，松樹林擋在屋後。首都近郊把農村生活的尺度整排攤開。我們慢慢走過去拍照——離開前，想把「日常」也帶走一點。",
     "露天博物館"),
    ("tallinn-open-air-well-sweep.jpg", "47 · Tallinn", "取水智慧", "桔槔水井",
     "苔蘚爬滿小木屋屋頂，旁邊豎起傳統桔槔：長槓一翹、木桶就能探井。綠草與松林襯著這套舊時取水裝置。農舍日常的智慧，靜靜立在博物館草坪上——……",
     "苔蘚爬滿小木屋屋頂，旁邊豎起傳統桔槔：長槓一翹、木桶就能探井。綠草與松林襯著這套舊時取水裝置。農舍日常的智慧，靜靜立在博物館草坪上——原來便利以前長這樣。",
     "傳統桔槔"),
    ("tallinn-open-air-cat-bingge.jpg", "48 · Tallinn", "農場貓", "露天農場貓咪",
     "蹲在木平台上托著舊木桶，黑白貓卻在腳邊呼呼大睡。指著牠的白尾尖——……",
     "蹲在木平台上托著舊木桶，黑白貓卻在腳邊呼呼大睡。指著牠的白尾尖——露天農場連貓咪都來湊一腳。最後一天的輕鬆，就這樣寫進合影；賦歸路上，記得還有一隻睡著的貓。",
     "露天農場"),
    ("tallinn-baltic-sea-bingge.jpg", "49 · Tallinn", "終於見海", "波羅的海",
     "站在岸邊，灰色海面一直鋪到對岸吊臂。這次旅程名叫波羅的海三國，沒想到到了最後一天才真正拍到海。風從水面吹上來——……",
     "站在岸邊，灰色海面一直鋪到對岸吊臂。這次旅程名叫波羅的海三國，沒想到到了最後一天才真正拍到海。風從水面吹上來——終於把這片海收進鏡頭，也把十一天的名字說圓。",
     "波羅的海"),
    ("estonia-chicken-skewer-lunch.jpg", "50 · Tallinn", "賦歸午餐", "烤肉串",
     "中午一盤烤雞串配花椰菜、櫛瓜與紅椒，醬汁鋪在盤底。色香味俱全——……",
     "中午一盤烤雞串配花椰菜、櫛瓜與紅椒，醬汁鋪在盤底。色香味俱全——賦歸前這一餐，先把愛沙尼亞味道再記一口。吃完，行李箱好像也比較好拉。",
     "愛沙尼亞式烤肉串"),
    ("tallinn-balti-jaama-turg-bingge.jpg", "51 · Tallinn", "市集門口", "Balti Jaama 市場",
     "午後走到標著「TURG」的市場入口，金屬球雕塑在廣場旋轉。豎起大拇指——……",
     "午後走到標著「TURG」的市場入口，金屬球雕塑在廣場旋轉。豎起大拇指——漁人市場的門面已經打招呼。接著進去看攤位，起飛前的最後一圈，從這裡開始。",
     "Balti Jaama Turg"),
    ("tallinn-fish-market-berries.jpg", "52 · Tallinn", "果籃顏色", "漁人市場水果攤",
     "草莓、藍莓、紅醋栗與醋栗一盒盒排開，標價並不便宜，卻豐盛得讓人想全買。在起飛前最後逛一圈，把塔林市集的顏色帶走——……",
     "草莓、藍莓、紅醋栗與醋栗一盒盒排開，標價並不便宜，卻豐盛得讓人想全買。在起飛前最後逛一圈，把塔林市集的顏色帶走——旅程結束前，口袋裡最好還留一點甜。",
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
            # fallback for chess alias
            if photo.endswith("tartu-chess-pieces.jpg"):
                photo = "day07/tartu-thumbtack-sculpture.jpg"
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
  <div class="note">點卡片展開全文 · 壓縮四拍旅行札記</div>
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
    for c in by_day.get("day07", []):
        slug = c.get("replace_old_slug") and c["slug"] or c["slug"]
        # use chess slug in md
        photo = c["slug"]
        if photo == "tartu-chess-pieces.jpg" and not (PHOTOS / "day07" / photo).exists():
            photo = "tartu-thumbtack-sculpture.jpg"
        lines.append(f"### ![{c['md_title']}](day07/{photo}) {c['md_title']}")
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
            parts.append(f"### ![{c['md_title']}]({day}/{c['slug']}) {c['md_title']}")
            parts.append(c["body"])
            parts.append("")
        path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    pack_day910()
    # verify photos
    missing = []
    for c in CARDS:
        p = PHOTOS / c["photo"]
        if not p.exists() and c["photo"].endswith("tartu-chess-pieces.jpg"):
            p = PHOTOS / "day07/tartu-thumbtack-sculpture.jpg"
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
