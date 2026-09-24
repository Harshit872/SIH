import shippingDataset from './generated/shipping_dataset.json';
import balticIndices from './generated/baltic_indices.json';

export interface Vessel {
  "Vessel Type": string;
  "DWT (mt)": number;
  "SSW Draft (m)": number;
  "LOA (m)": number;
  "Beam (m)": number;
  "Grain Capacity (cbm)": number;
  "Laden Speed (kn)": number;
  "Ballast Speed (kn)": number;
  "Max Age (yr)": number;
  "Geared": boolean;
  "Source": string;
}

export interface PortBerth {
  "Port": string;
  "Berth/Facility": string;
  "Commodity": string;
  "Max LOA (m)": number | string;
  "Max Beam (m)": number | string;
  "Max Draft (m)": number | string;
  "High Tide Qualification": boolean | string;
  "Handling / Facility": string;
  "Source": string;
  "Remarks": string;
}

export interface Cargo {
  "Cargo": string;
  "Cargo Class": string;
  "Use": string;
  "Example Quantity": number;
  "Unit": string;
  "Origin Example": string;
  "Destination Example": string;
  "Candidate Vessel Types": string;
  "Source": string;
  "Status": string;
}

export interface RouteBenchmark {
  "Origin": string;
  "Destination": string;
  "Cargo": string;
  "Vessel Type": string;
  "Cargo Quantity (mt)": number | string;
  "Freight Rate": number | string;
  "Rate Unit": string;
  "Baltic Route": string;
  "Source": string;
  "Status": string;
}

export interface BunkerPrice {
  "Date": string | number;
  "Singapore VLSFO Indicative (USD/mt)": number;
  "Source": string;
  "Status": string;
}

export interface BalticIndex {
  "Date": string;
  "BDI": number | string;
  "BCI": number | string;
  "BPI": number | string;
  "BSI": number | string;
  "BHSI": number | string;
}

export class DatasetService {
  static getVessels(): Vessel[] {
    return shippingDataset['03_Vessel_Master'] as Vessel[];
  }

  static getPorts(): PortBerth[] {
    return shippingDataset['04_Port_Berth_Master'] as PortBerth[];
  }

  static getUniquePorts(): string[] {
    const ports = new Set(this.getPorts().map(p => p.Port));
    // Also include origins/destinations from routes
    this.getRoutes().forEach(r => {
      if (r.Origin) ports.add(r.Origin);
      if (r.Destination) ports.add(r.Destination);
    });
    return Array.from(ports).filter(Boolean);
  }

  static getCargoes(): Cargo[] {
    return shippingDataset['05_Cargo_Master'] as Cargo[];
  }

  static getRoutes(): RouteBenchmark[] {
    return shippingDataset['06_Route_Benchmarks'] as RouteBenchmark[];
  }

  static getBunkerPrices(): BunkerPrice[] {
    return shippingDataset['07_Bunker_Prices'] as BunkerPrice[];
  }

  static getBalticIndices(): BalticIndex[] {
    return balticIndices as BalticIndex[];
  }
}
