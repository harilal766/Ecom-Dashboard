function darkMode(){
    console.log("----");
    let dayAndNight = {
        "white" : "black",
    };
    /*
    find back ground colors by accessi
    convert white background to black
    */
}


const addedStoresDiv = document.querySelector("#addedStores");
const addedStoresTitles = addedStoresDiv.querySelectorAll(".store-title");
const dashboardTitle = document.getElementById("dashboardTitle");

// click the title and return the store name from it
let selectedStore = addedStoresTitles[0];
selectedStore.classList.add("active");
console.log(`Default Store : ${selectedStore.innerHTML}`);





/*
access the stores api and find its slugs
*/ 


async function fetchEndpoint(endpoint){
    try {
        const response = await fetch(endpoint);
        if (!response.ok){
            throw new Error (`Response status : ${response.status}`);
        }
        const json = await response.json();
        return json;
    }
    catch(error) {
        console.log(error.message);
    }
}
