let upload_button = document.querySelector("#upload-button");
let status = document.querySelector("#status");

upload_button.addEventListener("click", upload);

renderBoard();

function upload() {
  showProcess(status, "上傳中...", "orange");
  const board_content = document.querySelector("#board-content");
  const board_file = document.querySelector("#board-file");
  const form_data = new FormData();
  const file = board_file.files[0];

  form_data.append("file", file);
  form_data.append("content", board_content.value);

  const url = "/api/board";
  const method = "POST";
  //   const headers = { "Content-Type": "multipart/form-data" };

  fetch(url, {
    method: method,
    // headers: headers,
    body: form_data,
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["error"] === true) {
        showProcess(status, "上傳失敗", "red");
      } else if (data["ok"] === true) {
        showProcess(status, "上傳成功", "green");
        location.reload();
      }
    });
}

async function renderBoard() {
  const url = "/api/board";
  let response = await fetch(url);
  let posts = await response.json();
  let board = document.querySelector("#board");
  let image_CDN = "d2q4ypya0go8ne.cloudfront.net";
  for (i in posts) {
    const post_node = document.createElement("div");

    const post_message_node = document.createElement("div");
    post_message_node.textContent = posts[i].message;

    const post_image_node = new Image();
    post_image_node.src = "https://" + image_CDN + "/" + posts[i].image;

    const hr = document.createElement("hr");

    post_node.appendChild(post_message_node);
    post_node.appendChild(post_image_node);
    post_node.appendChild(hr);

    board.appendChild(post_node);
  }
}

// 顯示表格回應訊息
function showProcess(element, message, color) {
  // 顯示訊息及內容
  element.style.display = "flex";
  element.style.color = `${color}`;
  element.textContent = message;
  if (color == "green") {
    setTimeout(() => {
      element.style.display = "none";
    }, 1500);
  }
}
