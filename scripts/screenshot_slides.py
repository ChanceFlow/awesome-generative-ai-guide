#!/usr/bin/env python3
"""
HTML 幻灯片截图工具

将本地 HTML 文件中的每个 .slide 元素截取为独立的 JPEG 图片。
"""

import argparse
import re
import sys
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

# 默认字体文件路径（华文楷体）
DEFAULT_FONT_PATH = Path(__file__).parent / "Fonts" / "STKaiti.ttf"
DEFAULT_FONT_FAMILY = "STKaiti"


def inject_font_css(
    page: Page,
    font_path: Path,
    font_family: str,
    text_stroke: float = 0.0,
) -> None:
    """
    向页面注入自定义字体 CSS。

    Args:
        page: Playwright 页面对象
        font_path: 字体文件路径
        font_family: 字体族名称
        text_stroke: 文字描边宽度（px），用于增加字重效果
    """
    font_url = font_path.resolve().as_uri()

    # 构建字重增强 CSS（使用 -webkit-text-stroke 模拟加粗）
    stroke_css = ""
    if text_stroke > 0:
        stroke_css = f"""
            -webkit-text-stroke: {text_stroke}px currentColor;
            paint-order: stroke fill;
        """

    css = f"""
        @font-face {{
            font-family: '{font_family}';
            src: url('{font_url}') format('truetype');
            font-weight: normal;
            font-style: normal;
        }}
        body, .slide, .slide * {{
            font-family: '{font_family}', 'Kaiti SC', 'KaiTi', serif !important;
            {stroke_css}
        }}
    """
    page.add_style_tag(content=css)


def parse_size(size_str: str) -> tuple[int, int]:
    """
    解析尺寸字符串，格式为 widthxheight。

    Args:
        size_str: 尺寸字符串，如 "1500x2000"

    Returns:
        (width, height) 元组

    Raises:
        argparse.ArgumentTypeError: 格式不正确时抛出
    """
    match = re.match(r"^(\d+)x(\d+)$", size_str.lower())
    if not match:
        raise argparse.ArgumentTypeError(
            f"尺寸格式错误: '{size_str}'，应为 widthxheight，如 1500x2000"
        )
    return int(match.group(1)), int(match.group(2))


def preview_page(
    html_file: Path,
    width: int = 1500,
    height: int = 2000,
    scale: float = 1.0,
    font_path: Path | None = None,
    font_family: str = DEFAULT_FONT_FAMILY,
    text_stroke: float = 0.0,
) -> None:
    """
    在浏览器窗口中预览 HTML 页面效果。

    打开一个可视化的浏览器窗口，应用所有样式设置，等待用户关闭。

    Args:
        html_file: 本地 HTML 文件路径
        width: 视口宽度
        height: 视口高度
        scale: 浏览器缩放比例 (CSS zoom)，类似 Ctrl+/- 效果
        font_path: 自定义字体文件路径，默认使用华文楷体
        font_family: 字体族名称
        text_stroke: 文字描边宽度（px），用于增加字重效果
    """
    # 设置默认字体路径
    if font_path is None:
        font_path = DEFAULT_FONT_PATH

    # 验证文件存在
    if not html_file.exists():
        raise FileNotFoundError(f"HTML 文件不存在: {html_file}")

    # 构建 file:// URL
    file_url = html_file.resolve().as_uri()

    with sync_playwright() as p:
        # 启动浏览器（非无头模式，显示窗口）
        browser = p.chromium.launch(headless=False)

        # 创建上下文，设置视口
        context = browser.new_context(
            viewport={"width": width, "height": height},
        )

        page = context.new_page()

        # 加载本地 HTML 文件
        page.goto(file_url)

        # 等待页面加载完成
        page.wait_for_load_state("networkidle")

        # 注入自定义字体（华文楷体）
        if font_path.exists():
            inject_font_css(page, font_path, font_family, text_stroke)
            # 等待字体加载
            page.wait_for_timeout(200)
            stroke_info = f"，字重+{text_stroke}px" if text_stroke > 0 else ""
            print(f"已加载字体: {font_family} ({font_path.name}){stroke_info}")
        else:
            print(f"警告: 字体文件不存在: {font_path}")

        # 应用浏览器缩放（CSS zoom，类似 Ctrl+/-）
        if scale != 1.0:
            page.evaluate(f"document.body.style.zoom = {scale}")
            # 等待缩放生效
            page.wait_for_timeout(100)

        print(f"预览模式 - 视口尺寸: {width}x{height}px，缩放: {scale}x")
        print("按 Enter 键关闭浏览器...")

        # 等待用户输入
        input()

        browser.close()


def screenshot_slides(
    html_file: Path,
    width: int = 1500,
    height: int = 2000,
    scale: float = 1.0,
    quality: int = 90,
    font_path: Path | None = None,
    font_family: str = DEFAULT_FONT_FAMILY,
    text_stroke: float = 0.0,
) -> list[Path]:
    """
    截取 HTML 文件中所有 .slide 元素为 JPEG 图片。

    滚动到每个 slide 后截取整个视口，输出固定尺寸的图片。

    Args:
        html_file: 本地 HTML 文件路径
        width: 视口宽度
        height: 视口高度
        scale: 浏览器缩放比例 (CSS zoom)，类似 Ctrl+/- 效果
        quality: JPEG 质量 (1-100)
        font_path: 自定义字体文件路径，默认使用华文楷体
        font_family: 字体族名称
        text_stroke: 文字描边宽度（px），用于增加字重效果

    Returns:
        生成的图片路径列表
    """
    # 设置默认字体路径
    if font_path is None:
        font_path = DEFAULT_FONT_PATH
    # 验证文件存在
    if not html_file.exists():
        raise FileNotFoundError(f"HTML 文件不存在: {html_file}")

    # 创建输出目录（与 HTML 文件同名）
    output_dir = html_file.parent / html_file.stem
    output_dir.mkdir(exist_ok=True)

    # 构建 file:// URL
    file_url = html_file.resolve().as_uri()

    output_files: list[Path] = []

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch()

        # 创建上下文，设置视口
        context = browser.new_context(
            viewport={"width": width, "height": height},
        )

        page = context.new_page()

        # 加载本地 HTML 文件
        page.goto(file_url)

        # 等待页面加载完成
        page.wait_for_load_state("networkidle")

        # 注入自定义字体（华文楷体）
        if font_path.exists():
            inject_font_css(page, font_path, font_family, text_stroke)
            # 等待字体加载
            page.wait_for_timeout(200)
            stroke_info = f"，字重+{text_stroke}px" if text_stroke > 0 else ""
            print(f"已加载字体: {font_family} ({font_path.name}){stroke_info}")
        else:
            print(f"警告: 字体文件不存在: {font_path}")

        # 应用浏览器缩放（CSS zoom，类似 Ctrl+/-）
        if scale != 1.0:
            page.evaluate(f"document.body.style.zoom = {scale}")
            # 等待缩放生效
            page.wait_for_timeout(100)

        # 查询所有 .slide 元素
        slides = page.query_selector_all(".slide")

        if not slides:
            print("警告: 未找到任何 .slide 元素")
            browser.close()
            return output_files

        print(f"找到 {len(slides)} 个幻灯片，开始截图...")
        print(f"视口尺寸: {width}x{height}px，缩放: {scale}x")

        for i, slide in enumerate(slides, 1):
            output_path = output_dir / f"slide_{i:02d}.jpg"

            # 滚动让 slide 内容居中显示在视口中
            slide.evaluate(
                "el => el.scrollIntoView({ block: 'center', inline: 'center' })"
            )

            # 等待滚动动画完成
            page.wait_for_timeout(150)

            # 截取整个视口（固定尺寸）
            page.screenshot(
                path=str(output_path),
                type="jpeg",
                quality=quality,
            )

            output_files.append(output_path)
            print(f"  [{i}/{len(slides)}] 已保存: {output_path.name}")

        browser.close()

    print(f"\n完成！共生成 {len(output_files)} 张图片")
    print(f"输出目录: {output_dir}")

    return output_files


def main() -> None:
    """命令行入口。"""
    parser = argparse.ArgumentParser(
        description="将 HTML 幻灯片截图为 JPEG 图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s page.html                        # 默认 1500x2000，使用华文楷体
  %(prog)s page.html --size 1080x1080       # 自定义尺寸
  %(prog)s page.html --scale 1.5            # 页面内容放大 1.5 倍
  %(prog)s page.html --scale 0.8            # 页面内容缩小到 80%%
  %(prog)s page.html --font path/to/font.ttf  # 使用自定义字体
  %(prog)s page.html --stroke 0.5           # 字重 +0.5px
  %(prog)s page.html --stroke 1             # 字重 +1px
  %(prog)s page.html --preview              # 预览模式，打开浏览器窗口
  %(prog)s page.html --preview --stroke 0.5 --scale 1.2  # 预览组合效果
        """,
    )
    parser.add_argument(
        "html_file",
        type=Path,
        help="本地 HTML 文件路径",
    )
    parser.add_argument(
        "--size",
        type=parse_size,
        default=(1500, 2000),
        metavar="WIDTHxHEIGHT",
        help="视口尺寸，格式 widthxheight，默认 1500x2000",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="浏览器缩放比例 (CSS zoom)，类似 Ctrl+/-，默认 1.0",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=90,
        choices=range(1, 101),
        metavar="1-100",
        help="JPEG 质量，默认 90",
    )
    parser.add_argument(
        "--font",
        type=Path,
        default=None,
        metavar="FONT_PATH",
        help=f"自定义字体文件路径，默认使用华文楷体 ({DEFAULT_FONT_PATH.name})",
    )
    parser.add_argument(
        "--stroke",
        type=float,
        default=0.0,
        metavar="PX",
        help="文字描边宽度（px），用于增加字重效果，如 0.5、1.0",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="预览模式，打开浏览器窗口查看效果（不截图）",
    )

    args = parser.parse_args()
    width, height = args.size

    try:
        if args.preview:
            # 预览模式
            preview_page(
                html_file=args.html_file,
                width=width,
                height=height,
                scale=args.scale,
                font_path=args.font,
                text_stroke=args.stroke,
            )
        else:
            # 截图模式
            screenshot_slides(
                html_file=args.html_file,
                width=width,
                height=height,
                scale=args.scale,
                quality=args.quality,
                font_path=args.font,
                text_stroke=args.stroke,
            )
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"截图失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
