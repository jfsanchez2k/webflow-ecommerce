namespace AgilpayBackend.Models.Requests
{
    public class PaymentRequest
    {
        public string CustomerName { get; set; } = string.Empty;
        public string CustomerEmail { get; set; } = string.Empty;
        public string CustomerAddress { get; set; } = string.Empty;
        public List<PaymentItem> Items { get; set; } = new();
        public string? SuccessUrl { get; set; }
        public string? ReturnUrl { get; set; }
    }

    public class PaymentItem
    {
        public string Name { get; set; } = string.Empty;
        public decimal Price { get; set; }
        public int Quantity { get; set; }
    }
}
