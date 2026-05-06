from gene_set_consensus.adapters.generic_gene_list import (
    GenericGeneListAdapter
)

from gene_set_consensus.adapters.gtr_panel import (
    GTRPanelAdapter
)

ADAPTER_REGISTRY = {
    "generic_gene_list": GenericGeneListAdapter,
    "gtr_panel": GTRPanelAdapter,
}

def get_adapter(adapter_name):

    if adapter_name not in ADAPTER_REGISTRY:
        raise ValueError(
            f"Unknown adapter: {adapter_name}"
        )

    return ADAPTER_REGISTRY[adapter_name]()
