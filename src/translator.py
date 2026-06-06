"""
翻译模块 - 增强离线词典版
完全离线的本地词典翻译器，无需网络连接
"""

import time
import re
from typing import Optional, Dict, List


class LocalTranslator:
    """本地词典翻译器 - 完全离线"""

    def __init__(self, source_lang: str = 'en', target_lang: str = 'zh'):
        """
        初始化翻译器

        Args:
            source_lang: 源语言代码 (en, ja, zh 等)
            target_lang: 目标语言代码 (zh, en, ja 等)
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.cache = {}  # 翻译缓存
        self.history = []  # 历史记录
        self.dictionary = self._load_dictionary()
        print(f"✅ 使用本地词典翻译器 (源语言: {source_lang}, 目标语言: {target_lang})")
        print(f"📚 词典包含 {len(self.dictionary)} 个词汇")

    def _load_dictionary(self) -> Dict[str, str]:
        """加载本地词典"""
        # 常用英语-中文词典
        en_zh_dict = {
            # 基础词汇
            "hello": "你好", "hi": "嗨", "hey": "嘿", "goodbye": "再见", "bye": "拜拜",
            "thank": "谢谢", "thanks": "谢谢", "please": "请", "sorry": "对不起", "excuse": "打扰",
            "yes": "是", "no": "不", "ok": "好的", "okay": "好的", "alright": "好的", "sure": "当然",
            "maybe": "也许", "perhaps": "也许", "probably": "可能", "possibly": "可能",
            "certainly": "当然", "definitely": "肯定", "absolutely": "绝对", "really": "真的",
            "truly": "真正", "actually": "实际上", "obviously": "明显", "clearly": "清楚地",
            
            # 代词
            "i": "我", "you": "你", "he": "他", "she": "她", "it": "它", "we": "我们", "they": "他们",
            "this": "这个", "that": "那个", "these": "这些", "those": "那些",
            "my": "我的", "your": "你的", "his": "他的", "her": "她的", "its": "它的",
            "our": "我们的", "their": "他们的", "mine": "我的", "yours": "你的",
            "ours": "我们的", "theirs": "他们的", "myself": "我自己", "yourself": "你自己",
            "himself": "他自己", "herself": "她自己", "itself": "它自己", "ourselves": "我们自己",
            "themselves": "他们自己", "someone": "某人", "something": "某事", "anyone": "任何人",
            "anything": "任何事", "everyone": "每个人", "everything": "一切", "nobody": "没有人",
            "nothing": "没有什么", "who": "谁", "what": "什么", "where": "哪里", "when": "什么时候",
            "why": "为什么", "how": "如何", "which": "哪个", "whose": "谁的",
            
            # 动词
            "is": "是", "are": "是", "am": "是", "was": "是", "were": "是", "be": "是",
            "been": "是", "being": "是", "have": "有", "has": "有", "had": "有",
            "do": "做", "does": "做", "did": "做", "done": "完成", "will": "将", "would": "会",
            "can": "能", "could": "能", "should": "应该", "must": "必须", "may": "可能", "might": "可能",
            "go": "去", "goes": "去", "went": "去了", "gone": "去了", "going": "去",
            "come": "来", "comes": "来", "came": "来了", "coming": "来",
            "say": "说", "says": "说", "said": "说了", "saying": "说",
            "speak": "说", "speaks": "说", "spoke": "说了", "spoken": "说了", "speaking": "说",
            "tell": "告诉", "tells": "告诉", "told": "告诉了", "telling": "告诉",
            "ask": "问", "asks": "问", "asked": "问了", "asking": "问",
            "answer": "回答", "answers": "回答", "answered": "回答了", "answering": "回答",
            "think": "想", "thinks": "想", "thought": "想了", "thinking": "想",
            "know": "知道", "knows": "知道", "knew": "知道了", "known": "知道", "knowing": "知道",
            "understand": "理解", "understands": "理解", "understood": "理解了", "understanding": "理解",
            "see": "看", "sees": "看", "saw": "看了", "seen": "看过", "seeing": "看",
            "look": "看", "looks": "看", "looked": "看了", "looking": "看",
            "watch": "看", "watches": "看", "watched": "看了", "watching": "看",
            "listen": "听", "listens": "听", "listened": "听了", "listening": "听",
            "hear": "听", "hears": "听", "heard": "听到了", "hearing": "听",
            "read": "读", "reads": "读", "reading": "读",
            "write": "写", "writes": "写", "wrote": "写了", "written": "写了", "writing": "写",
            "eat": "吃", "eats": "吃", "ate": "吃了", "eating": "吃",
            "drink": "喝", "drinks": "喝", "drank": "喝了", "drunk": "喝了", "drinking": "喝",
            "sleep": "睡觉", "sleeps": "睡觉", "slept": "睡了", "sleeping": "睡觉",
            "work": "工作", "works": "工作", "worked": "工作了", "working": "工作",
            "study": "学习", "studies": "学习", "studied": "学习了", "studying": "学习",
            "learn": "学习", "learns": "学习", "learned": "学习了", "learning": "学习",
            "teach": "教", "teaches": "教", "taught": "教了", "teaching": "教",
            "play": "玩", "plays": "玩", "played": "玩了", "playing": "玩",
            "love": "爱", "loves": "爱", "loved": "爱过", "loving": "爱",
            "like": "喜欢", "likes": "喜欢", "liked": "喜欢过", "liking": "喜欢",
            "want": "想要", "wants": "想要", "wanted": "想要过", "wanting": "想要",
            "need": "需要", "needs": "需要", "needed": "需要过", "needing": "需要",
            "make": "制作", "makes": "制作", "made": "制作了", "making": "制作",
            "get": "得到", "gets": "得到", "got": "得到了", "gotten": "得到", "getting": "得到",
            "give": "给", "gives": "给", "gave": "给了", "given": "给了", "giving": "给",
            "take": "拿", "takes": "拿", "took": "拿了", "taken": "拿走", "taking": "拿",
            "find": "找到", "finds": "找到", "found": "找到了", "finding": "找到",
            "use": "使用", "uses": "使用", "used": "使用过", "using": "使用",
            "help": "帮助", "helps": "帮助", "helped": "帮助过", "helping": "帮助",
            "call": "打电话", "calls": "打电话", "called": "打了电话", "calling": "打电话",
            "start": "开始", "starts": "开始", "started": "开始了", "starting": "开始",
            "stop": "停止", "stops": "停止", "stopped": "停止了", "stopping": "停止",
            "open": "打开", "opens": "打开", "opened": "打开了", "opening": "打开",
            "close": "关闭", "closes": "关闭", "closed": "关闭了", "closing": "关闭",
            "show": "显示", "shows": "显示", "showed": "显示了", "shown": "显示", "showing": "显示",
            "keep": "保持", "keeps": "保持", "kept": "保持了", "keeping": "保持",
            "let": "让", "lets": "让", "letting": "让",
            "put": "放", "puts": "放", "putting": "放",
            "bring": "带来", "brings": "带来", "brought": "带来了", "bringing": "带来",
            "buy": "买", "buys": "买", "bought": "买了", "buying": "买",
            "sell": "卖", "sells": "卖", "sold": "卖了", "selling": "卖",
            "pay": "付", "pays": "付", "paid": "付了", "paying": "付",
            "cost": "花费", "costs": "花费", "costing": "花费",
            "try": "尝试", "tries": "尝试", "tried": "尝试过", "trying": "尝试",
            "change": "改变", "changes": "改变", "changed": "改变了", "changing": "改变",
            "move": "移动", "moves": "移动", "moved": "移动了", "moving": "移动",
            "live": "生活", "lives": "生活", "lived": "生活过", "living": "生活",
            "die": "死", "dies": "死", "died": "死了", "dying": "死",
            "grow": "生长", "grows": "生长", "grew": "生长了", "grown": "生长", "growing": "生长",
            "build": "建造", "builds": "建造", "built": "建造了", "building": "建造",
            "create": "创建", "creates": "创建", "created": "创建了", "creating": "创建",
            "destroy": "破坏", "destroys": "破坏", "destroyed": "破坏了", "destroying": "破坏",
            "break": "打破", "breaks": "打破", "broke": "打破了", "broken": "打破", "breaking": "打破",
            "fix": "修理", "fixes": "修理", "fixed": "修理了", "fixing": "修理",
            "solve": "解决", "solves": "解决", "solved": "解决了", "solving": "解决",
            "meet": "见面", "meets": "见面", "met": "见面了", "meeting": "见面",
            "join": "加入", "joins": "加入", "joined": "加入了", "joining": "加入",
            "leave": "离开", "leaves": "离开", "left": "离开了", "leaving": "离开",
            "stay": "停留", "stays": "停留", "stayed": "停留过", "staying": "停留",
            "wait": "等待", "waits": "等待", "waited": "等待了", "waiting": "等待",
            "hope": "希望", "hopes": "希望", "hoped": "希望过", "hoping": "希望",
            "wish": "希望", "wishes": "希望", "wished": "希望过", "wishing": "希望",
            "dream": "梦想", "dreams": "梦想", "dreamed": "梦想过", "dreaming": "梦想",
            "believe": "相信", "believes": "相信", "believed": "相信过", "believing": "相信",
            "trust": "信任", "trusts": "信任", "trusted": "信任过", "trusting": "信任",
            "remember": "记得", "remembers": "记得", "remembered": "记得", "remembering": "记得",
            "forget": "忘记", "forgets": "忘记", "forgot": "忘记了", "forgotten": "忘记", "forgetting": "忘记",
            "feel": "感觉", "feels": "感觉", "felt": "感觉过", "feeling": "感觉",
            "smell": "闻", "smells": "闻", "smelled": "闻过", "smelling": "闻",
            "taste": "尝", "tastes": "尝", "tasted": "尝过", "tasting": "尝",
            "touch": "触摸", "touches": "触摸", "touched": "触摸过", "touching": "触摸",
            "enjoy": "享受", "enjoys": "享受", "enjoyed": "享受过", "enjoying": "享受",
            "prefer": "更喜欢", "prefers": "更喜欢", "preferred": "更喜欢过", "preferring": "更喜欢",
            "choose": "选择", "chooses": "选择", "chose": "选择了", "chosen": "选择", "choosing": "选择",
            "decide": "决定", "decides": "决定", "decided": "决定了", "deciding": "决定",
            "plan": "计划", "plans": "计划", "planned": "计划了", "planning": "计划",
            "expect": "期待", "expects": "期待", "expected": "期待过", "expecting": "期待",
            "promise": "承诺", "promises": "承诺", "promised": "承诺过", "promising": "承诺",
            "agree": "同意", "agrees": "同意", "agreed": "同意了", "agreeing": "同意",
            "disagree": "不同意", "disagrees": "不同意", "disagreed": "不同意了", "disagreeing": "不同意",
            "accept": "接受", "accepts": "接受", "accepted": "接受了", "accepting": "接受",
            "reject": "拒绝", "rejects": "拒绝", "rejected": "拒绝了", "rejecting": "拒绝",
            "support": "支持", "supports": "支持", "supported": "支持过", "supporting": "支持",
            "oppose": "反对", "opposes": "反对", "opposed": "反对过", "opposing": "反对",
            "suggest": "建议", "suggests": "建议", "suggested": "建议过", "suggesting": "建议",
            "recommend": "推荐", "recommends": "推荐", "recommended": "推荐过", "recommending": "推荐",
            "advise": "建议", "advises": "建议", "advised": "建议过", "advising": "建议",
            "warn": "警告", "warns": "警告", "warned": "警告过", "warning": "警告",
            "threaten": "威胁", "threatens": "威胁", "threatened": "威胁过", "threatening": "威胁",
            "protect": "保护", "protects": "保护", "protected": "保护过", "protecting": "保护",
            "attack": "攻击", "attacks": "攻击", "attacked": "攻击过", "attacking": "攻击",
            "defend": "防御", "defends": "防御", "defended": "防御过", "defending": "防御",
            "fight": "战斗", "fights": "战斗", "fought": "战斗过", "fighting": "战斗",
            "win": "赢", "wins": "赢", "won": "赢了", "winning": "赢",
            "lose": "输", "loses": "输", "lost": "输了", "losing": "输",
            "fail": "失败", "fails": "失败", "failed": "失败过", "failing": "失败",
            "succeed": "成功", "succeeds": "成功", "succeeded": "成功过", "succeeding": "成功",
            "attempt": "尝试", "attempts": "尝试", "attempted": "尝试过", "attempting": "尝试",
            "manage": "管理", "manages": "管理", "managed": "管理过", "managing": "管理",
            "control": "控制", "controls": "控制", "controlled": "控制过", "controlling": "控制",
            "lead": "领导", "leads": "领导", "led": "领导过", "leading": "领导",
            "follow": "跟随", "follows": "跟随", "followed": "跟随过", "following": "跟随",
            "organize": "组织", "organizes": "组织", "organized": "组织过", "organizing": "组织",
            "arrange": "安排", "arranges": "安排", "arranged": "安排过", "arranging": "安排",
            "prepare": "准备", "prepares": "准备", "prepared": "准备过", "preparing": "准备",
            "complete": "完成", "completes": "完成", "completed": "完成了", "completing": "完成",
            "finish": "完成", "finishes": "完成", "finished": "完成了", "finishing": "完成",
            "begin": "开始", "begins": "开始", "began": "开始了", "begun": "开始", "beginning": "开始",
            "continue": "继续", "continues": "继续", "continued": "继续过", "continuing": "继续",
            "end": "结束", "ends": "结束", "ended": "结束了", "ending": "结束",
            
            # 名词
            "time": "时间", "day": "天", "week": "周", "month": "月", "year": "年",
            "today": "今天", "tomorrow": "明天", "yesterday": "昨天",
            "morning": "早上", "afternoon": "下午", "evening": "晚上", "night": "晚上",
            "hour": "小时", "minute": "分钟", "second": "秒",
            "people": "人们", "person": "人", "man": "男人", "men": "男人们",
            "woman": "女人", "women": "女人们", "child": "孩子", "children": "孩子们",
            "family": "家庭", "friend": "朋友", "friends": "朋友们", "teacher": "老师",
            "student": "学生", "doctor": "医生", "nurse": "护士", "worker": "工人",
            "employee": "员工", "boss": "老板", "manager": "经理", "leader": "领导者",
            "member": "成员", "team": "团队", "group": "组", "company": "公司",
            "business": "生意", "organization": "组织", "government": "政府",
            "country": "国家", "nation": "国家", "city": "城市", "town": "城镇",
            "village": "村庄", "street": "街道", "road": "道路", "house": "房子",
            "home": "家", "building": "建筑", "room": "房间", "school": "学校",
            "university": "大学", "college": "学院", "class": "班级", "lesson": "课程",
            "subject": "科目", "language": "语言", "word": "词", "sentence": "句子",
            "paragraph": "段落", "story": "故事", "book": "书", "novel": "小说",
            "poem": "诗", "article": "文章", "news": "新闻", "newspaper": "报纸",
            "magazine": "杂志", "television": "电视", "radio": "收音机", "music": "音乐",
            "song": "歌曲", "movie": "电影", "film": "电影", "video": "视频",
            "picture": "图片", "photo": "照片", "photograph": "照片", "camera": "相机",
            "phone": "手机", "telephone": "电话", "computer": "电脑", "laptop": "笔记本电脑",
            "tablet": "平板", "keyboard": "键盘", "mouse": "鼠标", "screen": "屏幕",
            "monitor": "显示器", "internet": "互联网", "website": "网站", "webpage": "网页",
            "email": "电子邮件", "message": "消息", "letter": "信", "paper": "纸",
            "pen": "笔", "pencil": "铅笔", "eraser": "橡皮", "ruler": "尺子",
            "scissors": "剪刀", "glue": "胶水", "money": "钱", "cash": "现金",
            "coin": "硬币", "bill": "钞票", "card": "卡", "bank": "银行",
            "account": "账户", "price": "价格", "cost": "成本", "value": "价值",
            "quality": "质量", "quantity": "数量", "number": "数字", "amount": "数量",
            "total": "总计", "sum": "总和", "average": "平均", "percentage": "百分比",
            "fraction": "分数", "decimal": "小数", "math": "数学", "science": "科学",
            "physics": "物理", "chemistry": "化学", "biology": "生物", "history": "历史",
            "geography": "地理", "art": "艺术", "sport": "运动", "sports": "运动",
            "game": "游戏", "games": "游戏", "match": "比赛", "competition": "竞赛",
            "prize": "奖品", "award": "奖项", "trophy": "奖杯", "medal": "奖章",
            "food": "食物", "drink": "饮料", "water": "水", "milk": "牛奶",
            "juice": "果汁", "coffee": "咖啡", "tea": "茶", "bread": "面包",
            "rice": "米饭", "noodle": "面条", "meat": "肉", "fish": "鱼",
            "chicken": "鸡肉", "beef": "牛肉", "pork": "猪肉", "vegetable": "蔬菜",
            "fruit": "水果", "apple": "苹果", "banana": "香蕉", "orange": "橙子",
            "grape": "葡萄", "strawberry": "草莓", "cake": "蛋糕", "cookie": "饼干",
            "chocolate": "巧克力", "ice cream": "冰淇淋", "candy": "糖果", "sugar": "糖",
            "salt": "盐", "pepper": "胡椒", "oil": "油", "butter": "黄油",
            "cheese": "奶酪", "egg": "鸡蛋", "breakfast": "早餐", "lunch": "午餐",
            "dinner": "晚餐", "supper": "晚餐", "snack": "零食", "meal": "餐",
            "restaurant": "餐厅", "cafe": "咖啡馆", "bar": "酒吧", "shop": "商店",
            "store": "商店", "market": "市场", "supermarket": "超市", "mall": "商场",
            "center": "中心", "office": "办公室", "factory": "工厂", "hospital": "医院",
            "clinic": "诊所", "pharmacy": "药店", "police": "警察", "police station": "警察局",
            "fire station": "消防站", "post office": "邮局", "hotel": "酒店", "airport": "机场",
            "train station": "火车站", "bus station": "公交站", "subway": "地铁", "bus": "公交车",
            "car": "汽车", "truck": "卡车", "taxi": "出租车", "bicycle": "自行车",
            "bike": "自行车", "motorcycle": "摩托车", "boat": "船", "ship": "船",
            "plane": "飞机", "airplane": "飞机", "train": "火车", "ticket": "票",
            "passport": "护照", "visa": "签证", "luggage": "行李", "bag": "包",
            "suitcase": "手提箱", "backpack": "背包", "purse": "钱包", "wallet": "钱包",
            "clothes": "衣服", "clothing": "服装", "shirt": "衬衫", "t-shirt": "T恤",
            "pants": "裤子", "jeans": "牛仔裤", "dress": "连衣裙", "skirt": "裙子",
            "coat": "外套", "jacket": "夹克", "sweater": "毛衣", "hat": "帽子",
            "cap": "帽子", "shoes": "鞋子", "socks": "袜子", "gloves": "手套",
            "scarf": "围巾", "belt": "腰带", "watch": "手表", "glasses": "眼镜",
            "sunglasses": "太阳镜", "jewelry": "珠宝", "ring": "戒指", "necklace": "项链",
            "earring": "耳环", "bracelet": "手镯", "makeup": "化妆品", "perfume": "香水",
            "soap": "肥皂", "shampoo": "洗发水", "toothbrush": "牙刷", "toothpaste": "牙膏",
            "towel": "毛巾", "blanket": "毯子", "pillow": "枕头", "bed": "床",
            "chair": "椅子", "table": "桌子", "desk": "书桌", "sofa": "沙发",
            "couch": "沙发", "lamp": "灯", "light": "灯", "bulb": "灯泡",
            "switch": "开关", "socket": "插座", "plug": "插头", "wire": "电线",
            "cable": "电缆", "battery": "电池", "charger": "充电器", "remote": "遥控器",
            "key": "钥匙", "lock": "锁", "door": "门", "window": "窗户",
            "wall": "墙", "floor": "地板", "ceiling": "天花板", "roof": "屋顶",
            "garden": "花园", "yard": "院子", "park": "公园", "tree": "树",
            "flower": "花", "grass": "草", "plant": "植物", "animal": "动物",
            "pet": "宠物", "dog": "狗", "cat": "猫", "bird": "鸟",
            "fish": "鱼", "insect": "昆虫", "nature": "自然", "environment": "环境",
            "weather": "天气", "climate": "气候", "sun": "太阳", "moon": "月亮",
            "star": "星星", "sky": "天空", "cloud": "云", "rain": "雨",
            "snow": "雪", "wind": "风", "storm": "暴风雨", "thunder": "雷",
            "lightning": "闪电", "rainbow": "彩虹", "earth": "地球", "world": "世界",
            "universe": "宇宙", "space": "太空", "planet": "行星", "galaxy": "星系",
            
            # 形容词
            "good": "好的", "bad": "坏的", "big": "大的", "small": "小的",
            "large": "大的", "little": "小的", "long": "长的", "short": "短的",
            "high": "高的", "low": "低的", "tall": "高的", "fast": "快的",
            "slow": "慢的", "hot": "热的", "cold": "冷的", "warm": "温暖的",
            "cool": "凉爽的", "new": "新的", "old": "旧的", "young": "年轻的",
            "easy": "容易的", "hard": "困难的", "difficult": "困难的", "simple": "简单的",
            "complex": "复杂的", "important": "重要的", "different": "不同的", "same": "相同的",
            "similar": "相似的", "real": "真实的", "true": "真实的", "false": "假的",
            "right": "对的", "wrong": "错的", "correct": "正确的", "incorrect": "不正确的",
            "happy": "快乐的", "sad": "悲伤的", "angry": "生气的", "excited": "兴奋的",
            "bored": "无聊的", "tired": "累的", "hungry": "饿的", "thirsty": "渴的",
            "sick": "生病的", "healthy": "健康的", "beautiful": "美丽的", "ugly": "丑陋的",
            "clean": "干净的", "dirty": "脏的", "rich": "富有的", "poor": "贫穷的",
            "strong": "强壮的", "weak": "弱的", "busy": "忙碌的", "free": "空闲的",
            "full": "满的", "empty": "空的", "heavy": "重的", "light": "轻的",
            "dark": "暗的", "bright": "明亮的", "loud": "大声的", "quiet": "安静的",
            "soft": "软的", "hard": "硬的", "smooth": "光滑的", "rough": "粗糙的",
            "wet": "湿的", "dry": "干的", "sweet": "甜的", "sour": "酸的",
            "bitter": "苦的", "salty": "咸的", "spicy": "辣的", "delicious": "美味的",
            "tasty": "好吃的", "fresh": "新鲜的", "expensive": "昂贵的", "cheap": "便宜的",
            "valuable": "有价值的", "useful": "有用的", "useless": "无用的", "dangerous": "危险的",
            "safe": "安全的", "careful": "小心的", "careless": "粗心的", "lucky": "幸运的",
            "unlucky": "不幸的", "successful": "成功的", "unsuccessful": "不成功的", "famous": "著名的",
            "unknown": "未知的", "popular": "流行的", "common": "常见的", "rare": "罕见的",
            "strange": "奇怪的", "normal": "正常的", "special": "特别的", "ordinary": "普通的",
            "excellent": "优秀的", "terrible": "糟糕的", "wonderful": "精彩的", "amazing": "惊人的",
            "fantastic": "极好的", "great": "伟大的", "perfect": "完美的", "awful": "糟糕的",
            "horrible": "可怕的", "possible": "可能的", "impossible": "不可能的", "likely": "可能的",
            "unlikely": "不太可能的", "certain": "确定的", "uncertain": "不确定的", "sure": "确定的",
            "unsure": "不确定的", "ready": "准备好的", "unready": "未准备的", "available": "可用的",
            "unavailable": "不可用的", "open": "开放的", "closed": "关闭的", "public": "公开的",
            "private": "私人的", "local": "本地的", "international": "国际的", "national": "国家的",
            "regional": "地区的", "global": "全球的", "digital": "数字的", "electronic": "电子的",
            "mechanical": "机械的", "automatic": "自动的", "manual": "手动的", "physical": "物理的",
            "mental": "精神的", "emotional": "情感的", "social": "社会的", "cultural": "文化的",
            "political": "政治的", "economic": "经济的", "financial": "金融的", "commercial": "商业的",
            "industrial": "工业的", "agricultural": "农业的", "medical": "医疗的", "legal": "法律的",
            "educational": "教育的", "professional": "专业的", "personal": "个人的", "official": "官方的",
            "formal": "正式的", "informal": "非正式的", "traditional": "传统的", "modern": "现代的",
            "ancient": "古代的", "recent": "最近的", "current": "当前的", "future": "未来的",
            "past": "过去的", "present": "现在的", "daily": "每天的", "weekly": "每周的",
            "monthly": "每月的", "yearly": "每年的", "annual": "每年的", "permanent": "永久的",
            "temporary": "临时的", "final": "最后的", "initial": "最初的", "basic": "基本的",
            "advanced": "高级的", "simple": "简单的", "complicated": "复杂的", "confusing": "令人困惑的",
            "clear": "清楚的", "obvious": "明显的", "hidden": "隐藏的", "secret": "秘密的",
            "visible": "可见的", "invisible": "不可见的", "audible": "可听的", "silent": "沉默的",
            "loud": "大声的", "quiet": "安静的", "peaceful": "和平的", "violent": "暴力的",
            "gentle": "温柔的", "rough": "粗暴的", "polite": "礼貌的", "rude": "粗鲁的",
            "kind": "善良的", "cruel": "残忍的", "generous": "慷慨的", "selfish": "自私的",
            "honest": "诚实的", "dishonest": "不诚实的", "brave": "勇敢的", "cowardly": "懦弱的",
            "wise": "明智的", "foolish": "愚蠢的", "smart": "聪明的", "stupid": "愚蠢的",
            "intelligent": "聪明的", "creative": "有创造力的", "practical": "实用的", "theoretical": "理论的",
            "scientific": "科学的", "technical": "技术的", "artistic": "艺术的", "musical": "音乐的",
            "literary": "文学的", "historical": "历史的", "geographical": "地理的", "mathematical": "数学的",
            
            # 副词
            "very": "非常", "too": "太", "quite": "相当", "rather": "相当",
            "almost": "几乎", "nearly": "几乎", "hardly": "几乎不", "barely": "几乎不",
            "completely": "完全", "totally": "完全", "entirely": "完全", "fully": "完全",
            "partly": "部分", "partially": "部分", "really": "真的", "truly": "真正",
            "actually": "实际上", "certainly": "当然", "definitely": "肯定", "absolutely": "绝对",
            "probably": "可能", "possibly": "可能", "maybe": "也许", "perhaps": "也许",
            "surely": "肯定", "clearly": "清楚地", "obviously": "明显", "simply": "简单地",
            "easily": "容易地", "quickly": "快速地", "slowly": "缓慢地", "carefully": "小心地",
            "carelessly": "粗心地", "happily": "快乐地", "sadly": "悲伤地", "angrily": "生气地",
            "quietly": "安静地", "loudly": "大声地", "softly": "轻柔地", "just": "刚刚",
            "already": "已经", "still": "仍然", "yet": "还", "now": "现在",
            "then": "那时", "later": "后来", "soon": "很快", "early": "早",
            "late": "晚", "before": "之前", "after": "之后", "during": "期间",
            "while": "当...时", "until": "直到", "since": "自从", "always": "总是",
            "never": "从不", "sometimes": "有时", "often": "经常", "usually": "通常",
            "frequently": "频繁", "rarely": "很少", "seldom": "很少", "every": "每个",
            "each": "每个", "all": "所有", "some": "一些", "any": "任何",
            "many": "许多", "much": "很多", "few": "很少", "little": "一点",
            "more": "更多", "most": "最多", "less": "更少", "least": "最少",
            "better": "更好", "best": "最好", "worse": "更差", "worst": "最差",
            "further": "更远", "farthest": "最远", "closer": "更近", "closest": "最近",
            "again": "再次", "once": "一次", "twice": "两次", "first": "首先",
            "second": "第二", "third": "第三", "last": "最后", "next": "下一个",
            "previous": "之前的", "following": "以下的", "inside": "在里面", "outside": "在外面",
            "above": "在上面", "below": "在下面", "around": "周围", "between": "之间",
            "among": "之中", "through": "通过", "across": "穿过", "along": "沿着",
            "behind": "后面", "beside": "旁边", "near": "附近", "far": "远",
            
            # 介词
            "in": "在...里", "on": "在...上", "at": "在", "to": "到", "from": "从",
            "with": "和", "without": "没有", "by": "通过", "for": "为了", "of": "的",
            "about": "关于", "between": "在...之间", "among": "在...之中", "through": "通过",
            "during": "在...期间", "since": "自从", "until": "直到", "before": "在...之前",
            "after": "在...之后", "above": "在...上面", "below": "在...下面", "over": "在...上方",
            "under": "在...下方", "around": "围绕", "behind": "在...后面", "in front of": "在...前面",
            "next to": "在...旁边", "near": "靠近", "far from": "远离", "inside": "在...里面",
            "outside": "在...外面", "up": "向上", "down": "向下", "into": "进入",
            "out of": "从...出来", "onto": "到...上", "off": "离开", "toward": "朝向",
            "away from": "远离", "along": "沿着", "across": "穿过", "past": "经过",
            "beyond": "超出", "against": "反对", "for": "为了", "with": "和",
            
            # 连词
            "and": "和", "but": "但是", "or": "或者", "so": "所以",
            "because": "因为", "since": "因为", "as": "因为", "although": "虽然",
            "though": "虽然", "even though": "即使", "while": "当...时", "when": "当...时",
            "if": "如果", "unless": "除非", "until": "直到", "before": "在...之前",
            "after": "在...之后", "both": "两者都", "either": "两者之一", "neither": "两者都不",
            "not only": "不仅", "also": "也", "whether": "是否", "that": "那个",
            "which": "哪个", "who": "谁", "whom": "谁", "whose": "谁的",
            "what": "什么", "when": "什么时候", "where": "哪里", "why": "为什么",
            "how": "如何",
            
            # 常用短语
            "how are you": "你好吗", "how do you do": "你好", "nice to meet you": "很高兴见到你",
            "thank you": "谢谢你", "you're welcome": "不客气", "excuse me": "打扰一下",
            "i'm sorry": "对不起", "no problem": "没问题", "of course": "当然",
            "good morning": "早上好", "good afternoon": "下午好", "good evening": "晚上好",
            "good night": "晚安", "see you": "再见", "see you later": "回头见",
            "have a nice day": "祝你今天愉快", "take care": "保重", "good luck": "祝你好运",
            "congratulations": "恭喜", "i love you": "我爱你", "i don't know": "我不知道",
            "i think so": "我也这么认为", "i agree": "我同意", "i disagree": "我不同意",
            
            # 技术词汇
            "technology": "技术", "computer": "电脑", "software": "软件", "hardware": "硬件",
            "program": "程序", "code": "代码", "data": "数据", "database": "数据库",
            "network": "网络", "internet": "互联网", "website": "网站", "application": "应用程序",
            "app": "应用程序", "system": "系统", "interface": "接口", "function": "函数",
            "variable": "变量", "constant": "常量", "array": "数组", "list": "列表",
            "dictionary": "字典", "string": "字符串", "number": "数字", "boolean": "布尔值",
            "object": "对象", "class": "类", "method": "方法", "parameter": "参数",
            "argument": "参数", "return": "返回", "import": "导入", "export": "导出",
            "module": "模块", "package": "包", "library": "库", "framework": "框架",
            "platform": "平台", "environment": "环境", "configuration": "配置", "deployment": "部署",
            "testing": "测试", "debugging": "调试", "optimization": "优化", "performance": "性能",
            "security": "安全", "authentication": "认证", "authorization": "授权", "encryption": "加密",
            "decryption": "解密", "compression": "压缩", "decompression": "解压", "backup": "备份",
            "restore": "恢复", "migration": "迁移", "integration": "集成", "api": "接口",
            "json": "JSON", "xml": "XML", "html": "HTML", "css": "CSS",
            "javascript": "JavaScript", "python": "Python", "java": "Java", "c": "C语言",
            "cpp": "C++", "ruby": "Ruby", "php": "PHP", "sql": "SQL",
            "git": "Git", "github": "GitHub", "docker": "Docker", "kubernetes": "Kubernetes",
            "cloud": "云", "server": "服务器", "client": "客户端", "frontend": "前端",
            "backend": "后端", "fullstack": "全栈", "mobile": "移动", "desktop": "桌面",
            "web": "网页", "browser": "浏览器", "search": "搜索", "engine": "引擎",
            "social": "社交", "media": "媒体", "streaming": "流媒体", "video": "视频",
            "audio": "音频", "image": "图像", "text": "文本", "file": "文件",
            "folder": "文件夹", "directory": "目录", "path": "路径", "url": "网址",
            "link": "链接", "button": "按钮", "menu": "菜单", "toolbar": "工具栏",
            "statusbar": "状态栏", "scrollbar": "滚动条", "window": "窗口", "dialog": "对话框",
            "message": "消息", "notification": "通知", "alert": "警告", "error": "错误",
            "warning": "警告", "info": "信息", "success": "成功", "failure": "失败",
            "loading": "加载中", "processing": "处理中", "completed": "已完成", "pending": "待处理",
            "cancelled": "已取消", "deleted": "已删除", "updated": "已更新", "created": "已创建",
            "saved": "已保存", "downloaded": "已下载", "uploaded": "已上传", "sent": "已发送",
            "received": "已接收", "read": "已读", "unread": "未读", "online": "在线",
            "offline": "离线", "connected": "已连接", "disconnected": "已断开", "available": "可用",
            "unavailable": "不可用", "enabled": "已启用", "disabled": "已禁用", "active": "活跃",
            "inactive": "不活跃", "visible": "可见", "invisible": "不可见", "public": "公开",
            "private": "私有", "shared": "共享", "locked": "已锁定", "unlocked": "已解锁",
            "encrypted": "已加密", "decrypted": "已解密", "compressed": "已压缩", "decompressed": "已解压",
            "backed up": "已备份", "restored": "已恢复", "migrated": "已迁移", "integrated": "已集成",
            "artificial intelligence": "人工智能", "machine learning": "机器学习", "deep learning": "深度学习",
            "neural network": "神经网络", "algorithm": "算法", "programming": "编程",
            
            # 冠词和量词
            "a": "一个", "an": "一个", "the": "这个",
            "one": "一", "two": "二", "three": "三", "four": "四", "five": "五",
            "six": "六", "seven": "七", "eight": "八", "nine": "九", "ten": "十",
            "hundred": "百", "thousand": "千", "million": "百万", "billion": "十亿",
            
            # 常见疑问词和回答
            "what's": "什么是", "where's": "哪里是", "who's": "谁是", "how's": "怎么样",
            "why's": "为什么是", "when's": "什么时候是", "can't": "不能", "won't": "不会",
            "don't": "不", "doesn't": "不", "didn't": "不", "isn't": "不是",
            "aren't": "不是", "wasn't": "不是", "weren't": "不是", "haven't": "没有",
            "hasn't": "没有", "hadn't": "没有", "couldn't": "不能", "wouldn't": "不会",
            "shouldn't": "不应该", "mustn't": "不许", "mightn't": "可能不",
            
            # 更多常用短语
            "good luck": "祝好运", "best wishes": "最美好的祝愿", "no worries": "不用担心",
            "take it easy": "放轻松", "hang in there": "坚持住", "keep it up": "继续保持",
            "well done": "做得好", "job well done": "工作做得好", "nice work": "做得好",
            "great job": "做得很好", "excellent work": "出色的工作", "good job": "做得好",
            "keep going": "继续前进", "don't give up": "不要放弃", "you can do it": "你能行的",
            "believe in yourself": "相信自己", "stay positive": "保持积极", "think positive": "积极思考",
            "be happy": "要快乐", "be safe": "注意安全", "take care": "保重",
            "see you soon": "很快见", "talk to you later": "回头聊", "have fun": "玩得开心",
            "enjoy yourself": "享受自己", "have a good time": "玩得愉快", "make the most of it": "充分利用",
            "live life to the fullest": "充分享受生活", "follow your dreams": "追随梦想",
            "never give up": "永不放弃", "stay strong": "保持坚强", "be brave": "要勇敢",
            "be kind": "要善良", "be honest": "要诚实", "be true to yourself": "忠于自己",
            "love yourself": "爱自己", "respect others": "尊重他人", "help others": "帮助他人",
            "make a difference": "产生影响", "change the world": "改变世界", "be the change": "成为改变",
            "think big": "想得大一点", "dream big": "梦想大一点", "aim high": "目标高一点",
            "work hard": "努力工作", "study hard": "努力学习", "play hard": "努力玩",
            "stay healthy": "保持健康", "eat well": "吃好", "sleep well": "睡好",
            "exercise regularly": "经常锻炼", "stay fit": "保持健康", "be active": "要活跃",
            "learn something new": "学点新东西", "try something new": "尝试新事物",
            "explore the world": "探索世界", "travel often": "经常旅行", "meet new people": "认识新朋友",
            "make new friends": "交新朋友", "keep in touch": "保持联系", "stay connected": "保持联系",
            "be grateful": "要感恩", "count your blessings": "数数你的祝福", "appreciate life": "珍惜生活",
            "cherish every moment": "珍惜每一刻", "live in the moment": "活在当下",
            "be present": "要专注", "mindful": "正念", "meditate": "冥想",
            "relax": "放松", "take a break": "休息一下", "take a vacation": "去度假",
            "have fun": "玩得开心", "enjoy life": "享受生活", "be happy": "要快乐",
        }
        
        # 根据语言对返回对应的词典
        if self.source_lang.lower() == 'en' and self.target_lang.lower().startswith('zh'):
            return en_zh_dict
        else:
            return {}

    def _clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        text = text.replace(" .", ".")
        text = text.replace(" ,", ",")
        text = text.replace(" !", "!")
        text = text.replace(" ?", "?")
        
        return text

    def _translate_word(self, word: str) -> str:
        """翻译单个单词"""
        word_lower = word.lower()
        if word_lower in self.dictionary:
            return self.dictionary[word_lower]
        return word  # 如果词典中没有，返回原词

    def translate(self, text: str, use_context: bool = True) -> str:
        """
        翻译文本

        Args:
            text: 待翻译的文本
            use_context: 是否使用上下文

        Returns:
            翻译后的文本
        """
        text = self._clean_text(text)
        
        if not text:
            return ""

        if text in self.cache:
            return self.cache[text]

        # 分词翻译
        words = text.split()
        translated_words = []
        
        for word in words:
            # 去除标点
            clean_word = re.sub(r'[^\w\']', '', word)
            punctuation = re.sub(r'[\w\']', '', word)
            
            # 翻译
            translated = self._translate_word(clean_word)
            
            # 添加标点
            if punctuation:
                translated += punctuation
            
            translated_words.append(translated)

        translated = ' '.join(translated_words)

        # 存入缓存
        self.cache[text] = translated

        # 更新历史记录
        self.history.append({
            "source": text,
            "target": translated,
            "timestamp": time.time()
        })

        if len(self.history) > 20:
            self.history.pop(0)

        return translated

    def translate_with_context(self, text: str, context_window: int = 3) -> str:
        """带上下文的翻译"""
        return self.translate(text, use_context=True)

    def clear_cache(self):
        """清空翻译缓存"""
        self.cache = {}
        self.history = []
        print("翻译缓存已清空")


# 测试代码
if __name__ == "__main__":
    print("=== 测试本地词典翻译器 ===")
    
    translator = LocalTranslator(source_lang='en', target_lang='zh')
    
    test_texts = [
        "Hello, how are you?",
        "I am a student.",
        "This is a computer.",
        "I like programming.",
        "Artificial intelligence is amazing.",
        "Good morning!",
        "Thank you very much.",
        "See you later.",
    ]
    
    for text in test_texts:
        result = translator.translate(text)
        print(f"{text}\n→ {result}\n")