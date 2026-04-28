// These functions are for the Profile App

// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    const statChangeButtons = document.getElementsByClassName("stats-update-button");
    for (let s of statChangeButtons) {
        s.addEventListener("click", function () {
            showStatsForm(this);
        })
    }
})

/**
 * This function shows the stats form so that users can change their tennis info
 */
function showStatsForm(e) {
    const yearPlayInfo = document.getElementById("years-playing-info");
    const faveSurfInfo = document.getElementById("fave-surface-info");
    const faveShotInfo = document.getElementById("fave-shot-info");
    const yearPlayFormContainer = document.getElementById("years-playing-form-container");
    const faveSurfFormContainer = document.getElementById("fave-surface-form-container");
    const faveShotFormContainer = document.getElementById("fave-shot-form-container");
    if (e.getAttribute("id") == "years-playing-form-show") {
        yearPlayInfo.classList.add("d-none");
        yearPlayFormContainer.classList.remove("d-none");
    } else if (e.getAttribute("id") == "fave-surface-form-show") {
        faveSurfInfo.classList.add("d-none");
        faveSurfFormContainer.classList.remove("d-none");
    } else if (e.getAttribute("id") == "fave-shots-form-show") {
        faveShotInfo.classList.add("d-none");
        faveShotFormContainer.classList.remove("d-none");
    }
}