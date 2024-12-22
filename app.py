from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# 샘플 데이터
products = {
    "가전제품": {
        "냉장고": [
            {"name": "삼성 2023년 비스포크 냉장고 1도어 키친핏 인피니트라인 408L", "price": 200000, "image": "20fridge.png", "link": "http://s.godo.kr/2kpvh"},
            {"name": "LG 모던엣지 M451S53", "price": 400000, "image": "40fridge.png", "link": "https://www.lge.co.kr/refrigerators/b124s14"},
            {"name": "LG 일반냉장고 오브제컬렉션 461L 3등급", "price": 700000, "image": "70fridge.png", "link": "https://www.lge.co.kr/refrigerators/d463mrr33"},
            {"name": "LG 디오스 오브제컬렉션 STEM 얼음정수 냉장고 (매직스페이스) 820L 2등급", "price": 4000000, "image": "300fridge.png", "link": "https://www.lge.co.kr/refrigerators/j825p142"}
        ],
        "TV": [
            {"name": "LG 울트라 HD TV (스탠드형) 107cm (43UT8300ENA)", "price": 700000, "image": "70tv.png", "link": "https://www.lge.co.kr/tvs/43ut8300ena-stand"},
            {"name": "삼성 더세리프 108cm TV KQ43LSB01AFXKR", "price": 1000000, "image": "100tv.png", "link": "http://s.godo.kr/2kpbz"},
            {"name": "LG 울트라 HD TV (벽걸이형) 163cm (65UR931C0NA)", "price": 2400000, "image": "200tv.png", "link": "https://www.lge.co.kr/tvs/65ur931c0na-wall"},
            {"name": "삼성 OLED 163cm 스텐드형 KQ65SC95AFXKR TV", "price": 4390000, "image": "400tv.png", "link": "http://s.godo.kr/2kpf7"}
        ],
        "세탁기": [
            {"name": "LG 트롬 세탁기 9kg(F9WTQ)", "price": 600000, "image": "60washer.png", "link": "https://www.lge.co.kr/washing-machines/f9wtq"},
            {"name": "LG 꼬망스 플러스 8kg (F8VV)", "price": 800000, "image": "80washer.png", "link": "https://www.lge.co.kr/washing-machines/f8vv"},
            {"name": "LG 트롬 오브제컬렉션 세탁기 24kg (FG24GN)", "price": 1800000, "image": "100washer.png", "link": "https://www.lge.co.kr/washing-machines/fg24gn-akor2"},
            {"name": "LG 트롬 오브제컬렉션 세탁기 25kg (FX25ESER)", "price": 2000000, "image": "200washer.png", "link": "https://www.lge.co.kr/washing-machines/fx25eser-akor2"}
        ],
        "건조기": [
            {"name": "LG 트롬 건조기 10kg (RD22GS)", "price": 1200000, "image": "120dryer.png", "link": "https://www.lge.co.kr/dryers/rh10wtw"},
            {"name": "LG 트롬 오브제컬렉션 건조기 21kg (FX23ENEX-EE)", "price": 2000000, "image": "200dryer.png", "link": "https://www.lge.co.kr/dryers/rd21en"},
            {"name": "LG 트롬 오브제컬렉션 + 건조기 + 스태킹키트(KG24KN-G8NW)", "price": 3000000, "image": "300dryer.png", "link": "https://www.lge.co.kr/dryers/kg24kn-g8nw"},
            {"name": "LG 트롬 오브제컬렉션 트윈워시 + 건조기(FX23ENEX-EE)", "price": 4000000, "image": "400dryer.png", "link": "https://www.lge.co.kr/dryers/fx23enexee"}
        ],
        "청소기": [
            {"name": "LG CYKING POWER 흡입 전용 (C40SGY)", "price": 200000, "image": "20vacuum.png", "link": "https://www.lge.co.kr/vacuum-cleaners/c40sgy"},
            {"name": "LG CYKING K8 흡입 전용 (K83WGY)", "price": 400000, "image": "40vacuum.png", "link": "https://www.lge.co.kr/vacuum-cleaners/k83wgy"},
            {"name": "LG 코드제로 R5 흡입+물걸레 (R585WKA1)", "price": 800000, "image": "80vacuum.png", "link": "https://www.lge.co.kr/vacuum-cleaners/r585wka1"},
            {"name": "LG 코드제로 로보킹 AI 올인원 (프리스탠딩) (B95AWBH)", "price": 2000000, "image": "200vacuum.png", "link": "https://www.lge.co.kr/vacuum-cleaners/b95awbh"}
        ],
        "에어컨": [
            {"name": "LG 휘센 벽걸이에어컨 18.7㎡ (SQ06EA1WCS)", "price": 600000, "image": "60air_conditioner.png", "link": "https://www.lge.co.kr/air-conditioners/sq06ea1wcs-akor"},
            {"name": "LG 휘센 벽걸이에어컨 42.3㎡ 2등급 (SQ13EK1WAS)", "price": 1700000, "image": "170air_conditioner.png", "link": "https://www.lge.co.kr/air-conditioners/sq13ek1was"},
            {"name": "삼성 비스포 무풍 에어컨 갤러리 청정 KF17CX738ESS", "price": 2500000, "image": "250air_conditioner.png", "link": "http://s.godo.kr/2kpfb"},
            {"name": "LG 휘센 오브제컬렉션 타워II 사계절에어컨 (디럭스) 62.6㎡(FW19DETBA1)", "price": 3700000, "image": "370air_conditioner.png", "link": "https://www.lge.co.kr/air-conditioners/fw19detba1"}
        ],
        "공기청정기": [
            {"name": "LG 퓨리케어 360˚ 공기청정기 Hit 62 2등급(AS183HWWA)", "price": 650000, "image": "65air_purifier.png", "link": "https://www.lge.co.kr/air-purifier/as183hwwa-akor1"},
            {"name": "LG 퓨리케어 360˚ 공기청정기 Hit 62 2등급(AS283DWFL)", "price": 1200000, "image": "120air_purifier.png", "link": "https://www.lge.co.kr/air-purifier/as283dwfl"},
            {"name": "LG 퓨리케어 360˚ 공기청정기 펫 플러스 100㎡ 2등급 (AS301DNPA)", "price": 1500000, "image": "150air_purifier.png", "link": "https://www.lge.co.kr/air-purifier/as301dnpa"},
            {"name": "LG 퓨리케어 오브제컬렉션 360˚ 공기청정기 (AS354NS4A)", "price": 2200000, "image": "220air_purifier.png", "link": "https://www.lge.co.kr/air-purifier/as354ns4a"}
        ]
    },
    "전자제품": {
        "휴대폰": [
            {"name": "갤럭시 A24 자급제", "price": 300000, "image": "30smartphone.png", "link": "https://www.samsung.com/sec/smartphones/galaxy-a24-lte-a245/SM-A245NLGNKOO/"},
            {"name": "iPhone SE", "price": 650000, "image": "65smartphone.png", "link": "https://www.apple.com/kr/shop/buyiphone/iphone-se"},
            {"name": "iPhone 16 & iPhone 16 Plus ", "price": 1200000, "image": "65smartphone.png", "link": "https://www.apple.com/kr/shop/buy-iphone/iphone-16"},
            {"name": "갤럭시 Z 폴드6 자급제", "price": 2200000, "image": "220smartphone.png", "link": "https://www.samsung.com/sec/smartphones/galaxy-z-fold6/buy/?modelCode=SM-F956NDBAKOO"}
        ],
        "패드": [
            {"name": "갤럭시 탭 A9+ (Wi-Fi)", "price": 300000, "image": "30tablet.png", "link": "https://www.samsung.com/sec/tablets/galaxy-tab-a9-plus-wifi-x210-1/SM-X210NZSEKOO/"},
            {"name": "iPad", "price": 550000, "image": "55tablet.png", "link": "https://www.apple.com/kr/shop/buy-ipad/ipad"},
            {"name": "Tablet C", "price": 600000, "image": "30tablet.png", "link": "https://example.com/tablet_c"},
            {"name": "iPad Pro ", "price": 1500000, "image": "150tablet.png", "link": "https://www.apple.com/kr/shop/buy-ipad/ipad-pro"}
        ],
        "무선이어폰": [
            {"name": "갤럭시 버즈 FE", "price": 120000, "image": "12earbuds.png", "link": "https://www.samsung.com/sec/buds/galaxy-buds-fe-r400/SM-R400NZWAKOO/"},
            {"name": "AirPods 4", "price": 200000, "image": "32earbuds.png", "link": "https://www.apple.com/kr/shop/buy-airpods/airpods-4"},
            {"name": "갤럭시 버즈3 프로", "price": 300000, "image": "30earbuds.png", "link": "https://www.samsung.com/sec/buds/galaxy-buds3/buy/?modelCode=SM-R630NZWAKOO"},
            {"name": "AirPods Max", "price": 8000000, "image": "80earbuds.png", "link": "https://www.apple.com/kr/shop/buy-airpods/airpods-max"}
        ],
        "스마트워치": [
            {"name": "Apple Watch SE", "price": 300000, "image": "30smartwatch.png", "link": "https://www.apple.com/kr/shop/buy-watch/apple-watch-se"},
            {"name": "갤럭시 워치6 클래식 골프 에디션 47mm (블루투스)", "price": 500000, "image": "50smartwatch.png", "link": "https://www.samsung.com/sec/watches/galaxywatch6-golf-edition-11-r960/SM-R960NZSGK01/"},
            {"name": "갤럭시 워치 울트라 47mm (LTE 자급제)", "price": 800000, "image": "80smartwatch.png", "link": "https://www.samsung.com/sec/watches/galaxy-watch7/buy/?modelCode=SM-L705NDAAKOO"},
            {"name": "Apple Watch Hermes Ultra 2", "price": 2000000, "image": "200smartwatch.png", "link": "https://www.apple.com/kr/shop/buy-watch/apple-watch-hermes-ultra"}
        ],
        "노트북": [
            {"name": "MacBook Air", "price": 1400000, "image": "140laptop.png", "link": "https://www.apple.com/kr/shop/buy-mac/macbook-air"},
            {"name": "갤럭시 북4 (39.6cm) Core™ 5 / 512GB NVMe SSD", "price": 1500000, "image": "150laptop.png", "link": "https://www.samsung.com/sec/galaxybook/galaxy-book4-nt750xgk-kc51g/NT750XGK-KC51S/"},
            {"name": "MacBook Pro", "price": 2300000, "image": "230laptop.png", "link": "https://www.apple.com/kr/shop/buy-mac/macbook-pro"},
            {"name": "갤럭시 북4 Pro 360 (40.6cm) Core™ Ultra 7 / 1TB NVMe SSD", "price": 3000000, "image": "300laptop.png", "link": "https://www.samsung.com/sec/galaxybook/galaxy-book4-pro-360-nt960qgk-kd72g/NT960QGK-KD72G/"}
        ]
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    category = data["category"]
    subcategory = data["subcategory"]
    budget = int(data["budget"])

    recommendations = [p for p in products[category][subcategory] if p["price"] <= budget]
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
