from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'data')
STATIC_IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'Images')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

hazard_data_path = os.path.join(DATA_DIR, 'hazard_data.csv')

hazard_data = pd.read_csv(hazard_data_path, delimiter=';')


img_src_actox = 'static/Images/acutetox.jpg'
img_src_corr_path = 'static/Images/corrosive.jpg'
img_src_health_path = 'static/Images/healthhaz.jpg'
img_src_warning_path = 'static/Images/warning.jpg'

#hazard_data = pd.read_csv('data/hazard_data.csv',delimiter=';')

#img_src_actox = '/static/Images/acutetox.jpg'
#img_src_corr_path = '/static/Images/corrosive.jpg'
#img_src_health_path = '/static/Images/healthhaz.jpg'
#img_src_warning_path =  '/static/Images/warning.jpg'


def calculate_stotre(components):
  """
    Determine the stot re category of a chemical mixture based on its components.

    Parameters:
    components (list of dicts): A list where each dict represents a chemical component with its 'stot re' and 'percentage'.

    Returns:
    str: The stot re category of the mixture ('1', '2', or 'Not Classified').
  """
  stotre_cat = None
  sum_stotre_cat_1 = 0
  sum_stotre_cat_2 = 0

  for component in components:
    stotre_cat_component = component.get('Specific Target Organ Toxicity (repeated exposure)', None)
    stotre_perc = component['percentage']
    if stotre_cat_component == '1': 
      sum_stotre_cat_1 += stotre_perc
      if sum_stotre_cat_1 >= 1: #If ingredients classified as category 1 stot re exceed 1% immediately return cat 1 classification
        return '1'

    if stotre_cat_component == '2': #If ingredients classified as category 2 stot re exceed 1%, save the resultant classification as cat 2. If no cat 1 exist, cat 2 will be returned when loop finished.
      sum_stotre_cat_2 += stotre_perc
      if sum_stotre_cat_2 >= 1:
        stotre_cat = '2'

  return stotre_cat

def calculate_stotse(components):
    """
    Determine the stot se category of a chemical mixture based on its components.

    Parameters:
    components (list of dicts): A list where each dict represents a chemical component with its 'stot se' and 'percentage'.

    Returns:
    str: The stot se category of the mixture ('1', '2', or 'Not Classified').
    """
 
    stotse_cat = None
    sum_stotse_cat_1 = 0
    sum_stotse_cat_2 = 0
    for component in components:
        stotse_cat_component = component.get('Specific Target Organ Toxicity (single exposure)', None)
        stotse_perc = component['percentage']

        if stotse_cat_component == '1':
          sum_stotse_cat_1 += stotse_perc
          if sum_stotse_cat_1 >= 1:
            return '1'
        if stotse_cat_component == '2':
          sum_stotse_cat_2 += stotse_perc
          if sum_stotse_cat_2 >= 1:
            stotse_cat = '2'
    return stotse_cat

def calculate_muta(components):
    """
    Determine the mutagenicity category of a chemical mixture based on its components.

    Parameters:
    components (list of dicts): A list where each dict represents a chemical component with its 'Mutagenicity' and 'percentage'.

    Returns:
    str: The mutagenicity category of the mixture ('1A', '1B', '2', or 'Not Classified').
    """
    muta_cat = None
    muta_cat_1A_sum = 0
    muta_cat_1B_sum = 0
    muta_cat_2_sum = 0
    for component in components:
        muta_cat_component = component.get('Mutagenicity', None)
        muta_perc = component['percentage']

        if muta_cat_component == '1A':
          muta_cat_1A_sum += muta_perc
          if muta_cat_1A_sum >= 0.1:
            return '1A'  # Highest priority category, return immediately


        if muta_cat_component == '1B':
          muta_cat_1B_sum += muta_perc
          if muta_cat_1B_sum >= 0.1:
            muta_cat = '1B'  # Update category if 1A is not found


        if muta_cat_component == '2':
          muta_cat_2_sum += muta_perc
          if muta_cat_2_sum >= 1:
            if muta_cat != '1B':  # Update category if neither 1A nor 1B is found
                muta_cat = '2'
    return muta_cat

def calculate_carc(components):
    """
    Determine the carcinogenicity category of a chemical mixture based on its components.

    Parameters:
    components (list of dicts): A list where each dict represents a chemical component with its 'Carcinogenicity' and 'percentage'.

    Returns:
    str: The carcinogenicity category of the mixture ('1A', '1B', '2', or 'Not Classified').
    """

    carc_cat = None
    carc_cat_1A_sum = 0
    carc_cat_1B_sum = 0
    carc_cat_2_sum = 0

    for component in components:
        carc_cat_component = component.get('Carcinogenicity',None)
        carc_perc = component['percentage']

        if carc_cat_component == '1A':
          carc_cat_1A_sum += carc_perc
          if carc_cat_1A_sum >= 0.1:
            return '1A'  # Highest priority category, return immediately

        if carc_cat_component == '1B':
          carc_cat_1B_sum += carc_perc
          if carc_cat_1B_sum >= 0.1:
            carc_cat = '1B'  # Update category if 1A is not found

        if carc_cat_component == '2':
          carc_cat_2_sum += carc_perc
          if carc_cat_2_sum >= 0.1:
            if carc_cat != '1B':  # Update category if neither 1A nor 1B is found
                carc_cat = '2'
    return carc_cat

def calculate_repr(components):
    """
    Determine the reproductive hazard category of a chemical mixture based on its components.

    Parameters:
    components (list of dicts): A list where each dict represents a chemical component with its 'Reproductive' and 'percentage'.

    Returns:
    str: The reproductive category of the mixture ('1A', '1B', '2', or 'Not Classified').
    """
    repr_cat = None
    for component in components:
        repr_cat_component = component.get('Reproductive Toxicity', None)
        repr_perc = component['percentage']
        if repr_cat_component == '1A' and repr_perc >= 0.1:
            return '1A'  # Highest priority category, return immediately
        if repr_cat_component == '1B' and repr_perc >= 0.1:
            repr_cat = '1B'  # Update category if 1A is not found
        if repr_cat_component == '2' and repr_perc >= 0.1:
            if repr_cat != '1B':  # Update category if neither 1A nor 1B is found
                repr_cat = '2'
    return repr_cat

                    
def calculate_skin_corr_irr(components):
    for component in components:
        skin_cat = component.get('Skin Corrosion / Irritation', None)
        skin_perc = component['percentage']
    for component in components:
        skin_cat = component.get('Skin Corrosion / Irritation', None)
        skin_perc = component['percentage']
        if skin_cat == '1' and skin_perc >= 5: #If skin cat 1 exists at greater than 5%, immediately return cat. 1
            return '1'
        if skin_cat =='1' and skin_perc >= 1: #If skin cat 1 exists at between 1<= percentage <5 return cat. 2
            if skin_perc <5:
                return '2'
        if skin_cat == '2' and skin_perc >= 10: #If skin cat 2 exists at greater than 10% , return cat. 2
            return '2'
        if skin_cat == '2' and skin_perc >=1:
            if skin_perc <10 and skin_cat != 2: #if skin cat 2 exists at 1<= percentage <10, return cat. 3
                return '3'
        if skin_cat == '3' and skin_perc >=10: #if skin cat 3 exists at greater than 10% return cat. 3 (if skin_cat is not 2)
            if skin_cat != 2:
                return '3'
    return None




def calculate_oral_acute_toxicity(components):

    acute_oral_perc = 0
    adjusted_oral_perc = 0

    for component in components:
        oral_cat = component.get('Acute Toxicity (Oral)', None)
        perc = component['percentage']
        #Applying Acute Toxicity Estimate (ATE) values to oral classification 
        if oral_cat == "1":
            ATE = 0.5
        if oral_cat == "2": 
            ATE = 5
        if oral_cat == "3":
            ATE = 100
        if oral_cat == "4":
            ATE = 500
        if oral_cat:
            acute_oral_perc += perc
        if oral_cat:
            frac = perc
            adjusted_oral_perc += frac / ATE #calculating RHS of ATE formula

        
    if acute_oral_perc > 10:
        ATE_oral = (100-acute_oral_perc) / adjusted_oral_perc #If the sum of acute oral toxic ingredients is greater than 10%, apply the appropriate formula (100-acute_oral_perc)
    if acute_oral_perc == 0: #if no acute oral toxic ingredients exist, return none
        return None 
    else: 
        ATE_oral = 100 / adjusted_oral_perc

    if ATE_oral > 0 and ATE_oral <= 5:
        ATE_oral_cat = 1
    if ATE_oral >5 and ATE_oral <=50:
        ATE_oral_cat = 2
    if ATE_oral >50 and ATE_oral <= 300:
        ATE_oral_cat = 3
    if ATE_oral >300 and ATE_oral <= 2000:
        ATE_oral_cat = 4
    if ATE_oral > 2000:
        ATE_oral_cat = None
    print(f'ATE_oral : {ATE_oral}') #For dev
    return ATE_oral_cat

def calculate_dermal_acute_toxicity(components):

    acute_dermal_perc = 0
    adjusted_dermal_perc = 0

    for component in components:
        dermal_cat = component.get('Acute Toxicity (Dermal)', None)
        perc = component['percentage']
        if dermal_cat == "1":
            ATE = 5
        if dermal_cat == "2": 
            ATE = 50
        if dermal_cat == "3":
            ATE = 300
        if dermal_cat == "4":
            ATE = 1100
        if dermal_cat:
            acute_dermal_perc += perc
        if dermal_cat:
            frac = perc
            adjusted_dermal_perc += frac / ATE
        
    if acute_dermal_perc > 10:
        ATE_dermal = (100-acute_dermal_perc) / adjusted_dermal_perc
    if acute_dermal_perc == 0:
        return None
    else:
        ATE_dermal = 100 / adjusted_dermal_perc
    if ATE_dermal > 0 and ATE_dermal <= 50:
        ATE_dermal_cat = 1
    if ATE_dermal >50 and ATE_dermal <=200:
        ATE_dermal_cat = 2
    if ATE_dermal >200 and ATE_dermal <= 1000:
        ATE_dermal_cat = 3
    if ATE_dermal >1000 and ATE_dermal <= 2000:
        ATE_dermal_cat = 4
    if ATE_dermal > 2000:
        ATE_dermal_cat = None
    
    print(f'ATE_dermal : {ATE_dermal}')
    return ATE_dermal_cat

def calculate_inhalation_gases_acute_toxicity(components):

    acute_inh_perc = 0
    adjusted_inh_perc = 0
    
    for component in components:
        inh_cat = component.get('Acute Toxicity (Inhalation, gases)', None)
        perc = component['percentage']
        if inh_cat == "1":
            ATE = 10
        if inh_cat == "2": 
            ATE = 100
        if inh_cat == "3":
            ATE = 700
        if inh_cat == "4":
            ATE = 4500
        if inh_cat:
            acute_inh_perc += perc
        if inh_cat:
            frac = perc
            print(frac)
            adjusted_inh_perc += frac / ATE

    print(adjusted_inh_perc)
    if acute_inh_perc > 10:
        ATE_inh = (100-acute_inh_perc) / adjusted_inh_perc
    if acute_inh_perc == 0:
        return None
    else:
        ATE_inh = 100 / adjusted_inh_perc

    if ATE_inh > 0 and ATE_inh <= 100:
        ATE_inh_cat = 1
    if ATE_inh > 100 and ATE_inh <=500:
        ATE_inh_cat = 2
    if ATE_inh >500 and ATE_inh <= 2500:
        ATE_inh_cat = 3
    if ATE_inh >2500 and ATE_inh <= 20000:
        ATE_inh_cat = 4
    if ATE_inh > 20000:
        ATE_inh_cat = None

    print(f'ATE_inh_gas : {ATE_inh}')

    return ATE_inh_cat

def calculate_respiratory_sensitizer(components):
    for component in components:
        resp_cat = component.get('Respiratory Sensitizer', None)
        perc = component['percentage']
        if resp_cat == '1':
            if perc >= 0.1:
                return '1'
        if resp_cat == '1A':
            if perc >= 0.1:
                return '1'
        if resp_cat == '1B':
            if perc >= 1:
                return '1'
                
def calculate_skin_sensitizer(components):
    for component in components:
        skin_cat = component.get('Skin Sensitizer', None)
        perc = component['percentage']
        if skin_cat == '1':
            if perc >= 0.1:
                return '1'
        if skin_cat == '1A':
            if perc >= 0.1:
                return '1'
        if skin_cat == '1B':
            if perc >= 1:
                return '1'

def calculate_inhalation_vapours_acute_toxicity(components):
    
    acute_inh_perc = 0
    adjusted_inh_perc = 0
    
    for component in components:
        inh_cat = component.get('Acute Toxicity (Inhalation, vapours)', None)
        perc = component['percentage']
        if inh_cat == "1":
            ATE = 0.05
        if inh_cat == "2": 
            ATE = 0.5
        if inh_cat == "3":
            ATE = 3
        if inh_cat == "4":
            ATE = 11
        if inh_cat:
            acute_inh_perc += perc
        if inh_cat:
            frac = perc
            adjusted_inh_perc += frac / ATE
        
    if acute_inh_perc > 10:
        ATE_inh = (100-acute_inh_perc) / adjusted_inh_perc
    if acute_inh_perc == 0:
        return None
    else:
        ATE_inh = 100 / adjusted_inh_perc
    if ATE_inh > 0 and ATE_inh <= 0.5:
        ATE_inh_cat = 1
    if ATE_inh > 0.5 and ATE_inh <=2:
        ATE_inh_cat = 2
    if ATE_inh >2 and ATE_inh <= 10:
        ATE_inh_cat = 3
    if ATE_inh >10 and ATE_inh <= 20:
        ATE_inh_cat = 4
    if ATE_inh > 20:
        ATE_inh_cat = None
    print(f'ATE_inh, vapours : {ATE_inh}')
    return ATE_inh_cat

def calculate_inhalation_mist_acute_toxicity(components):

    acute_inh_perc = 0
    adjusted_inh_perc = 0
    
    for component in components:
        inh_cat = component.get('Acute Toxicity (Inhalation, mist/dust)', None)
        perc = component['percentage']
        if inh_cat == "1":
            ATE = 0.005
        if inh_cat == "2": 
            ATE = 0.05
        if inh_cat == "3":
            ATE = 0.5
        if inh_cat == "4":
            ATE = 1.5
        if inh_cat:
            acute_inh_perc += perc
        if inh_cat:
            frac = perc
            adjusted_inh_perc += frac / ATE        
    if acute_inh_perc > 10:
        ATE_inh = (100-acute_inh_perc) / adjusted_inh_perc
    if acute_inh_perc == 0:
        return None
    else:
        ATE_inh = 100 / adjusted_inh_perc
    if ATE_inh > 0 and ATE_inh <= 0.05:
        ATE_inh_cat = 1
    if ATE_inh > 0.05 and ATE_inh <=0.5:
        ATE_inh_cat = 2
    if ATE_inh >0.5 and ATE_inh <= 1.0:
        ATE_inh_cat = 3
    if ATE_inh >1.0 and ATE_inh <= 5.0:
        ATE_inh_cat = 4
    if ATE_inh > 5.0:
        ATE_inh_cat = None
    print(f'ATE_inh,gas/mist : {ATE_inh}')
    return ATE_inh_cat

def calculate_eye_corr_irr(components):
    def_eye = None
    for component in components: 
        skin_cat = component.get('Skin Corrosion / Irritation', None)
        eye_cat = component.get('Eye Damage / Irritation', None)
        perc = component['percentage']
        if eye_cat == '1' and perc >=3:
            return '1'
        if skin_cat == '1' and perc >=3:
            return '1'
        if eye_cat == '2':
            if perc >= 10:
                def_eye = 2
        if eye_cat == '1' and perc >=1:
            def_eye = 2
        for component2 in components:
            eye_cat2 = component2.get('Eye Damage / Irritation', None)
            skin_cat2 = component2.get('Skin Corrosion / Irritation', None)
            perc2 = component2['percentage']
            if component != component2:
                if skin_cat and eye_cat2 == '1':
                    if perc + perc2 >= 3:
                        return '1'
                if skin_cat2 and eye_cat == '1':
                    if perc + perc2 >= 3:
                        return '1'
                if skin_cat and eye_cat2 == '1':
                    if perc + perc2 >= 1:
                        return '2'
                if skin_cat2 and eye_cat == '1':
                    if perc + perc2 >= 1:
                        return '2'
    return def_eye
def h_statements(hazards):
    toxic_oral_H, toxic_derm_H, toxic_inh_H, muta_H, carc_H, repr_H, stotse_H, stotre_H, skin_H, eye_H, skinsen_H, respsen_H = [None]*12
    carc, repr, muta, stotse, stotre, toxic_oral, toxic_derm, toxic_inhg, toxic_inhv, toxic_inhm, skin, eye, skinsen, respsen = hazards

    if toxic_oral != None:
        if toxic_oral == 1 or toxic_oral == 2 or toxic_oral == '1' or toxic_oral == '2':
            toxic_oral_H = 'H300'
        elif toxic_oral == 3 or toxic_oral == '3':
            toxic_oral_H = 'H301'
        elif toxic_oral == 4 or toxic_oral == '4':
            toxic_oral_H = 'H302'
        else:
            print('toxic oral not defined but not None')

    if toxic_derm != None:
        if toxic_derm == 1 or toxic_derm == 2 or toxic_derm == '1' or toxic_derm == '2':
            toxic_derm_H = 'H310'
        elif toxic_derm == 3:
            toxic_derm_H = 'H311'
        elif toxic_derm == 4:
            toxic_derm_H = 'H312'
        else:
            print('toxic dermal not defined but not None', toxic_derm)
    for tox in toxic_inhg, toxic_inhv, toxic_inhm:

        if tox != None:
            if tox == 1 or tox == 2 or tox == '1' or tox == '2':
                toxic_inh_H = 'H330'
            elif tox == 3:
                toxic_inh_H = 'H331'
            elif tox == 4:
                toxic_inh_H = 'H332'
            else:
                print('toxic inhalation not defined but not None', tox)
        else:
            continue

    if muta != None:
        if muta == 1 or muta == '1A' or muta == '1B' or muta == '1':
            muta_H = 'H340'
        elif muta == 2 or muta == '2':
            muta_H = 'H341'
        else:
            print('mutagenicity not defined but not None', muta)

    if carc != None:
        if carc == 1 or carc == '1A' or carc == '1B' or carc == '1':
            carc_H = 'H350'
        elif carc == 2 or carc == '2':
            carc_H = 'H351'
        else:
            print('carcinogenicity not defined but not None', carc)

    if repr != None:
        if repr == 1 or repr == '1A' or repr == '1B' or repr == '1':
            repr_H = 'H360'
        elif repr == 2 or repr == '2':
            repr_H = 'H361'
        else:
            print('reproductive toxicity not defined but not None', repr)

    if stotse != None:
        if stotse == 1 or stotse == '1':
            stotse_H = 'H370'
        elif stotse == 2 or stotse == '2':
            stotse_H = 'H371'
        else:
            print('STOT SE not defined but not None', stotse)
    if stotre != None:
        if stotre == 1 or stotre == '1':
            stotre_H = 'H372'
        elif stotre == 2 or stotre == '2':
            stotre_H = 'H373'
        else:
            print('STOT RE not defined but not None', stotre)

    if skin != None:
        if skin == 1 or skin == '1':
            skin_H = 'H314'
        elif skin == 2 or skin == '2':
            skin_H = 'H315'
        elif skin == 3 or skin == '3':
            skin_H = 'H316'
        else:
            print('Skin not defined but not None', skin)

    if eye != None:
        if eye == 1 or eye == '1':
            eye_H = 'H318'
        elif eye == '2A' or eye == '2' or eye == 2:
            eye_H = 'H319'
        elif eye == '2B':
            eye_H = 'H320'
        else:
            print('Eye not defined but not None', eye)
    if skinsen != None:
        if skinsen == 1 or skinsen == '1' or skinsen == '1A' or skinsen == '1B':
            skinsen_H = 'H317'
        else:
            print('Skinsen not defined but not None', skinsen)
    if respsen != None:
        if respsen == 1 or respsen == '1' or respsen == '1A' or respsen == '1B':
            respsen_H = 'H334'
        else:
            print('Respsen not defined but not None', respsen)
    H_statements = [toxic_oral_H, toxic_derm_H, toxic_inh_H, muta_H, carc_H, repr_H, stotse_H, stotre_H, skin_H, eye_H, skinsen_H, respsen_H]

    return H_statements


def get_H_statements(H_statements, components):
    hazard_no = []
    hazard_statement = []
    pictogram = []
    signal_word = []
    
    for H in H_statements:
        if H != None:
            h_no, h_stat, pict, sign = [hazard_data[hazard_data['H-code'] == H].values.flatten()[i] for i in range(4)]
            hazard_statement.append(h_stat); pictogram.append(pict); signal_word.append(sign); hazard_no.append(H)
        else:
            continue

    return hazard_no, hazard_statement, pictogram, signal_word


components = []
def calculations(components):
    carc = calculate_carc(components)
    repr = calculate_repr(components)
    muta = calculate_muta(components)
    stotse = calculate_stotse(components)
    stotre = calculate_stotre(components)
    toxic_oral = calculate_oral_acute_toxicity(components)
    toxic_dermal = calculate_dermal_acute_toxicity(components)
    toxic_inh_g = calculate_inhalation_gases_acute_toxicity(components)
    toxic_inh_v = calculate_inhalation_vapours_acute_toxicity(components)
    toxic_inh_m = calculate_inhalation_mist_acute_toxicity(components)
    skin = calculate_skin_corr_irr(components)
    eye = calculate_eye_corr_irr(components)
    skinsen = calculate_skin_sensitizer(components)
    respsen = calculate_respiratory_sensitizer(components)
    hazards = [carc, repr, muta, stotse, stotre, toxic_oral, toxic_dermal, toxic_inh_g, toxic_inh_v, toxic_inh_m, skin, eye, skinsen, respsen]

    for hazard in hazards:
        if hazard != None or 'Not classified':
            return carc, repr, muta, stotse, stotre, toxic_oral, toxic_dermal, toxic_inh_g, toxic_inh_v, toxic_inh_m, skin, eye, skinsen, respsen
print(components)
carc, repr, muta, stotse, stotre, toxic_oral, toxic_dermal, toxic_inh_g, toxic_inh_v, toxic_inh_m, skin, eye, skinsen, eyesen= calculations(components)
print(f'carc={carc}, repr = {repr}, muta = {muta}, stotse = {stotse}, stotre = {stotre}, toxic_oral = {toxic_oral}, toxic_dermal = {toxic_dermal}, toxic_inh_g ={toxic_inh_g}, toxic_inh_v = {toxic_inh_v}, toxic_inh_m = {toxic_inh_m}, skin={skin}, eye={eye}, skinsen={skinsen}, eyesen={eyesen}')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        percentage = request.form['percentage']
        acute_toxicity_oral = request.form['acute_toxicity_oral']
        acute_toxicity_dermal = request.form['acute_toxicity_dermal']
        acute_toxicity_inhalation_gases = request.form['acute_toxicity_inhalation_gases']
        acute_toxicity_inhalation_vapours = request.form['acute_toxicity_inhalation_vapours']
        acute_toxicity_inhalation_mist = request.form['acute_toxicity_inhalation_mist']
        mutagenicity = request.form['mutagenicity']
        carcinogenicity = request.form['carcinogenicity']
        reproductive_toxicity = request.form['reproductive_toxicity']
        stotse = request.form['stotse']
        stotre = request.form['stotre']
        skin = request.form['skin']
        eye = request.form['eye']
        skinsen = request.form['skin_sensitizer']
        respsen = request.form['respiratory_sensitizer']
        component = {
            'name': name,
            'percentage':percentage,
            'Acute Toxicity (Oral)': acute_toxicity_oral,
            'Acute Toxicity (Dermal)': acute_toxicity_dermal,
            'Acute Toxicity (Inhalation, gases)': acute_toxicity_inhalation_gases,
            'Acute Toxicity (Inhalation, vapours)': acute_toxicity_inhalation_vapours,
            'Acute Toxicity (Inhalation, mist/dust)': acute_toxicity_inhalation_mist,
            'Mutagenicity': mutagenicity,
            'Carcinogenicity': carcinogenicity,
            'Reproductive Toxicity': reproductive_toxicity,
            'Specific Target Organ Toxicity (single exposure)': stotse,
            'Specific Target Organ Toxicity (repeated exposure)': stotre,
            'Eye Damage / Irritation': eye,
            'Skin Corrosion / Irritation': skin,
            'Skin Sensitizer' : skinsen,
            'Respiratory Sensitizer' : respsen,
        }

        components.append(component)

        print(f"Component added: {component}")

    
    return render_template('index.html', components=components)
def get_pictograms(hazard_no):
    pictograms = set()

    for H in hazard_no:
        if H in ['H300', 'H301', 'H310', 'H311', 'H330', 'H331']:  # Acute toxicity
            pictograms.add(f'<img src="{img_src_actox}">')

        if H in ['H340', 'H341', 'H350', 'H351', 'H360', 'H361', 'H370', 'H371', 'H372', 'H373', 'H334']:  # Health hazard
            pictograms.add(f'<img src="{img_src_health_path}">')

        if H in ['H314', 'H318']:  # Corrosive
            pictograms.add(f'<img src="{img_src_corr_path}">')

        if H in ['H317', 'H320', 'H319', 'H316', 'H315', 'H312', 'H302', 'H332']:  # Warning
            pictograms.add(f'<img src="{img_src_warning_path}">')

    return list(pictograms)

@app.route("/add", methods=["POST"])
def add_component():
    name = request.form["name"]
    percentage = float(request.form["percentage"])

    components.append({"name": name, "percentage": percentage})

    return redirect(url_for("index"))



@app.route('/calculate')
def calculate():
    # Debugging print to verify components before calculation
    print(f"Components before calculation: {components}")

    ingred = []
    ingred_perc = []
    total_perc = 0
    for component in components:
        print('getting component percentage', component.get('percentage'))
        if component.get('percentage') != '':  # Handle percentage
            ingred.append(component.get('name')); ingred_perc.append(component.get('percentage'))
            component['percentage'] = float(component['percentage'])
            perc = component['percentage']
            total_perc += perc
            print(total_perc)

    if round(total_perc) != 100:
        raise ValueError(f"The total percentage of all components must sum to 100 \n Total percentage: {total_perc}")
    
    mixture_oral_toxicity = calculate_oral_acute_toxicity(components)
    mixture_dermal_toxicity= calculate_dermal_acute_toxicity(components)
    mixture_inhalation_toxicity_gases= calculate_inhalation_gases_acute_toxicity(components)
    mixture_inhalation_toxicity_vapours = calculate_inhalation_vapours_acute_toxicity(components)
    mixture_inhalation_toxicity_mist = calculate_inhalation_mist_acute_toxicity(components)
    mixture_muta = calculate_muta(components)
    mixture_carc = calculate_carc(components)
    mixture_repr = calculate_repr(components)
    mixture_stotse = calculate_stotse(components)
    mixture_stotre = calculate_stotre(components)
    mixture_skin = calculate_skin_corr_irr(components)
    mixture_eye = calculate_eye_corr_irr(components)
    mixture_skinsen = calculate_skin_sensitizer(components)
    mixture_respsen = calculate_respiratory_sensitizer(components)

    print(f"mixture_oral_toxicity: {mixture_oral_toxicity}")
    print(f"mixture_dermal_toxicity: {mixture_dermal_toxicity}")
    print(f"mixture_inhalation_toxicity_gases: {mixture_inhalation_toxicity_gases}")
    print(f"mixture_inhalation_toxicity_vapours: {mixture_inhalation_toxicity_vapours}")
    print(f"mixture_inhalation_toxicity_mist: {mixture_inhalation_toxicity_mist}")
    print(f"mixture_muta: {mixture_muta}")
    print(f"mixture_carc: {mixture_carc}")
    print(f"mixture_repr: {mixture_repr}")
    print(f"mixture_stotse: {mixture_stotse}")
    print(f"mixture_stotre: {mixture_stotre}")
    print(f"mixture_skin: {mixture_skin}")
    print(f"mixture_eye: {mixture_eye}")
    print(f"mixture_skinsen:{mixture_skinsen}")
    print(f"mixture_respsen:{mixture_respsen}")
    hazards = [mixture_carc, mixture_repr, mixture_muta, mixture_stotse, mixture_stotre, mixture_oral_toxicity, mixture_dermal_toxicity,
               mixture_inhalation_toxicity_gases, mixture_inhalation_toxicity_vapours, mixture_inhalation_toxicity_mist, mixture_skin, mixture_eye, mixture_skinsen, mixture_respsen]
    H_statements = h_statements(hazards)
    hazard_no, hazard_statement, pictogram, signal_word = get_H_statements(H_statements, components)
    print(hazard_no, hazard_statement, pictogram, signal_word)
    if len(signal_word) > 1:
        danger = False
        warning = False
        for word in signal_word:
            if word == 'Danger':
                danger = True
            if word == 'Warning':
                warning = True
        if danger == True:
            sig_word = 'Danger'
        if warning == True and danger == False:
            sig_word = 'Warning'
        if danger == False and warning == False:
            sig_word = None

    toxicity_data = {
    "acute oral toxicity category": mixture_oral_toxicity,
    "acute dermal toxicity category": mixture_dermal_toxicity,
    "acute inhalation toxicity (gases) category": mixture_inhalation_toxicity_gases,
    "acute inhalation toxicity (vapours) category": mixture_inhalation_toxicity_vapours,
    "acute inhalation toxicity (mist/dust) category": mixture_inhalation_toxicity_mist,
    "mutagenicity category": mixture_muta,
    "carcinogenicity category": mixture_carc,
    "reproductive toxicity category": mixture_repr,
    "skin sensitization category": mixture_skinsen,
    "respiratory sensitization category": mixture_respsen,
    "Specific Target Organ Toxicity (single exposure) category": mixture_stotse,
    "Specific Target Organ Toxicity (repeated exposure) category": mixture_stotre,
    "skin corrosion / irritation category": mixture_skin,
    "serious eye damage / eye irritation category": mixture_eye,
    }

    result = "\n".join(
        f"<p>The {desc} of the mixture is: {val}</p>"
        for desc, val in toxicity_data.items() if val is not None
    )
    print('length of result', len(result))
    if len(result) == 0:
        result = "Not classified as a hazardous mixture in accordance with GHS"

    result_imgs = list(set(get_pictograms(hazard_no)))
    print(f"Number of pictograms", len(result_imgs), len(hazard_statement))

    if sig_word == 'Danger' or sig_word == 'Warning':
        result_H_statements = (
            f"<ul>"
            +"".join(f"<li><strong>Signal word: {sig_word}</strong>")
            + "".join(f"<li><strong>{hazard_no[i]}</strong>: {hazard_statement[i]}</li>" for i in range(len(hazard_statement)))
            + "</ul>"
        )
    else:
        result_H_statements = (
            f"<ul>"
            + "".join(f"<li><strong>{hazard_no[i]}</strong>: {hazard_statement[i]}</li>" for i in range(len(hazard_statement)))
            + "</ul>"
        )
    print(len(result_H_statements))
    if len(result_H_statements) < 10:
        result_H_statements = "Not classified as a hazardous mixture in accordance with GHS"
    return render_template("results.html", result = result, result_imgs = result_imgs, result_H_statements = result_H_statements)


@app.route("/")
def home():
    return render_template("index.html", components = components)

@app.route("/reset", methods=["POST"])
def reset():
    global components
    components.clear()
    return redirect('/')
def main():
    app.run(debug=True)