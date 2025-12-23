import math
from collections import defaultdict
from lunar_python import Solar, Lunar

# --- 五行映射 ---
GAN_WUXING = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
ZHI_WUXING = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}

# --- V4 核心常量：地支藏干比例 ---
ZHI_RATIOS = {
    "子": {"癸": 1.0}, "丑": {"己": 0.6, "癸": 0.3, "辛": 0.1},
    "寅": {"甲": 0.6, "丙": 0.3, "戊": 0.1}, "卯": {"乙": 1.0},
    "辰": {"戊": 0.6, "乙": 0.3, "癸": 0.1}, "巳": {"丙": 0.6, "戊": 0.3, "庚": 0.1},
    "午": {"丁": 0.7, "己": 0.3}, "未": {"己": 0.6, "丁": 0.3, "乙": 0.1},
    "申": {"庚": 0.6, "壬": 0.3, "戊": 0.1}, "酉": {"辛": 1.0},
    "戌": {"戊": 0.6, "辛": 0.3, "丁": 0.1}, "亥": {"壬": 0.7, "甲": 0.3},
}

# --- V9.6 DAY MASTER IMAGERY ---
DAY_MASTER_MAP = {
    "甲": {"image": "参天大树", "icon": "🌲", "wuxing": "木", "traits": "正直 · 倔强 · 进取", "desc": "宁折不弯的栋梁之材，有极强的保护欲和进取心，但有时略显固执。"},
    "乙": {"image": "花草藤蔓", "icon": "☘️", "wuxing": "木", "traits": "柔韧 · 灵活 · 社交", "desc": "能屈能伸的社交天才，善于借力打力，生命力顽强，适应环境极快。"},
    "丙": {"image": "普照艳阳", "icon": "☀️", "wuxing": "火", "traits": "热情 · 慷慨 · 急躁", "desc": "光芒万丈的太阳，藏不住心事，充满感染力，乐于奉献但容易冲动。"},
    "丁": {"image": "暗夜烛光", "icon": "🕯️", "wuxing": "火", "traits": "细腻 · 专注 · 神秘", "desc": "外柔内刚的星星之火，洞察力极强，往往有独特的艺术天赋和内秀。"},
    "戊": {"image": "泰山磐石", "icon": "⛰️", "wuxing": "土", "traits": "稳重 · 固执 · 诚信", "desc": "不动如山的守护者，值得信赖，沉稳厚重，但有时显得不知变通。"},
    "己": {"image": "田园沃土", "icon": "🪴", "wuxing": "土", "traits": "包容 · 务实 · 内敛", "desc": "温润的培育者，多才多艺，做事周全，具有极强的包容力和策划力。"},
    "庚": {"image": "利斧刀剑", "icon": "⚔️", "wuxing": "金", "traits": "刚毅 · 义气 · 杀伐", "desc": "雷厉风行的改革者，爱憎分明，也是最讲义气的朋友，但性格刚烈。"},
    "辛": {"image": "高贵珠宝", "icon": "💎", "wuxing": "金", "traits": "精致 · 虚荣 · 敏锐", "desc": "经过打磨的宝石，追求完美和面子，往往气质出众，心思非常细腻。"},
    "壬": {"image": "江河奔流", "icon": "🌊", "wuxing": "水", "traits": "智慧 · 奔放 · 多变", "desc": "大开大合的战略家，聪明绝顶，反应极快，但有时容易冲动任性。"},
    "癸": {"image": "春雨润物", "icon": "🌧️", "wuxing": "水", "traits": "温柔 · 敏感 · 灵感", "desc": "无孔不入的渗透者，心思缜密，第六感极强，善于以柔克刚。"}
}

# --- V9.4 TAI SUI MAPPING ---
TAISUI_MAP = {
    "子": {"子": "值太岁", "午": "冲太岁", "卯": "刑太岁", "未": "害太岁", "酉": "破太岁"},
    "丑": {"丑": "值太岁", "未": "冲太岁", "戌": "刑太岁", "午": "害太岁", "辰": "破太岁"},
    "寅": {"寅": "值太岁", "申": "冲太岁", "巳": "刑太岁", "巳": "害太岁", "亥": "破太岁"},
    "卯": {"卯": "值太岁", "酉": "冲太岁", "子": "刑太岁", "辰": "害太岁", "午": "破太岁"},
    "辰": {"辰": "值太岁", "戌": "冲太岁", "辰": "刑太岁", "卯": "害太岁", "丑": "破太岁"},
    "巳": {"巳": "值太岁", "亥": "冲太岁", "申": "刑太岁", "寅": "害太岁", "申": "破太岁"},
    "午": {"午": "值太岁", "子": "冲太岁", "午": "刑太岁", "丑": "害太岁", "卯": "破太岁"},
    "未": {"未": "值太岁", "丑": "冲太岁", "戌": "刑太岁", "子": "害太岁", "戌": "破太岁"},
    "申": {"申": "值太岁", "寅": "冲太岁", "寅": "刑太岁", "亥": "害太岁", "巳": "破太岁"},
    "酉": {"酉": "值太岁", "卯": "冲太岁", "酉": "刑太岁", "戌": "害太岁", "子": "破太岁"},
    "戌": {"戌": "值太岁", "辰": "冲太岁", "未": "刑太岁", "酉": "害太岁", "未": "破太岁"},
    "亥": {"亥": "值太岁", "巳": "冲太岁", "亥": "刑太岁", "申": "害太岁", "寅": "破太岁"},
}

# --- 十神映射 ---
SHISHEN_MAP = {
    "甲": {"甲": "比肩", "乙": "劫财", "丙": "食神", "丁": "伤官", "戊": "偏财", "己": "正财", "庚": "七杀", "辛": "正官", "壬": "偏印", "癸": "正印"},
    "乙": {"乙": "比肩", "甲": "劫财", "丁": "食神", "丙": "伤官", "己": "偏财", "戊": "正财", "辛": "七杀", "庚": "正官", "癸": "偏印", "壬": "正印"},
    "丙": {"丙": "比肩", "丁": "劫财", "戊": "食神", "己": "伤官", "庚": "偏财", "辛": "正财", "壬": "七杀", "癸": "正官", "甲": "偏印", "乙": "正印"},
    "丁": {"丁": "比肩", "丙": "劫财", "己": "食神", "戊": "伤官", "辛": "偏财", "庚": "正财", "癸": "七杀", "壬": "正官", "乙": "偏印", "甲": "正印"},
    "戊": {"戊": "比肩", "己": "劫财", "庚": "食神", "辛": "伤官", "壬": "偏财", "癸": "正财", "甲": "七杀", "乙": "正官", "丙": "偏印", "丁": "正印"},
    "己": {"己": "比肩", "戊": "劫财", "辛": "食神", "庚": "伤官", "癸": "偏财", "壬": "正财", "乙": "七杀", "甲": "正官", "丁": "偏印", "丙": "正印"},
    "庚": {"庚": "比肩", "辛": "劫财", "壬": "食神", "癸": "伤官", "甲": "偏财", "乙": "正财", "丙": "七杀", "丁": "正官", "戊": "偏印", "己": "正印"},
    "辛": {"辛": "比肩", "庚": "劫财", "癸": "食神", "壬": "伤官", "乙": "偏财", "甲": "正财", "丁": "七杀", "丙": "正官", "己": "偏印", "戊": "正印"},
    "壬": {"壬": "比肩", "癸": "劫财", "甲": "食神", "乙": "伤官", "丙": "偏财", "丁": "正财", "戊": "七杀", "己": "正官", "庚": "偏印", "辛": "正印"},
    "癸": {"癸": "比肩", "壬": "劫财", "乙": "食神", "甲": "伤官", "丁": "偏财", "丙": "正财", "己": "七杀", "戊": "正官", "辛": "偏印", "庚": "正印"},
}


class BaziEngineV4:
    def __init__(self, year, month, day, hour, minute, gender, longitude):
        self.gender = gender
        self.solar = self._get_true_solar(year, month, day, hour, minute, longitude)
        self.lunar = self.solar.getLunar()
        self.bazi = self.lunar.getEightChar()
        self.bazi.setSect(2)
        
        # 获取八字各柱（字符串形式）
        self.year_gan = self.bazi.getYearGan()
        self.year_zhi = self.bazi.getYearZhi()
        self.month_gan = self.bazi.getMonthGan()
        self.month_zhi = self.bazi.getMonthZhi()
        self.day_gan = self.bazi.getDayGan()
        self.day_zhi = self.bazi.getDayZhi()
        self.time_gan = self.bazi.getTimeGan()
        self.time_zhi = self.bazi.getTimeZhi()
        
        self.day_master = self.day_gan
        self.day_gan_name = self.day_gan
        self.year_zhi_name = self.year_zhi
        
        self.scores = defaultdict(float)
        self.climate = "平"
        self.favorable = []
        
        self._calculate_energy()
        self._check_climate()
        self._determine_pattern()

    def _get_true_solar(self, y, m, d, h, min, lon):
        offset = (lon - 120.0) * 4
        total = h * 60 + min + offset
        return Solar.fromYmdHms(y, m, d, int((total/60)%24), int(total%60), 0)

    def _calculate_energy(self):
        # V5 修正版权重：加入了 day_gan (日主)
        # 总分约为 100+，但这没关系，我们最后看的是比例
        weights = {
            "year_gan": 7,   "year_zhi": 7,
            "month_gan": 10, "month_zhi": 40, # 月令权重最高 (40%)
            "day_gan": 10,   "day_zhi": 16,   # 日主 (10%) + 日支 (16%)
            "time_gan": 8,   "time_zhi": 12
        }
        
        parts = [
            ("year_gan", self.year_gan), 
            ("year_zhi", self.year_zhi),
            ("month_gan", self.month_gan), 
            ("month_zhi", self.month_zhi),
            ("day_gan", self.day_gan), # ✅ 新增：日主本人
            ("day_zhi", self.day_zhi),
            ("time_gan", self.time_gan), 
            ("time_zhi", self.time_zhi)
        ]
        
        for pos, item in parts:
            base_weight = weights[pos]
            
            if "gan" in pos:
                # 天干能量纯粹
                wx = GAN_WUXING.get(item, "土")
                self.scores[wx] += base_weight
            else:
                # 地支能量按藏干比例拆分
                zhi_name = item
                hidden_ratios = ZHI_RATIOS.get(zhi_name, {})
                for gan_name, ratio in hidden_ratios.items():
                    # 将藏干转换为五行
                    gan_wx = GAN_WUXING.get(gan_name, "土")
                    self.scores[gan_wx] += base_weight * ratio

        # 归一化处理：保留一位小数
        for k in self.scores:
            self.scores[k] = round(self.scores[k], 1)

    def _check_climate(self):
        m = self.month_zhi
        if m in ["亥", "子", "丑"]: self.climate = "寒"
        elif m in ["巳", "午", "未"]: self.climate = "燥"

    def _determine_pattern(self):
        me_wx = GAN_WUXING.get(self.day_master, "土")
        sheng_wo = self._get_rel(me_wx, "生我")
        strength = self.scores[me_wx] + self.scores[sheng_wo]
        self.is_strong = strength >= 45
        ke_wo = self._get_rel(me_wx, "克我")
        wo_ke = self._get_rel(me_wx, "我克")
        wo_sheng = self._get_rel(me_wx, "我生")
        
        if self.is_strong:
            self.favorable = [ke_wo, wo_sheng, wo_ke]
        else:
            self.favorable = [sheng_wo, me_wx]
            
        if self.climate == "寒" and "火" not in self.favorable:
            self.favorable.insert(0, "火")
        elif self.climate == "燥" and "水" not in self.favorable:
            self.favorable.insert(0, "水")

    def _get_rel(self, me, mode):
        maps = {
            "生我": {"木":"水", "火":"木", "土":"火", "金":"土", "水":"金"},
            "克我": {"木":"金", "火":"水", "土":"木", "金":"火", "水":"土"},
            "我生": {"木":"火", "火":"土", "土":"金", "金":"水", "水":"木"},
            "我克": {"木":"土", "火":"金", "土":"水", "金":"木", "水":"火"}
        }
        return maps[mode].get(me, "土")
    
    def _is_clash(self, zhi1_name, zhi2_name):
        """Check if two Earthly Branches clash (六冲)"""
        clashes = {
            "子":"午", "午":"子", 
            "丑":"未", "未":"丑", 
            "寅":"申", "申":"寅", 
            "卯":"酉", "酉":"卯", 
            "辰":"戌", "戌":"辰", 
            "巳":"亥", "亥":"巳"
        }
        return clashes.get(zhi1_name) == zhi2_name
    
    def get_bazi_info(self):
        """获取八字基本信息"""
        return {
            "year_gan": self.year_gan,
            "year_zhi": self.year_zhi,
            "month_gan": self.month_gan,
            "month_zhi": self.month_zhi,
            "day_gan": self.day_gan,
            "day_zhi": self.day_zhi,
            "time_gan": self.time_gan,
            "time_zhi": self.time_zhi,
        }
    
    def get_energy_scores(self):
        """获取五行能量分数"""
        return dict(self.scores)
    
    def get_day_master_info(self):
        """V9.6: 获取日主元神信息"""
        day_gan = self.day_gan
        info = DAY_MASTER_MAP.get(day_gan, {})
        return {
            "gan": day_gan,
            "wuxing": info.get("wuxing", "未知"),
            "image": info.get("image", "未知"),
            "icon": info.get("icon", "❓"),
            "traits": info.get("traits", ""),
            "description": info.get("desc", "")
        }


# --- V4 核心：神煞查表 ---
# 1. 天乙贵人 (日干查流年支)
NOBLE_MAP = {"甲":["丑","未"], "戊":["丑","未"], "庚":["丑","未"], "乙":["子","申"], "己":["子","申"], "丙":["亥","酉"], "丁":["亥","酉"], "壬":["巳","卯"], "癸":["巳","卯"], "辛":["午","寅"]}
# 2. 桃花/咸池 (年支查流年支)
TAOHUA_MAP = {"申":"酉", "子":"酉", "辰":"酉", "寅":"卯", "午":"卯", "戌":"卯", "巳":"午", "酉":"午", "丑":"午", "亥":"子", "卯":"子", "未":"子"}
# 3. 驿马 (年支查流年支)
YIMA_MAP = {"申":"寅", "子":"寅", "辰":"寅", "寅":"申", "午":"申", "戌":"申", "巳":"亥", "酉":"亥", "丑":"亥", "亥":"巳", "卯":"巳", "未":"巳"}
# 4. 红鸾天喜 (年支查流年支) - 婚恋大宿
HONGLUAN_MAP = {"子":"卯", "丑":"寅", "寅":"丑", "卯":"子", "辰":"亥", "巳":"戌", "午":"酉", "未":"申", "申":"未", "酉":"午", "戌":"巳", "亥":"辰"}
# 5. 文昌贵人 (日干查流年支) - 学业事业
WENCHANG_MAP = {"甲":"巳", "乙":"午", "丙":"申", "戊":"申", "丁":"酉", "己":"酉", "庚":"亥", "辛":"子", "壬":"寅", "癸":"卯"}
# 6. 华盖 (年支查流年支) - 艺术孤独
HUAGAI_MAP = {"申":"辰", "子":"辰", "辰":"辰", "寅":"戌", "午":"戌", "戌":"戌", "巳":"丑", "酉":"丑", "丑":"丑", "亥":"未", "卯":"未", "未":"未"}
# 7. 禄神 (日干查流年支) - 财禄享受
LU_MAP = {"甲":"寅", "乙":"卯", "丙":"巳", "丁":"午", "戊":"巳", "己":"午", "庚":"申", "辛":"酉", "壬":"亥", "癸":"子"}
# 8. 病符 (年支查流年支) - 健康不佳
BINGFU_MAP = {"子":"巳", "丑":"午", "寅":"未", "卯":"申", "辰":"酉", "巳":"戌", "午":"亥", "未":"子", "申":"丑", "酉":"寅", "戌":"卯", "亥":"辰"}
# 9. 丧门 (年支查流年支) - 丧事凶星
SANGMEN_MAP = {"子":"寅", "丑":"卯", "寅":"辰", "卯":"巳", "辰":"午", "巳":"未", "午":"申", "未":"酉", "申":"戌", "酉":"亥", "戌":"子", "亥":"丑"}
# 10. 劫煞 (年支查流年支) - 破财凶星
JIESHA_MAP = {"申":"巳", "子":"巳", "辰":"巳", "寅":"亥", "午":"亥", "戌":"亥", "巳":"寅", "酉":"寅", "丑":"寅", "亥":"申", "卯":"申", "未":"申"}
# 11. 天德贵人 (月支查流年干)
TIANDE_MAP = {"寅":"丁", "卯":"申", "辰":"壬", "巳":"辛", "午":"亥", "未":"甲", "申":"癸", "酉":"寅", "戌":"丙", "亥":"乙", "子":"巳", "丑":"庚"}
# 12. 月德贵人 (月支查流年干)
YUEDE_MAP = {"寅":"丙", "午":"丙", "戌":"丙", "申":"壬", "子":"壬", "辰":"壬", "巳":"庚", "酉":"庚", "丑":"庚", "亥":"甲", "卯":"甲", "未":"甲"}


def _get_shishen(day_gan, target_gan):
    """获取十神"""
    return SHISHEN_MAP.get(day_gan, {}).get(target_gan, "")


def _calculate_dimension_score(base_score, dimension, year_gan, year_zhi, engine, markers):
    """计算各维度分数"""
    dg = engine.day_gan_name
    yz_orig = engine.year_zhi_name
    mz = engine.month_zhi
    fav = engine.favorable
    
    yg_wx = GAN_WUXING.get(year_gan, "土")
    yz_wx = ZHI_WUXING.get(year_zhi, "土")
    
    # 获取十神
    shishen = _get_shishen(dg, year_gan)
    
    score = base_score
    dim_markers = []
    
    if dimension == "career":  # 事业运
        # 事业相关十神：正官、七杀、正印、偏印
        career_shishen = ["正官", "七杀", "正印", "偏印"]
        if shishen in career_shishen:
            score += 15
        
        # 文昌贵人利事业
        if year_zhi == WENCHANG_MAP.get(dg):
            score += 12
            dim_markers.append({"name": "文昌贵人", "icon": "📜", "type": "吉", "desc": "才思敏捷，利考学职，事业有成"})
        
        # 天乙贵人利事业
        if year_zhi in NOBLE_MAP.get(dg, []):
            score += 10
            dim_markers.append({"name": "天乙贵人", "icon": "🛡️", "type": "吉", "desc": "贵人相助，事业顺遂"})
        
        # 天德月德利事业
        if year_gan == TIANDE_MAP.get(mz):
            score += 8
            dim_markers.append({"name": "天德贵人", "icon": "⭐", "type": "吉", "desc": "逢凶化吉，事业稳定"})
        
        # 驿马主变动
        if year_zhi == YIMA_MAP.get(yz_orig):
            score -= 5  # 事业变动
            dim_markers.append({"name": "驿马", "icon": "🐎", "type": "动", "desc": "事业变动，可能换工作或出差"})
        
        # 七杀无制主事业波折
        if shishen == "七杀" and "正印" not in [_get_shishen(dg, g) for g in ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]]:
            score -= 8
            dim_markers.append({"name": "七杀无制", "icon": "⚠️", "type": "凶", "desc": "事业压力大，小人作祟"})
            
    elif dimension == "wealth":  # 财运
        # 财运相关十神：正财、偏财、食神、伤官
        wealth_shishen = ["正财", "偏财", "食神", "伤官"]
        if shishen in wealth_shishen:
            score += 15
        
        # 禄神主财
        if year_zhi == LU_MAP.get(dg):
            score += 18
            dim_markers.append({"name": "禄神临门", "icon": "💰", "type": "吉", "desc": "财运亨通，收入增加"})
        
        # 天乙贵人利财
        if year_zhi in NOBLE_MAP.get(dg, []):
            score += 8
            dim_markers.append({"name": "天乙贵人", "icon": "🛡️", "type": "吉", "desc": "贵人相助，财运顺利"})
        
        # 劫煞主破财
        if year_zhi == JIESHA_MAP.get(yz_orig):
            score -= 20
            dim_markers.append({"name": "劫煞", "icon": "💸", "type": "凶", "desc": "破财之年，谨慎投资"})
        
        # 比肩劫财主破财
        if shishen in ["比肩", "劫财"]:
            score -= 10
            dim_markers.append({"name": "比劫夺财", "icon": "⚠️", "type": "凶", "desc": "钱财易散，防小人"})
            
    elif dimension == "health":  # 健康运
        # 病符主健康问题
        if year_zhi == BINGFU_MAP.get(yz_orig):
            score -= 25
            dim_markers.append({"name": "病符", "icon": "🏥", "type": "凶", "desc": "健康欠佳，注意身体"})
        
        # 丧门主凶
        if year_zhi == SANGMEN_MAP.get(yz_orig):
            score -= 15
            dim_markers.append({"name": "丧门", "icon": "⚰️", "type": "凶", "desc": "注意长辈健康，防意外"})
        
        # 天德月德化解
        if year_gan == TIANDE_MAP.get(mz) or year_gan == YUEDE_MAP.get(mz):
            score += 15
            dim_markers.append({"name": "天德护佑", "icon": "✨", "type": "吉", "desc": "逢凶化吉，健康无虞"})
        
        # 天乙贵人化解
        if year_zhi in NOBLE_MAP.get(dg, []):
            score += 10
            dim_markers.append({"name": "天乙贵人", "icon": "🛡️", "type": "吉", "desc": "贵人相助，健康平安"})
        
        # 印星主健康
        if shishen in ["正印", "偏印"]:
            score += 8
            
    elif dimension == "love":  # 姻缘运
        # 红鸾主婚恋
        if year_zhi == HONGLUAN_MAP.get(yz_orig):
            score += 25
            dim_markers.append({"name": "红鸾星动", "icon": "💍", "type": "吉", "desc": "婚恋大吉，喜事临门"})
        
        # 桃花主异性缘
        if year_zhi == TAOHUA_MAP.get(yz_orig):
            score += 15
            dim_markers.append({"name": "咸池桃花", "icon": "🌸", "type": "缘", "desc": "异性缘旺，桃花朵朵"})
        
        # 天喜主喜事
        tianxi_map = {"子":"酉", "丑":"申", "寅":"未", "卯":"午", "辰":"巳", "巳":"辰", "午":"卯", "未":"寅", "申":"丑", "酉":"子", "戌":"亥", "亥":"戌"}
        if year_zhi == tianxi_map.get(yz_orig):
            score += 12
            dim_markers.append({"name": "天喜", "icon": "🎊", "type": "吉", "desc": "喜事临门，感情顺利"})
        
        # 华盖主孤独
        if year_zhi == HUAGAI_MAP.get(yz_orig):
            score -= 10
            dim_markers.append({"name": "华盖", "icon": "🎨", "type": "平", "desc": "才华横溢，但感情上可能有些孤僻"})
        
        # 驿马主分离
        if year_zhi == YIMA_MAP.get(yz_orig):
            score -= 8
            dim_markers.append({"name": "驿马", "icon": "🐎", "type": "动", "desc": "聚少离多，异地恋情"})
        
        # 正财正官主婚姻（男看正财，女看正官）
        if engine.gender == 1 and shishen == "正财":  # 男
            score += 12
            dim_markers.append({"name": "正财临门", "icon": "💑", "type": "吉", "desc": "婚姻宫动，利婚恋"})
        elif engine.gender == 0 and shishen == "正官":  # 女
            score += 12
            dim_markers.append({"name": "正官临门", "icon": "💑", "type": "吉", "desc": "婚姻宫动，利婚恋"})
    
    # 确保分数在合理范围内
    score = max(15, min(95, score))
    
    return score, dim_markers


# --- V4 核心：多维度K线生成器 ---
def generate_life_trend_v4(engine: BaziEngineV4, start_year, count=80):
    """生成综合运势K线数据"""
    trend_data = []
    fav = engine.favorable
    yun = engine.bazi.getYun(engine.gender)
    dg = engine.day_gan_name
    yz_orig = engine.year_zhi_name

    year = start_year
    for dy in yun.getDaYun():
        for ln in dy.getLiuNian():
            year = ln.getYear()
            if year < start_year:
                continue
            if year >= start_year + count:
                break
            
            gz = ln.getGanZhi()
            yg, yz = gz[0], gz[1]
            yg_wx = GAN_WUXING.get(yg, "土")
            yz_wx = ZHI_WUXING.get(yz, "土")
            
            # 1. 计算基础分
            score = 50
            if yg_wx in fav:
                score += 10
            if yz_wx in fav:
                score += 20
            if engine.climate == "寒" and yz_wx == "火":
                score += 15  # 调候加分
            score = max(15, min(95, score)) + (hash(str(year)) % 10 - 5)  # 加点随机噪点让曲线更自然

            # 2. 查找流年神煞 (Tagging)
            markers = []
            if yz in NOBLE_MAP.get(dg, []):
                markers.append({"name": "天乙贵人", "icon": "🛡️", "type": "吉", "desc": "逢凶化吉，遇难呈祥"})
            if yz == TAOHUA_MAP.get(yz_orig):
                markers.append({"name": "咸池桃花", "icon": "🌸", "type": "缘", "desc": "异性缘旺，人际活跃"})
            if yz == YIMA_MAP.get(yz_orig):
                markers.append({"name": "驿马", "icon": "🐎", "type": "动", "desc": "奔波变动，远行搬迁"})
            if yz == HONGLUAN_MAP.get(yz_orig):
                markers.append({"name": "红鸾星动", "icon": "💍", "type": "缘", "desc": "婚恋大吉，喜事临门"})
            if yz == WENCHANG_MAP.get(dg):
                markers.append({"name": "文昌贵人", "icon": "📜", "type": "吉", "desc": "才思敏捷，利考学职"})
            if yz == HUAGAI_MAP.get(yz_orig):
                markers.append({"name": "华盖", "icon": "🎨", "type": "平", "desc": "才华横溢，但这年可能有点孤僻"})
            if yz == LU_MAP.get(dg):
                markers.append({"name": "禄神临门", "icon": "💰", "type": "吉", "desc": "财运亨通，享受增加"})

            trend_data.append({"year": year, "ganzhi": f"{yg}{yz}", "score": score, "markers": markers})
            
        if year >= start_year + count:
            break
    return trend_data


def generate_multi_dimension_trend(engine: BaziEngineV4, start_year, count=80):
    """生成多维度K线数据（综合、事业、财运、健康、姻缘、父母运、子女运）"""
    dimensions = {
        "overall": {"name": "综合运势", "data": []},
        "career": {"name": "事业运", "data": []},
        "wealth": {"name": "财运", "data": []},
        "health": {"name": "健康运", "data": []},
        "love": {"name": "姻缘运", "data": []},
        "parents": {"name": "父母运", "data": []},
        "children": {"name": "子女运", "data": []}
    }
    
    fav = engine.favorable
    yun = engine.bazi.getYun(engine.gender)
    dg = engine.day_gan_name
    yz_orig = engine.year_zhi_name

    year = start_year
    for dy in yun.getDaYun():
        for ln in dy.getLiuNian():
            year = ln.getYear()
            if year < start_year:
                continue
            if year >= start_year + count:
                break
            
            gz = ln.getGanZhi()
            yg, yz = gz[0], gz[1]
            yg_wx = GAN_WUXING.get(yg, "土")
            yz_wx = ZHI_WUXING.get(yz, "土")
            
            # 1. 计算综合基础分
            base_score = 50
            if yg_wx in fav:
                base_score += 10
            if yz_wx in fav:
                base_score += 20
            if engine.climate == "寒" and yz_wx == "火":
                base_score += 15
            base_score = max(15, min(95, base_score)) + (hash(str(year)) % 10 - 5)

            # 2. V9.4 太岁逻辑
            user_yz = engine.year_zhi  # 用户的年支
            curr_yz = yz  # 当前流年地支
            
            ts_type = TAISUI_MAP.get(curr_yz, {}).get(user_yz)
            taisui_penalty = 0
            taisui_marker = None
            if ts_type:
                ts_icon = {"值太岁": "🔴", "冲太岁": "💥", "刑太岁": "⚔️", "害太岁": "🐍", "破太岁": "💔"}
                taisui_marker = {
                    "name": ts_type,
                    "icon": ts_icon.get(ts_type, "⚠️"),
                    "type": "凶",
                    "desc": f"{ts_type}，注意化解"
                }
                # 太岁惩罚分数
                if ts_type == "冲太岁":
                    taisui_penalty = 15
                elif ts_type == "值太岁":
                    taisui_penalty = 10
                else:
                    taisui_penalty = 5
            
            # 应用太岁惩罚到基础分
            base_score -= taisui_penalty
            base_score = max(15, min(95, base_score))
            
            # 3. 综合运势神煎
            overall_markers = []
            if taisui_marker:
                overall_markers.append(taisui_marker)
            if yz in NOBLE_MAP.get(dg, []):
                overall_markers.append({"name": "天乙贵人", "icon": "🛡️", "type": "吉", "desc": "逢凶化吉，遇难呈祥"})
            if yz == TAOHUA_MAP.get(yz_orig):
                overall_markers.append({"name": "咸池桃花", "icon": "🌸", "type": "缘", "desc": "异性缘旺，人际活跃"})
            if yz == YIMA_MAP.get(yz_orig):
                overall_markers.append({"name": "驿马", "icon": "🐎", "type": "动", "desc": "奔波变动，远行搬迁"})
            if yz == HONGLUAN_MAP.get(yz_orig):
                overall_markers.append({"name": "红鸾星动", "icon": "💍", "type": "缘", "desc": "婚恋大吉，喜事临门"})
            if yz == WENCHANG_MAP.get(dg):
                overall_markers.append({"name": "文昌贵人", "icon": "📜", "type": "吉", "desc": "才思敏捷，利考学职"})
            if yz == HUAGAI_MAP.get(yz_orig):
                overall_markers.append({"name": "华盖", "icon": "🎨", "type": "平", "desc": "才华横溢，但这年可能有点孤僻"})
            if yz == LU_MAP.get(dg):
                overall_markers.append({"name": "禄神临门", "icon": "💰", "type": "吉", "desc": "财运亨通，享受增加"})

            dimensions["overall"]["data"].append({
                "year": year, 
                "ganzhi": f"{yg}{yz}", 
                "score": base_score, 
                "markers": overall_markers
            })
            
            # 3. 计算各维度分数
            for dim_key in ["career", "wealth", "health", "love"]:
                dim_score, dim_markers = _calculate_dimension_score(
                    base_score, dim_key, yg, yz, engine, overall_markers
                )
                # 添加一些随机波动使曲线更自然
                dim_score += (hash(f"{year}{dim_key}") % 8 - 4)
                dim_score = max(15, min(95, dim_score))
                
                dimensions[dim_key]["data"].append({
                    "year": year,
                    "ganzhi": f"{yg}{yz}",
                    "score": dim_score,
                    "markers": dim_markers
                })
            
            # 4. 计算父母运 (Parents Luck)
            me_wx = GAN_WUXING.get(engine.day_gan, "土")
            resource_star = engine._get_rel(me_wx, "生我")  # 印星 (母)
            wealth_star = engine._get_rel(me_wx, "我克")    # 财星 (父)
            
            p_score = 60  # 基础分
            p_markers = []
            
            # 冶: 流年支冲父母宫/年柱
            if engine._is_clash(yz, engine.month_zhi):
                p_score -= 25  # 冲提纲，动荡
                p_markers.append({"name": "冲月柱", "icon": "⚠️", "type": "冶", "desc": "冲提纲，父母宫动荡，注意父母健康"})
            if engine._is_clash(yz, engine.year_zhi):
                p_score -= 10
                p_markers.append({"name": "冲年柱", "icon": "⚠️", "type": "冶", "desc": "冲年柱，祖业宫动荡"})
            
            # 吉: 流年生母亲或父亲星
            if yg_wx == resource_star or yz_wx == resource_star:
                p_score += 10
                p_markers.append({"name": "印星临门", "icon": "👩", "type": "吉", "desc": "母亲星旺，母亲运势佳"})
            if yg_wx == wealth_star or yz_wx == wealth_star:
                p_score += 10
                p_markers.append({"name": "财星临门", "icon": "👨", "type": "吉", "desc": "父亲星旺，父亲运势佳"})
            
            # 天乙贵人化解
            if yz in NOBLE_MAP.get(dg, []):
                p_score += 8
                p_markers.append({"name": "贵人护佑", "icon": "🛡️", "type": "吉", "desc": "贵人相助，父母平安"})
            
            p_score = max(20, min(95, p_score)) + (hash(f"{year}parents") % 6 - 3)
            p_score = max(20, min(95, p_score))
            
            dimensions["parents"]["data"].append({
                "year": year,
                "ganzhi": f"{yg}{yz}",
                "score": p_score,
                "markers": p_markers
            })
            
            # 5. 计算子女运 (Children Luck)
            if engine.gender == 1:  # 男
                child_star = engine._get_rel(me_wx, "克我")  # 官杀
            else:  # 女
                child_star = engine._get_rel(me_wx, "我生")  # 食伤
            
            c_score = 60  # 基础分
            c_markers = []
            
            # 冶: 流年支冲子女宫 (时柱)
            if engine._is_clash(yz, engine.time_zhi):
                c_score -= 30  # 冲时柱，最忌
                c_markers.append({"name": "冲时柱", "icon": "⚠️", "type": "冶", "desc": "冲子女宫，注意子女健康安全"})
            
            # 吉: 流年匹配子女星
            if yg_wx == child_star or yz_wx == child_star:
                c_score += 15
                c_markers.append({"name": "子女星旺", "icon": "👶", "type": "吉", "desc": "子女星临门，子女运势佳"})
            
            # 天乙贵人化解
            if yz in NOBLE_MAP.get(dg, []):
                c_score += 8
                c_markers.append({"name": "贵人护佑", "icon": "🛡️", "type": "吉", "desc": "贵人相助，子女平安"})
            
            # 红鸾天喜利子女
            if yz == HONGLUAN_MAP.get(yz_orig):
                c_score += 10
                c_markers.append({"name": "红鸾天喜", "icon": "🎉", "type": "吉", "desc": "喜事临门，利子女"})
            
            c_score = max(20, min(95, c_score)) + (hash(f"{year}children") % 6 - 3)
            c_score = max(20, min(95, c_score))
            
            dimensions["children"]["data"].append({
                "year": year,
                "ganzhi": f"{yg}{yz}",
                "score": c_score,
                "markers": c_markers
            })
            
        if year >= start_year + count:
            break
    
    return dimensions


def get_dayun_info(engine: BaziEngineV4):
    """获取大运信息"""
    yun = engine.bazi.getYun(engine.gender)
    dayun_list = []
    for dy in yun.getDaYun():
        if dy.getIndex() == 0:
            continue
        dayun_list.append({
            "ganzhi": dy.getGanZhi(),
            "start_year": dy.getStartYear(),
            "end_year": dy.getEndYear(),
            "start_age": dy.getStartAge(),
        })
    return dayun_list
