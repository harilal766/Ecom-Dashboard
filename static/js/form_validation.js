



/* 
submit button should not be visible until the credentials are approved..
read the password and its length
*/

function passwordStrength() {
    const password_field = document.getElementById("password");
    // check the typed word
    password_field.addEventListener("keydown",function (event) {
        let password_input = password_field.value;
        let title = document.getElementById("title");

        let status = "Weak"; const strength = 8;
        if (password_input.length >= strength) {
            status = "Strong";
        } 

        // update the status on the text box label on each keypress..
        console.log(status); console.log(title.value);
    });
}