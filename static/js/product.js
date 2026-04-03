// These functions are for the Product App

// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname === "/shop" || window.location.pathname === "/shop/") {
        window.onscroll = function () {
            buttonShowHide();
        }
    } else if (window.location.pathname === "/shop/basket" || window.location.pathname === "/shop/basket/") {
        const clickableP = document.getElementsByClassName("clickable-p");
        for (let p of clickableP) {
            p.addEventListener("click", function () {
                quantityChange(this);
            })
        }
    }
})

/**
 * This function shows the scroll to top button when a user has scroll through a certain amount of the page, the
 * stops the button from going over the footer
 */
function buttonShowHide() {
    const topButton = document.getElementById("top-of-page");
    const footer = document.getElementsByTagName('footer')[0];

    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
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


/**
 * This function shows the quantity selector and allows for a change to be made to the quantity
 */
function quantityChange(item) {
    let itemSku = item.getAttribute("data-sku");
    let itemSize = item.getAttribute("data-size");
    let itemQuanCurrent = item.getAttribute("data-quan");
    let selectQuantity = "To be set"
    let quanContain = "To be set";
    let changeQuanContain = "To be set";
    let keepQuanButtonContain = "To be set";
    let changeQuanButtonContain = "To be set";
    let keepQuanButton = "To be set";
    if (itemSize == "None") {
        quanContain = document.getElementById(`quantity-${itemSku}-container`);
        changeQuanContain = document.getElementById(`choose-quantity-${itemSku}-container`);
        selectQuantity = document.getElementById(`quantity-selector-${itemSku}`);
        keepQuanButtonContain = document.getElementById(`keep-quantity-button-${itemSku}-container`);
        changeQuanButtonContain = document.getElementById(`change-quantity-button-${itemSku}-container`);
        keepQuanButton = document.getElementById(`keep-quantity-button-${itemSku}`);
    } else {
        quanContain = document.getElementById(`quantity-${itemSku}-${itemSize}-container`);
        changeQuanContain = document.getElementById(`choose-quantity-${itemSku}-${itemSize}-container`);
        selectQuantity = document.getElementById(`quantity-selector-${itemSku}-${itemSize}`);
        keepQuanButtonContain = document.getElementById(`keep-quantity-button-${itemSku}-${itemSize}-container`);
        changeQuanButtonContain = document.getElementById(`change-quantity-button-${itemSku}-${itemSize}-container`);
        keepQuanButton = document.getElementById(`keep-quantity-button-${itemSku}-${itemSize}`);
    }
    quanContain.classList.remove("d-flex");
    quanContain.classList.add("d-none");
    changeQuanContain.classList.remove("d-none");
    changeQuanContain.classList.add("d-flex");

    selectQuantity.addEventListener("change", function () {
        quantitySelect = selectQuantity.value;
        if (quantitySelect != parseInt(itemQuanCurrent)) {
            keepQuanButtonContain.classList.toggle("d-block");
            keepQuanButtonContain.classList.add("d-none");
            changeQuanButtonContain.classList.remove("d-none");
            changeQuanButtonContain.classList.add("d-block");
        } else if (quantitySelect == parseInt(itemQuanCurrent)) {
            changeQuanButtonContain.classList.remove("d-block");
            changeQuanButtonContain.classList.add("d-none");
            keepQuanButtonContain.classList.remove("d-none");
            keepQuanButtonContain.classList.add("d-block");
        }
    })

    keepQuanButton.addEventListener("click", function () {
        changeQuanContain.classList.remove("d-flex");
        changeQuanContain.classList.add("d-none");
        quanContain.classList.remove("d-none");
        quanContain.classList.add("d-flex");
    })
}
