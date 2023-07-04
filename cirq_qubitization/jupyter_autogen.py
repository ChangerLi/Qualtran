"""Autogeneration of stub Jupyter notebooks.

For each module listed in the `NOTEBOOK_SPECS` global variable (in this file)
we write a notebook with a title, module docstring,
standard imports, and information on each `GateWithRegisters` listed in the
`gate_specs` field. For each gate, we render a docstring and diagrams.

## Adding a new gate.

 1. Create a new function in `jupyter_autogen_factories.py` that takes no arguments
    and returns an instance of the desired gate.
 2. If this is a new module: add a new key/value pair to the NOTEBOOK_SPECS global variable
    in this file. The key should be the name of the module with a `NotebookSpec` value. See
    the docstring for `NotebookSpec` for more information.
 3. Update the `NotebookSpec` `gate_specs` field to include a `GateNbSpec` for your new gate.
    Provide your factory function from step (1).

## Autogen behavior.

Each autogenerated notebook cell is tagged, so we know it was autogenerated. Each time
this script is re-run, these cells will be re-rendered. *Modifications to generated _cells_
will not be persisted*.

If you add additional cells to the notebook it will *preserve them* even when this script is
re-run

Usage as a script:
    cd cirq_qubitization/ && python jupyter_autogen.py
"""

import inspect
import re
from pathlib import Path
from types import ModuleType
from typing import Callable, Dict, List, Optional, Tuple, Type, Union

import nbformat
from attrs import frozen, mutable
from cirq_ft import GateWithRegisters
from sphinx.ext.napoleon import Config, GoogleDocstring

import cirq_qubitization.bloq_algos.and_bloq_test
import cirq_qubitization.bloq_algos.arithmetic_test
import cirq_qubitization.bloq_algos.basic_gates.cnot_test
import cirq_qubitization.bloq_algos.basic_gates.rotation_test
import cirq_qubitization.bloq_algos.basic_gates.swap_test
import cirq_qubitization.bloq_algos.basic_gates.x_basis_test
import cirq_qubitization.bloq_algos.factoring.mod_exp
import cirq_qubitization.bloq_algos.factoring.mod_exp_test
import cirq_qubitization.bloq_algos.factoring.mod_mul_test
import cirq_qubitization.bloq_algos.sorting_test
import cirq_qubitization.bloq_algos.swap_network
import cirq_qubitization.bloq_algos.swap_network_test
import cirq_qubitization.quantum_graph
from cirq_qubitization.quantum_graph.bloq import Bloq


@frozen
class GateNbSpec:
    """Notebook specification for a particular Gate.

    Attributes:
        factory: A factory function that produces the gate. Its source code will be rendered
            to the notebook. See the `jupyter_autogen_factories` module.
        draw_vertical: Whether to render `vertical=True` in the rendered call to
            `display_gate_and_compilation`
    """

    factory: Callable[[], GateWithRegisters]
    draw_vertical: bool = False

    @property
    def cqid(self):
        """A cirq_qubitization-unique id for this `GateNbSpec` to tag generated cells."""
        return self.factory.__name__

    @property
    def gate_cls(self):
        gate_obj = self.factory()
        return gate_obj.__class__


@frozen
class BloqNbSpec:
    """Notebook specification for a particular Bloq.

    Attributes:
        factory: A factory function that produces the bloq. Its source code will be rendered
            to the notebook. See the `jupyter_autogen_factories_2` module.
    """

    factory: Callable[[], Bloq]

    @property
    def cqid(self):
        """A cirq_qubitization-unique id for this `BloqNbSpec` to tag generated cells."""
        return self.factory.__name__

    @property
    def gate_cls(self):
        gate_obj = self.factory()
        return gate_obj.__class__


@frozen(kw_only=True)
class NotebookSpec:
    """Specification for rendering a jupyter notebook for a given module.

    Attributes:
        title: The title of the notebook
        module: The module it documents. This is used to render the module docstring
            at the top of the notebook.
        gate_specs: A list of gate or bloq specs.
    """

    title: str
    module: ModuleType
    gate_specs: List[Union[GateNbSpec, BloqNbSpec]]
    directory: str = '.'
    _path_stem: Optional[str] = None

    @property
    def path_stem(self):
        if self._path_stem is None:
            return self.module.__name__.split('.')[-1]
        return self._path_stem


NOTEBOOK_SPECS: List[NotebookSpec] = [
    NotebookSpec(
        title='Swap Network',
        module=cirq_qubitization.bloq_algos.swap_network,
        gate_specs=[
            BloqNbSpec(cirq_qubitization.bloq_algos.basic_gates.swap_test._make_CSwap),
            BloqNbSpec(cirq_qubitization.bloq_algos.swap_network_test._make_CSwapApprox),
            BloqNbSpec(cirq_qubitization.bloq_algos.swap_network_test._make_SwapWithZero),
        ],
        directory='./bloq_algos',
    ),
    NotebookSpec(
        title='Basic Gates',
        module=cirq_qubitization.bloq_algos.basic_gates,
        gate_specs=[
            BloqNbSpec(cirq_qubitization.bloq_algos.basic_gates.cnot_test._make_CNOT),
            BloqNbSpec(cirq_qubitization.bloq_algos.basic_gates.x_basis_test._make_plus_state),
            BloqNbSpec(cirq_qubitization.bloq_algos.basic_gates.rotation_test._make_Rz),
        ],
        directory='./bloq_algos',
    ),
    NotebookSpec(
        title='And',
        module=cirq_qubitization.bloq_algos.and_bloq,
        gate_specs=[
            BloqNbSpec(cirq_qubitization.bloq_algos.and_bloq_test._make_and),
            BloqNbSpec(cirq_qubitization.bloq_algos.and_bloq_test._make_multi_and),
        ],
        directory='./bloq_algos',
    ),
    NotebookSpec(
        title='Arithmetic',
        module=cirq_qubitization.bloq_algos.arithmetic,
        gate_specs=[
            BloqNbSpec(cirq_qubitization.bloq_algos.arithmetic_test._make_add),
            BloqNbSpec(cirq_qubitization.bloq_algos.arithmetic_test._make_product),
            BloqNbSpec(cirq_qubitization.bloq_algos.arithmetic_test._make_square),
            BloqNbSpec(cirq_qubitization.bloq_algos.arithmetic_test._make_sum_of_squares),
            BloqNbSpec(cirq_qubitization.bloq_algos.arithmetic_test._make_greater_than),
        ],
        directory='./bloq_algos',
    ),
    NotebookSpec(
        title='Sorting',
        module=cirq_qubitization.bloq_algos.sorting,
        gate_specs=[
            BloqNbSpec(cirq_qubitization.bloq_algos.sorting_test._make_comparator),
            BloqNbSpec(cirq_qubitization.bloq_algos.sorting_test._make_bitonic_sort),
        ],
        directory='./bloq_algos',
    ),
    NotebookSpec(
        title='Modular arithmetic',
        module=cirq_qubitization.bloq_algos.factoring,
        path_stem='ref-factoring',
        gate_specs=[
            BloqNbSpec(cirq_qubitization.bloq_algos.factoring.mod_exp_test._make_modexp),
            BloqNbSpec(cirq_qubitization.bloq_algos.factoring.mod_mul_test._make_modmul),
        ],
        directory='./bloq_algos/factoring',
    ),
]


class _GoogleDocstringToMarkdown(GoogleDocstring):
    """Subclass of sphinx's parser to emit Markdown from Google-style docstrings."""

    def _parse_parameters_section(self, section: str) -> List[str]:
        """Sphinx method to emit a 'Parameters' section."""

        def _template(name, desc_lines):
            desc = ' '.join(desc_lines)
            return f' - `{name}`: {desc}'

        return [
            '#### Parameters',
            *[_template(name, desc) for name, _type, desc in self._consume_fields()],
            '',
        ]

    def _parse_references_section(self, section: str) -> List[str]:
        """Sphinx method to emit a 'References' section."""
        return [
            '#### References',
            ' '.join(line.strip() for line in self._consume_to_next_section()),
            '',
        ]


def get_markdown_docstring_lines(cls: Type) -> List[str]:
    """From a class `cls`, return its docstring as Markdown."""

    # 1. Sphinx incantation
    config = Config()
    docstring = cls.__doc__ if cls.__doc__ else ""
    gds = _GoogleDocstringToMarkdown(inspect.cleandoc(docstring), config=config, what='class')

    # 2. Pre-pend a header.
    lines = [f'## `{cls.__name__}`'] + gds.lines()

    # 3. Substitute restructured text inline-code blocks to markdown-style backticks.
    lines = [re.sub(r':py:func:`(\w+)`', r'`\1`', line) for line in lines]

    return lines


def _get_lines_for_constructing_an_object(func: Callable):
    """Parse out the source code from a factory function, so we can render it into a cell.

    Args:
        func: The factory function. Its definition must be one line; its body must be
            indented with four spaces; and it must end with a top-level return statement that
            is one line.

    Returns:
        trimmed_lines: The un-indented body of the function without the return statement.
        obj_expression: The expression used in the terminal `return` statement.
    """
    def_line, *pre, ret_line = inspect.getsource(func).splitlines()
    assert def_line.startswith('def '), def_line

    trimmed_lines = []
    for line in pre:
        assert line == '' or line.startswith(' ' * 4), line
        trimmed_lines.append(line[4:])
    assert ret_line.startswith('    return '), ret_line
    obj_expression = ret_line[len('    return ') :]
    return trimmed_lines, obj_expression


_IMPORTS = """\
import cirq
import numpy as np
import cirq_qubitization
import cirq_ft
import cirq_ft.infra.testing as cq_testing
from cirq_qubitization.jupyter_tools import display_gate_and_compilation, show_bloq
from typing import *\
"""

_GATE_DISPLAY = """\
{lines}
g = cq_testing.GateHelper(
    {obj_expression}
)

display_gate_and_compilation(g{vert_str})\
"""

_BLOQ_DISPLAY = """\
{lines}
bloq = {obj_expression}
show_bloq(bloq)\
"""


def _get_code_for_demoing_a_gate(gate_func: Callable, vertical: bool) -> str:
    """Render the Python code for constructing and visualizing a Gate.

    This renders into the `_GATE_DISPLAY` template.
    """
    lines, obj_expression = _get_lines_for_constructing_an_object(gate_func)

    vert_str = ''
    if vertical:
        vert_str = ', vertical=True'

    return _GATE_DISPLAY.format(
        lines='\n'.join(lines), obj_expression=obj_expression, vert_str=vert_str
    )


def _get_code_for_demoing_a_bloq(bloq_func: Callable) -> str:
    """Render the Python code for constructing and visualizing a Bloq.

    This renders into the `_BLOQ_DISPLAY` template.
    """
    lines, obj_expression = _get_lines_for_constructing_an_object(bloq_func)

    return _BLOQ_DISPLAY.format(lines='\n'.join(lines), obj_expression=obj_expression)


def _get_code_for_demoing(spec: Union[GateNbSpec, BloqNbSpec]) -> str:
    if isinstance(spec, GateNbSpec):
        return _get_code_for_demoing_a_gate(gate_func=spec.factory, vertical=spec.draw_vertical)
    if isinstance(spec, BloqNbSpec):
        return _get_code_for_demoing_a_bloq(bloq_func=spec.factory)


def _get_title_cell_with_module_docstring(title: str, mod: ModuleType) -> str:
    """Return markdown text for the title cell.

    This consists of the specified title as well as the associated module's docstring.
    """
    lines = [f'# {title}', '']

    if mod.__doc__ is None:
        return lines[0]

    lines += inspect.cleandoc(mod.__doc__).splitlines()
    return '\n'.join(lines)


_K_CQ_AUTOGEN = 'cq.autogen'
"""The jupyter metadata key we use to identify cells we've autogenerated."""


def _md_cell(source: str, cqid: str) -> nbformat.NotebookNode:
    """Helper function to return a markdown cell with correct metadata"""
    return nbformat.v4.new_markdown_cell(source, metadata={_K_CQ_AUTOGEN: cqid})


def _code_cell(source: str, cqid: str) -> nbformat.NotebookNode:
    """Helper function to return a code cell with correct metadata"""
    return nbformat.v4.new_code_cell(source, metadata={_K_CQ_AUTOGEN: cqid})


@frozen(kw_only=True)
class _GateCells:
    """Rendered cells for a gate."""

    md: nbformat.NotebookNode
    py: nbformat.NotebookNode


@mutable
class NbCells:
    """Rendered notebook cells.

    Attributes:
        title_cell: The title cell
        top_imports: The cell for doing imports at the top of the notebook
        gate_cells: A mapping from "cqid" to the `_GateCells` pair of cells for each
            gate.
    """

    title_cell: nbformat.NotebookNode
    top_imports: nbformat.NotebookNode
    gate_cells: Dict[str, _GateCells]

    def get_all_cqids(self) -> List[str]:
        """Get all the cqid's for generated cells.

        These are ordered in the way the cells should appear in a rendered notebook.
        It is a flat list that includes both notebook-level cells and all the cqids
        for the `GateCells` in `self.gate_cells`.
        """
        cqids = ['title_cell', 'top_imports']
        for gate_cqid in self.gate_cells.keys():
            cqids.append(f'{gate_cqid}.md')
            cqids.append(f'{gate_cqid}.py')
        return cqids

    def get_cell_from_cqid(self, cqid: str) -> nbformat.NotebookNode:
        """Look up the cell from its cqid metadata string.

        For `_GateCells` this will look up the constituent `md` or `py` cell.
        """
        if '.' in cqid:
            gate_cqid, ext = cqid.split('.')
            return getattr(self.gate_cells[gate_cqid], ext)

        return getattr(self, cqid)


def render_notebook_cells(nbspec: NotebookSpec) -> NbCells:
    """Generate cells for a given notebook."""

    return NbCells(
        title_cell=_md_cell(
            _get_title_cell_with_module_docstring(title=nbspec.title, mod=nbspec.module),
            cqid='title_cell',
        ),
        top_imports=_code_cell(_IMPORTS, cqid='top_imports'),
        gate_cells={
            gspec.cqid: _GateCells(
                md=_md_cell(
                    '\n'.join(get_markdown_docstring_lines(cls=gspec.gate_cls)),
                    cqid=f'{gspec.cqid}.md',
                ),
                py=_code_cell(_get_code_for_demoing(gspec), cqid=f'{gspec.cqid}.py'),
            )
            for gspec in nbspec.gate_specs
        },
    )


def _init_notebook(
    path_stem: str, overwrite=False, directory: str = '.'
) -> Tuple[nbformat.NotebookNode, Path]:
    """Initialize a jupyter notebook.

    If one already exists: load it in. Otherwise, create a new one.

    Args:
        path_stem: The extensionless filename to find the notebook if it exists.
        overwrite: If set, remove any existing notebook and start from scratch.
        directory: The directory in which we look for the filename.
    """

    nb_path = Path(f'{directory}') / f'{path_stem}.ipynb'

    if overwrite:
        nb_path.unlink(missing_ok=True)

    if nb_path.exists():
        with nb_path.open('r') as f:
            return nbformat.read(f, as_version=4), nb_path

    nb = nbformat.v4.new_notebook()
    nb['metadata'].update(
        {
            'kernelspec': {'language': 'python', 'name': 'python3', 'display_name': 'Python 3'},
            'language_info': {'name': 'python'},
        }
    )
    return nb, nb_path


def render_notebooks():
    for nbspec in NOTEBOOK_SPECS:
        # 1. get a notebook (existing or empty)
        nb, nb_path = _init_notebook(path_stem=nbspec.path_stem, directory=nbspec.directory)

        # 2. Render all the cells we can render
        cells = render_notebook_cells(nbspec)

        # 3. Merge rendered cells into the existing notebook.
        #     -> we use the cells metadata field to match up cells.
        cqids_to_render: List[str] = cells.get_all_cqids()
        for i in range(len(nb.cells)):
            cell = nb.cells[i]
            if _K_CQ_AUTOGEN in cell.metadata:
                cqid: str = cell.metadata[_K_CQ_AUTOGEN]
                print(f"[{nbspec.path_stem}] Replacing {cqid} cell.")
                new_cell = cells.get_cell_from_cqid(cqid)
                new_cell.id = cell.id  # keep id from existing cell
                nb.cells[i] = new_cell
                cqids_to_render.remove(cqid)

        # 4. Any rendered cells that weren't already there, append.
        for cqid in cqids_to_render:
            print(f"[{nbspec.path_stem}] Adding {cqid}")
            new_cell = cells.get_cell_from_cqid(cqid)
            nb.cells.append(new_cell)

        # 5. Write the notebook.
        with nb_path.open('w') as f:
            nbformat.write(nb, f)


if __name__ == '__main__':
    render_notebooks()
