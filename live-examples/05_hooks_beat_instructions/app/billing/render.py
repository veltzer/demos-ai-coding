"""Plain-text invoice rendering."""


def render(invoice):
    out = [f"{line.description:<30}{line.total:>10}" for line in invoice.lines]
    out.append(f"{'subtotal':<30}{invoice.subtotal:>10}")
    out.append(f"{'VAT 17%':<30}{invoice.vat:>10}")
    out.append(f"{'TOTAL':<30}{invoice.total:>10}")
    return "\n".join(out)
