const urlParams = new URLSearchParams(window.location.search);
const fadeSpeed = 50;

var active_cat = urlParams.get("category");
var currentPage = urlParams.get("page");

if (currentPage == null) {
    currentPage = "aesthetics";
}

var cat_index = getCatIndex(active_cat);

// code -> index
function getCatIndex(code) {
    switch(code) {
        case null:
            return 0;
        case "SKIN":
            return 0;
        case "HEALTH":
            return 1;
        case "NON_INV":
            return 2;
        case "APP":
            return 3;
        default:
            return 0;
    }
}

// index -> code
function getCatCode(index) {
    switch(index) {
        case 0:
            return "SKIN";
        case 1:
            return "HEALTH";
        case 2:
            return "NON_INV";
        case 3:
            return "APP";
        default:
            return 0;
    }
}

// code -> name
function getCatName(code) {
    switch(code) {
        case "SKIN":
            return "Skin";
        case "HEALTH":
            return "Health";
        case "NON_INV":
            return "Non-invasive";
        case "APP":
            return "Appearance";
        default:
            return code;
    }
}


function swipe(n) {
    cat_index = loopIndex(cat_index + n, 3);
    active_cat = getCatCode(cat_index);

    console.log(cat_index, active_cat);

    showNewCat();
}

function showNewCat() {
    updateCatName();
    $(".category").fadeOut(fadeSpeed);
    
    setTimeout(function() {
        $("#" + active_cat).fadeIn(250);
    }, fadeSpeed - 10); // reduce to prevent footer showing at the top for 1ms
}

function updateCatName() {
    $("#catname").text(getCatName(active_cat));
}

function loopIndex(index, max) {
    if (index > max) {
        return 0;
    } else if (index < 0) {
        return max;
    } else {
        return index;
    }
}

$(document).ready(function() {
    // out of 3
    active_cat = getCatCode(cat_index);

    updateCatName();
    $("#page").text(currentPage.toUpperCase());
    $(".category").hide()
    $("#" + active_cat).show();
});