## 这套 HTML 与 Markdown 的关联关系：它在做什么任务/业务/职责？

### 关联关系（输入 → 输出）

- **Markdown（内容源）**：信息源，提供“事实与证据”——章节结构、要点、关键数字、案例与结论。
- **HTML（解读页）**：呈现层与传播载体，把 Markdown 内容**重写/重组**为适合手机阅读与分享的“竖屏分页科普稿”（横向滑动、卡片化、高亮关键数字）。

### 它所做的任务

- **信息抽取**：从 Markdown 里抽取最重要的观点、对比、指标、方法、经验与局限。
- **叙事重写**：把“原文结构”改写为“传播结构”（痛点 → 方法 → 结果 → 机制 → 总结）。
- **可视化表达**：把关键数字变成小卡片/流程卡；把复杂概念用类比页/分步流程解释。
- **前端落地**：输出一个能直接打开的单文件 HTML（内联 CSS），实现横向 scroll-snap；并且**禁止页内纵向滚动**（每页必须一屏放下，内容不够就分页拆分）。

### 职责边界

- **不负责**：补齐原文未给的数据、臆造指标或案例。
- **负责**：忠实提炼 Markdown 中“可验证的陈述/数字”，并用清晰的结构与视觉组件表达出来（同时减少术语堆砌）。

---

## 目标（通用）

给大模型一份通用 Prompt：当我提供**任意 Markdown（通用 Markdown，不限主题）**，或提供一个**参考风格 HTML** 时，它能够生成一个**类似风格与交互**的“2K 竖屏滑动解读页”单文件 HTML。

你可以用任何现成 HTML 作为风格参考（比如本目录的 `html_generater/2601.07372_intro.html`），但 Prompt 本身不应绑定某一篇 Markdown 内容。

---

## 你要给大模型的“生成提示词”（可直接复制使用）

> 说明：把下面提示词发给大模型，并把 Markdown 原文（或其摘录）贴进去，模型就应输出一份完整 HTML。

### 提示词正文（通用版，支持输入 Markdown 或参考 HTML）

你是一名擅长信息可视化与科普写作的前端工程师+研究员。请根据我提供的输入材料，生成一个用于“手机竖屏滑动解读”的**单文件 HTML**（不拆分为多个文件）。

#### 输入（我会提供以下之一或多项）
- **A. Markdown 原文/摘录**：标题、章节、要点、列表、表格、关键数字、示例或结论（我会粘贴给你）。
- **B. 参考风格 HTML**：一份现成 HTML（或其片段），你需要尽量复刻其视觉与组件结构（配色、布局、卡片组件、分页交互），但内容换成我的 Markdown。

#### 你需要做的事（务必遵守）
- **内容侧**：从 Markdown 材料中提炼要点，重组为易传播的叙事结构；对每个关键数字/结论，尽量给出“来自原文哪里”的上下文提示（如“来自章节小节/列表/表格描述”，无需精确页码）。
- **样式侧**：如果我提供了参考 HTML，你要尽可能复刻其视觉风格与组件 class；如果没提供，就按你内置的手写笔记/手帐风格输出。

#### 输出要求（非常重要）
- **只输出一份完整 HTML**（从 `<!DOCTYPE html>` 到 `</html>`），不要输出解释文字。
- 语言：**简体中文为主**，必要时在括号里附英文短语（与原文对齐）。
- 页面形态：**横向滑动分页**（类似 PPT），容器固定为竖屏卡片比例。
- 风格：**手写笔记/手帐风格**，像纸质笔记本/便签与手写标注；整体视觉与交互保持一致，但质感为“纸张、笔迹、贴纸”。
- **分页强约束**：**不允许任何 slide 内上下滚动**；每个 `.slide` 必须“屏内一页即一页”。如果内容放不下，必须**拆成更多页**或**删减**，宁可页数增加也不要溢出或滚动。

#### 结构与交互规范（按此实现）
- `body` 居中；主容器 `.mobile-container`：
  - `max-width: 720px; height: 100vh; display:flex; overflow-x: scroll; overflow-y: hidden; scroll-snap-type: x mandatory;`
  - 隐藏滚动条（webkit + firefox + ms）
- 每一页 `.slide`：
  - `flex-shrink: 0; width: 100%; aspect-ratio: 4 / 5; scroll-snap-align: start; padding: 40px;`
  - 页内必须 `overflow: hidden;`（禁止上下滚动与左右溢出）
  - 偶数页浅纸色、奇数页米白纸色
- 第 1 页为封面 `.slide.cover`：
  - 手帐封面质感（暖色纸张/封面卡纸），标题居中带手写感
  - 可包含一个 logo/主题图标（像贴纸），右侧加滑动提示符 `›`
- 文案组件（必须实现这些 class，便于复用；**命名不变，但视觉换成手写笔记风**）：
  - `.big-icon`：每页视觉锚点（大号 emoji），可做成“贴纸”效果
  - `.logo-img`：封面主视觉（圆角大图标/贴纸），建议 `width/height: 140px; border-radius: 28px; box-shadow` 明显
  - `.quote-card`：手帐便签块（浅色纸张 + 虚线边框/手绘边缘 + 轻阴影）
  - `.flow-card`：手绘流程块（淡色纸片 + 明显描边），字号偏大
  - `.arrow-down`：手绘箭头（使用内联 SVG），建议 `width:100%; text-align:center; color: var(--accent-color);`
  - `.scroll-hint`：每页右侧淡色 `›` 提示可横滑（封面可用更浅色）
  - `.spacer`：需要“把页脚顶到底部”时使用（`flex-grow: 1;`）
- 字体：优先 `Kaiti SC`、`KaiTi`、`STKaiti`、`FangSong`，回退 `Microsoft YaHei`、`sans-serif`
- 主题色变量（用于“纸张/墨色/贴纸”的统一风格）：
  - `--primary-color: #7c6f57; --bg-color:#efe7da; --accent-color:#c08457; --sub-text:#6b6457;`

#### 视觉与排版基线（**强制**，手写笔记/手帐风）
- **整体外壳**：`body` 用暖色“桌面底”背景，主容器 `.mobile-container` 有纸张/本子阴影与边框，容器内为浅米色纸张。
- **页面布局**：`.slide` 必须是 `display:flex; flex-direction:column; justify-content:center; align-items:flex-start; text-align:left;`（封面页例外居中）。
- **标题样式**：`h2` 用“手绘下划线或贴纸条”而不是现代左侧强调条，字号偏大（约 `2.0–2.4em`）。
- **段落字级**：`p` 字号偏大（约 `1.2–1.3em`），行高 `1.6`，颜色为深灰墨色，段间距舒展（`margin: 15px 0`）。
- **强调文字**：`strong` **必须**做“荧光笔高亮”效果（半透明笔刷底），不要只改颜色，避免满屏高亮。
- **封面质感**：封面为“手帐封面/卡纸”质感，可放 `logo-img`（像贴纸），并用半透明卡片承载“核心结论”。
- **分割与边界**：每页可用细虚线/纸张边界感，不要现代硬线；偶数页用不同纸色或不同纸张纹理。

#### 强制模板（**非常重要：请从模板复制开始，不要自由发挥**）

你输出的 HTML **必须**以以下 CSS/结构为基底（允许：替换文案、替换封面纸张配色、在局部元素上用 `style=""` 做便签色变体；不允许：删除/重命名核心 class、把版式改成非 flex、把 strong 改成纯色无底、把容器改成无纸张质感的“平面页面”）。

**A) CSS 模板（直接复制到 `<style>`；你可以微调数值，但总体风格要保持一致）**

```html
<style>
  :root {
    /* 手帐风主题色（纸张/墨色/贴纸） */
    --primary-color: #5b4f44; /* 墨色/标题色 */
    --accent-color: #c08457;  /* 贴纸/强调色 */
    --bg-color: #e9dfd2;      /* 桌面/外壳底 */
    --text-color: #3f3a32;    /* 正文墨色 */
    --card-bg: #fdf8f1;       /* 纸张底色 */
    --paper-alt: #f7efe5;     /* 另一张纸 */
    --line-color: rgba(120, 105, 90, 0.18);  /* 笔记横线 */
    --margin-line: rgba(198, 120, 110, 0.35); /* 书写边线 */
    --highlight-color: rgba(255, 219, 126, 0.65); /* 荧光笔 */
    --sub-text: #6b6457;

    /* 2K 竖屏卡片设计画布（4:5），用于“字号尺度感”参考 */
    --design-w: 1600px; /* 4 */
    --design-h: 2000px; /* 5 */
  }

  * { box-sizing: border-box; }

  body {
    font-family: 'Kaiti SC', 'KaiTi', 'STKaiti', 'FangSong', 'Microsoft YaHei', sans-serif;
    margin: 0;
    padding: 0;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    min-height: 100vh;
  }

  .mobile-container {
    /*
      固定页面比例为 4:5（2K 竖屏卡片思路）：
      - 高度跟随视口：100vh
      - 宽度锁定为 4/5 * 高度（同时不超过屏宽与最大宽度）
    */
    width: min(720px, 100vw, calc(100vh * 4 / 5));
    background: var(--card-bg);
    box-shadow: 0 18px 36px rgba(0,0,0,0.28);
    border: 1px solid rgba(90, 75, 60, 0.25);
    border-radius: 18px;
    overflow-x: scroll;
    overflow-y: hidden;
    scroll-snap-type: x mandatory;
    height: 100vh;
    scrollbar-width: none;
    -ms-overflow-style: none;
    display: flex;
    flex-direction: row;
  }
  .mobile-container::-webkit-scrollbar { display: none; }

  .slide {
    width: 100%;
    flex-shrink: 0;
    scroll-snap-align: start;
    padding: 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
    background-color: var(--card-bg);
    border-right: 1px dashed rgba(120, 105, 90, 0.25);
    position: relative;
    overflow: hidden; /* 强制：每页一屏，禁止上下滚动 */
    background-image:
      linear-gradient(90deg, var(--margin-line) 0 2px, transparent 2px),
      repeating-linear-gradient(to bottom, transparent 0, transparent 30px, var(--line-color) 31px);
    background-size: 100% 100%, 100% 31px;
    background-position: 0 0, 0 12px;
  }
  .slide:nth-child(even) { background-color: var(--paper-alt); }

  .slide.cover {
    background: linear-gradient(135deg, #f6e6cf 0%, #f2d8bb 100%);
    color: #3f352b;
    align-items: center;
    text-align: center;
    background-image: none;
  }

  /*
    移动端优先：整体字号再大一档。
    说明：这里用 em 保持“比例一致”，需要更大就整体上调这些数值。
  */
  h1 { font-size: clamp(30px, 3.4em, 56px); margin: 0 0 22px 0; line-height: 1.1; letter-spacing: 0.01em; }
  h2 {
    font-size: clamp(24px, 2.5em, 44px);
    color: var(--primary-color);
    margin: 0 0 28px 0;
    width: 100%;
    line-height: 1.3;
    padding-bottom: 8px;
    border-bottom: 3px dashed var(--accent-color);
  }
  p { font-size: clamp(18px, 1.38em, 26px); line-height: 1.6; margin: 16px 0; color: #4a4339; }
  .slide.cover p { color: #5a4d41; font-size: clamp(18px, 1.25em, 24px); }

  strong {
    color: var(--text-color);
    font-weight: 700;
    background: linear-gradient(transparent 52%, var(--highlight-color) 52%);
    padding: 2px 6px;
    border-radius: 4px;
  }

  .big-icon {
    font-size: 6em;
    margin-bottom: 30px;
    align-self: center;
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.12));
    transform: rotate(-2deg);
  }

  .logo-img {
    width: 140px;
    height: 140px;
    border-radius: 28px;
    margin-bottom: 30px;
    padding: 8px;
    background: #fff;
    border: 2px solid rgba(120, 105, 90, 0.2);
    box-shadow: 0 8px 16px rgba(0,0,0,0.18);
  }

  .quote-card {
    background: #fff6cc;
    border: 2px dashed rgba(120, 105, 90, 0.35);
    padding: 26px;
    border-radius: 14px;
    font-size: clamp(18px, 1.35em, 26px);
    margin: 20px 0;
    width: 100%;
    box-shadow: 0 8px 14px rgba(0, 0, 0, 0.08);
    color: #4a4339;
    line-height: 1.6;
    transform: rotate(-0.4deg);
  }

  .flow-card {
    background: #fffaf3;
    color: #5b4f44;
    padding: 20px;
    border-radius: 14px;
    font-size: clamp(18px, 1.35em, 26px);
    text-align: center;
    font-weight: 700;
    width: 100%;
    margin: 10px 0;
    border: 2px solid var(--accent-color);
  }

  .arrow-down {
    color: var(--accent-color);
    text-align: center;
    width: 100%;
    margin: 8px 0;
  }
  .arrow-down svg {
    width: 56px;
    height: 56px;
  }

  .scroll-hint {
    position: absolute;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    font-size: clamp(28px, 3.2em, 52px);
    color: rgba(60, 50, 40, 0.25);
    user-select: none;
  }

  .spacer { flex-grow: 1; }
</style>
```

#### 移动端字号与密度（**强制：手机用户优先**）

- **整体原则**：宁可“字大一点、页数多一点”，也不要字小密密麻麻。
- **标题字号下限**：封面 `h1` 必须足够大（用 `clamp(30px, 3.4em, 56px)`），`h2` 必须明显（不小于 24px）。
- **正文字号下限**：`p` 必须 `>= 18px`（建议用 `clamp(18px, 1.38em, 26px)`）。
- **卡片字号**：`quote-card/flow-card` 不得小于 18px，且不得小于正文。
- **行宽控制**：每页尽量用卡片、分行、短句控制行宽；避免一行超过 ~14–18 个汉字的“长行”。

#### 页面比例（**强制：4:5（2K）竖屏卡片**）

- 你生成的页面必须按 “4:5 竖屏卡片” 设计（可视区域像海报/PPT），并在 CSS 中通过：
  - `.mobile-container { height: 100vh; width: min(..., calc(100vh * 4 / 5)); }`
  来**锁定比例**（不要仅靠 `aspect-ratio` 让浏览器自由拉伸）。
- 每个 `.slide` 用 `width:100%` 跟随容器宽度即可（无需再额外指定 `aspect-ratio`）。

#### 主题色策略（**强制：手帐纸张 + 墨色 + 贴纸，不要固定蓝色**）

你必须在生成 HTML 时，先确定主题的“情绪色”（来自内容主题或组织品牌），然后**据此设置 CSS 变量**：`--primary-color`、`--accent-color`、`--bg-color`、`--card-bg`、`--paper-alt`、`--highlight-color`。规则如下：

**1) 选色流程（必须按顺序执行）**
- **Step A：墨色** → 填入 `--primary-color`
  - 选一个“可读性强的深色墨”，不要纯黑，偏棕灰/深褐更像手写笔记。
- **Step B：贴纸/强调色** → 填入 `--accent-color`
  - 从主题色取一档“温和但可见”的色，用于标题下划线、箭头、便签边框。
- **Step C：桌面/外壳底** → 填入 `--bg-color`
  - 用更深一档的暖色，让纸张更突出（像木桌/桌垫）。
- **Step D：纸张底色** → 填入 `--card-bg` 与 `--paper-alt`
  - 选择两种相近的米白/浅纸色，用于奇偶页区别。
- **Step E：荧光笔色** → 填入 `--highlight-color`
  - 高亮要“半透明荧光笔”，不要纯色块。

**2) 对比度与可读性（必须满足）**
- 正文在纸张上清晰可读，避免过浅墨色。
- `h2` 下划线、箭头、卡片描边统一使用 `--accent-color`。
- `strong` 只能用荧光笔高亮（`--highlight-color`），不要改成纯色。

**3) 可直接套用的“手帐配色例子”（仅作参考）**
- **原木手帐**：`--primary-color:#5b4f44; --accent-color:#c08457; --bg-color:#e9dfd2; --card-bg:#fdf8f1; --paper-alt:#f7efe5; --highlight-color:rgba(255,219,126,0.65);`
- **清爽绿笔记**：`--primary-color:#4a5a4f; --accent-color:#7fb48f; --bg-color:#e3eadf; --card-bg:#f8fbf7; --paper-alt:#f1f6ef; --highlight-color:rgba(193, 241, 205, 0.7);`
- **紫系手帐**：`--primary-color:#54495f; --accent-color:#9b7bd1; --bg-color:#e7e0ee; --card-bg:#fbf8ff; --paper-alt:#f4eefb; --highlight-color:rgba(216, 191, 255, 0.7);`
- **橙棕笔记**：`--primary-color:#5c4b3b; --accent-color:#d49a6a; --bg-color:#e8dbcf; --card-bg:#fff8f1; --paper-alt:#f7efe7; --highlight-color:rgba(255, 214, 170, 0.7);`

**4) 输出要求（必须）**
- 你输出的 CSS 变量必须是“最终值”（真实色值），不能留占位符。
- 全文（标题线、箭头、便签边框、高亮底色）必须只使用这套变量派生出来的颜色，避免“混入另一套风格色”。

**B) HTML 结构模板（直接复制到 `<body>`；你只需要替换每页的文案/数字/小组件）**

```html
<div class="mobile-container">

  <!-- P1: 封面 -->
  <div class="slide cover">
    <!-- 封面主视觉：必须“巨大”，二选一：品牌 Logo 或主题 Icon（见下方封面策略） -->
    <img src="https://avatars.githubusercontent.com/u/148330874?s=200&v=4" class="logo-img" alt="DeepSeek Logo">
    <h1>【Markdown 标题】<br>【短副标题】</h1>
    <p>【作者/组织/系列/年份】<br>【一句话结论】</p>
    <div style="background: rgba(255,255,255,0.7); border:2px dashed rgba(120,105,90,0.35); color:#4a4339; margin-top:40px; padding:20px; border-radius:12px; width:100%;">
      <p style="color:#4a4339; margin:0;">
        <strong>核心结论</strong><br>
        【2–3 行短句，像海报一样】<br>
        【可选：塞 1 个最炸裂数字/对比（例如 +5.0 BBH）】
      </p>
    </div>
    <div class="scroll-hint">›</div>
  </div>

  <!-- P2..P10: 内容页（每页建议：big-icon + h2 + p + 卡片化组件） -->
  <div class="slide">
    <span class="big-icon">😓</span>
    <h2>【本页标题】</h2>
    <p>【2–4 句短段落】</p>
    <div class="quote-card" style="background:#ffe9e7; color:#7a3a32; border-color:#e9b3ab;">
      【卡片正文，可用 <br> 换行；关键术语用 <strong> 浅底高亮】
    </div>
    <div class="scroll-hint">›</div>
  </div>

  <!-- 需要流程时：flow-card + arrow-down + flow-card（用 style 做红/绿变体） -->
  <div class="slide">
    <span class="big-icon">🛠️</span>
    <h2>【How it works】</h2>
    <div class="flow-card">输入</div>
    <div class="arrow-down" aria-hidden="true">
      <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" role="img">
        <path d="M32 10v34" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>
        <path d="M18 34l14 14 14-14" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <div class="flow-card" style="background:#e8f7ea; color:#2f5b3a; border-color:#a9d5b2;">核心模块</div>
    <div class="arrow-down" aria-hidden="true">
      <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" role="img">
        <path d="M32 10v34" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>
        <path d="M18 34l14 14 14-14" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <div class="flow-card">输出</div>
    <div class="scroll-hint">›</div>
  </div>

  <!-- 总结页：用 spacer 把页脚顶到底 -->
  <div class="slide">
    <span class="big-icon">🚀</span>
    <h2>【总结】</h2>
    <div class="quote-card">【Takeaway 1】</div>
    <div class="quote-card">【Takeaway 2】</div>
    <div class="quote-card">【Takeaway 3】</div>
    <div class="spacer"></div>
    <div style="font-size:0.9em; color:#94a3b8; text-align:center; padding-bottom:20px;">
      Source: 【Markdown 标题/章节标识】 | 【作者/组织（可选）】
    </div>
  </div>

</div>
```

**C) 变体规则（让页面“活”起来，但不破坏统一风格）**
- **粉色便签（问题/提醒）**：在 `quote-card/flow-card` 上用 `style="background:#ffe9e7; color:#7a3a32; border-color:#e9b3ab;"`
- **绿色便签（改进/收益）**：`style="background:#e8f7ea; color:#2f5b3a; border-color:#a9d5b2;"`
- **橙色便签（类比/提示）**：`style="background:#fff1df; color:#6a4a2e; border-color:#e0bb8c;"`
- **小数字网格**：允许在单页内用内联 `display:grid; grid-template-columns: 1fr 1fr 1fr; gap:8px; text-align:center;` 做 3 列小卡（只在 1 页使用，避免满屏网格）

#### 封面策略（阅读意愿优先，**强制执行**）

封面是整篇解读的“封皮”。很多人只看封面就决定是否继续阅读，所以封面必须满足：
- **一个巨大主视觉（必须）**：要么是品牌 Logo（作者/组织明确时），要么是主题 Icon（作者不突出或主题更重要时）。
- **一句话核心结论（必须）**：用 8–16 字的“结论式短句”，不要写背景铺垫。
- **一个硬数字（强烈建议）**：塞进封面结论卡里（例如 `+5.0 BBH` / `NIAH 84.2→97.0`），只放 1 个，越醒目越好。

**1) 主视觉选择规则（你必须按这个自动决策）**
- **如果作者/组织是品牌型（如 DeepSeek、OpenAI、Anthropic、Google 等）**：优先用“巨大品牌 Logo”做封面中心视觉。
  - 例：DeepSeek 可用 `https://avatars.githubusercontent.com/u/148330874?s=200&v=4`（和示例一致）。
- **如果主题比作者更重要（例如 Agent、RAG、MoE、推理、对齐、安全等）**：用“巨大极简主题 Icon”。
  - 要求：Icon 必须是**简约**、**单色或双层色**、**几何风**；不要用复杂插画。
  - 推荐：用内联 SVG（不依赖外链图片也能完整显示）。

**2) 主视觉尺寸与位置（必须）**
- **Logo/Image 方案**：把 `.logo-img` 视为“主海报视觉”，必须足够大：
  - 建议把 `.logo-img` 调整到 `width/height: 160–220px`（比示例更大），`border-radius: 28–40px`，并有明显阴影。
- **SVG Icon 方案**：Icon 视觉高度要接近 `120–180px`，居中，配轻投影。
- 无论哪种方案：主视觉必须位于封面上半部分中央；标题在其下；结论卡在更下方。

**3) 封面文案结构（必须像海报）**
- `h1`：中文标题（两行内，避免很长），必要时用 `<br>` 手动断行。
- `p`：一行“身份标识”（系列/章节/年份/组织），一行“一句话结论”。
- 结论卡（半透明块）：固定写“核心结论”，下面 2–3 行短句 + 可选 1 个硬数字。

**4) 封面模板（你必须二选一，并完整输出）**

- **A. 品牌 Logo 封面（优先）**：使用 `.logo-img`（大尺寸）+ 标题 + 结论卡。

- **B. 主题 SVG Icon 封面（当没有可靠 Logo 或主题更重要）**：把 `<img class="logo-img">` 替换为以下内联 SVG（示例为 Agent 图标，你要按主题替换图形，但保持“极简几何风”）：

```html
<div style="width:200px; height:200px; margin-bottom:30px; display:flex; align-items:center; justify-content:center; border-radius:32px; background: rgba(255,255,255,0.7); border:2px dashed rgba(120,105,90,0.35); box-shadow: 0 8px 16px rgba(0,0,0,0.12);">
  <svg width="140" height="140" viewBox="0 0 140 140" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Agent Icon">
    <rect x="18" y="24" width="104" height="84" rx="22" stroke="rgba(90,75,60,0.9)" stroke-width="8"/>
    <circle cx="52" cy="64" r="8" fill="rgba(90,75,60,0.9)"/>
    <circle cx="88" cy="64" r="8" fill="rgba(90,75,60,0.9)"/>
    <path d="M46 90C56 98 84 98 94 90" stroke="rgba(90,75,60,0.9)" stroke-width="8" stroke-linecap="round"/>
    <path d="M42 24L30 10" stroke="rgba(90,75,60,0.9)" stroke-width="8" stroke-linecap="round"/>
    <path d="M98 24L110 10" stroke="rgba(90,75,60,0.9)" stroke-width="8" stroke-linecap="round"/>
  </svg>
</div>
```

**5) 可靠性要求（必须）**
- 即使图片加载失败：封面仍然要“好看且信息完整”（标题+结论卡必须能独立成立）。
- 不要把关键信息写在图片里（图片只负责氛围与识别度）。

#### 内容编排：必须生成 8–12 页（通用叙事模板）

按“痛点 → 方法 → 结果 → 机制/洞察 → 总结”的传播叙事组织。下面是**强制页面骨架**（你必须按顺序产出；但每页细节根据 Markdown 替换）：

1) **封面**
   - Markdown 标题（中文概括）+ 作者/组织（可选）+ 标识（系列/章节/年份）
   - 一句话核心结论（从原文提炼）

2) **问题/动机（Before）**
   - 旧做法的瓶颈/成本/失败案例（从原文开头或背景段落提炼）
   - 用 1 个卡片写清“为什么现在要做这件事”

3) **关键想法（Big Idea）**
   - 用 1–2 句把核心观点/方法/框架讲清楚
   - 配一个流程卡：输入 → 核心模块 → 输出

4) **方法拆解（How it works）**
   - 3–5 个要点卡（每条回答：它做什么 + 解决什么）
   - 避免术语堆砌：术语出现时，必须配一句白话解释

5) **与基线/相关方法对比（Why it’s better）**
   - 旧做法 vs 新做法：更快/更准/更省/更稳 的原因
   - 用对照卡表达（可包含局限/代价）

6) **结果与证据（Headline numbers）**
   - 选 2–6 个最重要数字做“数字小卡片”
   - 每个数字写明：指标名 + 提升方向 + 对比对象（来自原文数据/表格/示例）

7) **进一步分析/机制解释（Insight）**
   - 讲清楚为什么会提升（机制或经验观察）
   - 如果原文有分析方法（如可视化/对比/案例拆解），用一页解释其结论

8) **适用边界与局限（When it fails / trade-offs）**
   - 至少给出 2 条：适用条件、潜在风险、工程成本或下一步

9) **类比页（强烈建议，便于传播）**
   - 用生活类比把核心概念再讲一遍（短、押韵、易记）

10) **总结页**
   - 3 条 takeaways：是什么、为什么有用、下一步意味着什么
   - 页脚：来源标识（Markdown 标题/章节）+ 作者/组织（可选）

#### 文案风格约束
- 每页 1 个明确标题（`h2`），段落不要太长（2–4 句内），尽量卡片化呈现。
- 关键术语用 `<strong>` 高亮，但不要全页都是高亮。
- 可以使用 1 个大图标（emoji 或 SVG）作为每页视觉锚点，但要克制（不超过 1 个）。

#### 资源与安全约束
- 允许引用外链图片（如 GitHub avatar），但请保证没有也能正常阅读（即不依赖图片表达关键信息）。
- 不要引入任何外部 JS/CSS 文件；所有 CSS 写在 `<style>` 内。

#### 输出检查清单（输出前自检）
- [ ] HTML 单文件，能直接打开渲染
- [ ] 横向 scroll-snap 生效；**slide 内无纵向滚动（overflow hidden）**
- [ ] 8–12 页，叙事完整，关键数字清晰
- [ ] 样式接近手帐：暖色桌面底 + 米白纸张交替页 + 便签/贴纸卡片