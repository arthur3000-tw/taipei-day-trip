//
let SIGN_IN_LOCATION;

// 渲染 nav bar
function renderNavBar(isAuthStatus) {
  // 選取 nav booking button
  const nav_booking_button = document.querySelector("#nav-booking-button");
  nav_booking_button.addEventListener("click", navBookingButton);
  // 渲染登入 nav bar
  if (isAuthStatus) {
    renderMemberNav();
  }
  // 渲染未登入 nav bar
  else {
    renderNullNav();
  }
}

// 點選 nav booking button
function navBookingButton() {
  if (IS_AUTH_STATUS === true) {
    location.href = "/booking";
  } else {
    SIGN_IN_LOCATION = "/booking"
    toggleSignInForm(this);
  }
}

// 點選 登入/註冊按鈕
function signInButton(){
    SIGN_IN_LOCATION = location.href
    console.log(SIGN_IN_LOCATION)
    toggleSignInForm(this);
}

// 登入 nav bar
function renderMemberNav() {
  // 選擇 登入/註冊 按鈕
  const signIn_button = document.querySelector("#signin-button");
  // 不顯示 登入/註冊 按鈕
  signIn_button.style.display = "none";
  // 選擇 登出系統 按鈕
  const signOut_button = document.querySelector("#signout-button");
  // 顯示 登出系統 按鈕
  signOut_button.style.display = "flex";
  signOut_button.addEventListener("click", signOut);
}

// 未登入 nav bar
function renderNullNav() {
  // add event listener
  const signIn_button = document.querySelector("#signin-button");
  signIn_button.addEventListener("click", signInButton);
  const signIn_cancel_button = document.querySelector(".cancel");
  signIn_cancel_button.addEventListener("click", toggleSignInForm);
  const form_hint = document.querySelector(".form-hint");
  form_hint.addEventListener("click", toggleFormContent);
  // 顯示 登入/註冊 按鈕
  signIn_button.style.display = "flex";
  // 選擇 登出系統 按鈕
  const signOut_button = document.querySelector("#signout-button");
  // 不顯示 登出系統 按鈕
  signOut_button.style.display = "none";
  clearForm();
  toggleFormContent();
  // 選取 sign in layer
  const signIn_layer_node = document.querySelector(".signin-layer");
  // 點選登入/註冊頁面之外區域
  window.onmousedown = function (e) {
    if (e.target === signIn_layer_node) {
      toggleSignInForm();
    }
  };
}

// email 格式驗證
function isEmailValid(email) {
  // RFC 2822 standard
  const email_pattern =
    /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
  return email_pattern.test(email);
}

// 顯示表格回應訊息
function showFormResponse(message, color) {
  // 選擇訊息
  const form_response = document.querySelector(".form-response");
  // 顯示訊息及內容
  form_response.style.display = "flex";
  form_response.style.color = `${color}`;
  form_response.textContent = message;
}

// 清除表格
function clearForm() {
  const form_name = document.querySelector("#form-name");
  const form_email = document.querySelector("#form-email");
  const form_password = document.querySelector("#form-password");
  form_name.value = "";
  form_email.value = "";
  form_password.value = "";
  const form_response = document.querySelector(".form-response");
  form_response.style.display = "none";
}

// 登入與註冊頁面切換
function toggleFormContent() {
  const form_title = document.querySelector("#form-title");
  const form_name_node = document.querySelector(".form-input.form-name");
  const form_button = document.querySelector("#form-button");
  const form_hint = document.querySelector(".form-hint");
  if (form_title.textContent === "登入會員帳號") {
    form_title.textContent = "註冊會員帳號";
    form_name_node.style.display = "flex";
    form_button.textContent = "註冊新帳戶";
    form_button.addEventListener("click", register);
    form_button.removeEventListener("click", signIn);
    form_hint.textContent = "已經有帳戶了？點此登入";
  } else {
    form_title.textContent = "登入會員帳號";
    form_name_node.style.display = "none";
    form_button.textContent = "登入帳戶";
    form_button.addEventListener("click", signIn);
    form_button.removeEventListener("click", register);
    form_hint.textContent = "還沒有帳戶？點此登入";
  }
  clearForm();
}

// 登入/註冊頁面與主頁面顯示切換
function toggleSignInForm(element) {
    console.log(element)
  // 選取 sign in layer
  const signIn_layer_node = document.querySelector(".signin-layer");
  //
  signIn_layer_node.style.display =
    signIn_layer_node.style.display === "flex" ? "none" : "flex";
}

//註冊流程
function register() {
  showFormResponse("驗證中...", "orange");
  const form_name = document.querySelector("#form-name");
  const form_email = document.querySelector("#form-email");
  const form_password = document.querySelector("#form-password");
  // 檢查是否為空值
  if (form_name.value == "" || form_email.value == "" || form_password == "") {
    showFormResponse("請輸入完整資料", "red");
    return;
  }
  if (!isEmailValid(form_email.value)) {
    showFormResponse("電子郵件格式錯誤", "red");
    return;
  }
  // 後端註冊
  const url = "/api/user";
  const method = "POST";
  const headers = { "Content-Type": "application/json" };
  const body = {
    name: form_name.value,
    email: form_email.value,
    password: form_password.value,
  };
  fetch(url, {
    method: method,
    headers: headers,
    body: JSON.stringify(body),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["error"] === true) {
        showFormResponse("電子郵件重複", "red");
      } else if (data["ok"] === true) {
        showFormResponse("註冊成功", "green");
      }
    });
}

// 登入流程
function signIn() {
  showFormResponse("驗證中...", "orange");
  const form_email = document.querySelector("#form-email");
  const form_password = document.querySelector("#form-password");
  // 檢查是否為空值
  if (form_email.value == "" || form_password == "") {
    showFormResponse("電子郵件或密碼錯誤", "red");
    return;
  }
  // 檢查 email 格式
  if (!isEmailValid(form_email.value)) {
    showFormResponse("電子郵件格式錯誤", "red");
    return;
  }
  // 後端確認密碼
  const url = "/api/user/auth";
  const method = "PUT";
  const headers = { "Content-Type": "application/json" };
  const body = { email: form_email.value, password: form_password.value };
  fetch(url, { method: method, headers: headers, body: JSON.stringify(body) })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // 登入成功取得 JWT，存放於 local storage
      if (data["token"]) {
        localStorage.setItem("TOKEN", data["token"]);
        showFormResponse("正確", "green");
        // 導入頁面
        location.href = SIGN_IN_LOCATION;
      }
      // 登入失敗，顯示錯誤
      else {
        showFormResponse("電子郵件或密碼錯誤", "red");
      }
    });
}

// 登出
function signOut() {
  // 清除 TOKEN
  localStorage.removeItem("TOKEN");
  // 重新整理頁面
  location.reload();
}
