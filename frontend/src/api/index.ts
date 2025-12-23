const API_BASE = import.meta.env.VITE_API_URL || '';

export interface BirthFormData {
  nickname: string;
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  gender: number;
  is_lunar: boolean;
  province: string;
  city: string;
  city_long: number;
}

export interface Marker {
  name: string;
  icon: string;
  type: string;
  desc: string;
}

export interface TrendData {
  year: number;
  ganzhi: string;
  score: number;
  markers: Marker[];
}

export interface City {
  name: string;
  longitude: number;
}

export async function calculateBazi(data: BirthFormData) {
  const response = await fetch(`${API_BASE}/api/calculate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    throw new Error('计算失败');
  }
  
  return response.json();
}

export async function getProvinces(): Promise<string[]> {
  const response = await fetch(`${API_BASE}/api/provinces`);
  const data = await response.json();
  return data.provinces;
}

export async function getCities(province: string): Promise<City[]> {
  const response = await fetch(`${API_BASE}/api/cities/${encodeURIComponent(province)}`);
  const data = await response.json();
  return data.cities;
}

// 兼容旧版API
export const api = {
  getProvinces,
  getCities,
  calculate: calculateBazi,
};
