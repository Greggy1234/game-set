// These functions are for the Product App

// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname === "/shop" || window.location.pathname === "/shop/") {
        const tagSelec = document.getElementById("tag-selector-update");
        updateTagSelec();
        tagSelec.addEventListener("click", function () {
            updateUrlWTag();
        })
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
    const footer = document.getElementById('footer-wrapper');


    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        topButton.classList.add("show-button");
    } else {
        topButton.classList.remove("show-button");
    }

    let baseBottom = parseInt(topButton.getAttribute("data-css-bottom"));
    let footerTop = footer.getBoundingClientRect().top;
    let viewportHeight = window.innerHeight;

    if (footerTop < viewportHeight) {
    let footerVisibleHeight = viewportHeight - footerTop;
    topButton.style.bottom = (baseBottom + footerVisibleHeight) + "px";
    } else {
    topButton.style.bottom = baseBottom + "px";
    }
}


/**
 * This function shows the quantity selector and allows for a change to be made to the quantity
 */
function quantityChange(item) {
    let itemSku = item.getAttribute("data-sku");
    let itemSize = item.getAttribute("data-size");
    let itemQuanCurrent = item.getAttribute("data-quan");
    let selectQuantity = undefined;
    let quanContain = undefined;
    let changeQuanContain = undefined;
    let keepQuanButtonContain = undefined;
    let changeQuanButtonContain = undefined;
    let keepQuanButton = undefined;
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

/**
 * This function updates the URL with the correct tag search parameters as determined by the user
 */
function updateUrlWTag() {
    let checkboxes = document.querySelectorAll('input[type=checkbox');
    selecCheckboxes = [];
    for (let check of checkboxes) {
        if (check.checked) {
            selecCheckboxes.push(check.value);
        }
    }
    let strSelecCheckboxes = selecCheckboxes.toString();
    let currentURL = window.location.href;
    let currentParams = new URLSearchParams(window.location.search);
    let currentURLNoQ = currentURL.split('?')[0];
    if (selecCheckboxes.length > 0) {
        currentParams.set('tag', strSelecCheckboxes)
    } else {
        currentParams.delete('tag')
    }
    let newURL = currentURLNoQ.concat("?", currentParams);
    window.location = newURL;
}

/**
 * This function updates the tag select box to tick any tags that have been selected
 */
function updateTagSelec(){
    let currentParams = new URLSearchParams(window.location.search);
    let selecTags = [];
    for (const [key, value] of currentParams){
        if (key == "tag"){
            selecTags.push(value);
        }
    }
    let splitStringSelecTags = selecTags[0].split(",");
    let checkboxes = document.querySelectorAll('input[type=checkbox');
    for (let check of checkboxes) {
        checkValue = check.getAttribute("value");
        if (splitStringSelecTags.includes(checkValue)) {
            check.checked = true;
        }
    }
}