using Microsoft.AspNetCore.Mvc;
using ParfumTakipWeb.Models;
using System.Linq;

namespace ParfumTakipWeb.Controllers
{
    public class FragrancesController : Controller
    {
        private readonly AppDbContext _context;

        public FragrancesController(AppDbContext context)
        {
            _context = context;
        }

        public IActionResult Index()
        {
            // Veritabanındaki tüm fiyat geçmişini alıyoruz.
            
            var guncelListe = _context.FiyatGecmisi
                .GroupBy(x => x.urun_adi)
                .Select(g => g.OrderByDescending(x => x.id).FirstOrDefault())
                .ToList();

            return View(guncelListe);
        }
    }
}