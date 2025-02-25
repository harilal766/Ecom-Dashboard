async function nameValidation(inputNameField,endpoint,key,statusId){
    let existingNames = []
    // name status
    let statusBar = document.getElementById(statusId);
    statusBar.style.color = "red"; let status = "";

    try{ 
        let response = await fetch(endpoint);
        let stores = await response.json();
        
        stores.forEach(store => {
            existingNames.push(store[key]);
        });
        console.log(existingNames);

        const StoreName = document.getElementById("storeName");

        StoreName.addEventListener("input",function(event){
            const typedName = event.target.value;
            // display status only if input value is present
            if (inputNameField.value) {
                if (existingNames.includes(typedName)){
                    statusBar.style.color = "red"
                    status = "Name already exists."
                }
                else {
                    statusBar.style.color = "green"
                    status = "Name available";
                }
                statusBar.innerText = status;
                inputNameField.focus();
            }
            else{
                statusBar.innerText = "";
            }            
        });
    }
    catch (error){
        console.log("Error",error);
    }
}

const apiDiv = document.getElementById("apiCreds"); 

const form = document.getElementById("storeForm");
const storeButton = document.getElementById("storeButton");

const storeType = document.getElementById("storePlatform");

if (storeType) {
    storeType.addEventListener("change",function(event){
        const selectedType = event.target.value;
    
        // dict that consists common fields
        const commonDict = {
            "Access Token" : "accessToken",
        }
    
        // field array for amazon
        const amazonDict = {
            "Refresh Token" : "refreshToken",
            "Client Id" : "clientId",
            "Client Secret" : "clientSecret"
        };
        
        const ShopifyDict = {...commonDict,"API secret key" : "apiSecretKey"};
    
        // choosing the field dictionary based on user choice
        let selectedDict = {};
        if (selectedType){
            if (selectedType === "Amazon") {
                selectedDict = amazonDict;
            }
            else if (selectedType === "Shopify") {
                selectedDict = ShopifyDict;
            }
    
            apiDiv.innerHTML = "";
            
            // make sure the fields does not exists already
            Object.entries(selectedDict).forEach(([key,value]) =>{
                let field = key; let id = value; 
                // need seperate div for each field for accomodating the label and input
                const fieldDiv = document.createElement("div");
                // add label , then the input to it
                const label = document.createElement("label");
                const inputField = document.createElement("input");
                
                inputField.id = `${selectedType}-${id}`;
                inputField.name = field.toLowerCase().replace(/\s+/g, "_");
                inputField.classList.add("form-control");
                inputField.type = "text";
                inputField.placeholder = `Enter ${field} for ${selectedType}`;
    
                fieldDiv.appendChild(label);
                fieldDiv.appendChild(inputField);
                apiDiv.appendChild(fieldDiv);
    
                console.log(inputField);
            });
    
            // button
            let button = document.createElement("button");
            button.innerText = `Create ${selectedType} Store`;
            button.classList.add("btn","btn-primary");
            apiDiv.appendChild(button)
        }
    });
    
}


document.addEventListener("DOMContentLoaded",function () {
    let storeNameField = document.getElementById("storeName");
    
    // Name validation
    nameValidation(inputNameField = storeNameField,
        endpoint = "http://127.0.0.1:8000/api/stores/",key = "store_name", statusId = "statusBar"); 
});


