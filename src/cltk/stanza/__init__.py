"""Optional Stanza-backed processes for CLTK.

This subpackage is available when installing the stanza extra:

    pip install "cltk[stanza]"

It exposes: StanzaAnalyzeProcess
"""

from .processes import StanzaAnalyzeProcess  # re-export for convenience

__all__ = ["StanzaAnalyzeProcess"]
