const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api/v1';

async function fetchApi(endpoint: string, payload: any) {
  const token = localStorage.getItem('odyssey_auth_token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = 'Bearer ' + token;
  }
  const res = await fetch(API_URL + endpoint, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error('API Error ' + res.status);
  }
  return res.json();
}

export const submitVoyage = async (req: any) => fetchApi('/voyage/submit', req);
export const getFeasibility = async (req: any) => fetchApi('/voyage/feasibility', req);
export const getCosts = async (req: any) => fetchApi('/voyage/cost', req);
export const getRisks = async (req: any) => fetchApi('/voyage/risk', req);
export const evaluateScenarios = async (req: any) => fetchApi('/evaluate_scenarios', req);
export const generateRecommendation = async (req: any) => fetchApi('/generate_recommendation', req);
