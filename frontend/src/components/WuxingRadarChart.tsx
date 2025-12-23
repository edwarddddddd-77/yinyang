import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

interface WuxingRadarChartProps {
  energyScores: Record<string, number>;
  favorable: string[];
}

// 五行配置
const WUXING_CONFIG = [
  { name: '木', key: '木', angle: 90 },
  { name: '火', key: '火', angle: 18 },
  { name: '土', key: '土', angle: 306 },
  { name: '金', key: '金', angle: 234 },
  { name: '水', key: '水', angle: 162 },
];

export default function WuxingRadarChart({ energyScores, favorable }: WuxingRadarChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    // 初始化图表
    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current, 'dark');
    }

    // 计算总能量用于归一化
    const totalEnergy = Object.values(energyScores).reduce((a, b) => a + b, 0);
    
    // 准备雷达图数据 - 归一化到 0-100
    const radarData = WUXING_CONFIG.map(wx => {
      const score = energyScores[wx.key] || 0;
      return totalEnergy > 0 ? (score / totalEnergy) * 100 : 0;
    });

    // 最大值用于雷达图范围
    const maxValue = Math.max(...radarData, 40);

    const option: echarts.EChartsOption = {
      backgroundColor: 'transparent',
      radar: {
        indicator: WUXING_CONFIG.map(wx => ({
          name: wx.name,
          max: maxValue,
        })),
        center: ['50%', '50%'],
        radius: '65%',
        startAngle: 90,
        splitNumber: 4,
        shape: 'polygon',
        axisName: {
          color: '#D4AF37',
          fontSize: 16,
          fontWeight: 'bold',
          fontFamily: 'Noto Serif SC, serif',
          formatter: (value?: string) => {
            if (!value) return '';
            const isFavorable = favorable.includes(value);
            return isFavorable ? `{favorable|${value}}` : value;
          },
          rich: {
            favorable: {
              color: '#2ECC71',
              fontSize: 18,
              fontWeight: 'bold',
              textShadowColor: '#2ECC71',
              textShadowBlur: 10,
            },
          },
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(212, 175, 55, 0.15)',
            width: 1,
          },
        },
        splitArea: {
          show: true,
          areaStyle: {
            color: [
              'rgba(212, 175, 55, 0.02)',
              'rgba(212, 175, 55, 0.05)',
              'rgba(212, 175, 55, 0.02)',
              'rgba(212, 175, 55, 0.05)',
            ],
          },
        },
        axisLine: {
          lineStyle: {
            color: 'rgba(212, 175, 55, 0.2)',
          },
        },
      },
      series: [
        {
          name: '五行能量',
          type: 'radar',
          data: [
            {
              value: radarData,
              name: '五行分布',
              symbol: 'circle',
              symbolSize: 8,
              lineStyle: {
                color: '#D4AF37',
                width: 2,
                shadowColor: 'rgba(212, 175, 55, 0.8)',
                shadowBlur: 10,
              },
              itemStyle: {
                color: '#D4AF37',
                borderColor: '#1F1F1F',
                borderWidth: 2,
              },
              areaStyle: {
                color: new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
                  { offset: 0, color: 'rgba(212, 175, 55, 0.6)' },
                  { offset: 0.5, color: 'rgba(212, 175, 55, 0.3)' },
                  { offset: 1, color: 'rgba(212, 175, 55, 0.1)' },
                ]),
              },
            },
          ],
        },
      ],
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(31, 31, 31, 0.95)',
        borderColor: 'rgba(212, 175, 55, 0.4)',
        borderWidth: 1,
        padding: [12, 16],
        textStyle: {
          color: '#F7F4ED',
          fontFamily: 'Noto Sans SC, sans-serif',
        },
        formatter: () => {
          let html = '<div style="font-family: Noto Serif SC, serif;">';
          html += '<div style="font-size: 14px; color: #D4AF37; margin-bottom: 8px; font-weight: bold;">五行能量分布</div>';
          WUXING_CONFIG.forEach((wx, index) => {
            const score = radarData[index];
            const isFavorable = favorable.includes(wx.key);
            const color = isFavorable ? '#2ECC71' : '#D4AF37';
            html += `<div style="display: flex; justify-content: space-between; gap: 20px; margin: 4px 0;">
              <span style="color: ${color};">${wx.name}${isFavorable ? ' (喜)' : ''}</span>
              <span style="color: #F7F4ED;">${score.toFixed(1)}%</span>
            </div>`;
          });
          html += '</div>';
          return html;
        },
      },
    };

    chartInstance.current.setOption(option, true);

    // 响应式
    const handleResize = () => {
      chartInstance.current?.resize();
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [energyScores, favorable]);

  return (
    <div className="w-full h-full">
      <div ref={chartRef} className="w-full h-[280px]" />
    </div>
  );
}
