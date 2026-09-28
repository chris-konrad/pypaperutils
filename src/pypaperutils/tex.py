import os
import datetime
from pathlib import Path

from pypaperutils.io import make_fileheader 

def writetex(lines, config, tex_name, metadata={}, verbose=True):
    """Write lines into a tex-file.

    Parameters
    ----------
    lines : list
        List of lines to write.
    config : dict
        Config-dictionary. Uses the fields 'file_metadata' ( if available) and 'dir_out'.
        'file_metadata' is printed as metadata in tex comments to the header of the file. 
        'dir_out' contains the directory to save the tex-file to. Must be given. 
    tex_name : str
        The filename of the tex-file to write. 
    metadata : dict, optional
        Extra metadata to add to the header of the file, by default {}
    verbose : bool, optional
        Activate verbose output, by default True
    """
    
    filename = filename.rstrip(".tex")+".tex"
    header = make_fileheader(filename, metadata=config['file_metadata'] | metadata)
    lines = header + lines

    filepath = os.path.join(config['dir_out'], filename)
    file_exists = os.path.isfile(filepath)

    with open(filepath, 'w') as f:
        for l in lines:
            f.write(l.rstrip("\n")+"\n")

    if verbose:
        if file_exists:
            print(f"Overwrote existing '{filepath}'.")
        else:
            print(f"Wrote '{filepath}'.")


def tex_bold(val):
    """Make val bold (mathmode.)
    """
    return rf"\textbf{{{val}}}"


def tex_list2tabrow(vals):
    """ Turn a list of vals into a row for tex tabular:
        e.g.: [val1, val2, val3] -> 'val1 & val2 & val3 \\'
    """
    vals = [str(v) for v in vals]
    return " & ".join(vals) + r"\\"


def tex_formatpercent(val, precision=2):
    """Format val as number in pecent."""
    val = val * 100
    return rf"{val:.{precision}f} \%"


def tex_formatsi(val, unit, precision=2):
    """Format val as number with SI unit."""
    return rf"\SI{{{val:.{precision}f}}}{{{unit}}}"


def tex_tabhrules():
    """Return the tex tabrule commands."""
    return r"\toprule", r"\midrule", r"\bottomrule"


def tex_tabmultcol(val, columns, alignment='c'):
    """Return the tex mutlicolumn command."""
    return rf"\multicolumn{{{columns}}}{{{alignment}}}{{{val}}}"

def tex_tabmultrow(val, rows, vdisplacement=""):
    """Return the tex multirow command.""
    """
    if vdisplacement == "":
        return rf"\multirow{{{rows}}}{{*}}{{{val}}}"
    else:
        return rf"\multirow{{{rows}}}{{*}}[{vdisplacement}]{{{val}}}"

def tex_maketabular(header, alignment, body):
    """Create a list of lines representing a tabular tex environment.
    
    Parameters
    ----------
    header : str
        The header of the tabular.
    alignment : str
        The alignment of the tabuler. E.g. 'cccc'
    body : list
        A list of str or lists representing the lines of the body of the tabular. If 
        the top-level list contains a nested list, tex_list2tabrow is applied to that list. 
    
    Returns
    -------
    lines : list
        List of str representing the tabulr. Pass this to writetex().
    """
    rules = tex_tabhrules()

    lines = [rf"\begin{{tabular}}{{{alignment}}}"]
    lines.append(rules[0])

    lines.append(header)
    lines.append(rules[1])

    for row in body:
        if isinstance(row, str):
            lines.append(row)
        elif isinstance(row, list):
            lines.append(tex_list2tabrow(row))
        else:
            raise ValueError(f"Tabular rows must be str or list.")

    lines.append(rules[2])
    lines.append(r"\end{tabular}")

    return lines

def tex_formatp(p, significance_level=0.05):
    """Format p-values. Prints the p value in bold if smaller than significance level. 
    Prints <0.001 if smaller than 0.001. Prints the p value directly otherwise."""
    if p < 0.001:
        return r"\textbf{< .001}"
    elif p < significance_level:
        return rf"\textbf{{{p:.3f}}}"
    else:
        return f"{p:.3f}"

def export_as_texcommand(key, value, config, unit=None, precision=None, verbose=True):
    """Export a value as as tex command to a .tex file. 
    
    The command will have the form `\key` and will print `value`, formatted
    according to the remaining kwargs. 

    The .tex file for export is specified in config. 
    [dir_out_base]/[subdir_doctype]/[filename_values]

    If the .tex specified in config does already contain the command, it is overwritten. 
    
    Parameters
    ----------
    key : str
        The name of the latex command. Must be no numbers, no spaces, no special characters.
    value : str, float, int
        The value to print. Other datatypes are casted to str.
    config : config
        A confg dictionary. Requires the fields:
            dir_out_base : str
                The ouput directory base
            subdir_out_doctype :  str
                The subdirectory for the chosen doctype (paper or presentation)
            filename_values : str
                The filename of the valuecommand file. 
    unit : str, optional
        A SI unit for the value. Must be a command for the LaTeX siunix package. If None, no unit is appended.
        By default None
    precision : int, optional
        The precicion for the value. Default is 0 for int and 2 for float.
    verbose : bool, optional
        Verbose output, by default True
    """

    if precision is None:
        if isinstance(value, int):
            precision = 0
        elif isinstance(value, float):
            precision = 2
        else:
            precision = None

    if precision is not None and isinstance(value, (int, float)):
        value_str = f"{value:.{precision}f}"
    else:
        value_str = str(value)

    command = rf"\newcommand{{\{key}}}"
    if unit is not None:
        definition = command + rf"{{\SI{{{value_str}}}{{{unit}}}}}"
    else:
        definition = command + rf"{{{value_str}}}"

    filepath = os.path.join(config["dir_out_base"], config['subdir_out_doctype'], config["filename_values"])
    _add_texcommand_line(filepath, command, definition, verbose=verbose)


def _add_texcommand_line(filepath, prefix, line, verbose=True):
    """Adds a line to a texcommand latexfile.
    
    Helper function for export_as_texcommand.
    """
    suffix = f"     % {Path(sys.argv[0]).name}, {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"

    if not os.path.isfile(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            header = make_fileheader(Path(filepath).name)
            for l in header:
                f.write(l.rstrip("\n")+"\n")
            lines = header
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

    line_exists = False
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            lines[i] = line.rstrip("\n") + suffix
            line_exists=True
            break
    else:
        lines.append(line.rstrip("\n") + suffix)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)

    if verbose:
        if line_exists:
            print(f"Overwrote existing '{prefix}' in '{filepath}'.")
        else:
            print(f"Appended '{prefix}' to '{filepath}'.")


