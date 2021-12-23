const globalOptions = {
    "maxNotifications": 2,
    icons: {enabled: false}
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