import { Panel } from './Panel';
import { getCSSColor } from '@/utils';
import { calculateCII, type CountryScore } from '@/services/country-instability';
import { t } from '../services/i18n';
import { h, replaceChildren, rawHtml } from '@/utils/dom-utils';
import { arcGauge } from '@/utils/sparkline';

export class CIIPanel extends Panel {
  private scores: CountryScore[] = [];
  private focalPointsReady = false;
  private onShareStory?: (code: string, name: string) => void;

  constructor() {
    super({
      id: 'cii',
      title: t('panels.cii'),
      infoTooltip: t('components.cii.infoTooltip'),
    });
    this.showLoading(t('common.loading'));
  }

  public setShareStoryHandler(handler: (code: string, name: string) => void): void {
    this.onShareStory = handler;
  }

  private getLevelColor(level: CountryScore['level']): string {
    switch (level) {
      case 'critical': return getCSSColor('--semantic-critical');
      case 'high': return getCSSColor('--semantic-high');
      case 'elevated': return getCSSColor('--semantic-elevated');
      case 'normal': return getCSSColor('--semantic-normal');
      case 'low': return getCSSColor('--semantic-low');
    }
  }

  // Kept for potential future use but currently unused with arc gauge
  // private getLevelEmoji(level: CountryScore['level']): string { ... }

  private static readonly SHARE_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v7a2 2 0 002 2h12a2 2 0 002-2v-7"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>';

  private buildTrendArrow(trend: CountryScore['trend'], change: number): HTMLElement {
    if (trend === 'rising') return h('span', { className: 'trend-up' }, `↑${change > 0 ? change : ''}`);
    if (trend === 'falling') return h('span', { className: 'trend-down' }, `↓${Math.abs(change)}`);
    return h('span', { className: 'trend-stable' }, '→');
  }

  private getComponentColor(component: string, value: number): string {
    // Higher values = more severe. Color by value intensity.
    if (value >= 70) return getCSSColor('--semantic-critical');
    if (value >= 45) return getCSSColor('--semantic-high');
    if (value >= 25) return getCSSColor('--semantic-elevated');
    // Color hint by component type for low values
    switch (component) {
      case 'unrest': return getCSSColor('--semantic-high');
      case 'conflict': return getCSSColor('--semantic-critical');
      case 'security': return getCSSColor('--semantic-info');
      case 'information': return getCSSColor('--semantic-elevated');
      default: return getCSSColor('--text-dim');
    }
  }

  private buildComponentBars(components: CountryScore['components']): HTMLElement {
    const entries: Array<{ key: string; label: string; value: number }> = [
      { key: 'unrest', label: 'U', value: components.unrest },
      { key: 'conflict', label: 'C', value: components.conflict },
      { key: 'security', label: 'S', value: components.security },
      { key: 'information', label: 'I', value: components.information },
    ];

    const rows = entries.map(({ key, label, value }) => {
      const color = this.getComponentColor(key, value);
      const pct = Math.min(100, Math.max(0, value));
      return h('div', { className: 'cii-component-row' },
        h('span', { className: 'cii-component-label', title: t(`common.${key}`) }, label),
        h('div', { className: 'cii-component-bar' },
          h('div', { className: 'cii-component-fill', style: `width:${pct}%;background:${color}` }),
        ),
        h('span', { className: 'cii-component-val', style: `color:${color}` }, String(value)),
      );
    });

    return h('div', { className: 'cii-component-bars' }, ...rows);
  }

  private buildCountry(country: CountryScore): HTMLElement {
    const color = this.getLevelColor(country.level);

    const shareBtn = h('button', {
      className: 'cii-share-btn',
      dataset: { code: country.code, name: country.name },
      title: t('common.shareStory'),
    });
    shareBtn.appendChild(rawHtml(CIIPanel.SHARE_SVG));

    // Arc gauge for overall score
    const arcHtml = arcGauge(country.score, 100, color, 44);

    return h('div', { className: 'cii-country', dataset: { code: country.code }, style: `border-left: 3px solid ${color}` },
      h('div', { className: 'cii-hero-row' },
        rawHtml(arcHtml),
        h('div', { className: 'cii-hero-info' },
          h('div', { className: 'cii-hero-name' }, country.name),
          h('div', { className: 'cii-hero-trend' },
            this.buildTrendArrow(country.trend, country.change24h),
            shareBtn,
          ),
        ),
      ),
      this.buildComponentBars(country.components),
    );
  }

  private bindShareButtons(): void {
    if (!this.onShareStory) return;
    this.content.querySelectorAll('.cii-share-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const el = e.currentTarget as HTMLElement;
        const code = el.dataset.code || '';
        const name = el.dataset.name || '';
        if (code && name) this.onShareStory!(code, name);
      });
    });
  }

  public async refresh(forceLocal = false): Promise<void> {
    if (!this.focalPointsReady && !forceLocal) {
      return;
    }

    if (forceLocal) {
      this.focalPointsReady = true;
      console.log('[CIIPanel] Focal points ready, calculating scores...');
    }

    this.showSkeleton(8);

    try {
      const localScores = calculateCII();
      const localWithData = localScores.filter(s => s.score > 0).length;
      this.scores = localScores;
      console.log(`[CIIPanel] Calculated ${localWithData} countries with focal point intelligence`);

      const withData = this.scores.filter(s => s.score > 0);
      this.setCount(withData.length);

      if (withData.length === 0) {
        replaceChildren(this.content, h('div', { className: 'empty-state' }, t('components.cii.noSignals')));
        return;
      }

      const listEl = h('div', { className: 'cii-list' }, ...withData.map(s => this.buildCountry(s)));
      replaceChildren(this.content, listEl);
      this.bindShareButtons();
    } catch (error) {
      console.error('[CIIPanel] Refresh error:', error);
      this.showError(t('common.failedCII'));
    }
  }

  public getScores(): CountryScore[] {
    return this.scores;
  }
}
