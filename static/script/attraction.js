console.log("Hi")
// fetch url
const url = "/api" + document.location.pathname


// fetch
fetchData(url).then(data=>{
    console.log(data)
    let attraction = data["data"]
    console.log(attraction)
    
})


// GET
async function fetchData(url){
    return await fetch(url).then(response=>{
        return response.json()
    })
}

