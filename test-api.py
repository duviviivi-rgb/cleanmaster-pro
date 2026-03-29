import urllib.request
import json

# 测试API接口
def test_api(url):
    print(f"测试接口: {url}")
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("测试成功!")
    except Exception as e:
        print(f"测试失败: {e}")
    print("-" * 50)

# 测试各个API接口
test_api('http://localhost:5001/api/test')
test_api('http://localhost:5001/api/disk')
test_api('http://localhost:5001/api/settings')
test_api('http://localhost:5001/api/scan/quick')
test_api('http://localhost:5001/api/scan/deep')
test_api('http://localhost:5001/api/scan/analysis')
test_api('http://localhost:5001/api/space/usage')
test_api('http://localhost:5001/api/history')