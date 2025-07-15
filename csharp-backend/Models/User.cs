using System.ComponentModel.DataAnnotations;

namespace AgilpayBackend.Models
{
    public class User
    {
        public int Id { get; set; }
        
        [Required]
        [StringLength(80)]
        public string Username { get; set; } = string.Empty;
        
        [Required]
        [StringLength(120)]
        [EmailAddress]
        public string Email { get; set; } = string.Empty;
        
        public override string ToString()
        {
            return $"User {Username}";
        }
    }
}
