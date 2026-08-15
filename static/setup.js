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
function submitFields()
{
    // check for blank fields
    if (firstNameInput.value == "" || lastNameInput.value == "" || cityInput.value == "" || schoolInput.value == "" || occupationInput.value == "")
    {
        alert("Please fill in all fields.");
    }
    // check for valid age (between 0 and 120, not blank, does not contain whitespaces, and is a number)
    if (ageInput.value <= 0 || ageInput.value > 120)
    {
        alert("Please enter a valid age.");
    }
    else if (Number.isNaN(parseInt(ageInput.value, 10)))
    {
        alert("Please enter a valid age.");
    }
    else if (/\s/.test(ageInput.value))
    {
        alert("Error: Age cannot contain spaces.");
    }
    // all fields are valid, send data to server and navigate to dashboard
    else
    {
        let firstName = firstNameInput.value;
        let lastName = lastNameInput.value;
        let city = cityInput.value;
        let school = schoolInput.value;
        let occupation = occupationInput.value;
        let age = parseInt(ageInput.value, 10);
        console.log(age);
        fetch("/createaccount",
        {
            method: "POST",
            headers:
            {
                "Content-type": "application/json"
            },
            body: JSON.stringify
            (
                {
                    firstname: firstName,
                    lastname: lastName,
                    city: city,
                    school: school,
                    occupation: occupation,
                    age: age
                }
            )
        }).then(navigateToDashboard);
        clearFields();
    }
}
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
    window.location.href = "/dashboard"
}

// actionListeners
submitButton.addEventListener("click", function()
{
    submitFields();
});

clearButton.addEventListener("click", function()
{
    clearFields();
});

// on load, check if an account already exists. If so, auto populate the fields with the existing account's information
fetch("/checkaccount").then(response=>response.json()).then(data=>
{
    if (!(Object.keys(data).length === 0 && data.constructor === Object))
    {
        firstNameInput.value = data["firstname"];
        lastNameInput.value = data["lastname"];
        cityInput.value = data["city"];
        schoolInput.value = data["school"];
        occupationInput.value = data["occupation"];
        ageInput.value = data["age"];
    }
}); 
