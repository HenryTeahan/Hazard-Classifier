const components = JSON.parse(document.getElementById("components-data").textContent);
    
console.log("Components loaded from template:", components);

function getTotalPercentage() {
    return components.reduce((sum, comp) => sum + Number(comp.percentage), 0);
}

function handleCalculate() {
    const total = getTotalPercentage();
    const popup = document.getElementById("error-popup");

    if (total < 99 || total > 101) {
        popup.classList.add("show");
    } else {
        popup.classList.remove("show");
        window.location.href = "/calculate";  // Allow calculation
    }
}

function validateForReset() {
    
    const total = getTotalPercentage();
    
    // Don't show the popup on reset, just silently block it
    
    return total >= 99 && total <= 101;
    
}
