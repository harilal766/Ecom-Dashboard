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
                    statusBar.style.color = "green"
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


function storeFormBuilder (type){
    console.log(type);
    storeType.addEventListener("change",function(event){
        const selectedType = event.target.value;
        console.log(selectedType);
    });
}

let storeNameField = document.getElementById("storeName");
const storeType = document.getElementById("storePlatform").value;


nameValidation(inputNameField = storeNameField,
    endpoint = "http://127.0.0.1:8000/api/stores/",key = "store_name", statusId = "statusBar"); 

storeFormBuilder(type = storeType);

