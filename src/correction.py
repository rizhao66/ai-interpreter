"""
纠错模块 - 滑动窗口重叠识别与自动修正
"""

import time
import re
from collections import deque
from typing import List, Tuple, Optional


class SlidingWindowCorrector:
    """滑动窗口纠错器"""

    def __init__(self, window_size: int = 3, overlap: float = 0.5):
        """
        初始化纠错器

        Args:
            window_size: 滑动窗口大小（秒）
            overlap: 重叠比例（0.3-0.7）
        """
        self.window_size = window_size
        self.overlap = overlap
        self.text_history = deque(maxlen=10)  # 历史文本
        self.correction_count = 0
        self.last_corrected_text = ""

    def compute_similarity(self, text1: str, text2: str) -> float:
        """计算两段文本的相似度"""
        if not text1 or not text2:
            return 0.0

        # 分词
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        # Jaccard 相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def find_best_correction(self, new_text: str, old_text: str) -> Tuple[str, bool]:
        """
        找出最佳修正方案

        Args:
            new_text: 新识别的文本
            old_text: 旧的文本

        Returns:
            (修正后的文本, 是否发生了修正)
        """
        if not new_text:
            return old_text, False

        if not old_text:
            return new_text, False

        # 计算相似度
        similarity = self.compute_similarity(new_text, old_text)

        # 如果相似度很高，说明可能是重复识别，不修正
        if similarity > 0.8:
            return old_text, False

        # 如果新文本明显更长，可能是补充识别
        if len(new_text.split()) > len(old_text.split()) * 1.2:
            # 检查新文本是否包含旧文本
            if old_text.lower() in new_text.lower():
                self.correction_count += 1
                return new_text, True

        # 如果旧文本明显更长，可能是之前识别过度
        if len(old_text.split()) > len(new_text.split()) * 1.2:
            if new_text.lower() in old_text.lower():
                self.correction_count += 1
                return new_text, True

        return new_text, False

    def correct_with_context(self, new_text: str, confidence: float = 0.7) -> str:
        """
        结合上下文进行纠错

        Args:
            new_text: 新识别的文本
            confidence: 识别置信度（0-1）

        Returns:
            纠错后的文本
        """
        if not new_text or confidence < 0.5:
            return self.last_corrected_text if self.last_corrected_text else new_text

        # 与上一帧对比
        if self.text_history:
            last_text = self.text_history[-1]
            corrected, has_correction = self.find_best_correction(new_text, last_text)

            if has_correction:
                print(f"[纠错] {last_text} → {corrected}")

            self.last_corrected_text = corrected
            self.text_history.append(corrected)
            return corrected

        # 没有历史记录，直接返回
        self.text_history.append(new_text)
        self.last_corrected_text = new_text
        return new_text

    def get_stats(self) -> dict:
        """获取纠错统计"""
        return {
            "correction_count": self.correction_count,
            "history_size": len(self.text_history),
            "last_text": self.last_corrected_text
        }

    def reset(self):
        """重置纠错器"""
        self.text_history.clear()
        self.correction_count = 0
        self.last_corrected_text = ""


class ContextualTranslator:
    """上下文感知翻译器 - 保证术语一致性"""

    def __init__(self, translator):
        """
        初始化上下文翻译器

        Args:
            translator: 基础翻译器实例
        """
        self.translator = translator
        self.term_cache = {}  # 术语缓存
        self.context_window = []  # 上下文窗口

    def register_term(self, source: str, target: str):
        """注册自定义术语映射"""
        self.term_cache[source.lower()] = target

    def translate_with_context(self, text: str, context_size: int = 3) -> str:
        """
        带上下文的翻译

        Args:
            text: 待翻译文本
            context_size: 上下文窗口大小

        Returns:
            翻译后的文本
        """
        if not text:
            return ""

        # 1. 先应用术语缓存
        for source, target in self.term_cache.items():
            if source in text.lower():
                text = text.lower().replace(source, target)

        # 2. 使用基础翻译器翻译
        translated = self.translator.translate(text)

        # 3. 更新上下文窗口
        self.context_window.append({
            "source": text,
            "target": translated,
            "timestamp": time.time()
        })

        # 保持窗口大小
        if len(self.context_window) > context_size:
            self.context_window.pop(0)

        return translated

    def get_consistent_translation(self, text: str) -> str:
        """
        获取一致的翻译（保证同一术语翻译相同）
        """
        # 提取关键词
        words = text.lower().split()

        # 检查是否有已注册的术语
        for word in words:
            if word in self.term_cache:
                # 使用注册的翻译
                return self.translator.translate(text)

        return self.translator.translate(text)