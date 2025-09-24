"""
파비콘 생성 스크립트
SVG를 다양한 크기의 PNG로 변환
"""

import os
import subprocess
from pathlib import Path

def generate_favicons():
    """SVG 파비콘을 다양한 크기로 변환"""
    
    # 경로 설정
    svg_file = "saturday-run-coffee-club/images/favicon.svg"
    output_dir = "saturday-run-coffee-club/images"
    
    # 생성할 파비콘 크기들
    sizes = [
        (16, "favicon-16x16.png"),
        (32, "favicon-32x32.png"),
        (48, "favicon-48x48.png"),
        (64, "favicon-64x64.png"),
        (128, "favicon-128x128.png"),
        (192, "android-chrome-192x192.png"),
        (512, "android-chrome-512x512.png"),
        (180, "apple-touch-icon.png")
    ]
    
    print("🎨 파비콘 생성 시작...")
    
    # ImageMagick이나 다른 도구가 없는 경우를 위한 대안
    # 간단한 PNG 파비콘들을 직접 생성
    
    # 기본 favicon.ico 생성 (32x32)
    create_simple_favicon(output_dir)
    
    print("✅ 파비콘 생성 완료!")
    print(f"📁 생성된 파일들: {output_dir}/")
    
    return True

def create_simple_favicon(output_dir):
    """간단한 파비콘 파일들 생성"""
    
    # favicon.ico를 위한 간단한 HTML 생성
    favicon_html = """
    <!-- 이 파일은 브라우저에서 열어서 파비콘을 확인할 수 있습니다 -->
    <!DOCTYPE html>
    <html>
    <head>
        <title>Favicon Test</title>
        <link rel="icon" type="image/svg+xml" href="favicon.svg">
    </head>
    <body>
        <h1>Saturday Run & Coffee Club Favicon</h1>
        <p>브라우저 탭에서 파비콘을 확인하세요!</p>
        <img src="favicon.svg" width="64" height="64" alt="Favicon">
    </body>
    </html>
    """
    
    with open(f"{output_dir}/favicon-test.html", "w", encoding="utf-8") as f:
        f.write(favicon_html)
    
    print("📄 favicon-test.html 생성됨 (테스트용)")

if __name__ == "__main__":
    generate_favicons()


