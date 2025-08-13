import streamlit as st

st.set_page_config(page_title="Carcinogenicity, Mutagenicity, Reproductive Toxicity and Sensitization", layout="wide")

st.title("Carcinogenicity, Mutagenicity, Reproductive Toxicity and Sensitization")

# Intro
st.write("""
This section looks at five different health hazards: **Carcinogenicity**, **Mutagenicity**, **Reproductive Toxicity**, **Skin Sensitization**, and **Respiratory Sensitization**.

The explanation for grouping these hazards together can be found in [GHS Rev. 10, 2023](https://unece.org/transport/dangerous-goods/ghs-rev10-2023),  
where the cut-off concentration limits are uniform across these hazards.
""")

# Carcinogenicity
st.header("Carcinogenicity")
st.write("""
As defined in [GHS Rev. 10, 2023](https://unece.org/transport/dangerous-goods/ghs-rev10-2023), **Carcinogenicity** refers to the induction of cancer  
or an increase in the incidence of cancer occurring after exposure to a substance or mixture.  
The classification of a mixture as posing a carcinogenic hazard is based on its inherent properties and does not provide information on the level of human cancer risk.

This calculator applies the lowest possible cut-off concentration limits given by GHS:
""")
st.image("static/carc.png", use_container_width=True)
st.write("""
The cut-off concentration limit for any ingredient classified as **Category 1A**, **1B**, or **Category 2 carcinogen**  
is therefore **≥ 0.1%**.
""")

# Germ Cell Mutagenicity
st.header("Germ Cell Mutagenicity")
st.write("""
As defined in [GHS Rev. 10, 2023](https://unece.org/transport/dangerous-goods/ghs-rev10-2023),  
**Germ Cell Mutagenicity** refers to heritable gene mutations, including heritable structural and numerical chromosome aberrations in germ cells occurring after exposure to a substance or mixture.

The cut-off concentration limits for ingredients of a mixture classified as germ cell mutagens can be found below:
""")
st.image("static/germcell.png", use_container_width=True)

# Reproductive Toxicity
st.header("Reproductive Toxicity")
st.write("""
As defined in [GHS Rev. 10, 2023](https://unece.org/transport/dangerous-goods/ghs-rev10-2023), **Reproductive Toxicity** is classified based on  
a range of adverse effects on sexual function and fertility in adult males and females, as well as developmental toxicity occurring after exposure.

The cut-off concentration limits for ingredients classified as reproductive toxicants or for effects on/via lactation are shown below:
""")
st.image("static/reprtox.png", use_container_width=True)
st.write("""
This calculator uses the lowest possible cut-off concentration limits, meaning the cut-off concentration is **0.1%** for any reproductive toxicant in a mixture.
""")

# Skin & Respiratory Sensitization
st.header("Skin & Respiratory Sensitization")
st.write("""
As defined in [GHS Rev. 10, 2023](https://unece.org/transport/dangerous-goods/ghs-rev10-2023):

- **Respiratory Sensitization**: Hypersensitivity of the airways occurring after inhalation of a substance or mixture.  
- **Skin Sensitization**: Allergic response occurring after skin contact with a substance or mixture.

The cut-off concentration limits for skin or respiratory sensitizers can be found below:
""")
st.image("static/sens.png", use_container_width=True)
st.write("""
This calculator applies the lowest possible cut-off limits:  
- **Category 1 sensitizer**: ≥ 0.1%  
- **Category 1B sensitizer**: ≥ 1.0%
""")