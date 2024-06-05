console.log("hi");

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

// nextPage
let nextPage = null;

// 取得按照排名之捷運站列表
let url = "/api/mrts";
// let url = "http://13.213.240.133:8000/api/mrts";
result = fetchData(url);
result.then((data) => {
  // 取 mrt array
  mrts = data["data"];
  // 計算 mrt 數量
  //   let mrtCounts = mrts.length;
  // mrt_text_node.textContent = mrts
  //   console.log(mrtCounts);
  // const mrt_node = document.createElement("div")
  // mrt_node.textContent = mrts[0]
  // mrt_node.id = "mrt-text"
  // mrt_text_node.appendChild(mrt_node)
  for (mrt of mrts) {
    // console.log(mrt);
    const mrt_node = document.createElement("div");
    mrt_node.textContent = mrt;
    mrt_node.className = "mrt-text";
    mrt_node.addEventListener("click", searchByMRT);
    mrt_container_node.appendChild(mrt_node);
  }
});

// 取得 /api/attractions 資料
url = "/api/attractions?page=0";
// url = "http://13.213.240.133:8000/api/attractions?page=0";
result = fetchData(url);
result.then((data) => {
  let attractions = data["data"];
  nextPage = data["nextPage"];
  console.log(nextPage);
  console.log(attractions[0]["mrt"] == null);
  renderAttractions(attractions);

  //   for (attraction of attractions) {
  //     // 建立 attraction 區塊
  //     const attraction_node = document.createElement("div");
  //     // class name 命名
  //     attraction_node.className = "attraction";
  //     // 加入 attractions group 中
  //     attractions_group_node.appendChild(attraction_node);

  //     // 建立 image 區塊
  //     const attraction_img = document.createElement("div");
  //     // class name 命名
  //     attraction_img.className = "attraction-img";
  //     // 加入 attraction 中
  //     attraction_node.appendChild(attraction_img);
  //     // 取得第一張 image 連結
  //     img_url = attraction["images"][0];
  //     console.log(attraction["mrt"]);
  //     // 設定 image 連結
  //     attraction_img.style.backgroundImage = `url(${img_url})`;

  //     // 建立 name 區塊
  //     const attraction_name = document.createElement("div");
  //     // class name 命名
  //     attraction_name.className = "attraction-name";
  //     // 加入 attraction 中
  //     attraction_node.appendChild(attraction_name);

  //     // 建立 name-text 區塊
  //     const name_text = document.createElement("div");
  //     // class name 命名
  //     name_text.className = "attraction-name-text";
  //     // 加入 attraction-name 中
  //     attraction_name.appendChild(name_text);
  //     // 設定 name 名稱
  //     name_text.textContent = `${attraction["name"]}`;

  //     // 建立 info 區塊
  //     const attraction_info = document.createElement("div");
  //     // class name 命名
  //     attraction_info.className = "attraction-info";
  //     // 加入 attraction 中
  //     attraction_node.appendChild(attraction_info);

  //     // 建立 info-mrt 區塊
  //     const info_mrt = document.createElement("div");
  //     // class name 命名
  //     info_mrt.className = "attraction-info-mrt";
  //     // 加入 attraction-info 中
  //     attraction_info.appendChild(info_mrt);

  //     // 建立 info-mrt-name 區塊
  //     const info_mrt_name = document.createElement("div");
  //     // class name 命名
  //     info_mrt_name.className = "attraction-info-mrt-name";
  //     // 加入 attraction-info 中
  //     info_mrt.appendChild(info_mrt_name);
  //     // 設定 name 名稱
  //     info_mrt_name.textContent = `${
  //       attraction["mrt"] == null ? "無" : attraction["mrt"]
  //     }`;

  //     // 建立 info-category 區塊
  //     const info_category = document.createElement("div");
  //     // class name 命名
  //     info_category.className = "attraction-info-category";
  //     // 加入 attraction-info 中
  //     attraction_info.appendChild(info_category);

  //     // 建立 info-category-name 區塊
  //     const info_category_name = document.createElement("div");
  //     // class name 命名
  //     info_category_name.className = "attraction-info-category-name";
  //     // 加入 attraction-info 中
  //     info_category.appendChild(info_category_name);
  //     // 設定 name 名稱
  //     info_category_name.textContent = `${attraction["category"]}`;
  //   }
});

// 選擇 left-arrow
let left_arrow = document.getElementById("left-arrow");
left_arrow.addEventListener("click", moveLeft);

// MRT List Scroll Left
function moveLeft() {
  left_arrow.removeEventListener("click", moveLeft);
  //   console.log("click");
  // 更新 mrt text container width
  mrt_container_width = mrt_container_node.offsetWidth;
  //   console.log(mrt_container_width);
  // 更新 mrt list width
  mrt_list_width = mrt_list_node.offsetWidth;
  //   console.log(mrt_list_width);
  //   mrt_container_node.style.transform += "translate(100px)";
  //   const matrix = new DOMMatrixReadOnly(
  //     window.getComputedStyle(mrt_container_node).transform
  //   );
  //   console.log(matrix.m41);
  //   console.log(getTransformMatrix(mrt_container_node).m41);
  // 計算 translate X 距離，取 floor
  let x_translate = Math.floor(mrt_list_width * translate_scale);
  // m41 為 translate X 值
  let x_transform = getTransformMatrix(mrt_container_node).m41;
  if (x_transform >= 0) {
    return;
  } else {
    mrt_container_node.style.transform += `translateX(${x_translate}px)`;
  }
}

// 選擇 right-arrow
let right_arrow = document.getElementById("right-arrow");
right_arrow.addEventListener("click", moveRight);

// MRT List Scroll Right
function moveRight() {
  right_arrow.removeEventListener("click", moveRight);
  // console.log("click");
  // 更新 mrt text container width
  mrt_container_width = mrt_container_node.offsetWidth;
  // 更新 mrt list width
  mrt_list_width = mrt_list_node.offsetWidth;
  // 計算 translate X 距離，取 floor
  let x_translate = Math.floor(mrt_list_width * translate_scale);
  // m41 為 translate X 值
  let x_transform = getTransformMatrix(mrt_container_node).m41;
  if (x_transform <= mrt_list_width - mrt_container_width) {
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
    console.log(attraction["mrt"]);
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

// get transform matrix
// 輸入 element
// 輸出 matrix
function getTransformMatrix(element) {
  const matrix = new DOMMatrixReadOnly(
    window.getComputedStyle(element).transform
  );
  return matrix;
}

// search by MRT
function searchByMRT() {
  console.log("click");
  console.log(this.textContent);
  attractions_group_node.replaceChildren();
  url = ""
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
    return pre_url + splitter + page + last_url;
  }
}

// EventListener after transition
addEventListener("transitionend", () => {
  right_arrow.addEventListener("click", moveRight);
  left_arrow.addEventListener("click", moveLeft);
});

// render next page after scroll to bottom
const option = {
  threshold: 1,
};
const renderPage = function (entries) {
  //   console.log(entries);
  if (entries[0].intersectionRatio < 1) return;
  console.log("bottom!");
  if (nextPage != null) {
    console.log("nextPage not null, nextPage is " + nextPage);
    url = getNextPageURL(url,"page=",nextPage)
    console.log(url);
    // url = "http://0.0.0.0:8000/api/attractions?page=" + nextPage;
    // url = "http://13.213.240.133:8000/api/attractions?page=" + nextPage;
    result = fetchData(url);
    result.then((data) => {
      let attractions = data["data"];
      nextPage = data["nextPage"];
      console.log(nextPage);
      renderAttractions(attractions);
    });
  }
};
setTimeout(() => {
  const observer = new IntersectionObserver(renderPage, option);
  observer.observe(document.querySelector("footer"));
}, 1000);
