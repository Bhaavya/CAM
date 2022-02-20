Repository for code and data associated with the A2M framework paper.

## Data

# PLM-based Analogy Generation

* `/data/discp_adapt`: Candidate Discipline-specific Adaptive Analogies for arts, social science (ss) and business (bus) disciplines
* `/data/pref_adapt`: Candidate Preference-specific Adaptive Analogies for cooking (cook), gardening (gar), music (mus), and sports preferences
* `/data/non_adapt`: Candidate Non-Adaptive Analogies for Cybersecurity (cyber), Machine Learning (ai), and High-school science (sci) domains
* `/data/non_analogies`: Non-Analogies used as negative sample for training Analoginess Scorer
* `/data/sci_src`: Additional Analogies (generated with source concept as part of the prompt) for High-school science domain used as positive samples for training Analoginess Scorer

For all files names, p<em>n</em> means analogies generated with prompt id <em>n</em> in the paper, ht means high temperature, lt means low temperature.

Each file contains the following fields separated by tab: (1) Generated Analogy, (2) Target Concept, (3) Prompt

# Source Extraction

* `/data/extracted_src/discp_adapt.txt`: Source extracted from Discipline-specific Adaptive Analogies 
* `/data/extracted_src/pref_adapt.txt`: Source extracted from Preference-specific Adaptive Analogies
* `/data/extracted_src/non_adapt.txt`: Source extracted from Non-Adaptive Analogies

Each file contains the following fields separated by tab: (1) Generated Analogy, (2) Target Concept, (3) Prompt, (4) Temperature (low -- lt or high --ht) (5) Domain (for non-adaptive analogies)/Preference/Discipline, (6) Extracted Source(s)



