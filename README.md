# ⚗️ GHS Mixture Hazard Classification Calculator

A web-based calculator that classifies chemical mixtures using official **GHS cut-off concentrations**, producing a full hazard profile based on ingredient data.

## 🔍 What It Does

Enter a list of chemical ingredients and their contributions (by percentage or moles), and this app automatically:

- Applies **GHS classification rules** for health hazards
- Calculates applicable hazard classes such as:
  - Acute Toxicity
  - Skin Corrosion/Irritation
  - Carcinogenicity
  - And more
- Outputs a complete hazard profile, including:
  - ✅ Hazard class names
  - ✅ GHS pictograms
  - ✅ Signal words (e.g., *Danger*, *Warning*)
  - ✅ H-statements (e.g., *H301: Toxic if swallowed*)
- Allows **printing to PDF** for documentation or SDS use

## 💻 Built With

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- HTML/CSS/Javascript

## 📦 Features

- Mass or mole-based input (supports molar mass entry)
- Fully compliant with **GHS health hazard thresholds**
- Automatically composes hazard pictograms and signal words
- Clean, printable summary page
- No internet or API dependency — runs **entirely locally**

## 🧪 Use Cases

- SDS authoring and compliance checks  
- Laboratory safety and chemical mixture assessments  
- Regulatory prep for REACH, CLP, OSHA HazCom  
- Teaching and training in chemical safety  

## 🚀 Getting Started
  Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ghs-mixture-calculator.git
   cd ghs-mixture-calculator
   # Set up virtual environment
   python3 -m venv venv
   source venv/bin/activate
   # Install dependencies
   pip install -r requirements.txt
   # On Windows:
   Double-click start_app.bat - will launch local session
   # On Linux, navigate to the main directory
   cd .../'Hazard Classifier'
   # Run .sh file:
   ./start_app.sh
   # Alternatively, run directly in terminal:
   py run.py
   Open http://127.0.0.1:5000
   ```
## 🔗 Integration with On-Site Registry Checks

This calculator is designed to be easily integrated with **on-site chemical registry systems** or compliance workflows.

While proprietary registry documents cannot be shared publicly, the app's modular architecture allows seamless extension or API hooking to:

- Automatically fetch ingredient details from internal chemical databases  
- Perform batch hazard classification against local chemical inventories  
- Streamline SDS creation and regulatory audits on-site  

To facilitate this, example integration workflows and scripts can be provided privately upon request to henry@teahan.dk.


