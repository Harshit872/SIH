import { BrowserRouter, Routes, Route, Navigate } from "react-router";
import { FoundationCheck } from "./pages/FoundationCheck";
import { AuthLayout } from "./layouts/AuthLayout";
import { MainLayout } from "./layouts/MainLayout";
import { Login } from "./pages/auth/Login";
import { Signup } from "./pages/auth/Signup";
import { VoyageRequirementInput } from "./pages/voyage/VoyageRequirementInput";
import { FreightForecasting } from "./pages/forecasting/FreightForecasting";
import { DecisionWorkspace } from "./pages/decision/DecisionWorkspace";
import { FinalRecommendation } from "./pages/recommendation/FinalRecommendation";
import { HumanApproval } from "./pages/approval/HumanApproval";
import { FinalPlan } from "./pages/finalplan/FinalPlan";
import { VoyageReceipt } from "./pages/finalplan/VoyageReceipt";
import { Settings } from "./pages/settings/Settings";
import { VoyageProvider } from "./contexts/VoyageContext";
import { ApprovalProvider } from "./contexts/ApprovalContext";

function App() {
  return (
    <VoyageProvider>
      <ApprovalProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />

            <Route element={<AuthLayout />}>
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
            </Route>

            <Route element={<MainLayout />}>
              <Route path="/voyage-requirement-input" element={<VoyageRequirementInput />} />
              <Route path="/freight-forecasting"      element={<FreightForecasting />} />
              <Route path="/decision-workspace"       element={<DecisionWorkspace />} />
              <Route path="/final-recommendation"     element={<FinalRecommendation />} />
              <Route path="/human-approval"           element={<HumanApproval />} />
              <Route path="/final-plan"               element={<FinalPlan />} />
              <Route path="/voyage-receipt"           element={<VoyageReceipt />} />
              <Route path="/settings"                 element={<Settings />} />
            </Route>

            <Route path="/foundation-check" element={<FoundationCheck />} />
          </Routes>
        </BrowserRouter>
      </ApprovalProvider>
    </VoyageProvider>
  );
}

export default App;
