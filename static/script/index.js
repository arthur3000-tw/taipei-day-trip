console.log("hi");
fetch("http://13.213.240.133:8000/api/mrts")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data["data"]);
  });
