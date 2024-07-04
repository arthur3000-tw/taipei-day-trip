tappay_initialize();

function tappay_initialize() {
  TPDirect.setupSDK(
    151752,
    // FIXME:
    "app_kOLbUXj0njMHsZEWYJKgThRdTQgU807I3vJEnQPsziTgVV1DwmgeUxu0eoa6",
    "sandbox"
  );

  let fields = {
    number: {
      // css selector
      element: "#card-number",
      placeholder: "**** **** **** ****",
    },
    expirationDate: {
      // DOM object
      element: "#card-expire",
      placeholder: "MM / YY",
    },
    ccv: {
      element: "#card-credential",
      placeholder: "後三碼",
    },
  };

  TPDirect.card.setup({
    fields: fields,
    styles: {
      // Style all elements
      input: {
        color: "gray",
        "font-size": "16px",
      },
      // Styling ccv field
      "input.ccv": {
        // 'font-size': '16px'
      },
      // Styling expiration-date field
      "input.expiration-date": {
        // 'font-size': '16px'
      },
      // Styling card-number field
      "input.card-number": {
        // 'font-size': '16px'
      },
      // style focus state
      ":focus": {
        color: "black",
      },
      // style valid state
      ".valid": {
        color: "green",
      },
      // style invalid state
      ".invalid": {
        color: "red",
      },
      // Media queries
      // Note that these apply to the iframe, not the root window.
      "@media screen and (max-width: 400px)": {
        input: {
          color: "orange",
        },
      },
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    //   isMaskCreditCardNumber: true,
    //   maskCreditCardNumberRange: {
    //     beginIndex: 6,
    //     endIndex: 11,
    //   },
  });
}

// 取得 prime
async function getPrime() {
  //
  const confirm_area_hint = document.querySelector(".confirm-area-hint");
  // 取得 TapPay Fields 的 status
  const tappayStatus = TPDirect.card.getTappayFieldsStatus();
  // 確認是否可以 getPrime
  if (tappayStatus.canGetPrime === false) {
    showConfirmResponse(confirm_area_hint, "信用卡資料錯誤", "red");
    // alert("can not get prime");
    return;
  }
  // Get prime
  let data = await getPrimePromise();
  // 設置 promise
  function getPrimePromise() {
    return new Promise((resolve) => {
      TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
          showConfirmResponse(confirm_area_hint, "信用卡取得授權錯誤", "red");
          //   alert("get prime error " + result.msg);
          return;
        }
        showConfirmResponse(confirm_area_hint, "資料正確", "green");
        // alert("get prime 成功，prime: " + result.card.prime);
        resolve(result.card.prime);
      });
    });
  }
  return data;
}

// 呈現確認付款按鈕
function renderConfirmButton(data, element) {
  //
  element.addEventListener("click", sendPayment.bind(event, data));
}

// 付款按鈕
async function sendPayment(data) {
  //
  const contact_name = document.querySelector("#contact-name");
  const contact_email = document.querySelector("#contact-email");
  const contact_phone = document.querySelector("#contact-phone");
  const confirm_area_hint = document.querySelector(".confirm-area-hint");
  // 確認聯絡資訊
  if (
    contact_name.value === "" ||
    contact_email.value === "" ||
    contact_phone.value === ""
  ) {
    showConfirmResponse(confirm_area_hint, "請輸入完整聯絡資訊", "red");
    return;
  }
  if (!isPhoneValid(contact_phone.value)) {
    showConfirmResponse(confirm_area_hint, "請輸入正確手機號碼", "red");
    return;
  }

  // 先由前端向 TapPay 取得 prime
  showConfirmResponse(confirm_area_hint, "取得授權中...", "orange");
  let prime = await getPrime();
  // 資料錯誤
  if (prime === undefined) {
    showConfirmResponse(confirm_area_hint, "信用卡授權錯誤（尚未付款）", "red");
    return;
  }
  showConfirmResponse(confirm_area_hint, "完成授權，進行預定行程...", "orange");
  //
  let price = data.price;
  let trip = new Trip({
    attraction: data.attraction,
    date: data.date,
    time: data.time,
  });
  let contact = new Contact({
    name: contact_name.value,
    email: contact_email.value,
    phone: contact_phone.value,
  });
  let order = new Order({ price: price, trip: trip, contact: contact });
  // 像後端 POST order
  const url = "/api/orders";
  const method = "POST";
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${TOKEN}`,
  };
  const body = {
    prime: prime,
    order: order,
  };
  // fetch
  let response = await fetch(url, {
    method: method,
    headers: headers,
    body: JSON.stringify(body),
  });
  let response_body = await response.json();
  showConfirmResponse(confirm_area_hint, "預定完成", "green");
  if (response_body.data !== null) {
    location.href = `/thankyou?number=${response_body.data.number}`;
  }
}

// 顯示表格回應訊息
function showConfirmResponse(element, message, color) {
  // 顯示訊息及內容
  element.style.display = "flex";
  element.style.color = `${color}`;
  element.textContent = message;
  setTimeout(() => {
    element.style.display = "none";
  }, 1500);
}

// phone 格式驗證
function isPhoneValid(phone) {
  //09xx xxx xxx
  const phone_pattern = /^09[0-9]{8}$/;
  return phone_pattern.test(phone);
}
