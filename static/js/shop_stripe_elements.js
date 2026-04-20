var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Montserrat", sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '1rem',
        '::placeholder': {
            color: '#3C638E'
        }
    },
    invalid: {
        color: '#ff0000',
        iconColor: '#ff0000'
    }
};
var card = elements.create('card', { style: style });
card.mount('#card-element');

/** 
 * This function ensures that all errors are reported back to the user if there are any
*/
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="card-error-icon">
                <i class="fa-solid fa-circle-exclamation"></i> ERROR:
            </span>
            <span>${event.error.message}</span>`;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

/** 
 * This function handles the payment form submission
*/
var form = document.getElementById("shop-checkout-form")
form.addEventListener('submit', function (sub) {
    sub.preventDefault();
    card.update({ 'disabled': true });
    $('#submit-shop-checkout').attr('disabled', true);
    $('#loading-overlay').fadeToggle(100);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function (result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
            <span class="card-error-icon">
                <i class="fa-solid fa-circle-exclamation"></i> ERROR:
            </span>
            <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            $('#loading-overlay').fadeToggle(100);
            card.update({ 'disabled': false });
            $('#submit-shop-checkout').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});