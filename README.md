# GHS Mixture Hazard Classification Calculator

A Streamlit-based calculator that classifies chemical mixtures using official **[GHS cut-off concentrations](https://unece.org/transport/documents/2023/07/standards/ghs-rev10)**, producing a hazard profile based on ingredient hazard data.

## What It Does

Enter a list of chemical ingredients and their contributions (by percentage or moles), and this app automatically:

- Applies **GHS classification rules** for health hazards
- Calculates applicable hazard classes such as:
  - Acute Toxicity
  - Skin Corrosion/Irritation
  - Carcinogenicity
  - And more
- Outputs a complete hazard profile, including:
  - Hazard class names
  - GHS pictograms
  - Signal words (e.g., *Danger*, *Warning*)
  - H-statements (e.g., *H301: Toxic if swallowed*)
- Allows **printing to PDF** for documentation or SDS use

## Built With

- [Python](https://www.python.org/)  
- [Streamlit](https://streamlit.io/) (web app framework)  


## Features

- Mass or concentration and molar mass based input calculated automatically to w/w%
- Fully compliant with **GHS health hazard thresholds**
- Takes most careful approach, always choosing lowest possible cut-off concentration limit
- Automatically composes hazard pictograms and signal words
- Clean, printable summary page
- No internet or API dependency — runs **entirely locally**
- About page detailing calculations
  
## Use Cases

- SDS authoring and compliance checks  
- Laboratory safety and chemical mixture assessments  
- Regulatory prep for REACH, CLP, OSHA HazCom  
- Teaching and training in chemical safety  

> **Note:** This calculator applies **only the GHS cut-off concentration thresholds** to classify mixture hazards.  
> It does **not** incorporate experimental toxicity data or in-depth risk assessment.  
> Use this tool as a **guidance aid** and **not as definitive evidence** for regulatory or safety decisions.  
> Always consult qualified safety professionals and official testing results when necessary.

## Getting Started
  Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ghs-mixture-calculator.git
   cd ghs-mixture-calculator
   # Set up virtual environment
   python3 -m venv venv
   source venv/bin/activate
   # Install dependencies
   pip install -r requirements.txt
   # Run Streamlit App
   streamlit run App.py
   ```
## Integration with On-Site Registry Checks

This calculator is designed to be easily integrated with **on-site chemical registry systems** or compliance workflows.

While proprietary registry documents cannot be shared publicly, the app's modular architecture allows seamless extension or API hooking to:

- Automatically fetch ingredient details from internal chemical databases  
- Perform batch hazard classification against local chemical inventories  
- Streamline SDS creation and regulatory audits on-site  

To facilitate this, example integration workflows and scripts can be provided privately upon request to henry@teahan.dk.

## Disclaimer

This calculator performs hazard classification exclusively using **GHS cut-off concentration thresholds** as defined by international regulations.  

It **does not** use empirical toxicity testing or replace comprehensive chemical risk assessments.  

The results are intended as a **guidance tool** only. For formal safety evaluations or legal compliance, please refer to certified testing data and consult with chemical safety experts.


