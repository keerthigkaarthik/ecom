var updateBtns = document.getElementsByClassName('add-to-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productID = this.dataset.product

        if (user == 'AnonumousUser') {
            
        } else {
            addToCart(productID)
        }
    })
}

function addToCart(productID) {
    var url = '/update_item/'
    var csrftoken = Cookies.get('csrftoken')

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFtoken':csrftoken
        },
        body: JSON.stringify({'productID': productID, 'action': 'increase'})
    })
    .then((data) => location.reload())
}