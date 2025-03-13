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
