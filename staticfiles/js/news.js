// These functions are for the News App

// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    let editCommentButton = document.getElementById("edit-comment-button");
    editCommentButton.addEventListener("click", function () {
        editComment();
    })
})

/**
 * This function lets users edit their comments ont he article.html page
 */
function editComment() {
    const editContainerPreForm = document.getElementById("edit-comment-no-form-container");
    const editFormContainer = document.getElementById("edit-comment-form-container");
    const commentForm = document.getElementById("id_comment")
    let userCommentOriginal = document.getElementById("user-comment").getAttribute("data-comment");
    editContainerPreForm.classList.add("d-none");
    editFormContainer.classList.remove("d-none");
    commentForm.innerText = userCommentOriginal
}