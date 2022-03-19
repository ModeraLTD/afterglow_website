function remove(prodID) {
    notifier.confirm(
        `Are you sure you want to remove this service?`,
        function confirmRemove() {
            $.ajax(
                `/basket/toggle?id=${prodID}`,
                {
                    success: function(d,s,x) {
                        console.log(d);
                        notifier.success(`${d}!`);
                        
                        let product = $(`#${prodID}`);
                        product.fadeOut(750);
                        setTimeout(function() {
                            product.remove();
                        }, 750);

                        updatePrice();
                        updateBookButton();
                        updateServiceEmptyText();
                    },
                    error: function(j, s, errMsg) {
                        notifier.alert(j['responseText']);
                        console.log(j, s);
                    }
                }
            );
        }, // continue
        function() {}, // cancel
        {
            labels: {
                confirm: "Remove service",
            }
        }
    )
}

// disable if no services
function updateBookButton() {
    setTimeout(
        function() {$("#book").prop("disabled", noServices());},
        750,
    );
}

function updateServiceEmptyText() {
    setTimeout(function() {
        if (noServices()) {
            $(".serviceEmptyText").removeClass("hidden");
        } else {
            $(".serviceEmptyText").addClass("hidden");
        }
    }, 750);
}

function noServices() {
    return $(".services").children().length == 0;
}

function updatePrice() {
    $.ajax(
        "/basket/getTotalPrice",
        {
            success: function(d, s, x) {
                $(".totalPrice").text(`Total price: £${d}`);
            },
            error: function(j, s, errMsg) {
                notifier.alert(j['responseText']);
                console.log(j, s);
            }
        }
    );
}

function clearServices() {
    notifier.confirm(
        "Are you sure you want to remove all services in basket? This action cannot be undone.",
        function() {
            $.ajax(
                "/basket/clearAll",
                {
                    success: function(d, s, x) {
                        notifier.success("Removed all services!");
                        deleteAllServices();
                        updatePrice();
                        updateBookButton();
                        updateServiceEmptyText();
                    },
                    error: function(j, s, errMsg) {
                        notifier.alert(j['responseText']);
                        console.log(j, s);
                    }
                }
            );
        },
        function() {},
        {
            labels: {
                confirm: "Remove all services",
            }
        }
    );
}

function deleteAllServices() {
    $(".services").find("*").fadeOut(750);
    setTimeout(
        function() {$(".services").empty();},
        750
    );
}

$(document).ready(function() {
    // updateBookButton();
    console.warn("booking is disabled");
})