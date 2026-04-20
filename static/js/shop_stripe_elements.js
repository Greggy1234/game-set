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
var card = elements.create('card', {style: style});
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
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';        
    }
});