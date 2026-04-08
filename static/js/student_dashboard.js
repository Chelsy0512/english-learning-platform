// 這個函式用來開啟指定的彈窗
// 傳入的參數 modalId 是彈窗的 HTML ID (例如 'honorModal')
function openModal(modalId) {
  // 透過 ID 找到對應的彈窗元素，並將其顯示出來 (設為 flex 或 block)
  document.getElementById(modalId).style.display = "block";
}

// 這個函式用來關閉指定的彈窗
function closeModal(modalId) {
  // 透過 ID 找到對應的彈窗元素，並將其隱藏 (設為 none)
  document.getElementById(modalId).style.display = "none";
}

// 這個函式用來回到上一頁 (模擬瀏覽器的上一頁功能)
function goBack() {
  window.history.back();
}

// 6. 處理證照欄位的修改與儲存切換
function toggleEdit(field) {
  const displaySpan = document.getElementById(`display-${field}`);
  const inputField = document.getElementById(`input-${field}`);
  const btn = event.target; // 抓取被點擊的按鈕

  if (inputField.classList.contains("hidden")) {
    // 進入編輯模式：隱藏純文字，顯示輸入框
    inputField.classList.remove("hidden");
    displaySpan.classList.add("hidden");
    btn.innerText = "儲存";
    btn.style.backgroundColor = "#4CAF50"; // 變成綠色
  } else {
    // 儲存模式：把輸入框的值塞回純文字，隱藏輸入框
    displaySpan.innerText = inputField.value;
    inputField.classList.add("hidden");
    displaySpan.classList.remove("hidden");
    btn.innerText = "修改";
    btn.style.backgroundColor = "var(--primary-color)"; // 變回橘色

    // 這裡未來可以寫 AJAX 呼叫後端 API 更新資料庫
    console.log(`準備將 ${field} 的新值 "${inputField.value}" 存入資料庫`);
  }
}

// 1. 處理「喜好」多重勾選的修改與儲存 (修正拼字警告)
function toggleEditPreferences() {
  const displayDiv = document.getElementById("display-preferences");
  const inputDiv = document.getElementById("input-preferences");
  const btn = event.target;

  if (inputDiv.classList.contains("hidden")) {
    // 顯示勾選框
    inputDiv.classList.remove("hidden");
    displayDiv.classList.add("hidden");
    btn.innerText = "儲存";
    btn.style.backgroundColor = "#4CAF50";
  } else {
    // 找出所有被打勾的 checkbox
    const checkboxes = inputDiv.querySelectorAll('input[type="checkbox"]:checked');
    // 將打勾的值收集成陣列
    const selected = Array.from(checkboxes).map((cb) => cb.value);

    // 更新顯示文字
    displayDiv.innerText = selected.length > 0 ? selected.join(", ") : "無";

    // 隱藏勾選框
    inputDiv.classList.add("hidden");
    displayDiv.classList.remove("hidden");
    btn.innerText = "修改";
    btn.style.backgroundColor = "var(--primary-color)";
  }
}
