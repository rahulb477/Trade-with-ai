'use client';

import React, { useRef, useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  Circle,
  Clock,
  FileImage,
  Loader2,
  RefreshCw,
  Trash2,
  UploadCloud,
} from 'lucide-react';
import { formatBytes } from '@/lib/api';
import type { AnalysisStage } from '@/lib/types';

export interface SelectedChartFile {
  file?: File;
  name: string;
  size: number;
  format: string;
  mimeType: string;
  dataUrl: string;
}

const ACCEPTED_MIME_TYPES = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
const ACCEPTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp'];

export function validateChartFile(
  file: Pick<File, 'name' | 'size' | 'type'>,
  maxUploadMb = 10
): string | null {
  const lowerName = (file.name || '').toLowerCase();
  const mime = (file.type || '').toLowerCase();

  if (
    mime.includes('heic') ||
    mime.includes('heif') ||
    lowerName.endsWith('.heic') ||
    lowerName.endsWith('.heif')
  ) {
    return 'HEIC/HEIF images are not supported by the current server decoder. Please upload PNG, JPG, JPEG, or WEBP.';
  }

  const extAllowed = ACCEPTED_EXTENSIONS.some((ext) => lowerName.endsWith(ext));
  const mimeAllowed = ACCEPTED_MIME_TYPES.includes(mime);

  if (!mimeAllowed && !extAllowed) {
    return 'Unsupported image format. Please select a PNG, JPG, JPEG, or WEBP chart screenshot.';
  }

  if (file.size <= 0) {
    return 'Selected image file is empty (0 bytes).';
  }

  const maxBytes = maxUploadMb * 1024 * 1024;
  if (file.size > maxBytes) {
    return `Image exceeds the maximum allowed upload size of ${maxUploadMb} MB (${formatBytes(file.size)}).`;
  }

  return null;
}

export function ImagePreview({
  selected,
  onRemove,
  onReplaceClick,
}: {
  selected: SelectedChartFile;
  onRemove: () => void;
  onReplaceClick: () => void;
}) {
  return (
    <div className="space-y-3" data-testid="image-preview">
      <div className="relative rounded-xl overflow-hidden border border-[#1F2E47] bg-[#080D19] flex items-center justify-center max-h-[360px]">
        <img
          src={selected.dataUrl}
          alt={`Selected chart preview: ${selected.name}`}
          className="max-h-[340px] w-auto object-contain"
        />
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-[#1F2E47] bg-[#101827] px-3.5 py-2.5 text-xs">
        <div className="flex items-center gap-2.5 min-w-0">
          <FileImage className="h-4 w-4 text-[#667AFF] shrink-0" />
          <div className="min-w-0">
            <p className="font-semibold truncate text-[#E8EDF7]">{selected.name}</p>
            <p className="ti-text-muted">
              {selected.format.toUpperCase()} &middot; {formatBytes(selected.size)}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={onReplaceClick}
            className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-[#1F2E47] hover:border-[#667AFF] font-medium transition-colors"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            <span>Replace</span>
          </button>
          <button
            type="button"
            onClick={onRemove}
            className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-[#F16F83]/40 text-[#F16F83] hover:bg-[#F16F83]/15 font-medium transition-colors"
          >
            <Trash2 className="h-3.5 w-3.5" />
            <span>Remove</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export function UploadCard({
  selected,
  onSelect,
  onClear,
  maxUploadMb = 10,
  uploadProgress = 0,
}: {
  selected: SelectedChartFile | null;
  onSelect: (chart: SelectedChartFile) => void;
  onClear: () => void;
  maxUploadMb?: number;
  uploadProgress?: number;
}) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [readingProgress, setReadingProgress] = useState<number>(0);

  const handleFileObject = (file: File) => {
    setValidationError(null);
    const err = validateChartFile(file, maxUploadMb);
    if (err) {
      setValidationError(err);
      return;
    }

    const reader = new FileReader();
    reader.onprogress = (ev) => {
      if (ev.lengthComputable) {
        setReadingProgress(Math.round((ev.loaded / ev.total) * 100));
      }
    };
    reader.onload = () => {
      setReadingProgress(100);
      const dataUrl = String(reader.result || '');
      const ext =
        file.name.split('.').pop()?.toUpperCase() ||
        file.type.replace('image/', '').toUpperCase() ||
        'PNG';
      onSelect({
        file,
        name: file.name,
        size: file.size,
        format: ext === 'JPG' ? 'JPEG' : ext,
        mimeType: file.type || 'image/png',
        dataUrl,
      });
      setTimeout(() => setReadingProgress(0), 300);
    };
    reader.onerror = () => {
      setValidationError('Could not read the selected image file. Please try another screenshot.');
      setReadingProgress(0);
    };
    reader.readAsDataURL(file);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) handleFileObject(f);
    e.target.value = '';
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const f = e.dataTransfer.files?.[0];
    if (f) handleFileObject(f);
  };

  const activeProgress = uploadProgress > 0 ? uploadProgress : readingProgress;

  return (
    <div className="space-y-3">
      <input
        ref={inputRef}
        type="file"
        accept="image/png,image/jpeg,image/webp"
        onChange={handleInputChange}
        aria-label="Upload chart screenshot"
        data-testid="chart-file-input"
        className="hidden"
      />

      {!selected ? (
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragActive(true);
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              inputRef.current?.click();
            }
          }}
          role="button"
          tabIndex={0}
          data-testid="upload-dropzone"
          className={`rounded-2xl border-2 border-dashed p-8 sm:p-12 text-center cursor-pointer transition-colors ${
            dragActive
              ? 'border-[#667AFF] bg-[#667AFF]/10'
              : 'border-[#24344E] hover:border-[#667AFF]/70 bg-[#080D19]/50'
          }`}
        >
          <div className="h-14 w-14 rounded-2xl bg-[#667AFF]/15 border border-[#667AFF]/30 flex items-center justify-center text-[#667AFF] mx-auto mb-4">
            <UploadCloud className="h-7 w-7" />
          </div>
          <p className="text-base sm:text-lg font-semibold">
            Drag &amp; drop your chart screenshot, or click to browse
          </p>
          <p className="text-xs sm:text-sm ti-text-muted mt-1.5">
            Supports PNG, JPG, JPEG, WEBP &middot; Mobile gallery upload supported &middot; Up to {maxUploadMb} MB
          </p>
        </div>
      ) : (
        <ImagePreview
          selected={selected}
          onRemove={() => {
            setValidationError(null);
            onClear();
          }}
          onReplaceClick={() => inputRef.current?.click()}
        />
      )}

      {activeProgress > 0 && activeProgress < 100 && (
        <div className="space-y-1">
          <div className="flex justify-between text-xs ti-text-muted">
            <span>Processing image upload…</span>
            <span>{activeProgress}%</span>
          </div>
          <div className="h-1.5 w-full rounded-full bg-[#1A273D] overflow-hidden">
            <div
              className="h-full bg-[#667AFF] transition-all duration-200"
              style={{ width: `${activeProgress}%` }}
            />
          </div>
        </div>
      )}

      {validationError && (
        <div
          role="alert"
          data-testid="upload-validation-error"
          className="flex items-start gap-2.5 rounded-xl border border-[#F16F83]/40 bg-[#F16F83]/10 px-3.5 py-2.5 text-xs text-[#F16F83]"
        >
          <AlertTriangle className="h-4 w-4 shrink-0 mt-0.5" />
          <span>{validationError}</span>
        </div>
      )}
    </div>
  );
}

export function AnalysisProgress({
  stages,
  activeStageIndex,
}: {
  stages: AnalysisStage[];
  activeStageIndex: number;
}) {
  return (
    <div
      data-testid="analysis-progress"
      className="ti-surface rounded-2xl p-5 sm:p-6 space-y-4"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <Loader2 className="h-5 w-5 text-[#667AFF] animate-spin" />
          <h3 className="font-semibold text-sm sm:text-base">
            Running V1–V3 Trading Intelligence Pipeline
          </h3>
        </div>
        <span className="text-xs font-mono ti-text-muted">
          Stage {Math.min(stages.length, activeStageIndex + 1)}/{stages.length}
        </span>
      </div>

      <div className="space-y-2">
        {stages.map((st, idx) => {
          let Icon = Circle;
          let color = 'ti-text-muted';
          if (st.status === 'completed') {
            Icon = CheckCircle2;
            color = 'text-[#16B995]';
          } else if (st.status === 'partial' || st.status === 'skipped_unavailable') {
            Icon = Clock;
            color = 'text-[#F5B841]';
          } else if (idx === activeStageIndex || st.status === 'running') {
            Icon = Loader2;
            color = 'text-[#667AFF] animate-spin';
          }

          return (
            <div
              key={st.id}
              className="flex items-start justify-between gap-3 rounded-lg bg-[#080D19]/50 border border-[#1F2E47]/70 px-3 py-2 text-xs"
            >
              <div className="flex items-start gap-2.5 min-w-0">
                <Icon className={`h-4 w-4 shrink-0 mt-0.5 ${color}`} />
                <div className="min-w-0">
                  <p className="font-medium text-[#E8EDF7]">{st.label}</p>
                  {st.detail && (
                    <p className="ti-text-muted mt-0.5 break-words">{st.detail}</p>
                  )}
                </div>
              </div>
              <span className="uppercase text-[10px] font-mono ti-text-muted shrink-0">
                {st.status === 'skipped_unavailable' ? 'unavailable' : st.status}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
