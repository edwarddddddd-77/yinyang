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

interface BaziDisplayV5Props {
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

// 日主强弱判断
const getDayMasterStrength = (energyScores: Record<string, number>, dayMaster: string): string => {
  const dayMasterWuxing = GAN_WUXING[dayMaster];
  const score = energyScores[dayMasterWuxing] || 0;
  if (score >= 30) return '身强';
  if (score >= 20) return '中和';
  return '身弱';
};

export default function BaziDisplayV5({ bazi, dayun }: BaziDisplayV5Props) {
  // 获取气候图标
  const getClimateIcon = (climate: string) => {
    switch (climate) {
      case '寒': return '❄️';
      case '燥': return '🔥';
      default: return '☯';
    }
  };

  const dayMasterStrength = getDayMasterStrength(bazi.energy_scores, bazi.day_master);

  return (
    <div className="bazi-display-v5">
      {/* 三栏布局：雷达图 | 四柱 | 关键信息 */}
      <div className="bazi-grid">
        {/* 左栏：五行雷达图 */}
        <div className="bazi-grid-left">
          <div className="radar-card">
            <h4 className="card-title">五行能量</h4>
            <div className="radar-container">
              <WuxingRadarChart 
                energyScores={bazi.energy_scores} 
                favorable={bazi.favorable}
              />
            </div>
          </div>
        </div>

        {/* 中栏：四柱八字 */}
        <div className="bazi-grid-center">
          <h4 className="card-title card-title-center">四柱八字</h4>
          <div className="pillars-container">
            {bazi.pillars.map((pillar, index) => {
              const ganWx = GAN_WUXING[pillar.gan];
              const zhiWx = ZHI_WUXING[pillar.zhi];
              return (
                <div 
                  key={index} 
                  className="pillar-card-v5"
                >
                  {/* 天干 */}
                  <div 
                    className="pillar-gan"
                    style={{ 
                      background: `linear-gradient(180deg, ${WUXING_COLORS[ganWx]}CC 0%, ${WUXING_COLORS[ganWx]} 100%)`,
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                    }}
                  >
                    {pillar.gan}
                  </div>
                  {/* 分隔线 */}
                  <div className="pillar-divider"></div>
                  {/* 地支 */}
                  <div 
                    className="pillar-zhi"
                    style={{ color: WUXING_COLORS[zhiWx] }}
                  >
                    {pillar.zhi}
                  </div>
                  {/* 柱名 */}
                  <div className="pillar-name">
                    {pillar.name}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* 右栏：关键信息 */}
        <div className="bazi-grid-right">
          <div className="stats-card">
            <h4 className="card-title">命格信息</h4>
            
            {/* 日主 */}
            <div className="stat-item">
              <span className="stat-label">日主</span>
              <span 
                className="stat-value stat-value-large"
                style={{ color: WUXING_COLORS[GAN_WUXING[bazi.day_master]] }}
              >
                {bazi.day_master}
              </span>
            </div>

            {/* 身强弱 */}
            <div className="stat-item">
              <span className="stat-label">强弱</span>
              <span className="stat-value">{dayMasterStrength}</span>
            </div>

            {/* 气候 */}
            <div className="stat-item">
              <span className="stat-label">气候</span>
              <span className="stat-value">
                <span className="climate-icon">{getClimateIcon(bazi.climate)}</span>
                {bazi.climate === '寒' ? '寒命' : bazi.climate === '燥' ? '燥命' : '平命'}
              </span>
            </div>

            {/* 喜用神 */}
            <div className="stat-item stat-item-vertical">
              <span className="stat-label">喜用神</span>
              <div className="favorable-tags">
                {bazi.favorable.map((wx, i) => (
                  <span
                    key={i}
                    className="favorable-tag"
                    style={{ 
                      backgroundColor: `${WUXING_COLORS[wx]}20`,
                      color: WUXING_COLORS[wx],
                      borderColor: `${WUXING_COLORS[wx]}40`
                    }}
                  >
                    {wx}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 大运排盘 */}
      <div className="dayun-section">
        <h4 className="card-title">大运排盘</h4>
        <div className="dayun-container">
          {dayun.slice(0, 8).map((dy, index) => {
            const gan = dy.ganzhi[0];
            const zhi = dy.ganzhi[1];
            const ganWx = GAN_WUXING[gan];
            const zhiWx = ZHI_WUXING[zhi];
            
            return (
              <div 
                key={index}
                className="dayun-item"
              >
                <div className="dayun-ganzhi">
                  <span style={{ color: WUXING_COLORS[ganWx] }}>{gan}</span>
                  <span style={{ color: WUXING_COLORS[zhiWx] }}>{zhi}</span>
                </div>
                <div className="dayun-age">
                  {dy.start_age}-{dy.start_age + 9}岁
                </div>
                <div className="dayun-year">
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
