/**
 * Live civilian flight tracking for Magen variant.
 * Queries OpenSky for ALL flights in the Israel/MENA region,
 * returning simplified position data for map visualization.
 */

import { SITE_VARIANT } from '@/config';

export interface LiveFlight {
  icao24: string;
  callsign: string;
  lat: number;
  lon: number;
  altitude: number;    // feet
  heading: number;     // degrees
  speed: number;       // knots
  onGround: boolean;
  country: string;
  lastSeen: Date;
}

// Israel/MENA focused bounding box
const MENA_REGION = { lamin: 27, lamax: 38, lomin: 31, lomax: 43 };

const OPENSKY_PROXY_URL = '/api/opensky';
const CACHE_TTL = 2 * 60 * 1000; // 2 minutes
let flightCache: { data: LiveFlight[]; timestamp: number } | null = null;
let fetchInFlight: Promise<LiveFlight[]> | null = null;

type OpenSkyStateArray = [
  string,        // 0: icao24
  string | null, // 1: callsign
  string,        // 2: origin_country
  number | null, // 3: time_position
  number,        // 4: last_contact
  number | null, // 5: longitude
  number | null, // 6: latitude
  number | null, // 7: baro_altitude (meters)
  boolean,       // 8: on_ground
  number | null, // 9: velocity (m/s)
  number | null, // 10: true_track (degrees)
  number | null, // 11: vertical_rate (m/s)
  number[] | null, // 12: sensors
  number | null, // 13: geo_altitude
  string | null, // 14: squawk
  boolean,       // 15: spi
  number         // 16: position_source
];

function parseFlights(states: OpenSkyStateArray[] | null): LiveFlight[] {
  if (!states) return [];
  const now = new Date();
  const flights: LiveFlight[] = [];

  for (const s of states) {
    const lat = s[6];
    const lon = s[5];
    if (lat === null || lon === null) continue;

    flights.push({
      icao24: s[0],
      callsign: (s[1] || '').trim() || s[0].toUpperCase().slice(0, 6),
      lat,
      lon,
      altitude: s[7] ? Math.round(s[7] * 3.28084) : 0,
      heading: s[10] || 0,
      speed: s[9] ? Math.round(s[9] * 1.94384) : 0,
      onGround: s[8],
      country: s[2],
      lastSeen: now,
    });
  }

  return flights;
}

export async function fetchLiveFlights(): Promise<LiveFlight[]> {
  if (SITE_VARIANT !== 'magen') return [];

  // Return cached data if fresh
  if (flightCache && Date.now() - flightCache.timestamp < CACHE_TTL) {
    return flightCache.data;
  }

  // Deduplicate concurrent calls
  if (fetchInFlight) return fetchInFlight;

  fetchInFlight = (async () => {
    try {
      const query = `lamin=${MENA_REGION.lamin}&lamax=${MENA_REGION.lamax}&lomin=${MENA_REGION.lomin}&lomax=${MENA_REGION.lomax}`;
      const res = await fetch(`${OPENSKY_PROXY_URL}?${query}`, {
        headers: { Accept: 'application/json' },
      });

      if (!res.ok) {
        console.warn(`[LiveFlights] OpenSky returned ${res.status}`);
        return flightCache?.data || [];
      }

      const data = await res.json() as { states: OpenSkyStateArray[] | null };
      const flights = parseFlights(data.states);
      flightCache = { data: flights, timestamp: Date.now() };
      return flights;
    } catch (err) {
      console.warn('[LiveFlights] Fetch failed:', err);
      return flightCache?.data || [];
    } finally {
      fetchInFlight = null;
    }
  })();

  return fetchInFlight;
}

export function getLiveFlightsCount(): number {
  return flightCache?.data.length || 0;
}
