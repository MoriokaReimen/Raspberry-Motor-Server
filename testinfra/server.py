from flask import Flask, render_template
import testinfra
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    print("Test Executed!!")
    contents = "Test Result:</br>"

    return render_template('layout.html', title = 'Test', datetime =datetime.now() ,test_all = test_all)

def test_all():
    result = {}
    host = testinfra.host.get_host("local://", sudo=True)

    # test password file for root access rights
    passwd = host.file("/etc/passwd")
    result["Password Root"]  =   "OK" if passwd.contains("root") else "NG"
    result["Password User"]  =   "OK" if passwd.user == "root"   else "NG"
    result["Password Group"] =  "OK" if passwd.group == "root"  else "NG"
    result["Password Mode"]  =   "OK" if passwd.mode == 0o644    else "NG"

    # test local host resolvable
    localhost = host.addr("localhost")
    result["localhost Resovable"]  =   "OK" if localhost.is_resolvable else "NG"

    # test wan dns
    wan_dns = host.addr("8.8.8.8")
    result["WAN DNS Reachable"]  =   "OK" if wan_dns.is_reachable else "NG"

    # test sshd
    sshd = host.service("sshd")
    result["sshd running"]  =   "OK" if sshd.is_running else "NG"
    ssh_port = host.socket("tcp://0.0.0.0:22")
    result["ssh port"]  =   "OK" if ssh_port.is_listening else "NG"

    # test ufw
    ufw = host.service("ufw")
    result["ufw running"]  =   "OK" if ufw.is_running else "NG"

    # test docker
    nginx = host.docker("nginx")
    result["docker nginx"]  =   "OK" if nginx.is_running else "NG"

    gitea = host.docker("gitea")
    result["docker gitea"]  =   "OK" if gitea.is_running else "NG"

    giteadb = host.docker("giteadb")
    result["docker giteadb"]  =   "OK" if giteadb.is_running else "NG"

    # test gitea
    gitea_http = host.run("curl -Is http://192.168.11.20/gitea/ | head -1")
    print(gitea_http.stdout)
    result["gitea working"]  =   "OK" if 'HTTP/1.1 200 OK' in gitea_http.stdout else "NG"

    return result


if __name__ == '__main__':
    app.config['TESTING'] = False
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=30000)
