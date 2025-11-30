import os
import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from typing import Optional, List
from pathlib import Path
from app.tool.base import BaseTool, ToolResult
from app.logger import logger
import asyncio

class NotebookExecutionTool(BaseTool):
    name: str = "execute_notebook"
    description: str = (
        "Create and execute Jupyter Notebooks (.ipynb). "
        "Use this tool for data analysis, visualization, or complex calculations where preserving the state and steps is important. "
        "You can create a new notebook or append cells to an existing one. "
        "Returns the output of the executed cells."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name of the notebook file (e.g., 'analysis.ipynb').",
            },
            "cells": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "cell_type": {
                            "type": "string",
                            "enum": ["code", "markdown"],
                            "description": "Type of the cell.",
                        },
                        "source": {
                            "type": "string",
                            "description": "Content of the cell.",
                        },
                    },
                    "required": ["cell_type", "source"],
                },
                "description": "List of cells to add and execute.",
            },
            "kernel_name": {
                "type": "string",
                "description": "Kernel to use for execution. Defaults to 'python3'.",
                "default": "python3"
            }
        },
        "required": ["filename", "cells"],
    }

    async def execute(self, filename: str, cells: List[dict], kernel_name: str = "python3") -> ToolResult:
        try:
            workspace_root = Path(os.getcwd()) / "workspace"
            workspace_root.mkdir(parents=True, exist_ok=True)
            file_path = workspace_root / filename

            # Load existing notebook or create new one
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    nb = nbformat.read(f, as_version=4)
            else:
                nb = new_notebook()
                nb.metadata.kernelspec = {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": kernel_name
                }

            # Add new cells
            added_cells_indices = []
            start_index = len(nb.cells)
            
            for cell_data in cells:
                if cell_data['cell_type'] == 'code':
                    cell = new_code_cell(source=cell_data['source'])
                else:
                    cell = new_markdown_cell(source=cell_data['source'])
                nb.cells.append(cell)
                added_cells_indices.append(len(nb.cells) - 1)

            # Execute the notebook (only the new cells if possible, but nbclient executes the whole nb by default or we can configure it)
            # For simplicity and context preservation, we usually re-execute or execute from a certain point.
            # However, standard nbclient executes the whole notebook. 
            # To be efficient, we might want to only execute new cells if we had a persistent kernel, 
            # but here we are stateless between tool calls unless we keep a kernel running.
            # For this implementation, we will execute the entire notebook to ensure state consistency.
            
            client = NotebookClient(nb, timeout=600, kernel_name=kernel_name, resources={'metadata': {'path': str(workspace_root)}})
            
            # This executes the notebook in-place
            await asyncio.to_thread(client.execute)

            # Save the executed notebook
            with open(file_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)

            # Extract outputs from the newly added cells
            outputs = []
            for idx in added_cells_indices:
                cell = nb.cells[idx]
                if cell.cell_type == 'code':
                    cell_outputs = []
                    for output in cell.outputs:
                        if output.output_type == 'stream':
                            cell_outputs.append(output.text)
                        elif output.output_type == 'execute_result' or output.output_type == 'display_data':
                            data = output.data
                            if 'text/plain' in data:
                                cell_outputs.append(data['text/plain'])
                            # We could also handle image data here if we wanted to extract it
                        elif output.output_type == 'error':
                            cell_outputs.append(f"Error: {output.evalue}")
                    
                    outputs.append(f"Cell {idx+1} Output:\n" + "\n".join(cell_outputs))

            return ToolResult(output=f"Notebook '{filename}' executed successfully.\n\n" + "\n\n".join(outputs))

        except Exception as e:
            logger.error(f"Error executing notebook: {e}")
            return ToolResult(error=f"Failed to execute notebook: {str(e)}")
