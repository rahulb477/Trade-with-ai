import type { Metadata } from 'next';
import './globals.css';
import { AppProvider } from '@/context/AppContext';

export const metadata: Metadata = {
  title: 'AI Trading Intelligence — Deep Market Intelligence. Simple Trading Insights.',
  description:
    'Upload a chart screenshot and receive concise, evidence-based technical research powered by the V1+V2+V3 AI Trading Intelligence engine.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme="dark" className="dark">
      <body className="min-h-screen font-sans antialiased">
        <AppProvider>{children}</AppProvider>
      </body>
    </html>
  );
}
