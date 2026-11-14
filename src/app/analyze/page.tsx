'use client';

import React, { Suspense, useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  ChevronDown,
  ChevronRight,
  Info,
  Sparkles,
  Zap,
} from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import { EducationalDisclaimer, ErrorState } from '@/components/StateViews';
import {
  AnalysisProgress,
  SelectedChartFile,
  UploadCard,
} from '@/components/UploadComponents';
import { useApp } from '@/context/AppContext';
import { apiFetch } from '@/lib/api';
import type {
  AnalysisModeType,
  AnalysisRecord,
  AnalysisStage,
  LanguageType,
  MarketType,
  SamplePreset,
} from '@/lib/types';

const INITIAL_STAGES: AnalysisStage[] = [
  { id: 'read_screenshot', label: 'Reading chart screenshot', status: 'pending', detail: '' },
  { id: 'identify_instrument', label: 'Identifying instrument', status: 'pending', detail: '' },
  { id: 'detect_timeframe', label: 'Detecting timeframe', status: 'pending', detail: '' },
  { id: 'analyze_candles', label: 'Analyzing candlesticks', status: 'pending', detail: '' },
  { id: 'check_structure', label: 'Checking market structure', status: 'pending', detail: '' },
  { id: 'evaluate_indicators', label: 'Evaluating indicators', status: 'pending', detail: '' },
  { id: 'research_context', label: 'Researching market context', status: 'pending', detail: '' },
  { id: 'validate_scenarios', label: 'Validating hypothetical scenarios', status: 'pending', detail: '' },
  { id: 'prepare_report', label: 'Preparing final report', status: 'pending', detail: '' },
];

function AnalyzePageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { settings } = useApp();

  const [selectedChart, setSelectedChart] = useState<SelectedChartFile | null>(null);
  const [market, setMarket] = useState<MarketType>(settings.preferred_market || 'auto');
  const [timeframe, setTimeframe] = useState<string>('auto');
  const [mode, setMode] = useState<AnalysisModeType>(settings.default_mode || 'quick');
  const [language, setLanguage] = useState<LanguageType>(settings.language || 'english');

  // Optional chart level transcription panel (per SKILL.md §3 when no external AI Vision API key is set)
  const [showObservedInputs, setShowObservedInputs] = useState<boolean>(false);
  const [instrumentInput, setInstrumentInput] = useState<string>('');
  const [exchangeInput, setExchangeInput] = useState<string>('');
  const [directionInput, setDirectionInput] = useState<string>('');
  const [lastPriceInput, setLastPriceInput] = useState<string>('');
  const [entryLowInput, setEntryLowInput] = useState<string>('');
  const [entryHighInput, setEntryHighInput] = useState<string>('');
  const [supportInput, setSupportInput] = useState<string>('');
  const [resistanceInput, setResistanceInput] = useState<string>('');
  const [stopInput, setStopInput] = useState<string>('');
  const [targetsInput, setTargetsInput] = useState<string>('');
  const [atrInput, setAtrInput] = useState<string>('');
  const [candleStateInput, setCandleStateInput] = useState<string>('unknown');
  const [closeConfirmed, setCloseConfirmed] = useState<boolean>(false);
  const [volumeConfirmed, setVolumeConfirmed] = useState<boolean>(false);
  const [retestConfirmed, setRetestConfirmed] = useState<boolean>(false);

  // Presets & capabilities
  const [presets, setPresets] = useState<SamplePreset[]>([]);
  const [sampleDataUrl, setSampleDataUrl] = useState<string>('');
  const [activePresetId, setActivePresetId] = useState<string | null>(null);
  const [visionConfigured, setVisionConfigured] = useState<boolean>(false);
  const [visionLabel, setVisionLabel] = useState<string>('');

  // Processing state
  const [analyzing, setAnalyzing] = useState<boolean>(false);
  const [stages, setStages] = useState<AnalysisStage[]>(INITIAL_STAGES);
  const [stageIdx, setStageIdx] = useState<number>(0);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    setMarket(settings.preferred_market || 'auto');
    setMode(settings.default_mode || 'quick');
    setLanguage(settings.language || 'english');
  }, [settings.preferred_market, settings.default_mode, settings.language]);

  useEffect(() => {
    const sym = searchParams.get('symbol');
    if (sym) {
      setInstrumentInput(sym.toUpperCase());
      setShowObservedInputs(true);
    }
  }, [searchParams]);

  useEffect(() => {
    (async () => {
      try {
        const [healthRes, presetRes] = await Promise.all([
          apiFetch<{ capabilities: { vision: { configured: boolean; mode_label: string } } }>('/api/health'),
          apiFetch<{ presets: SamplePreset[]; sample_image: string }>('/api/presets'),
        ]);
        setVisionConfigured(Boolean(healthRes.capabilities?.vision?.configured));
        setVisionLabel(healthRes.capabilities?.vision?.mode_label || '');
        setPresets(presetRes.presets || []);
        setSampleDataUrl(presetRes.sample_image || '');

        const requestedPreset = searchParams.get('preset');
        if (requestedPreset && presetRes.presets?.some((p) => p.id === requestedPreset)) {
          const found = presetRes.presets.find((p) => p.id === requestedPreset)!;
          applySamplePreset(found, presetRes.sample_image);
        }
      } catch {
        // ignore preflight errors
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const applySamplePreset = (preset: SamplePreset, dataUrlOverride?: string) => {
    const url = dataUrlOverride || sampleDataUrl;
    if (!url) return;
    setActivePresetId(preset.id);
    setSubmitError(null);
    setSelectedChart({
      name: `${preset.instrument.replace(/\s+/g, '_')}_${preset.timeframe}_demo.png`,
      size: Math.round((url.length * 3) / 4),
      format: 'PNG',
      mimeType: 'image/png',
      dataUrl: url,
    });
  };

  const handleAnalyze = async () => {
    if (!selectedChart) {
      setSubmitError('Please upload a chart screenshot first.');
      return;
    }

    setSubmitError(null);
    setAnalyzing(true);
    setStages(INITIAL_STAGES);
    setStageIdx(0);

    try {
      const transcription: Record<string, any> = {};
      if (instrumentInput.trim()) transcription.instrument = instrumentInput.trim();
      if (exchangeInput.trim()) transcription.exchange = exchangeInput.trim();
      if (directionInput) transcription.direction = directionInput;
      if (lastPriceInput.trim()) transcription.last_price = Number(lastPriceInput);
      if (entryLowInput.trim() && entryHighInput.trim()) {
        transcription.entry_low = Number(entryLowInput);
        transcription.entry_high = Number(entryHighInput);
      } else if (entryLowInput.trim()) {
        transcription.entry_price = Number(entryLowInput);
      }
      if (supportInput.trim()) transcription.support_level = Number(supportInput);
      if (resistanceInput.trim()) transcription.resistance_level = Number(resistanceInput);
      if (stopInput.trim()) transcription.structural_stop = Number(stopInput);
      if (targetsInput.trim()) transcription.levels_for_targets = targetsInput;
      if (atrInput.trim()) transcription.atr = Number(atrInput);
      if (candleStateInput !== 'unknown') transcription.candle_state = candleStateInput;
      if (closeConfirmed) transcription.has_close_confirmation = true;
      if (volumeConfirmed) {
        transcription.volume_present = true;
        transcription.volume_confirmed = true;
      }
      if (retestConfirmed) transcription.retest_status = 'confirmed';

      // Start asynchronous job so we track real backend job stages
      const startRes = await apiFetch<{
        ok: boolean;
        job_id: string;
        status: string;
        analysis?: AnalysisRecord;
      }>('/api/analyze', {
        method: 'POST',
        body: JSON.stringify({
          image_base64: selectedChart.dataUrl,
          filename: selectedChart.name,
          sample_preset_id: activePresetId,
          async_job: true,
          preferences: {
            market,
            timeframe,
            mode,
            language,
          },
          transcription,
        }),
      });

      if (startRes.analysis?.id) {
        router.push(`/results/${startRes.analysis.id}${mode === 'full' ? '?view=full' : ''}`);
        return;
      }

      const jobId = startRes.job_id;
      let attempts = 0;
      const maxAttempts = 60; // 30 seconds max — never infinite loading

      while (attempts < maxAttempts) {
        attempts += 1;
        await new Promise((r) => setTimeout(r, 350));
        const jobRes = await apiFetch<{
          ok: boolean;
          job: {
            status: string;
            current_stage_index: number;
            stages: AnalysisStage[];
            analysis_id: string | null;
            error: string | null;
          };
        }>(`/api/jobs/${jobId}`);

        const job = jobRes.job;
        if (job.stages?.length) {
          setStages(job.stages);
        }
        setStageIdx(job.current_stage_index || 0);

        if (job.status === 'completed' && job.analysis_id) {
          router.push(`/results/${job.analysis_id}${mode === 'full' ? '?view=full' : ''}`);
          return;
        }
        if (job.status === 'failed') {
          throw new Error(job.error || 'Analysis job failed on the server.');
        }
      }

      throw new Error('Analysis timed out after 30 seconds. Please retry.');
    } catch (err: any) {
      setSubmitError(err?.message || 'Failed to analyze chart screenshot.');
      setAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="space-y-1.5">
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">
          AI Chart Analysis
        </h1>
        <p className="text-sm sm:text-base ti-text-muted">
          Upload your chart screenshot and get intelligent technical research.
        </p>
      </div>

      {/* Provider honesty banner */}
      {visionLabel && (
        <div className="rounded-xl border border-[#1F2E47] bg-[#101827] px-4 py-3 text-xs flex items-start gap-2.5">
          <Info className="h-4 w-4 text-[#667AFF] shrink-0 mt-0.5" />
          <div className="ti-text-muted leading-relaxed">
            <strong className="text-[#E8EDF7]">Active Engine Status:</strong> {visionLabel}.{' '}
            {!visionConfigured && (
              <span>
                In offline no-key mode, upload any chart and optionally enter visible price levels below (or pick an educational demo fixture) — the engine never invents unreadable prices.
              </span>
            )}
          </div>
        </div>
      )}

      {analyzing ? (
        <AnalysisProgress stages={stages} activeStageIndex={stageIdx} />
      ) : (
        <div className="ti-surface rounded-2xl p-5 sm:p-7 shadow-card space-y-6">
          {/* Upload Dropzone + Preview */}
          <UploadCard
            selected={selectedChart}
            onSelect={(chart) => {
              setActivePresetId(null);
              setSelectedChart(chart);
              setSubmitError(null);
            }}
            onClear={() => {
              setActivePresetId(null);
              setSelectedChart(null);
            }}
          />

          {/* Quick Educational Sample Fixtures */}
          {presets.length > 0 && (
            <div className="rounded-xl border border-[#1F2E47] bg-[#080D19]/50 p-3.5 space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold ti-text-muted">
                <Sparkles className="h-3.5 w-3.5 text-[#667AFF]" />
                <span>Or load an educational paper-trading sample fixture (labelled FICTIONAL):</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {presets.map((p) => (
                  <button
                    key={p.id}
                    type="button"
                    onClick={() => applySamplePreset(p)}
                    className={`px-3 py-1.5 rounded-lg border text-xs font-medium transition-colors ${
                      activePresetId === p.id
                        ? 'border-[#667AFF] bg-[#667AFF]/20 text-[#E8EDF7]'
                        : 'border-[#1F2E47] bg-[#111C2D] ti-text-muted hover:text-[#E8EDF7]'
                    }`}
                  >
                    {p.instrument} &middot; {p.timeframe} ({p.id.split('_').pop()?.toUpperCase()})
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Optional Analysis Preferences */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 pt-2 border-t border-[#1F2E47]">
            <div>
              <label htmlFor="pref-market" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Market (Optional)
              </label>
              <select
                id="pref-market"
                value={market}
                onChange={(e) => setMarket(e.target.value as MarketType)}
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2 text-sm"
              >
                <option value="auto">Auto Detect</option>
                <option value="india">Indian (NSE / BSE)</option>
                <option value="us">US (NYSE / NASDAQ)</option>
                <option value="forex">Forex</option>
                <option value="commodities">Commodities</option>
                <option value="crypto">Crypto</option>
              </select>
            </div>

            <div>
              <label htmlFor="pref-timeframe" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Timeframe (Optional)
              </label>
              <select
                id="pref-timeframe"
                value={timeframe}
                onChange={(e) => setTimeframe(e.target.value)}
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2 text-sm"
              >
                <option value="auto">Auto Detect</option>
                <option value="1m">1m</option>
                <option value="5m">5m</option>
                <option value="15m">15m</option>
                <option value="30m">30m</option>
                <option value="1H">1H</option>
                <option value="4H">4H</option>
                <option value="1D">1D</option>
                <option value="1W">1W</option>
              </select>
            </div>

            <div>
              <label htmlFor="pref-mode" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Analysis Mode
              </label>
              <select
                id="pref-mode"
                value={mode}
                onChange={(e) => setMode(e.target.value as AnalysisModeType)}
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2 text-sm"
              >
                <option value="quick">Quick Signal (Default)</option>
                <option value="full">Full 22-Section Report</option>
              </select>
            </div>

            <div>
              <label htmlFor="pref-language" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Language
              </label>
              <select
                id="pref-language"
                value={language}
                onChange={(e) => setLanguage(e.target.value as LanguageType)}
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2 text-sm"
              >
                <option value="english">English</option>
                <option value="hinglish">Hinglish</option>
                <option value="hindi">Hindi (हिंदी)</option>
              </select>
            </div>
          </div>

          {/* Expandable Optional Observed Chart Levels (SKILL.md §3 Transcription Support) */}
          <div className="rounded-xl border border-[#1F2E47] bg-[#101827]/70 overflow-hidden">
            <button
              type="button"
              onClick={() => setShowObservedInputs((v) => !v)}
              aria-expanded={showObservedInputs}
              className="w-full px-4 py-3 flex items-center justify-between text-left text-xs sm:text-sm font-medium hover:bg-[#1A273D]/40"
            >
              <span>
                Optional: Supply Visible Chart Levels for Exact R:R Calculation (Recommended in Offline Mode)
              </span>
              {showObservedInputs ? (
                <ChevronDown className="h-4 w-4 ti-text-muted" />
              ) : (
                <ChevronRight className="h-4 w-4 ti-text-muted" />
              )}
            </button>

            {showObservedInputs && (
              <div className="p-4 border-t border-[#1F2E47] grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div>
                  <label className="block ti-text-muted mb-1">Instrument Symbol</label>
                  <input
                    type="text"
                    value={instrumentInput}
                    onChange={(e) => setInstrumentInput(e.target.value)}
                    placeholder="e.g. BTCUSD, NIFTY 50"
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block ti-text-muted mb-1">Exchange / Venue</label>
                  <input
                    type="text"
                    value={exchangeInput}
                    onChange={(e) => setExchangeInput(e.target.value)}
                    placeholder="e.g. NSE, Bitstamp, NASDAQ"
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block ti-text-muted mb-1">Setup Direction</label>
                  <select
                    value={directionInput}
                    onChange={(e) => setDirectionInput(e.target.value)}
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  >
                    <option value="">Auto / Undecided</option>
                    <option value="long">Long (Bullish)</option>
                    <option value="short">Short (Bearish)</option>
                  </select>
                </div>

                <div>
                  <label className="block ti-text-muted mb-1">Last Price</label>
                  <input
                    type="number"
                    step="any"
                    value={lastPriceInput}
                    onChange={(e) => setLastPriceInput(e.target.value)}
                    placeholder="Visible current price"
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block ti-text-muted mb-1">Entry Price / Zone Low</label>
                  <input
                    type="number"
                    step="any"
                    value={entryLowInput}
                    onChange={(e) => setEntryLowInput(e.target.value)}
                    placeholder="e.g. 67300"
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block ti-text-muted mb-1">Entry Zone High (Optional)</label>
                  <input
                    type="number"
                    step="any"
                    value={entryHighInput}
                    onChange={(e) => setEntryHighInput(e.target.value)}
                    placeholder="e.g. 67400"
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  />
                </div>

                <div>
                  <label className="block ti-text-muted mb-1">Structural Stop Loss</label>
                  <input
                    type="number"
                    step="any"
                    value={stopInput}
                    onChange={(e) => setStopInput(e.target.value)}
                    placeholder="Invalidation price"
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block ti-text-muted mb-1">Support Level</label>
                  <input
                    type="number"
                    step="any"
                    value={supportInput}
                    onChange={(e) => setSupportInput(e.target.value)}
                    placeholder="Nearest support"
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block ti-text-muted mb-1">Resistance Level</label>
                  <input
                    type="number"
                    step="any"
                    value={resistanceInput}
                    onChange={(e) => setResistanceInput(e.target.value)}
                    placeholder="Nearest resistance"
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block ti-text-muted mb-1">
                    Structural Target Levels (comma-separated for TP1, TP2, TP3)
                  </label>
                  <input
                    type="text"
                    value={targetsInput}
                    onChange={(e) => setTargetsInput(e.target.value)}
                    placeholder="e.g. 66950, 66500, 66200"
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block ti-text-muted mb-1">Visible ATR (Optional)</label>
                  <input
                    type="number"
                    step="any"
                    value={atrInput}
                    onChange={(e) => setAtrInput(e.target.value)}
                    placeholder="e.g. 80"
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  />
                </div>

                <div>
                  <label className="block ti-text-muted mb-1">Candle State</label>
                  <select
                    value={candleStateInput}
                    onChange={(e) => setCandleStateInput(e.target.value)}
                    className="w-full rounded-lg border border-[#1F2E47] bg-[#080D19] px-3 py-2"
                  >
                    <option value="unknown">Auto / Unknown</option>
                    <option value="forming">Candle Still Forming</option>
                    <option value="unconfirmed_breakout">Unconfirmed Breakout</option>
                    <option value="confirmed_breakout">Confirmed Breakout</option>
                    <option value="unconfirmed_breakdown">Unconfirmed Breakdown</option>
                    <option value="confirmed_breakdown">Confirmed Breakdown</option>
                    <option value="failed_breakout">Failed Breakout (Trap)</option>
                  </select>
                </div>

                <div className="sm:col-span-2 flex flex-wrap items-center gap-4 pt-4">
                  <label className="inline-flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={closeConfirmed}
                      onChange={(e) => setCloseConfirmed(e.target.checked)}
                    />
                    <span>Candle Close Confirmed</span>
                  </label>
                  <label className="inline-flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={volumeConfirmed}
                      onChange={(e) => setVolumeConfirmed(e.target.checked)}
                    />
                    <span>Volume Confirmed</span>
                  </label>
                  <label className="inline-flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={retestConfirmed}
                      onChange={(e) => setRetestConfirmed(e.target.checked)}
                    />
                    <span>Retest Hold Confirmed</span>
                  </label>
                </div>
              </div>
            )}
          </div>

          {submitError && <ErrorState message={submitError} />}

          {/* Prominent ANALYZE CHART Button */}
          <button
            type="button"
            disabled={!selectedChart || analyzing}
            onClick={handleAnalyze}
            data-testid="analyze-chart-btn"
            className="w-full py-4 px-6 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] disabled:opacity-45 disabled:cursor-not-allowed text-white font-bold text-sm sm:text-base tracking-wide flex items-center justify-center gap-2.5 shadow-lg transition-colors"
          >
            <Zap className="h-5 w-5" />
            <span>ANALYZE CHART</span>
          </button>
        </div>
      )}

      <EducationalDisclaimer />
    </div>
  );
}

export default function AnalyzePage() {
  return (
    <AppShell requireAuth>
      <Suspense fallback={<div className="ti-surface rounded-xl p-6 text-sm">Loading analyzer…</div>}>
        <AnalyzePageContent />
      </Suspense>
    </AppShell>
  );
}
