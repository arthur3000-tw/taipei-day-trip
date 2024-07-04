initialize();

// 初始化函式
async function initialize() {
  // 確認是否登入
  if (await isAuthorized()) {
    IS_AUTH_STATUS = true;
    renderPage();
  }
  // 沒有登入（未登入導向，不可留在本頁）
  else {
    // 導向至首頁（book.html無法給未登入的人使用）
    location.replace("/");
  }
  // 根據登入狀態渲染 nav bar（這邊一定是登入的狀態）
  renderNavBar(IS_AUTH_STATUS);
}

async function renderPage() {
  const urlParams = new URLSearchParams(window.location.search);
  const myParam = urlParams.get("number");
  // 取得 order 資訊
  const url = "/api/order/" + myParam;
  const method = "GET";
  const headers = { Authorization: `Bearer ${TOKEN}` };
  let response = await fetch(url, { method: method, headers: headers });
  let response_body = await response.json();
  //
  if (response_body.data !== null) {
    renderOrder(response_body);
  }
}

function renderOrder(data) {
  const order_title = document.querySelector(".order-title");
  order_title.textContent = `您好，${USER.name}，行程預定成功。您的訂單編號如下：`;
  const order_content = document.querySelector(".order-content");
  order_content.textContent = `${data.data.number}。請記錄此編號，以方便現場確認，謝謝！`;
}
