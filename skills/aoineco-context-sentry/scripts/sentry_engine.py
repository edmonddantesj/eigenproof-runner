#!/usr/bin/env python3
"""
🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill
S-DNA: AOI-2026-0213-SDNA-CS01

Aoineco Context-Sentry — Intelligent Context Diet Engine
Layer 1: Noise Filter (FREE, 10+ languages, regex-based)
Layer 2: Semantic Compression (PAID, LLM-based summarization)
Layer 3: Priority Retention (Sacred keyword protection)

Copyright (c) 2026 Aoineco & Co. All rights reserved.
"""

import re
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone, timedelta

__sdna__ = {
    "protocol": "aoineco-sdna-v1",
    "id": "AOI-2026-0213-SDNA-CS01",
    "author_agent": "aoineco-collective",
    "org": "aoineco-co",
    "created": "2026-02-13T11:50:00+09:00",
    "tier": "standard",
    "nexus_compatible": True,
    "classification": "open",
}

KST = timezone(timedelta(hours=9))


# ═══════════════════════════════════════════════════════════
# LAYER 1: GLOBAL NOISE FILTER (FREE — 10+ Languages)
# Zero LLM cost. Pure regex. < 1ms per message.
# ═══════════════════════════════════════════════════════════

NOISE_PATTERNS = {
    "en": {
        "filler": [
            r"^(Sure|Got it|Understood|OK|Okay|I see|Alright|Right|Yeah|Yep|Yup)[.!,]*$",
            r"^(Thank you|Thanks|Thx|Ty)[.!]*$",
            r"^(Great|Awesome|Perfect|Nice|Cool|Good)[.!]*$",
            r"^(I understand|Makes sense|Of course|Absolutely|Definitely)[.!]*$",
            r"^(Hmm|Hm|Ah|Oh|Uh|Um)[.!,]*$",
        ],
        "acknowledgment": [
            r"^(Yes|No|Yep|Nope|Nah)[.!,]*$",
            r"^(I agree|Agreed|Exactly|Indeed|True|Correct)[.!]*$",
        ],
    },
    "ko": {
        "filler": [
            r"^(알겠습니다|알겠어|알았어|네|예|응|ㅇㅇ|ㅇ|넹|넵)[.!]*$",
            r"^(감사합니다|고마워|ㄱㅅ|감사)[.!]*$",
            r"^(좋아|좋아요|좋습니다|좋네|좋다|굿|ㄱㄱ)[.!]*$",
            r"^(이해했습니다|이해했어|알겠어요)[.!]*$",
            r"^(ㅋㅋ|ㅎㅎ|ㅋㅋㅋ|ㅎㅎㅎ|ㅋ|ㅎ)+$",
            r"^(오|아|음|흠|어)[.!]*$",
        ],
        "acknowledgment": [
            r"^(맞아|맞아요|맞습니다|그래|그렇지|그렇네|ㅇㅇ)[.!]*$",
            r"^(동의|동의해|ㅇㅈ|인정)[.!]*$",
        ],
    },
    "ja": {
        "filler": [
            r"^(はい|うん|ええ|そうですね|なるほど|了解|わかりました|承知しました)[。！]*$",
            r"^(ありがとうございます|ありがとう|どうも)[。！]*$",
            r"^(いいですね|いいね|すごい|素晴らしい)[。！]*$",
        ],
        "acknowledgment": [
            r"^(そうです|その通り|確かに|おっしゃる通り)[。！]*$",
        ],
    },
    "zh": {
        "filler": [
            r"^(好的|明白了|收到|知道了|了解|嗯|哦|啊)[。！]*$",
            r"^(谢谢|感谢|多谢)[。！]*$",
            r"^(不错|很好|太好了|棒|厉害)[。！]*$",
        ],
        "acknowledgment": [
            r"^(对|是的|没错|正确|同意)[。！]*$",
        ],
    },
    "es": {
        "filler": [
            r"^(Entendido|Vale|De acuerdo|OK|Sí|Claro|Bueno)[.!]*$",
            r"^(Gracias|Genial|Perfecto|Bien)[.!]*$",
        ],
    },
    "fr": {
        "filler": [
            r"^(Compris|D'accord|OK|Oui|Bien sûr|Entendu|Parfait)[.!]*$",
            r"^(Merci|Super|Très bien|Excellent)[.!]*$",
        ],
    },
    "de": {
        "filler": [
            r"^(Verstanden|Okay|OK|Alles klar|Ja|Klar|Gut)[.!]*$",
            r"^(Danke|Super|Perfekt|Prima|Toll)[.!]*$",
        ],
    },
    "pt": {
        "filler": [
            r"^(Entendido|Certo|OK|Sim|Claro|Beleza|Legal)[.!]*$",
            r"^(Obrigado|Obrigada|Valeu|Perfeito)[.!]*$",
        ],
    },
    "ar": {
        "filler": [
            r"^(حسنا|فهمت|تمام|نعم|أوك|طيب)[.!]*$",
            r"^(شكرا|ممتاز|رائع)[.!]*$",
        ],
    },
    "hi": {
        "filler": [
            r"^(ठीक है|समझ गया|हाँ|जी|अच्छा|ओके)[.!]*$",
            r"^(धन्यवाद|शुक्रिया|बढ़िया)[.!]*$",
        ],
    },
}

# Flatten all patterns for quick global scan
ALL_NOISE_PATTERNS = []
for lang, categories in NOISE_PATTERNS.items():
    for cat, patterns in categories.items():
        ALL_NOISE_PATTERNS.extend(patterns)


# ═══════════════════════════════════════════════════════════
# LAYER 3: SACRED KEYWORDS (Never compress/remove these)
# ═══════════════════════════════════════════════════════════

SACRED_KEYWORDS = [
    # Identity & Soul
    "IDENTITY", "SOUL", "PERSONA", "CHARACTER",
    # Security
    "S-DNA", "GUARDIAN", "API_KEY", "SECRET", "PASSWORD", "WALLET",
    "PRIVATE_KEY",
    # Governance
    "CRITICAL", "DECISION", "APPROVED", "CONFIRMED", "CHAIRMAN",
    "VETO", "L3",
    # Business
    "$AOI", "NEXUS", "SURVIVAL", "REVENUE", "TOKENOMICS",
    # User-specific (Aoineco & Co.)
    "의장님", "에드몽", "청묘", "Aoineco",
    # Technical anchors
    "DEPLOYED", "SUBMITTED", "MERGED", "HOTFIX",
]


# ═══════════════════════════════════════════════════════════
# TOOL RESPONSE COMPRESSOR
# ═══════════════════════════════════════════════════════════

class ToolResponseCompressor:
    """
    Compress verbose tool call responses that waste context.
    E.g., a 500-line git log → "Git log: 47 commits, latest: abc123"
    """
    
    COMPRESSIBLE_PATTERNS = {
        "error_trace": {
            "pattern": r"Traceback \(most recent call last\):[\s\S]*?(?=\n\n|\Z)",
            "compress_to": "[TRACEBACK: {lines} lines — last error: {last_line}]",
        },
        "empty_result": {
            "pattern": r'\{"status":\s*"error"[^}]*\}',
            "compress_to": "[ERROR RESPONSE — skipped]",
        },
        "repeated_output": {
            "threshold": 3,  # If same output appears 3+ times
            "compress_to": "[REPEATED {count}x — showing once]",
        },
    }
    
    def compress_tool_response(self, response: str, max_lines: int = 20) -> str:
        """Compress a single tool response to essential information."""
        lines = response.strip().split('\n')
        
        if len(lines) <= max_lines:
            return response  # Short enough, keep as-is
        
        # Extract first and last lines as summary
        header = '\n'.join(lines[:5])
        footer = '\n'.join(lines[-3:])
        omitted = len(lines) - 8
        
        return f"{header}\n[... {omitted} lines omitted by Context-Sentry ...]\n{footer}"


# ═══════════════════════════════════════════════════════════
# CONTEXT SENTRY ENGINE
# ═══════════════════════════════════════════════════════════

@dataclass
class Message:
    role: str           # "user", "assistant", "system", "tool"
    content: str
    turn_index: int     # Position in conversation (0 = oldest)
    token_estimate: int = 0
    
    def __post_init__(self):
        if self.token_estimate == 0:
            # Rough estimate: 1 token ≈ 4 chars (English) or 2 chars (CJK)
            cjk_count = len(re.findall(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]', self.content))
            ascii_count = len(self.content) - cjk_count
            self.token_estimate = (ascii_count // 4) + (cjk_count // 2)


@dataclass
class DiagnosticReport:
    total_messages: int
    total_tokens_estimate: int
    noise_messages: int
    noise_tokens: int
    sacred_messages: int
    sacred_tokens: int
    compressible_messages: int
    compressible_tokens: int
    potential_savings_tokens: int
    potential_savings_percent: float
    recommendation: str


class ContextSentry:
    """
    The 3-Layer Context Diet Engine.
    
    Layer 1 (Noise Filter):     FREE — Regex, zero-cost, 10+ languages
    Layer 2 (Semantic Compress): PAID — LLM-based, meaningful summarization
    Layer 3 (Priority Retain):   AUTO — Sacred keywords always preserved
    """
    
    COMPRESSION_AGE = 10  # Messages older than 10 turns are compressible
    
    def __init__(self, languages: List[str] = None):
        """Initialize with supported languages. Default: all."""
        if languages:
            self.noise_patterns = []
            for lang in languages:
                if lang in NOISE_PATTERNS:
                    for cat_patterns in NOISE_PATTERNS[lang].values():
                        self.noise_patterns.extend(cat_patterns)
        else:
            self.noise_patterns = ALL_NOISE_PATTERNS
        
        self.tool_compressor = ToolResponseCompressor()
    
    def is_noise(self, content: str) -> bool:
        """Check if a message is pure noise (Layer 1)."""
        text = content.strip()
        if not text or len(text) > 100:
            # Empty or too long to be simple filler
            return len(text) == 0
        
        for pattern in self.noise_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def is_sacred(self, content: str) -> bool:
        """Check if a message contains sacred keywords (Layer 3)."""
        for keyword in SACRED_KEYWORDS:
            if keyword.lower() in content.lower():
                return True
        return False
    
    def diagnose(self, messages: List[Message]) -> DiagnosticReport:
        """Analyze current context and produce a diet plan."""
        total_tokens = sum(m.token_estimate for m in messages)
        
        noise_msgs = []
        sacred_msgs = []
        compressible_msgs = []
        
        current_turn = max(m.turn_index for m in messages) if messages else 0
        
        for msg in messages:
            age = current_turn - msg.turn_index
            
            if self.is_noise(msg.content):
                noise_msgs.append(msg)
            elif self.is_sacred(msg.content):
                sacred_msgs.append(msg)
            elif age > self.COMPRESSION_AGE and msg.role != "system":
                compressible_msgs.append(msg)
        
        noise_tokens = sum(m.token_estimate for m in noise_msgs)
        sacred_tokens = sum(m.token_estimate for m in sacred_msgs)
        compressible_tokens = sum(m.token_estimate for m in compressible_msgs)
        
        # Potential savings: all noise + 70% of compressible
        savings = noise_tokens + int(compressible_tokens * 0.7)
        savings_pct = round(savings / max(total_tokens, 1) * 100, 1)
        
        return DiagnosticReport(
            total_messages=len(messages),
            total_tokens_estimate=total_tokens,
            noise_messages=len(noise_msgs),
            noise_tokens=noise_tokens,
            sacred_messages=len(sacred_msgs),
            sacred_tokens=sacred_tokens,
            compressible_messages=len(compressible_msgs),
            compressible_tokens=compressible_tokens,
            potential_savings_tokens=savings,
            potential_savings_percent=savings_pct,
            recommendation=self._recommend(savings_pct, total_tokens),
        )
    
    def execute_diet(self, messages: List[Message],
                     enable_layer2: bool = False) -> Tuple[List[Message], Dict]:
        """
        Execute the context diet.
        
        Layer 1 (FREE): Remove noise messages entirely.
        Layer 2 (PAID): Summarize old messages (requires LLM callback).
        Layer 3 (AUTO): Never touch sacred messages.
        """
        current_turn = max(m.turn_index for m in messages) if messages else 0
        optimized = []
        stats = {
            "removed_noise": 0,
            "compressed_semantic": 0,
            "preserved_sacred": 0,
            "kept_recent": 0,
            "compressed_tools": 0,
        }
        
        for msg in messages:
            age = current_turn - msg.turn_index
            
            # Layer 1: Remove noise
            if self.is_noise(msg.content):
                stats["removed_noise"] += 1
                continue
            
            # Layer 3: Preserve sacred
            if self.is_sacred(msg.content):
                optimized.append(msg)
                stats["preserved_sacred"] += 1
                continue
            
            # Compress tool responses regardless of age
            if msg.role == "tool":
                compressed_content = self.tool_compressor.compress_tool_response(
                    msg.content, max_lines=15
                )
                optimized.append(Message(
                    role=msg.role,
                    content=compressed_content,
                    turn_index=msg.turn_index,
                ))
                if len(compressed_content) < len(msg.content):
                    stats["compressed_tools"] += 1
                else:
                    stats["kept_recent"] += 1
                continue
            
            # Layer 2: Semantic compression for old messages (PAID)
            if enable_layer2 and age > self.COMPRESSION_AGE:
                # In production: call LLM to summarize
                # For now: truncate to first 200 chars + "..."
                summary = msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
                optimized.append(Message(
                    role=msg.role,
                    content=f"[COMPRESSED] {summary}",
                    turn_index=msg.turn_index,
                ))
                stats["compressed_semantic"] += 1
                continue
            
            # Keep recent messages as-is
            optimized.append(msg)
            stats["kept_recent"] += 1
        
        return optimized, stats
    
    def realtime_monitor(self, usage_percent: float) -> Dict:
        """Monitor context usage and provide alerts."""
        if usage_percent >= 80:
            return {
                "alert": "🔴 CRITICAL",
                "level": "critical",
                "action": "immediate_compact",
                "message": f"⚠️ Context {usage_percent:.0f}%! Immediate compression required.",
            }
        elif usage_percent >= 60:
            return {
                "alert": "🟡 WARNING",
                "level": "warning",
                "action": "prepare_compact",
                "message": f"⚠️ Context {usage_percent:.0f}%. Preparing compression.",
            }
        elif usage_percent >= 40:
            return {
                "alert": "🟢 MONITOR",
                "level": "monitor",
                "action": "log_only",
                "message": f"Context {usage_percent:.0f}%. Stable. Monitoring.",
            }
        else:
            return {
                "alert": "🧊 OPTIMAL",
                "level": "optimal",
                "action": "none",
                "message": f"Context {usage_percent:.0f}%. Optimal performance.",
            }
    
    def _recommend(self, savings_pct: float, total_tokens: int) -> str:
        if savings_pct > 40:
            return f"🔴 Heavy diet needed! {savings_pct}% savings possible. Run Layer 1+2 now."
        elif savings_pct > 20:
            return f"🟡 Moderate diet available. {savings_pct}% savings. Layer 1 recommended."
        elif savings_pct > 5:
            return f"🟢 Light cleanup. {savings_pct}% savings with noise removal."
        else:
            return "🧊 Context is clean. No diet needed."


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════

def demo():
    """Demonstrate the Context Sentry engine."""
    print("=" * 60)
    print("🗑️ AOINECO CONTEXT-SENTRY — Context Diet Demo")
    print("   10+ Languages. Zero Waste. Maximum Intelligence.")
    print("=" * 60)
    
    sentry = ContextSentry()
    
    # Simulated conversation
    messages = [
        Message(role="user", content="BTC 분석해줘", turn_index=0),
        Message(role="assistant", content="네, BTC를 분석하겠습니다. 현재 $66,000 부근에서...", turn_index=1),
        Message(role="user", content="알겠습니다", turn_index=2),  # NOISE (ko)
        Message(role="user", content="OK", turn_index=3),  # NOISE (en)
        Message(role="user", content="좋아", turn_index=4),  # NOISE (ko)
        Message(role="tool", content='{"status":"error","message":"API timeout"}\n' * 20, turn_index=5),
        Message(role="assistant", content="CRITICAL: $AOI 의장님 승인이 필요한 결정입니다", turn_index=6),  # SACRED
        Message(role="user", content="はい", turn_index=7),  # NOISE (ja)
        Message(role="user", content="Verstanden", turn_index=8),  # NOISE (de)
        Message(role="user", content="다음 단계로 넘어가자", turn_index=9),
        Message(role="assistant", content="Phase 2를 시작하겠습니다..." + "A" * 500, turn_index=10),
        Message(role="user", content="ㅋㅋㅋ", turn_index=11),  # NOISE (ko)
        Message(role="user", content="Perfecto", turn_index=12),  # NOISE (es)
        Message(role="assistant", content="S-DNA Protocol을 설계 중입니다. 의장님의 승인이 필요합니다.", turn_index=13),  # SACRED
        Message(role="user", content="현재를 저장해줘", turn_index=14),
    ]
    
    # Diagnose
    print("\n📊 DIAGNOSIS")
    print("-" * 40)
    report = sentry.diagnose(messages)
    print(f"  Total Messages: {report.total_messages}")
    print(f"  Total Tokens (est): {report.total_tokens_estimate}")
    print(f"  Noise Messages: {report.noise_messages} ({report.noise_tokens} tokens)")
    print(f"  Sacred Messages: {report.sacred_messages} ({report.sacred_tokens} tokens)")
    print(f"  Compressible: {report.compressible_messages} ({report.compressible_tokens} tokens)")
    print(f"  Potential Savings: {report.potential_savings_tokens} tokens ({report.potential_savings_percent}%)")
    print(f"  → {report.recommendation}")
    
    # Execute diet
    print("\n🗑️ EXECUTING DIET (Layer 1 + Tool Compression)")
    print("-" * 40)
    optimized, stats = sentry.execute_diet(messages, enable_layer2=False)
    print(f"  Removed noise: {stats['removed_noise']}")
    print(f"  Compressed tools: {stats['compressed_tools']}")
    print(f"  Preserved sacred: {stats['preserved_sacred']}")
    print(f"  Kept recent: {stats['kept_recent']}")
    print(f"  Result: {len(messages)} → {len(optimized)} messages")
    
    # Realtime monitor
    print("\n📡 REALTIME MONITOR")
    print("-" * 40)
    for pct in [12, 42, 63, 85]:
        status = sentry.realtime_monitor(pct)
        print(f"  {status['alert']} {status['message']}")
    
    # Language detection showcase
    print("\n🌍 GLOBAL NOISE DETECTION")
    print("-" * 40)
    test_phrases = [
        ("en", "Got it!"),
        ("ko", "알겠습니다"),
        ("ja", "わかりました"),
        ("zh", "明白了"),
        ("de", "Verstanden"),
        ("es", "Entendido"),
        ("fr", "Compris"),
        ("pt", "Certo"),
        ("ko", "이건 중요한 CRITICAL 결정이야"),  # NOT noise (sacred)
    ]
    for lang, phrase in test_phrases:
        is_n = sentry.is_noise(phrase)
        is_s = sentry.is_sacred(phrase)
        status = "🗑️ NOISE" if is_n else ("🛡️ SACRED" if is_s else "✅ KEEP")
        print(f"  [{lang}] \"{phrase}\" → {status}")
    
    print("\n" + "=" * 60)
    return report


if __name__ == "__main__":
    demo()
