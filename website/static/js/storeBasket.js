const globalOptions = {
    "maxNotifications": 2,
    icons: {enabled: false},
    durations: {
        global: 2500,
    }
};

let notifier = new AWN(globalOptions);

// popup for help
function help(id) {
    var text = helpTexts[id];

    if (text == "") {
        text = "No description has been added for this service.";
    }

    if (text == null) {
        notifier.error("Unknown product");
        console.log("Unknown product ID", id);
    } else {
        notifier.modal(
            `<h2 class="popup">Help for ${id}</h2>
<p class="popup">${text}</p>
<p class="popup footerText">Tap outside this window to close.</p>`
            );
    }
}

function addToBasket(id, prodID) {
    $.ajax(
        `/basket/add?id=${id}`,
        {
            success: function(d,s,x) {
                notifier.success("Added to basket!");
                $(`#${prodID}`).prop("disabled", true);
            },
            error: function(j, s, errMsg) {
                notifier.alert(j['responseText']);
                console.log(j, s);
            }
        }
    );
}