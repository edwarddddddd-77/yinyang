# backend/data/cities_full.py
# 全量中国城市经度数据库 - 用于真太阳时校正

CITY_DATA = {
    '北京市': [{'name': '北京', 'longitude': 116.41}],
    '天津市': [{'name': '天津', 'longitude': 117.20}],
    '上海市': [{'name': '上海', 'longitude': 121.47}],
    '重庆市': [{'name': '重庆', 'longitude': 106.55}, {'name': '万州', 'longitude': 108.39}, {'name': '涪陵', 'longitude': 107.39}],
    '河北省': [
        {'name': '石家庄', 'longitude': 114.48}, {'name': '唐山', 'longitude': 118.18}, {'name': '秦皇岛', 'longitude': 119.57},
        {'name': '邯郸', 'longitude': 114.47}, {'name': '邢台', 'longitude': 114.48}, {'name': '保定', 'longitude': 115.48},
        {'name': '张家口', 'longitude': 114.87}, {'name': '承德', 'longitude': 117.93}, {'name': '沧州', 'longitude': 116.83},
        {'name': '廊坊', 'longitude': 116.70}, {'name': '衡水', 'longitude': 115.72}
    ],
    '山西省': [
        {'name': '太原', 'longitude': 112.53}, {'name': '大同', 'longitude': 113.29}, {'name': '阳泉', 'longitude': 113.57},
        {'name': '长治', 'longitude': 113.08}, {'name': '晋城', 'longitude': 112.82}, {'name': '朔州', 'longitude': 112.43},
        {'name': '晋中', 'longitude': 112.74}, {'name': '运城', 'longitude': 111.00}, {'name': '忻州', 'longitude': 112.72},
        {'name': '临汾', 'longitude': 111.51}, {'name': '吕梁', 'longitude': 111.13}
    ],
    '内蒙古': [
        {'name': '呼和浩特', 'longitude': 111.65}, {'name': '包头', 'longitude': 109.83}, {'name': '乌海', 'longitude': 106.82},
        {'name': '赤峰', 'longitude': 118.96}, {'name': '通辽', 'longitude': 122.19}, {'name': '鄂尔多斯', 'longitude': 109.78},
        {'name': '呼伦贝尔', 'longitude': 119.75}, {'name': '巴彦淖尔', 'longitude': 107.41}, {'name': '乌兰察布', 'longitude': 113.09}
    ],
    '辽宁省': [
        {'name': '沈阳', 'longitude': 123.43}, {'name': '大连', 'longitude': 121.62}, {'name': '鞍山', 'longitude': 122.99},
        {'name': '抚顺', 'longitude': 123.97}, {'name': '本溪', 'longitude': 123.73}, {'name': '丹东', 'longitude': 124.37},
        {'name': '锦州', 'longitude': 121.15}, {'name': '营口', 'longitude': 122.18}, {'name': '阜新', 'longitude': 121.66},
        {'name': '辽阳', 'longitude': 123.18}, {'name': '盘锦', 'longitude': 122.06}, {'name': '铁岭', 'longitude': 123.84},
        {'name': '朝阳', 'longitude': 120.44}, {'name': '葫芦岛', 'longitude': 120.85}
    ],
    '吉林省': [
        {'name': '长春', 'longitude': 125.32}, {'name': '吉林', 'longitude': 126.57}, {'name': '四平', 'longitude': 124.37},
        {'name': '辽源', 'longitude': 125.15}, {'name': '通化', 'longitude': 125.92}, {'name': '白山', 'longitude': 126.40},
        {'name': '松原', 'longitude': 124.82}, {'name': '白城', 'longitude': 122.84}, {'name': '延边', 'longitude': 129.51}
    ],
    '黑龙江省': [
        {'name': '哈尔滨', 'longitude': 126.63}, {'name': '齐齐哈尔', 'longitude': 123.97}, {'name': '鸡西', 'longitude': 130.97},
        {'name': '鹤岗', 'longitude': 130.28}, {'name': '双鸭山', 'longitude': 131.16}, {'name': '大庆', 'longitude': 125.11},
        {'name': '伊春', 'longitude': 128.91}, {'name': '佳木斯', 'longitude': 130.35}, {'name': '七台河', 'longitude': 131.02},
        {'name': '牡丹江', 'longitude': 129.62}, {'name': '黑河', 'longitude': 127.53}, {'name': '绥化', 'longitude': 126.97}
    ],
    '江苏省': [
        {'name': '南京', 'longitude': 118.78}, {'name': '无锡', 'longitude': 120.30}, {'name': '徐州', 'longitude': 117.18},
        {'name': '常州', 'longitude': 119.98}, {'name': '苏州', 'longitude': 120.62}, {'name': '南通', 'longitude': 120.86},
        {'name': '连云港', 'longitude': 119.16}, {'name': '淮安', 'longitude': 119.02}, {'name': '盐城', 'longitude': 120.13},
        {'name': '扬州', 'longitude': 119.42}, {'name': '镇江', 'longitude': 119.44}, {'name': '泰州', 'longitude': 119.90},
        {'name': '宿迁', 'longitude': 118.28}
    ],
    '浙江省': [
        {'name': '杭州', 'longitude': 120.16}, {'name': '宁波', 'longitude': 121.56}, {'name': '温州', 'longitude': 120.65},
        {'name': '嘉兴', 'longitude': 120.76}, {'name': '湖州', 'longitude': 120.10}, {'name': '绍兴', 'longitude': 120.58},
        {'name': '金华', 'longitude': 119.64}, {'name': '衢州', 'longitude': 118.88}, {'name': '舟山', 'longitude': 122.10},
        {'name': '台州', 'longitude': 121.43}, {'name': '丽水', 'longitude': 119.92}
    ],
    '安徽省': [
        {'name': '合肥', 'longitude': 117.27}, {'name': '芜湖', 'longitude': 118.38}, {'name': '蚌埠', 'longitude': 117.34},
        {'name': '淮南', 'longitude': 116.98}, {'name': '马鞍山', 'longitude': 118.51}, {'name': '淮北', 'longitude': 116.80},
        {'name': '铜陵', 'longitude': 117.82}, {'name': '安庆', 'longitude': 117.04}, {'name': '黄山', 'longitude': 118.31},
        {'name': '滁州', 'longitude': 118.31}, {'name': '阜阳', 'longitude': 115.82}, {'name': '宿州', 'longitude': 116.97},
        {'name': '六安', 'longitude': 116.50}, {'name': '亳州', 'longitude': 115.78}, {'name': '池州', 'longitude': 117.48},
        {'name': '宣城', 'longitude': 118.75}
    ],
    '福建省': [
        {'name': '福州', 'longitude': 119.30}, {'name': '厦门', 'longitude': 118.10}, {'name': '莆田', 'longitude': 119.00},
        {'name': '三明', 'longitude': 117.64}, {'name': '泉州', 'longitude': 118.58}, {'name': '漳州', 'longitude': 117.66},
        {'name': '南平', 'longitude': 118.17}, {'name': '龙岩', 'longitude': 117.03}, {'name': '宁德', 'longitude': 119.52}
    ],
    '江西省': [
        {'name': '南昌', 'longitude': 115.89}, {'name': '景德镇', 'longitude': 117.18}, {'name': '萍乡', 'longitude': 113.85},
        {'name': '九江', 'longitude': 115.97}, {'name': '新余', 'longitude': 114.92}, {'name': '鹰潭', 'longitude': 117.03},
        {'name': '赣州', 'longitude': 114.94}, {'name': '吉安', 'longitude': 114.98}, {'name': '宜春', 'longitude': 114.38},
        {'name': '抚州', 'longitude': 116.34}, {'name': '上饶', 'longitude': 117.97}
    ],
    '山东省': [
        {'name': '济南', 'longitude': 117.00}, {'name': '青岛', 'longitude': 120.33}, {'name': '淄博', 'longitude': 118.05},
        {'name': '枣庄', 'longitude': 117.57}, {'name': '东营', 'longitude': 118.49}, {'name': '烟台', 'longitude': 121.39},
        {'name': '潍坊', 'longitude': 119.10}, {'name': '济宁', 'longitude': 116.59}, {'name': '泰安', 'longitude': 117.13},
        {'name': '威海', 'longitude': 122.10}, {'name': '日照', 'longitude': 119.46}, {'name': '临沂', 'longitude': 118.35},
        {'name': '德州', 'longitude': 116.39}, {'name': '聊城', 'longitude': 115.97}, {'name': '滨州', 'longitude': 118.02},
        {'name': '菏泽', 'longitude': 115.48}
    ],
    '河南省': [
        {'name': '郑州', 'longitude': 113.65}, {'name': '开封', 'longitude': 114.35}, {'name': '洛阳', 'longitude': 112.44},
        {'name': '平顶山', 'longitude': 113.29}, {'name': '安阳', 'longitude': 114.35}, {'name': '鹤壁', 'longitude': 114.17},
        {'name': '新乡', 'longitude': 113.85}, {'name': '焦作', 'longitude': 113.21}, {'name': '濮阳', 'longitude': 115.04},
        {'name': '许昌', 'longitude': 113.81}, {'name': '漯河', 'longitude': 114.02}, {'name': '三门峡', 'longitude': 111.19},
        {'name': '南阳', 'longitude': 112.53}, {'name': '商丘', 'longitude': 115.65}, {'name': '信阳', 'longitude': 114.07},
        {'name': '周口', 'longitude': 114.63}, {'name': '驻马店', 'longitude': 114.02}
    ],
    '湖北省': [
        {'name': '武汉', 'longitude': 114.31}, {'name': '黄石', 'longitude': 115.09}, {'name': '十堰', 'longitude': 110.79},
        {'name': '宜昌', 'longitude': 111.29}, {'name': '襄阳', 'longitude': 112.14}, {'name': '鄂州', 'longitude': 114.88},
        {'name': '荆门', 'longitude': 112.20}, {'name': '孝感', 'longitude': 113.91}, {'name': '荆州', 'longitude': 112.24},
        {'name': '黄冈', 'longitude': 114.87}, {'name': '咸宁', 'longitude': 114.32}, {'name': '随州', 'longitude': 113.37},
        {'name': '恩施', 'longitude': 109.48}
    ],
    '湖南省': [
        {'name': '长沙', 'longitude': 112.98}, {'name': '株洲', 'longitude': 113.15}, {'name': '湘潭', 'longitude': 112.91},
        {'name': '衡阳', 'longitude': 112.61}, {'name': '邵阳', 'longitude': 111.50}, {'name': '岳阳', 'longitude': 113.09},
        {'name': '常德', 'longitude': 111.69}, {'name': '张家界', 'longitude': 110.48}, {'name': '益阳', 'longitude': 112.36},
        {'name': '郴州', 'longitude': 113.03}, {'name': '永州', 'longitude': 111.63}, {'name': '怀化', 'longitude': 110.00},
        {'name': '娄底', 'longitude': 112.01}, {'name': '湘西', 'longitude': 109.73}
    ],
    '广东省': [
        {'name': '广州', 'longitude': 113.23}, {'name': '韶关', 'longitude': 113.60}, {'name': '深圳', 'longitude': 114.07},
        {'name': '珠海', 'longitude': 113.52}, {'name': '汕头', 'longitude': 116.70}, {'name': '佛山', 'longitude': 113.11},
        {'name': '江门', 'longitude': 113.06}, {'name': '湛江', 'longitude': 110.40}, {'name': '茂名', 'longitude': 110.88},
        {'name': '肇庆', 'longitude': 112.44}, {'name': '惠州', 'longitude': 114.41}, {'name': '梅州', 'longitude': 116.10},
        {'name': '汕尾', 'longitude': 115.36}, {'name': '河源', 'longitude': 114.68}, {'name': '阳江', 'longitude': 111.95},
        {'name': '清远', 'longitude': 113.01}, {'name': '东莞', 'longitude': 113.75}, {'name': '中山', 'longitude': 113.38},
        {'name': '潮州', 'longitude': 116.63}, {'name': '揭阳', 'longitude': 116.35}, {'name': '云浮', 'longitude': 112.02}
    ],
    '广西': [
        {'name': '南宁', 'longitude': 108.33}, {'name': '柳州', 'longitude': 109.41}, {'name': '桂林', 'longitude': 110.29},
        {'name': '梧州', 'longitude': 111.34}, {'name': '北海', 'longitude': 109.12}, {'name': '防城港', 'longitude': 108.35},
        {'name': '钦州', 'longitude': 108.62}, {'name': '贵港', 'longitude': 109.60}, {'name': '玉林', 'longitude': 110.14},
        {'name': '百色', 'longitude': 106.62}, {'name': '贺州', 'longitude': 111.55}, {'name': '河池', 'longitude': 108.06}
    ],
    '海南省': [
        {'name': '海口', 'longitude': 110.35}, {'name': '三亚', 'longitude': 109.51}, {'name': '三沙', 'longitude': 112.33},
        {'name': '儋州', 'longitude': 109.57}
    ],
    '四川省': [
        {'name': '成都', 'longitude': 104.06}, {'name': '自贡', 'longitude': 104.77}, {'name': '攀枝花', 'longitude': 101.71},
        {'name': '泸州', 'longitude': 105.39}, {'name': '德阳', 'longitude': 104.37}, {'name': '绵阳', 'longitude': 104.73},
        {'name': '广元', 'longitude': 105.82}, {'name': '遂宁', 'longitude': 105.57}, {'name': '内江', 'longitude': 105.06},
        {'name': '乐山', 'longitude': 103.77}, {'name': '南充', 'longitude': 106.08}, {'name': '眉山', 'longitude': 103.81},
        {'name': '宜宾', 'longitude': 104.56}, {'name': '广安', 'longitude': 106.63}, {'name': '达州', 'longitude': 107.50},
        {'name': '雅安', 'longitude': 103.00}, {'name': '巴中', 'longitude': 106.73}, {'name': '资阳', 'longitude': 104.64}
    ],
    '贵州省': [
        {'name': '贵阳', 'longitude': 106.71}, {'name': '六盘水', 'longitude': 104.84}, {'name': '遵义', 'longitude': 106.90},
        {'name': '安顺', 'longitude': 105.93}, {'name': '毕节', 'longitude': 105.28}, {'name': '铜仁', 'longitude': 109.19}
    ],
    '云南省': [
        {'name': '昆明', 'longitude': 102.73}, {'name': '曲靖', 'longitude': 103.79}, {'name': '玉溪', 'longitude': 102.52},
        {'name': '保山', 'longitude': 99.18}, {'name': '昭通', 'longitude': 103.70}, {'name': '丽江', 'longitude': 100.25},
        {'name': '普洱', 'longitude': 100.97}, {'name': '临沧', 'longitude': 100.08}, {'name': '大理', 'longitude': 100.23}
    ],
    '西藏': [{'name': '拉萨', 'longitude': 91.11}, {'name': '日喀则', 'longitude': 88.88}, {'name': '林芝', 'longitude': 94.36}],
    '陕西省': [
        {'name': '西安', 'longitude': 108.95}, {'name': '铜川', 'longitude': 109.11}, {'name': '宝鸡', 'longitude': 107.15},
        {'name': '咸阳', 'longitude': 108.70}, {'name': '渭南', 'longitude': 109.50}, {'name': '延安', 'longitude': 109.47},
        {'name': '汉中', 'longitude': 107.03}, {'name': '榆林', 'longitude': 109.74}, {'name': '安康', 'longitude': 109.02},
        {'name': '商洛', 'longitude': 109.93}
    ],
    '甘肃省': [
        {'name': '兰州', 'longitude': 103.82}, {'name': '嘉峪关', 'longitude': 98.28}, {'name': '金昌', 'longitude': 102.18},
        {'name': '白银', 'longitude': 104.17}, {'name': '天水', 'longitude': 105.73}, {'name': '武威', 'longitude': 102.63},
        {'name': '张掖', 'longitude': 100.45}, {'name': '酒泉', 'longitude': 98.51}, {'name': '庆阳', 'longitude': 107.63}
    ],
    '青海省': [{'name': '西宁', 'longitude': 101.74}, {'name': '海东', 'longitude': 102.08}],
    '宁夏': [{'name': '银川', 'longitude': 106.27}, {'name': '石嘴山', 'longitude': 106.39}, {'name': '吴忠', 'longitude': 106.21}],
    '新疆': [
        {'name': '乌鲁木齐', 'longitude': 87.68}, {'name': '克拉玛依', 'longitude': 84.87}, {'name': '吐鲁番', 'longitude': 89.19},
        {'name': '哈密', 'longitude': 93.51}, {'name': '昌吉', 'longitude': 87.30}, {'name': '博乐', 'longitude': 82.07},
        {'name': '库尔勒', 'longitude': 86.15}, {'name': '阿克苏', 'longitude': 80.26}, {'name': '喀什', 'longitude': 75.94},
        {'name': '和田', 'longitude': 79.94}, {'name': '伊宁', 'longitude': 81.33}
    ],
    '港澳台': [
        {'name': '香港', 'longitude': 114.17}, {'name': '澳门', 'longitude': 113.54},
        {'name': '台北', 'longitude': 121.50}, {'name': '高雄', 'longitude': 120.30}, {'name': '台中', 'longitude': 120.65}
    ]
}
