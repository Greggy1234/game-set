// These functions are for the Book App

// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    stepOneDatePickerInputHidden = document.getElementById("step-1-date-input-hidden");
    flatpickr(stepOneDatePickerInputHidden, {
        minDate: "today",
        altInput: true,
        altFormat: "F j, Y",
        dateFormat: "Y-m-d",
        inline: true,
        altInputClass: "alt-input-date-picker",
    });
    let calendarClass = document.getElementsByClassName("flatpickr-calendar");
    let calendarWidth = calendarClass[0].offsetWidth;
    let altInputClass = document.getElementsByClassName("alt-input-date-picker")[0];
    altInputClass.style.width = calendarWidth + 'px';
});