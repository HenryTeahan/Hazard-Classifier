import streamlit as st

st.title("About Health Hazard Calculator")
st.markdown("""
This calculator is built upon the Globally Harmonized System of Classification and 
Labelling of Chemicals ([GHS Rev. 10, 2023](https://unece.org/transport/dangerous-goods/ghs-rev10-2023)) as produced by the United Nations.

This calculator uses the harmonized criteria for classifying mixtures according to their health hazards along with their required hazard communication elements such as pictograms and H-statements.

As mentioned in GHS Rev. 10, 2023, if a complete mixture has actual test data available, the classification of the mixture should always be based on that data.

If test data is not available, bridging principles or specific calculations may be applied, giving an estimation of the different health hazards as documented in Part 3 of GHS Rev. 10, 2023.

**Note:** This calculator is a general guide exclusively using the calculations and thresholds provided in the GHS. It does not replace expert judgement and does not account for specific thresholds provided by [ECHA](https://echa.europa.eu/en/home) or similar chemical agencies.

Always carefully read the SDS in full, as specific hazards not covered here may be raised.
""")

