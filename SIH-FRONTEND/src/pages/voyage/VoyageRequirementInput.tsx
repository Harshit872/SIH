import { useState, useMemo, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router";
import { MapPin, Calendar, Navigation, Info } from "lucide-react";
import { useVoyage } from "../../contexts/VoyageContext";
import { Button } from "../../components/ui/button";
import { SearchableSelect } from "../../components/ui/SearchableSelect";
import { DatePicker } from "../../components/ui/DatePicker";
import type { DateRange } from "react-day-picker";
import { format } from "date-fns";

import { DatasetService } from "../../data/DatasetService";
import { DEMO_SCENARIOS } from "../../data/demo/demoVoyages";

const PORT_OPTIONS = DatasetService.getUniquePorts().map(port => ({
  value: port.toLowerCase().replace(/[^a-z0-9]/g, '_'),
  label: port
}));

const COMMODITY_OPTIONS = DatasetService.getCargoes().map(cargo => ({
  value: cargo.Cargo.toLowerCase().replace(/[^a-z0-9]/g, '_'),
  label: cargo.Cargo
}));

const CONTRACT_OPTIONS = [
  { value: "voyage_charter", label: "Voyage Charter" },
  { value: "time_charter", label: "Time Charter" },
  { value: "coa", label: "Contract of Affreightment (COA)" },
  { value: "bareboat", label: "Bareboat Charter" },
];

// Assumed standard vessel capacity for calculation
const STANDARD_VESSEL_CAPACITY_MT = 50000;

export function VoyageRequirementInput() {
  const navigate = useNavigate();
  const { setRequirements, markStepComplete } = useVoyage();
  const [isLoading, setIsLoading] = useState(false);
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [commodity, setCommodity] = useState("");
  const [cargoMt, setCargoMt] = useState("");
  const [contract, setContract] = useState("");
  const [deliveryDate, setDeliveryDate] = useState<Date | null>(null);
  const [laycan, setLaycan] = useState<DateRange | undefined>();
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  // Hidden demo loader
  const [searchParams] = useSearchParams();
  useEffect(() => {
    const demoId = searchParams.get('demo');
    if (demoId) {
      handleDemoSelect(demoId);
    }
  }, [searchParams]);

  // Dynamic calculated field
  const calculatedVoyages = useMemo(() => {
    const mt = Number(cargoMt);
    if (!mt || isNaN(mt) || mt <= 0) return 0;
    return Math.ceil(mt / STANDARD_VESSEL_CAPACITY_MT);
  }, [cargoMt]);

  const clearError = (field: string) => {
    if (errors[field]) setErrors(prev => ({ ...prev, [field]: "" }));
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    if (!origin) newErrors.origin = "Origin is required";
    if (!destination) newErrors.destination = "Destination is required";
    if (!commodity) newErrors.commodity = "Commodity is required";
    if (!cargoMt) {
      newErrors.cargoMt = "Cargo MT is required";
    } else if (Number(cargoMt) <= 0) {
      newErrors.cargoMt = "Must be positive";
    }
    if (!contract) newErrors.contract = "Contract is required";
    if (!deliveryDate) newErrors.deliveryDate = "Delivery Date is required";
    if (!laycan?.from || !laycan?.to) newErrors.laycan = "Full Laycan window is required";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleDemoSelect = (demoId: string) => {
    if (!demoId) return;
    
    const demo = DEMO_SCENARIOS.find(d => d.id === demoId);
    if (demo) {
      setOrigin(demo.origin);
      setDestination(demo.destination);
      setCommodity(demo.commodity);
      setCargoMt(demo.cargoQuantity);
      setContract(demo.contract);
      setDeliveryDate(demo.deliveryDate);
      setLaycan({ from: demo.laycanStart, to: demo.laycanEnd });
      setErrors({});
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      setIsLoading(true);
      setTimeout(() => {
        setRequirements({
          origin: PORT_OPTIONS.find(o => o.value === origin)?.label || origin,
          destination: PORT_OPTIONS.find(o => o.value === destination)?.label || destination,
          commodity: COMMODITY_OPTIONS.find(o => o.value === commodity)?.label || commodity,
          cargoMt: Number(cargoMt),
          deliveryDate: deliveryDate ? format(deliveryDate, "yyyy-MM-dd") : "",
          contract: CONTRACT_OPTIONS.find(o => o.value === contract)?.label || contract,
          laycan: (laycan?.from && laycan?.to) ? `${format(laycan.from, "dd MMM yyyy")} - ${format(laycan.to, "dd MMM yyyy")}` : "",
          noOfVoyages: calculatedVoyages
        });
        setIsLoading(false);
        markStepComplete("/voyage-requirement-input");
        navigate("/freight-forecasting");
      }, 800);
    }
  };

  return (
    <div className="w-full relative flex flex-col min-h-full">
      {/* Subtle Maritime Background */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div 
          className="absolute inset-0 scale-[1.02]"
          style={{
            backgroundImage: 'url("/ship-bg.jpg")',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            filter: 'blur(3px)'
          }}
        />
        {/* Light professional blue/white maritime tint overlay to ensure form readability */}
        <div className="absolute inset-0 bg-white/70" />
        <div className="absolute inset-0 bg-blue-900/5 mix-blend-color" />
      </div>

      <main className="flex-1 max-w-4xl w-full mx-auto p-6 md:p-8 relative z-10 py-12">
        <div className="mb-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <h2 className="text-3xl font-bold text-slate-900 tracking-tight">Voyage Details</h2>
          <p className="text-muted-foreground mt-2 text-lg drop-shadow-sm">
            Define the fundamental parameters for your upcoming shipping requirement.
          </p>
        </div>

        <div className="bg-card/95 backdrop-blur-md border border-border rounded-xl shadow-xl overflow-hidden animate-in fade-in slide-in-from-bottom-6 duration-700">
          <div className="bg-muted/80 px-6 py-4 border-b border-border flex items-center gap-2">
            <Navigation className="text-secondary" size={20} />
            <h3 className="font-semibold text-primary">Requirement Specifications</h3>
          </div>
          
          <form onSubmit={handleSubmit} className="p-6 md:p-8 space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              
              {/* Route Parameters */}
              <div className="space-y-6">
                <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider border-b border-border pb-2 flex items-center gap-2">
                  <MapPin size={16} /> Route & Logistics
                </h4>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Origin Port / Region</label>
                  <SearchableSelect 
                    options={PORT_OPTIONS}
                    value={origin}
                    onChange={(val) => { setOrigin(val); clearError("origin"); }}
                    placeholder="Search origin..."
                    error={!!errors.origin}
                  />
                  {errors.origin && <p className="text-xs text-destructive">{errors.origin}</p>}
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Destination Port / Region</label>
                  <SearchableSelect 
                    options={PORT_OPTIONS}
                    value={destination}
                    onChange={(val) => { setDestination(val); clearError("destination"); }}
                    placeholder="Search destination..."
                    error={!!errors.destination}
                  />
                  {errors.destination && <p className="text-xs text-destructive">{errors.destination}</p>}
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground flex items-center gap-2">Commodity</label>
                  <SearchableSelect 
                    options={COMMODITY_OPTIONS}
                    value={commodity}
                    onChange={(val) => { setCommodity(val); clearError("commodity"); }}
                    placeholder="Search commodity..."
                    error={!!errors.commodity}
                  />
                  {errors.commodity && <p className="text-xs text-destructive">{errors.commodity}</p>}
                </div>

                <div className="space-y-2">
                  <label htmlFor="cargoMt" className="text-sm font-medium text-foreground flex items-center gap-2">Cargo Volume (MT)</label>
                  <input
                    id="cargoMt"
                    name="cargoMt"
                    type="number"
                    min="1"
                    placeholder="e.g., 50000"
                    value={cargoMt}
                    onChange={(e) => { setCargoMt(e.target.value); clearError("cargoMt"); }}
                    className={`flex h-11 w-full rounded-md border ${errors.cargoMt ? 'border-destructive' : 'border-input'} bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring`}
                  />
                  {errors.cargoMt && <p className="text-xs text-destructive">{errors.cargoMt}</p>}
                </div>
              </div>

              {/* Schedule & Commercial */}
              <div className="space-y-6">
                <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-wider border-b border-border pb-2 flex items-center gap-2">
                  <Calendar size={16} /> Schedule & Commercial
                </h4>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Delivery Date (Target)</label>
                  <DatePicker 
                    mode="single"
                    selected={deliveryDate}
                    onSelect={(date) => { setDeliveryDate(date); clearError("deliveryDate"); }}
                    placeholder="Select delivery date"
                    error={!!errors.deliveryDate}
                  />
                  {errors.deliveryDate && <p className="text-xs text-destructive">{errors.deliveryDate}</p>}
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Laycan (Window)</label>
                  <DatePicker 
                    mode="range"
                    selected={laycan}
                    onSelect={(range) => { setLaycan(range); clearError("laycan"); }}
                    placeholder="Start Date -> End Date"
                    error={!!errors.laycan}
                  />
                  {errors.laycan && <p className="text-xs text-destructive">{errors.laycan}</p>}
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground flex items-center gap-2">Contract Type</label>
                  <SearchableSelect 
                    options={CONTRACT_OPTIONS}
                    value={contract}
                    onChange={(val) => { setContract(val); clearError("contract"); }}
                    placeholder="Select contract..."
                    error={!!errors.contract}
                  />
                  {errors.contract && <p className="text-xs text-destructive">{errors.contract}</p>}
                </div>

                {/* System Calculated: No. of Voyages */}
                <div className="pt-4">
                  <div className="bg-primary/5 border border-primary/10 rounded-lg p-4">
                    <h5 className="text-sm font-semibold text-primary mb-1 flex items-center gap-2">
                      <Info size={16} /> Estimated Voyages Required
                    </h5>
                    <div className="flex items-baseline gap-2">
                      <span className="text-3xl font-bold text-secondary">
                        {calculatedVoyages}
                      </span>
                      <span className="text-muted-foreground font-medium">Voyage{calculatedVoyages !== 1 ? 's' : ''}</span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">
                      Calculated automatically based on {cargoMt || "0"} MT cargo volume and standard available vessel capacity.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-6 border-t border-border flex justify-end">
              <Button type="submit" size="lg" className="bg-blue-600 hover:bg-blue-700 h-12 px-8 text-base shadow-md text-white font-semibold" disabled={isLoading}>
                {isLoading ? "Saving Requirements..." : "Analyze Voyage"}
              </Button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}
