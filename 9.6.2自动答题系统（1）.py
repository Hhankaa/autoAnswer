#encoding:utf-8

from selenium import webdriver
import json, time
url = 'https://zhidao.baidu.com/list?fr=daohang'
path = r'D:\Google\Chrome\Application\chromedriver.exe'
driver = webdriver.Chrome(executable_path=path)
driver.get(url)
def login_zhidao(driver):
    driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__footerULoginBtn"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__userName"]').send_keys('17568937997')
    driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__password"]').send_keys('1996519..')

    try:
        verifyCode = driver.find_element_by_class_name('verifyCode')
        code_number = input('请输入图片验证码')
        verifyCode.send_keys(str(code_number))
    except:
        pass

    driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__submit"]').click()
    time.sleep(2)

driver.delete_all_cookies()
f1 = open('cookie.txt')
cookie =json.loads(f1.read())
f1.close()
for c in cookie:
    if 'expiry' in c:
        del c['expiry']
    driver.add_cookie(c)
driver.refresh()
# 获取问题列表
title_link = driver.find_elements_by_class_name('title-link')
for i in title_link:
    # 打开问题详细页并切换窗口
    driver.switch_to.window(driver.window_handles[0])
    href = i.get_attribute('href')
    driver.execute_script('window.open("%s");' % (href))#把href里面的打开
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    try:
        # 查找iframe，判断问题是否已被回答
        driver.find_element_by_id('ueditor_0')
        # 获取问题题目并搜索答案
        title = driver.find_element_by_class_name('ask-title ').text
        title_url = 'https://zhidao.baidu.com/search?&word=' + title
        js = 'window.open("%s");' % (title_url)
        driver.execute_script(js)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[2])
        # 获取答案列表
        answer_list = driver.find_elements_by_class_name('dt,mb-3,line')
        #以列表的形式保存题目
        '''
        <selenium.webdriver.remote.webelement.WebElement 
        (session="1c55ce91f51fb493f7d9c48b3137dcbc", element="01bce34c-b86e-4efe-8a0b-6c6366dc9a79")>
        '''
        for k in answer_list:
            # 打开答案详细页
            href = k.find_element_by_tag_name('a').get_attribute('href')
            driver.execute_script('window.open("%s");' % (href))
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[3])
            # 获取最佳答案
            try:
                text = driver.find_element_by_class_name('best-text,mb-10').text
            except:
                text = ''
            finally:
                # 关闭答案详情页的窗口
                driver.close()
            # 答案不为空
            if text:
                # 关闭答案列表页的窗口
                driver.switch_to.window(driver.window_handles[2])
                driver.close()
                # 将答案写在问题回答文本框上并点击提交答案按钮
                driver.switch_to.window(driver.window_handles[1])
                driver.switch_to.frame('ueditor_0')
                driver.find_element_by_xpath('/html/body').click()
                driver.find_element_by_xpath('/html/body').send_keys(text)
                # 跳回到网页的HTML
                driver.switch_to.default_content()
                # 点击提交回答按钮
                driver.find_element_by_xpath('//*[@id="answer-editor"]/div[2]/a').click()
                time.sleep(2)
                # 关闭问题详细页的窗口
                login = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__form"]/p[1]')
                if login:
                    login_zhidao(driver)
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                break

    except Exception as err:
        # 除了问题列表页，关闭其他窗口
        all_handles = driver.window_handles
        for i, v in enumerate(all_handles):
            if i != 0:
                driver.switch_to.window(v)
                driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(err)