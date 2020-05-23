# ScrapingSPRestMethods
Retrieve REST endpoints in SharePoint Online.

First, get the root site. Gets each endpoint from the href element in the return value. And then, by reoccurring this process, you get a list of Rest endpoints.

The Office365-REST-Python-Client 2.1.5 module is used to authenticate and create REST requests.
https://pypi.org/project/Office365-REST-Python-Client/2.1.5/

You can get these result by using this script


Web/Lists

Web/RootFolder

Web/ThemeInfo

, etc.
