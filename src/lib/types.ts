export type VerdictType = 'WAIT' | 'NO TRADE' | 'PAPER-TRADING SETUP READY';
export type LanguageType = 'english' | 'hinglish' | 'hindi';
export type ThemeType = 'dark' | 'midnight' | 'light';
export type AnalysisModeType = 'quick' | 'full';
export type MarketType = 'auto' | 'india' | 'us' | 'forex' | 'commodities' | 'crypto';

export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  bio: string;
  created_at: string;
  updated_at: string;
}

export interface UserSettings {
  language: LanguageType;
  theme: ThemeType;
  default_mode: AnalysisModeType;
  preferred_market: MarketType;
  timezone: string;
  save_history: boolean;
  share_anonymous_diagnostics: boolean;
  updated_at?: string;
}

export interface AnalysisStage {
  id: string;
  label: string;
  status: 'pending' | 'running' | 'completed' | 'partial' | 'skipped_unavailable' | 'failed';
  detail: string;
}

export interface FullReportSection {
  id: string;
  number: number;
  title: string;
  status: string;
  summary: string;
  details: string[];
}

export interface AnalysisRecord {
  id: string;
  user_id?: string;
  status: string;
  stage: string;
  stage_index: number;
  is_fictional_demo?: boolean;
  instrument: string;
  exchange: string;
  market: string;
  timeframe: string;
  mode: AnalysisModeType;
  language: LanguageType;
  screenshot_ref: string;
  screenshot_filename: string;
  screenshot_mime: string;
  screenshot_width: number;
  screenshot_height: number;
  screenshot_size_bytes: number;
  analysis_timestamp: string;
  data_timestamp: string;
  verdict: VerdictType;
  legacy_verdict: string;
  direction: string;
  wait_condition: string;
  entry_display: string;
  entry_status: string;
  stop_loss: string;
  stop_basis?: string;
  tp1: string;
  tp2: string;
  tp3: string;
  risk_reward: string;
  short_explanation: string;
  english_explanation?: string;
  hinglish_explanation: string;
  hindi_explanation: string;
  immutable_version?: number;
  snapshot_sha256?: string;
  persisted?: boolean;
  evidence?: Array<{ module: string; role: string }>;
  data_quality?: {
    quality_score: number;
    quality_max: number;
    consequence: string;
    missing_dimensions: string[];
    freshness: string;
    source_type: string;
    anti_fabrication_verified: boolean;
  };
  provider_info?: {
    vision: {
      configured: boolean;
      active_provider: string;
      model: string | null;
      mode_label: string;
    };
    vision_run?: {
      used: boolean;
      provider: string;
      error?: string;
    };
    market_data: {
      configured: boolean;
      provider: string | null;
      live_quotes_available: boolean;
      note: string;
    };
    news: {
      configured: boolean;
      provider: string | null;
      note: string;
    };
    ocr_available: boolean;
  };
  quick_payload?: {
    compact_text: string;
    rr_t1: number | null;
    rr_t2: number | null;
    rr_t3: number | null;
    net_rr_t1: number | null;
    net_rr_t2: number | null;
    net_rr_t3: number | null;
    tp1_basis: string;
    tp2_basis: string;
    tp3_basis: string;
    stop_basis: string;
    entry_confirmation: string;
    provenance: Record<string, string>;
    disclaimer: string;
  };
  full_report?: {
    legacy_verdict: string;
    sections: FullReportSection[];
    sizing_illustrative?: {
      paper_equity: number;
      risk_pct: number;
      units: number;
      risk_amount: number;
      notional: number;
      break_even_win_rate_t1_pct: number | null;
      note: string;
    } | null;
  };
  stages?: AnalysisStage[];
}

export interface WatchlistItem {
  id: string;
  symbol: string;
  exchange: string;
  market: string;
  notes: string;
  created_at: string;
  last_analysis: {
    id: string;
    verdict: VerdictType;
    timeframe: string;
    analysis_timestamp: string;
    entry_display: string;
    stop_loss: string;
    tp1: string;
  } | null;
  live_quote?: {
    available: boolean;
    last: number;
    change_pct: number;
    timestamp: string;
    source: string;
    freshness: string;
  };
}

export interface MarketGuide {
  id: string;
  name: string;
  venues: string[];
  session: string;
  settlement: string;
  key_instruments: string[];
  structural_rules: string[];
  doc_path: string;
  documented: boolean;
  word_count: number;
}

export interface NewsArticle {
  title: string;
  summary: string;
  source: string;
  published_at: string;
  url: string;
  market: string;
  instrument: string | null;
  relevance: string;
  freshness: string;
}

export interface SamplePreset {
  id: string;
  label: string;
  instrument: string;
  exchange: string;
  market: string;
  timeframe: string;
  is_fictional_demo: boolean;
}
