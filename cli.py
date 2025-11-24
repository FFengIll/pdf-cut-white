import sys
import os
from pathlib import Path
import typer

from pdf_white_cut.logger import add_file_log, logger
from pdf_white_cut.worker import batch_cut_pdf, cut_pdf

app = typer.Typer(help="PDF white borders cutting tool")


def setup_logging(verbose: bool):
    """Setup logging based on verbose flag."""
    if verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
        add_file_log()


def is_directory(path: str) -> bool:
    """Check if path is a directory."""
    return os.path.isdir(path)


def is_file(path: str) -> bool:
    """Check if path is a file."""
    return os.path.isfile(path)


@app.command()
def main(
    input: str = typer.Option(
        ..., "-i", "--input", help="Input file or directory"
    ),
    output: str = typer.Option(
        "output.pdf", "-o", "--output", help="Output file or directory"
    ),
    ignore: int = typer.Option(
        0, "--ignore", help="Ignore global pixels"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", help="Enable verbose logging (DEBUG)"
    ),
):
    """Cut white borders from PDF files.

    Automatically detects if input is a file or directory:
    - File: processes single PDF to output file
    - Directory: processes all PDFs to output directory
    """
    setup_logging(verbose)

    try:
        # Determine input type
        if is_file(input):
            # Single file mode
            if not input.lower().endswith('.pdf'):
                typer.echo(f"Error: Input file must be a PDF: {input}", err=True)
                raise typer.Exit(1)

            # If output is a directory, create filename based on input
            if is_directory(output):
                input_filename = Path(input).stem
                output_file = os.path.join(output, f"{input_filename}_cut.pdf")
            else:
                output_file = output

            cut_pdf(input, output_file, ignore)
            typer.echo(f"✓ Cut white borders from {input} to {output_file}")

        elif is_directory(input):
            # Batch directory mode
            # If output is a file, treat it as directory
            if is_file(output):
                typer.echo(f"Error: Output must be a directory when input is a directory", err=True)
                raise typer.Exit(1)

            # Create output directory if it doesn't exist
            os.makedirs(output, exist_ok=True)

            batch_cut_pdf(input, output, ignore)
            typer.echo(f"✓ Processed PDF files from {input} to {output}")

        else:
            typer.echo(f"Error: Input path does not exist: {input}", err=True)
            raise typer.Exit(1)

    except Exception as e:
        logger.exception(e)
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
