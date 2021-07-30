from flask import Flask, render_template
import testinfra
from datetime import datetime
import humanfriendly
import io

app = Flask(__name__)


@app.route('/')
def index():
    print("Test Executed!!")
    contents = "Test Result:</br>"

    return render_template('layout.html', title = 'Test', datetime =datetime.now() ,test_all = test_all)

def test_all():
      result = {}
    try:
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

      # test glances
      glances_http = host.run("sudo curl -Is http://192.168.11.20:20000 | head -1")
      result["glances working"]  =   "OK" if 'HTTP/1.0 401 Unauthorized' in glances_http.stdout else "NG"

      # test docker
      docker = host.service("docker")
      result["docker running"]  =   "OK" if docker.is_running else "NG"

      nginx = host.docker("nginx")
      result["docker nginx"]  =   "OK" if nginx.is_running else "NG"

      gitea = host.docker("gitea")
      result["docker gitea"]  =   "OK" if gitea.is_running else "NG"

      giteadb = host.docker("giteadb")
      result["docker giteadb"]  =   "OK" if giteadb.is_running else "NG"

      jenkins = host.docker("jenkins")
      result["docker jenkins"]  =   "OK" if jenkins.is_running else "NG"

      docker_df = host.run("sudo docker system df --format='{{.Size}}'").stdout
      size = 0
      for line in io.StringIO(docker_df):
          size += humanfriendly.parse_size(line)
      print(size)
      result["docker size"]  =   "OK" if size < 8000000000 else "NG"

      # test gitea
      gitea_http = host.run("sudo curl -Is http://192.168.11.20/gitea/ | head -1")
      result["gitea working"]  =   "OK" if 'HTTP/1.1 200 OK' in gitea_http.stdout else "NG"

      # test jenkins
      jenkins_http = host.run("sudo curl -Is http://192.168.11.20/jenkins/login | head -1")
      result["jenkins working"]  =   "OK" if 'HTTP/1.1 200 OK' in jenkins_http.stdout else "NG"

      # test directory size
      gitea_file = host.file("/root/Server/Docker/Gitea/gitea-data/")
      result["gitea file size"]  =   "OK" if  gitea_file.size < 4000000000 else "NG"

      giteadb_file = host.file("/root/Server/Docker/GiteaDB/giteadb-data/")
      result["giteadb file size"]  =   "OK" if  giteadb_file.size < 2000000000 else "NG"

      jenkins_file = host.file("/root/Server/Docker/Jenkins/jenkins_home/")
      result["jenkins file size"]  =   "OK" if  jenkins_file.size < 4000000000 else "NG"
    except:
        err = sys.exc_info()[0]
        result["Unit test Pailed out!!"] =  err

    return result


if __name__ == '__main__':
    app.config['TESTING'] = False
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=30000)
