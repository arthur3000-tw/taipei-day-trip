// 確認是否登入
async function isAuthorized() {
  // 若無 token
  if (TOKEN === null) {
    // 回傳 false
    return false;
  }
  // 有 token
  // 進行授權確認 send to backend for authorization
  else {
    // 進行驗證
    if (await isTokenValid(TOKEN)) {
      // 回傳 true
      return true;
    }
    // 驗證失敗
    else {
      // 清除 TOKEN
      localStorage.removeItem("TOKEN");
      // 回傳 false
      return false;
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
    // 驗證完成，取得結果放入 USER 中，驗證成功放入加密資訊，失敗放入 null
    USER = await result;
    return USER !== null;
  }