using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ParfumTakipWeb.Models
{
    [Table("fiyat_gecmisi")]
    public class FiyatGecmisi
    {
        [Key]
        public int id { get; set; }
        public string urun_adi { get; set; }
        public string magaza { get; set; }
        public string url { get; set; }
        public double fiyat { get; set; }
        public string tarih { get; set; }

    }
}