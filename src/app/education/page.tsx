'use client';

import React, { Suspense, useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { BookOpen, FileText, Search } from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import {
  EducationalDisclaimer,
  ErrorState,
  LoadingState,
} from '@/components/StateViews';
import { apiFetch } from '@/lib/api';

interface TopicMeta {
  slug: string;
  title: string;
  summary: string;
  path: string;
}

interface DomainCatalog {
  domain: string;
  label: string;
  description: string;
  count: number;
  topics: TopicMeta[];
}

interface KnowledgeArticle {
  domain: string;
  slug: string;
  title: string;
  summary: string;
  path: string;
  markdown: string;
}

function EducationContent() {
  const searchParams = useSearchParams();
  const [catalog, setCatalog] = useState<DomainCatalog[]>([]);
  const [activeDomain, setActiveDomain] = useState<string>('candlesticks');
  const [searchQuery, setSearchQuery] = useState<string>(searchParams.get('q') || '');
  const [article, setArticle] = useState<KnowledgeArticle | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [articleLoading, setArticleLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const q = searchParams.get('q');
    if (q !== null) setSearchQuery(q);
  }, [searchParams]);

  const loadCatalog = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch<{ catalog: DomainCatalog[] }>('/api/education');
      setCatalog(res.catalog || []);
      if (res.catalog?.length && res.catalog[0].topics.length) {
        await openArticle(res.catalog[0].domain, res.catalog[0].topics[0].slug);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to load knowledge repository.');
    } finally {
      setLoading(false);
    }
  };

  const openArticle = async (domain: string, slug: string) => {
    setArticleLoading(true);
    setActiveDomain(domain);
    try {
      const res = await apiFetch<{ article: KnowledgeArticle }>(
        `/api/education?domain=${encodeURIComponent(domain)}&slug=${encodeURIComponent(slug)}`
      );
      setArticle(res.article);
    } catch (err: any) {
      setError(err?.message || 'Could not load module markdown.');
    } finally {
      setArticleLoading(false);
    }
  };

  useEffect(() => {
    void loadCatalog();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const qLower = searchQuery.trim().toLowerCase();
  const filteredDomains = catalog
    .map((dom) => {
      if (!qLower) return dom;
      const matchingTopics = dom.topics.filter(
        (t) =>
          t.title.toLowerCase().includes(qLower) ||
          t.summary.toLowerCase().includes(qLower) ||
          t.slug.toLowerCase().includes(qLower)
      );
      return { ...dom, topics: matchingTopics };
    })
    .filter((dom) => (qLower ? dom.topics.length > 0 : true));

  const currentDomainObj =
    filteredDomains.find((d) => d.domain === activeDomain) || filteredDomains[0];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight flex items-center gap-2.5">
            <BookOpen className="h-7 w-7 text-[#667AFF]" />
            <span>Trading Intelligence Learning Center</span>
          </h1>
          <p className="text-sm ti-text-muted mt-1">
            Browse all 119+ documented V1–V3 modules directly from <code className="font-mono">knowledge/</code> (candlesticks, indicators, SMC, risk, Hinglish lessons).
          </p>
        </div>
        <div className="relative w-full sm:w-72">
          <Search className="h-4 w-4 ti-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Filter 119+ modules…"
            aria-label="Filter knowledge modules"
            className="w-full rounded-xl border border-[#1F2E47] bg-[#111C2D] pl-9 pr-3 py-2 text-sm"
          />
        </div>
      </div>

      {error && <ErrorState message={error} onRetry={loadCatalog} />}
      {loading ? (
        <LoadingState label="Indexing knowledge repository…" rows={5} />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Domain & Topic Browser */}
          <aside className="lg:col-span-4 space-y-4">
            <div className="flex flex-wrap gap-1.5">
              {filteredDomains.map((dom) => (
                <button
                  key={dom.domain}
                  type="button"
                  onClick={() => setActiveDomain(dom.domain)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                    currentDomainObj?.domain === dom.domain
                      ? 'bg-[#667AFF] text-white border-[#667AFF]'
                      : 'bg-[#111C2D] border-[#1F2E47] ti-text-muted hover:text-[#E8EDF7]'
                  }`}
                >
                  {dom.label} ({dom.topics.length})
                </button>
              ))}
            </div>

            {currentDomainObj && (
              <div className="ti-surface rounded-2xl p-3 max-h-[540px] overflow-y-auto space-y-1">
                {currentDomainObj.topics.map((topic) => {
                  const selected =
                    article?.domain === currentDomainObj.domain &&
                    article?.slug === topic.slug;
                  return (
                    <button
                      key={topic.slug}
                      type="button"
                      onClick={() => void openArticle(currentDomainObj.domain, topic.slug)}
                      className={`w-full text-left rounded-xl px-3 py-2.5 text-xs transition-colors ${
                        selected
                          ? 'bg-[#667AFF]/20 border border-[#667AFF]/40 text-[#E8EDF7]'
                          : 'hover:bg-[#1A273D]/50 ti-text-muted'
                      }`}
                    >
                      <p className="font-semibold text-[#E8EDF7] flex items-center gap-1.5">
                        <FileText className="h-3.5 w-3.5 text-[#667AFF] shrink-0" />
                        <span className="truncate">{topic.title}</span>
                      </p>
                      <p className="mt-0.5 line-clamp-2 text-[11px] ti-text-muted">
                        {topic.summary}
                      </p>
                    </button>
                  );
                })}
              </div>
            )}
          </aside>

          {/* Markdown Module Reader */}
          <section className="lg:col-span-8">
            {articleLoading ? (
              <LoadingState label="Opening module…" rows={6} />
            ) : article ? (
              <article className="ti-surface rounded-2xl p-5 sm:p-7 space-y-4">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#1F2E47] pb-3">
                  <div>
                    <h2 className="text-lg sm:text-xl font-bold">{article.title}</h2>
                    <p className="text-xs font-mono ti-text-muted mt-0.5">
                      Source file: {article.path}
                    </p>
                  </div>
                </div>
                <pre className="whitespace-pre-wrap font-sans text-xs sm:text-sm leading-relaxed text-[#E8EDF7]/95 overflow-x-auto">
                  {article.markdown}
                </pre>
              </article>
            ) : (
              <div className="ti-surface rounded-2xl p-8 text-center text-sm ti-text-muted">
                Select any module on the left to read its complete specification.
              </div>
            )}
          </section>
        </div>
      )}

      <EducationalDisclaimer />
    </div>
  );
}

export default function EducationPage() {
  return (
    <AppShell>
      <Suspense fallback={<div className="p-6 text-sm">Loading Learning Center…</div>}>
        <EducationContent />
      </Suspense>
    </AppShell>
  );
}
