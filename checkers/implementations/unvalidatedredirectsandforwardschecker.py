from checkers.basechecker import BaseChecker
from HTMLParser import HTMLParser


class UnvalidatedRedirectsChecker(BaseChecker):
    FORBIDDEN_RESOURCES = [
        'admin.aspx', 'admin.asp', 'admin.php', 'admin', 'administrator',
        'moderator', 'webadmin', 'adminarea',
        'bb-admin', 'adminLogin', 'admin_area',
        'panel-administracion', 'instadmin',
        'memberadmin', 'administratorlogin',
        'adm', 'adminaccount.php', 'adminindex.php',
        'adminlogin.php', 'adminadmin.php',
        'adminaccount.php', 'joomlaadministrator',
        'login.php', 'admin_areaadmin.php',
        'admin_arealogin.php', 'siteadminlogin.php',
        'siteadminindex.php', 'siteadminlogin.html',
        'adminaccount.html', 'adminindex.html',
        'adminlogin.html', 'adminadmin.html',
        'admin_areaindex.php', 'bb-adminindex.php',
        'bb-adminlogin.php', 'bb-adminadmin.php',
        'adminhome.php', 'admin_arealogin.html',
        'admin_areaindex.html', 'admincontrolpanel.php',
        'admincpindex.asp', 'admincplogin.asp',
        'admincpindex.html', 'adminaccount.html',
        'adminpanel.html', 'webadmin.html', 'webadminindex.html',
        'webadminadmin.html', 'webadminlogin.html',
        'adminadmin_login.html', 'admin_login.html',
        'panel-administracionlogin.html',
        'admincp.php', 'cp.php', 'administratorindex.php',
        'administratorlogin.php', 'nswadminlogin.php',
        'webadminlogin.php', 'adminadmin_login.php',
        'admin_login.php', 'administratoraccount.php',
        'administrator.php', 'admin_areaadmin.html',
        'pagesadminadmin-login.php', 'adminadmin-login.php',
        'admin-login.php', 'bb-adminindex.html',
        'bb-adminlogin.html', 'bb-adminadmin.html',
        'adminhome.html', 'modelsearchlogin.php', 'moderator.php',
        'moderatorlogin.php', 'moderatoradmin.php',
        'account.php', 'pagesadminadmin-login.html',
        'adminadmin-login.html', 'admin-login.html',
        'controlpanel.php', 'admincontrol.php',
        'adminadminLogin.html', 'adminLogin.html',
        'adminadminLogin.html', 'home.html',
        'rcjakaradminlogin.php', 'adminareaindex.html',
        'adminareaadmin.html', 'webadmin.php', 'webadminindex.php',
        'webadminadmin.php', 'admincontrolpanel.html',
        'admin.html', 'admincp.html', 'cp.html',
        'adminpanel.php', 'moderator.html',
        'administratorindex.html', 'administratorlogin.html',
        'user.html', 'administratoraccount.html',
        'administrator.html', 'login.html', 'modelsearchlogin.html',
        'moderatorlogin.html', 'adminarealogin.html',
        'panel-administracionindex.html',
        'panel-administracionadmin.html', 'modelsearchindex.html',
        'modelsearchadmin.html', 'admincontrollogin.html', 'admindex.html',
        'adm.html', 'moderatoradmin.html', 'user.php', 'account.html',
        'controlpanel.html','admincontrol.html', 'panel-administracionlogin.php',
        'wp-login.php', 'adminLogin.php', 'adminadminLogin.php',
        'home.php', 'adminareaindex.php', 'adminareaadmin.php',
        'adminarealogin.php', 'panel-administracionindex.php',
        'panel-administracionadmin.php',
        'modelsearchindex.php', 'modelsearchadmin.php',
        'admincontrollogin.php', 'admadmloginuser.php',
        'admloginuser.php', 'admin2.php', 'admin2login.php',
        'admin2index.php', 'admindex.php', 'adm.php', 'affiliate.php',
        'adm_auth.php  ', 'memberadmin.php', 'administratorlogin.php',
        'loginadmin.asp', 'adminlogin.asp', 'administratorlogin.asp',
        'loginasmindstrator.asp', 'adminlogin.aspx', 'loginadmin.aspx',
        'administartorlogin.aspx', 'loginadministrator.aspx',
        'adminlogin.asp', 'adminlogin.aspx', 'admin_login.asp',
        'admin_login.aspx', 'adminhome.asp', 'adminhome.aspx'
        'administrator_login.asp', 'administrator_login.aspx'
    ]

    def get_attack_name(self):
        return 'unvalidated_redirects_and_forwards'

    def is_enabled(self):
        return True

    def check_request(self, request, context):
        h = HTMLParser()
        unescaped_trimmed_request = h.unescape(request.replace(' ', '').replace('\\n', '').lower())

        for item in UnvalidatedRedirectsChecker.FORBIDDEN_RESOURCES:
            if item in unescaped_trimmed_request:
                return None
        return request

    def check_response(self, response, context):
        return response
