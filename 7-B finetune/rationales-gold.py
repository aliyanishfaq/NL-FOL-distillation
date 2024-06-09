import requests
import random
import json
import time


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = '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'


def get_rationales(nl, fol):
    messages_choice_1 = [
        {"role": "user", "content": f"""
            Here is a natural language statement: {nl} Here is its first order logic translation: {fol}
            Your task is to write a brief explanation to teach how to come up with the first order logic (FOL) statement when given the natural language (NL) statement. Be brief. 
            Actually explain how or why the logic works, why those specific logical operators were chosen, how to identify what are the predicates and its arguments, etc. 
            Explain the reasoning behind these choices, don't just state them. When explaining the reasoning, quote evidence for the reasoning directly from the natural language statement and quote words directly corresponding to choice of logical operators.
            REFERENCING THE NATURAL LANGUAGE STATEMENT WHEN EXPLAINING IS VERY VERY VERY IMPORTANT.
            Strictly follow the same format exactly as the example outputs. Provide the explanation in a similar way with references from the natural language statement. 
            Only output the explanation, nothing else, no other comment or remarks, and no other headings. Follow the same subheadings as in the example outputs.
            3 EXAMPLES
            EXAMPLE INPUT 1
            NL: An architecturally interesting building features unique design elements, visually appealing materials, and innovative construction techniques.
            FOL: ∀x (Building(x) ∧ UniqueDesignElements(x) ∧ VisuallyAppealingMaterials(x) ∧ InnovativeConstructionTechniques(x) → ArchitecturallyInteresting(x))
            EXAMPLE OUTPUT 1:
            Identify Key Entities and Relationships: The key entities are Building, UniqueDesignElements, VisuallyAppealingMaterials, InnovativeConstructionTechniques, and ArchitecturallyInteresting.
            The relationships are described as attributes of the building. Use variables \( x \) for Building.
            Logical Formulation Structure: ∀x (Building(x) ∧ UniqueDesignElements(x) ∧ VisuallyAppealingMaterials(x) ∧ InnovativeConstructionTechniques(x) → ArchitecturallyInteresting(x))
            Explanation for Logical Formulation: The universal quantifier \( \forall x \) ensures the statement applies to all buildings ("An architecturally interesting building").
            The predicates Building(x), UniqueDesignElements(x), VisuallyAppealingMaterials(x), and InnovativeConstructionTechniques(x) identify the building and its attributes. The implication (\( \rightarrow \)) indicates that if all these attributes are true for a building, then it is architecturally interesting, capturing the condition "features unique design elements, visually appealing materials, and innovative construction techniques" leading to "architecturally interesting". 
            Logical conjunctions (\( \land \)) link the attributes ("unique design elements", "visually appealing materials", and "innovative construction techniques").
            EXAMPLE INPUT 2
            NL: A rainbow appears when sunlight is refracted, reflected, and dispersed by water droplets in the atmosphere.
            FOL: ∀x (Rainbow(x) ↔ ∃y ∃z (Sunlight(y) ∧ WaterDroplets(z) ∧ Refracted(y, z) ∧ Reflected(y, z) ∧ Dispersed(y, z)))
            EXAMPLE OUTPUT 2:
            Identify Key Entities and Relationships: The key entities are Rainbow, Sunlight, and WaterDroplets, and the relationships are Refracted (Sunlight, WaterDroplets), Reflected (Sunlight, WaterDroplets), and Dispersed (Sunlight, WaterDroplets). Use variables \( x \) for Rainbow, \( y \) for Sunlight, and \( z \) for WaterDroplets.
            Logical Formulation Structure: ∀x (Rainbow(x) ↔ ∃y ∃z (Sunlight(y) ∧ WaterDroplets(z) ∧ Refracted(y, z) ∧ Reflected(y, z) ∧ Dispersed(y, z)))
            Explanation for Logical Formulation: The universal quantifier \( \forall x \) ensures the statement applies to all instances where a rainbow appears ("A rainbow appears"). Existential quantifiers \( \exists y \) and \( \exists z \) indicate there exists sunlight and water droplets necessary for the appearance of a rainbow. 
            The predicates Rainbow(x), Sunlight(y), and WaterDroplets(z) identify the rainbow, sunlight, and water droplets respectively. Refracted(y, z), Reflected(y, z), and Dispersed(y, z) describe the physical interactions between sunlight and water droplets. The biconditional operator \( \leftrightarrow \) in \( (Rainbow(x) \leftrightarrow ...) \) specifies that a rainbow's appearance is directly and exclusively tied to the conditions of sunlight being refracted, reflected, and dispersed by water droplets, capturing the entirety of the condition "when sunlight is refracted, reflected, and dispersed by water droplets in the atmosphere". Logical conjunctions (\( \land \)) link these conditions to emphasize that all these interactions are necessary simultaneously for a rainbow to appear.
            EXAMPLE INPUT 3
            NL: A cake is ready to be served if it's cooled and the frosting is applied.
            FOL: ReadyToServe(cake) ↔ (Cooled(cake) ∧ FrostingApplied(cake))
            EXAMPLE OUTPUT 3:
            Identify Key Entities and Relationships: The key entities are "cake," and the states or conditions affecting it are represented by the predicates "Cooled" and "FrostingApplied." The primary relationship described is "ReadyToServe," indicating the cake's readiness based on certain conditions.
            Logical Formulation Structure: ReadyToServe(cake) ↔ (Cooled(cake) ∧ FrostingApplied(cake))
            Explanation for Logical Formulation: The biconditional operator (↔) is used to express that the readiness of the cake to be served is directly and exclusively linked to two simultaneous conditions: the cake being cooled and having frosting applied.
            This operator choice directly corresponds to the phrasing "A cake is ready to be served if it's cooled and the frosting is applied," which indicates a necessary and sufficient condition relationship.
            The logical conjunction ( ∧ ) connects "Cooled(cake)" and "FrostingApplied(cake)" to reflect the conjunction "and" in the natural language statement, showing that both conditions must be simultaneously true for the cake to be considered ready to serve. The predicates "Cooled" and "FrostingApplied" clearly encapsulate the conditions mentioned in the statement, identifying the specific states or actions required for the cake to be ready.
            """}
    ]
    messages_choice_2 = [
                {"role": "user", "content": f"""
                Here is a natural language statement: {nl} Here is its first order logic translation: {fol}
                Your task is to write a brief explanation to teach how to come up with the first order logic (FOL) statement when given the natural language (NL) statement. Be brief. Actually explain how or why the logic works, why those specific logical operators were chosen, how to identify what are the predicates and its arguments, etc.
                Explain the reasoning behind these choices, don't just state them. When explaining the reasoning, quote evidence for the reasoning directly from the natural language statement and quote words directly corresponding to choice of logical operators.
                REFERENCING THE NATURAL LANGUAGE STATEMENT WHEN EXPLAINING IS VERY VERY VERY IMPORTANT.
                Strictly follow the same format exactly as the example outputs. Provide the explanation in a similar way with references from the natural language statement.
                Only output the explanation, nothing else, no other comment or remarks, and no other headings. Follow the same subheadings as in the example outputs.
                3 EXAMPLES
                EXAMPLE INPUT 1
                NL: A coat provides warmth, an umbrella protects from rain, and sunglasses shield from sunlight.
                FOL: ∀x ∀y ∀z (Coat(x) → ProvidesWarmth(x)) ∧ (Umbrella(y) → ProtectsFromRain(y)) ∧ (Sunglasses(z) → ShieldsFromSunlight(z))
                EXAMPLE OUTPUT 1:
                Identify Key Entities and Relationships: The key entities are Coat, Umbrella, and Sunglasses, and the relationships are ProvidesWarmth (Coat), ProtectsFromRain (Umbrella), and ShieldsFromSunlight (Sunglasses). Use variables \( x \) for Coat, \( y \) for Umbrella, and \( z \) for Sunglasses.
                Logical Formulation Structure: ∀x ∀y ∀z (Coat(x) → ProvidesWarmth(x)) ∧ (Umbrella(y) → ProtectsFromRain(y)) ∧ (Sunglasses(z) → ShieldsFromSunlight(z))
                Explanation for Logical Formulation: The universal quantifiers \( \forall x \), \( \forall y \), and \( \forall z \) ensure the statement applies to all instances of coats, umbrellas, and sunglasses respectively. This captures the generality of the statement "A coat", "an umbrella", and "sunglasses" in the natural language statement. The predicates Coat(x), Umbrella(y), and Sunglasses(z) identify each item as belonging to their respective categories. The implications in the form (Coat(x) → ProvidesWarmth(x)), (Umbrella(y) → ProtectsFromRain(y)), and (Sunglasses(z) → ShieldsFromSunlight(z)) express the functional properties of each item as stated directly in the natural language: a coat "provides warmth", an umbrella "protects from rain", and sunglasses "shield from sunlight". Logical conjunctions (\( \land \)) connect these independent clauses, reflecting the structured listing of item functions in the natural language statement.
                EXAMPLE INPUT 2
                NL: Hospitals treat patients with medical professionals and appropriate equipment.
                FOL: ∀x∀y (Hospital(x) ∧ Patient(y) → ∃z∃w (MedicalProfessional(z) ∧ Equipment(w) ∧ TreatsWith(x, y, z, w)))
                EXAMPLE OUTPUT 2:
                Identify Key Entities and Relationships: The key entities in the natural language statement are "Hospitals", "patients", "medical professionals", and "equipment". The relationship expressed is "treats", involving hospitals, patients, medical professionals, and equipment. We use variables \( x \) for Hospitals, \( y \) for Patients, \( z \) for Medical Professionals, and \( w \) for Equipment.
                Logical Formulation Structure: \( \forall x \forall y (Hospital(x) \land Patient(y) \rightarrow \exists z \exists w (MedicalProfessional(z) \land Equipment(w) \land TreatsWith(x, y, z, w))) \)
                Explanation for Logical Formulation: The universal quantifiers \( \forall x \) and \( \forall y \) ensure the statement applies to all hospitals and all patients, reflecting the generality suggested by the phrase "Hospitals treat patients". The existential quantifiers \( \exists z \) and \( \exists w \) indicate there exists at least one medical professional and one piece of equipment involved in the treatment, aligning with the inclusion of "medical professionals and appropriate equipment". The predicates Hospital(x), Patient(y), MedicalProfessional(z), and Equipment(w) define the entities involved. The predicate TreatsWith(x, y, z, w) describes the treatment relationship, capturing the action "treat" specified in the natural language. Logical conjunctions (\( \land \)) connect the characteristics of each entity, and the implication (\( \rightarrow \)) in the formula represents the conditional nature of the treatment process stated as "Hospitals treat patients with medical professionals and appropriate equipment". This logical operator choice ensures that for each hospital and patient, if they are indeed a hospital and a patient, there must exist some medical professional and equipment that participate in the treatment process.
                EXAMPLE INPUT 3
                NL: A dessert is delicious if it's sweet but not overly sweet and has a pleasant texture.
                FOL: DeliciousDessert(x) ↔ (Sweet(x) ∧ ¬OverlySweet(x) ∧ PleasantTexture(x))
                EXAMPLE OUTPUT 3:
                Identify Key Entities and Relationships: The key entities are "dessert" and the qualitative attributes related to it: "sweet," "overly sweet," and "pleasant texture." The relationships captured are conditions that determine whether a dessert is considered delicious. The variable \( x \) represents a dessert.
                Logical Formulation Structure: DeliciousDessert(x) ↔ (Sweet(x) ∧ ¬OverlySweet(x) ∧ PleasantTexture(x))
                Explanation for Logical Formulation: The biconditional operator \( ↔ \) is used to express that a dessert being delicious is precisely equivalent to the conditions specified. The statement "A dessert is delicious if it's sweet but not overly sweet and has a pleasant texture" directly suggests this equivalence. The conjunction \( \land \) connects the predicates Sweet(x), ¬OverlySweet(x), and PleasantTexture(x), reflecting the conjunction "and" used in the natural language to cumulatively describe the conditions for a dessert being delicious. The predicate Sweet(x) directly maps to the word "sweet," ¬OverlySweet(x) (where ¬ represents negation) captures "not overly sweet," addressing the negation "not" used in the statement. Finally, PleasantTexture(x) corresponds to "has a pleasant texture," aligning directly with these words. The use of these logical operators and predicates accurately encodes the conditional and exclusionary nuances from the natural language description into the first order logic expression.
            """}
    ]

    # Randomly choose between the two message choices
    messages = random.choice([messages_choice_1, messages_choice_2])

    payload = {
        "model": "gpt-4o",
        "messages": messages
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    try:
        response = requests.post(OPENAI_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            generated_text = response_data['choices'][0]['message']['content'] if response_data.get('choices') else ""
            if generated_text.strip():  # Check if the response has content
                return generated_text
        else:
            time.sleep(2)
            return get_rationales(nl, fol)
    except requests.RequestException as e:
       raise e
    
train_data_path = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Train/MALLS-v0.1-train.json'
with open(train_data_path, 'r') as f:
    train_data = json.load(f)

sample_size = int(len(train_data) * 0.1)

existing_dataset_path = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Train/rationale_dataset.json'
with open(existing_dataset_path, 'r') as file:
    existing_data = json.load(file)
existing_nl_statements = {entry['NL'] for entry in existing_data}

selected_entries = []
while len(selected_entries) < sample_size:
    potential_entry = random.choice(train_data)
    if potential_entry['NL'] not in existing_nl_statements:
        selected_entries.append(potential_entry)
        existing_nl_statements.add(potential_entry['NL'])

rationale_dataset = '/Users/aliyanishfaq/Documents/GitHub/NL-FOL-distillation/Dataset/Train/rationale_dataset-gold.json'

# Open the file in append mode
results = []
import concurrent.futures

with open(rationale_dataset, 'a') as outfile:
    def process_entry(entry):
        nl = entry['NL']
        fol = entry['FOL']
        rationals = get_rationales(nl, fol)
        if rationals:
            result = {'NL': nl, 'FOL': fol, 'Rationals': rationals}
            json.dump(result, outfile, indent=4)
            if selected_entries.index(entry) != len(selected_entries) - 1:
                outfile.write(",\n")
            return result
        return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_entry, selected_entries))
        results = [result for result in results if result is not None]

print(results)
