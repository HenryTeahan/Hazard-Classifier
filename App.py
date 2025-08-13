import streamlit as st
import os
import yaml
import pandas as pd

from calculations import (
    calculate_masses_with_hazards,
    calculate_masses,
    calculations,
    #calculate
    )


if "page" not in st.session_state:
    st.session_state.page = "input"
if "results" not in st.session_state:
    st.session_state.results = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'data')
STATIC_IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'Images')

hazard_data_path = os.path.join(DATA_DIR, 'hazard_data.csv')

limits_data_path = os.path.join(DATA_DIR, 'limits.yaml')

hazard_data = pd.read_csv(hazard_data_path, delimiter=';')


img_src_actox = 'static/acutetox.jpg'
img_src_corr_path = 'static/corrosive.jpg'
img_src_health_path = 'static/healthhaz.jpg'
img_src_warning_path = 'static/warning.jpg'

img_dirs = img_src_actox, img_src_health_path, img_src_corr_path, img_src_warning_path

st.markdown(
    """
    <style>
    .stApp {
        background-color: #ADD8E6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    div[data-baseweb="select"] > div {
        background-color: #e6f0ff !important;
        color: #000000 !important;         
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] svg {
      color: black !important;
      stroke: black !important;
      fill: black !important;
    }


    }
    div[data-baseweb="popover"] {
        background-color: #e6f0ff !important;
        color: #003366 !important;
    }
    </style>
    <style>
    div[data-baseweb="input"] input[type="number"] {
        background-color: #e6f0ff !important; 
        color: #000000 !important; 
    }
    div[data-baseweb="input"] {
        border: 1px solid #003366 !important;
    }
    </style>
    <style>
    div[data-baseweb="input"] input[type="text"] {
        background-color: #e6f0ff !important;
        color: #000000 !important; 
    }
    h1 {color: 
    #123499 !important} 
    h3 {color:
    black !important}

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>
/* Change selectbox label text color */
[data-testid="stSelectbox"] label {
    color: black !important;
}
[data-testid="stTextInput"] label {
    color: black !important
    }
[data-testid="stNumberInput"] label {
    color: black !important
    }
</style>
""", unsafe_allow_html=True)


limits = {}
with open(limits_data_path,'r') as file:
    limits = yaml.safe_load(file)

if "components" not in st.session_state:
    st.session_state.components = []



def show_input_page():
    if "reset" not in st.session_state:
        st.session_state.reset = False

    defaults = {
        "Name": "",
        "Percentage": 0.0,
        "ConcentrationmM": 0.0,
        "ConcentrationM": 0.0,
        "MolarMass": 0.0,
        "acortox": "Not Classified",
        "acdetox": "Not Classified",
        "acigtox": "Not Classified",
        "acivtox": "Not Classified",
        "acimtox": "Not Classified",
        "mut": "Not Classified",
        "car": "Not Classified",
        "rep": "Not Classified",
        "ski": "Not Classified",
        "res": "Not Classified",
        "se": "Not Classified",
        "re": "Not Classified",
        "sci": "Not Classified",
        "edi": "Not Classified",
        "cas": ""
    }

    st.title("Health Hazard Calculator")
    st.markdown(
    "<hr style='border: 2px solid black;'>",
    unsafe_allow_html=True
    )
    st.markdown("### Add your ingredients one-by-one. Click **Add Component** \
                when you have input the necessary data.")

    name = st.text_input("Name", value=defaults["Name"] if st.session_state.reset else st.session_state.get("Name", defaults["Name"]), key="Name")
    percentage = st.number_input("Percentage (w/w%)", min_value=0.0, step=0.01,
                                  value=defaults["Percentage"] if st.session_state.reset else st.session_state.get("Percentage", defaults["Percentage"]),
                                  key="Percentage")
    conc_mM = st.number_input("Concentration (mM)", min_value=0.0, step=0.01,
                               value=defaults["ConcentrationmM"] if st.session_state.reset else st.session_state.get("ConcentrationmM", defaults["ConcentrationmM"]),
                               key="ConcentrationmM")
    conc_M = st.number_input("Concentration (M)", min_value=0.0, step=0.0001,
                              value=defaults["ConcentrationM"] if st.session_state.reset else st.session_state.get("ConcentrationM", defaults["ConcentrationM"]),
                              key="ConcentrationM")
    molar_mass = st.number_input("Molar Mass (g/mol)", min_value=0.0, step=0.01,
                                  value=defaults["MolarMass"] if st.session_state.reset else st.session_state.get("MolarMass", defaults["MolarMass"]),
                                  key="MolarMass")

    st.markdown("---")

    def selectbox_with_reset(label, key, options):
        return st.selectbox(label, options,
                            index=options.index(defaults[key]) if st.session_state.reset else options.index(st.session_state.get(key, defaults[key])),
                            key=key)

    acute_oral = selectbox_with_reset("Acute Oral Toxicity", "acortox", ["Not Classified", "1", "2", "3", "4"])
    acute_dermal = selectbox_with_reset("Acute Dermal Toxicity", "acdetox", ["Not Classified", "1", "2", "3", "4"])
    acute_inhalation_gases = selectbox_with_reset("Inhalation Toxicity (gases)", "acigtox", ["Not Classified", "1", "2", "3", "4"])
    acute_inhalation_vapours = selectbox_with_reset("Inhalation Toxicity (vapours)", "acivtox", ["Not Classified", "1", "2", "3", "4"])
    acute_inhalation_mist = selectbox_with_reset("Inhalation Toxicity (mist/dust)", "acimtox", ["Not Classified", "1", "2", "3", "4"])
    mutagenicity = selectbox_with_reset("Mutagenicity", "mut", ["Not Classified", "1A", "1B", "2"])
    carcinogenicity = selectbox_with_reset("Carcinogenicity", "car", ["Not Classified", "1A", "1B", "2"])
    reproductive_toxicity = selectbox_with_reset("Reproductive Toxicity", "rep", ["Not Classified", "1A", "1B", "2"])
    skin_sensitizer = selectbox_with_reset("Skin Sensitization", "ski", ["Not Classified", "1", "1A", "1B"])
    respiratory_sensitizer = selectbox_with_reset("Respiratory Sensitization", "res", ["Not Classified", "1", "1A", "1B"])
    stotse = selectbox_with_reset("Single Target Organ Toxicity (single exposure)", "se", ["Not Classified", "1", "2"])
    stotre = selectbox_with_reset("Specific Target Organ Toxicity (repeated exposure)", "re", ["Not Classified", "1", "2"])
    skin = selectbox_with_reset("Skin Corrosion / Irritation", "sci", ["Not Classified", "1", "2", "3"])
    eye = selectbox_with_reset("Eye Damage / Irritation", "edi", ["Not Classified", "1", "2", "3"])

    st.markdown("### For including a registry search in your calculations, add the CAS number.")
    cas = st.text_input("CAS number", value=defaults["cas"] if st.session_state.reset else st.session_state.get("cas", defaults["cas"]), key="cas")

    component = {
        "name": name,
        "Acute Toxicity (Oral)": acute_oral,
        "Acute Toxicity (Dermal)": acute_dermal,
        "Acute Toxicity (Inhalation, gases)": acute_inhalation_gases,
        "Acute Toxicity (Inhalation, vapours)": acute_inhalation_vapours,
        "Acute Toxicity (Inhalation, mist/dust)": acute_inhalation_mist,
        "Mutagenicity": mutagenicity,
        "Carcinogenicity": carcinogenicity,
        "Reproductive Toxicity": reproductive_toxicity,
        "Specific Target Organ Toxicity (single exposure)": stotse,
        "Specific Target Organ Toxicity (repeated exposure)": stotre,
        "Eye Damage / Irritation": eye,
        "Skin Corrosion / Irritation": skin,
        "Skin Sensitizer": skin_sensitizer,
        "Respiratory Sensitizer": respiratory_sensitizer,
        "CAS": cas
    }

    if percentage:
        component["percentage"] = percentage
    if conc_mM:
        component["mM"] = conc_mM
        component["molarmass"] = molar_mass
    if conc_M:
        component["M"] = conc_M
        component["molarmass"]

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Add Component"):
            st.session_state.components.append(component)
            st.success(f"Added: {name}")
            st.session_state.reset = True 
            st.rerun()
    with col2:
        if st.button("Fill with Water"):
            st.session_state.components = calculate_masses(st.session_state.components)
            st.success("Filled with water to 100%")

    with col3:
        if st.button("Fill with Current Component"):
            st.session_state.components.append(component)
            st.session_state.components = calculate_masses_with_hazards(st.session_state.components)
            st.success("Filled with current component to 100%")

    if st.session_state.components:
        st.subheader("Current Components")
        df = pd.DataFrame(st.session_state.components)
        for col in ["name", "percentage", "CAS"]:
            if col not in df.columns:
                df[col] = None  # or ""
        df_show = df[["name", "percentage", "CAS"]]
        st.dataframe(df_show)

    if st.button("Calculate!", type="primary"):
        components = st.session_state.components
        calculations(components, limits, hazard_data, img_dirs)

    if st.button("Reset Components"):
        st.session_state.components.clear()
        st.session_state.reset = True
        st.rerun()
    else:
        st.session_state.reset = False

    
def show_results_page():
    st.markdown("""
    <style>
    strong {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>Hazard Classification Results</h1>", unsafe_allow_html=True)
    st.markdown(
    "<hr style='border: 2px solid black;'>",
    unsafe_allow_html=True
    )
    comps = st.session_state.results["components"]
    st.subheader("Ingredients")

    for c in comps:
        st.markdown(f"**{c['name']}: {c['percentage']}%**")
    st.subheader("Mixture Toxicity Profile")
    for desc, val in st.session_state.results["toxicity_data"].items():
        if val != None:
            st.markdown(f"**- {desc}: {val}**")
    st.subheader("H-Statements")
    sig = st.session_state.results["signal_word"]
    if sig:
        st.markdown(f"**Signal word: {sig}**") #TODO: Fix sometimes signal word comes in a list.
    for code, statement in zip(st.session_state.results['H_codes'],st.session_state.results["H_statement"]):
        st.markdown(f"**{code}: {statement}**")
    st.subheader("Pictograms")
    pictogram_paths = st.session_state.results["pictograms"]
    # TODO: Make sure max number of pictograms can fit in width!
    if len(pictogram_paths) > 0:
        cols = st.columns(len(pictogram_paths), gap = 'small', width = 280)
        for col, img_path in zip(cols, pictogram_paths):
            col.image(img_path, width=80) 
    
    st.markdown('</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.components.clear()
            st.session_state.page = "input"
            st.rerun()
    with col2:
        if st.button("Back without reset"):
            st.session_state.page = "input"
            st.rerun()
if st.session_state.page == "input":
    show_input_page()
else:
    show_results_page()