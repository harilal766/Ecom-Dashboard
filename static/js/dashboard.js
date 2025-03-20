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





const addedStoresDiv = document.querySelector("#addedStores");
const addedStoresTitles = addedStoresDiv.querySelectorAll(".store-title");
const dashboardTitle = document.getElementById("dashboardTitle");

// click the title and return the store name from it
let selectedTitle = addedStoresTitles[0];
selectedTitle.classList.add("active");

addedStoresTitles.forEach((title) => {
    title.addEventListener("click",function(event){
        selectedTitle.style.color = "";
        console.log(title);
        selectedTitle = event.target;
        selectedTitle.classList.add("active");
    });
});






reportTypes = document.getElementById("reportTypes");
generatorButton = document.getElementById("generatorButton");
generatorButton.innerText = `Create ${reportTypes.value}`;
reportTypes.addEventListener("change",function(event){
    let selection = event.target.value;
    generatorButton.innerText = `Create ${selection}`
});



