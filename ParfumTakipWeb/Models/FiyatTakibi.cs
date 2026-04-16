using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ParfumTakipWeb.Models
{
    [Table("fiyat_takibi")]
    public class FiyatTakibi
    {
        [Key]
        public int id { get; set; }
        public string kullanici_mail { get; set; }
        public string urun_adi { get; set; }
        public double hedef_fiyat { get; set; }
        public bool aktif_mi { get; set; }
    }
}