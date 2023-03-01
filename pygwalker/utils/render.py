from ..base import *

def gwalker_script():
    global gwalker_js
    if gwalker_js is None:
        with open(os.path.join(HERE, 'templates', 'graphic-walker.iife.js'), 'r', encoding='utf8') as f:
            gwalker_js = f.read()
    return gwalker_js

from jinja2 import Environment, PackageLoader, select_autoescape
jinja_env = Environment(
    loader=PackageLoader("pygwalker"),
    autoescape=(()), # select_autoescape()
)

class DataFrameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def render_gwalker_html(gid: int, props: tp.Dict):
    walker_template = jinja_env.get_template("walk.js")
    js = walker_template.render(gwalker={'id': gid, 'props': json.dumps(props, cls=DataFrameEncoder)} )
    js = "var exports={};var process={env:{NODE_ENV:\"production\"} };" + gwalker_script() + js
    
    template = jinja_env.get_template("index.html")
    html = f"{template.render(gwalker={'id': gid, 'script': js})}"
    # print("html =", html)
    import html as m_html
    srcdoc = m_html.escape(html)
    sandbox = "allow-forms allow-pointer-lock allow-popups allow-same-origin allow-scripts allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation"
    style = "display: block; width: 100%; border: none;"
    iframe = \
f"""<div>
<iframe id="ifr-gw-{gid}" width="100%" height="900px" srcdoc="{srcdoc}" sandbox="{sandbox}" style="{style}"></iframe>

</div>
"""
    return iframe

def render_gwalker_js(gid: int, props: tp.Dict):
    pass
    # walker_template = jinja_env.get_template("walk.js")
    # js = walker_template.render(gwalker={'id': gid, 'props': json.dumps(props, cls=DataFrameEncoder)} )
    # js = gwalker_script() + js
    # return js
