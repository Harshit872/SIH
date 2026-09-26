import os
import re

path = 'SIH-FRONTEND/src/pages/voyage/VoyageRequirementInput.tsx'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace PORT_OPTIONS with ORIGIN and DESTINATION options
text = re.sub(
    r'const PORT_OPTIONS = .*?;\s+',
    '''const ORIGIN_OPTIONS = [
  { value: "Port Hedland", label: "Port Hedland" },
  { value: "Gladstone", label: "Gladstone" },
  { value: "Newcastle", label: "Newcastle" },
  { value: "Hay Point", label: "Hay Point" },
  { value: "Dalrymple Bay", label: "Dalrymple Bay" },
  { value: "Richards Bay", label: "Richards Bay" },
];

const DESTINATION_OPTIONS = [
  { value: "Dhamra", label: "Dhamra" },
  { value: "Paradip", label: "Paradip" },
  { value: "Haldia", label: "Haldia" },
  { value: "Visakhapatnam", label: "Visakhapatnam" },
];

''', text, flags=re.DOTALL)

text = re.sub(
    r'const COMMODITY_OPTIONS = .*?;\s+',
    '''const COMMODITY_OPTIONS = [
  { value: "Iron Ore", label: "Iron Ore" },
  { value: "Coal", label: "Coal" },
  { value: "Coking Coal", label: "Coking Coal" },
  { value: "Thermal Coal", label: "Thermal Coal" },
];

''', text, flags=re.DOTALL)

# Now fix the SearchableSelect props
text = text.replace('options={PORT_OPTIONS}', 'options={ORIGIN_OPTIONS}', 1) # first is origin
text = text.replace('options={PORT_OPTIONS}', 'options={DESTINATION_OPTIONS}', 1) # second is dest

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

