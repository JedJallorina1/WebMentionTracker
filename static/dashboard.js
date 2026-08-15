// POC: Jed Jallorina
const configureSearch = document.getElementById("configure-search");
const viewAllMentions = document.getElementById("view-all-mentions");
const getHelp = document.getElementById("help");

// summary numbers
const yearCount = document.getElementById("total-mentions-number");
const monthCount = document.getElementById("thirty-day-mentions-number");
const weekCount = document.getElementById("seven-day-mentions-number");
const dayCount = document.getElementById("twentyfour-hour-mentions-number");

// highlight text fields
const yearHighlight = document.getElementById("total-mentions-highlight");
const monthHighlight = document.getElementById("thirty-day-mentions-highlight");
const weekHighlight = document.getElementById("seven-day-mentions-highlight");
const dayHighlight = document.getElementById("twentyfour-hour-mentions-highlight");

configureSearch.addEventListener("click", function()
{
    window.location.href = "/setup"
});
viewAllMentions.addEventListener("click", function()
{
    // navigate to all mentions page
});
getHelp.addEventListener("click", function()
{
    // show popup
});

// ONSTART: execute the search query in the backend
fetch("/search").then(response=>response.json().then(data=>
{
    if (data == -1)
    {
        alert("Search yielded no results...");
    }
    else
    {
        if (data["explicit"] == true)
        {
            alert("ALERT: Explicit results found.");
        }
        yearCount.textContent = data["basicYear"]["count"];
        if (data["basicYear"]["count"] == 20)
        {
            yearCount.textContent = "20+";
        }
        yearHighlight.textContent = data["basicYear"]["title"];

        monthCount.textContent = data["basicMonth"]["count"];
        if (data["basicMonth"]["count"] == 20)
        {
            monthCount.textContent = "20+";
        }
        monthHighlight.textContent = data["basicMonth"]["title"];

        weekCount.textContent = data["basicWeek"]["count"];
        if (data["basicWeek"]["count"] == 20)
        {
            weekCount.textContent = "20+";
        }
        weekHighlight.textContent = data["basicWeek"]["title"];

        dayCount.textContent = data["basicDay"]["count"];
        if (data["basicDay"]["count"] == 20)
        {
            dayCount.textContent = "20+";
        }
        dayHighlight.textContent = data["basicDay"]["title"];
    }
}));
