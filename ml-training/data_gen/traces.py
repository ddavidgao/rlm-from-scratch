"""
Aggregator module - imports all trace definitions and combines into ALL_TRACES.
"""

from .traces_clean_find import CLEAN_FIND_TRACES
from .traces_retry import KEYWORD_RETRY_TRACES, DEAD_END_TRACES
from .traces_errors import (
    REDEFINE_CONTEXT_TRACES,
    NO_CODE_TRACES,
    RUNTIME_ERROR_TRACES,
    NO_CONTEXT_REF_TRACES,
)
from .traces_advanced import (
    FALSE_POSITIVE_TRACES,
    MULTI_SEARCH_TRACES,
    LLM_QUERY_TRACES,
    LLM_FAILURE_TRACES,
    LARGE_DOC_TRACES,
    MIXED_TRACES,
)

ALL_TRACES = (
    CLEAN_FIND_TRACES
    + KEYWORD_RETRY_TRACES
    + DEAD_END_TRACES
    + REDEFINE_CONTEXT_TRACES
    + NO_CODE_TRACES
    + RUNTIME_ERROR_TRACES
    + NO_CONTEXT_REF_TRACES
    + FALSE_POSITIVE_TRACES
    + MULTI_SEARCH_TRACES
    + LLM_QUERY_TRACES
    + LLM_FAILURE_TRACES
    + LARGE_DOC_TRACES
    + MIXED_TRACES
)

print(f"Loaded {len(ALL_TRACES)} total traces")
