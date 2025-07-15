using AgilpayBackend.Models;
using AgilpayBackend.Models.Requests;
using AgilpayBackend.Models.Responses;
using AgilpayBackend.Services;
using Microsoft.AspNetCore.Mvc;

namespace AgilpayBackend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AgilpayController : ControllerBase
    {
        private readonly IAgilpayService _agilpayService;
        private readonly ILogger<AgilpayController> _logger;

        public AgilpayController(IAgilpayService agilpayService, ILogger<AgilpayController> logger)
        {
            _agilpayService = agilpayService;
            _logger = logger;
        }

        [HttpPost("create-payment")]
        public async Task<ActionResult<PaymentResponse>> CreatePayment([FromBody] PaymentRequest request)
        {
            try
            {
                var result = await _agilpayService.CreatePaymentAsync(request);
                
                if (result.Success)
                {
                    return Ok(result);
                }
                else
                {
                    return BadRequest(result);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error procesando solicitud de pago");
                return StatusCode(500, new PaymentResponse
                {
                    Success = false,
                    Error = "Error interno del servidor"
                });
            }
        }

        [HttpPost("payment-response")]
        public ActionResult<ApiResponse<object>> PaymentResponse([FromForm] IFormCollection form)
        {
            try
            {
                // Aquí se procesaría la respuesta de Agilpay
                // Por ahora, simplemente registramos los datos recibidos
                var formData = form.ToDictionary(kvp => kvp.Key, kvp => kvp.Value.ToString());
                _logger.LogInformation("Respuesta de Agilpay: {@FormData}", formData);

                // En una implementación real, aquí se validaría la respuesta
                // y se actualizaría el estado de la orden en la base de datos

                return Ok(new ApiResponse<object>
                {
                    Success = true,
                    Message = "Respuesta recibida"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error procesando respuesta de pago");
                return StatusCode(500, new ApiResponse<object>
                {
                    Success = false,
                    Error = "Error procesando respuesta"
                });
            }
        }

        [HttpGet("products")]
        public ActionResult<ApiResponse<IEnumerable<Product>>> GetProducts()
        {
            try
            {
                var products = new List<Product>
                {
                    new Product
                    {
                        Id = 1,
                        Name = "Producto Premium A",
                        Description = "Descripción detallada del producto premium A",
                        Price = 99.99m,
                        Image = "https://via.placeholder.com/300x200?text=Producto+A"
                    },
                    new Product
                    {
                        Id = 2,
                        Name = "Producto Estándar B",
                        Description = "Descripción detallada del producto estándar B",
                        Price = 59.99m,
                        Image = "https://via.placeholder.com/300x200?text=Producto+B"
                    },
                    new Product
                    {
                        Id = 3,
                        Name = "Producto Básico C",
                        Description = "Descripción detallada del producto básico C",
                        Price = 29.99m,
                        Image = "https://via.placeholder.com/300x200?text=Producto+C"
                    },
                    new Product
                    {
                        Id = 4,
                        Name = "Producto Deluxe D",
                        Description = "Descripción detallada del producto deluxe D",
                        Price = 149.99m,
                        Image = "https://via.placeholder.com/300x200?text=Producto+D"
                    },
                    new Product
                    {
                        Id = 5,
                        Name = "Producto Especial E",
                        Description = "Descripción detallada del producto especial E",
                        Price = 79.99m,
                        Image = "https://via.placeholder.com/300x200?text=Producto+E"
                    }
                };

                return Ok(new ApiResponse<IEnumerable<Product>>
                {
                    Success = true,
                    Data = products
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error obteniendo productos");
                return StatusCode(500, new ApiResponse<IEnumerable<Product>>
                {
                    Success = false,
                    Error = "Error interno del servidor"
                });
            }
        }
    }
}
