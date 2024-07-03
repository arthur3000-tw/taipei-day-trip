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

// 以下渲染 attraction.html 頁面

// fetch url
const url = "/api" + document.location.pathname;

// 選取 attraction-images
const attraction_images_node = document.querySelector(".attraction-images");
let attraction_images_width =
  attraction_images_node.getBoundingClientRect()["width"];

// 選取 images-container
const image_container_node = document.querySelector(".image-container");

// 選取 image-list
const image_list_node = document.querySelector(".image-list");

// 選取 left-arrow
const left_arrow = document.getElementById("left-arrow");
left_arrow.addEventListener("click", moveLeft);

// 選取 right-arrow
const right_arrow = document.getElementById("right-arrow");
right_arrow.addEventListener("click", moveRight);

// 選取 image-dot-group
const image_dot_group_node = document.querySelector(".image-dot-group");

// 選取 attraction-name
const attraction_name_node = document.querySelector(".attraction-name");

// 選取 attraction-category-mrt
const attraction_category_mrt_node = document.querySelector(
  ".attraction-category-mrt"
);

// 選取 info-content
const attraction_info_content_node = document.querySelector(".info-content");

// 選取 address-content
const attraction_address_content_node =
  document.querySelector(".address-content");

// 選取 transport-content
const attraction_transport_content_node =
  document.querySelector(".transport-content");

// image index
let image_index = 0;

// image index max
let image_index_max = 0;

// fetch data
fetchData(url).then((data) => {
  let attraction = data["data"];
  renderAttraction(attraction);
});

// render attraction
function renderAttraction(attraction) {
  // get name
  const attraction_name = attraction["name"];
  // 設定 attraction-name
  attraction_name_node.textContent = `${attraction_name}`;
  // get category
  const attraction_category = attraction["category"];
  // get mrt
  const attraction_mrt = attraction["mrt"];
  //設定 category mrt
  attraction_category_mrt_node.textContent = `${attraction_category} at ${attraction_mrt}`;
  // get description
  const attraction_description = attraction["description"];
  // 設定 info-content
  attraction_info_content_node.textContent = `${attraction_description}`;
  // get address
  const attraction_address = attraction["address"];
  // 設定 address-content
  attraction_address_content_node.textContent = `${attraction_address}`;
  // get transport
  const attraction_transport = attraction["transport"];
  // 設定 transport-content
  attraction_transport_content_node.textContent = `${attraction_transport}`;

  // render images
  for (i in attraction["images"]) {
    // 建立 image
    const image_node = document.createElement("div");
    // class name 命名
    image_node.className = "profile-image";
    // 加入 images-container
    image_container_node.appendChild(image_node);

    // 設定 background image
    img_url = attraction["images"][i];
    image_node.style.backgroundImage = `url(${img_url})`;
    image_node.style.width = `${attraction_images_width}px`;

    // 建立 image-dot
    const image_dot_node = document.createElement("div");
    // class name 命名
    image_dot_node.className = "image-dot";
    // id 命名
    image_dot_node.id = `image-${i}`;
    // 加入 image-dot-group
    image_dot_group_node.appendChild(image_dot_node);
    // 建立 event listener
    image_dot_node.addEventListener("click", clickDot);
    // 設定第一個 image dot
    if (i == 0) {
      image_dot_node.style.backgroundColor = "black";
      image_dot_node.style.border = "solid 1.5px #dedede";
    }
  }
  // set image index max
  image_index_max = attraction["images"].length - 1;

  // set image width
  const image_nodes = document.querySelectorAll(".profile-image");
  image_nodes.forEach((image_node) => {
    attraction_images_width =
      attraction_images_node.getBoundingClientRect()["width"];
    image_node.style.width = `${attraction_images_width}px`;
  });
}

// image scroll left
function moveLeft() {
  left_arrow.removeEventListener("click", moveLeft);
  // 更新 image container width
  let image_container_width =
    image_container_node.getBoundingClientRect()["width"];
  // 更新 image list width
  let image_list_width = image_list_node.getBoundingClientRect()["width"];
  //確認當前 image index
  if (Number(image_index) <= 0) {
    // index <= 0 時，目前在第一張照片
    // m41 為 translated X 值
    let x_translated = getTransformMatrix(image_container_node).m41;
    // 計算移動至最後一張照片的距離
    let translate_x = image_container_width - image_list_width - x_translated;
    // 移動
    image_container_node.style.transform += `translateX(-${translate_x}px)`;
    // 設定 image dot
    setImageDot(Number(image_index), Number(image_index_max));
    return;
  } else {
    // index > 0，往右移動一個 attraction_image 的寬度
    image_container_node.style.transform += `translateX(${attraction_images_width}px)`;
    // 設定 image dot
    setImageDot(Number(image_index), Number(image_index) - 1);
  }
}

// image scroll right
function moveRight() {
  right_arrow.removeEventListener("click", moveRight);
  //確認當前 image index
  if (Number(image_index) >= Number(image_index_max)) {
    // index >= index_max 時，目前在最後一張照片
    // m41 為 translated X 值
    let x_translated = getTransformMatrix(image_container_node).m41;
    // 計算移動至第一張照片的距離，就是 x_translated，但方向相反
    x_translated *= -1;
    // 移動
    image_container_node.style.transform += `translateX(${x_translated}px)`;
    // 設定 image dot
    setImageDot(Number(image_index), 0);
    return;
  } else {
    // index < index max，往左移動一個 attraction_image 的寬度
    image_container_node.style.transform += `translateX(-${attraction_images_width}px)`;
    // 設定 image dot
    setImageDot(Number(image_index), Number(image_index) + 1);
  }
}

//
function clickDot() {
  // remove event listener
  const image_dots = document.querySelectorAll(".image-dot");
  image_dots.forEach((image_dot) => {
    image_dot.removeEventListener("click", clickDot);
  });
  // 點選 dot 的 index
  this_index = Number(this.id.split("image-")[1]);
  // 確認與目前顯示 image index 是否相同
  if (this_index === Number(image_index)) {
    // add event listener
    image_dots.forEach((image_dot) => {
      image_dot.addEventListener("click", clickDot);
    });
    return;
  }
  // 計算移動距離，利用點選 dot 的 index 與目前 index 計算
  let value = (image_index - this_index) * attraction_images_width;
  // 移動
  image_container_node.style.transform += `translateX(${value}px)`;
  // 設定 image dot
  setImageDot(Number(image_index), Number(this_index));
}

// set image
function setImageDot(preIndex, nextIndex) {
  // 選取原 image dot
  const pre_image_dot_node = document.getElementById(`image-${preIndex}`);
  // 將黑點轉換為空點
  pre_image_dot_node.style.backgroundColor = "#dedede";
  pre_image_dot_node.style.border = "0";
  // 選取新 image dot
  const next_image_dot_node = document.getElementById(`image-${nextIndex}`);
  // 將空點轉為黑點
  next_image_dot_node.style.backgroundColor = "black";
  next_image_dot_node.style.border = "solid 1.5px #dedede";
  // 更新目前 index
  image_index = Number(nextIndex);
}

// GET
async function fetchData(url) {
  return await fetch(url).then((response) => {
    return response.json();
  });
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

// window resize event listener
window.addEventListener("resize", () => {
  const image_nodes = document.querySelectorAll(".profile-image");
  // 更新所有 image width
  image_nodes.forEach((image_node) => {
    attraction_images_width =
      attraction_images_node.getBoundingClientRect()["width"];
    image_node.style.width = `${attraction_images_width}px`;
  });
  // 確認目前 index
  if (Number(image_index) === 0) {
    // index 為 0 時，不需要做任何事情
    return;
  } else {
    // index 不為 0 時，移動至第一張照片
    // image list scroll bar go to initial position
    let x_translated = getTransformMatrix(image_container_node).m41;
    // 計算移動至第一張照片的距離，就是 x_translated，但方向相反
    x_translated *= -1;
    // 移動
    image_container_node.style.transform += `translateX(${x_translated}px)`;
    // 設定 image dot
    setImageDot(Number(image_index), 0);
  }
});

// add image-list EventListener after transition
image_list_node.addEventListener("transitionend", () => {
  right_arrow.addEventListener("click", moveRight);
  left_arrow.addEventListener("click", moveLeft);
  const image_dots = document.querySelectorAll(".image-dot");
  image_dots.forEach((image_dot) => {
    image_dot.addEventListener("click", clickDot);
  });
});

// page unload
window.onbeforeunload = function () {
  const dateChoice_node = document.getElementById("dateChoice");
  dateChoice_node.value = "";
  const timeChoice1_node = document.getElementById("timeChoice1");
  timeChoice1_node.checked = false;
  const timeChoice2_node = document.getElementById("timeChoice2");
  timeChoice2_node.checked = false;
  reservation_fee_content_node.textContent = "";
};
