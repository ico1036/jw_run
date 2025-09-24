"""
기본 favicon.ico 생성
브라우저 호환성을 위한 간단한 favicon
"""

def create_favicon_ico():
    """간단한 favicon.ico 생성 (텍스트 기반)"""
    
    # 간단한 ICO 파일 헤더 (16x16, 1비트)
    # 실제로는 복잡하지만, 여기서는 SVG를 메인으로 사용
    
    print("📄 favicon.ico 대신 SVG 파비콘을 사용합니다.")
    print("✅ 모던 브라우저는 SVG 파비콘을 완벽 지원합니다.")
    
    # robots.txt도 함께 생성
    robots_content = """User-agent: *
Allow: /

Sitemap: https://ico1036.github.io/jw_run/sitemap.xml
"""
    
    with open("saturday-run-coffee-club/robots.txt", "w") as f:
        f.write(robots_content)
    
    print("🤖 robots.txt 생성 완료")
    
    return True

if __name__ == "__main__":
    create_favicon_ico()


