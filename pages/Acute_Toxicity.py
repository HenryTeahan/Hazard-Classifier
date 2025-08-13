import streamlit as st

st.title("Acute Toxicity Calculations")
st.markdown(
    "As defined in [GHS Rev. 10, 2023](https://unece.org/transport/dangerous-goods/ghs-rev10-2023), "
    "acute toxicity refers to serious adverse health effects (i.e. lethality) occurring after a single "
    "or short-term oral, dermal or inhalation exposure to a substance or mixture."
)
st.markdown(
    "Acute Toxicity Calculations in this calculator are based on numerical Acute Toxicity Estimates (ATE), "
    "which can be seen as a proxy for the lethal dose or concentration for 50% of the test animals "
    "(respectively called LD50 and LC50)."
)
st.subheader("ATE Thresholds for Various Exposures")
st.table([
    ["Oral (mg/kg bodyweight)", "≤ 5", "> 5 - ATE ≤ 50", "> 50 - ATE ≤ 300", "> 300 - ATE ≤ 2000"],
    ["Dermal (mg/kg bodyweight)", "≤ 50", "> 50 - ATE ≤ 200", "> 200 - ATE ≤ 1000", "> 1000 - ATE ≤ 2000"],
    ["Inhalation, Gas (ppmV)", "≤ 100", "> 100 - ATE ≤ 500", "> 500 - ATE ≤ 2500", "> 2500 - ATE ≤ 20000"],
    ["Inhalation, Vapours (mg/L)", "≤ 0.5", "> 0.5 - ATE ≤ 2", "> 2 - ATE ≤ 10", "> 10 - ATE ≤ 20"],
    ["Inhalation, Mist (mg/L)", "≤ 0.05", "> 0.05 - ATE ≤ 0.5", "> 0.5 - ATE ≤ 1", "> 1 - ATE ≤ 5"]
])
st.markdown("**Conversion Table for ATE values:**")
st.table([
    ["Oral (mg/kg bodyweight)", "0.5", "5", "100", "500"],
    ["Dermal (mg/kg bodyweight)", "5", "50", "300", "1100"],
    ["Inhalation, Gas (ppmV)", "10", "100", "700", "4500"],
    ["Inhalation, Vapours (mg/L)", "0.05", "0.5", "3", "11"],
    ["Inhalation, Mist (mg/L)", "0.005", "0.05", "0.5", "1.5"]
])
st.markdown("The ATE of the mixture (**ATEmix**) is calculated as follows, for each individual route of exposure:")
st.image("static/atemix.png", use_container_width=True)
st.markdown(
    "The resulting ATE of the mixture is then matched with the conversion table, "
    "and the final classification for each of the exposure routes is found."
)
st.subheader("Example")
st.markdown("Let's look at an example:")
st.markdown("**5% Formic Acid** and **5% Methanol** in an aqueous solution, with the following acute oral toxicity values:")
st.markdown("- Formic acid: Acute Oral Toxicity, category 3")
st.markdown("- Methanol: Acute Oral Toxicity, category 3")
st.markdown("The concentration is given as the weight percentages (5% for each).")
st.markdown("**Calculation:**")
st.markdown("`= 0.05/100 + 0.05/100 = 0.1/100`")
st.markdown("**Now find ATEmix:**")
st.markdown("`= 100 / (0.1/100) = 1000`")
st.markdown("Looking up this value in the threshold table:")
st.markdown("- **1000** falls into **category 4**")
st.markdown("- Therefore the mixture will be classified as **Category 4 acute oral toxicant**")
