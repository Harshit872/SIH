import { createContext, useContext, useState, type ReactNode } from 'react';
import type { ScenarioType, FinalRecommendationType } from '../utils/DecisionLogic';

// The final decision — either the system's or the human's modified version
export interface FinalDecision {
  bestTime: ScenarioType | "Unavailable";
  bestVessel: any | "Unavailable";   // actual dataset record or "Unavailable"
  bestPort: any | "Unavailable";     // actual dataset record or "Unavailable"
  recommendation: FinalRecommendationType;
}

export interface HumanApprovalResult {
  status: "approved" | "modified";
  approvedAt: string;                     // ISO timestamp
  originalRecommendation: FinalRecommendationType;
  finalDecision: FinalDecision;
}

interface ApprovalContextType {
  approvalResult: HumanApprovalResult | null;
  setApprovalResult: (result: HumanApprovalResult) => void;
  clearApproval: () => void;
}

const ApprovalContext = createContext<ApprovalContextType | undefined>(undefined);

export function ApprovalProvider({ children }: { children: ReactNode }) {
  const [approvalResult, setApprovalResult] = useState<HumanApprovalResult | null>(null);

  function clearApproval() {
    setApprovalResult(null);
  }

  return (
    <ApprovalContext.Provider value={{ approvalResult, setApprovalResult, clearApproval }}>
      {children}
    </ApprovalContext.Provider>
  );
}

export function useApproval() {
  const context = useContext(ApprovalContext);
  if (context === undefined) {
    throw new Error('useApproval must be used within an ApprovalProvider');
  }
  return context;
}
