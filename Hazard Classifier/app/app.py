from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
import numpy as np
import pandas as pd
import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'data')
STATIC_IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'Images')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

hazard_data_path = os.path.join(DATA_DIR, 'hazard_data.csv')
hhm_data_path = os.path.join(DATA_DIR, 'hhm_data2.csv')
pf_data_path = os.path.join(DATA_DIR, 'pf_data.csv')
limits_data_path = os.path.join(DATA_DIR, 'limits.yaml')

hazard_data = pd.read_csv(hazard_data_path, delimiter=';')
hhm_data = pd.read_csv(hhm_data_path)
pf_data = pd.read_csv(pf_data_path)

img_src_actox = 'static/Images/acutetox.jpg'
img_src_corr_path = 'static/Images/corrosive.jpg'
img_src_health_path = 'static/Images/healthhaz.jpg'
img_src_warning_path = 'static/Images/warning.jpg'
img_src_hhm = 'static/Images/hhm.jpg'
img_src_pf = 'static/Images/pf.jpg'

#hazard_data = pd.read_csv('data/hazard_data.csv',delimiter=';')
#hhm_data = pd.read_csv('data/hhm_data2.csv',delimiter=',')
#pf_data = pd.read_csv('data/pf_data.csv',delimiter=',')

hhm_data_cas = hhm_data['CAS number'].to_list()
pf_data_cas = set(pf_data['CAS'].to_list())
limits = {}
with open(limits_data_path,'r') as file:
    limits = yaml.safe_load(file)
def calculate_masses_with_hazards(components, total_mass = 1000):
    total_solute_mass = 0
    for c in components[:-1]:
        perc = c.get('percentage')
        mM = c.get('milimolar')
        M = c.get('molar')
        molar_mass = c.get('molarmass')

        if perc not in [None, '']:
            mass = float(perc) * total_mass / 100
            c['mass'] = mass

        elif mM not in [None, ''] and molar_mass not in [None, '']:
            mass = float(mM) * 1e-3 * float(molar_mass) * 1
            c['mass'] = mass

        elif M not in [None, ''] and molar_mass not in [None, '']:
            mass = float(M) * float(molar_mass) * 1
            c['mass'] = mass

        else:
            c['mass'] = 0

        total_solute_mass += c['mass']
    water_mass = total_mass - total_solute_mass
    if water_mass < 0:
        print("Warning: solute masses exceed total target mass. No water added.")
        water_mass = 0    
    components[-1]['mass'] = water_mass

    final_total_mass = total_solute_mass + water_mass
    for c in components:
        print(c)
        c['percentage'] = (c['mass'] / final_total_mass) * 100     
    print(f"Total mass (g): {final_total_mass}")
    print(f"Sum of percentages after fill: {sum(c['percentage'] for c in components)}")

    return components
    
def calculate_masses(components, total_mass=1000):
    """
    Convert percentages and molarities into mass in grams,
    add missing water mass to fill total_mass,
    then return updated components with 'mass' and final 'percentage'.
    """

    total_solute_mass = 0
    for c in components:
        perc = c.get('percentage')
        mM = c.get('milimolar')
        M = c.get('molar')
        molar_mass = c.get('molarmass')

        if perc not in [None, '']:
            mass = float(perc) * total_mass / 100
            c['mass'] = mass

        elif mM not in [None, ''] and molar_mass not in [None, '']:
            mass = float(mM) * 1e-3 * float(molar_mass) * 1
            c['mass'] = mass

        elif M not in [None, ''] and molar_mass not in [None, '']:
            mass = float(M) * float(molar_mass) * 1
            c['mass'] = mass

        else:
            c['mass'] = 0

        total_solute_mass += c['mass']

    water_mass = total_mass - total_solute_mass
    if water_mass < 0:
        print("Warning: solute masses exceed total target mass. No water added.")
        water_mass = 0

    components.append({'name': 'water', 'mass': water_mass})

    final_total_mass = total_solute_mass + water_mass
    for c in components:
        c['percentage'] = (c['mass'] / final_total_mass) * 100

    print(f"Total mass (g): {final_total_mass}")
    print(f"Sum of percentages after fill: {sum(c['percentage'] for c in components)}")

    return components



def calculate_stotre(components, limits):
  """
    Determine the stot re category of a chemical mixture based on its components.

    Parameters:
    components (list of dicts): A list where each dict represents a chemical component with its 'stot re' and 'percentage'.

    Returns:
    str: The stot re category of the mixture ('1', '2', or 'Not Classified').
  """
  l = limits['stotre_limits'] 
  stotre_cat = None
  sum_stotre_cat_1 = 0
  sum_stotre_cat_2 = 0

  for component in components:
    stotre_cat_component = component.get('Specific Target Organ Toxicity (repeated exposure)', None)
    stotre_perc = component['percentage']
    if stotre_cat_component == '1': 
      sum_stotre_cat_1 += stotre_perc
      if sum_stotre_cat_1 >= l["1"]: 
        return '1'

    if stotre_cat_component == '2': 
      sum_stotre_cat_2 += stotre_perc
      if sum_stotre_cat_2 >= l["2"]:
        stotre_cat = '2'

  return stotre_cat

def calculate_stotse(components, limits):
    """
    Determine the stot se category of a chemical mixture based on its components.

    Parameters:
    components (list of dicts): A list where each dict represents a chemical component with its 'stot se' and 'percentage'.

    Returns:
    str: The stot se category of the mixture ('1', '2', or 'Not Classified').
    """
    l = limits['stotse_limits']
    stotse_cat = None
    sum_stotse_cat_1 = 0
    sum_stotse_cat_2 = 0
    for component in components:
        stotse_cat_component = component.get('Specific Target Organ Toxicity (single exposure)', None)
        stotse_perc = component['percentage']

        if stotse_cat_component == '1':
          sum_stotse_cat_1 += stotse_perc
          if sum_stotse_cat_1 >= l["1"]:
            return '1'
        if stotse_cat_component == '2':
          sum_stotse_cat_2 += stotse_perc
          if sum_stotse_cat_2 >= l["2"]:
            stotse_cat = '2'
    return stotse_cat

def calculate_muta(components, limits):
    """
    Determine the mutagenicity category of a chemical mixture based on its components.

    Parameters:
    components (list of dicts): A list where each dict represents a chemical component with its 'Mutagenicity' and 'percentage'.

    Returns:
    str: The mutagenicity category of the mixture ('1A', '1B', '2', or 'Not Classified').
    """
    l = limits['muta_limits']
    muta_cat = None
    muta_cat_1A_sum = 0
    muta_cat_1B_sum = 0
    muta_cat_2_sum = 0
    for component in components:
        muta_cat_component = component.get('Mutagenicity', None)
        muta_perc = component['percentage']

        if muta_cat_component == '1A':
          muta_cat_1A_sum += muta_perc
          if muta_cat_1A_sum >= l["1A"]:
            return '1A'  


        if muta_cat_component == '1B':
          muta_cat_1B_sum += muta_perc
          if muta_cat_1B_sum >= l["1B"]:
            muta_cat = '1B'


        if muta_cat_component == '2':
          muta_cat_2_sum += muta_perc
          if muta_cat_2_sum >= l["2"]:
            if muta_cat != '1B': 
                muta_cat = '2'
    return muta_cat

def calculate_carc(components, limits):
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
    
    l = limits['carc_limits']

    for component in components:
        carc_cat_component = component.get('Carcinogenicity',None)
        carc_perc = component['percentage']

        if carc_cat_component == '1A':
          carc_cat_1A_sum += carc_perc
          if carc_cat_1A_sum >= l["1A"]:
            return '1A'  

        if carc_cat_component == '1B':
          carc_cat_1B_sum += carc_perc
          if carc_cat_1B_sum >= l["1B"]:
            carc_cat = '1B'

        if carc_cat_component == '2':
          carc_cat_2_sum += carc_perc
          if carc_cat_2_sum >= l["2"]:
            if carc_cat != '1B': 
                carc_cat = '2'
    return carc_cat

def calculate_repr(components, limits):
    """
    Determine the reproductive hazard category of a chemical mixture based on its components.

    Parameters:
    components (list of dicts): A list where each dict represents a chemical component with its 'Reproductive' and 'percentage'.

    Returns:
    str: The reproductive category of the mixture ('1A', '1B', '2', or 'Not Classified').
    """
    l = limits['repr_limits']

    repr_cat = None
    for component in components:
        repr_cat_component = component.get('Reproductive Toxicity', None)
        repr_perc = component['percentage']
        if repr_cat_component == '1A' and repr_perc >= l["1A"]:
            return '1A'  
        if repr_cat_component == '1B' and repr_perc >= l["1B"]:
            repr_cat = '1B'  
        if repr_cat_component == '2' and repr_perc >= l["2"]:
            if repr_cat != '1B':  
                repr_cat = '2'
    return repr_cat

                    
def calculate_skin_corr_irr(components, limits):

    l = limits['skin_corr_limits']
    skin_dict = {'cat1':0, 
                 'cat2':0,
                 'cat3':0}
    for component in components:
        skin_cat = component.get('Skin Corrosion / Irritation', None)
        skin_perc = component['percentage']
        if skin_cat == '1' and skin_perc >= l["1_geq"]: 
            return '1' # direct return if one immmediately triggers category 1
        if skin_cat == '1':
            skin_dict['cat1'] += skin_perc
        if skin_cat == '2':
            skin_dict['cat2'] += skin_perc
        if skin_cat == '3':
            skin_dict['cat3'] += skin_perc
    # looking at cumulative sum of the different classes
    print(skin_dict)
    if skin_dict['cat1'] >= l["1_geq"]:
        return '1'
    elif skin_dict['cat1'] >= l["cat1_to_cat2 geq"]:
        return '2'
    elif skin_dict['cat2'] >= l["2_geq"]:
         return '2'
    elif skin_dict['cat2'] + 10*skin_dict['cat1'] >= l["2_geq"]:
        return '2'
    elif skin_dict['cat2'] >= l['cat2_to_cat3 geq']:
        return '3'
    elif skin_dict['cat3'] >= l['3_geq']:
        return '3'
    elif skin_dict['cat2'] + 10*skin_dict['cat1'] >= l["2_10xskin+skin2_geq"]:
        return '3'
    elif skin_dict['cat2'] + 10*skin_dict['cat1'] + skin_dict['cat3'] >= l["3_geq"]:
        return '3'
    else:
        return None



def calculate_oral_acute_toxicity(components, limits):

    acute_oral_perc = 0
    adjusted_oral_perc = 0

    cat = limits["ate_category_translation_oral"]
    thr = limits["ate_oral_thresholds"]

    for component in components:
        oral_cat = component.get('Acute Toxicity (Oral)', None)
        perc = component['percentage']
        if oral_cat == "1":
            ATE = cat["1"]
        if oral_cat == "2": 
            ATE = cat["2"]
        if oral_cat == "3":
            ATE = cat["3"]
        if oral_cat == "4":
            ATE = cat["4"]
        if oral_cat:
            acute_oral_perc += perc
        if oral_cat:
            frac = perc
            adjusted_oral_perc += frac / ATE 

        
   # if acute_oral_perc > 10:
   #     ATE_oral = (100-acute_oral_perc) / adjusted_oral_perc 
    if acute_oral_perc == 0: 
        return None 
    else: 
        ATE_oral = 100 / adjusted_oral_perc

    if ATE_oral > 0 and ATE_oral <= thr["max_leq_1"]:
        ATE_oral_cat = 1
    if ATE_oral > thr["max_leq_1"] and ATE_oral <= thr["max_leq_2"]:
        ATE_oral_cat = 2
    if ATE_oral > thr["max_leq_2"] and ATE_oral <= thr["max_leq_3"]:
        ATE_oral_cat = 3
    if ATE_oral > thr["max_leq_3"] and ATE_oral <= thr["max_leq_4"]:
        ATE_oral_cat = 4
    if ATE_oral > thr["max_leq_4"]:
        ATE_oral_cat = None
    print(f'ATE_oral : {ATE_oral}') 
    return ATE_oral_cat

def calculate_dermal_acute_toxicity(components, limits):

    cat = limits["ate_category_translation_dermal"]
    thr = limits["ate_dermal_thresholds"]

    acute_dermal_perc = 0
    adjusted_dermal_perc = 0

    for component in components:
        dermal_cat = component.get('Acute Toxicity (Dermal)', None)
        perc = component['percentage']
        if dermal_cat == "1":
            ATE = cat["1"]
        if dermal_cat == "2": 
            ATE = cat["2"]
        if dermal_cat == "3":
            ATE = cat["3"]
        if dermal_cat == "4":
            ATE = cat["4"]
        if dermal_cat:
            acute_dermal_perc += perc
        if dermal_cat:
            frac = perc
            adjusted_dermal_perc += frac / ATE
        
   # if acute_dermal_perc > 10:
   #     ATE_dermal = (100-acute_dermal_perc) / adjusted_dermal_perc
    if acute_dermal_perc == 0:
        return None
    else:
        ATE_dermal = 100 / adjusted_dermal_perc
    if ATE_dermal > 0 and ATE_dermal <= thr["max_leq_1"]:
        ATE_dermal_cat = 1
    if ATE_dermal > thr["max_leq_1"] and ATE_dermal <= thr["max_leq_2"]:
        ATE_dermal_cat = 2
    if ATE_dermal > thr["max_leq_2"] and ATE_dermal <= thr["max_leq_3"]:
        ATE_dermal_cat = 3
    if ATE_dermal > thr["max_leq_3"] and ATE_dermal <= thr["max_leq_4"]:
        ATE_dermal_cat = 4
    if ATE_dermal > thr["max_leq_4"]:
        ATE_dermal_cat = None
    
    print(f'ATE_dermal : {ATE_dermal}')
    return ATE_dermal_cat

def calculate_inhalation_gases_acute_toxicity(components, limits):

    cat = limits["ate_category_translation_inh"]
    thr = limits["ate_inh_thresholds"]

    acute_inh_perc = 0
    adjusted_inh_perc = 0
    
    for component in components:
        inh_cat = component.get('Acute Toxicity (Inhalation, gases)', None)
        perc = component['percentage']
        if inh_cat == "1":
            ATE = cat["1"]
        if inh_cat == "2": 
            ATE = cat["2"]
        if inh_cat == "3":
            ATE = cat["3"]
        if inh_cat == "4":
            ATE = cat["4"]
        if inh_cat:
            acute_inh_perc += perc
        if inh_cat:
            frac = perc
            print(frac)
            adjusted_inh_perc += frac / ATE

    print(adjusted_inh_perc)
  #  if acute_inh_perc > 10:
  #      ATE_inh = (100-acute_inh_perc) / adjusted_inh_perc
    if acute_inh_perc == 0:
        return None
    else:
        ATE_inh = 100 / adjusted_inh_perc

    if ATE_inh > 0 and ATE_inh <= thr["max_leq_1"]:
        ATE_inh_cat = 1
    if ATE_inh > thr["max_leq_1"] and ATE_inh <=thr["max_leq_2"]:
        ATE_inh_cat = 2
    if ATE_inh > thr["max_leq_2"] and ATE_inh <= thr["max_leq_3"]:
        ATE_inh_cat = 3
    if ATE_inh > thr["max_leq_3"] and ATE_inh <= thr["max_leq_4"]:
        ATE_inh_cat = 4
    if ATE_inh > thr["max_leq_4"]:
        ATE_inh_cat = None

    print(f'ATE_inh_gas : {ATE_inh}')

    return ATE_inh_cat

def calculate_respiratory_sensitizer(components, limits):
    l = limits['respi_sens_limits']
    for component in components:
        resp_cat = component.get('Respiratory Sensitizer', None)
        perc = component['percentage']
        if resp_cat == '1':
            if perc >= l["1"]:
                return '1'
        if resp_cat == '1A':
            if perc >= l["1A"]:
                return '1'
        if resp_cat == '1B':
            if perc >= l["1B"]:
                return '1'
                
def calculate_skin_sensitizer(components, limits):
    l = limits['skin_sens_limits']
    for component in components:
        skin_cat = component.get('Skin Sensitizer', None)
        perc = component['percentage']
        if skin_cat == '1':
            if perc >= l['1']:
                return '1'
        if skin_cat == '1A':
            if perc >= l['1A']:
                return '1'
        if skin_cat == '1B':
            if perc >= l['1B']:
                return '1'

def calculate_inhalation_vapours_acute_toxicity(components, limits):
    
    acute_inh_perc = 0
    adjusted_inh_perc = 0
    
    cat = limits["ate_category_translation_inh_vapours"]
    thr = limits["ate_inh_vapours_thresholds"]
    
    for component in components:
        inh_cat = component.get('Acute Toxicity (Inhalation, vapours)', None)
        perc = component['percentage']
        if inh_cat == "1":
            ATE = cat["1"]
        if inh_cat == "2": 
            ATE = cat["2"]
        if inh_cat == "3":
            ATE = cat["3"]
        if inh_cat == "4":
            ATE = cat["4"]
        if inh_cat:
            acute_inh_perc += perc
        if inh_cat:
            frac = perc
            adjusted_inh_perc += frac / ATE
        
   # if acute_inh_perc > 10:
   #     ATE_inh = (100-acute_inh_perc) / adjusted_inh_perc
    if acute_inh_perc == 0:
        return None
    else:
        ATE_inh = 100 / adjusted_inh_perc
    if ATE_inh > 0 and ATE_inh <= thr["max_leq_1"]:
        ATE_inh_cat = 1
    if ATE_inh >  thr["max_leq_1"] and ATE_inh <=  thr["max_leq_2"]:
        ATE_inh_cat = 2
    if ATE_inh >  thr["max_leq_2"] and ATE_inh <=  thr["max_leq_3"]:
        ATE_inh_cat = 3
    if ATE_inh > thr["max_leq_3"] and ATE_inh <=  thr["max_leq_4"]:
        ATE_inh_cat = 4
    if ATE_inh >  thr["max_leq_4"]:
        ATE_inh_cat = None
    print(f'ATE_inh, vapours : {ATE_inh}')
    return ATE_inh_cat

def calculate_inhalation_mist_acute_toxicity(components, limits):
    cat = limits["ate_category_translation_inh_mist"]
    thr = limits["ate_inh_mist_thresholds"]
    
    acute_inh_perc = 0
    adjusted_inh_perc = 0
    
    for component in components:
        inh_cat = component.get('Acute Toxicity (Inhalation, mist/dust)', None)
        perc = component['percentage']
        if inh_cat == "1":
            ATE = cat["1"]
        if inh_cat == "2": 
            ATE = cat["2"]
        if inh_cat == "3":
            ATE = cat["3"]
        if inh_cat == "4":
            ATE = cat["4"]
        if inh_cat:
            acute_inh_perc += perc
        if inh_cat:
            frac = perc
            adjusted_inh_perc += frac / ATE        
  #  if acute_inh_perc > 10:
  #      ATE_inh = (100-acute_inh_perc) / adjusted_inh_perc
    if acute_inh_perc == 0:
        return None
    else:
        ATE_inh = 100 / adjusted_inh_perc
    if ATE_inh > 0 and ATE_inh <= thr["max_leq_1"]:
        ATE_inh_cat = 1
    if ATE_inh > thr["max_leq_1"] and ATE_inh <= thr["max_leq_2"]:
        ATE_inh_cat = 2
    if ATE_inh > thr["max_leq_2"] and ATE_inh <= thr["max_leq_3"]:
        ATE_inh_cat = 3
    if ATE_inh > thr["max_leq_3"] and ATE_inh <= thr["max_leq_4"]:
        ATE_inh_cat = 4
    if ATE_inh > thr["max_leq_4"]:
        ATE_inh_cat = None
    print(f'ATE_inh,gas/mist : {ATE_inh}')
    return ATE_inh_cat

def calculate_eye_corr_irr(components, limits):
    l = limits["eye_limits"]
    dictio = {'eyecat1':0, 'eyecat2':0, 'skin1':0}

    for component in components:
        skin_cat = component.get('Skin Corrosion / Irritation', None)
        eye_cat = component.get('Eye Damage / Irritation', None)
        perc = component['percentage']

        # Immediate return if either is above 3%
        if eye_cat == '1' and perc >= l["1_eye"]: 
            return '1'
        if skin_cat == '1' and perc >=l["1_skin"]:
            return '1'
        # If both cat 1 skin and eye; only count once
        if skin_cat == '1' and eye_cat == '1':
            dictio['skin1'] += perc 
        # If not both cat 1 skin and eye; count as many as needed
        elif skin_cat == '1':
            dictio['skin1'] += perc
        elif eye_cat == '1':
            dictio['eyecat1'] += perc
        elif eye_cat == '2':
            dictio['eyecat2'] += perc

    if dictio['eyecat1'] + dictio['skin1'] >= l['1_eye']:
        return '1'
    elif dictio['eyecat1'] + dictio['skin1'] >= l['eye_cat1_to_cat2_geq']:
        return '2'
    if dictio['eyecat2'] >= l['2_eye']:
        return '2'
    elif 10*(dictio['skin1']+dictio['eyecat1'])+dictio['eyecat2'] >= l['10(skincat1+eyecat1)+eyecat2']:
        return '2'       
    else:
        return None

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

        if H == 'HHM':
            pictograms.add(f'<img src="{img_src_hhm}">')
        if H == 'PF':
            pictograms.add(f'<img src="{img_src_pf}">')
    return list(pictograms)

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

def is_hhm(components, limits):
        l = limits["hhm_limits"]
        hhm = []
        for component in components:
            if 'CAS' in component:
                if component['CAS'] in hhm_data_cas:  # hhm_data_cas must be defined somewhere as a set or list
                    if component["percentage"] > l["hhm"]:
                        hhm.append({
                            'cas': component['CAS'],
                            'name': component['name'],
                            'percentage': component['percentage']
                        })
            else:
                continue
        return hhm

def is_pf(components, limits):
    l = limits["peroxide_limits"]
    pf = []
    for component in components:
        if 'CAS' in component:
            if component['CAS'] in pf_data_cas:
                if component["percentage"] > l["per"]:
                    pf.append({
                        'cas': component['CAS'],
                        'name': component['name'],
                        'percentage': component['percentage']})
        else:
            continue
    return pf

def get_H_statements(H_statements, components, limits):
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

    hhm = is_hhm(components, limits)
    pf = is_pf(components, limits)

    if len(hhm) > 0:

        print([f"Has HHM {h}" for h in hhm])
        hhm_string = ""
        for item in hhm:
            hhm_string += f"This mixture contains an Amgen High Hazard material: {item['name']} at {item['percentage']}%.\n"
        hazard_statement.append(hhm_string); pictogram.append('hhm'); signal_word.append('HHM'); hazard_no.append('HHM')

    if len(pf) > 0:

        print([f"Has Amgen Peroxide former {p}" for p in pf])
        pf_string = ""
        for item in pf:
            pf_string += f"This mixture contains an Amgen Peroxide Former: {item['name']} at {item['percentage']}%.\n"
            print(item['name'])
        hazard_statement.append(pf_string); pictogram.append('PF'); signal_word.append('PF'); hazard_no.append('PF')

    return hazard_no, hazard_statement, pictogram, signal_word


components = []
def calculations(components, limits):
    carc = calculate_carc(components, limits)
    repr = calculate_repr(components, limits)
    muta = calculate_muta(components, limits)
    stotse = calculate_stotse(components, limits)
    stotre = calculate_stotre(components, limits)
    toxic_oral = calculate_oral_acute_toxicity(components, limits)
    toxic_dermal = calculate_dermal_acute_toxicity(components, limits)
    toxic_inh_g = calculate_inhalation_gases_acute_toxicity(components, limits)
    toxic_inh_v = calculate_inhalation_vapours_acute_toxicity(components, limits)
    toxic_inh_m = calculate_inhalation_mist_acute_toxicity(components, limits)
    skin = calculate_skin_corr_irr(components, limits)
    eye = calculate_eye_corr_irr(components, limits)
    skinsen = calculate_skin_sensitizer(components, limits)
    respsen = calculate_respiratory_sensitizer(components, limits)
    hazards = [carc, repr, muta, stotse, stotre, toxic_oral, toxic_dermal, toxic_inh_g, toxic_inh_v, toxic_inh_m, skin, eye, skinsen, respsen]

    for hazard in hazards:
        if hazard != None or 'Not classified':
            return carc, repr, muta, stotse, stotre, toxic_oral, toxic_dermal, toxic_inh_g, toxic_inh_v, toxic_inh_m, skin, eye, skinsen, respsen
print(components)
carc, repr, muta, stotse, stotre, toxic_oral, toxic_dermal, toxic_inh_g, toxic_inh_v, toxic_inh_m, skin, eye, skinsen, eyesen= calculations(components, limits)
print(f'carc={carc}, repr = {repr}, muta = {muta}, stotse = {stotse}, stotre = {stotre}, toxic_oral = {toxic_oral}, toxic_dermal = {toxic_dermal}, toxic_inh_g ={toxic_inh_g}, toxic_inh_v = {toxic_inh_v}, toxic_inh_m = {toxic_inh_m}, skin={skin}, eye={eye}, skinsen={skinsen}, eyesen={eyesen}')

@app.route('/', methods=['GET', 'POST'])
def index():

    global components
    print("Index route accessed")
    if request.method == 'POST':
        action = request.form.get("action")
        print("received action", action)
        name = request.form['name']
        if request.form['percentage']:
            percentage = request.form['percentage']
        else:
            percentage = None
        if request.form['mM']:
            milimolar = float(request.form["mM"])
            molarmass = float(request.form["molarmass"])
        else:
            milimolar = None
        if request.form['M']:
            molar = float(request.form["M"])
            molarmass = float(request.form["molarmass"])
        else:
            molar = None
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
        cas = request.form['CAS']

        component = {
            'name': name,
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
            'CAS' : cas
            
        }
        if percentage != None:
            component['percentage'] = percentage
        if milimolar != None:
            component['milimolar'] = milimolar
            component['molarmass'] = molarmass
        if molar != None:
            component['molar'] = molar
            component['molarmass'] = molarmass

        print(f"Component added: {component}")
        
        if action == 'add':
            components.append(component)
            print(f"Added component: {component}")

        elif action == 'fill':
            components = calculate_masses(components, total_mass=1000)

        elif action == 'fillwcomps':
        
            components.append(component)
            print(f"Added component: {component}")
            print(f"Added component for hazard-based fill: {component}")

            components = calculate_masses_with_hazards(components, total_mass=1000)
            print(f"filled",components)
        else:
            print(
                    " Problem !!"
            )
    
    return render_template('index.html', components=components)

@app.route('/calculate')
def calculate():
    global components

    # Debugging print to verify components before calculation
    print(f"Components before calculation: {components}")
  #  print(f"cas numbers before calculation: {}")

    components = calculate_masses(components, total_mass=1000)
    for component in components:
        component['percentage'] = float(component['percentage'])
    mixture_oral_toxicity = calculate_oral_acute_toxicity(components, limits)
    mixture_dermal_toxicity= calculate_dermal_acute_toxicity(components, limits)
    mixture_inhalation_toxicity_gases= calculate_inhalation_gases_acute_toxicity(components, limits)
    mixture_inhalation_toxicity_vapours = calculate_inhalation_vapours_acute_toxicity(components, limits)
    mixture_inhalation_toxicity_mist = calculate_inhalation_mist_acute_toxicity(components, limits)
    mixture_muta = calculate_muta(components, limits)
    mixture_carc = calculate_carc(components, limits)
    mixture_repr = calculate_repr(components, limits)
    mixture_stotse = calculate_stotse(components, limits)
    mixture_stotre = calculate_stotre(components, limits)
    mixture_skin = calculate_skin_corr_irr(components, limits)
    mixture_eye = calculate_eye_corr_irr(components, limits)
    mixture_skinsen = calculate_skin_sensitizer(components, limits)
    mixture_respsen = calculate_respiratory_sensitizer(components, limits)

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
    hazard_no, hazard_statement, pictogram, signal_word = get_H_statements(H_statements, components, limits)
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
    else:
        print('signalword',signal_word, type(signal_word))
        if len(signal_word) == 1:
            if signal_word[0] != 'HHM' or signal_word[0] != 'PF':
                sig_word = signal_word
            else:
                sig_word = None
        else:
            sig_word = signal_word
            print('signal word bug length',len(signal_word))
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
    return render_template("results.html", components = components, result = result, result_imgs = result_imgs, result_H_statements = result_H_statements)

@app.route("/reset", methods=["POST"])
def reset():
    global components
    components.clear()
    return redirect('/')

@app.route("/Delete", methods=["POST"])
def delete():
    global components
    if len(components) > 1:
        del components[-1]
    return redirect('/')
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/acutetoxicity")
def acutetoxicity():
    return render_template("acutetoxicity.html")

@app.route("/eyeandskin")
def eyeandskin():
    return render_template("eyeandskin.html")

@app.route("/carcmutarepr")
def carcmutarepr():
    return render_template("carcmutarepr.html")
def main():
    app.run(debug=True)