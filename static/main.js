console.log("zouerezr");

// Get Stripe publishable key
fetch("/items/config/").then((result) => { return result.json(); }).then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // Event handler
    document.querySelector("#submitBtn").addEventListener("click", () => {
        // Get Checkout Session ID
        fetch("/items/create-checkout-session/")
        .then((result) => { return result.json(); })
        .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .then((res) => {
        console.log(res);
        });
    });
});