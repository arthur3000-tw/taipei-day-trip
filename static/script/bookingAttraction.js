// 取得 local storage 至中的 token
const token = localStorage.getItem("TOKEN");

// 取得 attraction id
const attraction_id = document.location.pathname.split("/")[2];

// 選取 input-date
const input_date = document.querySelector(".input-date");
input_date.addEventListener("focus", checkDateTime);

// 選取 selection-morning
const selection_morning = document.querySelector(".selection-morning");

// 選取 selection-afternoon
const selection_afternoon = document.querySelector(".selection-afternoon");

// 選取 reservation fee content
const reservation_fee_content_node = document.querySelector(".fee-content");

// 選取 booking-button
const booking_button = document.querySelector(".booking-button");
booking_button.addEventListener("click", bookingAttraction);

// 點選 booking 按鈕
function bookingAttraction() {
  // 確認日期是否填寫
  if (input_date.value == "") {
    input_date.setCustomValidity("請選擇日期");
    input_date.reportValidity();
    return;
  }
  // 確認時間是否選取
  if (!selection_morning.checked && !selection_afternoon.checked) {
    selection_morning.setCustomValidity("請選擇一個時段");
    selection_morning.reportValidity();
    return;
  }
  // 取得被選取的 radio
  const checked_radio = document.querySelector(
    "input[type='radio'][name='price']:checked"
  );
  const time = checked_radio.className.split("-")[1];
  const price = checked_radio.value;
  // 進行預定
  const url = "/api/booking";
  const method = "POST";
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
  const body = {
    attractionId: attraction_id,
    date: input_date.value,
    time: time,
    price: price,
  };
  // 後端 fetch
  fetch(url, { method: method, headers: headers, body: JSON.stringify(body) })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["error"] === true) {
        if (data["message"] === "重複預訂行程") {
          showBookingResult(data["message"], "red");
          // booking page
          location.href = "/booking";
        } else if (data["message"] === "尚未登入") {
          showBookingResult(data["message"], "red");
          SIGN_IN_LOCATION = "/booking";
          toggleSignInForm();
        }
      } else if (data["ok"] === true) {
        showBookingResult("預訂成功", "green");
        // booking page
        location.href = "/booking";
      }
    });
}

// 確認 Date Time
function checkDateTime() {
  // 幾日前預定
  const reserved_days = 3;
  // 取得今天日期
  let available_day = new Date();
  available_day.setDate(available_day.getDate() + reserved_days);
  available_day = available_day.toISOString().split("T")[0];
  // 設定最小 booking 日期
  input_date.setAttribute("min", available_day);
}

// set price
function setPrice() {
  reservation_fee_content_node.textContent = `新台幣${this.value}元`;
}

// 顯示 booking 結果
function showBookingResult(message, color) {
  // 選取 booking-result
  const booking_result = document.querySelector(".booking-result");
  // 顯示內容
  booking_result.style.color = `${color}`;
  booking_result.textContent = message;
}

// page unload
window.addEventListener("beforeunload", () => {
  // 選取 booking-result
  const booking_result = document.querySelector(".booking-result");
  booking_result.textContent = "";
});
