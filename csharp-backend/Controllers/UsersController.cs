using AgilpayBackend.Data;
using AgilpayBackend.Models;
using AgilpayBackend.Models.Responses;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace AgilpayBackend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class UsersController : ControllerBase
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<UsersController> _logger;

        public UsersController(ApplicationDbContext context, ILogger<UsersController> logger)
        {
            _context = context;
            _logger = logger;
        }

        [HttpGet]
        public async Task<ActionResult<ApiResponse<IEnumerable<User>>>> GetUsers()
        {
            try
            {
                var users = await _context.Users.ToListAsync();
                return Ok(new ApiResponse<IEnumerable<User>>
                {
                    Success = true,
                    Data = users
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error obteniendo usuarios");
                return StatusCode(500, new ApiResponse<IEnumerable<User>>
                {
                    Success = false,
                    Error = "Error interno del servidor"
                });
            }
        }

        [HttpPost]
        public async Task<ActionResult<ApiResponse<User>>> CreateUser(User user)
        {
            try
            {
                if (!ModelState.IsValid)
                {
                    return BadRequest(new ApiResponse<User>
                    {
                        Success = false,
                        Error = "Datos inválidos"
                    });
                }

                _context.Users.Add(user);
                await _context.SaveChangesAsync();

                return CreatedAtAction(nameof(GetUser), new { id = user.Id }, 
                    new ApiResponse<User>
                    {
                        Success = true,
                        Data = user
                    });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creando usuario");
                return StatusCode(500, new ApiResponse<User>
                {
                    Success = false,
                    Error = "Error interno del servidor"
                });
            }
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<ApiResponse<User>>> GetUser(int id)
        {
            try
            {
                var user = await _context.Users.FindAsync(id);

                if (user == null)
                {
                    return NotFound(new ApiResponse<User>
                    {
                        Success = false,
                        Error = "Usuario no encontrado"
                    });
                }

                return Ok(new ApiResponse<User>
                {
                    Success = true,
                    Data = user
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error obteniendo usuario {UserId}", id);
                return StatusCode(500, new ApiResponse<User>
                {
                    Success = false,
                    Error = "Error interno del servidor"
                });
            }
        }

        [HttpPut("{id}")]
        public async Task<ActionResult<ApiResponse<User>>> UpdateUser(int id, User user)
        {
            try
            {
                if (id != user.Id)
                {
                    return BadRequest(new ApiResponse<User>
                    {
                        Success = false,
                        Error = "ID no coincide"
                    });
                }

                var existingUser = await _context.Users.FindAsync(id);
                if (existingUser == null)
                {
                    return NotFound(new ApiResponse<User>
                    {
                        Success = false,
                        Error = "Usuario no encontrado"
                    });
                }

                existingUser.Username = user.Username;
                existingUser.Email = user.Email;

                await _context.SaveChangesAsync();

                return Ok(new ApiResponse<User>
                {
                    Success = true,
                    Data = existingUser
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error actualizando usuario {UserId}", id);
                return StatusCode(500, new ApiResponse<User>
                {
                    Success = false,
                    Error = "Error interno del servidor"
                });
            }
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult<ApiResponse<object>>> DeleteUser(int id)
        {
            try
            {
                var user = await _context.Users.FindAsync(id);
                if (user == null)
                {
                    return NotFound(new ApiResponse<object>
                    {
                        Success = false,
                        Error = "Usuario no encontrado"
                    });
                }

                _context.Users.Remove(user);
                await _context.SaveChangesAsync();

                return Ok(new ApiResponse<object>
                {
                    Success = true,
                    Message = "Usuario eliminado correctamente"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error eliminando usuario {UserId}", id);
                return StatusCode(500, new ApiResponse<object>
                {
                    Success = false,
                    Error = "Error interno del servidor"
                });
            }
        }
    }
}
