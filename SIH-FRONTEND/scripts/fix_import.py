import re

with open("src/pages/finalplan/VoyageReceipt.tsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('import { useApproval } from "../../contexts/ApprovalContext";', 'import { useApproval } from "../../contexts/ApprovalContext";\nimport { useAuth } from "../../contexts/AuthContext";')

with open("src/pages/finalplan/VoyageReceipt.tsx", "w", encoding="utf-8") as f:
    f.write(text)
