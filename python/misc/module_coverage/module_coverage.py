import os
import argparse
from docstr_coverage import get_docstring_coverage


def progress_bar(percent, bar_length=60):
    return '`[{}{}]`'.format(
        '#'*int(round((percent * bar_length / 100.0), 0)),
        '-'*int(round(((100 - percent) * bar_length / 100.0), 0)))


def progress_stats(missing, total):
    return '`{}/{} ({}%)`'.format(
            total - missing,
            total,
            round((total - missing) * 100 / max(total, 1), 1))


def find_module(module):
    from inspect import getfile
    from os.path import dirname
    from importlib import import_module

    return dirname(
        getfile(
            import_module(module)
        )
    )


def get_modinfo(modules, docname):
    modinfo = {}
    modinfo['files'] = {m: [] for m in modules}
    modinfo['dirs'] = {m: find_module(m) for m in modules}

    modinfo['doc'] = {
        m: '{}-{}.md'.format(docname, m)
        for m in modules}
    modinfo['topdoc'] = '{}.md'.format(docname)

    for mod in modules:
        for root, dirs, files in os.walk(modinfo['dirs'][mod]):
            for file in (f for f in files if f.endswith(".py")):
                modinfo['files'][mod].append(
                    os.path.join(root, file))

    modinfo['coverage'] = {
        m: get_docstring_coverage(
            filenames=modinfo['files'][m],
            skip_magic=True) for m in modules
        }

    return modinfo


def build_top_doc(modinfo):
    msg_lines = []
    msg_lines.append('# Docstring coverage')
    for mod in sorted(modinfo['coverage']):
        msg_lines.append('* [{}]({})'.format(mod, modinfo['doc'][mod]))

    doc_content = '  \n'.join(msg_lines)
    return doc_content


def build_mod_doc(modinfo, module):
    if len(modinfo['coverage'][module]) < 2:
        raise RuntimeError('Malformed coverage data from docstr-coverage')

    stats = modinfo['coverage'][module][1]
    msg_lines = []
    msg_lines.append('# Docstring coverage for {} module'.format(module))
    msg_lines.append('Docstrings in module: {}'.format(
        progress_stats(stats['missing_count'], stats['needed_count'])))

    progress = progress_bar(stats['coverage'])
    msg_lines.append(progress)

    # Add report for each file
    for file_path in sorted(modinfo['coverage'][module][0]):
        file_stats = modinfo['coverage'][module][0][file_path]

        rel_path = os.path.relpath(file_path, modinfo['dirs'][module])
        msg_lines.append('## {}'.format(rel_path))

        msg_lines.append('Docstrings in file: {}'.format(
            progress_stats(
                file_stats['missing_count'],
                file_stats['needed_count'])))

        progress = progress_bar(file_stats['coverage'])
        msg_lines.append(progress)

        if file_stats['missing']:
            msg_lines.append('### Missing docstrings:')
            for m in file_stats['missing']:
                msg_lines.append('* `{}`'.format(m))

    doc_content = '  \n'.join(msg_lines)
    return doc_content


def main(modules, outdir=None, basename=None):
    outdir = outdir or '.'

    modinfo = get_modinfo(modules, basename)

    # === Build documents ===
    doc_content = build_top_doc(modinfo)
    doc_path = os.path.join(outdir, modinfo['topdoc'])
    with open(doc_path, 'w') as f:
        f.write(doc_content)

    for mod in modinfo['coverage']:
        doc_content = build_mod_doc(modinfo, mod)
        doc_path = os.path.join(outdir, modinfo['doc'][mod])
        with open(doc_path, 'w') as f:
            f.write(doc_content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--outdir', action='store',
        help='Directory for generated output docs')
    parser.add_argument(
        '-b', '--basename', action='store',
        default='coverage',
        help='Base name to be used for file names in generated documents')
    parser.add_argument(
        'modules', action='store', nargs='+',
        help='List of modules to generate docs for')
    args = parser.parse_args()

    main(modules=args.modules, outdir=args.outdir, basename=args.basename)
