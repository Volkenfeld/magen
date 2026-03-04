import { createRelayHandler } from './_relay.js';

export const config = { runtime: 'edge' };

export default createRelayHandler({
  buildRelayPath: (_req, url) => {
    const endpoint = url.searchParams.get('endpoint');
    return endpoint === 'history' ? '/oref/history' : '/oref/alerts';
  },
  forwardSearch: false,
  timeout: 12000,
  onlyOk: true,
  cacheHeaders: () => ({
    // Short cache for near-real-time alert delivery (Tzevaadom feeds relay instantly)
    'Cache-Control': 'public, max-age=5, s-maxage=10, stale-while-revalidate=5, stale-if-error=30',
  }),
  fallback: (_req, corsHeaders) => new Response(JSON.stringify({
    configured: false,
    alerts: [],
    historyCount24h: 0,
    timestamp: new Date().toISOString(),
    error: 'No data source available',
  }), {
    status: 503,
    headers: { 'Content-Type': 'application/json', ...corsHeaders },
  }),
});
