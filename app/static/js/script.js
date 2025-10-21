
function dropdown(buttonID) {
    //Gets all elements that are collapsed dropdowns as well as the related elements sharing and ID with the button
    var element = document.querySelector(`.DropdownCollapsed[id='${buttonID}']`);
    var arrow = document.querySelector(`.dropdownarrow[id='${buttonID}']`);
    var button = document.querySelector(`.dropbtn[id='${buttonID}']`);

    // If a valid dropdown was found
    if (element){
        // Change the class of the elements
        element.className = 'DropdownOpen'
        arrow.className = 'dropdownarrowActive'
        button.className = 'dropbtnActive'
    }
    // If no matching dropdown were found, checks for open dropdowns of the same ID
    else {
        // Gets active dropdown elements with the same ID as the button
        var element = document.querySelector(`.DropdownOpen[id='${buttonID}']`);
        var arrow = document.querySelector(`.dropdownarrowActive[id='${buttonID}']`);
        var button = document.querySelector(`.dropbtnActive[id='${buttonID}']`);
        // Change the class of the elements
        element.className = 'DropdownCollapsed'
        arrow.className = 'dropdownarrow'
        button.className = 'dropbtn'
    }
}
