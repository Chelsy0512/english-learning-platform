// 切換側邊欄顯示/隱藏
function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('closed');
}

// 切換子選單 (展開/收合)
function toggleSubmenu(id) {
    var submenu = document.getElementById(id);
    if (submenu.style.display === "block") {
        submenu.style.display = "none";
    } else {
        submenu.style.display = "block";
    }
}

// 切換右側內容顯示
function showContent(sectionId) {
    // 1. 隱藏所有內容
    var sections = document.querySelectorAll('.content-section');
    sections.forEach(function(section) {
        section.classList.remove('active');
    });

    // 2. 顯示目標內容
    document.getElementById(sectionId).classList.add('active');

    // 3. (手機版優化) 點擊連結後自動收起側邊欄，若不需要可註解掉下面這行
    if (window.innerWidth < 768) {
        document.getElementById('sidebar').classList.add('closed');
    }
}

// 新增班級的判斷邏輯
function addClass() {
    var input = document.getElementById('new-class-input');
    var reminder = document.getElementById('class-reminder');
    
    // 檢查是否有輸入文字 (trim() 用來去除前後空白，避免使用者只輸入空白鍵)
    if (input.value.trim() !== "") {
        reminder.innerText = "已新增班級";
        reminder.style.display = "block";
    } else {
        reminder.innerText = "名稱不能為空白！";
        reminder.style.display = "block";
    }
    
    // 無論輸入什麼，最後都將輸入框清空
    input.value = ""; 
}

// 點擊學生時，將資料填入右側面板並顯示
function showStudent(name, nickname, hobby, stars) {
    document.getElementById('stu-name').innerText = name;
    document.getElementById('stu-nickname').innerText = nickname;
    document.getElementById('stu-hobby').innerText = hobby;
    document.getElementById('stu-stars').innerText = stars;
    
    // 顯示右側面板
    document.getElementById('student-detail').style.display = 'inline-block';
}

// 暫時儲存原始使用者名稱的變數
var originalUsername = "王小明";

// 暫時儲存所有學生的資料 (含資料與成績)
const studentDatabase = {
    'classA': [
        { seat: 1, name: '學生A', nickname: '小A', hobby: '畫畫', stars: 6, exam1: 85, exam2: 90 },
        { seat: 2, name: '學生B', nickname: '小B', hobby: '閱讀', stars: 12, exam1: 78, exam2: 82 }
    ],
    'classB': [
        { seat: 25, name: '學生Y', nickname: '小Y', hobby: '唱歌', stars: 3, exam1: 92, exam2: 88 },
        { seat: 26, name: '學生Z', nickname: '小Z', hobby: '跳舞', stars: 8, exam1: 65, exam2: 70 }
    ]
}

// 確認更改名稱
function confirmNameChange() {
    var input = document.getElementById('username-input');
    if(input.value.trim() !== "") {
        originalUsername = input.value; // 更新記錄的名字
        alert("成功更改名稱為：" + originalUsername); // 跳出提示讓使用者知道已更改
    } else {
        alert("名稱不能為空白！");
        input.value = originalUsername; // 恢復原狀
    }
}

// 取消更改名稱
function cancelNameChange() {
    var input = document.getElementById('username-input');
    input.value = originalUsername; // 將輸入框內容改回原始名字
}

// 班級管理的下拉選單事件，動態抓取並生成學生名單
function changeClass() {
    var selected = document.getElementById('class-selector').value;
    var listContainer = document.getElementById('dynamic-student-list');
    listContainer.innerHTML = ''; // 清空現有列表
    
    if (selected && studentDatabase[selected]) {
        studentDatabase[selected].forEach(function(student) {
            var li = document.createElement('li');
            // 綁定點擊事件，傳入基本資料顯示在右側
            li.onclick = function() { 
                showStudent(student.name, student.nickname, student.hobby, student.stars); 
            };
            li.innerHTML = '<span class="seat-num">' + student.seat + '</span>' + student.name;
            listContainer.appendChild(li);
        });
        listContainer.style.display = 'block';
    } else {
        listContainer.style.display = 'none';
    }
    
    document.getElementById('student-detail').style.display = 'none';
}

// 學習狀況的下拉選單事件，動態抓取並生成成績表格與下方統計圖
// 修改：生成成績表格時，把學生姓名加上 onclick 事件
function changeLearningClass() {
    var selected = document.getElementById('learning-class-selector').value;
    var tbody = document.getElementById('learning-status-tbody');
    var statsContainer = document.getElementById('unit-stats-container');
    var statsChart = document.getElementById('unit-stats-chart');
    
    tbody.innerHTML = ''; // 清空表格內容
    document.getElementById('learning-detail-panel').style.display = 'none'; // 切換班級時隱藏右側
    
    if (selected && studentDatabase[selected]) {
        var exam1Scores = [];
        var exam2Scores = [];

        // 生成表格內容並收集分數
        studentDatabase[selected].forEach(function(student) {
            var tr = document.createElement('tr');
            tr.innerHTML = '<td>' + student.seat + '</td>' +
                            '<td onclick="showStudentLearning(\'' + student.name + '\')" style="cursor: pointer; color: #0066cc; text-decoration: underline;">' + student.name + '</td>' +
                            '<td>' + student.exam1 + '</td>' +
                            '<td>' + student.exam2 + '</td>';
            tbody.appendChild(tr);

            exam1Scores.push(student.exam1);
            exam2Scores.push(student.exam2);
        });

        // 計算平均函數 (長條圖高度還是需要平均分數)
        var getAverage = function(arr) {
            return Math.round(arr.reduce(function(a, b) { return a + b; }, 0) / arr.length);
        };

        var avg1 = getAverage(exam1Scores);
        var avg2 = getAverage(exam2Scores);

        // 動態生成長條圖內容 (高度綁定平均分數)
        statsChart.innerHTML = `
            <div class="bar-vertical-col">
                <div class="bar-vertical" style="height: ${avg1}px; background-color: #ff9800;" title="平均 ${avg1} 分"></div>
                <span class="bar-vertical-label">單元一</span>
                <span style="font-size: 10px; color: #555;">${avg1}分</span>
            </div>
            <div class="bar-vertical-col">
                <div class="bar-vertical" style="height: ${avg2}px; background-color: #ff9800;" title="平均 ${avg2} 分"></div>
                <span class="bar-vertical-label">單元二</span>
                <span style="font-size: 10px; color: #555;">${avg2}分</span>
            </div>
        `;

        statsContainer.style.display = 'block';
    } else {
        statsContainer.style.display = 'none';
    }
}

// 新增 1：點擊學生姓名時，顯示選擇單元與繪本
function showStudentLearning(studentName) {
    var panel = document.getElementById('learning-detail-panel');
    panel.innerHTML = `
        <h3 style="margin-top: 0; border-bottom: 2px solid #ccc; padding-bottom: 5px;">${studentName}</h3>
        <div>
            <select id="unit-dropdown" onchange="checkUnitSelected()">
                <option value="">選擇單元...</option>
                <option value="1">單元一</option>
                <option value="2">單元二</option>
            </select>
            <select id="book-dropdown" style="display: none; margin-left: 10px;">
                <option value="">選擇繪本...</option>
                <option value="A">繪本 A</option>
                <option value="B">繪本 B</option>
            </select>
        </div>
    `;
    panel.style.display = 'inline-block';
}

// 新增 2：判斷是否選擇了單元，若有才顯示繪本選單
function checkUnitSelected() {
    var unitVal = document.getElementById('unit-dropdown').value;
    var bookSelect = document.getElementById('book-dropdown');
    bookSelect.style.display = (unitVal !== "") ? 'inline-block' : 'none';
}

// 新增 3：點擊總複習成績表頭時，顯示圖表與統計資料
function showExamStats(unitName) {
    var panel = document.getElementById('learning-detail-panel');
    
    // 隨機產生測試用的統計數據
    var avgScore = (unitName === '單元一') ? 78 : 82;
    var medianScore = (unitName === '單元一') ? 80 : 85;

    // 組合垂直長條圖 (縱軸為答對人數，暫時用隨機高度)
    var verticalBarsHTML = '';
    for(let i = 1; i <= 10; i++) {
        let height = Math.floor(Math.random() * 80) + 20; // 高度 20~100px
        verticalBarsHTML += `
            <div class="bar-vertical-col">
                <div class="bar-vertical" style="height: ${height}px;" title="隨機人數"></div>
                <span class="bar-vertical-label">Q${i}</span>
            </div>`;
    }

    // 組合水平長條圖 (縱軸區間，橫軸人數，暫時用隨機寬度)
    var horizontalBarsHTML = '';
    var ranges = ['90-100', '80-89', '70-79', '60-69', '< 60'];
    ranges.forEach(range => {
        let width = Math.floor(Math.random() * 120) + 20; // 寬度 20~140px
        horizontalBarsHTML += `
            <div class="bar-horizontal-row">
                <span class="bar-horizontal-label">${range} 分</span>
                <div class="bar-horizontal" style="width: ${width}px;" title="隨機人數"></div>
            </div>`;
    });

    // 填入右側面板
    panel.innerHTML = `
        <h3 style="margin-top: 0; border-bottom: 2px solid #ccc; padding-bottom: 5px;">${unitName}總複習成績</h3>
        <div style="margin-bottom: 10px; font-weight: bold;">
            <span style="margin-right: 20px;">平均： ${avgScore} 分</span>
            <span>中位數： ${medianScore} 分</span>
        </div>
        
        <div class="chart-wrapper">
            <div style="font-size: 13px; font-weight: bold;">各題答對人數 (共 10 題)</div>
            <div class="bar-vertical-container">
                ${verticalBarsHTML}
            </div>
        </div>

        <div class="chart-wrapper">
            <div style="font-size: 13px; font-weight: bold;">成績區間人數分佈</div>
            <div class="bar-horizontal-container">
                ${horizontalBarsHTML}
            </div>
        </div>
    `;
    // 呼叫寬度判斷函式，取代原本固定顯示在右側的設定
    checkPanelPosition();
}

// 判斷表格寬度，決定詳細資料面板要並排還是放到下方
function checkPanelPosition() {
    var panel = document.getElementById('learning-detail-panel');
    var tableContainer = document.querySelector('.table-container');
    
    // 如果面板目前沒有要顯示的內容，就跳過
    if (!panel || panel.innerHTML.trim() === "") return;

    var windowWidth = window.innerWidth;
    var tableWidth = tableContainer.offsetWidth;

    // 當表格寬度大於視窗 55% 時
    if (tableWidth > windowWidth * 0.55) {
        panel.style.display = 'block'; // block 會強制換行到表格下方
        panel.style.marginLeft = '0';  // 移除左邊距，貼齊左側
        panel.style.marginTop = '20px';// 與上方的表格保持距離
    } else {
        panel.style.display = 'inline-block'; // 維持在右側並排
        panel.style.marginLeft = '20px';
        panel.style.marginTop = '15px';
    }
}

// 當視窗大小改變時，自動重新計算位置與側邊欄狀態
window.addEventListener('resize', function() {
    // 學習狀況右側面板的位置調整
    var panel = document.getElementById('learning-detail-panel');
    if (panel && panel.style.display !== 'none') {
        checkPanelPosition();
    }
    
    // 新增：只要視窗寬度小於 768，就自動收起側邊欄
    if (window.innerWidth < 768) {
        document.getElementById('sidebar').classList.add('closed');
    }
});