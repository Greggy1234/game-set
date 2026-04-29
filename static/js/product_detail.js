// These functions are for the product details page

// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    let editReviewButton = document.getElementById("edit-product-review-rating-button");
    editReviewButton.addEventListener("click", function () {
        editReview();
    })
})

/**
 * This function lets users edit their comments ont he article.html page
 */
function editReview() {
    const editContainerPreForm = document.getElementById("edit-review-no-form-container");
    const editFormContainer = document.getElementById("edit-review-form-container");
    const reviewTextForm = document.getElementById("id_review");
    const reviewRatingForm = document.getElementById("id_rating");
    let userReviewTextOriginal = document.getElementById("user-review-text").getAttribute("data-review");
    let userRatingOriginal = document.getElementById("user-rating").getAttribute("data-rating");
    editContainerPreForm.classList.add("d-none");
    editFormContainer.classList.remove("d-none");
    reviewTextForm.innerText = userReviewTextOriginal;
    if (parseFloat(userRatingOriginal) > 0){
        reviewRatingForm.value = parseFloat(userRatingOriginal).toFixed(2);        
    } else {
        reviewRatingForm.value = null;
    }
    console.log(parseFloat(userRatingOriginal).toFixed(2))
}