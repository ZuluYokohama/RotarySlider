import './globals.css';
import { GlobalCanvas } from '../components/GlobalCanvas';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div id="canvas-container">
          <GlobalCanvas />
        </div>
        <main className="relative z-10 w-full h-full pointer-events-auto">
          {children}
        </main>
      </body>
    </html>
  );
}
