import requests
from scrapy.selector import Selector
import time
from VideoSpider.utils.MySqlPool import getConn


def crawl_ips():
    conn = getConn()
    cursor = conn.cursor()
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Hosts': 'hm.baidu.com',
        'Referer': 'http://www.xicidaili.com/nn',
        'Connection': 'keep-alive'
    }

    for i in range(1, 6):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        time.sleep(10)
        selector = Selector(text=re.text)
        tr = selector.css("#ip_list tr")
        for j in range(1, len(tr)):
            info = tr[j].css("td::text").extract()
            ip = info[0]
            port = info[1]
            if len(info) == 12:
                proxy_type = info[5]
            else:
                proxy_type = info[4]
            speed = tr[j].css(".bar::attr(title)").extract()[0].split("秒")[0]
            # print(info)
            # print(ip + port + proxy_type + speed)
            cursor.execute(
                "insert into proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', '{2}', '{3}')".format(
                   ip, port, speed, proxy_type
                )
            )
        conn.commit()


class GetIp(object):
    def __init__(self):
        self.conn = getConn()

    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """
            delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor = self.conn.cursor()
        cursor.execute(delete_sql)
        self.conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = 'http://www.baidu.com'
        proxy_url = 'http://{0}:{1}'.format(ip, port)
        try:
            proxy_dict = {
                        "http": proxy_url,
                    }
            response = requests.get(http_url, proxies=proxy_dict)
            print(response.status_code)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code in (200, 299):
                print(f"effective ip,code is {code}")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        random_sql = """
                  SELECT ip, port FROM proxy_ip
                  ORDER BY RAND()
                  LIMIT 1
                """
        cursor = self.conn.cursor()
        cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            # print('http' + '://' + ip + ':' + port)
            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return f"http://{ip}:{port}"
            else:
                return self.get_random_ip()


if __name__ == '__main__':
    crawl_ips()
    GetIp().get_random_ip()
    pass
