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
    let datePickerInput = document.getElementById("step-1-date-input-hidden");
    datePickerInput.addEventListener("input", function () {
        showStep2Button();
    })
    let timeButtons = document.getElementsByClassName("time-slot-button");
    for (let tb of timeButtons) {
        tb.addEventListener("click", function () {
            selectedTime(this);
        })
    }
    let changeDateButton = document.getElementById("change-date-picker");
    changeDateButton.addEventListener("click", function () {
        changeDate();
    })
});

/**
 * This function shows the next step button from step 1 to step 2
 */
function showStep2Button() {
    let goToStep2Button = document.getElementById("go-to-step-2");
    goToStep2Button.classList.remove("d-none");
    goToStep2Button.classList.add("d-block");
    goToStep2Button.addEventListener("click", function () {
        showStep2();
    })
    let showSelecDate = document.getElementById("date-chosen-field");
    let datePickerInput = document.getElementById("step-1-date-input-hidden");
    let datePickerValue = datePickerInput.value;
    let datePickerValueDate = new Date(datePickerValue);
    let datePickerValueDateUse = datePickerValueDate.toLocaleDateString("en-GB", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
    })
    showSelecDate.classList.remove("d-none");
    showSelecDate.classList.add("d-block");
    showSelecDate.innerHTML = `YOUR SELECTED DATE: ${datePickerValueDateUse}`;
}

/**
 * This function shows the next step in booking for time
 */
function showStep2() {
    let changeDateButton = document.getElementById("change-date-picker");
    let goToStep2Button = document.getElementById("go-to-step-2");
    let step2Contain = document.getElementById("step-2-container");
    let calendarPicker = document.getElementById("step-1-date-input-container")
    changeDateButton.classList.remove("d-none");
    changeDateButton.classList.add("d-block");
    goToStep2Button.classList.add("d-none");
    goToStep2Button.classList.remove("d-block");
    step2Contain.classList.remove("d-none");
    step2Contain.classList.add("d-block");
    calendarPicker.classList.add("d-none");
    calendarPicker.classList.remove("d-block");
    let datePickerInput = document.getElementById("step-1-date-input-hidden");
    let datePickerValue = datePickerInput.value;
    let dateValueDate = new Date(datePickerValue);
    let days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    let dayOfWeekIndex = dateValueDate.getDay();
    let chosenDay = days[dayOfWeekIndex];
    let dayOfWeekTimes = document.getElementById(chosenDay);
    dayOfWeekTimes.classList.remove("d-none");
}

/**
 * This function changes the date and resets the booking process
 */
function changeDate() {
    let timeButtons = document.getElementsByClassName("time-slot-button");
    for (let tb of timeButtons) {
        tb.classList.add("time-slot-button-not-selected");
        tb.classList.remove("time-slot-button-selected");
    }
    let timeSlotDays = document.getElementsByClassName("time-slot-dat-container");
    for (let tsd of timeSlotDays) {
        tsd.classList.add("d-none");
        tsd.classList.remove("d-block");
    }
    let showSelecTime = document.getElementById("time-chosen-field");
    showSelecTime.innerHTML = ``;
    showSelecTime.classList.add("d-none");
    let changeDateButton = document.getElementById("change-date-picker");
    let calendarPicker = document.getElementById("step-1-date-input-container")
    let showSelecDate = document.getElementById("date-chosen-field");
    let goToStep3Button = document.getElementById("go-to-step-3");
    let step2Contain = document.getElementById("step-2-container");
    step2Contain.classList.add("d-none");
    step2Contain.classList.remove("d-block");
    goToStep3Button.classList.remove("d-block");
    goToStep3Button.classList.add("d-none");
    changeDateButton.classList.add("d-none");
    changeDateButton.classList.remove("d-block");
    calendarPicker.classList.remove("d-none");
    calendarPicker.classList.add("d-block");
    showSelecDate.classList.add("d-none");
    showSelecDate.classList.remove("d-block");
    showSelecDate.innerHTML = ``
    datePickerInput.addEventListener("input", function () {
        showStep2Button();
    })
}


/**
 * This function pulls the selected time, turns the time button green and shows it to the user. 
 * If another time is chosen, it will change the time button chosen
 */
function selectedTime(button) {
    let timeButtons = document.getElementsByClassName("time-slot-button");
    for (let tb of timeButtons) {
        tb.classList.add("time-slot-button-not-selected");
        tb.classList.remove("time-slot-button-selected");
    }
    button.classList.remove("time-slot-button-not-selected");
    button.classList.add("time-slot-button-selected");
    let buttonValue = button.innerText;
    let baseNumber = buttonValue.split(":")[0];
    let nextHour = parseInt(baseNumber) + 1;
    if (nextHour < 10) {
        nextHour = `0${nextHour}`;
    }
    let showSelecTime = document.getElementById("time-chosen-field");
    showSelecTime.innerHTML = `YOUR SELECTED TIME: ${buttonValue} - ${nextHour}:00`;
    showSelecTime.classList.remove("d-none");
    showSelecTime.classList.add("d-block");
    let goToStep3Button = document.getElementById("go-to-step-3");
    goToStep3Button.classList.add("d-block");
    goToStep3Button.classList.remove("d-none");
}