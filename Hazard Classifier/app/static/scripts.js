
// Load the components data embedded in the HTML as JSON
const components = JSON.parse(document.getElementById("components-data").textContent);
console.log("Components loaded from template:", components); 

// Sums total percentage of all components
function getTotalPercentage() {
    return components.reduce((sum, comp) => sum + (Number(comp.percentage) || 0), 0);
}
// Check if all components have a percentage set
function allHavePercentages() {
    return components.every(c => c.percentage !== null && c.percentage !== undefined && c.percentage !== '');
}
// Update the visibility of the calculate button based on whether all components have percentages
function updateCalculateButtonVisibility() {
    const calculateBtn = document.querySelector("button[onclick='handleCalculate()']");
    if (allHavePercentages()) {
        calculateBtn.style.display = 'inline-block'; 
    } else {
        calculateBtn.style.display = 'none';       
    }
}
// Handle the click event for the calculate button
function handleCalculate() {
    const total = getTotalPercentage();
    const popup = document.getElementById("error-popup");

    if (total < 99 || total > 101) {
        popup.textContent = "Total percentage must be 100%";
        popup.classList.add("show");
    } else {
        popup.classList.remove("show");
        window.location.href = "/calculate"; 
    }
}
// Run on page load to show/hide the Calculate button appropriately
updateCalculateButtonVisibility();
