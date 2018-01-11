# EWS Cracker
      ____|  \ \        /    ___|        ___|                         |    
      __|     \ \  \   /   \___ \       |        __|    _` |    __|   |  / 
      |        \ \  \ /          |      |       |      (   |   (        <  
     _____|     \_/\_/     _____/      \____|  _|     \__,_|  \___|  _|\_\ 
                                                                       
## What's EWS?

EWS stands for Exchange Web Services.  This is a SOAP based protocol used for free/busy scheduling, and leveraged by third party clients.  It allows a user to read email, send email, test credentials.

Unfortunately, EWS only supports Basic Authentication.  If you have multi-factor authentication through a third party provider, such as Ping, Duo or Okta, EWS can be used to bypass MFA. It can also be used to bypass MDM solutions.

[This was documented by the fine folks at Black Hills InfoSec](https://www.blackhillsinfosec.com/bypassing-two-factor-authentication-on-owa-portals/) as well as [by Duo](https://duo.com/blog/on-vulnerabilities-disclosed-in-microsoft-exchange-web-services) over a year ago.  

Microsoft's official response is to use Microsoft provided MFA, which produce an application specific password. This leaves an enourmous amount of O365 customers in a difficult state.  Most customers seem unaware of this issue or choose to ignore it.

Other fun facts about EWS:

* Logging is not 100%. It may log failed attempts in your audit logs, it may not.
* It helpfully provides user enumeration.  If a user doesn't exist, a different error is returned.

## Single user test mode

`ews-crack.py --mode single --username jsmith --domain contoso.com --password mypassword`

## Colon delimited username:password tester

`ews-crack.py --mode creds --file user-passwords.txt --domain contoso.com`

## Spray a single password against a list of user accounts

` python ews-crack.py --mode spray --filename users.txt --domain contoso.com --password Winter2018!`
