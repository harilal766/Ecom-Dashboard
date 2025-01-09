function cssDebugger() {
    const debug_style = "1px solid red";
    // find the element
    
    const elements = document.querySelectorAll("#index *"); 

    elements.forEach((element) => {
        let css_style = element.style.border;
        if(css_style === ""){
            element.style.border = debug_style;
        }
        else {
            element.style.border = "";
        }
    });

    // if the style already exists, disble it
    // else, add the style to the document
}