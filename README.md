**Hazard Classifier**
=======

**Introduction**
-----------
This is an app to calculate the chemical health hazards of mixtures/solutions based on the Global Harmonized System of Classification and Labelling of Chemicals (GHS Rev. 10, 2023).

**Input required:**
1. Chemical Name
2. Mass percentage (numerical, e.g. 10, 20 etc.)
3. Health hazard classifications as found in the Safety Data Sheet (SDS) (choose category from dropdown tab)

**Features:**
1. Outputs the calculated health hazard categories for the mixture/solution based on the principles in GHS Rev. 10, 2023 (See **Details**)
2. Outputs the associated hazard statements, pictograms and signal words. 
3. Entirely offline and open source.

**Requirements:**
1. Python 3.11.9 (tested)
2. Flask
3. numpy
4. pandas
(see requirements.txt)

**Limitations:**
This is a beta version and has not been thoroughly bug tested. 
GHS classification principles are merely approximations and these calculations in this app cannot be used as replacements for toxicological tests, or as confirmation of the non-hazardous nature of chemicals. This is a tool to speed up classifications and should not act as a replacement for good chemical intuitions or safe practices.

**Details**
-----------
_Acute Toxicity:_
Acute toxicity is calculated by using the Acute toxicity estimate (ATE) values and criteria for acute toxicity hazard categories. These ATE values are based on the conversion tables given in Table 3.1.2 in GHS Rev. 10, 2023. The oral, dermal and inhalation ATEs are calculated based on the equation in 3.1.3.6.1 if the concentrations of acutely toxic ingredients are under 10%, and otherwise based on the equation in 3.1.3.6.2.3. The final classification category is thus given by the updated ATE of the mixture compared to the ATE cutoff values for each of the acute toxicity classes and their categories (See Table 3.1.1). The associated hazard statements, signal words and pictograms are found in Table 3.1.3.

_Carcinogenicity, Germ Cell Mutagenicity, Reproductive Toxicity_:
Carcinogenicity, Mutagenicity and Reproductive Toxicity all share the same concentration cut off values of 0.1 % across all categories. 

_Specific target organ toxicity - single & repeated exposure_:
A cautious approach has been taken here. GHS Rev. 10, 2023 states that some authorities would first require label warnings at >10% concentrations of Specific target organ toxicants, where some require between 1-10%. We choose to take the most safe approach and set it at 1% for labelling, signal words and hazard statements for category 1 and 2 target organ toxicants. Note: Category 3 repeated exposure and single exposure toxicants are not included. The classification of such toxicants is too ambiguous without toxicological testing. 

_Sensitizers - skin and respiratory_:
Following GHS Rev. 10, 2023, any category 1 or 1A sensitizers have a cutoff of 0.1% and category 1B sensitiziers have a cutoff of 1%.

_Skin and eye damage_:
Skin corrosion / irritation are directly based on the hazard classifications through concentrations from GHS Rev. 10, 2023, Table 3.3.3 and Table 3.2.3.