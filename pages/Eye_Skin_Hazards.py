import streamlit as st

st.set_page_config(page_title="Eye and Skin Hazard Calculations", layout="wide")

st.title("Skin Corrosion / Irritation")


st.write("""
As defined in [GHS Rev. 10, 2023](https://unece.org/transport/dangerous-goods/ghs-rev10-2023):

- **Skin corrosion**: Irreversible damage to the skin.  
- **Skin irritation**: Reversible damage to the skin.  

Both occur after exposure to a substance or mixture.

The table below provides **cut-off concentration limits** used to determine if mixtures should be classified as seriously damaging to the eye or as an eye irritant.

⚠ **Note:** Particular care must be taken when classifying mixtures containing certain substances such as acids and bases, inorganic salts, aldehydes, phenols, and surfactants.  
In some cases, the additivity approach does not apply, and instead the **pH** should be used as the method of classification.
""")

st.image("static/skineye.png", use_container_width=True)

st.write("""
This method fails in certain situations — when that happens, consult [GHS Rev. 10, 2023](https://unece.org/transport/dangerous-goods/ghs-rev10-2023)  
to find more appropriate classification methods.
""")

st.subheader("Example")
st.write("""
**Scenario:** 8% Ethanol + 0.1% Formic acid

- Ethanol → Category 2 eye irritant  
- Formic acid → Category 1 eye damage **and** Category 1 skin corrosion  

**Step-by-step:**
- 8% Ethanol alone does **not** trigger any hazard.
- Combined with skin category 1 and eye category 1 hazards:  

10 × (skin Category 1 + eye Category 1) + eye Category 2
= 10 × (0.1% + 0.1%) + 8%
= 10% → Category 2 eye irritant

""")