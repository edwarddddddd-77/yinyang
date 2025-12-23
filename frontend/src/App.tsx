import { useState } from 'react';
import BirthFormV4 from './components/BirthFormV4';
import BaziDisplayV5 from './components/BaziDisplayV5';
import LifeKLineChartV4 from './components/LifeKLineChartV4';
import AIInsight from './components/AIInsight';
import SoulCard from './components/SoulCard';
import { calculateBazi } from './api';

interface Marker {
  name: string;
  icon: string;
  type: string;
  desc: string;
}

interface TrendDataItem {
  year: number;
  ganzhi: string;
  score: number;
  markers: Marker[];
}

interface DimensionData {
  name: string;
  data: TrendDataItem[];
}

interface MultiDimensionTrend {
  overall: DimensionData;
  career: DimensionData;
  wealth: DimensionData;
  health: DimensionData;
  love: DimensionData;
  parents: DimensionData;
  children: DimensionData;
}

interface BaziData {
  nickname: string;
  birth_info: {
    solar: string;
    location: string;
    longitude: number;
    true_solar_offset: number;
  };
  bazi: {
    pillars: Array<{
      name: string;
      gan: string;
      zhi: string;
    }>;
    day_master: string;
    climate: string;
    favorable: string[];
    energy_scores: Record<string, number>;
  };
  dayun: Array<{
    ganzhi: string;
    start_year: number;
    end_year: number;
    start_age: number;
  }>;
  life_trend: TrendDataItem[];
  multi_dimension_trend?: MultiDimensionTrend;
  gender: string;
  meta?: {
    pattern: string;
    fav_gods: string[];
    soul?: {
      gan: string;
      wuxing: string;
      image: string;
      icon: string;
      traits: string;
      description: string;
    };
  };
}

function App() {
  const [baziData, setBaziData] = useState<BaziData | null>(null);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(true);
  const [selectedYear, setSelectedYear] = useState<TrendDataItem | null>(null);
  const [activeDimension, setActiveDimension] = useState<string>('overall');

  const handleSubmit = async (formData: any) => {
    setLoading(true);
    try {
      const response = await calculateBazi(formData);
      if (response.success) {
        setBaziData(response.data);
        setShowForm(false);
        setSelectedYear(null);
      }
    } catch (error) {
      console.error('计算失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setBaziData(null);
    setShowForm(true);
    setSelectedYear(null);
  };

  const handleYearClick = (yearData: TrendDataItem) => {
    setSelectedYear(yearData);
  };

  const handleDimensionChange = (dimension: string) => {
    setActiveDimension(dimension);
  };

  return (
    <div className="min-h-screen">
      {/* 全局头部 - 毛玻璃效果固定头部 */}
      <header className="header-glass">
        <div className="header-container">
          {/* 左侧 Logo */}
          <div className="header-logo">
            <span className="header-logo-icon">☯</span>
            <div className="header-logo-text">
              <h1 className="header-title">YinYang</h1>
              <p className="header-subtitle">东方玄学 · 人生大数据平台</p>
            </div>
          </div>
          
          {/* 右侧副文本 */}
          <div className="header-meta">
            <p>基于传统八字命理</p>
            <p>真太阳时精准排盘</p>
          </div>
        </div>
      </header>

      {/* 主内容区域 - 添加顶部间距以避免被固定头部遮挡 */}
      <main className="main-content">
        {showForm ? (
          /* 首页 - 输入表单 */
          <div className="home-container">
            {/* Hero 标题区域 */}
            <div className="hero-section">
              <h2 className="hero-title">探知命运的纹理</h2>
              <p className="hero-subtitle">Explore the Texture of Destiny</p>
            </div>
            
            {/* 表单卡片 */}
            <div className="form-card animate-fade-in-up">
              <div className="form-card-header">
                <h3 className="form-card-title">命理排盘</h3>
                <p className="form-card-desc">请输入您的出生信息</p>
              </div>
              <BirthFormV4 onSubmit={handleSubmit} loading={loading} />
            </div>
          </div>
        ) : baziData ? (
          /* 结果展示页面 */
          <div className="dashboard-container animate-fade-in-up">
            {/* 顶部导航栏 */}
            <div className="dashboard-nav">
              <button
                onClick={handleReset}
                className="back-button"
              >
                <span>←</span>
                <span>重新排盘</span>
              </button>
              <div className="user-info">
                <p className="user-name">{baziData.nickname} · {baziData.gender}</p>
                <p className="user-birth">
                  {baziData.birth_info.solar} | {baziData.birth_info.location}
                </p>
                <p className="user-correction">
                  真太阳时校正: {baziData.birth_info.true_solar_offset > 0 ? '+' : ''}{baziData.birth_info.true_solar_offset}分钟
                </p>
              </div>
            </div>

            {/* 八字命盘展示 - 使用新的 V5 布局 */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
              <div className="lg:col-span-3">
                <BaziDisplayV5 bazi={baziData.bazi} dayun={baziData.dayun} />
              </div>
              <div className="lg:col-span-1">
                {/* V9.6: 日主元神卡片 */}
                <SoulCard soul={baziData.meta?.soul} />
              </div>
            </div>

            {/* 多维度人生K线图 */}
            <div className="kline-section">
              <h3 className="section-title">
                <span className="section-icon">📈</span>
                多维度人生运势K线
              </h3>
              <LifeKLineChartV4 
                data={baziData.life_trend} 
                multiDimensionData={baziData.multi_dimension_trend}
                birthYear={parseInt(baziData.birth_info.solar)}
                onYearClick={handleYearClick}
                onDimensionChange={handleDimensionChange}
              />
            </div>

            {/* AI 解读区域 */}
            <AIInsight 
              selectedYear={selectedYear} 
              userBazi={{
                day_gan: baziData.bazi.pillars[2]?.gan,
                day_zhi: baziData.bazi.pillars[2]?.zhi,
                year_gan: baziData.bazi.pillars[0]?.gan,
                year_zhi: baziData.bazi.pillars[0]?.zhi,
                month_gan: baziData.bazi.pillars[1]?.gan,
                month_zhi: baziData.bazi.pillars[1]?.zhi,
                time_gan: baziData.bazi.pillars[3]?.gan,
                time_zhi: baziData.bazi.pillars[3]?.zhi,
              }}
              activeDimension={activeDimension}
            />

            {/* 页脚 */}
            <footer className="dashboard-footer">
              <p>☯ YinYang · 东方玄学人生大数据平台</p>
              <p>本平台仅供娱乐参考，命运掌握在自己手中</p>
            </footer>
          </div>
        ) : null}
      </main>
    </div>
  );
}

export default App;
