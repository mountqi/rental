# app.extensions['bootstrap'] = {
#     'cdns': {
#         'local': local,
#         'static': static,
#         'bootstrap': bootstrap,
#         'jquery': jquery,
#         'html5shiv': html5shiv,
#         'respond.js': respondjs,
#     },
# }
#

from flask_bootstrap import ConditionalCDN, StaticCDN, WebCDN

BOOTSTRAP_VERSION = "3.0.3"
JQUERY_VERSION = "2.0.0"

def change_cdn(app):
    local = StaticCDN('bootstrap.static', rev=True)
    static = StaticCDN()
    def lwrap(cdn, primary=static):
        return ConditionalCDN('BOOTSTRAP_SERVE_LOCAL', primary, cdn)

    bootstrap = lwrap(
        WebCDN('//libs.baidu.com/bootstrap/%s/'
               % BOOTSTRAP_VERSION),
        local)

    jquery = lwrap(
        WebCDN('//libs.baidu.com/jquery/%s/'
               % JQUERY_VERSION),
        local)

    app.extensions['bootstrap']['cdns']['bootstrap'] = bootstrap
    app.extensions['bootstrap']['cdns']['jquery'] = jquery


