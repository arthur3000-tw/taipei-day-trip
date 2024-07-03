// 初始化
initialize();

// 初始化函式
async function initialize() {
  // 確認是否登入
  if (await isAuthorized()) {
    // 設置登入狀態
    IS_AUTH_STATUS = true;
  }
  // 根據登入狀態渲染 nav bar
  renderNavBar(IS_AUTH_STATUS);
}

// 以下渲染 index.html 頁面

// 選取 mrt-text-container
const mrt_container_node = document.querySelector(".mrt-text-container");
// 取得 mrt-text-container width
let mrt_container_width = mrt_container_node.offsetWidth;

// 選取 mrt-list
const mrt_list_node = document.querySelector(".mrt-list");
// 取得 mrt-list width
let mrt_list_width = mrt_container_node.offsetWidth;

// 決定 translate scale
const translate_scale = 0.8;

// 選取 attractions group
const attractions_group_node = document.querySelector(".attractions-group");

// 選取 search-input-text
const search_input_text = document.getElementById("search-input-text");
search_input_text.value = "";
search_input_text.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    searchByButton();
  }
});

// 選取 search-button
const search_button = document.getElementById("search-button");
search_button.addEventListener("click", searchByButton);

// 選取 left-arrow
const left_arrow = document.getElementById("left-arrow");
left_arrow.addEventListener("click", moveLeft);

// 選取 right-arrow
const right_arrow = document.getElementById("right-arrow");
right_arrow.addEventListener("click", moveRight);

// nextPage
let nextPage = null;

// pageLoaded
let pageLoaded = false;

// 取得按照排名之捷運站列表
let url = "/api/mrts";
result = fetchData(url);
result.then((data) => {
  // 取 mrt array
  mrts = data["data"];
  for (mrt of mrts) {
    const mrt_node = document.createElement("div");
    mrt_node.textContent = mrt;
    mrt_node.className = "mrt-text";
    mrt_node.addEventListener("click", searchByMRT);
    mrt_container_node.appendChild(mrt_node);
  }
});

// 取得 /api/attractions 資料
url = "/api/attractions?page=0";
result = fetchData(url);
result.then((data) => {
  let attractions = data["data"];
  nextPage = data["nextPage"];
  renderAttractions(attractions);
  pageLoaded = true;
});

// MRT List Scroll Left
function moveLeft() {
  left_arrow.removeEventListener("click", moveLeft);
  // 更新 mrt text container width
  mrt_container_width = mrt_container_node.offsetWidth;
  // 更新 mrt list width
  mrt_list_width = mrt_list_node.offsetWidth;
  // 計算 translate X 距離，取 floor
  let x_translate = Math.floor(mrt_list_width * translate_scale);
  // m41 為 translated X 值
  let x_translated = getTransformMatrix(mrt_container_node).m41;
  if (x_translated >= 0) {
    return;
  } else {
    mrt_container_node.style.transform += `translateX(${x_translate}px)`;
  }
}

// MRT List Scroll Right
function moveRight() {
  right_arrow.removeEventListener("click", moveRight);
  // 更新 mrt text container width
  mrt_container_width = mrt_container_node.offsetWidth;
  // 更新 mrt list width
  mrt_list_width = mrt_list_node.offsetWidth;
  // 計算 translate X 距離，取 floor
  let x_translate = Math.floor(mrt_list_width * translate_scale);
  // m41 為 translated X 值
  let x_translated = getTransformMatrix(mrt_container_node).m41;
  if (x_translated <= mrt_list_width - mrt_container_width) {
    return;
  } else {
    mrt_container_node.style.transform += `translateX(-${x_translate}px)`;
  }
}

// render attractions
function renderAttractions(attractions) {
  for (attraction of attractions) {
    // 建立 attraction 區塊
    const attraction_node = document.createElement("div");
    // class name 命名
    attraction_node.className = "attraction";
    // 設定 attraction onclick 屬性
    attraction_node.setAttribute(
      "onclick",
      `window.location='/attraction/${attraction["id"]}'`
    );
    // 加入 attractions group 中
    attractions_group_node.appendChild(attraction_node);

    // 建立 image 區塊
    const attraction_img = document.createElement("div");
    // class name 命名
    attraction_img.className = "attraction-img";
    // 加入 attraction 中
    attraction_node.appendChild(attraction_img);
    // 取得第一張 image 連結
    img_url = attraction["images"][0];
    // 設定 image 連結
    attraction_img.style.backgroundImage = `url(${img_url})`;

    // 建立 name 區塊
    const attraction_name = document.createElement("div");
    // class name 命名
    attraction_name.className = "attraction-name";
    // 加入 attraction 中
    attraction_node.appendChild(attraction_name);

    // 建立 name-text 區塊
    const name_text = document.createElement("div");
    // class name 命名
    name_text.className = "attraction-name-text";
    // 加入 attraction-name 中
    attraction_name.appendChild(name_text);
    // 設定 name 名稱
    name_text.textContent = `${attraction["name"]}`;

    // 建立 info 區塊
    const attraction_info = document.createElement("div");
    // class name 命名
    attraction_info.className = "attraction-info";
    // 加入 attraction 中
    attraction_node.appendChild(attraction_info);

    // 建立 info-mrt 區塊
    const info_mrt = document.createElement("div");
    // class name 命名
    info_mrt.className = "attraction-info-mrt";
    // 加入 attraction-info 中
    attraction_info.appendChild(info_mrt);

    // 建立 info-mrt-name 區塊
    const info_mrt_name = document.createElement("div");
    // class name 命名
    info_mrt_name.className = "attraction-info-mrt-name";
    // 加入 attraction-info 中
    info_mrt.appendChild(info_mrt_name);
    // 設定 name 名稱
    info_mrt_name.textContent = `${
      attraction["mrt"] == null ? "無" : attraction["mrt"]
    }`;

    // 建立 info-category 區塊
    const info_category = document.createElement("div");
    // class name 命名
    info_category.className = "attraction-info-category";
    // 加入 attraction-info 中
    attraction_info.appendChild(info_category);

    // 建立 info-category-name 區塊
    const info_category_name = document.createElement("div");
    // class name 命名
    info_category_name.className = "attraction-info-category-name";
    // 加入 attraction-info 中
    info_category.appendChild(info_category_name);
    // 設定 name 名稱
    info_category_name.textContent = `${attraction["category"]}`;
  }
}

// render error
function renderError(message) {
  // 建立 error 區塊
  const error_node = document.createElement("div");
  // class name 命名
  error_node.className = "error";
  // 加入 attractions group 中
  attractions_group_node.appendChild(error_node);
  // 顯示錯誤資訊
  error_node.textContent = message;
}

// get transform matrix
// 輸入 element
// 輸出 matrix
function getTransformMatrix(element) {
  const matrix = new DOMMatrixReadOnly(
    window.getComputedStyle(element).transform
  );
  return matrix;
}

// search by button
function searchByButton() {
  search_button.removeEventListener("click", searchByButton);
  let new_url = "/api/attractions?page=0&keyword=" + search_input_text.value;
  new_url = encodeURI(new_url);
  // prevent multiple clicks for same query
  if (new_url == url) {
    // search_button add event listener
    search_button.addEventListener("click", searchByButton);
    return;
  } else {
    url = new_url;
  }
  // new query
  nextPage = null;
  // clean attractions_group_node children
  attractions_group_node.replaceChildren();
  result = fetchData(url);
  result.then((data) => {
    try {
      let attractions = data["data"];
      nextPage = data["nextPage"];
      renderAttractions(attractions);
    } catch {
      if (data["error"] == true) {
        renderError(data["message"]);
      }
    }
  });
  // search_button add event listener
  search_button.addEventListener("click", searchByButton);
  // MRT List scroll bar go to initial position
  let x_translated = getTransformMatrix(mrt_container_node).m41;
  x_translated *= -1;
  mrt_container_node.style.transform += `translateX(${x_translated}px)`;
}

// search by MRT
function searchByMRT() {
  let new_url = "/api/attractions?page=0&keyword=" + this.textContent;
  new_url = encodeURI(new_url);
  // prevent multiple clicks for same query
  if (new_url == url) {
    return;
  } else {
    url = new_url;
  }
  // new query
  nextPage = null;
  // clean attractions_group_node children
  attractions_group_node.replaceChildren();
  result = fetchData(url);
  search_input_text.value = this.textContent;
  result.then((data) => {
    let attractions = data["data"];
    nextPage = data["nextPage"];
    renderAttractions(attractions);
  });
}

// GET
async function fetchData(url) {
  return await fetch(url).then((response) => {
    return response.json();
  });
}

// get nextPage url
function getNextPageURL(url, splitter, page) {
  let pre_url = url.split(splitter)[0];
  if (!isNaN(url.split(splitter)[1])) {
    return pre_url + splitter + page;
  } else {
    let last_url = url.split(splitter)[1].split("&")[1];
    return pre_url + splitter + page + "&" + last_url;
  }
}

// EventListener after transition
mrt_list_node.addEventListener("transitionend", () => {
  right_arrow.addEventListener("click", moveRight);
  left_arrow.addEventListener("click", moveLeft);
});

// render next page after scroll to bottom
const option = {
  threshold: 1,
};
const renderPage = function (entries) {
  //   console.log(entries);
  if (entries[0].intersectionRatio < 1 || pageLoaded == false) return;
  if (nextPage != null) {
    url = getNextPageURL(url, "page=", nextPage);
    result = fetchData(url);
    result.then((data) => {
      let attractions = data["data"];
      nextPage = data["nextPage"];
      renderAttractions(attractions);
    });
  }
};

// add observer
const observer = new IntersectionObserver(renderPage, option);
observer.observe(document.querySelector("footer"));

// // add after reload let scroll to top
// window.onbeforeunload = function () {
//   window.scrollTo(0, 0);
// };

// window position handling
document.addEventListener("DOMContentLoaded", function () {
  let scrollpos = localStorage.getItem("scrollpos");
  if (scrollpos) window.scrollTo(0, scrollpos);
});

window.onbeforeunload = function () {
  localStorage.setItem("scrollpos", window.scrollY);
};
