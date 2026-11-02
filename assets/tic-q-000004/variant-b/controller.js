export async function invoiceHandler(req, res) {
  const invoice = await invoices.findById(req.params.invoiceId);
  res.json(invoice);
}
