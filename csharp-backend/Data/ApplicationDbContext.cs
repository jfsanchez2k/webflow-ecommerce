using AgilpayBackend.Models;
using Microsoft.EntityFrameworkCore;

namespace AgilpayBackend.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<User> Users { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Configure User entity
            modelBuilder.Entity<User>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.Username).IsUnique();
                entity.HasIndex(e => e.Email).IsUnique();
                entity.Property(e => e.Username).HasMaxLength(80).IsRequired();
                entity.Property(e => e.Email).HasMaxLength(120).IsRequired();
            });

            base.OnModelCreating(modelBuilder);
        }
    }
}
