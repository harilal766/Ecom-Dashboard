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
let defaultSelection = addedStoresTitles[0];
console.log(`Default store : ${defaultSelection.innerHTML}`);
defaultSelection.classList.add("active");

addedStoresTitles.forEach((title) =>{
    console.log(title);

    title.addEventListener("click", function(event){
        // removing the highlighting from the preselected title
        addedStoresTitles.forEach((preSelection) => preSelection.classList.remove("active"));
        
        event.target.classList.add("active");
    });
    
});


/*
access the store debrief api
and print its contents
*/ 
