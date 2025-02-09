async function nameValidation(inputNameField,endpoint,key,statusId){
    let status = "short";
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

            inputNameField.addEventListener("blur",event =>{
                let inputValue = inputNameField.value;

                if (inputValue > 5 ){
                    status = "Strong";
                }
                //!existingNames.includes(inputName);
                statusBar.innerText = `Input : ${inputValue} - status ${status}`;
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


const storePlatform = document.getElementById("storePlatform");
console.log(999);