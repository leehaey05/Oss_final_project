let selectedCategory = "";

function selectCategory(category) {
    selectedCategory = category;

    const subcategories = category === "가전제품"
        ? [
            { name: "냉장고", img: "fridge.png" },
            { name: "TV", img: "tv.png" },
            { name: "세탁기", img: "washer.png" },
            { name: "건조기", img: "dryer.png" },
            { name: "청소기", img: "vacuumcleaner.png" }, // 수정된 파일명
            { name: "에어컨", img: "airconditioner.png" },
            { name: "공기청정기", img: "airpurifier.png" }
        ]
        : [
            { name: "휴대폰", img: "smartphone.png" }, // 수정된 파일명
            { name: "패드", img: "tablet.png" },
            { name: "무선이어폰", img: "wirelessearbuds.png" }, // 수정된 파일명
            { name: "스마트워치", img: "smartwatch.png" },
            { name: "노트북", img: "laptop.png" }
        ];

    let html = "<h2>세부 항목 선택</h2><div class='subcategory-buttons'>";
    subcategories.forEach(sub => {
        html += `
            <button class="subcategory-button" onclick="selectSubcategory('${sub.name}')">
                <img src="/static/images/${sub.img}" alt="${sub.name}">
                <span>${sub.name}</span>
            </button>`;
    });
    html += "</div>";

    document.getElementById("subcategory").innerHTML = html;

    // 초기 상태 변경
    document.getElementById("category-buttons").style.display = 'none';
    document.getElementById("resetButton").style.display = 'block';
}

function selectSubcategory(subcategory) {
    const html = `
        <h2>예산 입력</h2>
        <input type="number" id="budgetInput" placeholder="예산 입력 (원)">
        <button onclick="getRecommendations('${subcategory}')">추천 받기</button>
    `;
    document.getElementById("subcategory").innerHTML = html;
}

function getRecommendations(subcategory) {
    const budget = document.getElementById("budgetInput").value;

    if (!budget) {
        alert("예산을 입력해주세요!");
        return;
    }

    fetch("/recommend", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ category: selectedCategory, subcategory: subcategory, budget: budget })
    })
    .then(response => response.json())
    .then(data => {
        let html = "<h2>추천 제품 리스트</h2>";
        if (data.length > 0) {
            data.forEach(product => {
                html += `
                    <div class="product">
                        <img src="/static/images/${product.image}" alt="${product.name}" width="100">
                        <p>${product.name}</p>
                        <p>${product.price.toLocaleString()}원</p>
                        <a href="${product.link}" target="_blank">구매 링크</a>
                    </div>
                `;
            });
        } else {
            html += "<p>추천 제품이 없습니다.</p>";
        }
        document.getElementById("result").innerHTML = html;
    })
    .catch(error => {
        console.error("Error:", error);
        alert("추천 제품을 불러오는 데 실패했습니다.");
    });
}

function resetSelection() {
    document.getElementById("category-buttons").style.display = 'block';
    document.getElementById("subcategory").innerHTML = '';
    document.getElementById("result").innerHTML = '';
    document.getElementById("resetButton").style.display = 'none';
    selectedCategory = '';
}
