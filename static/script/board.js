let upload_button = document.querySelector("#upload-button");

upload_button.addEventListener("click", upload);

function upload() {
  const board_content = document.querySelector("#board-content");
  const board_file = document.querySelector("#board-file");
  const form_data = new FormData();
  const file = board_file.files[0];
  console.log(file);

  form_data.append("file", file);
  form_data.append("content", board_content.value)

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
        console.log("錯誤")
      } else if (data["ok"] === true) {
        console.log("上傳成功")
      }
    });
}
