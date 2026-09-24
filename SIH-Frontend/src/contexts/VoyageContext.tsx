import { createContext, useContext, useState, type ReactNode } from 'react';

export interface VoyageRequirements {
  origin: string;
  destination: string;
  commodity: string;
  cargoMt: number | '';
  deliveryDate: string;
  contract: string;
  laycan: string;
  noOfVoyages: number | '';
}

interface VoyageContextType {
  requirements: VoyageRequirements | null;
  setRequirements: (reqs: VoyageRequirements) => void;
  completedSteps: string[];
  markStepComplete: (stepPath: string) => void;
}

const VoyageContext = createContext<VoyageContextType | undefined>(undefined);

export function VoyageProvider({ children }: { children: ReactNode }) {
  const [requirements, setRequirements] = useState<VoyageRequirements | null>(null);
  const [completedSteps, setCompletedSteps] = useState<string[]>(['/voyage-requirement-input']);

  const markStepComplete = (stepPath: string) => {
    setCompletedSteps((prev) => {
      if (!prev.includes(stepPath)) {
        return [...prev, stepPath];
      }
      return prev;
    });
  };

  return (
    <VoyageContext.Provider value={{ requirements, setRequirements, completedSteps, markStepComplete }}>
      {children}
    </VoyageContext.Provider>
  );
}

export function useVoyage() {
  const context = useContext(VoyageContext);
  if (context === undefined) {
    throw new Error('useVoyage must be used within a VoyageProvider');
  }
  return context;
}
