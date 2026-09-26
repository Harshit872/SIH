import os

new_workspace = '''import { useState, useEffect } from "react";
import { useNavigate } from "react-router";
import { useVoyage } from "../../contexts/VoyageContext";
import { GitBranch, Navigation, CheckCircle2, XCircle, AlertCircle, TrendingUp, Ship, FileText } from "lucide-react";
import { Button } from "../../components/ui/button";

export function DecisionWorkspace() {
  const { requirements } = useVoyage();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [feasibility, setFeasibility] = useState<any>(null);
  const [freight, setFreight] = useState<any>(null);
  const [cost, setCost] = useState<any>(null);
  const [deadline, setDeadline] = useState<any>(null);
  const [risk, setRisk] = useState<any>(null);
  const [whatif, setWhatif] = useState<any>(null);

  useEffect(() => {
    if (!requirements) return;
    
    async function fetchData() {
      try {
        const basePayload = {
          origin_port: requirements?.origin || "Gladstone",
          destination_port: requirements?.destination || "Paradip",
          cargo_type: requirements?.commodity || "Coal",
          quantity_mt: Number(requirements?.cargoMt) || 75000,
          route_distance_nm: 6300,
          bunker_price_usd_per_mt: 850,
          bdi_value: 1500,
          port_turnaround_days: 4.5,
          demurrage_rate: 20000,
          laycan_start_date: requirements?.laycan ? requirements.laycan.split(" - ")[0] : "2026-10-01",
          required_delivery_date: requirements?.deliveryDate || "2026-10-25"
        };
        
        // 1. Feasibility
        const fRes = await fetch("http://localhost:8000/api/v1/vessel-feasibility", {
          method: "POST", headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            cargo_quantity_mt: basePayload.quantity_mt,
            origin_port: basePayload.origin_port,
            destination_port: basePayload.destination_port
          })
        });
        const fData = await fRes.json();
        setFeasibility(fData);
        
        let vessel = "Panamax";
        if (fData.vessels && fData.vessels.length > 0) {
            const feasible = fData.vessels.find((v: any) => v.feasible);
            if (feasible) vessel = feasible.vessel_class;
            else if (fData.nearest_feasible_option) vessel = fData.nearest_feasible_option.vessel_class;
        }
        basePayload.vessel_class = vessel;

        // 2. Freight Rate
        const frRes = await fetch("http://localhost:8000/api/v1/forecast/freight-rate", {
          method: "POST", headers: {"Content-Type": "application/json"},
          body: JSON.stringify(basePayload)
        });
        const frData = await frRes.json();
        setFreight(frData);

        // 3. Voyage Cost
        const vcRes = await fetch("http://localhost:8000/api/v1/voyage-cost", {
          method: "POST", headers: {"Content-Type": "application/json"},
          body: JSON.stringify({...basePayload, freight_rate_usd_per_mt: frData.predicted_freight_rate_usd_per_mt})
        });
        const vcData = await vcRes.json();
        setCost(vcData);

        // 4. Deadline
        const dlRes = await fetch("http://localhost:8000/api/v1/deadline-check", {
          method: "POST", headers: {"Content-Type": "application/json"},
          body: JSON.stringify({...basePayload, vessel_speed_knots: 13.5})
        });
        const dlData = await dlRes.json();
        setDeadline(dlData);

        // 5. Risk Score
        const rsRes = await fetch("http://localhost:8000/api/v1/risk-score", {
          method: "POST", headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            freight_rate_confidence_flag: frData.confidence_flag,
            deadline_buffer_days: dlData.buffer_days,
            port_cost_source: vcData.port_cost_source,
            vessel_feasibility_mode: fData.nearest_feasible_option ? fData.nearest_feasible_option.mode : "direct_feasible"
          })
        });
        const rsData = await rsRes.json();
        setRisk(rsData);

        // 6. What-If
        const wiRes = await fetch("http://localhost:8000/api/v1/what-if", {
          method: "POST", headers: {"Content-Type": "application/json"},
          body: JSON.stringify(basePayload)
        });
        const wiData = await wiRes.json();
        setWhatif(wiData);

      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    
    fetchData();
  }, [requirements]);

  if (loading) return <div className="p-10 text-center text-xl">Running AI Engines...</div>;

  return (
    <div className="w-full relative flex flex-col min-h-full">
      <main className="flex-1 w-full max-w-7xl mx-auto p-6 space-y-6">
        
        <div className="bg-white border rounded-xl p-6 shadow-sm">
           <h3 className="text-xl font-bold mb-4 text-blue-800">1. Vessel Feasibility Engine</h3>
           <div className="grid grid-cols-2 gap-4 text-sm">
             <div>
               <p className="font-bold border-b pb-2 mb-2">Ranked Options:</p>
               {feasibility?.vessels?.map((v: any) => (
                 <div key={v.vessel_class} className="flex justify-between py-1 border-b border-slate-50 last:border-0">
                   <span className="font-medium">{v.vessel_class}</span>
                   <span className={v.feasible ? "text-green-600" : "text-red-500"}>{v.feasible ? "Feasible" : v.reason}</span>
                 </div>
               ))}
             </div>
             {feasibility?.nearest_feasible_option && (
               <div className="bg-orange-50 text-orange-800 p-4 rounded-lg flex flex-col justify-center border border-orange-100">
                 <strong className="text-lg">Fallback Triggered</strong>
                 <p className="mt-1">{feasibility.nearest_feasible_option.note}</p>
                 <span className="mt-2 inline-block bg-orange-200 px-2 py-1 rounded text-xs w-max font-bold uppercase">Mode: {feasibility.nearest_feasible_option.mode}</span>
               </div>
             )}
           </div>
        </div>

        <div className="bg-white border rounded-xl p-6 shadow-sm">
           <h3 className="text-xl font-bold mb-4 text-blue-800">2. ML Freight Rate Engine</h3>
           <p className="text-4xl font-bold text-slate-800">${freight?.predicted_freight_rate_usd_per_mt?.toFixed(2)} <span className="text-lg font-normal text-slate-500">/ MT</span></p>
           <div className="flex gap-2 mt-3">
             <span className="bg-slate-100 px-3 py-1 rounded text-xs font-medium">Model: {freight?.model_version}</span> 
             <span className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded text-xs font-medium" title="Transparency Disclosure">Synthetic Data Used: {freight?.is_model_trained_on_synthetic_data ? "Yes" : "No"}</span>
             <span className={`px-3 py-1 rounded text-xs font-medium ${freight?.confidence_flag === 'normal' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`} title="Confidence Flag">Confidence: {freight?.confidence_flag}</span>
           </div>
        </div>

        <div className="bg-white border rounded-xl p-6 shadow-sm">
           <h3 className="text-xl font-bold mb-4 text-blue-800">3. Voyage Cost Engine</h3>
           <ul className="text-sm space-y-3 mb-4 bg-slate-50 p-4 rounded-lg">
             <li className="flex justify-between"><span>Freight Cost:</span> <strong className="text-slate-700">${cost?.freight_cost_usd?.toLocaleString(undefined, {maximumFractionDigits:0})}</strong></li>
             <li className="flex justify-between"><span>Bunker Cost:</span> <strong className="text-slate-700">${cost?.bunker_cost_usd?.toLocaleString(undefined, {maximumFractionDigits:0})}</strong></li>
             <li className="flex justify-between"><span>Port Cost:</span> <strong className="text-slate-700">${cost?.port_cost_usd?.toLocaleString(undefined, {maximumFractionDigits:0})}</strong></li>
             <li className="flex justify-between border-t border-slate-200 pt-3 text-lg mt-2"><span>Total Cost:</span> <strong className="text-slate-900">${cost?.total_cost_usd?.toLocaleString(undefined, {maximumFractionDigits:0})}</strong></li>
           </ul>
           <p className="text-xs bg-amber-50 text-amber-800 border border-amber-200 p-2 rounded inline-block" title="Port Cost Source"><strong>Port Cost Source:</strong> {cost?.port_cost_source}</p>
        </div>

        <div className="bg-white border rounded-xl p-6 shadow-sm">
           <h3 className="text-xl font-bold mb-4 text-blue-800">4. Deadline Validator</h3>
           <p className="text-lg">Estimated Arrival: <strong className="text-slate-800">{deadline?.estimated_arrival_date}</strong></p>
           <p className={`text-sm font-medium mt-1 ${deadline?.feasible ? 'text-green-600' : 'text-red-600'}`}>
             Feasible: {deadline?.feasible ? 'Yes' : 'No'} (Buffer: {deadline?.buffer_days} days)
           </p>
        </div>

        <div className="bg-white border rounded-xl p-6 shadow-sm">
           <h3 className="text-xl font-bold mb-4 text-blue-800">5. Risk Scoring Engine</h3>
           <p className="text-2xl font-bold mb-4">Tier: <span className={risk?.risk_tier === 'Low' ? 'text-green-600' : risk?.risk_tier === 'Medium' ? 'text-yellow-600' : 'text-red-600'}>{risk?.risk_tier}</span> <span className="text-slate-400 text-lg ml-2">(Score: {risk?.risk_score})</span></p>
           <div className="space-y-2 text-sm">
             {risk?.breakdown?.map((b: any, idx: number) => (
                <div key={idx} className="flex gap-4 p-3 bg-red-50 text-red-900 rounded-lg border border-red-100 items-center">
                  <span className="font-bold bg-red-200 px-2 py-1 rounded">+{b.points}</span>
                  <span>{b.description}</span>
                </div>
             ))}
             {risk?.breakdown?.length === 0 && <p className="text-slate-500 bg-slate-50 p-3 rounded-lg border">No risk factors triggered.</p>}
           </div>
        </div>

        <div className="bg-white border rounded-xl p-6 shadow-sm">
           <h3 className="text-xl font-bold mb-4 text-blue-800">6. What-If Decision Engine</h3>
           <div className="mb-6 bg-blue-50 text-blue-900 border border-blue-200 p-4 rounded-lg" title="Recommendation Basis">
             <strong className="text-lg flex items-center gap-2"><CheckCircle2 size={20}/> Recommendation: {whatif?.recommended_scenario}</strong>
             <p className="mt-1 text-sm text-blue-700">Basis: {whatif?.recommendation_basis}</p>
           </div>
           <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
             {whatif?.scenarios?.map((s: any) => (
                <div key={s.scenario_name} className={`p-5 rounded-xl border-2 ${s.scenario_name === whatif?.recommended_scenario ? 'border-blue-500 bg-white shadow-md relative' : 'border-slate-200 bg-slate-50'}`}>
                  {s.scenario_name === whatif?.recommended_scenario && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Recommended</div>
                  )}
                  <h4 className="font-bold text-lg mb-4 text-center">{s.scenario_name}</h4>
                  <div className="space-y-2">
                    <p className="text-sm flex justify-between"><span className="text-slate-500">Cost:</span> <strong>${s.total_cost_usd?.toLocaleString(undefined, {maximumFractionDigits:0})}</strong></p>
                    <p className={`text-sm flex justify-between`}><span className="text-slate-500">Feasible:</span> <strong className={s.deadline_feasible ? 'text-green-600' : 'text-red-600'}>{s.deadline_feasible ? 'Yes' : 'No'}</strong></p>
                    <p className="text-sm flex justify-between"><span className="text-slate-500">Risk Tier:</span> <strong>{s.risk_tier} ({s.risk_score})</strong></p>
                    <p className="text-sm flex justify-between border-t pt-2 mt-2"><span className="text-slate-500">Arrives:</span> <strong>{s.estimated_arrival_date}</strong></p>
                  </div>
                </div>
             ))}
           </div>
        </div>

      </main>
    </div>
  );
}
'''
with open("SIH-FRONTEND/src/pages/decision/DecisionWorkspace.tsx", "w", encoding='utf-8') as f:
    f.write(new_workspace)
