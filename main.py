from DrissionPage import ChromiumOptions, Chromium
import time


class GoogleCrawler:
    def __init__(self, chrome_path='/usr/bin/google-chrome'):
        """初始化浏览器配置"""
        co = ChromiumOptions()
        co = co.headless(True) # 开启无头模式，开发过程中可以设置为 False 以便调试
        co.set_argument('--no-sandbox')  # Linux/WSL 必加
        co.binary_location = chrome_path
        self.tab = Chromium(co).latest_tab

    def login(self, email, password):
        """登录 Google 账号"""
        self.tab.get('https://accounts.google.com')
        self.tab.wait.doc_loaded()

        if 'accounts.google.com' in self.tab.url:
            # 输入邮箱
            email_input = self.tab.ele('#identifierId')
            email_input.input(email)

            # 点击“下一步”
            next_btn = self.tab.ele('@class=VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b')
            next_btn.click()
            self.tab.wait.doc_loaded()

            # 输入密码
            pwd_input = self.tab.ele('#password')
            pwd_input.input(password)

            # 点击“下一步”
            login_btn = self.tab.ele('@class=VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b')
            login_btn.click()

            # 等待跳转
            time.sleep(10)

            if 'accounts.google.com' in self.tab.url:
                print("登录失败")
                return False
            else:
                print("登录成功")
                return True
        else:
            print("当前已登录")
            return True

    def get_user_info_list(self, label):
        """
        获取某个 Google Scholar label 下的所有学者信息
        :param label: 领域标签，例如 'ai_drug_discovery'
        :return: list[dict] 学者信息
        """
        base_url = f'https://scholar.google.com/citations?view_op=search_authors&hl=zh-CN&mauthors=label:{label}'
        self.tab.get(base_url)

        scholars = []
        while True:
            # 找到当前页所有学者卡片
            cards = self.tab.eles('.gsc_1usr')  # 每个学者的信息卡
            for card in cards:
                # print(card.text)
                name_ele = card.ele('tag:h3@class=gs_ai_name').ele('tag:a')
                name = name_ele.text
                # print(name)
                profile_url = name_ele.attr('href')

                # affiliation = card.ele('.gs_ai_aff').text
                # interests = [i.text for i in card.eles('.gs_ai_int a')]
                # cited_by = card.ele('.gs_ai_cby').text

                scholars.append({
                    'name': name,
                    'user_id': profile_url.split('user=')[-1],
                    # 'profile_url': profile_url,
                    # 'affiliation': affiliation,
                    # 'interests': interests,
                    # 'cited_by': cited_by
                })
                # print(scholars[-1]['name'])
            # 查找“下一页”按钮
            next_btn = self.tab.ele('.gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx')
            if next_btn.attr('onclick') is not None:
                next_btn.click()
                time.sleep(1)
            else:
                break

        return scholars

if __name__ == '__main__':
    gl = GoogleCrawler()
    gl.login('d4997086@gmail.com', 'dt12345678')
    print(gl.get_user_info_list('ai_drug_discovery'))

