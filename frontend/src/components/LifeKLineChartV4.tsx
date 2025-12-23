import { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';

interface Marker {
  name: string;
  icon: string;
  type: string;
  desc: string;
}

interface TrendData {
  year: number;
  ganzhi: string;
  score: number;
  markers: Marker[];
}

interface DimensionData {
  name: string;
  data: TrendData[];
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

interface LifeKLineChartV4Props {
  data: TrendData[];
  multiDimensionData?: MultiDimensionTrend;
  birthYear?: number;
  onYearClick?: (yearData: TrendData) => void;
  onDimensionChange?: (dimension: string) => void;
}

type DimensionKey = 'overall' | 'career' | 'wealth' | 'health' | 'love' | 'parents' | 'children';

const DIMENSION_CONFIG: Record<DimensionKey, { name: string; icon: string; color: string; description: string }> = {
  overall: { name: '综合运势', icon: '☯️', color: '#D4AF37', description: '整体运势走向' },
  career: { name: '事业运', icon: '💼', color: '#3498DB', description: '事业发展、职场晋升' },
  wealth: { name: '财运', icon: '💰', color: '#F39C12', description: '财富收入、投资理财' },
  health: { name: '健康运', icon: '❤️', color: '#2ECC71', description: '身体健康、精神状态' },
  love: { name: '姻缘运', icon: '💕', color: '#E91E63', description: '感情婚姻、人际关系' },
  parents: { name: '父母运', icon: '👨‍👩‍👧', color: '#9B59B6', description: '父母健康、家庭和睦' },
  children: { name: '子女运', icon: '👶', color: '#1ABC9C', description: '子女健康、子女发展' },
};

export default function LifeKLineChartV4({ data, multiDimensionData, onYearClick, onDimensionChange }: LifeKLineChartV4Props) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);
  const [timeRange, setTimeRange] = useState<'first40' | 'last40' | 'all'>('all');
  const [activeDimension, setActiveDimension] = useState<DimensionKey>('overall');

  // 获取当前维度的数据
  const getCurrentDimensionData = (): TrendData[] => {
    if (multiDimensionData && multiDimensionData[activeDimension]) {
      return multiDimensionData[activeDimension].data;
    }
    return data;
  };

  // 根据时间范围过滤数据
  const getFilteredData = () => {
    const currentData = getCurrentDimensionData();
    if (timeRange === 'first40') {
      return currentData.slice(0, 40);
    } else if (timeRange === 'last40') {
      return currentData.slice(40);
    }
    return currentData;
  };

  useEffect(() => {
    if (!chartRef.current) return;

    // 初始化图表
    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current, 'dark');
    }

    const filteredData = getFilteredData();
    const years = filteredData.map(d => d.year);
    const scores = filteredData.map(d => d.score);
    const dimensionColor = DIMENSION_CONFIG[activeDimension].color;

    // 找出有标记的年份
    const markerPoints = filteredData
      .filter(d => d.markers.length > 0)
      .map(d => ({
        coord: [d.year, d.score],
        value: d.score,
        markers: d.markers,
        ganzhi: d.ganzhi,
        year: d.year,
      }));

    const option: echarts.EChartsOption = {
      backgroundColor: 'transparent',
      grid: {
        top: 60,
        right: 40,
        bottom: 80,
        left: 60,
      },
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(31, 31, 31, 0.95)',
        borderColor: `${dimensionColor}40`,
        borderWidth: 1,
        padding: [16, 20],
        textStyle: {
          color: '#F7F4ED',
        },
        formatter: (params: any) => {
          const dataIndex = params[0]?.dataIndex;
          if (dataIndex === undefined) return '';
          
          const item = filteredData[dataIndex];
          const scoreColor = item.score >= 70 ? '#2ECC71' : item.score < 40 ? '#E74C3C' : dimensionColor;
          const dimConfig = DIMENSION_CONFIG[activeDimension];
          
          let html = `
            <div style="font-family: 'Noto Serif SC', serif;">
              <div style="font-size: 14px; color: ${dimensionColor}; margin-bottom: 4px;">
                ${dimConfig.icon} ${dimConfig.name}
              </div>
              <div style="font-size: 18px; font-weight: bold; color: #D4AF37; margin-bottom: 8px;">
                ${item.year}年 · ${item.ganzhi}
              </div>
              <div style="font-size: 24px; font-weight: bold; color: ${scoreColor}; margin-bottom: 12px;">
                运势指数: ${item.score}
              </div>
          `;
          
          if (item.markers.length > 0) {
            html += `<div style="border-top: 1px solid rgba(212, 175, 55, 0.2); padding-top: 12px;">`;
            item.markers.forEach(m => {
              const typeColor = m.type === '吉' ? '#2ECC71' : m.type === '凶' ? '#E74C3C' : m.type === '缘' ? '#FF69B4' : m.type === '动' ? '#6495ED' : '#D4AF37';
              html += `
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                  <span style="font-size: 20px;">${m.icon}</span>
                  <div>
                    <div style="color: ${typeColor}; font-weight: 500;">${m.name}</div>
                    <div style="color: rgba(247, 244, 237, 0.6); font-size: 12px;">${m.desc}</div>
                  </div>
                </div>
              `;
            });
            html += `</div>`;
          }
          
          html += `<div style="margin-top: 12px; padding-top: 8px; border-top: 1px dashed rgba(212, 175, 55, 0.2); font-size: 12px; color: rgba(247, 244, 237, 0.5);">
            💡 点击查看 AI 详细解读
          </div>`;
          html += `</div>`;
          return html;
        },
      },
      xAxis: {
        type: 'category',
        data: years,
        axisLine: {
          lineStyle: {
            color: `${dimensionColor}40`,
          },
        },
        axisLabel: {
          color: 'rgba(247, 244, 237, 0.6)',
          fontSize: 11,
          interval: 4,
        },
        axisTick: {
          show: false,
        },
      },
      yAxis: {
        type: 'value',
        min: 0,
        max: 100,
        splitNumber: 5,
        axisLine: {
          show: false,
        },
        axisLabel: {
          color: 'rgba(247, 244, 237, 0.4)',
          fontSize: 11,
        },
        splitLine: {
          lineStyle: {
            color: `${dimensionColor}15`,
          },
        },
      },
      visualMap: {
        show: false,
        pieces: [
          { gte: 70, color: '#2ECC71' },
          { gte: 40, lt: 70, color: dimensionColor },
          { lt: 40, color: '#E74C3C' },
        ],
      },
      series: [
        // 主线条
        {
          name: DIMENSION_CONFIG[activeDimension].name,
          type: 'line',
          data: scores,
          smooth: 0.4,
          symbol: 'circle',
          symbolSize: 6,
          lineStyle: {
            width: 3,
            shadowColor: `${dimensionColor}80`,
            shadowBlur: 10,
          },
          itemStyle: {
            borderWidth: 2,
            borderColor: '#1F1F1F',
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: `${dimensionColor}50` },
              { offset: 0.5, color: `${dimensionColor}20` },
              { offset: 1, color: `${dimensionColor}00` },
            ]),
          },
          markLine: {
            silent: true,
            symbol: 'none',
            lineStyle: {
              type: 'dashed',
            },
            data: [
              {
                yAxis: 70,
                lineStyle: { color: 'rgba(46, 204, 113, 0.3)' },
                label: { 
                  show: true, 
                  position: 'end',
                  formatter: '吉',
                  color: '#2ECC71',
                  fontSize: 12,
                },
              },
              {
                yAxis: 40,
                lineStyle: { color: 'rgba(231, 76, 60, 0.3)' },
                label: { 
                  show: true, 
                  position: 'end',
                  formatter: '凶',
                  color: '#E74C3C',
                  fontSize: 12,
                },
              },
            ],
          },
          markPoint: {
            symbol: 'pin',
            symbolSize: (_value: any, params: any) => {
              // V9.4: 太岁标记特殊大尺寸
              const point = markerPoints.find(p => p.year === params.name);
              const hasTaiSui = point?.markers?.some((m: any) => m.name?.includes('太岁'));
              return hasTaiSui ? 70 : 50;
            },
            data: markerPoints.map(p => {
              // V9.4: 检查是否有太岁标记
              const taiSuiMarker = p.markers.find((m: any) => m.name?.includes('太岁'));
              const primaryMarker = taiSuiMarker || p.markers[0];
              const hasTaiSui = !!taiSuiMarker;
              
              return {
                name: `${p.year}`,
                coord: [p.year, p.value],
                value: primaryMarker?.icon || '★',
                itemStyle: {
                  color: hasTaiSui ? '#8B0000' :  // 太岁用深红色
                         primaryMarker?.type === '吉' ? '#2ECC71' : 
                         primaryMarker?.type === '凶' ? '#E74C3C' :
                         primaryMarker?.type === '缘' ? '#FF69B4' : 
                         primaryMarker?.type === '动' ? '#6495ED' : dimensionColor,
                  shadowColor: hasTaiSui ? 'rgba(255, 0, 0, 0.8)' : 'transparent',
                  shadowBlur: hasTaiSui ? 20 : 0,
                },
                label: {
                  show: true,
                  formatter: () => primaryMarker?.icon || '★',
                  fontSize: hasTaiSui ? 22 : 16,  // 太岁图标更大
                  color: '#fff',
                },
              };
            }),
          },
        },
        // 发光效果层
        {
          name: '发光',
          type: 'line',
          data: scores,
          smooth: 0.4,
          symbol: 'none',
          lineStyle: {
            width: 8,
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: `${dimensionColor}15` },
              { offset: 0.5, color: `${dimensionColor}30` },
              { offset: 1, color: `${dimensionColor}15` },
            ]),
          },
          z: -1,
        },
      ],
      dataZoom: [
        {
          type: 'inside',
          start: 0,
          end: 100,
        },
        {
          type: 'slider',
          show: true,
          height: 30,
          bottom: 10,
          borderColor: `${dimensionColor}30`,
          backgroundColor: 'rgba(31, 31, 31, 0.8)',
          fillerColor: `${dimensionColor}30`,
          handleStyle: {
            color: dimensionColor,
          },
          textStyle: {
            color: 'rgba(247, 244, 237, 0.6)',
          },
        },
      ],
    };

    chartInstance.current.setOption(option, true);

    // 添加点击事件
    chartInstance.current.off('click');
    chartInstance.current.on('click', 'series', (params: any) => {
      const dataIndex = params.dataIndex;
      if (dataIndex !== undefined && dataIndex >= 0 && dataIndex < filteredData.length && onYearClick) {
        const yearData = filteredData[dataIndex];
        onYearClick(yearData);
      }
    });
    
    // 使用 getZr 监听全局点击以支持点击图表任意位置
    const zr = chartInstance.current.getZr();
    zr.off('click');
    zr.on('click', (params: any) => {
      // 检查是否点击在图表区域内
      const pointInPixel = [params.offsetX, params.offsetY];
      if (chartInstance.current?.containPixel('grid', pointInPixel)) {
        try {
          // 尝试通过坐标转换获取数据索引
          const pointInGrid = chartInstance.current.convertFromPixel({ seriesIndex: 0 }, pointInPixel);
          if (pointInGrid) {
            const dataIndex = Math.round(pointInGrid[0]);
            if (dataIndex >= 0 && dataIndex < filteredData.length && onYearClick) {
              const yearData = filteredData[dataIndex];
              onYearClick(yearData);
            }
          }
        } catch (e) {
          // 如果坐标转换失败，使用备用方法
          const option = chartInstance.current?.getOption();
          const xAxisData = (option?.xAxis as any)?.[0]?.data || [];
          if (xAxisData.length > 0) {
            // 估算点击位置对应的数据索引
            const chartWidth = chartRef.current?.clientWidth || 1000;
            const gridLeft = 60;
            const gridRight = 60;
            const effectiveWidth = chartWidth - gridLeft - gridRight;
            const relativeX = params.offsetX - gridLeft;
            const dataIndex = Math.round((relativeX / effectiveWidth) * (xAxisData.length - 1));
            if (dataIndex >= 0 && dataIndex < filteredData.length && onYearClick) {
              const yearData = filteredData[dataIndex];
              onYearClick(yearData);
            }
          }
        }
      }
    });

    // 响应式
    const handleResize = () => {
      chartInstance.current?.resize();
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [data, multiDimensionData, timeRange, activeDimension, onYearClick]);

  // 获取当前维度的特殊标记图例
  const getDimensionLegend = () => {
    switch (activeDimension) {
      case 'career':
        return [
          { icon: '📜', name: '文昌' },
          { icon: '🛡️', name: '贵人' },
          { icon: '⭐', name: '天德' },
          { icon: '🐎', name: '驿马' },
          { icon: '⚠️', name: '凶煞' },
        ];
      case 'wealth':
        return [
          { icon: '💰', name: '禄神' },
          { icon: '🛡️', name: '贵人' },
          { icon: '💸', name: '劫煞' },
          { icon: '⚠️', name: '比劫' },
        ];
      case 'health':
        return [
          { icon: '✨', name: '天德' },
          { icon: '🛡️', name: '贵人' },
          { icon: '🏥', name: '病符' },
          { icon: '⚰️', name: '丧门' },
        ];
      case 'love':
        return [
          { icon: '💍', name: '红鸾' },
          { icon: '🌸', name: '桃花' },
          { icon: '🎊', name: '天喜' },
          { icon: '💑', name: '正缘' },
          { icon: '🎨', name: '华盖' },
        ];
      default:
        return [
          { icon: '🛡️', name: '贵人' },
          { icon: '🌸', name: '桃花' },
          { icon: '💍', name: '红鸾' },
          { icon: '💰', name: '禄神' },
          { icon: '🐎', name: '驿马' },
        ];
    }
  };

  return (
    <div>
      {/* 维度切换标签 */}
      <div className="mb-6">
        <div className="flex flex-wrap gap-2">
          {(Object.keys(DIMENSION_CONFIG) as DimensionKey[]).map((key) => {
            const config = DIMENSION_CONFIG[key];
            const isActive = activeDimension === key;
            return (
              <button
                key={key}
                className={`
                  px-4 py-2 rounded-lg font-medium transition-all duration-300
                  flex items-center gap-2
                  ${isActive 
                    ? 'text-ink shadow-lg' 
                    : 'bg-ink/50 text-rice/60 hover:text-rice/80 border border-gold/20 hover:border-gold/40'
                  }
                `}
                style={{
                  backgroundColor: isActive ? config.color : undefined,
                  boxShadow: isActive ? `0 0 20px ${config.color}40` : undefined,
                }}
                onClick={() => {
                  setActiveDimension(key);
                  onDimensionChange?.(key);
                }}
              >
                <span className="text-lg">{config.icon}</span>
                <span>{config.name}</span>
              </button>
            );
          })}
        </div>
        <p className="mt-2 text-sm text-rice/40">
          {DIMENSION_CONFIG[activeDimension].description}
        </p>
      </div>

      {/* 时间范围切换 */}
      <div className="flex gap-2 mb-4">
        <button
          className={`dimension-tab ${timeRange === 'first40' ? 'active' : ''}`}
          onClick={() => setTimeRange('first40')}
        >
          前40年
        </button>
        <button
          className={`dimension-tab ${timeRange === 'last40' ? 'active' : ''}`}
          onClick={() => setTimeRange('last40')}
        >
          后40年
        </button>
        <button
          className={`dimension-tab ${timeRange === 'all' ? 'active' : ''}`}
          onClick={() => setTimeRange('all')}
        >
          全部
        </button>
      </div>

      {/* 图表 */}
      <div ref={chartRef} className="w-full h-[400px] cursor-pointer" />

      {/* 图例说明 */}
      <div className="mt-4 flex flex-wrap gap-4 text-sm">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-[#2ECC71]"></span>
          <span className="text-rice/60">&gt;70 吉</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full" style={{ backgroundColor: DIMENSION_CONFIG[activeDimension].color }}></span>
          <span className="text-rice/60">40-70 平</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-[#E74C3C]"></span>
          <span className="text-rice/60">&lt;40 凶</span>
        </div>
        <div className="border-l border-gold/20 mx-2"></div>
        {getDimensionLegend().map((item, index) => (
          <div key={index} className="flex items-center gap-2">
            <span>{item.icon}</span>
            <span className="text-rice/60">{item.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
