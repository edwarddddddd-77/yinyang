import { useState, useEffect } from 'react';
import { getProvinces, getCities, type City } from '../api';

interface BirthFormV4Props {
  onSubmit: (data: any) => void;
  loading: boolean;
}

// 省份城市数据（内置备用）
const BUILTIN_DATA: Record<string, City[]> = {
  '北京市': [{ name: '北京', longitude: 116.41 }],
  '上海市': [{ name: '上海', longitude: 121.47 }],
  '天津市': [{ name: '天津', longitude: 117.20 }],
  '重庆市': [{ name: '重庆', longitude: 106.55 }],
  '广东省': [
    { name: '广州', longitude: 113.23 },
    { name: '深圳', longitude: 114.07 },
    { name: '东莞', longitude: 113.75 },
  ],
  '浙江省': [
    { name: '杭州', longitude: 120.15 },
    { name: '宁波', longitude: 121.55 },
    { name: '温州', longitude: 120.65 },
  ],
  '江苏省': [
    { name: '南京', longitude: 118.78 },
    { name: '苏州', longitude: 120.62 },
    { name: '无锡', longitude: 120.30 },
  ],
  '四川省': [
    { name: '成都', longitude: 104.07 },
    { name: '绵阳', longitude: 104.73 },
  ],
  '湖北省': [
    { name: '武汉', longitude: 114.31 },
    { name: '宜昌', longitude: 111.29 },
  ],
  '山东省': [
    { name: '济南', longitude: 117.00 },
    { name: '青岛', longitude: 120.33 },
  ],
};

export default function BirthFormV4({ onSubmit, loading }: BirthFormV4Props) {
  const currentYear = new Date().getFullYear();
  
  const [formData, setFormData] = useState({
    nickname: '',
    year: 1990,
    month: 1,
    day: 1,
    hour: 12,
    minute: 0,
    gender: 1,
    is_lunar: false,
    province: '',
    city: '',
    city_long: 120.0,
  });

  const [provinces, setProvinces] = useState<string[]>(Object.keys(BUILTIN_DATA));
  const [cities, setCities] = useState<City[]>([]);

  useEffect(() => {
    // 尝试从API获取省份
    getProvinces().then(data => {
      if (data && data.length > 0) {
        setProvinces(data);
      }
    }).catch(() => {
      // 使用内置数据
    });
  }, []);

  useEffect(() => {
    if (formData.province) {
      // 先尝试从API获取
      getCities(formData.province).then(data => {
        if (data && data.length > 0) {
          setCities(data);
          // 自动选择第一个城市
          const firstCity = data[0];
          setFormData(prev => ({
            ...prev,
            city: firstCity.name,
            city_long: firstCity.longitude,
          }));
        }
      }).catch(() => {
        // 使用内置数据
        const builtinCities = BUILTIN_DATA[formData.province] || [];
        setCities(builtinCities);
        if (builtinCities.length > 0) {
          setFormData(prev => ({
            ...prev,
            city: builtinCities[0].name,
            city_long: builtinCities[0].longitude,
          }));
        }
      });
    }
  }, [formData.province]);

  const handleChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleCityChange = (cityName: string) => {
    const city = cities.find(c => c.name === cityName);
    if (city) {
      setFormData(prev => ({
        ...prev,
        city: city.name,
        city_long: city.longitude,
      }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  // 生成年份选项
  const years = Array.from({ length: 100 }, (_, i) => currentYear - i);
  const months = Array.from({ length: 12 }, (_, i) => i + 1);
  const days = Array.from({ length: 31 }, (_, i) => i + 1);
  const hours = Array.from({ length: 24 }, (_, i) => i);
  const minutes = Array.from({ length: 60 }, (_, i) => i);

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* 昵称 */}
      <div>
        <label className="mystical-label">称呼</label>
        <input
          type="text"
          className="mystical-input"
          placeholder="请输入您的称呼"
          value={formData.nickname}
          onChange={(e) => handleChange('nickname', e.target.value)}
        />
      </div>

      {/* 性别 */}
      <div>
        <label className="mystical-label">性别</label>
        <div className="flex gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="gender"
              checked={formData.gender === 1}
              onChange={() => handleChange('gender', 1)}
              className="accent-gold"
            />
            <span className="text-rice">乾造（男）</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="gender"
              checked={formData.gender === 0}
              onChange={() => handleChange('gender', 0)}
              className="accent-gold"
            />
            <span className="text-rice">坤造（女）</span>
          </label>
        </div>
      </div>

      {/* 历法选择 */}
      <div>
        <label className="mystical-label">历法</label>
        <div className="flex gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="calendar"
              checked={!formData.is_lunar}
              onChange={() => handleChange('is_lunar', false)}
              className="accent-gold"
            />
            <span className="text-rice">公历</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="calendar"
              checked={formData.is_lunar}
              onChange={() => handleChange('is_lunar', true)}
              className="accent-gold"
            />
            <span className="text-rice">农历</span>
          </label>
        </div>
      </div>

      {/* 出生日期 */}
      <div>
        <label className="mystical-label">出生日期</label>
        <div className="grid grid-cols-3 gap-3">
          <select
            className="mystical-select"
            value={formData.year}
            onChange={(e) => handleChange('year', parseInt(e.target.value))}
          >
            {years.map(y => (
              <option key={y} value={y}>{y}年</option>
            ))}
          </select>
          <select
            className="mystical-select"
            value={formData.month}
            onChange={(e) => handleChange('month', parseInt(e.target.value))}
          >
            {months.map(m => (
              <option key={m} value={m}>{m}月</option>
            ))}
          </select>
          <select
            className="mystical-select"
            value={formData.day}
            onChange={(e) => handleChange('day', parseInt(e.target.value))}
          >
            {days.map(d => (
              <option key={d} value={d}>{d}日</option>
            ))}
          </select>
        </div>
      </div>

      {/* 出生时间 */}
      <div>
        <label className="mystical-label">出生时间</label>
        <div className="grid grid-cols-2 gap-3">
          <select
            className="mystical-select"
            value={formData.hour}
            onChange={(e) => handleChange('hour', parseInt(e.target.value))}
          >
            {hours.map(h => (
              <option key={h} value={h}>{h}时</option>
            ))}
          </select>
          <select
            className="mystical-select"
            value={formData.minute}
            onChange={(e) => handleChange('minute', parseInt(e.target.value))}
          >
            {minutes.map(m => (
              <option key={m} value={m}>{m}分</option>
            ))}
          </select>
        </div>
      </div>

      {/* 出生地 */}
      <div>
        <label className="mystical-label">出生地</label>
        <div className="grid grid-cols-2 gap-3">
          <select
            className="mystical-select"
            value={formData.province}
            onChange={(e) => handleChange('province', e.target.value)}
          >
            <option value="">选择省份</option>
            {provinces.map(p => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
          <select
            className="mystical-select"
            value={formData.city}
            onChange={(e) => handleCityChange(e.target.value)}
            disabled={!formData.province}
          >
            <option value="">选择城市</option>
            {cities.map(c => (
              <option key={c.name} value={c.name}>{c.name}</option>
            ))}
          </select>
        </div>
        {formData.city_long && (
          <p className="text-xs text-gold/50 mt-2">
            经度: {formData.city_long}° | 真太阳时校正: {((formData.city_long - 120) * 4).toFixed(1)}分钟
          </p>
        )}
      </div>

      {/* 提交按钮 */}
      <button
        type="submit"
        className="vermilion-btn w-full"
        disabled={loading || !formData.province || !formData.city}
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="loading-spinner w-5 h-5"></span>
            排盘中...
          </span>
        ) : (
          '开始排盘'
        )}
      </button>
    </form>
  );
}
