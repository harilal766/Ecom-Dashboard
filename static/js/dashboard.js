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

const container = document.getElementById("container");
const addedStoresDiv = container.querySelector("#addedStores");
const addedStoresTitles = addedStoresDiv.querySelectorAll(".store-title");
const dashboardTitle = document.getElementById("dashboardTitle");
/* 
once the document is loaded, the program should change color of the first store,
when another store is clicked, the selection should change to it.
*/
let selectedTitle = addedStoresTitles[0];
selectedTitle.classList.add('active');
addedStoresTitles.forEach((title) => {
    title.addEventListener("click",function(event){
        if (selectedTitle){
            selectedTitle.classList.remove('active');
        }
        selectedTitle = event.target;
        console.log(selectedTitle);
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