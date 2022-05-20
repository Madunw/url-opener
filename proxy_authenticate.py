import string
import zipfile


def create_proxy_auth_extension(proxy_authenticate_dict , scheme='http' ,
        plugin_path=None):

    """Proxy authentication plugin

     args:
         proxy_host (str): your proxy address or domain name (str)
         proxy_port (int): proxy port number (int)
         proxy_username (str): username (string)
         proxy_password (str): password (string)
     kwargs:
         scheme (str): proxy mode default http
         plugin_path (str): the absolute path to the extension

     return str -> plugin_path
     """

    if plugin_path is None:
        plugin_path = 'vimm_chrome_proxyauth_plugin.zip'

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template("""
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                  },
                  bypassList: ["foobar.com"]
                }
              };
    
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
    
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """).substitute(host=proxy_authenticate_dict['proxy_host'] , port=proxy_authenticate_dict['proxy_port'] , username=proxy_authenticate_dict['proxy_username'] , password=proxy_authenticate_dict['proxy_password'] ,
        scheme=scheme , )
    with zipfile.ZipFile(plugin_path , 'w') as zip:
        zip.writestr("manifest.json" , manifest_json)
        zip.writestr("background.js" , background_js)

    return plugin_path