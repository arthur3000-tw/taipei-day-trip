// 初始化
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

// 以下渲染 booking.html 頁面

function renderPage() {
  // 取得 booking 資訊
  const url = "/api/booking";
  const method = "GET";
  const headers = { Authorization: `Bearer ${TOKEN}` };
  // fetch booking 資訊
  fetch(url, { method: method, headers: headers })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["data"] !== undefined) {
        renderBooking(data["data"]);
        renderContact();
        renderConfirm(data["data"]);
        renderDelete();
      } else if (data["error"] === true) {
        renderEmpty();
      }
    });
}

//
function renderDelete() {
  //
  const booking_delete = document.querySelector(".booking-delete");
  booking_delete.addEventListener("click", deleteBooking);
}

function deleteBooking() {
  // 刪除 booking 資訊
  const url = "/api/booking";
  const method = "DELETE";
  const headers = { Authorization: `Bearer ${TOKEN}` };
  // fetch
  fetch(url, { method: method, headers: headers })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["ok"] === true) {
        location.reload()
      }
    });
}

// 渲染沒有 booking 資料畫面
function renderEmpty() {
  // 渲染 booking-title
  const booking_title = document.querySelector(".booking-title");
  booking_title.textContent = `您好，${USER.name}，待預訂的行程如下：`;

  //
  const booking_info_node = document.createElement("div");
  const booking_content = document.querySelector(".booking-content");
  booking_content.appendChild(booking_info_node);
  booking_info_node.textContent = "目前沒有任何待預定的行程";
  booking_info_node.style.margin = "10px 0px";
}

// 渲染 booking 資料畫面
function renderBooking(data) {
  //
  const booking = document.querySelector(".booking");
  booking.style.display = "flex";
  //
  const separators = document.querySelectorAll(".separator");
  separators.forEach((separator) => {
    separator.style.display = "block";
  });
  //
  const contact_info = document.querySelector(".contact-info");
  contact_info.style.display = "block";
  //
  const card_info = document.querySelector(".card-info");
  card_info.style.display = "block";
  //
  const confirm_info = document.querySelector(".confirm-info");
  confirm_info.style.display = "block";

  // 渲染 booking-title
  const booking_title = document.querySelector(".booking-title");
  booking_title.textContent = `您好，${USER.name}，待預訂的行程如下：`;
  // 渲染 booking-img
  const booking_image = document.querySelector(".booking-image");
  booking_image.style.backgroundImage = `url(${data.attraction.image})`;
  // 渲染 booking-info-title
  const booking_info_title = document.querySelector(".booking-info-title");
  booking_info_title.textContent = `台北一日遊：${data.attraction.name}`;
  // 渲染 booking-date-content
  const booking_date_content = document.querySelector(".booking-date-content");
  booking_date_content.textContent = `${data.date}`;
  // 渲染 booking-time-content
  renderInfoTime(data.time);
  // 渲染 booking-fee-content
  const booking_fee_content = document.querySelector(".booking-fee-content");
  booking_fee_content.textContent = `新台幣 ${data.price} 元`;
  // 渲染 booking-address-content
  const booking_address_content = document.querySelector(
    ".booking-address-content"
  );
  booking_address_content.textContent = `${data.attraction.address}`;
  // 渲染 booking-delete
  const booking_delete = document.querySelector(".booking-delete");
}

// 渲染時間狀態
function renderInfoTime(data) {
  const booking_time_content = document.querySelector(".booking-time-content");
  if (data === "morning") {
    booking_time_content.textContent = "早上 9 點到下午 4 點";
  } else if (data === "afternoon") {
    booking_time_content.textContent = "下午 2 點到晚上 9 點";
  } else {
    booking_time_content.textContent = "錯誤";
  }
}

// 渲染聯絡資訊
function renderContact() {
  // 選取 contact-name-input
  const contact_name_input = document.querySelector("#contact-name");
  contact_name_input.value = `${USER.name}`;
  // 選取 contact-email-input
  const contact_email_input = document.querySelector("#contact-email");
  contact_email_input.value = `${USER.email}`;
}

// 渲染付款資訊
function renderConfirm(data) {
  // 選取 confirm-fee-content
  const confirm_fee_content = document.querySelector(".confirm-fee-content");
  confirm_fee_content.textContent = `新台幣 ${data.price} 元`;
}
