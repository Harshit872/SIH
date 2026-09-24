import fs from 'fs';
import path from 'path';
import xlsx from 'xlsx';
import Papa from 'papaparse';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DATASETS_DIR = path.resolve(__dirname, '../../datasets');

const OUTPUT_DIR = path.resolve(__dirname, '../src/data/generated');

// Ensure output dir exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log('Parsing datasets...');

try {
  // 1. Parse Excel
  const excelPath = path.join(DATASETS_DIR, 'complete_shipping_decision_dataset.xlsx');
  console.log(`Reading Excel: ${excelPath}`);
  
  if (!fs.existsSync(excelPath)) {
    throw new Error(`Excel file not found at ${excelPath}`);
  }

  const workbook = xlsx.readFile(excelPath);
  const excelData = {};

  workbook.SheetNames.forEach(sheetName => {
    const sheet = workbook.Sheets[sheetName];
    // Convert to JSON array
    const data = xlsx.utils.sheet_to_json(sheet);
    excelData[sheetName] = data;
    console.log(`- Parsed sheet ${sheetName} with ${data.length} rows`);
  });

  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'shipping_dataset.json'),
    JSON.stringify(excelData, null, 2)
  );

  // 2. Parse CSV
  const csvPath = path.join(DATASETS_DIR, 'baltic_indices_historical.csv');
  console.log(`Reading CSV: ${csvPath}`);
  
  if (!fs.existsSync(csvPath)) {
    throw new Error(`CSV file not found at ${csvPath}`);
  }

  const csvContent = fs.readFileSync(csvPath, 'utf-8');
  Papa.parse(csvContent, {
    header: true,
    dynamicTyping: true,
    complete: (results) => {
      fs.writeFileSync(
        path.join(OUTPUT_DIR, 'baltic_indices.json'),
        JSON.stringify(results.data, null, 2)
      );
      console.log(`- Parsed CSV with ${results.data.length} rows`);
    },
    error: (error) => {
      console.error('Error parsing CSV:', error);
    }
  });

  console.log('Successfully generated JSON datasets.');

} catch (err) {
  console.error('Error:', err);
}
