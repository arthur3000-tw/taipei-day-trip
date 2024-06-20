// 選取 sign in layer
const signIn_layer_node = document.querySelector(".signin-layer");

// 初始化
initialize();

// 初始化
async function initialize() {
  // add event listener
  const signIn_button = document.querySelector("#signin-button");
  signIn_button.addEventListener("click", toggleSignInForm);
  const signOut_button = document.querySelector("#signout-button");
  signOut_button.addEventListener("click", signOut);
  const signIn_cancel_button = document.querySelector(".cancel");
  signIn_cancel_button.addEventListener("click", toggleSignInForm);
  const form_hint = document.querySelector(".form-hint");
  form_hint.addEventListener("click", toggleFormContent);
  // 確認 token
  const TOKEN = localStorage.getItem("TOKEN");
  // 若無 token
  // 選染 unauthorized 狀態頁面
  if (TOKEN === null) {
    // 渲染未登入頁面
    renderNullPage();
    return;
  }
  // 有 token
  // 進行授權確認 send to backend for authorization
  else {
    // 獲得授權
    // 渲染 authorized 狀態頁面
    if (await isTokenValid(TOKEN)) {
      // 渲染登入頁面
      renderMemberPage();
    }
    // 授權失敗
    else {
      // 登出流程
      signOut();
    }
  }
}

// token 驗證
async function isTokenValid(token) {
  const url = "/api/user/auth";
  const method = "GET";
  const headers = { Authorization: `Bearer ${token}` };
  // 後端進行 token 驗證
  let result = fetch(url, { method: method, headers: headers })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      return data["data"];
    });
  // 驗證成功，取得 token 中加密資訊：失敗則取得 null
  let data = await result;
  return data !== null;
}

// 渲染登入頁面
function renderMemberPage() {
  // 選擇 登入/註冊 按鈕
  const signIn_button = document.querySelector("#signin-button");
  // 不顯示 登入/註冊 按鈕
  signIn_button.style.display = "none";
  // 選擇 登出系統 按鈕
  const signOut_button = document.querySelector("#signout-button");
  // 顯示 登出系統 按鈕
  signOut_button.style.display = "flex";
}

// 渲染未登入頁面
function renderNullPage() {
  // 選擇 登入/註冊 按鈕
  const signIn_button = document.querySelector("#signin-button");
  // 顯示 登入/註冊 按鈕
  signIn_button.style.display = "flex";
  // 選擇 登出系統 按鈕
  const signOut_button = document.querySelector("#signout-button");
  // 不顯示 登出系統 按鈕
  signOut_button.style.display = "none";
  clearForm();
  toggleFormContent();
}

// email 格式驗證
function isEmailValid(email) {
  // RFC 2822 standard
  const email_pattern =
    /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
  return email_pattern.test(email);
}

//註冊流程
function register() {
  showFormResponse("驗證中...", "orange");
  const form_name = document.querySelector("#form-name");
  const form_email = document.querySelector("#form-email");
  const form_password = document.querySelector("#form-password");
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
        // 重新整理頁面
        location.reload();
      }
      // 登入失敗，顯示錯誤
      else {
        showFormResponse("電子郵件或密碼錯誤", "red");
      }
    });
}

//登出
function signOut() {
  localStorage.removeItem("TOKEN");
  // 重新整理頁面
  location.reload();
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
function toggleSignInForm() {
  signIn_layer_node.style.display =
    signIn_layer_node.style.display === "flex" ? "none" : "flex";
}

// 點選登入/註冊頁面之外區域
window.onmousedown = function (e) {
  if (e.target === signIn_layer_node) {
    toggleSignInForm();
  }
};
