import { Panel } from './Panel';
import { t } from '@/services/i18n';
import { escapeHtml } from '@/utils/sanitize';

export class CreditsPanel extends Panel {
  constructor() {
    super({
      id: 'credits',
      title: t('panels.credits') || 'Credits',
    });
    this.render();
  }

  private render(): void {
    const html = `
      <div class="credits-content" style="padding: 12px; line-height: 1.7; font-size: 0.95rem;">
        <div style="margin-bottom: 16px;">
          <strong>${escapeHtml(t('magen.credits.basedOn') || 'Based on')}</strong><br>
          <a href="https://github.com/koala73/worldmonitor" target="_blank" rel="noopener"
             style="color: var(--magen-accent, #00a6ff); text-decoration: none;">
            World Monitor
          </a>
          ${escapeHtml(t('magen.credits.by') || 'by')} Elie Habib
        </div>

        <div style="margin-bottom: 16px;">
          <strong>${escapeHtml(t('magen.credits.visualInspiration') || 'Visual inspiration')}</strong><br>
          <a href="https://github.com/kevtoe/worldview" target="_blank" rel="noopener"
             style="color: var(--magen-accent, #00a6ff); text-decoration: none;">
            WorldView
          </a>
          ${escapeHtml(t('magen.credits.by') || 'by')} kevtoe
        </div>

        <div style="margin-bottom: 16px;">
          <strong>${escapeHtml(t('magen.credits.license') || 'License')}</strong><br>
          <a href="https://www.gnu.org/licenses/agpl-3.0.html" target="_blank" rel="noopener"
             style="color: var(--magen-accent, #00a6ff); text-decoration: none;">
            AGPL v3
          </a>
          &mdash;
          <a href="https://github.com/magen-app/magen" target="_blank" rel="noopener"
             style="color: var(--magen-accent, #00a6ff); text-decoration: none;">
            ${escapeHtml(t('magen.credits.sourceCode') || 'Source Code')}
          </a>
        </div>

        <div style="color: var(--magen-text-secondary, #8899aa); font-size: 0.85rem; margin-top: 20px; padding-top: 12px; border-top: 1px solid var(--magen-border, #2a3544);">
          ${escapeHtml(t('magen.credits.builtWithLove') || 'Built with love for Israeli citizens.')}
        </div>
      </div>
    `;
    this.setContent(html);
  }
}
