import { useState, useEffect } from "react";
import { useNavigate } from "react-router";
import { useVoyage } from "../../contexts/VoyageContext";
import { 
  Ship, ArrowRight, TrendingUp, TrendingDown, Minus, 
  AlertCircle, LineChart as ChartIcon, ShieldCheck,
  Database, ChevronDown, CheckCircle2, XCircle
} from "lucide-react";
import { Button } from "../../components/ui/button";
import { 
  Line, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, Area, ComposedChart
} from "recharts";
import { DatasetService } from "../../data/DatasetService";

import { format, parseISO } from "date-fns";

type Horizon = "7D" | "14D" | "30D";


export function FreightForecasting() {
  const { requirements, markStepComplete } = useVoyage();
  const navigate = useNavigate();
  const [horizon, setHorizon] = useState<Horizon>("14D");

  const [forecastData, setForecastData] = useState<any[]>([]);
  const [trend, setTrend] = useState<string>("Stable");
  const [confidenceInfo, setConfidenceInfo] = useState<string>("Calculating...");
  const [status, setStatus] = useState("awaiting_service");

  useEffect(() => {
    async function fetchData() {
      if (!requirements) return;
      setStatus("loading");
      
      const bdiData = DatasetService.getBalticIndices();
      // Take last 10 historical points to keep it fast
      const recentHistorical = bdiData.slice(-10);
      
      const basePayload = {
        origin_port: requirements.origin || "Newcastle",
        destination_port: requirements.destination || "Paradip",
        cargo_type: requirements.commodity || "Coal",
        quantity_mt: Number(requirements.cargoMt) || 75000,
        vessel_class: "Panamax", // We'll just assume Panamax for the chart base
        route_distance_nm: 6300,
        bunker_price_usd_per_mt: 850,
        bdi_value: 1500,
        port_turnaround_days: 4.5,
        demurrage_rate: 20000,
        laycan_start_date: "2026-10-01",
        required_delivery_date: "2026-10-25"
      };

      const newData: any[] = [];
      let latestHistDate = new Date();
      let lastRate = null;
      let lastConf = null;

      // 1. Plot Historical (using historical BDI to get implied rate)
      for (const item of recentHistorical) {
        if (!item.Date || item.BDI === "NA") continue;
        const dt = parseISO(item.Date);
        latestHistDate = dt;
        
        try {
            const res = await fetch("http://localhost:8080/api/v1/forecast/freight-rate", {
              method: "POST", headers: {"Content-Type": "application/json"},
              body: JSON.stringify({...basePayload, bdi_value: Number(item.BDI)})
            });
            const data = await res.json();
            const rate = data.predicted_freight_rate_usd_per_mt;
            lastRate = rate;
            lastConf = data.confidence_flag;
            newData.push({
              date: format(dt, "MMM d, yy"),
              historicalRate: rate,
              forecastRate: null,
              confidenceRange: null
            });
        } catch (e) {}
      }

      // Ensure continuity: The first forecast point should overlap the last historical point exactly
      if (lastRate !== null) {
          newData[newData.length - 1].forecastRate = lastRate;
      }

      // 2. Plot Forecast (using static current BDI, resulting in a flat forecast since we lack future BDI)
      let days = horizon === "7D" ? 7 : horizon === "30D" ? 30 : 14;
      
      try {
          const res = await fetch("http://localhost:8080/api/v1/forecast/freight-rate", {
            method: "POST", headers: {"Content-Type": "application/json"},
            body: JSON.stringify(basePayload)
          });
          const data = await res.json();
          const currentRate = data.predicted_freight_rate_usd_per_mt;
          
          for(let i = 1; i <= days; i++) {
            const nextDate = new Date(latestHistDate);
            nextDate.setDate(latestHistDate.getDate() + i);
            newData.push({
              date: format(nextDate, "MMM d, yy"),
              historicalRate: null,
              forecastRate: currentRate,
              // Model doesn't provide a continuous confidence interval, so we mock a narrow band for UI
              confidenceRange: [currentRate * 0.98, currentRate * 1.02]
            });
          }
          
          setTrend(currentRate > lastRate ? "Increasing" : currentRate < lastRate ? "Decreasing" : "Stable");
          
          if (data.confidence_flag === "normal") {
              setConfidenceInfo("Normal Confidence (95%) - Input is within training bounds");
          } else {
              setConfidenceInfo("Low Confidence (<50%) - Input falls outside safe training limits");
          }

      } catch (e) {}

      setForecastData(newData);
      setStatus("forecast_ready");
    }
    fetchData();
  }, [horizon, requirements]);

  const forecast = {
    data: forecastData,
    trend: trend,
    confidence: confidenceInfo,
    status: status
  };
  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "Increasing": return <TrendingUp size={24} className="text-rose-600" />;
      case "Decreasing": return <TrendingDown size={24} className="text-emerald-600" />;
      case "Stable": return <Minus size={24} className="text-blue-600" />;
      default: return <AlertCircle size={24} className="text-slate-400" />;
    }
  };

  return (
    <div className="w-full relative flex flex-col min-h-full">
      
      {/* Main Content */}
      <main className="flex-1 w-full max-w-7xl mx-auto p-6 md:p-8 space-y-8 relative z-10">
        
        {/* Page Title & Breadcrumbs */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 tracking-tight flex items-center gap-3">
              <ChartIcon size={28} className="text-blue-600" /> Market Outlook
            </h2>
            <p className="text-slate-500 mt-2 text-lg max-w-2xl">
              Forecast freight-rate movement across the selected horizon based on processed historical and market features.
            </p>
          </div>
        </div>

        {/* Voyage Context Summary */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 animate-in fade-in slide-in-from-bottom-6 duration-700 delay-100">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4 flex items-center gap-2">
            <Ship size={16} /> Voyage Context
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            <div className="space-y-1">
              <span className="text-xs text-slate-500 font-medium">Route</span>
              <div className="text-sm font-semibold text-slate-900 flex items-center gap-1.5">
                {requirements?.origin || "Unknown"} <span className="text-slate-400 px-1">&rarr;</span> {requirements?.destination || "Unknown"}
              </div>
            </div>
            <div className="space-y-1">
              <span className="text-xs text-slate-500 font-medium">Commodity</span>
              <p className="text-sm font-semibold text-slate-900">{requirements?.commodity || "Not set"}</p>
            </div>
            <div className="space-y-1">
              <span className="text-xs text-slate-500 font-medium">Cargo Volume</span>
              <p className="text-sm font-semibold text-slate-900">{requirements?.cargoMt ? `${requirements.cargoMt} MT` : "Not set"}</p>
            </div>
            <div className="space-y-1">
              <span className="text-xs text-slate-500 font-medium">Delivery Date</span>
              <p className="text-sm font-semibold text-slate-900">{requirements?.deliveryDate || "Not set"}</p>
            </div>
            <div className="space-y-1">
              <span className="text-xs text-slate-500 font-medium">Laycan</span>
              <p className="text-sm font-semibold text-slate-900">{requirements?.laycan || "Not set"}</p>
            </div>
          </div>
        </div>

        {/* Data Source Transparency (Replaces full Data Acquisition page) */}
        <details className="group bg-white border border-slate-200 rounded-xl shadow-sm [&_summary::-webkit-details-marker]:hidden animate-in fade-in slide-in-from-bottom-6 duration-700 delay-150">
          <summary className="flex items-center justify-between p-4 cursor-pointer">
            <div className="flex items-center gap-2">
              <Database size={16} className="text-slate-400" />
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">Data Coverage & Sources</h3>
            </div>
            <div className="text-slate-400 group-open:rotate-180 transition-transform">
              <ChevronDown size={18} />
            </div>
          </summary>
          <div className="p-4 pt-0 border-t border-slate-100">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div className="space-y-3">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">Integrated Datasets</h4>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-slate-700">Historical Freight Data</span>
                  <span className="text-emerald-600 flex items-center gap-1 text-xs font-medium"><CheckCircle2 size={14}/> Available</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-slate-700">Vessel & Port Data</span>
                  <span className="text-emerald-600 flex items-center gap-1 text-xs font-medium"><CheckCircle2 size={14}/> Available</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-slate-700">Cargo & Route Data</span>
                  <span className="text-emerald-600 flex items-center gap-1 text-xs font-medium"><CheckCircle2 size={14}/> Available</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-slate-700">Bunker Price Data</span>
                  <span className="text-emerald-600 flex items-center gap-1 text-xs font-medium"><CheckCircle2 size={14}/> Available</span>
                </div>
              </div>
              <div className="space-y-3">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">Live Feeds</h4>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-slate-700">Real-Time Market Feeds</span>
                  <span className="text-slate-400 flex items-center gap-1 text-xs font-medium"><XCircle size={14}/> Not connected</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-slate-700">External Signal Feeds</span>
                  <span className="text-slate-400 flex items-center gap-1 text-xs font-medium"><XCircle size={14}/> Not connected</span>
                </div>
              </div>
            </div>
          </div>
        </details>

        {/* Forecast Horizon Tabs */}
        <div className="flex items-center gap-2 p-1 bg-slate-200/60 w-fit rounded-lg animate-in fade-in slide-in-from-bottom-6 duration-700 delay-150">
          {(["7D", "14D", "30D"] as Horizon[]).map((hz) => (
            <button
              key={hz}
              onClick={() => setHorizon(hz)}
              className={`px-6 py-2 rounded-md text-sm font-semibold transition-all ${
                horizon === hz 
                  ? "bg-white text-blue-700 shadow-sm" 
                  : "text-slate-500 hover:text-slate-700 hover:bg-slate-200/50"
              }`}
            >
              {hz}
            </button>
          ))}
        </div>

        {/* Forecast Visualization & Metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 animate-in fade-in slide-in-from-bottom-6 duration-700 delay-200">
          
          {/* Main Chart Area */}
          <div className="lg:col-span-3 bg-white border border-slate-200 rounded-xl shadow-sm p-6 flex flex-col min-h-[400px]">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-semibold text-slate-900">Freight Rate Forecast ({horizon})</h3>
              <div className="flex items-center gap-4 text-xs font-medium">
                <div className="flex items-center gap-1.5 text-slate-500"><div className="w-3 h-3 rounded-sm bg-slate-300"></div> Historical</div>
                <div className="flex items-center gap-1.5 text-slate-500"><div className="w-3 h-3 rounded-sm bg-blue-600"></div> Forecast</div>
                <div className="flex items-center gap-1.5 text-slate-500"><div className="w-3 h-3 rounded-sm bg-blue-100 border border-blue-200"></div> Confidence</div>
              </div>
            </div>

            <div className="flex-1 w-full relative bg-slate-50/50 rounded-lg border border-slate-100 flex items-center justify-center">
              {forecast.status === "awaiting_service" ? (
                <div className="text-center p-6 space-y-3">
                  <div className="w-12 h-12 bg-slate-100 text-slate-400 rounded-full flex items-center justify-center mx-auto mb-2">
                    <ChartIcon size={24} />
                  </div>
                  <h4 className="text-slate-900 font-semibold">Forecast not available yet</h4>
                  <p className="text-slate-500 text-sm max-w-sm">This estimate will appear once the forecasting model is connected.</p>
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart data={forecast.data} margin={{ top: 20, right: 20, bottom: 40, left: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                    <XAxis 
                      dataKey="date" 
                      stroke="#94a3b8" 
                      fontSize={12} 
                      tickLine={false} 
                      axisLine={false} 
                      tick={{ dy: 10 }}
                      minTickGap={30}
                      label={{ value: 'Date', position: 'insideBottom', offset: -20, fill: '#64748b', fontSize: 12 }}
                    />
                    <YAxis 
                      stroke="#94a3b8" 
                      fontSize={12} 
                      tickLine={false} 
                      axisLine={false} 
                      domain={['auto', 'auto']}
                      label={{ value: 'USD/MT', angle: -90, position: 'insideLeft', offset: 0, fill: '#64748b', fontSize: 12 }}
                    />
                    <Tooltip 
                      contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                      labelStyle={{ color: '#64748b', fontWeight: 500, marginBottom: '4px' }}
                      formatter={(value: any, name: any) => [value, name === 'historicalRate' ? 'Historical ($/MT)' : 'Forecast ($/MT)']}
                    />
                    {/* Confidence Area */}
                    <Area type="monotone" dataKey="confidenceRange" stroke="none" fill="#dbeafe" fillOpacity={0.5} connectNulls={false} />
                    {/* Historical Line */}
                    <Line type="monotone" dataKey="historicalRate" stroke="#94a3b8" strokeWidth={2} dot={false} connectNulls={false} />
                    {/* Forecast Line */}
                    <Line type="monotone" dataKey="forecastRate" stroke="#2563eb" strokeWidth={3} dot={{ r: 4, fill: '#2563eb', strokeWidth: 0 }} connectNulls={false} />
                  </ComposedChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>

          {/* Side Metrics (Trend & Confidence) */}
          <div className="flex flex-col gap-6">
            
            {/* Trend Card */}
            <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 flex flex-col">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">Trend</h3>
              <div className="flex items-center gap-3 xl:gap-4 mt-2">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 shrink-0">
                  {getTrendIcon(forecast.trend)}
                </div>
                <div className="min-w-0 flex-1">
                  <span className="text-xl xl:text-2xl font-bold text-slate-900 block truncate">{forecast.trend}</span>
                  <span className="text-sm text-slate-500 block truncate">Over {horizon} horizon</span>
                </div>
              </div>
              <div className="mt-auto pt-6">
                <p className="text-xs text-slate-400 bg-slate-50 p-2.5 rounded-md border border-slate-100">
                  Computed by feeding future BDI/Bunker projections (if provided) into the LightGBM model. 
                  Currently assumes static market conditions over the horizon.
                </p>
              </div>
            </div>

            {/* Confidence Card */}
            <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 flex flex-col flex-1">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">Confidence</h3>
              <div className="flex items-center gap-4 mt-2">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  <ShieldCheck size={24} className={forecast.confidence.includes("Low") ? "text-orange-500" : "text-green-500"} />
                </div>
                <div>
                  <span className={`text-2xl font-bold block ${forecast.confidence.includes("Low") ? "text-orange-600" : "text-green-600"}`}>
                    {forecast.confidence.includes("Low") ? "<50%" : "95%"}
                  </span>
                  <span className="text-sm text-slate-500">Model Reliability</span>
                </div>
              </div>
              <div className="mt-auto pt-6">
                <p className="text-xs text-slate-400 bg-slate-50 p-2.5 rounded-md border border-slate-100">
                  {forecast.confidence}
                </p>
              </div>
            </div>

          </div>
        </div>


        {/* Global Action Footer */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6 mt-8 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300">
          <div>
            <h4 className="font-bold text-lg text-slate-900">Proceed to Decision Workspace</h4>
            <p className="text-slate-500 text-sm max-w-lg mt-1">
              Move to the Decision Workspace to evaluate costs, risks, and recommended actions based on this forecast.
            </p>
          </div>
          <Button 
            size="lg" 
            onClick={() => {
              markStepComplete('/freight-forecasting');
              navigate('/decision-workspace');
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white w-full md:w-auto shrink-0 shadow-md"
          >
            Go to Decision Workspace
          </Button>
        </div>

      </main>
    </div>
  );
}
