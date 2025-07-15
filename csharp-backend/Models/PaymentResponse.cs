namespace AgilpayBackend.Models.Responses
{
    public class PaymentResponse
    {
        public bool Success { get; set; }
        public string PaymentUrl { get; set; } = string.Empty;
        public Dictionary<string, string> PaymentData { get; set; } = new();
        public string OrderId { get; set; } = string.Empty;
        public string? Error { get; set; }
    }

    public class ApiResponse<T>
    {
        public bool Success { get; set; }
        public T? Data { get; set; }
        public string? Error { get; set; }
        public string? Message { get; set; }
    }
}
