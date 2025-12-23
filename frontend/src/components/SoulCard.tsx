import React from 'react';

interface SoulInfo {
  gan: string;
  wuxing: string;
  image: string;
  icon: string;
  traits: string;
  description: string;
}

interface SoulCardProps {
  soul?: SoulInfo;
}

// 五行颜色映射
const WUXING_COLORS: Record<string, { bg: string; text: string; glow: string }> = {
  "木": { bg: "rgba(46, 204, 113, 0.15)", text: "#2ECC71", glow: "rgba(46, 204, 113, 0.3)" },
  "火": { bg: "rgba(231, 76, 60, 0.15)", text: "#E74C3C", glow: "rgba(231, 76, 60, 0.3)" },
  "土": { bg: "rgba(241, 196, 15, 0.15)", text: "#F1C40F", glow: "rgba(241, 196, 15, 0.3)" },
  "金": { bg: "rgba(212, 175, 55, 0.15)", text: "#D4AF37", glow: "rgba(212, 175, 55, 0.3)" },
  "水": { bg: "rgba(52, 152, 219, 0.15)", text: "#3498DB", glow: "rgba(52, 152, 219, 0.3)" },
};

const SoulCard: React.FC<SoulCardProps> = ({ soul }) => {
  if (!soul) return null;

  const colors = WUXING_COLORS[soul.wuxing] || WUXING_COLORS["金"];

  return (
    <div 
      className="relative bg-black/40 border border-[#d4af37]/30 rounded-xl p-6 backdrop-blur-md flex flex-col items-center text-center hover:border-[#d4af37]/60 transition-all duration-500 group overflow-hidden"
      style={{
        background: `linear-gradient(135deg, ${colors.bg} 0%, rgba(0,0,0,0.4) 100%)`,
      }}
    >
      {/* 背景光晕效果 */}
      <div 
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        style={{
          background: `radial-gradient(circle at 50% 30%, ${colors.glow} 0%, transparent 70%)`,
        }}
      />
      
      {/* Header */}
      <h3 className="relative text-[#d4af37] text-sm tracking-widest uppercase mb-4 opacity-80">
        本命元神
      </h3>
      
      {/* Huge Icon with Animation */}
      <div 
        className="relative text-7xl mb-4 transform group-hover:scale-110 transition-transform duration-500"
        style={{
          filter: `drop-shadow(0 0 20px ${colors.glow})`,
        }}
      >
        {soul.icon}
      </div>
      
      {/* Title */}
      <div className="relative flex items-center gap-2 mb-3">
        <span 
          className="text-3xl font-serif font-bold"
          style={{ color: colors.text }}
        >
          {soul.gan}{soul.wuxing}
        </span>
        <span className="text-[#d4af37] text-2xl">·</span>
        <span className="text-xl font-serif text-[#d4af37]">{soul.image}</span>
      </div>
      
      {/* Traits Badge */}
      <div 
        className="relative text-xs px-4 py-1.5 rounded-full mb-4 border"
        style={{
          backgroundColor: colors.bg,
          borderColor: `${colors.text}40`,
          color: colors.text,
        }}
      >
        {soul.traits}
      </div>
      
      {/* Description */}
      <p className="relative text-gray-300 text-sm font-light leading-relaxed max-w-xs">
        {soul.description}
      </p>
      
      {/* 底部装饰线 */}
      <div 
        className="absolute bottom-0 left-1/2 -translate-x-1/2 w-1/2 h-0.5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        style={{
          background: `linear-gradient(90deg, transparent, ${colors.text}, transparent)`,
        }}
      />
    </div>
  );
};

export default SoulCard;
