export function miniSparkline(data: number[] | undefined, change: number | null, w = 50, h = 16): string {
  if (!data || data.length < 2) return '';
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const color = change != null && change >= 0 ? 'var(--green)' : 'var(--red)';
  const points = data.map((v, i) => {
    const x = (i / (data.length - 1)) * w;
    const y = h - ((v - min) / range) * (h - 2) - 1;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');
  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" class="mini-sparkline"><polyline points="${points}" fill="none" stroke="${color}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
}

/**
 * Horizontal gauge bar with fill. Returns an HTML string.
 * value/max determines fill width. Color sets the bar color.
 */
export function gaugeBar(value: number, max: number, color: string, height = 6): string {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  return `<div class="viz-gauge" style="height:${height}px"><div class="viz-gauge-fill" style="width:${pct.toFixed(1)}%;background:${color}"></div></div>`;
}

/**
 * Labeled gauge bar with label on left, value on right, bar below.
 */
export function labeledGauge(label: string, value: number, max: number, color: string): string {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  return `<div class="viz-labeled-gauge">
    <div class="viz-gauge-header"><span class="viz-gauge-label">${label}</span><span class="viz-gauge-value" style="color:${color}">${value}</span></div>
    <div class="viz-gauge" style="height:4px"><div class="viz-gauge-fill" style="width:${pct.toFixed(1)}%;background:${color}"></div></div>
  </div>`;
}

/**
 * SVG arc/donut gauge. Shows value as a partial arc out of max.
 * Returns an SVG string. Size is diameter in px.
 */
export function arcGauge(value: number, max: number, color: string, size = 48): string {
  const pct = Math.min(1, Math.max(0, value / max));
  const r = (size - 6) / 2;
  const cx = size / 2;
  const cy = size / 2;
  const circumference = 2 * Math.PI * r;
  const dashLen = circumference * pct;
  const gapLen = circumference - dashLen;
  // Start at top (-90deg rotation)
  return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" class="viz-arc">
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="var(--overlay-medium)" stroke-width="4"/>
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${color}" stroke-width="4" stroke-linecap="round" stroke-dasharray="${dashLen.toFixed(1)} ${gapLen.toFixed(1)}" transform="rotate(-90 ${cx} ${cy})"/>
    <text x="${cx}" y="${cy}" text-anchor="middle" dominant-baseline="central" fill="${color}" font-size="${size * 0.3}px" font-weight="700" font-family="var(--font-mono)">${value}</text>
  </svg>`;
}

/**
 * Tone indicator bar. Maps tone (-10 to +10) to a color gradient.
 * Negative = red, neutral = gray, positive = green.
 */
export function toneIndicator(tone: number): string {
  const normalized = Math.min(10, Math.max(-10, tone));
  // Position: -10 = 0%, 0 = 50%, +10 = 100%
  const position = ((normalized + 10) / 20) * 100;
  const color = normalized < -2 ? 'var(--semantic-critical)' : normalized > 2 ? 'var(--semantic-normal)' : 'var(--text-dim)';
  return `<div class="viz-tone"><div class="viz-tone-track"><div class="viz-tone-marker" style="left:${position.toFixed(1)}%;background:${color}"></div></div></div>`;
}

/**
 * Mini horizontal stacked bar chart. Takes array of {value, color, label?}.
 */
export function stackedBar(segments: Array<{value: number; color: string; label?: string}>, height = 8): string {
  const total = segments.reduce((s, seg) => s + seg.value, 0);
  if (total === 0) return '';
  const bars = segments.map(seg => {
    const pct = (seg.value / total) * 100;
    return `<div class="viz-stack-seg" style="width:${pct.toFixed(1)}%;background:${seg.color}" ${seg.label ? `title="${seg.label}: ${seg.value}"` : ''}></div>`;
  }).join('');
  return `<div class="viz-stacked-bar" style="height:${height}px">${bars}</div>`;
}
