using AgilpayBackend.Models.Requests;
using AgilpayBackend.Models.Responses;
using Newtonsoft.Json;
using System.Text;

namespace AgilpayBackend.Services
{
    public class AgilpayService : IAgilpayService
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<AgilpayService> _logger;

        // Configuración de Agilpay (credenciales de prueba)
        private readonly AgilpayConfig _config = new()
        {
            ClientId = "API-001",
            ClientSecret = "Dynapay",
            MerchantKey = "TEST-001",
            TokenUrl = "https://sandbox-webapi.agilpay.net/oauth/paymenttoken",
            PaymentUrl = "https://sandbox-webpay.agilpay.net/Payment"
        };

        public AgilpayService(HttpClient httpClient, ILogger<AgilpayService> logger)
        {
            _httpClient = httpClient;
            _logger = logger;
        }

        public async Task<string?> GetOAuthTokenAsync(string orderId, string customerId, decimal amount)
        {
            try
            {
                var payload = new
                {
                    grant_type = "client_credentials",
                    client_id = _config.ClientId,
                    client_secret = _config.ClientSecret,
                    orderId = orderId,
                    customerId = customerId,
                    amount = amount
                };

                var json = JsonConvert.SerializeObject(payload);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync(_config.TokenUrl, content);

                if (response.IsSuccessStatusCode)
                {
                    var responseJson = await response.Content.ReadAsStringAsync();
                    var tokenResponse = JsonConvert.DeserializeObject<dynamic>(responseJson);
                    return tokenResponse?.access_token;
                }
                else
                {
                    _logger.LogError("Error obteniendo token: {StatusCode} - {Content}", 
                        response.StatusCode, await response.Content.ReadAsStringAsync());
                    return null;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Excepción obteniendo token");
                return null;
            }
        }

        public async Task<PaymentResponse> CreatePaymentAsync(PaymentRequest request)
        {
            try
            {
                // Validar datos requeridos
                if (string.IsNullOrWhiteSpace(request.CustomerName) ||
                    string.IsNullOrWhiteSpace(request.CustomerEmail) ||
                    string.IsNullOrWhiteSpace(request.CustomerAddress) ||
                    !request.Items.Any())
                {
                    return new PaymentResponse
                    {
                        Success = false,
                        Error = "Campos requeridos faltantes"
                    };
                }

                // Generar ID único para la orden
                var orderId = Guid.NewGuid().ToString();

                // Calcular el total
                decimal totalAmount = 0;
                var items = new List<object>();

                foreach (var item in request.Items)
                {
                    var itemTotal = item.Price * item.Quantity;
                    totalAmount += itemTotal;
                    items.Add(new
                    {
                        Description = item.Name,
                        Quantity = item.Quantity.ToString(),
                        Amount = itemTotal,
                        Tax = 0
                    });
                }

                // Obtener token JWT
                var token = await GetOAuthTokenAsync(orderId, request.CustomerEmail, totalAmount);
                if (token == null)
                {
                    return new PaymentResponse
                    {
                        Success = false,
                        Error = "No se pudo obtener el token de autenticación"
                    };
                }

                // Preparar detalles del pago
                var paymentDetails = new
                {
                    MerchantKey = _config.MerchantKey,
                    Service = orderId,
                    MerchantName = "Webflow Store",
                    Description = $"Orden {orderId}",
                    Amount = totalAmount,
                    Tax = 0,
                    Currency = "840", // USD
                    Items = items
                };

                // Preparar datos para el formulario de Agilpay
                var agilpayData = new Dictionary<string, string>
                {
                    { "SiteId", _config.ClientId },
                    { "UserId", request.CustomerEmail },
                    { "Names", request.CustomerName },
                    { "Email", request.CustomerEmail },
                    { "Address", request.CustomerAddress },
                    { "Detail", JsonConvert.SerializeObject(new { Payments = new[] { paymentDetails } }) },
                    { "SuccessURL", request.SuccessUrl ?? "https://example.com/success" },
                    { "ReturnURL", request.ReturnUrl ?? "https://example.com/return" },
                    { "token", token },
                    { "NoHeader", "2" } // Modo iframe
                };

                return new PaymentResponse
                {
                    Success = true,
                    PaymentUrl = _config.PaymentUrl,
                    PaymentData = agilpayData,
                    OrderId = orderId
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creando pago");
                return new PaymentResponse
                {
                    Success = false,
                    Error = $"Error interno del servidor: {ex.Message}"
                };
            }
        }

        private class AgilpayConfig
        {
            public string ClientId { get; set; } = string.Empty;
            public string ClientSecret { get; set; } = string.Empty;
            public string MerchantKey { get; set; } = string.Empty;
            public string TokenUrl { get; set; } = string.Empty;
            public string PaymentUrl { get; set; } = string.Empty;
        }
    }
}
