from jinja2 import Environment, FileSystemLoader


class MessageTemplate(object):
    def __init__(self, config):
        self.templatepath = config.get('TEMPLATE_PATH')
        self.templatefile = config.get('TEMPLATE_FILE')

    def __call__(self, **tmplargs):
        tmplenv = Environment(loader=FileSystemLoader(self.templatepath))
        tmpl = tmplenv.get_template(self.templatefile)
        return tmpl.render(tmplargs)
