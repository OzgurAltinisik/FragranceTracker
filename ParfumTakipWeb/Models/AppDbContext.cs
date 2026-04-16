using Microsoft.EntityFrameworkCore;


namespace ParfumTakipWeb.Models
{
    // DbContext'ten miras alarak bunun bir veritabanı köprüsü olduğunu belirtiyoruz
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }

        // Veritabanındaki tablolarımızın C# karşılıkları
        public DbSet<FiyatGecmisi> FiyatGecmisi { get; set; }
        public DbSet<FiyatTakibi> FiyatTakibi { get; set; }
    }
}