Repository for code and data associated with the A2M framework paper.

## Data

# PLM-based Analogy Generation

* [Candidate Discipline-specific Adaptive Analogies for arts, social science (ss) and business (bus) disciplines](/data/discp_adapt)
* [Candidate Preference-specific Adaptive Analogies for cooking (cook), gardening (gar), music (mus), and sports preferences](/data/pref_adapt)
* [Candidate Non-Adaptive Analogies for Cybersecurity (cyber), Machine Learning (ai), and High-school science (sci) domains](/data/non_adapt)
* [Non-Analogies used as negative sample for training Analoginess Scorer](/data/non_analogies)
* [Additional Analogies (generated with source concept as part of the prompt) for High-school science domain used as positive samples for training Analoginess Scorer](/data/sci_src)

For all files names, p<em>n</em> means analogies generated with prompt id <em>n</em> in the paper, ht means high temperature, lt means low temperature.

Each file contains the following on each new line:

>{Generated Analogy}\t{Target Concept}\t{Prompt}

# Source Extraction

* [Source extracted from Discipline-specific Adaptive Analogies](/data/extracted_src/discp_adapt)
* [Source extracted from Preference-specific Adaptive Analogies](/data/extracted_src/pref_adapt)
* [Source extracted from Non-Adaptive Analogies](/data/extracted_src/non_adapt)

Each file contains the following on each new line:

>{Generated Analogy}\t{Target Concept}\t{Prompt}\t{Temperature -- low: lt or high: ht}\t{Domain/Preference/Discipline}\t{Extracted Source(s)}



