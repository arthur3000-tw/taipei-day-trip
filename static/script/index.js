console.log("hi");
fetch("http://127.0.0.1:8000/api/mrts")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data["data"]);
  });
