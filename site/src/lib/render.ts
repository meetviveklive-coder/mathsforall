/**
 * Build-time rendering of content text: a small, safe subset of Markdown plus KaTeX maths.
 * Content is AI-written, so all text is HTML-escaped; only the tags produced here are emitted.
 * KaTeX runs with throwOnError, so bad LaTeX fails the build instead of reaching a learner.
 */
import katex from 'katex';

const ESC: Record<string, string> = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
export const escapeHtml = (s: string) => s.replace(/[&<>"']/g, (c) => ESC[c]);

function inlineMarkdown(escaped: string): string {
  return escaped
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*(?!\s)(.+?)\*(?!\*)/g, '$1<em>$2</em>');
}

/** Render one line or paragraph: text with $...$ maths. */
export function renderInline(text: string): string {
  const parts = text.split(/(\$[^$]+\$)/g);
  return parts
    .map((part) => {
      if (part.length > 2 && part.startsWith('$') && part.endsWith('$')) {
        const tex = part.slice(1, -1);
        // Full-size fractions inline: small \frac text is hard for young readers.
        const display = /\\frac/.test(tex) ? `\\displaystyle ${tex}` : tex;
        return katex.renderToString(display, { throwOnError: true, output: 'htmlAndMathml' });
      }
      return inlineMarkdown(escapeHtml(part));
    })
    .join('');
}

/** Render a block of text: paragraphs separated by blank lines, "- " lists. */
export function renderBlock(text: string): string {
  return text
    .split(/\n\s*\n/)
    .map((block) => {
      const lines = block.split('\n').filter((l) => l.trim() !== '');
      if (lines.length && lines.every((l) => /^\s*-\s+/.test(l))) {
        return '<ul>' + lines.map((l) => `<li>${renderInline(l.replace(/^\s*-\s+/, ''))}</li>`).join('') + '</ul>';
      }
      return `<p>${lines.map(renderInline).join('<br>')}</p>`;
    })
    .join('');
}
