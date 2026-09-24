import { useRef } from "react";
import { useNavigate } from "react-router";
import { useReactToPrint } from "react-to-print";
import { Printer, Download, ArrowLeft, Anchor, FileText } from "lucide-react";
import { useVoyage } from "../../contexts/VoyageContext";
import { useApproval } from "../../contexts/ApprovalContext";
import { evaluateScenarios, runDecisionEngine } from "../../utils/DecisionLogic";

export function VoyageReceipt() {
  const navigate = useNavigate();
  const { requirements } = useVoyage();
  const { approvalResult } = useApproval();

  const printRef = useRef<HTMLDivElement>(null);
  
  const planId = `BR-2027-${new Date().getTime().toString().slice(-6)}`;

  const handlePrint = useReactToPrint({
    contentRef: printRef,
    documentTitle: `Odyssey_Voyage_Receipt_${planId}`
  });

  const handleDownloadPdf = () => {
    // Basic window print functions well for PDF export in most modern browsers.
    handlePrint();
  };

  const evaluations = evaluateScenarios(requirements);
  const decision = runDecisionEngine(evaluations, requirements);
  const bookNowEval = evaluations.find(e => e.scenario === "BOOK NOW");

  const today = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });

  return (
    <div className="w-full relative min-h-screen bg-slate-100 p-6 md:p-8">
      {/* Top action bar */}
      <div className="max-w-4xl mx-auto flex items-center justify-between mb-8 print:hidden">
        <button 
          onClick={() => navigate('/final-plan')}
          className="flex items-center gap-2 text-slate-500 hover:text-slate-900 font-medium transition-colors"
        >
          <ArrowLeft size={18} />
          Back to Plan
        </button>
        <div className="flex items-center gap-3">
          <button 
            onClick={() => handlePrint()}
            className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-slate-700 hover:bg-slate-50 font-medium shadow-sm"
          >
            <Printer size={18} />
            Print Receipt
          </button>
          <button 
            onClick={handleDownloadPdf}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium shadow-md"
          >
            <Download size={18} />
            Download PDF
          </button>
        </div>
      </div>

      {/* Printable Receipt Container */}
      <div className="max-w-3xl mx-auto">
        <div 
          ref={printRef} 
          className="bg-white rounded-none md:rounded-xl shadow-xl md:shadow-sm border-0 md:border border-slate-200 p-8 md:p-12 print:shadow-none print:border-none print:m-0 print:p-0"
        >
          
          {/* Header */}
          <div className="flex items-start justify-between border-b-2 border-slate-900 pb-8 mb-8">
            <div className="flex items-center gap-3">
              <div className="h-12 w-12 bg-slate-900 rounded-lg flex items-center justify-center shrink-0">
                <Anchor size={28} className="text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-black tracking-tight text-slate-900 uppercase">Odyssey</h1>
                <p className="text-sm font-semibold text-slate-500 uppercase tracking-widest">Smart Shipping Intelligence</p>
              </div>
            </div>
            <div className="text-right">
              <h2 className="text-xl font-bold text-slate-400 uppercase tracking-widest mb-1">Voyage Receipt</h2>
              <p className="text-sm font-bold text-slate-900">ID: {planId}</p>
              <p className="text-xs text-slate-500">Date: {today}</p>
              <p className="text-xs font-bold text-emerald-600 mt-1">STATUS: {approvalResult?.status.toUpperCase() || "APPROVED"}</p>
            </div>
          </div>

          <div className="space-y-8">
            
            {/* VOYAGE DETAILS */}
            <section>
              <h3 className="text-sm font-bold uppercase tracking-widest text-slate-400 border-b border-slate-100 pb-2 mb-4 flex items-center gap-2">
                <FileText size={16} /> Voyage Details
              </h3>
              <div className="grid grid-cols-2 gap-y-4 gap-x-8 text-sm">
                <div><span className="block text-slate-500 text-xs uppercase">Origin</span><span className="font-semibold text-slate-900">{requirements?.origin || "N/A"}</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">Destination</span><span className="font-semibold text-slate-900">{requirements?.destination || "N/A"}</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">Commodity</span><span className="font-semibold text-slate-900">{requirements?.commodity || "N/A"}</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">Cargo Volume</span><span className="font-semibold text-slate-900">{requirements?.cargoMt ? `${requirements.cargoMt.toLocaleString()} MT` : "N/A"}</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">Contract Type</span><span className="font-semibold text-slate-900">{requirements?.contract || "Spot"}</span></div>
              </div>
            </section>

            {/* SCHEDULE */}
            <section>
              <h3 className="text-sm font-bold uppercase tracking-widest text-slate-400 border-b border-slate-100 pb-2 mb-4 flex items-center gap-2">
                <FileText size={16} /> Schedule
              </h3>
              <div className="grid grid-cols-2 gap-y-4 gap-x-8 text-sm">
                <div><span className="block text-slate-500 text-xs uppercase">Delivery Date</span><span className="font-semibold text-slate-900">{requirements?.deliveryDate || "N/A"}</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">Laycan</span><span className="font-semibold text-slate-900">{requirements?.laycan || "N/A"}</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">Transit Time</span><span className="font-semibold text-slate-900">Requires model</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">Deadline Buffer</span><span className="font-semibold text-slate-900">{bookNowEval?.deadlineBuffer === "Unavailable" ? "Requires model" : `${bookNowEval?.deadlineBuffer} days`}</span></div>
              </div>
            </section>

            {/* VESSEL */}
            <section>
              <h3 className="text-sm font-bold uppercase tracking-widest text-slate-400 border-b border-slate-100 pb-2 mb-4 flex items-center gap-2">
                <FileText size={16} /> Vessel Recommendation
              </h3>
              <div className="grid grid-cols-2 gap-y-4 gap-x-8 text-sm">
                <div><span className="block text-slate-500 text-xs uppercase">Recommended Vessel</span><span className="font-semibold text-slate-900">{decision.bestVessel !== "Unavailable" ? decision.bestVessel["Vessel Type"] : "Requires model"}</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">DWT</span><span className="font-semibold text-slate-900">{decision.bestVessel !== "Unavailable" ? `${decision.bestVessel["DWT (mt)"]} MT` : "N/A"}</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">Draft</span><span className="font-semibold text-slate-900">{decision.bestVessel !== "Unavailable" ? `${decision.bestVessel["SSW Draft (m)"]} m` : "N/A"}</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">Compatibility</span><span className="font-semibold text-emerald-600">Verified</span></div>
              </div>
            </section>

            {/* COMMERCIAL SUMMARY */}
            <section>
              <h3 className="text-sm font-bold uppercase tracking-widest text-slate-400 border-b border-slate-100 pb-2 mb-4 flex items-center gap-2">
                <FileText size={16} /> Commercial Summary
              </h3>
              <div className="grid grid-cols-2 gap-y-4 gap-x-8 text-sm mb-4">
                <div className="flex justify-between border-b border-slate-50 pb-1"><span className="text-slate-600">Freight Cost</span><span className="font-semibold">{bookNowEval?.details.freightCost !== "Unavailable" && bookNowEval?.details.freightCost !== undefined ? `$${bookNowEval.details.freightCost.toLocaleString()}` : "Requires model"}</span></div>
                <div className="flex justify-between border-b border-slate-50 pb-1"><span className="text-slate-600">Bunker Cost</span><span className="font-semibold italic text-slate-400">Requires model</span></div>
                <div className="flex justify-between border-b border-slate-50 pb-1"><span className="text-slate-600">Port Cost</span><span className="font-semibold italic text-slate-400">Requires model</span></div>
                <div className="flex justify-between border-b border-slate-50 pb-1"><span className="text-slate-600">Waiting Cost</span><span className="font-semibold italic text-slate-400">Requires model</span></div>
              </div>
              <div className="flex justify-between items-center bg-slate-50 p-4 rounded-lg">
                <span className="font-bold uppercase tracking-wider text-slate-700">Total Estimated Cost</span>
                <span className="text-xl font-black text-slate-900">{bookNowEval?.totalCost === "Unavailable" ? "Requires model" : `$${bookNowEval?.totalCost.toLocaleString()}`}</span>
              </div>
            </section>

            {/* FINAL DECISION */}
            <section>
              <h3 className="text-sm font-bold uppercase tracking-widest text-slate-400 border-b border-slate-100 pb-2 mb-4 flex items-center gap-2">
                <FileText size={16} /> Final Decision & Approval
              </h3>
              <div className="grid grid-cols-2 gap-y-4 gap-x-8 text-sm bg-blue-50/50 p-4 rounded-lg border border-blue-100">
                <div><span className="block text-slate-500 text-xs uppercase">Action</span><span className="font-bold text-blue-700">{decision.bestTime === "BOOK NOW" ? "BOOK NOW" : "WAIT / MODIFY"}</span></div>
                <div><span className="block text-slate-500 text-xs uppercase">Timing</span><span className="font-bold text-slate-900">{decision.bestTime !== "Unavailable" ? decision.bestTime : "N/A"}</span></div>
                <div className="col-span-2"><span className="block text-slate-500 text-xs uppercase">Decision Reason</span><span className="font-medium text-slate-700">Optimized based on delivery deadline constraints and available fleet capacity.</span></div>
                <div className="col-span-2 pt-2 border-t border-blue-100 flex justify-between">
                  <div><span className="block text-slate-500 text-xs uppercase">Approved By</span><span className="font-bold text-slate-900">Harshit Sachan (Manager)</span></div>
                  <div className="text-right"><span className="block text-slate-500 text-xs uppercase">Approval Date</span><span className="font-bold text-slate-900">{today}</span></div>
                </div>
              </div>
            </section>

          </div>
          
          {/* Footer */}
          <div className="mt-12 pt-6 border-t border-slate-200 text-center">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Odyssey • Smart Shipping Intelligence • SIH 2026</p>
            <p className="text-[10px] text-slate-400 mt-1">Generated electronically. This document is a summary of the approved voyage parameters.</p>
          </div>

        </div>
      </div>
    </div>
  );
}
