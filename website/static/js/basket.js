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
                        product.fadeOut(1000);
                        setTimeout(function() {
                            product.remove();
                        }, 1000);

                        updatePrice();
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