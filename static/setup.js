// text input fields
const firstNameInput = document.getElementById("first-name-field");
const lastNameInput = document.getElementById("last-name-field");
const cityInput = document.getElementById("city-field");
const schoolInput = document.getElementById("school-field");
const occupationInput = document.getElementById("occupation-field");
const ageInput = document.getElementById("age-field");

// buttons
const submitButton = document.getElementById("submit-button");
const clearButton = document.getElementById("clear-button");

// functions
function clearFields()
{
    firstNameInput.value = "";
    lastNameInput.value = "";
    cityInput.value = "";
    schoolInput.value = "";
    occupationInput.value = "";
    ageInput.value = "";
}
function navigateToDashboard()
{
    fetch("/dashboard");
}

// actionListeners
submitButton.addEventListener("click", function()
{
    if (ageInput.value <= 0 || ageInput.value > 120)
    {
        alert("Please enter a valid age.");
    }
    else if (typeof ageInput.value != "number" || Number.isNaN(ageInput.value))
    {
        alert("Please enter a valid age.");
    }
    else if (ageInput.indexOf(' ') >= 0)
    {
        alert("Error: Age cannot contain spaces.");
    }
    else
    {
        clearFields();
        let firstName = firstNameInput.value;
        let lastName = lastNameInput.value;
        let city = cityInput.value;
        let school = schoolInput.value;
        let occupation = occupationInput.value;
        let age = ageInput.value;

        fetch("/setupaccount",
        {
            method: "POST",
            headers:
            {
                "Content-type": "application/json"
            },
            body: JSON.stringify
            (
                {
                    firstName: firstName,
                    lastName: lastName,
                    city: city,
                    school: school,
                    occupation: occupation,
                    age: age
                }
            )
        }).then(navigateToDashboard());

    }
});

clearButton.addEventListener("click", function()
{
    clearFields();
});