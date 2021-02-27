// Receives ID of last pet voted and direction of vote from recommender.html 
// and returns next pet to recommender.html.

// Display a pet on page load (first pet by pet ID)
50664914

function getPetData(id)
{
    d3.json('/getInitialPet?id=' + id)
    
}

// Declare function to render pet photo and attributes
function showPet(id)
{
    "/getPetAttributes"
}

// Display the random pet's photo and attributes
showPet(id)


// Select div from recommender.html where next pet's attributes will be appended.
var tbody = d3.select(".pet");

// Select submit button element to add functionality.
var upButton = d3.select("#up-btn");
var downButton = d3.select("#down-btn");
var adoptButton = d3.select("#adopt-btn");

// Click handler for upButton
upButton.on
(
    "click", function()
    {
        // Prevent automatic page refresh
        d3.event.preventDefault();

        // Get user input
        var 
    }

)


// Click handler for downButton

// Click handler for adoptButton