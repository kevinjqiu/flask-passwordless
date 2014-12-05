from jinja2 import Environment, FileSystemLoader


class MessageTemplate(object):
    def __init__(self, config):
        config = config['TEMPLATES']
        self.templatepath = config['TEMPLATE_PATH']
        self.templatefile = config['TEMPLATE_FILE']

    def __call__(self, tmplargs):
        # basedir = os.path.dirname(__file__)
        # tmpllib_path = os.path.abspath(os.path.join(basedir, self.templatepath))
        tmplenv = Environment(loader=FileSystemLoader(self.templatepath))
        tmpl = tmplenv.get_template(self.templatefile)
        return tmpl.render(tmplargs)
