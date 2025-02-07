


async function nameValidation(inputNameField,endpoint,key,statusId){
    let inputName = ""; let status = "short";
    let existingNames = []; let statusBar = document.getElementById(statusId);
    try{ 
        let response = await fetch(endpoint);
        // find existing names 
        if (response){
            let data = await response.json();
            
            data.forEach(store => {
                existingNames.push(store[key]);
            });

            console.log(existingNames);

            inputNameField.addEventListener("keydown",event =>{
                inputName += event.key;
                let inputNames = inputName.split("Backspace");
                if (inputName.length > 5 ){
                    status = "Strong";
                }
                //!existingNames.includes(inputName);
                statusBar.innerText = `Input : ${inputName.at(-1)} - status ${status}`;
            });

            
        }
        else {
            console.log("Empty response");
        }
        
    }
    catch (error){
        console.log("Error",error);
    }
}


let storeNameField = document.getElementById("storeName");

nameValidation(inputNameField = storeNameField,
    endpoint = "http://127.0.0.1:8000/api/stores/",key = "store_name", statusId = "statusBar"); 


