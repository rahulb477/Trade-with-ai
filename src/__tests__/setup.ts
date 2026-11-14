import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';

// Mock next/navigation for component tests
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => '/analyze',
  useSearchParams: () => new URLSearchParams(),
  useParams: () => ({ id: 'anl_test123' }),
}));
