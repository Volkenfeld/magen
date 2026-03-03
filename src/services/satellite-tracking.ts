/**
 * Satellite tracking for Magen variant.
 * Fetches TLE data from CelesTrak and propagates positions using SGP4.
 * Shows ISS, notable satellites, and military satellites.
 */

import {
  twoline2satrec,
  propagate,
  gstime,
  eciToGeodetic,
  degreesLong,
  degreesLat,
} from 'satellite.js';
import { SITE_VARIANT } from '@/config';

export interface TrackedSatellite {
  id: string;
  name: string;
  lat: number;
  lon: number;
  altitude: number;      // km
  velocity: number;      // km/s
  category: 'station' | 'starlink' | 'military' | 'science' | 'weather';
  visible: boolean;      // currently in sunlight + above horizon
  orbitPath?: [number, number][]; // ground track points [lon, lat]
}

// Proxy through our Vercel edge function to avoid CORS issues with CelesTrak
const TLE_URLS: Record<string, string> = {
  stations: '/api/satellites?group=stations',
  military: '/api/satellites?group=military',
};

// Only fetch a subset to keep performance sane
const MAX_SATELLITES_PER_GROUP: Record<string, number> = {
  stations: 10,
  military: 15,
};

interface TLERecord {
  name: string;
  line1: string;
  line2: string;
  category: TrackedSatellite['category'];
}

const CACHE_TTL = 10 * 60 * 1000; // 10 minutes
let tleCache: { records: TLERecord[]; timestamp: number } | null = null;
let positionCache: { data: TrackedSatellite[]; timestamp: number } | null = null;
const POSITION_REFRESH = 30 * 1000; // Refresh positions every 30s

function parseTLEText(text: string, category: TrackedSatellite['category'], maxCount: number): TLERecord[] {
  const lines = text.trim().split('\n').map(l => l.trim()).filter(Boolean);
  const records: TLERecord[] = [];

  for (let i = 0; i + 2 < lines.length && records.length < maxCount; i += 3) {
    const name = lines[i];
    const line1 = lines[i + 1];
    const line2 = lines[i + 2];

    if (!name || !line1?.startsWith('1 ') || !line2?.startsWith('2 ')) continue;

    records.push({ name, line1, line2, category });
  }

  return records;
}

async function fetchTLEs(): Promise<TLERecord[]> {
  if (tleCache && Date.now() - tleCache.timestamp < CACHE_TTL) {
    return tleCache.records;
  }

  const allRecords: TLERecord[] = [];

  const groupsToFetch: Array<[string, TrackedSatellite['category']]> = [
    ['stations', 'station'],
    ['military', 'military'],
  ];

  const results = await Promise.allSettled(
    groupsToFetch.map(async ([group, category]) => {
      try {
        const url = TLE_URLS[group];
        if (!url) return [];
        const res = await fetch(url, {
          headers: { Accept: 'text/plain' },
        });
        if (!res.ok) return [];
        const text = await res.text();
        const max = MAX_SATELLITES_PER_GROUP[group] ?? 10;
        return parseTLEText(text, category, max);
      } catch {
        return [];
      }
    })
  );

  for (const result of results) {
    if (result.status === 'fulfilled') {
      allRecords.push(...result.value);
    }
  }

  if (allRecords.length > 0) {
    tleCache = { records: allRecords, timestamp: Date.now() };
  }

  return allRecords;
}

function propagatePosition(tle: TLERecord, date: Date): TrackedSatellite | null {
  try {
    const satrec = twoline2satrec(tle.line1, tle.line2);
    const pv = propagate(satrec, date);

    if (!pv || !pv.position || typeof pv.position === 'boolean') {
      return null;
    }

    const position = pv.position;
    const gmst = gstime(date);
    const geo = eciToGeodetic(position, gmst);

    const lat = degreesLat(geo.latitude);
    const lon = degreesLong(geo.longitude);
    const altitude = geo.height; // km

    // Calculate velocity magnitude
    let velocity = 0;
    if (pv.velocity && typeof pv.velocity !== 'boolean') {
      const v = pv.velocity;
      velocity = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
    }

    // Extract NORAD catalog number from TLE line 1
    const noradId = tle.line1.substring(2, 7).trim();

    return {
      id: `sat-${noradId}`,
      name: tle.name.replace(/^\d+\s*/, '').trim() || tle.name,
      lat,
      lon,
      altitude,
      velocity,
      category: tle.category,
      visible: altitude > 0,
    };
  } catch {
    return null;
  }
}

function computeOrbitPath(tle: TLERecord, date: Date, points = 60): [number, number][] {
  try {
    const satrec = twoline2satrec(tle.line1, tle.line2);
    // Estimate orbital period from mean motion (rev/day in line 2)
    const meanMotion = parseFloat(tle.line2.substring(52, 63));
    if (!meanMotion || meanMotion <= 0) return [];
    const periodMs = (24 * 60 * 60 * 1000) / meanMotion;
    const step = periodMs / points;
    const path: [number, number][] = [];

    for (let i = 0; i < points; i++) {
      const t = new Date(date.getTime() - periodMs / 2 + i * step);
      const pv2 = propagate(satrec, t);
      if (!pv2 || !pv2.position || typeof pv2.position === 'boolean') continue;

      const pos = pv2.position;
      const gmst = gstime(t);
      const geo = eciToGeodetic(pos, gmst);
      path.push([degreesLong(geo.longitude), degreesLat(geo.latitude)]);
    }

    return path;
  } catch {
    return [];
  }
}

export async function fetchSatellitePositions(): Promise<TrackedSatellite[]> {
  if (SITE_VARIANT !== 'magen') return [];

  // Return position cache if still fresh (positions change fast, but 30s is fine)
  if (positionCache && Date.now() - positionCache.timestamp < POSITION_REFRESH) {
    return positionCache.data;
  }

  const tles = await fetchTLEs();
  if (tles.length === 0) return positionCache?.data || [];

  const now = new Date();
  const satellites: TrackedSatellite[] = [];

  for (const tle of tles) {
    const sat = propagatePosition(tle, now);
    if (!sat) continue;

    // Only compute orbit path for ISS and station-category satellites
    if (tle.name.includes('ISS') || tle.name.includes('TIANGONG') || tle.category === 'station') {
      sat.orbitPath = computeOrbitPath(tle, now, 80);
    }

    satellites.push(sat);
  }

  positionCache = { data: satellites, timestamp: Date.now() };
  return satellites;
}

export function getSatelliteCount(): number {
  return positionCache?.data.length || 0;
}
