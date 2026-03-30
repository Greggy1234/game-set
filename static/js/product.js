// These functions are for the Product App

// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    window.onscroll = function() {
        buttonShowHide()
     } 
})

/**
 * This function shows the scroll to top button when a user has scroll through a certain amount of the page, the
 * stops the button from going over the footer
 */
function buttonShowHide() {
    const topButton = document.getElementById("top-of-page");
    const footer = document.getElementsByTagName('footer')[0];

    if(document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        topButton.classList.add("show-button");
    } else {
        topButton.classList.remove("show-button");
    }

    let topButtonBottomValue = parseInt(topButton.getAttribute("data-css-bottom"));
    let footerRect = footer.getBoundingClientRect();
    let footerRecYValue = footerRect.y;
    let topButtonRectYValue = topButton.getBoundingClientRect().bottom;

    if (footerRecYValue < topButtonRectYValue) {
        let yDiff = topButtonRectYValue - footerRecYValue;
        let newBottomValue = topButtonBottomValue + yDiff;
        topButton.style.bottom = newBottomValue + "px";
    } else {
        topButton.style.bottom = topButtonBottomValue + "px";
    }
}
