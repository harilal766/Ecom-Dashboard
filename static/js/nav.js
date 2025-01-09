function html_injector(element_id,content){
    const html_element = document.getElementById(element_id);
    if (html_element) {
        html_element.innerHTML = content;
    }
}

function dom_verifier() {
    pass
}

function navbar() {
    const navbar_contents = {
        "Home" : " ",
        "About us" : "/about",
        "Amazon" : "",
        "Shopify" : "",
        "Logout" : ""
    }
    const navbar_options = Object.keys(navbar_contents);
    const navbar_links = Object.values(navbar_contents);

    const navbar_length = Object.keys(navbar_contents).length;

    var nav_html_code = `<ul class = "nav_list">\n`;

    for (let i = 0; i < navbar_length; i++) {
        
        var list = `<li class="nav-item">
                        <a class="nav-link" href="${navbar_links[i]}">${navbar_options[i]}</a>
                    </li>`;
        nav_html_code += list;
    }
    nav_html_code += "</ul>";

    //return nav_code;
    if (nav_html_code){
        console.log(nav_html_code)
    }
    else {
        console.log("Error with navbar");
    }
    html_injector(element_id="navbar",content=nav_html_code)
}

function django_url_caller(){
    pass
}

const toggleBtn = document.getElementById("toggle-button");
const navbar = document.getElementById("navbar");

toggleBtn.addEventListener("click",()=>{
    console.log("Toggle button working");
});


