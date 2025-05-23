import requests
import pytest

BASE_URL = "http://localhost:81"
ADMIN_ACCOUNT = "admin"
ADMIN_PASSWORD = "1234"

# 全局存储token
AUTH_HEADERS = {"Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImp0aSI6MTgxODUzMzgwNDA5NzE5MTkzNywiZXhwIjoxNzQ3OTY1MjYyfQ.QhwBW_86QFWY9ae7OkqXePujOm6Qb1GtbhODcjgNosY"}

def setup_module():
    """初始化模块：管理员登录获取Token"""
    login_url = f"{BASE_URL}/auth/login"
    login_data = {
        "account": ADMIN_ACCOUNT,
        "password": ADMIN_PASSWORD
    }
    resp = requests.post(login_url, json=login_data)
    # 检查登录是否成功test_user
    if resp.status_code != 200:
        raise Exception("管理员登录失败")
    assert resp.status_code == 200
    token = resp.json()['data']['token']  # 根据实际返回结构调整
    print("获取管理员Token:", type(token))
    AUTH_HEADERS['Authorization'] = f"Bearer {token}"

    print("管理员登录成功，获取Token:", token)


# === 用户注册测试 ===
def test_user_registration():
    """测试正常注册流程"""
    # 正常注册用例
    valid_data = {
        "account": "new_user_2024",
        "password": "111",
        "name": "测试用户"
    }
    resp = requests.post(
        f"{BASE_URL}/auth/register",
        json=valid_data
    )
    # 断言响应结构
    assert resp.status_code == 200
    result = resp.json()
    assert result['status'] == 200
    assert result['data'] is True
    
    # 验证用户实际存在（需要管理员权限）
    check_resp = requests.get(
        f"{BASE_URL}/user/detail?account={valid_data['account']}",
        headers=AUTH_HEADERS
    )

    # 断言查询结果
    assert check_resp.status_code == 200

    print("用户注册，查询结果：", check_resp.json())
    assert check_resp.json()['data']['account'] == valid_data['account']

# === 用户管理测试 ===
def test_user_crud():
    # 创建用户
    user_data = {
        "account": "test_user",
        "password": "Test@1234",
        "name": "测试用户",
        "roleIds": [1]  # 根据实际角色ID调整
    }
    create_resp = requests.post(
        f"{BASE_URL}/user/save",
        json=user_data,
        headers=AUTH_HEADERS
    )

    print("新增用户，响应结果：", create_resp.json())
    assert create_resp.status_code == 200
    print(create_resp.json()['data'])
    user_id = create_resp.json()['data']['id']

    # 查询详情
    # detail_resp = requests.get(
    #     f"{BASE_URL}/user/detail?id={user_id}",
    #     headers=AUTH_HEADERS
    # )
    # assert detail_resp.json()['data']['name'] == "测试用户"

    # # 更新用户
    # update_data = {
    #     "id": user_id,
    #     "name": "更新用户",
    #     "roleIds": [1,2]
    # }
    # update_resp = requests.post(
    #     f"{BASE_URL}/user/update",
    #     json=update_data,
    #     headers=AUTH_HEADERS
    # )
    # assert update_resp.status_code == 200

    # # 删除用户
    delete_resp = requests.post(
        f"{BASE_URL}/user/remove?id={user_id}",
        headers=AUTH_HEADERS
    )
    assert delete_resp.status_code == 200



# === 设备管理测试 ===
def test_device_crud():
    # 新增设备
    device_data = {
        "deviceName": "Python编程",
        "isbn": "9787111128066",
        "category": "计算机科学"
    }
    create_resp = requests.post(
        f"{BASE_URL}/device/save",
        json=device_data,
        headers=AUTH_HEADERS
    )
    assert create_resp.status_code == 200
    device_id = create_resp.json()['data']['id']

    # 分页查询
    page_query = {
        "current": 1,
        "size": 10,
        "queryType": 0
    }
    page_resp = requests.post(
        f"{BASE_URL}/device/page",
        json=page_query,
        headers=AUTH_HEADERS
    )
    assert len(page_resp.json()['data']['records']) > 0

    # 更新设备状态
    update_data = {
        "id": device_id,
        "borrowed": True
    }
    update_resp = requests.post(
        f"{BASE_URL}/device/update",
        json=update_data,
        headers=AUTH_HEADERS
    )
    assert update_resp.status_code == 200

    # 删除设备
    delete_resp = requests.post(
        f"{BASE_URL}/device/remove?id={device_id}",
        headers=AUTH_HEADERS
    )
    assert delete_resp.status_code == 200

# === 权限验证测试 ===
def test_permission_check():
    # 使用普通用户token尝试访问管理接口
    user_headers = {}
    user_login = requests.post(
        f"{BASE_URL}/auth/login",
        json={"account": "user1", "password": "User@1234"}
    )
    user_headers['Authorization'] = f"Bearer {user_login.json()['data']['token']}"
    
    resp = requests.get(
        f"{BASE_URL}/user/detail?id=1",
        headers=user_headers
    )
    assert resp.status_code == 403  # 应返回权限不足


# === 运行测试 ===
if __name__ == "__main__":
    # setup_module()
    
    # 按顺序执行重要测试
    # test_user_registration()
    # test_invalid_registration()
    # test_duplicate_registration()
    
    # 原有测试...
    test_user_crud()
    # test_device_crud()
    
    # teardown_module()  # 新增清理