# Troubleshooting

- Missing API key errors: ensure the relevant environment variable is set.
- Ollama client errors about httpx: the `cltk[ollama]` extra pins a compatible httpx; upgrade with `pip install -U "cltk[ollama]"`.
- To suppress banner output in examples, pass `suppress_banner=True` when creating `NLP`.

# Logging

- To improve logging, optionally enable:
  - Whether the logger writes to a file cltk.log in the current working directory: `CLTK_LOG_TO_FILE=1|true|yes|on`. Default: `off`.
  - Whether sensitive content is emitted to logs at all (prompts, raw responses, extracted TSV rows, etc.): `CLTK_LOG_CONTENT=1|true|yes|on`. Default: `off`.
  - Log level: `CLTK_LOG_LEVEL=DEBUG|INFO|WARNING|ERROR`

Programmatic logging configuration (in code):

- Console debug only (no file):

```python
from cltk.core.cltk_logger import setup_cltk_logger

setup_cltk_logger(level="DEBUG", log_to_console=True, log_to_file=False)
```

- Write logs to a file (no sensitive content):

```python
from cltk.core.cltk_logger import setup_cltk_logger

setup_cltk_logger(level="INFO", log_to_console=True, log_to_file=True)
```

- Enable sensitive content logs (prompts/responses) at runtime:

```python
import os
from cltk.core.cltk_logger import setup_cltk_logger

os.environ["CLTK_LOG_CONTENT"] = "1"  # allow content logs
setup_cltk_logger(level="DEBUG", log_to_console=True, log_to_file=False)
```

- Persist sensitive content to disk (explicit opt‑in):

```python
import os
from cltk.core.cltk_logger import setup_cltk_logger

os.environ["CLTK_LOG_CONTENT"] = "1"
setup_cltk_logger(level="DEBUG", log_to_console=True, log_to_file=True)
# Note: certain rare error details (e.g., feature parse failures) are also
# written to features_err.log only when BOTH content logging and file logging are enabled.
```

- Revert to quiet defaults later in the same process:

```python
from cltk.core.cltk_logger import setup_cltk_logger

setup_cltk_logger(level="INFO", log_to_console=True, log_to_file=False)
```
