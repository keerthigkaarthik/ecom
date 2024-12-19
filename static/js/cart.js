var updateBtns = document.getElementsByClassName('change-item-quantitiy')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productID = this.dataset.product
        var action = this.dataset.action

        if (user == 'AnonumousUser') {
            
        } else {
            updateCart(productID, action)
        }
    })
}

function updateCart(productID, action) {
    var url = '/update_item/'
    var csrftoken = Cookies.get('csrftoken')

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFtoken':csrftoken
        },
        body: JSON.stringify({'productID': productID, 'action': action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => location.reload())
} 