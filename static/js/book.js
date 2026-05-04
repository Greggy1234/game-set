// These functions are for the Book App
// Global variables which will hold the selected day, time and coach
let daySelected = undefined
let timeSelected = undefined
let coachSelected = undefined
let fullDateSelected = undefined
let fullTimeSelected = undefined
let coachSelectedId = undefined


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
        "disable": [
            function (date) {
                let courtID = document.getElementById("booking-court-header").getAttribute("data-id");
                if (courtID == 7 || courtID == 8) {
                    return (date.getDay() === 1 || date.getDay() === 2);
                } else if (courtID == 5 || courtID == 6) {
                    return (date.getDay() === 4 || date.getDay() === 5);
                }
            }
        ],
    });
    let calendarClass = document.getElementsByClassName("flatpickr-calendar");
    let calendarWidth = calendarClass[0].offsetWidth;
    let altInputClass = document.getElementsByClassName("alt-input-date-picker")[0];
    altInputClass.style.width = calendarWidth + 'px';
    stepOneDatePickerInputHidden.addEventListener("input", function () {
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
    let changeTimeButton = document.getElementById("change-time-picker");
    changeTimeButton.addEventListener("click", function () {
        changeTime()
    })
    let bookCoachButtons = document.getElementsByClassName("book-coach-button");
    for (let cb of bookCoachButtons) {
        cb.addEventListener("click", function () {
            bookCoach(this);
        })
    }
    let changeCoachButton = document.getElementById("change-coach-button");
    changeCoachButton.addEventListener("click", function () {
        showStep3();
    })
    let finaliseBookingButton = document.getElementById("finalise-booking-button");
    finaliseBookingButton.addEventListener("click", function () {
        showBookingSummary();
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
    fullDateSelected = datePickerValueDateUse;
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
    daySelected = chosenDay;
    let dayOfWeekTimes = document.getElementById(chosenDay);
    dayOfWeekTimes.classList.remove("d-none");
    let bookedTimeSlotsJson = document.getElementById("step-1-2-container").getAttribute("data-booked-times");
    let bookedTimeSlots = JSON.parse(bookedTimeSlotsJson);
    if (bookedTimeSlots[datePickerValue] != undefined) {
        let timeButtons = document.getElementsByClassName("time-slot-button");
        for (let tb of timeButtons) {
            if (bookedTimeSlots[datePickerValue].includes(tb.innerText)) {
                tb.disabled = true
            }
        }
    }
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
    let timeSlotDays = document.getElementsByClassName("time-slot-date-container");
    for (let tsd of timeSlotDays) {
        tsd.classList.add("d-none");
        tsd.classList.remove("d-block");
    }
    let showSelecTime = document.getElementById("time-chosen-field");
    let bookingSummaryContain = document.getElementById("booking-summary-container");
    bookingSummaryContain.classList.add("d-none");
    bookingSummaryContain.classList.remove("d-block");
    showSelecTime.innerHTML = ``;
    showSelecTime.classList.add("d-none");
    let changeDateButton = document.getElementById("change-date-picker");
    let changeTimeButton = document.getElementById("change-time-picker");
    let calendarPicker = document.getElementById("step-1-date-input-container")
    let showSelecDate = document.getElementById("date-chosen-field");
    let goToStep3Button = document.getElementById("go-to-step-3");
    let step2Contain = document.getElementById("step-2-container");
    let step3Contain = document.getElementById("step-3-container");
    step3Contain.classList.add("d-none");
    step3Contain.classList.remove("d-block");
    step2Contain.classList.add("d-none");
    step2Contain.classList.remove("d-block");
    goToStep3Button.classList.remove("d-block");
    goToStep3Button.classList.add("d-none");
    changeDateButton.classList.add("d-none");
    changeDateButton.classList.remove("d-block");
    changeTimeButton.classList.add("d-none");
    changeTimeButton.classList.remove("d-block");
    calendarPicker.classList.remove("d-none");
    calendarPicker.classList.add("d-block");
    showSelecDate.classList.add("d-none");
    showSelecDate.classList.remove("d-block");
    showSelecDate.innerHTML = ``
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
    timeSelected = buttonValue;
    let baseNumber = buttonValue.split(":")[0];
    let nextHour = parseInt(baseNumber) + 1;
    if (nextHour < 10) {
        nextHour = `0${nextHour}`;
    }
    let showSelecTime = document.getElementById("time-chosen-field");
    showSelecTime.innerHTML = `YOUR SELECTED TIME: ${buttonValue} - ${nextHour}:00`;
    fullTimeSelected = `${buttonValue} - ${nextHour}:00`
    showSelecTime.classList.remove("d-none");
    showSelecTime.classList.add("d-block");
    let goToStep3Button = document.getElementById("go-to-step-3");
    goToStep3Button.classList.add("d-block");
    goToStep3Button.classList.remove("d-none");
    goToStep3Button.addEventListener("click", function () {
        showStep3();
    })
}

/**
 * This function allows a user to change their selected time
 */
function changeTime() {
    let timeButtons = document.getElementsByClassName("time-slot-button");
    for (let tb of timeButtons) {
        tb.classList.add("time-slot-button-not-selected");
        tb.classList.remove("time-slot-button-selected");
    }
    let showSelecTime = document.getElementById("time-chosen-field");
    let bookingSummaryContain = document.getElementById("booking-summary-container");
    bookingSummaryContain.classList.add("d-none");
    bookingSummaryContain.classList.remove("d-block");
    showSelecTime.innerHTML = ``;
    showSelecTime.classList.add("d-none");
    showSelecTime.classList.remove("d-block");
    let goToStep3Button = document.getElementById("go-to-step-3");
    let changeTimeButton = document.getElementById("change-time-picker");
    let step3Contain = document.getElementById("step-3-container");
    let step2Contain = document.getElementById("step-2-container");
    let dayOfWeekTimes = document.getElementById(daySelected);
    dayOfWeekTimes.classList.remove("d-none");
    step2Contain.classList.remove("d-none");
    step2Contain.classList.add("d-block");
    step3Contain.classList.add("d-none");
    step3Contain.classList.remove("d-block");
    goToStep3Button.classList.remove("d-block");
    goToStep3Button.classList.add("d-none");
    changeTimeButton.classList.add("d-none");
    changeTimeButton.classList.remove("d-block");
}

/**
 * This function checks if coaches are available for the selected time, then shows step 3 with the right information.
 * If there is no coach available, it shows the finalise booking button.
 */
function showStep3() {
    coachSelected = undefined
    let step3NoCoach = document.getElementById("step-3-coach-no-time")
    step3NoCoach.innerText = `Unfortunately, there are no coaches available to hire during that time. Here are the two coaches for this court, and when they are available:`
    let timeSlotDays = document.getElementsByClassName("time-slot-date-container");
    for (let tsd of timeSlotDays) {
        tsd.classList.add("d-none");
        tsd.classList.remove("d-block");
    }
    let goToStep3Button = document.getElementById("go-to-step-3");
    let changeTimeButton = document.getElementById("change-time-picker");
    let changeCoachButton = document.getElementById("change-coach-button");
    let bookingSummaryContain = document.getElementById("booking-summary-container");
    bookingSummaryContain.classList.add("d-none");
    bookingSummaryContain.classList.remove("d-block");
    goToStep3Button.classList.remove("d-block");
    goToStep3Button.classList.add("d-none");
    changeTimeButton.classList.remove("d-none");
    changeTimeButton.classList.add("d-block");
    changeCoachButton.classList.remove("d-block");
    changeCoachButton.classList.add("d-none");
    let step3Contain = document.getElementById("step-3-container");
    let noCoachContain = document.getElementById("no-coaches-available-container")
    let coach1AvailableContain = document.getElementById("coach-1-available")
    let coach2AvailableContain = document.getElementById("coach-2-available")
    let finaliseBookingButton = document.getElementById("finalise-booking-button");
    let showSelecCoach = document.getElementById("coach-chosen-field");
    step3Contain.classList.remove("d-none");
    step3Contain.classList.add("d-block");
    noCoachContain.classList.add("d-none");
    noCoachContain.classList.remove("d-block");
    coach1AvailableContain.classList.add("d-none");
    coach1AvailableContain.classList.remove("d-block");
    coach2AvailableContain.classList.add("d-none");
    coach2AvailableContain.classList.remove("d-block");
    showSelecCoach.innerHTML = ``;
    showSelecCoach.classList.remove("d-none");
    showSelecCoach.classList.add("d-block");
    let datePickerInput = document.getElementById("step-1-date-input-hidden");
    let datePickerValue = datePickerInput.value;
    let coach1SlotsJson = step3Contain.getAttribute("data-coach-1-slots");
    let coach2SlotsJson = step3Contain.getAttribute("data-coach-2-slots");
    let bookedCoachSlotsJson = step3Contain.getAttribute("data-coach-booked-slots");
    let coach1Id = document.getElementById("book-coach-1-button").getAttribute("data-coach-number");
    let coach2Id = document.getElementById("book-coach-2-button").getAttribute("data-coach-number");
    let coach1IdString = coach1Id.toString();
    let coach2IdString = coach2Id.toString();
    let coach1Slots = JSON.parse(coach1SlotsJson);
    let coach2Slots = JSON.parse(coach2SlotsJson);
    let bookedCoachSlots = JSON.parse(bookedCoachSlotsJson);
    let coach1available = false;
    let coach2available = false;
    if (coach1Slots[daySelected] != undefined) {
        if (coach1Slots[daySelected].includes(timeSelected)) {
            if (bookedCoachSlots[datePickerValue][coach1IdString] != undefined) {
                if (bookedCoachSlots[datePickerValue][coach1IdString].includes(timeSelected) == false) {
                    coach1available = true
                    coach1AvailableContain.classList.remove("d-none");
                    coach1AvailableContain.classList.add("d-block");
                } else {
                    step3NoCoach.innerText = `Unfortunately, all available coaches are booked for that time. Here are the two coaches for this court, and when they are available:`
                }
            } else {
                coach1available = true
                coach1AvailableContain.classList.remove("d-none");
                coach1AvailableContain.classList.add("d-block");
            }
        }
    }
    if (coach2Slots[daySelected] != undefined) {
        if (coach2Slots[daySelected].includes(timeSelected)) {
            if (bookedCoachSlots[datePickerValue][coach2IdString] != undefined) {
                if (bookedCoachSlots[datePickerValue][coach2IdString].includes(timeSelected) == false) {
                    coach2available = true;
                    coach2AvailableContain.classList.remove("d-none");
                    coach2AvailableContain.classList.add("d-block");
                } else {
                    step3NoCoach.innerText = `Unfortunately, all available coaches are booked for that time. Here are the two coaches for this court, and when they are available:`
                }
            } else {
                coach2available = true;
                coach2AvailableContain.classList.remove("d-none");
                coach2AvailableContain.classList.add("d-block");
            }
        }
    }
    if (coach1available == false && coach2available == false) {
        noCoachContain.classList.remove("d-none");
        noCoachContain.classList.add("d-block");
        showSelecCoach.innerHTML = `YOUR SELECTED COACH: NO COACH AVAILABLE AT THE SELECTED TIME AND DATE`;
        showSelecCoach.classList.remove("d-none");
        showSelecCoach.classList.add("d-block");
    }
    finaliseBookingButton.classList.remove("d-none");
    finaliseBookingButton.classList.add("d-block");
}

/**
 * This function books the selected coach and then shows the change coach button or finalise booking button.
 */
function bookCoach(button) {
    coachName = button.getAttribute("data-coach-name");
    coachNumber = button.getAttribute("data-coach-number");
    coachSelected = coachName;
    coachSelectedId = coachNumber;
    let showSelecCoach = document.getElementById("coach-chosen-field");
    let finaliseBookingButton = document.getElementById("finalise-booking-button");
    let changeCoachButton = document.getElementById("change-coach-button");
    let coach1AvailableContain = document.getElementById("coach-1-available");
    let coach2AvailableContain = document.getElementById("coach-2-available");
    let bookingSummaryContain = document.getElementById("booking-summary-container");
    bookingSummaryContain.classList.add("d-none");
    bookingSummaryContain.classList.remove("d-block");
    showSelecCoach.innerHTML = `YOUR SELECTED COACH: ${coachName}`;
    showSelecCoach.classList.remove("d-none");
    showSelecCoach.classList.add("d-block");
    finaliseBookingButton.classList.remove("d-none");
    finaliseBookingButton.classList.add("d-block");
    changeCoachButton.classList.remove("d-none");
    changeCoachButton.classList.add("d-block");
    coach1AvailableContain.classList.add("d-none");
    coach1AvailableContain.classList.remove("d-block");
    coach2AvailableContain.classList.add("d-none");
    coach2AvailableContain.classList.remove("d-block");
}

/**
 * This function shows the booking summary.
 */
function showBookingSummary() {
    let bookingSummaryContain = document.getElementById("booking-summary-container");
    let finaliseBookingButton = document.getElementById("finalise-booking-button")
    bookingSummaryContain.classList.remove("d-none");
    bookingSummaryContain.classList.add("d-block");
    finaliseBookingButton.classList.add("d-none");
    finaliseBookingButton.classList.remove("d-block");
    let bookingSummaryDate = document.getElementById("booking-summary-date");
    let bookingSummaryTime = document.getElementById("booking-summary-time");
    let bookingSummaryCoach = document.getElementById("booking-summary-coach");
    let bookingSummaryCost = document.getElementById("booking-summary-cost");
    let dateFormValue = document.getElementById("form-submit-date");
    let timeFormValue = document.getElementById("form-submit-time");
    let coachFormValue = document.getElementById("form-submit-coach");
    let costFormValue = document.getElementById("form-submit-cost");
    let datePickerInput = document.getElementById("step-1-date-input-hidden");
    let datePickerValue = datePickerInput.value;
    bookingSummaryDate.innerHTML = `<p class="white-text large-p">${fullDateSelected}</p>`;
    bookingSummaryTime.innerHTML = `<p class="white-text large-p">${fullTimeSelected}</p>`;
    bookingSummaryCoach.innerHTML = `<p class="white-text large-p">No coach selected</p>`;
    bookingSummaryCost.innerHTML = `<p class="white-text large-p">£10</p>`;
    dateFormValue.setAttribute("value", `${datePickerValue}`);
    timeFormValue.setAttribute("value", `${timeSelected}`)
    if (coachSelected != undefined) {
        bookingSummaryCoach.innerHTML = `<p class="white-text large-p">${coachSelected}</p>`;
        bookingSummaryCost.innerHTML = `<p class="white-text large-p">£85</p>`;
        coachFormValue.setAttribute("value", `${coachSelectedId}`);
        costFormValue.setAttribute("value", "85");
    }
}