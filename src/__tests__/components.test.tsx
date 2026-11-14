import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import {
  UploadCard,
  validateChartFile,
  AnalysisProgress,
} from '@/components/UploadComponents';
import {
  QuickSignalCard,
  FullAnalysisAccordion,
} from '@/components/SignalComponents';
import { VerdictBadge, EmptyState, ErrorState } from '@/components/StateViews';
import { SIDEBAR_ITEMS } from '@/components/AppShell';
import type { AnalysisRecord } from '@/lib/types';

describe('Image & Upload Validation', () => {
  it('accepts valid PNG, JPG, JPEG, and WEBP files within 10 MB', () => {
    expect(validateChartFile({ name: 'chart.png', size: 250_000, type: 'image/png' })).toBeNull();
    expect(validateChartFile({ name: 'nifty.jpg', size: 1_500_000, type: 'image/jpeg' })).toBeNull();
    expect(validateChartFile({ name: 'btc.webp', size: 900_000, type: 'image/webp' })).toBeNull();
  });

  it('rejects HEIC files with an explicit message', () => {
    const err = validateChartFile({ name: 'photo.heic', size: 500_000, type: 'image/heic' });
    expect(err).toContain('HEIC');
  });

  it('rejects oversized files exceeding maxUploadMb', () => {
    const err = validateChartFile(
      { name: 'huge.png', size: 12 * 1024 * 1024, type: 'image/png' },
      10
    );
    expect(err).toContain('maximum allowed upload size');
  });

  it('rejects empty 0-byte or unsupported format files', () => {
    expect(validateChartFile({ name: 'empty.png', size: 0, type: 'image/png' })).toContain('empty');
    expect(validateChartFile({ name: 'script.pdf', size: 1024, type: 'application/pdf' })).toContain('Unsupported');
  });

  it('renders UploadCard dropzone and displays validation error on unsupported file', () => {
    const onSelect = vi.fn();
    render(<UploadCard selected={null} onSelect={onSelect} onClear={vi.fn()} />);

    expect(screen.getByTestId('upload-dropzone')).toBeInTheDocument();
    const input = screen.getByTestId('chart-file-input') as HTMLInputElement;
    const badFile = new File(['bad'], 'unsupported.heic', { type: 'image/heic' });
    fireEvent.change(input, { target: { files: [badFile] } });

    expect(screen.getByTestId('upload-validation-error')).toHaveTextContent(/HEIC/i);
    expect(onSelect).not.toHaveBeenCalled();
  });
});

describe('Quick Signal Results & Full Analysis Components', () => {
  const sampleRecord: AnalysisRecord = {
    id: 'anl_demo1',
    status: 'completed',
    stage: 'completed',
    stage_index: 9,
    is_fictional_demo: true,
    instrument: 'BTCUSD',
    exchange: 'Bitstamp',
    market: 'crypto',
    timeframe: '5m',
    mode: 'quick',
    language: 'english',
    screenshot_ref: 'img_123',
    screenshot_filename: 'BTCUSD_5m.png',
    screenshot_mime: 'image/png',
    screenshot_width: 480,
    screenshot_height: 280,
    screenshot_size_bytes: 12400,
    analysis_timestamp: '2026-11-14T10:00:00+00:00',
    data_timestamp: '2026-11-14T10:00:00+00:00',
    verdict: 'WAIT',
    legacy_verdict: 'WAIT — NO CONFIRMED SETUP',
    direction: 'short',
    wait_condition: '5-minute candle closes below identified support (67,300).',
    entry_display: '67,300–67,400',
    entry_status: 'PENDING',
    stop_loss: '67,800',
    tp1: '66,950',
    tp2: '66,500',
    tp3: '66,200',
    risk_reward: 'T1 0.89 | T2 1.89 | T3 2.56',
    short_explanation: 'Wait for breakdown confirmation.',
    hinglish_explanation: 'Support break hua hai, lekin volume confirmation abhi nahi mili.',
    hindi_explanation: 'कन्फर्मेशन का इंतजार करें।',
    quick_payload: {
      compact_text: '',
      rr_t1: 0.89,
      rr_t2: 1.89,
      rr_t3: 2.56,
      net_rr_t1: 0.89,
      net_rr_t2: 1.89,
      net_rr_t3: 2.56,
      tp1_basis: 'prior swing',
      tp2_basis: 'next S/R',
      tp3_basis: 'extended structure',
      stop_basis: 'structural 67,800',
      entry_confirmation: 'Pending close',
      provenance: {},
      disclaimer: 'Educational only.',
    },
    full_report: {
      legacy_verdict: 'WAIT — NO CONFIRMED SETUP',
      sections: [
        {
          id: 'instrument_identification',
          number: 1,
          title: 'Instrument Identification',
          status: 'VERIFIED',
          summary: 'BTCUSD on Bitstamp (5m)',
          details: ['Crypto 24/7 venue'],
        },
        {
          id: 'risk_assessment',
          number: 19,
          title: 'Risk Assessment',
          status: 'VERIFIED',
          summary: 'Stop at 67,800',
          details: ['Paper sizing only'],
        },
      ],
    },
  };

  it('renders QuickSignalCard with Verdict, Entry, Stop Loss, TP1-TP3, R:R, and Hinglish', () => {
    const toggleFn = vi.fn();
    render(
      <QuickSignalCard
        analysis={sampleRecord}
        onToggleFullAnalysis={toggleFn}
        fullOpen={false}
      />
    );

    expect(screen.getByTestId('verdict-badge')).toHaveTextContent('VERDICT: WAIT');
    expect(screen.getByTestId('signal-entry')).toHaveTextContent('67,300–67,400');
    expect(screen.getByTestId('signal-stoploss')).toHaveTextContent('67,800');
    expect(screen.getByTestId('signal-tp1')).toHaveTextContent('66,950');
    expect(screen.getByTestId('signal-tp2')).toHaveTextContent('66,500');
    expect(screen.getByTestId('signal-tp3')).toHaveTextContent('66,200');
    expect(screen.getByTestId('signal-rr')).toHaveTextContent('T1 0.89 | T2 1.89 | T3 2.56');

    fireEvent.click(screen.getByTestId('view-full-analysis-btn'));
    expect(toggleFn).toHaveBeenCalledTimes(1);
  });

  it('renders FullAnalysisAccordion and toggles expandable sections', () => {
    render(
      <FullAnalysisAccordion
        sections={sampleRecord.full_report!.sections}
        legacyVerdict="WAIT — NO CONFIRMED SETUP"
      />
    );

    expect(screen.getByText('Instrument Identification')).toBeInTheDocument();
    expect(screen.getByText('BTCUSD on Bitstamp (5m)')).toBeInTheDocument();

    fireEvent.click(screen.getByText('Collapse All'));
    expect(screen.queryByText('BTCUSD on Bitstamp (5m)')).not.toBeInTheDocument();

    fireEvent.click(screen.getByText('Expand All'));
    expect(screen.getByText('BTCUSD on Bitstamp (5m)')).toBeInTheDocument();
  });

  it('renders VerdictBadge variants, AnalysisProgress, EmptyState, and ErrorState', () => {
    render(
      <div>
        <VerdictBadge verdict="PAPER-TRADING SETUP READY" />
        <VerdictBadge verdict="NO TRADE" />
        <AnalysisProgress
          activeStageIndex={1}
          stages={[
            { id: 's1', label: 'Reading chart screenshot', status: 'completed', detail: 'OK' },
            { id: 's2', label: 'Identifying instrument', status: 'running', detail: '' },
          ]}
        />
        <EmptyState title="Nothing here" description="Upload a chart" />
        <ErrorState message="Network timeout" />
      </div>
    );

    expect(screen.getByText('VERDICT: PAPER-TRADING SETUP READY')).toBeInTheDocument();
    expect(screen.getByText('VERDICT: NO TRADE')).toBeInTheDocument();
    expect(screen.getByText('Reading chart screenshot')).toBeInTheDocument();
    expect(screen.getByText('Nothing here')).toBeInTheDocument();
    expect(screen.getByText('Network timeout')).toBeInTheDocument();
  });

  it('defines all 8 required sidebar navigation routes', () => {
    const hrefs = SIDEBAR_ITEMS.map((i) => i.href);
    expect(hrefs).toEqual([
      '/dashboard',
      '/analyze',
      '/markets',
      '/watchlist',
      '/news',
      '/history',
      '/education',
      '/settings',
    ]);
  });
});
