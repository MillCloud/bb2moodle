#bb2moodle
import os
import string
import jinja2
import random
import datetime

def m_hash(*args):
    # TODO: Refactor?

    if len(args) > 1:
        the_hash = abs(hash(args))
    elif isinstance(args[0], dict):
        the_hash = abs(hash(tuple(args[0].values())))
    else:
        the_hash = abs(hash(args[0]))

    return int(str(the_hash))

def generate_stamp():
    chars = string.ascii_letters + string.digits

    host_part = 'unknownhost'
    date_part = datetime.datetime.now().strftime('%y%m%d%H%M%S')
    random_part = ''.join([random.choice(chars) for n in xrange(6)])

    return '+'.join([host_part, date_part, random_part])

def fix_filename(filename, res_num):
    '''In: internet.mp3, Out: internet_res_num.mp3'''

    filename = filename.replace(' ', '_')

    if not res_num:
        return filename

    if '.' not in filename:
        return filename

    ext, name = filename[::-1].split('.', 1)

    return (ext + '.' + res_num[::-1] + '_' + name)[::-1]

def fix_embed_filename(filename, linkname):
    '''In: /xid-508654_1 ceshi.mp4, Out: ceshi__xid-508654_1_csfiles.mp4'''

    filename = filename.replace('/', '_')
    linkname = linkname.replace(' ', '_')
    csfiles = 'csfiles'

    if not filename:
        return filename

    if 'xid' not in filename:
        return filename

    ext, name = linkname[::-1].split('.', 1)

    return (ext + '.' + csfiles[::-1] + '_' + filename[::-1] + '_' + name)[::-1]

def convert(course):
    tmpl_path = os.path.join(os.path.dirname(__file__), 'moodle.xml.template')

    template_content = open(tmpl_path).read()

    xml_template = jinja2.Template(template_content, autoescape=True)

    # jinja2's environment finalize wasn't working for some reason
    moodle_xml_str = xml_template.render(course=course).replace('>None<', '><')

    return moodle_xml_str
