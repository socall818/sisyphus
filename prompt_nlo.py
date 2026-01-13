from langchain.prompts import ChatPromptTemplate

simple_prompt_template_no_syn = ChatPromptTemplate.from_messages([
    ('user',"""
You are required to extract material information from text provided below and output desired format which generally a list of dictionaries, and for each includes metadata and property information. Return empty list if no property found. Specifically, the metadata has structure as follows:
metadata: {{
    "composition": "%s",
    }}
e.g., metadata: {{
    "composition": "NH4B4O6F",
    }}
Specifically for composition:
### **Composition Format:**.
    - Due to the phenomenon of homogeneous polycrystals (with the same chemical composition but different crystal structures) in some crystal materials, use prefix to indicate different crystal structures **if there are at least two crystal materials with the same chemical formula/abbreviation explicitly mentioned in the text**.
        - Example: `α-BaHgSnS4`, `β-BaHgSnS4`, `P1-Sr2[B5O8(OH)]2·[B(OH)3]·H2O`, `Pna21-Ba3Mg3(BO3)3F3`
        - Note: sometimes these crystal variants with the same chemical composition but different structures will indicate their crystal forms in parentheses, such as Sr3B14O24 (P21/c). Please record them in the form of P21/c-Sr3B14O24.  

For property specific instruction: 
{property_instruction}

Property section:
{property}
""")
]
)

nlo_coefficient_instruction = """Extract nonlinear optical property relevant to dij, deff from the text

Follow these rules:
- For dij and deff, the more specific the data, the higher the priority. For example, d33=4-9 pm V-1 has higher priority than dij=4–9 pm V-1, also d33=10 pm V-1 has higher priority than d33=4–9 pm V-1.
- For dij, if tested under different fundamental light of frequencies (such as @1064nm, @1950nm), only 1064nm needs to be extracted, ignore other frequencies. If there is no provided corresponding test wavelength for dij, just extract dij directly.
- For deff(not dij!!!), if tested under different fundamental light of frequencies (such as @1064nm, @1950nm), extract deff and test wavelength **in a one-to-one correspondence manner, do not confuse the order**. If a deff has no provided corresponding test wavelength, the wavelength extraction result will be 'Null', but don't affect the corresponding sequence relationship between deff and test wavelength!
- Only collect second-order nonlinear susceptibility tensor(dij) and effective nonlinear optical coefficient(deff)
- Prioritize experimental values over calculated values if there is a conflict.
- Prioritize table values over text if there is a conflict. 
- If the value provided is a range, for example, "from 4 pm V-1 to 9 pm V-1", extract it as "4-9 pm V-1".
- If the value is given as "greater than" or "less than", for example, "greater than 4 pm V-1", extract it as ">4 pm V-1".
- If the value is given as "approximately" or "around", for example, "approximately 9 pm v-1", extract it as "≈9 pm V-1".
- Otherwise, extract the value as it is."""

cutoffedge_instruction = """Extract the cutoff/absorption edge wavelength information with unit(nm) from the provided text. Do not record any other type of wavelength information (shortest phase-matching second harmonic wavelength (λSH),etc.).

Follow these rules:
- Prioritize experimental values over calculated values if there is a conflict.
- The more specific the data, the higher the priority. For example, 156 nm has higher priority than "<160 nm" or "~156 nm"
- If the value provided is a narrow range, extract with range e.g., "156-158 nm".
- If the value provided is a broad range, extract the smaller value e.g., "in the range of 260-800 nm" extract as "260 nm".
- If the value is given as "greater than" or "less than", for example, "greater than 140 nm", extract it as ">140 nm".
- If the value is given as "approximately" or "around", for example, "approximately 120 nm", extract it as "~120 nm".
- Otherwise, extract the value as it is.
"""

