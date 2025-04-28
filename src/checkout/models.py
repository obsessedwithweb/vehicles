from django.db import models
from cart.models import CartItem
from vehicle.models import Vehicle

# Create your models here.
class Order(models.Model):

    class WilayaChoices(models.TextChoices):
        ADRAR = '01', 'Adrar'
        CHLEF = '02', 'Chlef'
        LAGHOUAT = '03', 'Laghouat'
        OUM_EL_BOUAGHI = '04', 'Oum El Bouaghi'
        BATNA = '05', 'Batna'
        BEJAIA = '06', 'Béjaïa'
        BISKRA = '07', 'Biskra'
        BECHAR = '08', 'Béchar'
        BLIDA = '09', 'Blida'
        BOUIRA = '10', 'Bouira'
        TAMANRASSET = '11', 'Tamanrasset'
        TEBESSA = '12', 'Tébessa'
        TLEMCEN = '13', 'Tlemcen'
        TIARET = '14', 'Tiaret'
        TIZI_OUZOU = '15', 'Tizi Ouzou'
        ALGER = '16', 'Alger'
        DJELFA = '17', 'Djelfa'
        JIJEL = '18', 'Jijel'
        SETIF = '19', 'Sétif'
        SAIDA = '20', 'Saïda'
        SKIKDA = '21', 'Skikda'
        SIDI_BEL_ABBES = '22', 'Sidi Bel Abbès'
        ANNABA = '23', 'Annaba'
        GUELMA = '24', 'Guelma'
        CONSTANTINE = '25', 'Constantine'
        MEDEA = '26', 'Médéa'
        MOSTAGANEM = '27', 'Mostaganem'
        MSILA = '28', 'M’Sila'
        MASCARA = '29', 'Mascara'
        OUARGLA = '30', 'Ouargla'
        ORAN = '31', 'Oran'
        EL_BAYADH = '32', 'El Bayadh'
        ILLIZI = '33', 'Illizi'
        BORDJ_BOU_ARRERIDJ = '34', 'Bordj Bou Arreridj'
        BOUMERDES = '35', 'Boumerdès'
        EL_TARF = '36', 'El Tarf'
        TINDOUF = '37', 'Tindouf'
        TISSEMSILT = '38', 'Tissemsilt'
        EL_OUED = '39', 'El Oued'
        KHENCHELA = '40', 'Khenchela'
        SOUK_AHRAS = '41', 'Souk Ahras'
        TIPAZA = '42', 'Tipaza'
        MILA = '43', 'Mila'
        AIN_DEFLA = '44', 'Aïn Defla'
        NAAMA = '45', 'Naâma'
        AIN_TEMOUCHENT = '46', 'Aïn Témouchent'
        GHARDAIA = '47', 'Ghardaïa'
        RELIZANE = '48', 'Relizane'
        TIMIMOUN = '49', 'Timimoun'
        BORDJ_BADJI_MOKHTAR = '50', 'Bordj Badji Mokhtar'
        OULED_DJELLAL = '51', 'Ouled Djellal'
        BENI_ABBES = '52', 'Béni Abbès'
        IN_SALAH = '53', 'In Salah'
        IN_GUEZZAM = '54', 'In Guezzam'
        TOUGGOURT = '55', 'Touggourt'
        DJANET = '56', 'Djanet'
        EL_MGHAIR = '57', 'El M’Ghair'
        EL_MENIAA = '58', 'El Meniaa'
        

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    wilaya = models.CharField(max_length=2, choices=WilayaChoices.choices)
    daira = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    session_id = models.CharField(max_length=40)
    
    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} × {self.product.name} in Order {self.order.id}"
        
    def get_total(self):
        return self.price * self.quantity
