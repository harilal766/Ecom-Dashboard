function darkMode(){
    console.log("----");
    let dayAndNight = {
        "white" : "black",
    };
}



const addedStoresDiv = document.querySelector("#addedStores");
const addedStoresButtons = addedStoresDiv.querySelectorAll(".store");
const dashboardTitle = document.getElementById("dashboardTitle");

// click the button and return the store name from it
addedStoresButtons.forEach((button) => {
    button.addEventListener("click",function(event){
        // resetting the color after each click
        addedStoresButtons.forEach((btn) => (btn.style.backgroundColor = ""));

        let selectedStore = event.target.textContent.trim();
        event.target.style.backgroundColor = "green";
        dashboardTitle.innerText = `Dashboard - ${selectedStore}`;
    });
});