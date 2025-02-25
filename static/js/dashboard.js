function darkMode(){
    console.log("----");
    let dayAndNight = {
        "white" : "black",
    };
}

function dashboardData(){
    /* 
    get the store id 
    access endpoint and access store based on the id
    display the data
    on default the data should be displayed based on the first store displayed
    */

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

        selectedTitle = event.target;
        selectedTitle.classList.add("active");


    });
});

// set the first data as the default selection
console.log(addedStoresTitles[0].innerText);

