import re

with open("src/pages/approval/HumanApproval.tsx", "r", encoding="utf-8") as f:
    text = f.read()

reqSeed_line = """export function HumanApproval() {
  const { requirements, markStepComplete } = useVoyage();
  const reqSeed = `${requirements?.origin}-${requirements?.destination}-${requirements?.cargoMt}`;"""

text = text.replace('export function HumanApproval() {\n  const { requirements, markStepComplete } = useVoyage();', reqSeed_line)

with open("src/pages/approval/HumanApproval.tsx", "w", encoding="utf-8") as f:
    f.write(text)
