/**
 * Vercel Edge Function to proxy CelesTrak TLE data.
 * CelesTrak may not set CORS headers, so we proxy through our own domain.
 */
import { getCorsHeaders, isDisallowedOrigin } from './_cors.js';

export const config = { runtime: 'edge' };

const CELESTRAK_BASE = 'https://celestrak.org/NORAD/elements/gp.php';
const ALLOWED_GROUPS = new Set(['stations', 'military', 'science', 'weather', 'starlink']);

export default async function handler(req) {
  const corsHeaders = getCorsHeaders(req, 'GET, OPTIONS');

  if (isDisallowedOrigin(req)) {
    return new Response(JSON.stringify({ error: 'Origin not allowed' }), {
      status: 403,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  }

  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (req.method !== 'GET') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  }

  const url = new URL(req.url);
  const group = url.searchParams.get('group');

  if (!group || !ALLOWED_GROUPS.has(group)) {
    return new Response(JSON.stringify({ error: 'Invalid group parameter' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  }

  try {
    const celestrakUrl = `${CELESTRAK_BASE}?GROUP=${group}&FORMAT=tle`;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);

    const response = await fetch(celestrakUrl, {
      headers: { Accept: 'text/plain' },
      signal: controller.signal,
    });
    clearTimeout(timeout);

    if (!response.ok) {
      return new Response(JSON.stringify({ error: `CelesTrak returned ${response.status}` }), {
        status: 502,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      });
    }

    const body = await response.text();

    return new Response(body, {
      status: 200,
      headers: {
        'Content-Type': 'text/plain',
        'Cache-Control': 'public, s-maxage=600, stale-while-revalidate=300',
        ...corsHeaders,
      },
    });
  } catch (error) {
    const isTimeout = error?.name === 'AbortError';
    return new Response(JSON.stringify({
      error: isTimeout ? 'CelesTrak timeout' : 'CelesTrak fetch failed',
    }), {
      status: isTimeout ? 504 : 502,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  }
}
