function darkMode(){
    console.log("----");
    let dayAndNight = {
        "white" : "black",
    };
}


const addedStoresDiv = document.querySelector("#addedStores");
const addedStoresTitles = addedStoresDiv.querySelectorAll(".store-title");
const dashboardTitle = document.getElementById("dashboardTitle");

// click the title and return the store name from it
let selectedStore = addedStoresTitles[0];
selectedStore.classList.add("active");
console.log(`Default Store : ${selectedStore.innerHTML}`);

/* while the page is loaded there should */

addedStoresTitles.forEach((title) =>{
    title.addEventListener("click", function(event){
        // removing the highlighting from the preselected title
        addedStoresTitles.forEach((preSelection) => preSelection.classList.remove("active"));

        //event.target.classList.add("active");
        selectedStore = event.target;
        selectedStore.classList.add("active");
        console.log(selectedStore.innerHTML);
    });
});


/*
access the stores api and find its slugs
*/ 
