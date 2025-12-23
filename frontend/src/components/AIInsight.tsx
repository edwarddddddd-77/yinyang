import { useState, useEffect, useRef } from 'react';

interface Marker {
  name: string;
  icon: string;
  type: string;
  desc: string;
}

interface YearData {
  year: number;
  ganzhi: string;
  score: number;
  markers: Marker[];
}

interface BaziInfo {
  day_gan?: string;
  day_zhi?: string;
  year_gan?: string;
  year_zhi?: string;
  month_gan?: string;
  month_zhi?: string;
  time_gan?: string;
  time_zhi?: string;
}

interface AIInsightProps {
  selectedYear: YearData | null;
  userBazi?: BaziInfo;
  activeDimension?: string;
  meta?: {
    pattern?: string;
    fav_gods?: string[];
  };
}

// V9.3 - 强制调用真实 DeepSeek API，移除所有本地 Mock
const fetchRealAIAnalysis = async (
  yearData: YearData,
  userBazi: BaziInfo,
  dimension: string,
  meta?: { pattern?: string; fav_gods?: string[] }
): Promise<string> => {
  // 从干支中提取年干和年支
  const ganzhi = yearData.ganzhi || '';
  const yearGan = ganzhi.charAt(0) || '';
  const yearZhi = ganzhi.charAt(1) || '';
  
  // 提取神煞名称
  const shenshaNames = yearData.markers?.map(m => m.name) || [];
  
  // V9.3 标准 Payload
  const payload = {
    user_bazi: {
      year: userBazi?.year_gan && userBazi?.year_zhi ? `${userBazi.year_gan}${userBazi.year_zhi}` : '',
      month: userBazi?.month_gan && userBazi?.month_zhi ? `${userBazi.month_gan}${userBazi.month_zhi}` : '',
      day: userBazi?.day_gan && userBazi?.day_zhi ? `${userBazi.day_gan}${userBazi.day_zhi}` : '',
      time: userBazi?.time_gan && userBazi?.time_zhi ? `${userBazi.time_gan}${userBazi.time_zhi}` : '',
    },
    target_year: yearData.year,
    year_gan: yearGan,
    year_zhi: yearZhi,
    year_score: yearData.score,
    shensha: shenshaNames,
    dimension: dimension,
    // V9.3 新增字段
    pattern: meta?.pattern || '未知',
    fav_gods: meta?.fav_gods || []
  };

  console.log('[AIInsight V9.3] Calling Real API with payload:', payload);

  try {
    // 使用代理路径，不使用硬编码的 localhost:8000
    const response = await fetch('/api/analyze_year', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    
    if (!response.ok) {
      console.error('[AIInsight V9.3] API response not ok:', response.status);
      throw new Error(`API request failed: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('[AIInsight V9.3] API response:', data);
    
    if (data.success && data.data?.analysis_text) {
      return data.data.analysis_text;
    }
    
    throw new Error('Invalid response format');
  } catch (error) {
    console.error('[AIInsight V9.3] API call failed:', error);
    // 返回错误提示，不再使用本地 Mock
    return `【天机暂隐】连接云端失败，请稍后重试。(${yearData.year}年 ${yearData.ganzhi} 运势指数: ${yearData.score}分)`;
  }
};

export default function AIInsight({ selectedYear, userBazi, activeDimension = 'overall', meta }: AIInsightProps) {
  const [displayText, setDisplayText] = useState<string>('');
  const [isTyping, setIsTyping] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);
  
  // 维度中文映射
  const dimensionLabels: Record<string, string> = {
    overall: '综合运势',
    career: '仕途事业',
    wealth: '正财偏财',
    love: '姻缘桃花',
    health: '身体发肤',
    parents: '高堂父母',
    children: '子孙后代'
  };
  
  useEffect(() => {
    if (!selectedYear) {
      setDisplayText('');
      return;
    }
    
    let isCancelled = false;
    let typingInterval: ReturnType<typeof setInterval> | null = null;
    
    const fetchAndDisplay = async () => {
      setIsLoading(true);
      setDisplayText('');
      
      // V9.3 - 强制调用真实 API
      const fullText = await fetchRealAIAnalysis(
        selectedYear,
        userBazi || {},
        activeDimension,
        meta
      );
      
      if (isCancelled) return;
      
      setIsLoading(false);
      setIsTyping(true);
      
      // 打字机效果
      let index = 0;
      typingInterval = setInterval(() => {
        if (isCancelled) {
          if (typingInterval) clearInterval(typingInterval);
          return;
        }
        
        if (index < fullText.length) {
          setDisplayText(fullText.slice(0, index + 1));
          index++;
          // 自动滚动到底部
          if (contentRef.current) {
            contentRef.current.scrollTop = contentRef.current.scrollHeight;
          }
        } else {
          if (typingInterval) clearInterval(typingInterval);
          setIsTyping(false);
        }
      }, 25);
    };
    
    // 延迟 300ms 防止快速点击闪烁
    const timer = setTimeout(() => {
      fetchAndDisplay();
    }, 300);
    
    return () => {
      isCancelled = true;
      clearTimeout(timer);
      if (typingInterval) clearInterval(typingInterval);
    };
  }, [selectedYear, userBazi, activeDimension, meta]);
  
  return (
    <div className="ai-chat-card">
      {/* 聊天头部 */}
      <div className="ai-chat-header">
        <div className="ai-avatar">
          <span className="ai-avatar-icon">☯</span>
          <span className="ai-avatar-pulse"></span>
        </div>
        <div className="ai-header-info">
          <h3 className="ai-header-title">天机 AI 解读</h3>
          <p className="ai-header-status">
            {isLoading ? '正在推演...' : isTyping ? '正在解读...' : selectedYear ? '解读完成' : '等待查询'}
          </p>
        </div>
        {/* V9.3 标识 */}
        <div className="ai-version-badge" style={{ 
          marginLeft: 'auto', 
          fontSize: '10px', 
          color: '#888',
          padding: '2px 6px',
          background: 'rgba(255,215,0,0.1)',
          borderRadius: '4px'
        }}>
          V9.3 Real AI
        </div>
      </div>
      
      {/* 聊天内容区域 */}
      <div className="ai-chat-content" ref={contentRef}>
        {selectedYear ? (
          <div className="ai-message-container">
            {/* 用户查询气泡 */}
            <div className="user-query-bubble">
              <div className="query-year">
                <span className="query-year-number">{selectedYear.year}</span>
                <span className="query-year-ganzhi">{selectedYear.ganzhi}年</span>
              </div>
              {selectedYear.markers.length > 0 && (
                <div className="query-markers">
                  {selectedYear.markers.slice(0, 4).map((m, i) => (
                    <span key={i} className="query-marker" title={m.name}>
                      {m.icon}
                    </span>
                  ))}
                  {selectedYear.markers.length > 4 && (
                    <span className="query-marker-more">+{selectedYear.markers.length - 4}</span>
                  )}
                </div>
              )}
              <div className="query-score">
                <span className={`score-value ${selectedYear.score >= 70 ? 'high' : selectedYear.score < 40 ? 'low' : 'medium'}`}>
                  {selectedYear.score}
                </span>
                <span className="score-label">运势指数</span>
              </div>
              {/* 显示当前维度 */}
              <div className="query-dimension" style={{ 
                fontSize: '11px', 
                color: '#ffd700', 
                marginTop: '4px' 
              }}>
                {dimensionLabels[activeDimension] || '流年运势'}
              </div>
            </div>
            
            {/* AI 回复气泡 */}
            <div className="ai-response-bubble">
              <div className="ai-bubble-avatar">☯</div>
              <div className="ai-bubble-content">
                {isLoading ? (
                  <div className="ai-loading">
                    <div className="loading-taichi">
                      <span className="taichi-spinner">☯</span>
                    </div>
                    <p className="loading-text">天机正在推演中...</p>
                    <p className="loading-subtext">DeepSeek AI 分析命盘与流年关系</p>
                  </div>
                ) : (
                  <p className="ai-response-text">
                    {displayText}
                    {isTyping && <span className="typing-cursor">|</span>}
                  </p>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="ai-empty-state">
            <div className="empty-icon">
              <span className="empty-crystal">🔮</span>
              <span className="empty-glow"></span>
            </div>
            <p className="empty-title">点击K线图中的任意年份</p>
            <p className="empty-subtitle">天机将为您解读该年运势玄机</p>
            <div className="empty-hint">
              <span className="hint-arrow">↑</span>
              <span className="hint-text">选择年份开始解读</span>
            </div>
          </div>
        )}
      </div>
      
      {/* 底部免责声明 */}
      <div className="ai-chat-footer">
        <p className="ai-disclaimer">
          <span className="disclaimer-icon">⚠️</span>
          AI 解读仅供参考娱乐，不构成任何决策建议。命运掌握在自己手中。
        </p>
      </div>
    </div>
  );
}
