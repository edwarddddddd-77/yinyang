# backend/main.py
# YinYang V9.3 - Real AI Powered (DeepSeek)

import sys
import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI  # <--- MUST HAVE THIS

# --- 1. System Setup ---
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.engine_v4 import BaziEngineV4, generate_multi_dimension_trend, get_dayun_info

# Import City Data
try:
    from data.cities_full import CITY_DATA
except ImportError:
    CITY_DATA = {'北京市': [{'name': '北京', 'longitude': 116.41}]}

app = FastAPI(title="YinYang V9.3 - Real AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. DeepSeek Configuration ---
DEEPSEEK_API_KEY = "sk-f00d603b8c704f238c22f4edd0020998" # Verified Key
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# --- 3. Models ---
class BirthInfo(BaseModel):
    nickname: str = "用户"
    year: int
    month: int
    day: int
    hour: int
    minute: int
    gender: int  # 1=男, 0=女
    is_lunar: bool = False
    province: str = ""
    city: str = ""
    city_long: float = 120.0

class BaziRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    gender: int
    city_name: str
    province_name: str

class AnalyzeYearRequest(BaseModel):
    user_bazi: Dict[str, Any]
    target_year: int
    year_gan: str
    year_zhi: str
    year_score: float
    shensha: List[str]
    dimension: str = "overall"
    pattern: Optional[str] = "未知"
    fav_gods: Optional[List[str]] = []

# --- 4. The Real AI Function ---
def generate_real_ai_analysis(user_bazi, target_year, year_gan, year_zhi, year_score, shensha, dimension, pattern, fav_gods):
    # System Prompt for DeepSeek
    system_prompt = """
    你是一位隐居终南山的国学大师，精通《三命通会》、《滴天髓》。
    请为求测者撰写流年运程判词。
    风格要求：半文半白，引用古籍断语，一针见血。
    结构：先断吉凶，再论神煞，最后给一条具体的行动建议。
    字数：150字以内。
    """
    
    user_prompt = f"""
    【命盘】格局：{pattern} (喜用：{', '.join(fav_gods) if fav_gods else '未知'})
    【流年】{target_year}年 ({year_gan}{year_zhi})
    【维度】{dimension}
    【评分】{year_score}分
    【神煎】{', '.join(shensha) if shensha else '无'}
    (注意：若有"值太岁/冲太岁/刑太岁/害太岁/破太岁"等，请务必在判词中专门警示并给出化解之法，如穿红、拜太岁、佩戴太岁符等)
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=1.3,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"DeepSeek Error: {e}")
        return f"【天机暂隐】(AI连接中断) 此年运势 {year_score} 分。建议稳中求进。"

# --- 5. Endpoints ---
@app.get("/")
async def root():
    return {"message": "YinYang V9.6 - Soul Element", "version": "9.6-soul"}

@app.get("/api/provinces")
async def get_provinces():
    return {"provinces": list(CITY_DATA.keys())}

@app.get("/api/cities/{province}")
async def get_cities_by_province(province: str):
    if province in CITY_DATA:
        return {"cities": CITY_DATA[province]}
    return {"cities": []}

@app.get("/api/cities")
def get_cities():
    return CITY_DATA

@app.post("/api/calculate")
async def calculate(info: BirthInfo):
    try:
        # 创建V4引擎
        engine = BaziEngineV4(
            year=info.year,
            month=info.month,
            day=info.day,
            hour=info.hour,
            minute=info.minute,
            gender=info.gender,
            longitude=info.city_long
        )
        
        # 获取八字信息
        bazi_info = engine.get_bazi_info()
        
        # 获取五行能量
        energy_scores = engine.get_energy_scores()
        
        # 获取大运信息
        dayun_list = get_dayun_info(engine)
        
        # 生成多维度K线数据
        multi_trend = generate_multi_dimension_trend(engine, info.year, 80)
        
        # 计算真太阳时校正
        true_solar_offset = (info.city_long - 120.0) * 4
        
        # 构建响应
        response = {
            "success": True,
            "data": {
                "nickname": info.nickname,
                "birth_info": {
                    "solar": f"{info.year}年{info.month}月{info.day}日 {info.hour}时{info.minute}分",
                    "location": f"{info.province} {info.city}",
                    "longitude": info.city_long,
                    "true_solar_offset": round(true_solar_offset, 1),
                },
                "bazi": {
                    "pillars": [
                        {"name": "年柱", "gan": bazi_info["year_gan"], "zhi": bazi_info["year_zhi"]},
                        {"name": "月柱", "gan": bazi_info["month_gan"], "zhi": bazi_info["month_zhi"]},
                        {"name": "日柱", "gan": bazi_info["day_gan"], "zhi": bazi_info["day_zhi"]},
                        {"name": "时柱", "gan": bazi_info["time_gan"], "zhi": bazi_info["time_zhi"]},
                    ],
                    "day_master": bazi_info["day_gan"],
                    "climate": engine.climate,
                    "favorable": engine.favorable,
                    "energy_scores": energy_scores,
                },
                "dayun": dayun_list,
                "life_trend": multi_trend["overall"]["data"],
                "multi_dimension_trend": multi_trend,
                "gender": "乾造" if info.gender == 1 else "坤造",
                "meta": {
                    "pattern": engine.climate,
                    "fav_gods": engine.favorable,
                    "soul": engine.get_day_master_info()  # V9.6: 日主元神
                }
            }
        }
        
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/calculate_v2")
def calculate_v2(req: BaziRequest):
    """V2 计算接口"""
    province_cities = CITY_DATA.get(req.province_name, [])
    city_info = next((c for c in province_cities if c['name'] == req.city_name), None)
    longitude = city_info['longitude'] if city_info else 120.0
    
    engine = BaziEngineV4(req.year, req.month, req.day, req.hour, req.minute, req.gender, longitude)
    trend_data = generate_multi_dimension_trend(engine, req.year)
    bazi_info = engine.get_bazi_info()
    
    return {
        "bazi": bazi_info,
        "trend": trend_data,
        "meta": {
            "city": req.city_name, 
            "longitude": longitude,
            "pattern": engine.climate,
            "fav_gods": engine.favorable
        }
    }

@app.post("/api/analyze_year")
async def analyze_year(request: AnalyzeYearRequest):
    dim_map = {
        "overall": "综合运势", "career": "仕途事业", "wealth": "正财偏财",
        "love": "姻缘桃花", "health": "身体发肤", "parents": "高堂父母", "children": "子孙后代"
    }
    dim_label = dim_map.get(request.dimension, "流年运势")
    
    analysis_text = generate_real_ai_analysis(
        user_bazi=request.user_bazi,
        target_year=request.target_year,
        year_gan=request.year_gan,
        year_zhi=request.year_zhi,
        year_score=request.year_score,
        shensha=request.shensha,
        dimension=dim_label,
        pattern=request.pattern,
        fav_gods=request.fav_gods
    )
    
    return {
        "success": True, 
        "data": {
            "analysis_text": analysis_text,
            "year": request.target_year,
            "score": request.year_score,
            "dimension": request.dimension
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
