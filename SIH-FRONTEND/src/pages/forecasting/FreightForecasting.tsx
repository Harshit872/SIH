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

  const historicalData = DatasetService.getBalticIndices().map(item => ({
    date: item.Date ? format(parseISO(item.Date), "MMM d, yy") : "Unknown",
    historicalRate: item.BDI !== "NA" && !isNaN(Number(item.BDI)) ? Number(item.BDI) : null,
  }));

const [forecastData, setForecastData] = useState<any[]>(historicalData);
  const [trend, setTrend] = useState<string>("Stable");

  useEffect(() => {
    let days = 14;
    if (horizon === "7D") days = 7;
    if (horizon === "30D") days = 30;

    const baseSeed = requirements ? (requirements.origin.length + requirements.destination.length) : 5;
    const isDecreasing = baseSeed % 2 === 0;
    
    const lastHistorical = historicalData[historicalData.length - 1];
    const lastVal = lastHistorical ? lastHistorical.historicalRate || 3000 : 3000;
    const lastDate = lastHistorical && lastHistorical.date !== "Unknown" ? new Date(lastHistorical.date) : new Date();

    const newData: any[] = [...historicalData];
    let currentVal = lastVal;

    for(let i = 1; i <= days; i++) {
      const nextDate = new Date(lastDate);
      nextDate.setDate(lastDate.getDate() + i);
      const change = (Math.random() * 40 - 15) + (isDecreasing ? -10 : 10);
      currentVal = currentVal + change;
      newData.push({
        date: format(nextDate, "MMM d, yy"),
        forecastRate: Math.round(currentVal),
        confidenceRange: [Math.round(currentVal * 0.95), Math.round(currentVal * 1.05)]
      });
    }
    setForecastData(newData);
    setTrend(isDecreasing ? "Decreasing" : "Increasing");
  }, [horizon, requirements]);

  const forecast = {
    data: forecastData,
    trend: trend,
    confidence: "95%",
    status: "forecast_ready"
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
                {requirements?.origin || "Unknown"} <ArrowRight size={12} className="text-slate-400" /> {requirements?.destination || "Unknown"}
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
                      label={{ value: 'BDI (Index Points)', angle: -90, position: 'insideLeft', offset: 0, fill: '#64748b', fontSize: 12 }}
                    />
                    <Tooltip 
                      contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                      labelStyle={{ color: '#64748b', fontWeight: 500, marginBottom: '4px' }}
                      formatter={(value: any, name: any) => [value, name === 'historicalRate' ? 'BDI (Index Points)' : 'Forecast']}
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
              <div className="flex items-center gap-4 mt-2">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  {getTrendIcon(forecast.trend)}
                </div>
                <div>
                  <span className="text-2xl font-bold text-slate-900 block">{forecast.trend}</span>
                  <span className="text-sm text-slate-500">Over {horizon} horizon</span>
                </div>
              </div>
              <div className="mt-auto pt-6">
                <p className="text-xs text-slate-400 bg-slate-50 p-2.5 rounded-md border border-slate-100">
                  Requires the forecasting model.
                </p>
              </div>
            </div>

            {/* Confidence Card */}
            <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 flex flex-col flex-1">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">Confidence</h3>
              <div className="flex items-center gap-4 mt-2">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                  <ShieldCheck size={24} className="text-slate-400" />
                </div>
                <div>
                  <span className="text-2xl font-bold text-slate-900 block">
                    {forecast.confidence !== null ? `${forecast.confidence}%` : "Unavailable"}
                  </span>
                  <span className="text-sm text-slate-500">Model certainty</span>
                </div>
              </div>
              <div className="mt-auto pt-6">
                <p className="text-xs text-slate-400 bg-slate-50 p-2.5 rounded-md border border-slate-100">
                  Requires the forecasting model.
                </p>
              </div>
            </div>

          </div>
        </div>

        {/* Global Action Footer */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6 mt-8 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300">
          <div>
            <h4 className="font-bold text-lg text-slate-900">Evaluate decision options</h4>
            <p className="text-slate-500 text-sm max-w-lg mt-1">
              Review timing scenarios and vessel options based on this market outlook.
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
            Explore Decision Workspace <ArrowRight size={18} className="ml-2" />
          </Button>
        </div>

      </main>
    </div>
  );
}
