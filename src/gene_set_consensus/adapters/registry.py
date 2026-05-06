from gene_set_consensus.adapters.generic_gene_list import (
    GenericGeneListAdapter
)

from gene_set_consensus.adapters.gtr_panel import (
    GTRPanelAdapter
)

from gene_set_consensus.adapters.mitocarta import (
    MitoCartaAdapter
)

ADAPTER_REGISTRY = {
    "generic_gene_list": GenericGeneListAdapter,
    "gtr_panel": GTRPanelAdapter,
    "mitocarta": MitoCartaAdapter,
}

def get_adapter(adapter_name):

    if adapter_name not in ADAPTER_REGISTRY:
        raise ValueError(
            f"Unknown adapter: {adapter_name}"
        )

    return ADAPTER_REGISTRY[adapter_name]()
