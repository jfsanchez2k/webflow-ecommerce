using AgilpayBackend.Models.Requests;
using AgilpayBackend.Models.Responses;

namespace AgilpayBackend.Services
{
    public interface IAgilpayService
    {
        Task<string?> GetOAuthTokenAsync(string orderId, string customerId, decimal amount);
        Task<PaymentResponse> CreatePaymentAsync(PaymentRequest request);
    }
}
