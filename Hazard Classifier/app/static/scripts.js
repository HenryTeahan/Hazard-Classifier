const components = JSON.parse(document.getElementById("components-data").textContent);

console.log("Components loaded from template:", components);

function getTotalMass() {
    return components.reduce((sum, comp) => sum + (Number(comp.mass) || 0), 0);
}

function getTotalPercentage() {
    return components.reduce((sum, comp) => sum + (Number(comp.percentage) || 0), 0);
}

function allHavePercentages() {
    return components.every(c => c.percentage !== null && c.percentage !== undefined && c.percentage !== '');
}

function updateCalculateButtonVisibility() {
    const calculateBtn = document.querySelector("button[onclick='handleCalculate()']");
    if (allHavePercentages() && getTotalMass() >= 990) {
        calculateBtn.style.display = 'inline-block'; 
    } else {
        calculateBtn.style.display = 'none';       
    }
}

function handleCalculate() {
    const total = getTotalPercentage();
    const totalMass = getTotalMass();
    const popup = document.getElementById("error-popup");

    if (total < 99 || total > 101) {
        popup.textContent = "Total percentage must be 100%";
        popup.classList.add("show");
    } else if (totalMass < 990) {
        popup.textContent = "Total mass must be at least 1000 grams (1 liter solution used)";
        popup.classList.add("show");
    } else {
        popup.classList.remove("show");
        window.location.href = "/calculate"; 
    }
}

function validateForReset() {
    const total = getTotalPercentage();
    const totalMass = getTotalMass();
    return (total >= 99 && total <= 101) && totalMass >= 1000;
}

updateCalculateButtonVisibility();
