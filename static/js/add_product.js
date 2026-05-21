// These functions are for the Book App
// These map the long names for the categories and tags to their value for sku creation
const categoryShorthand = {
    "1": "m", 
    "2": "w", 
    "3": "g",
    "4": "a"}
const tagShorthand = {
    "1": "hood", 
    "2": "jack", 
    "3": "trou",
    "4": "short",
    "5": "tee", 
    "6": "sweat", 
    "7": "dress",
    "8": "skirt",
    "9": "tank", 
    "10": "legging",
    "11": "towel",
    "12": "waterbot",
    "13": "glasses", 
    "14": "bag", 
    "15": "wrist",
    "16": "socks",
    "17": "headband", 
    "18": "cap", 
    "19": "racket",
    "20": "strings",
    "21": "balls", 
    "22": "vibdamp", 
    "23": "grip",
    "24": "hopper",
    "25": "shoe",
}


// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    updateSkuField();
    let categorySelec = document.getElementById("id_category");
    let tagSelec = document.getElementById("id_tag");
    categorySelec.addEventListener("change", function () {
        updateSkuField();
    })
    tagSelec.addEventListener("change", function () {
        updateSkuField();
    })
})

/**
 * This function populates the sku field so consistency for skus are kept throughout the site, ensuring no products break the flow
 * The sku is also added to a hidden field, ensuring it is attached to the product correctly
 */
function updateSkuField() {
    let skuField = document.getElementById("id_sku");
    let hiddenSkuField = document.getElementById("sku_use");
    let updateSkuText;
    let categorySelecValue = document.getElementById("id_category").value;
    let tagSelecValue = document.getElementById("id_tag").value;
    let skuWord = categoryShorthand[categorySelecValue].concat(tagShorthand[tagSelecValue]);
    let allRecentSkus = JSON.parse(document.getElementById("add-product-form-container").getAttribute("data-skus"));
    console.log(allRecentSkus)
    if (allRecentSkus[skuWord] != undefined) {
        num = allRecentSkus[skuWord] + 1;
        updateSkuText = skuWord.concat(num);
    } else {
        updateSkuText = `${skuWord}1`;
    }
    skuField.value = updateSkuText;
    hiddenSkuField.value = updateSkuText;
}