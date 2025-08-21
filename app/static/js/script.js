
function dropdown(buttonID) {
    //Gets all elements that are collapsed dropdowns
    var elements = document.getElementsByClassName('DropdownCollapsed');
    var arrow = document.querySelector(`.dropdownarrow[id='${buttonID}']`);
    // Creates a found variable to see if opening succeeded
    let found = false;

    // Loops through the retrieved elements for one that matches the button that was clicked
    for (const element of elements){
        if(element.id == buttonID){
            // Change the class
            element.className = 'DropdownOpen'
            arrow.className = 'dropdownarrowActive'
            found = true
        }
    }   

    // If no matching objects were found, checks for open dropdowns
    if(!found) 
    {
        var elements = document.getElementsByClassName('DropdownOpen');
        var arrow = document.querySelector(`.dropdownarrowActive[id='${buttonID}']`);
        
        for (const element of elements){
            if(element.id == buttonID){
                // Change the class
                element.className = 'DropdownCollapsed'
                arrow.className = 'dropdownarrow'
            }
        } 
    }
}
