export const DOMAIN = 'https://www.globalairoperations.com';
export const OG_IMAGE = `${DOMAIN}/assets/og-image.jpg`;

export const INSIGHT_CATEGORY_LABELS = {
  article: 'Article',
  blog: 'Blog Post',
  business: 'Business Highlight',
};

export const ARTICLE_CARD_IMAGES = {
  'retardant-is-not-just-for-airtankers-anymore':
    '/assets/publications/retardant-featured-card.jpg',
};

export function slugify(name) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

export function parseInsightDate(dateStr) {
  return new Date(dateStr);
}

/** Featured first (JSON order), then newest-first by date. */
export function sortInsightsEntries(entries) {
  const featured = entries.filter((e) => e.featured);
  const rest = entries
    .filter((e) => !e.featured)
    .sort((a, b) => parseInsightDate(b.date) - parseInsightDate(a.date));
  return [...featured, ...rest];
}

export function formatAuthors(authors) {
  if (!authors?.length) return '';
  if (authors.length === 1) return authors[0];
  if (authors.length === 2) return `${authors[0]} & ${authors[1]}`;
  return `${authors.slice(0, -1).join(', ')}, & ${authors[authors.length - 1]}`;
}

export function formatByline(authors) {
  const names = formatAuthors(authors);
  return names ? `By ${names}` : '';
}

export function getInsightTakeLabel(entry) {
  if (entry.type === 'watch' && entry.category === 'business') {
    return "Why we think it's worth a look:";
  }
  return 'Why we think it matters:';
}

export function buildTeamLd(team) {
  const graph = [
    {
      '@type': 'ProfessionalService',
      name: 'Global Air Operations Group',
      url: `${DOMAIN}/`,
      email: 'info@globalairoperations.com',
    },
    ...team.map((p) => ({
      '@type': 'Person',
      name: p.name,
      jobTitle: p.role,
      worksFor: {
        '@type': 'Organization',
        name: 'Global Air Operations Group',
      },
    })),
  ];
  return { '@context': 'https://schema.org', '@graph': graph };
}

export function getArticleCardImage(slug) {
  return ARTICLE_CARD_IMAGES[slug] ?? null;
}

export function getServiceHeroImage(svc) {
  return svc.card_bg_image ?? '/assets/services-hero.jpg';
}

export function getArticleHeroImage(pub) {
  return (
    getArticleCardImage(pub.slug) ??
    pub.thumbnail ??
    '/assets/publications/retardant-featured-card.jpg'
  );
}
