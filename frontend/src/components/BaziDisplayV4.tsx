import WuxingRadarChart from './WuxingRadarChart';

interface Pillar {
  name: string;
  gan: string;
  zhi: string;
}

interface BaziInfo {
  pillars: Pillar[];
  day_master: string;
  climate: string;
  favorable: string[];
  energy_scores: Record<string, number>;
}

interface DaYun {
  ganzhi: string;
  start_year: number;
  end_year: number;
  start_age: number;
}

interface BaziDisplayV4Props {
  bazi: BaziInfo;
  dayun: DaYun[];
}

// 五行颜色映射
const WUXING_COLORS: Record<string, string> = {
  '木': '#2ECC71',
  '火': '#E74C3C',
  '土': '#F39C12',
  '金': '#BDC3C7',
  '水': '#3498DB',
};

// 天干五行映射
const GAN_WUXING: Record<string, string> = {
  '甲': '木', '乙': '木',
  '丙': '火', '丁': '火',
  '戊': '土', '己': '土',
  '庚': '金', '辛': '金',
  '壬': '水', '癸': '水',
};

// 地支五行映射
const ZHI_WUXING: Record<string, string> = {
  '子': '水', '丑': '土', '寅': '木', '卯': '木',
  '辰': '土', '巳': '火', '午': '火', '未': '土',
  '申': '金', '酉': '金', '戌': '土', '亥': '水',
};

export default function BaziDisplayV4({ bazi, dayun }: BaziDisplayV4Props) {
  // 获取气候图标
  const getClimateIcon = (climate: string) => {
    switch (climate) {
      case '寒': return '❄️';
      case '燥': return '🔥';
      default: return '☯';
    }
  };

  return (
    <div className="space-y-6">
      {/* 命格信息 */}
      <div className="glass-card p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <span className="text-2xl">{getClimateIcon(bazi.climate)}</span>
          <div>
            <p className="text-gold font-medium">
              {bazi.climate === '寒' ? '寒命' : bazi.climate === '燥' ? '燥命' : '平命'}
            </p>
            <p className="text-rice/50 text-sm">日主: {bazi.day_master}</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-rice/70 text-sm">喜用神</p>
          <div className="flex gap-2 mt-1">
            {bazi.favorable.map((wx, i) => (
              <span
                key={i}
                className="px-2 py-1 rounded text-sm font-medium"
                style={{ 
                  backgroundColor: `${WUXING_COLORS[wx]}20`,
                  color: WUXING_COLORS[wx],
                  border: `1px solid ${WUXING_COLORS[wx]}40`
                }}
              >
                {wx}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* 四柱八字和五行雷达图 - 并排布局 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 四柱八字 - 占 2/3 */}
        <div className="lg:col-span-2 glass-card p-6">
          <h3 className="title-mystical text-lg mb-6 flex items-center gap-2">
            <span>四柱八字</span>
          </h3>
          <div className="flex justify-center gap-4 md:gap-6">
            {bazi.pillars.map((pillar, index) => {
              const ganWx = GAN_WUXING[pillar.gan];
              const zhiWx = ZHI_WUXING[pillar.zhi];
              return (
                <div 
                  key={index} 
                  className="pillar-card-v5 p-4 text-center"
                >
                  {/* 天干 */}
                  <div 
                    className="heavenly-stem-v5 mb-3"
                    style={{ 
                      background: `linear-gradient(180deg, ${WUXING_COLORS[ganWx]}CC 0%, ${WUXING_COLORS[ganWx]} 100%)`,
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                    }}
                  >
                    {pillar.gan}
                  </div>
                  {/* 分隔线 */}
                  <div className="w-8 h-px bg-gold/30 mx-auto my-2"></div>
                  {/* 地支 */}
                  <div 
                    className="earthly-branch-v5"
                    style={{ color: WUXING_COLORS[zhiWx] }}
                  >
                    {pillar.zhi}
                  </div>
                  {/* 柱名 */}
                  <div className="text-gold/60 text-xs mt-4 tracking-widest font-medium">
                    {pillar.name}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* 五行雷达图 - 占 1/3 */}
        <div className="glass-card p-6">
          <h3 className="title-mystical text-lg mb-2 flex items-center gap-2">
            <span>五行能量</span>
          </h3>
          <WuxingRadarChart 
            energyScores={bazi.energy_scores} 
            favorable={bazi.favorable}
          />
        </div>
      </div>

      {/* 大运 */}
      <div className="glass-card p-6">
        <h3 className="title-mystical text-lg mb-4">大运排盘</h3>
        <div className="flex gap-2 overflow-x-auto pb-2">
          {dayun.slice(0, 8).map((dy, index) => {
            const gan = dy.ganzhi[0];
            const zhi = dy.ganzhi[1];
            const ganWx = GAN_WUXING[gan];
            const zhiWx = ZHI_WUXING[zhi];
            
            return (
              <div 
                key={index}
                className="flex-shrink-0 text-center p-3 rounded-lg bg-ink-700/50 border border-gold/10 min-w-[80px] hover:border-gold/30 transition-all duration-300"
              >
                <div className="flex justify-center gap-1 mb-1">
                  <span style={{ color: WUXING_COLORS[ganWx] }}>{gan}</span>
                  <span style={{ color: WUXING_COLORS[zhiWx] }}>{zhi}</span>
                </div>
                <div className="text-rice/40 text-xs">
                  {dy.start_age}-{dy.start_age + 9}岁
                </div>
                <div className="text-rice/30 text-xs">
                  {dy.start_year}-{dy.end_year}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
