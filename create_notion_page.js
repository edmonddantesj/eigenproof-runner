const axios = require('axios');

const NOTION_API_KEY = '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';
const PARENT_PAGE_ID = '2fa9c616de8680959d61f1db1071a697';

const headers = {
  'Authorization': `Bearer ${NOTION_API_KEY}`,
  'Content-Type': 'application/json',
  'Notion-Version': '2022-06-28'
};

const pageData = {
  parent: {
    page_id: PARENT_PAGE_ID
  },
  title: [
    {
      type: "text",
      text: {
        content: "에드몽 - 프로필 & 장기메모리"
      }
    }
  ],
  children: [
    {
      object: "block",
      type: "heading_1",
      heading_1: {
        rich_text: [{ type: "text", text: { content: "🎯 기본정보" } }]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "이름: " } },
          { type: "text", text: { content: "에드몽", marks: [{ type: "bold" }] } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "직업: LK삼양 열화상사업센터 (기술영업 / 사업전략팀)" } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "가족: 아내 DUKI, 딸 ONE" } }
        ]
      }
    },
    {
      object: "block",
      type: "heading_1",
      heading_1: {
        rich_text: [{ type: "text", text: { content: "💬 대화 스타일" } }]
      }
    },
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: "반말 기반, 친근한 톤" } }]
      }
    },
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: "돌려 말하지 않음 → 직설적이고 명확한 답변" } }]
      }
    },
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: "때때로 재기 넘치는 유머" } }]
      }
    },
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: "미래지향적 제안" } }]
      }
    },
    {
      object: "block",
      type: "heading_1",
      heading_1: {
        rich_text: [{ type: "text", text: { content: "🚀 진행중인 프로젝트" } }]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "Narratr ($DOG 기반)", marks: [{ type: "bold" }] } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "KOL 요약/태그 자동화 플랫폼, 인공지능 기반 자동 분류" } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "열화상 FDS 솔루션", marks: [{ type: "bold" }] } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "SYMON 시스템 확대, 대시보드·모니터링" } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "Cybertruck 아카이브", marks: [{ type: "bold" }] } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "가격 전략, 의사결정 모델, 국내 시장 분석" } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "Kaito Educator Series", marks: [{ type: "bold" }] } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "Sentient, Talus, Limitless, Theo, STBL 투자/기술 분석" } }
        ]
      }
    },
    {
      object: "block",
      type: "heading_1",
      heading_1: {
        rich_text: [{ type: "text", text: { content: "💰 자산관리" } }]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "BTC 솔로 마이닝: Avalon Nano S3, 6TH/s" } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "포트폴리오: $CTC, $SPACE, RWA, STBL, Theo, Multipli" } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "부동산 다수 보유, 증여·절세 전략" } }
        ]
      }
    },
    {
      object: "block",
      type: "heading_1",
      heading_1: {
        rich_text: [{ type: "text", text: { content: "🛠 기술환경" } }]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "OS: macOS (초보 수준)" } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "개발: Node.js, JavaScript (초보 수준)" } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "관심: Supabase, 서버리스, CI/CD, Web3" } }
        ]
      }
    },
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          { type: "text", text: { content: "이미지 리소스: 시바견 후드티, 피자닌자, 도비 (프로젝트별 혼용 금지)" } }
        ]
      }
    },
    {
      object: "block",
      type: "heading_1",
      heading_1: {
        rich_text: [{ type: "text", text: { content: "📋 기억해야할 사항" } }]
      }
    },
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: "프로젝트별 작업 흐름 & 포맷 일관성 유지" } }]
      }
    },
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: "X(Twitter) 스레드: 250자 훅 → 본문 → 요약 구조" } }]
      }
    },
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: "Step-by-step 가이드는 terminal 명령 + 파일 경로 정확하게" } }]
      }
    },
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: "macOS 초보 → 권한/경로 문제 자주 발생" } }]
      }
    }
  ]
};

axios.post('https://api.notion.com/v1/pages', pageData, { headers })
  .then(response => {
    console.log('✅ Notion 페이지 생성 완료!');
    console.log('Page ID:', response.data.id);
    console.log('URL:', response.data.url);
  })
  .catch(error => {
    console.error('❌ 에러:', error.response?.data || error.message);
  });
