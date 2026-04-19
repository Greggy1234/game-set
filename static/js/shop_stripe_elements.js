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
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#ff0000',
        iconColor: '#ff0000'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');