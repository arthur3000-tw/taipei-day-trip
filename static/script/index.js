console.log("hi");
fetch("http://0.0.0.0:8000/api/mrts")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data["data"]);
  });
