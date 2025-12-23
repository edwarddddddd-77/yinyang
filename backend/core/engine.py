# filename: engine.py
"""
BaziEngineV3 - 八字命理核心引擎
适配 lunar_python 库的实际API
"""

import math
from collections import defaultdict
from lunar_python import Solar, Lunar

# --- 1. 核心常量配置 ---

# 天干列表
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支列表
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干五行映射
GAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

# 地支五行映射
ZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 地支藏干比例 (Zi Ping Standard)
ZHI_RATIOS = {
    "子": {"癸": 1.0},
    "丑": {"己": 0.6, "癸": 0.3, "辛": 0.1},
    "寅": {"甲": 0.6, "丙": 0.3, "戊": 0.1},
    "卯": {"乙": 1.0},
    "辰": {"戊": 0.6, "乙": 0.3, "癸": 0.1},
    "巳": {"丙": 0.6, "戊": 0.3, "庚": 0.1},
    "午": {"丁": 0.7, "己": 0.3},
    "未": {"己": 0.6, "丁": 0.3, "乙": 0.1},
    "申": {"庚": 0.6, "壬": 0.3, "戊": 0.1},
    "酉": {"辛": 1.0},
    "戌": {"戊": 0.6, "辛": 0.3, "丁": 0.1},
    "亥": {"壬": 0.7, "甲": 0.3},
}

# 地支藏干（本气）
ZHI_HIDE_GAN = {
    "子": "癸", "丑": "己", "寅": "甲", "卯": "乙",
    "辰": "戊", "巳": "丙", "午": "丁", "未": "己",
    "申": "庚", "酉": "辛", "戌": "戊", "亥": "壬"
}

# 十神计算规则
# 以日主为基准，根据五行生克关系确定十神
def get_shi_shen(day_gan, target_gan):
    """计算十神"""
    day_wx = GAN_WUXING[day_gan]
    target_wx = GAN_WUXING[target_gan]
    
    # 判断阴阳
    day_yin = TIAN_GAN.index(day_gan) % 2  # 0阳 1阴
    target_yin = TIAN_GAN.index(target_gan) % 2
    same_yin = (day_yin == target_yin)
    
    # 五行生克关系
    sheng_map = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    ke_map = {"木": "土", "火": "金", "土": "水", "金": "木", "水": "火"}
    
    if day_wx == target_wx:
        return "比肩" if same_yin else "劫财"
    elif sheng_map[day_wx] == target_wx:  # 我生
        return "食神" if same_yin else "伤官"
    elif ke_map[day_wx] == target_wx:  # 我克
        return "偏财" if same_yin else "正财"
    elif sheng_map[target_wx] == day_wx:  # 生我
        return "偏印" if same_yin else "正印"
    elif ke_map[target_wx] == day_wx:  # 克我
        return "七杀" if same_yin else "正官"
    return "未知"


class BaziEngineV3:
    """
    V3 核心引擎：包含真太阳时、能量量化、格局判定、调候、神煞系统
    """
    def __init__(self, year, month, day, hour, minute, gender, longitude):
        self.gender = gender  # 1男 0女
        self.longitude = longitude
        
        # 1. 真太阳时校正
        self.solar = self._get_true_solar(year, month, day, hour, minute, longitude)
        self.lunar = self.solar.getLunar()
        self.bazi = self.lunar.getEightChar()
        self.bazi.setSect(2)  # 2 = 以立春交界 (专业八字标准)
        
        # 2. 提取核心数据
        self.year_gan = self.bazi.getYearGan()
        self.year_zhi = self.bazi.getYearZhi()
        self.month_gan = self.bazi.getMonthGan()
        self.month_zhi = self.bazi.getMonthZhi()
        self.day_gan = self.bazi.getDayGan()
        self.day_zhi = self.bazi.getDayZhi()
        self.time_gan = self.bazi.getTimeGan()
        self.time_zhi = self.bazi.getTimeZhi()
        
        self.day_master = self.day_gan  # 日主
        
        # 3. 初始化数据容器
        self.scores = defaultdict(float)  # 五行能量分数
        self.ten_gods = {}  # 十神映射 (Position -> Name)
        self.shen_sha = defaultdict(list)  # 神煞列表 (Position -> [List])
        self.pattern = "未知"  # 格局名称
        self.is_strong = False  # 身强/身弱
        self.climate = "平"  # 调候 (寒/燥/平)
        self.favorable = []  # 喜用神 (五行)
        
        # 4. 执行全流程计算
        self._calculate_ten_gods()  # 贴标签
        self._calculate_energy()    # 算能量
        self._check_climate()       # 查调候
        self._determine_pattern()   # 定格局喜忌
        self._calculate_shen_sha()  # 查神煞

    def _get_true_solar(self, y, m, d, h, min, lon):
        """计算真太阳时"""
        offset = (lon - 120.0) * 4
        total_minutes = h * 60 + min + offset
        
        # 处理日期进位
        day_offset = 0
        if total_minutes >= 1440:
            day_offset = 1
            total_minutes -= 1440
        elif total_minutes < 0:
            day_offset = -1
            total_minutes += 1440
            
        h_real = int(total_minutes // 60)
        m_real = int(total_minutes % 60)
        
        # 简单处理日期变化
        solar = Solar.fromYmdHms(y, m, d + day_offset, h_real, m_real, 0)
        return solar

    # --- 模块 A: 十神系统 ---
    def _calculate_ten_gods(self):
        # 天干十神
        self.ten_gods['year_gan'] = get_shi_shen(self.day_master, self.year_gan)
        self.ten_gods['month_gan'] = get_shi_shen(self.day_master, self.month_gan)
        self.ten_gods['day_gan'] = "日主"
        self.ten_gods['time_gan'] = get_shi_shen(self.day_master, self.time_gan)
        
        # 地支十神 (取本气)
        for pos, zhi in [('year_zhi', self.year_zhi), 
                         ('month_zhi', self.month_zhi), 
                         ('day_zhi', self.day_zhi), 
                         ('time_zhi', self.time_zhi)]:
            main_gan = ZHI_HIDE_GAN[zhi]
            self.ten_gods[pos] = get_shi_shen(self.day_master, main_gan)

    # --- 模块 B: 能量精算 (含藏干) ---
    def _calculate_energy(self):
        # 权重模型：月令最大
        weights = {
            "year_gan": 7,   "year_zhi": 7,
            "month_gan": 10, "month_zhi": 40,  # 提纲
            "day_gan": 0,    "day_zhi": 16,    # 日主自己不计分
            "time_gan": 8,   "time_zhi": 12
        }
        
        parts = [
            ("year_gan", self.year_gan, "gan"),
            ("year_zhi", self.year_zhi, "zhi"),
            ("month_gan", self.month_gan, "gan"),
            ("month_zhi", self.month_zhi, "zhi"),
            ("day_gan", self.day_gan, "gan"),
            ("day_zhi", self.day_zhi, "zhi"),
            ("time_gan", self.time_gan, "gan"),
            ("time_zhi", self.time_zhi, "zhi")
        ]
        
        for pos_name, item, item_type in parts:
            if pos_name == "day_gan":
                continue
            base_weight = weights[pos_name]
            
            if item_type == "gan":
                # 天干直接加分
                wx = GAN_WUXING[item]
                self.scores[wx] += base_weight
            else:
                # 地支按比例拆分
                ratios = ZHI_RATIOS.get(item, {})
                for gan_name, ratio in ratios.items():
                    wx = GAN_WUXING[gan_name]
                    self.scores[wx] += base_weight * ratio

        # 四舍五入保留1位
        for k in self.scores:
            self.scores[k] = round(self.scores[k], 1)

    # --- 模块 C: 调候与格局 ---
    def _check_climate(self):
        m = self.month_zhi
        if m in ["亥", "子", "丑"]:
            self.climate = "寒"
        elif m in ["巳", "午", "未"]:
            self.climate = "燥"

    def _determine_pattern(self):
        me_wx = GAN_WUXING[self.day_master]
        
        # 1. 找同党 (比劫 + 印枭)
        sheng_wo = self._get_relation(me_wx, "生我")
        strength_score = self.scores[me_wx] + self.scores[sheng_wo]
        
        # 2. 定格局 (简化版阈值)
        if strength_score >= 80:
            self.pattern = "专旺格"
            self.is_strong = True
        elif strength_score <= 20:
            self.pattern = "从弱格"
            self.is_strong = False
        elif strength_score >= 45:
            self.pattern = "正格(身强)"
            self.is_strong = True
        else:
            self.pattern = "正格(身弱)"
            self.is_strong = False
            
        # 3. 取喜用 (The Decision)
        ke_wo = self._get_relation(me_wx, "克我")
        wo_ke = self._get_relation(me_wx, "我克")
        wo_sheng = self._get_relation(me_wx, "我生")
        
        if "专旺" in self.pattern:
            self.favorable = [sheng_wo, me_wx, wo_sheng]
        elif "从弱" in self.pattern:
            self.favorable = [ke_wo, wo_ke, wo_sheng]
        elif self.is_strong:
            # 身强喜：克泄耗
            self.favorable = [ke_wo, wo_sheng, wo_ke]
        else:
            # 身弱喜：生扶
            self.favorable = [sheng_wo, me_wx]
            
        # 4. 调候强制修正 (Priority Override)
        if self.climate == "寒" and "火" not in self.favorable:
            self.favorable.insert(0, "火")
        elif self.climate == "燥" and "水" not in self.favorable:
            self.favorable.insert(0, "水")

    # --- 模块 D: 神煞系统 (Lookup Tables) ---
    def _calculate_shen_sha(self):
        day_gan = self.day_master
        year_zhi = self.year_zhi
        
        # 待查地支
        check_list = {
            "年": self.year_zhi,
            "月": self.month_zhi,
            "日": self.day_zhi,
            "时": self.time_zhi
        }
        
        # 1. 天乙贵人 (Day Gan -> Zhi)
        noble_map = {
            "甲": ["丑", "未"], "戊": ["丑", "未"], "庚": ["丑", "未"],
            "乙": ["子", "申"], "己": ["子", "申"],
            "丙": ["亥", "酉"], "丁": ["亥", "酉"],
            "壬": ["巳", "卯"], "癸": ["巳", "卯"],
            "辛": ["午", "寅"]
        }
        targets = noble_map.get(day_gan, [])
        for pos, zhi in check_list.items():
            if zhi in targets:
                self.shen_sha[pos].append("天乙贵人")

        # 2. 桃花 (Year Zhi -> Zhi)
        taohua_map = {
            "申": "酉", "子": "酉", "辰": "酉",
            "寅": "卯", "午": "卯", "戌": "卯",
            "巳": "午", "酉": "午", "丑": "午",
            "亥": "子", "卯": "子", "未": "子"
        }
        target = taohua_map.get(year_zhi)
        for pos, zhi in check_list.items():
            if zhi == target:
                self.shen_sha[pos].append("咸池桃花")

        # 3. 驿马 (Year Zhi -> Zhi)
        yima_map = {
            "申": "寅", "子": "寅", "辰": "寅",
            "寅": "申", "午": "申", "戌": "申",
            "巳": "亥", "酉": "亥", "丑": "亥",
            "亥": "巳", "卯": "巳", "未": "巳"
        }
        target = yima_map.get(year_zhi)
        for pos, zhi in check_list.items():
            if zhi == target:
                self.shen_sha[pos].append("驿马")

        # 4. 羊刃 (Day Gan -> Zhi)
        yangren_map = {
            "甲": "卯", "乙": "辰", "丙": "午", "丁": "未", "戊": "午",
            "己": "未", "庚": "酉", "辛": "戌", "壬": "子", "癸": "丑"
        }
        target = yangren_map.get(day_gan)
        for pos, zhi in check_list.items():
            if zhi == target:
                self.shen_sha[pos].append("羊刃")

        # 5. 华盖 (Year Zhi -> Zhi)
        huagai_map = {
            "申": "辰", "子": "辰", "辰": "辰",
            "寅": "戌", "午": "戌", "戌": "戌",
            "巳": "丑", "酉": "丑", "丑": "丑",
            "亥": "未", "卯": "未", "未": "未"
        }
        target = huagai_map.get(year_zhi)
        for pos, zhi in check_list.items():
            if zhi == target:
                self.shen_sha[pos].append("华盖")

        # 6. 文昌 (Day Gan -> Zhi)
        wenchang_map = {
            "甲": "巳", "乙": "午", "丙": "申", "丁": "酉", "戊": "申",
            "己": "酉", "庚": "亥", "辛": "子", "壬": "寅", "癸": "卯"
        }
        target = wenchang_map.get(day_gan)
        for pos, zhi in check_list.items():
            if zhi == target:
                self.shen_sha[pos].append("文昌")

    # --- 辅助方法 ---
    def _get_relation(self, me, mode):
        """五行生克字典"""
        maps = {
            "生我": {"木": "水", "火": "木", "土": "火", "金": "土", "水": "金"},
            "克我": {"木": "金", "火": "水", "土": "木", "金": "火", "水": "土"},
            "我生": {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"},
            "我克": {"木": "土", "火": "金", "土": "水", "金": "木", "水": "火"}
        }
        return maps[mode][me]

    def get_report(self):
        """返回 API 友好的字典格式"""
        return {
            "user_info": {"gender": "乾造" if self.gender == 1 else "坤造"},
            "bazi_char": [
                f"{self.year_gan}{self.year_zhi}",
                f"{self.month_gan}{self.month_zhi}",
                f"{self.day_gan}{self.day_zhi}",
                f"{self.time_gan}{self.time_zhi}"
            ],
            "energy_scores": dict(self.scores),
            "pattern": {"name": self.pattern, "strong": self.is_strong, "climate": self.climate},
            "useful_gods": self.favorable,
            "shen_sha": dict(self.shen_sha),
            "ten_gods": self.ten_gods
        }


# --- 独立的 K 线生成器函数 (供 API 调用) ---
def generate_life_trend(bazi_engine: BaziEngineV3, start_year, count=80):
    """
    根据 V3 引擎的喜用神，生成未来 N 年的运势数据
    """
    trend_data = []
    fav = bazi_engine.favorable
    day_master_wx = GAN_WUXING[bazi_engine.day_master]
    
    # 获取大运
    yun = bazi_engine.bazi.getYun(bazi_engine.gender)
    da_yun_arr = yun.getDaYun()
    
    # 遍历大运
    for dy in da_yun_arr:
        # 遍历该大运下的流年
        liu_nian_arr = dy.getLiuNian()
        for ln in liu_nian_arr:
            year = ln.getYear()
            if year < start_year:
                continue
            if year >= start_year + count:
                break
            
            # --- 1. 计算基础分 (五行喜忌) ---
            score = 50
            ganzhi = ln.getGanZhi()
            yg = ganzhi[0]  # 流年天干
            yz = ganzhi[1]  # 流年地支
            
            yg_wx = GAN_WUXING[yg]
            yz_wx = ZHI_WUXING[yz]
            
            # 天干喜用 +10
            if yg_wx in fav:
                score += 10
            elif yg_wx == bazi_engine._get_relation(day_master_wx, "克我"):
                score -= 5
            
            # 地支喜用 +20 (地支重)
            if yz_wx in fav:
                score += 20
            elif yz_wx == bazi_engine._get_relation(day_master_wx, "克我"):
                score -= 10
            
            # 调候加分 (雪中送炭)
            if bazi_engine.climate == "寒" and yz_wx == "火":
                score += 15
            elif bazi_engine.climate == "燥" and yz_wx == "水":
                score += 15
            
            # 限制分数
            score = max(10, min(95, score))
            
            # --- 2. 查找流年神煞 (Tagging) ---
            markers = []
            
            # 查流年支是否为天乙贵人
            day_gan = bazi_engine.day_master
            noble_map = {
                "甲": ["丑", "未"], "戊": ["丑", "未"], "庚": ["丑", "未"],
                "乙": ["子", "申"], "己": ["子", "申"],
                "丙": ["亥", "酉"], "丁": ["亥", "酉"],
                "壬": ["巳", "卯"], "癸": ["巳", "卯"],
                "辛": ["午", "寅"]
            }
            if yz in noble_map.get(day_gan, []):
                markers.append({"name": "天乙贵人", "icon": "🛡️", "type": "吉"})

            # 查流年是否为桃花 (年支查)
            year_zhi = bazi_engine.year_zhi
            taohua_map = {
                "申": "酉", "子": "酉", "辰": "酉",
                "寅": "卯", "午": "卯", "戌": "卯",
                "巳": "午", "酉": "午", "丑": "午",
                "亥": "子", "卯": "子", "未": "子"
            }
            if yz == taohua_map.get(year_zhi):
                markers.append({"name": "桃花", "icon": "🌸", "type": "缘"})

            # 查流年是否为驿马
            yima_map = {
                "申": "寅", "子": "寅", "辰": "寅",
                "寅": "申", "午": "申", "戌": "申",
                "巳": "亥", "酉": "亥", "丑": "亥",
                "亥": "巳", "卯": "巳", "未": "巳"
            }
            if yz == yima_map.get(year_zhi):
                markers.append({"name": "驿马", "icon": "🐎", "type": "动"})

            # 查流年是否为羊刃
            yangren_map = {
                "甲": "卯", "乙": "辰", "丙": "午", "丁": "未", "戊": "午",
                "己": "未", "庚": "酉", "辛": "戌", "壬": "子", "癸": "丑"
            }
            if yz == yangren_map.get(day_gan):
                markers.append({"name": "羊刃", "icon": "⚔️", "type": "凶"})
            
            trend_data.append({
                "year": year,
                "ganzhi": ganzhi,
                "score": score,
                "markers": markers
            })
            
            if year >= start_year + count - 1:
                return trend_data

    return trend_data
