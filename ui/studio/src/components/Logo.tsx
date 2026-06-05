export function Logo({ className = "" }: { className?: string }) {
  return (
    <svg 
      className={className} 
      viewBox="0 0 400 400" 
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
    >
      <rect width="400" height="400" fill="transparent"/>
      {/* Abstract Geometric Wolf Head Vector Lines */}
      <polyline points="200,80 140,160 160,260 200,320 240,260 260,160 200,80" stroke="#58a6ff" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round"/>
      <polyline points="140,160 200,220 260,160" stroke="#58a6ff" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round"/>
      <line x1="200" y1="80" x2="200" y2="220" stroke="#58a6ff" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round"/>
      {/* Eyes */}
      <circle cx="170" cy="180" r="8" fill="#3fb950"/>
      <circle cx="230" cy="180" r="8" fill="#3fb950"/>
    </svg>
  );
}
