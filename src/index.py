"""Varaston käyttömalli."""


from varasto import Varasto


def varastot(mehua, olutta):
    """Näyttää varastojen akuarvot ja getterit"""

    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {mehua}")
    print(f"Olutvarasto: {olutta}")

    print("Olut getterit:")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")

def mehuvarasto(mehua):
    """Käsittelee mehuvarastoa."""
    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")

def virheet():
    """Havainnollistaa virhetilanteita."""
    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)

    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)

def lisaaminen(olutta, mehua):
    """Havainnollistaa varastoon lisaamista."""
    print(f"Olutvarasto: {olutta}")
    print("olutta.lisaa_varastoon(1000.0)")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}")
    print("mehua.lisaa_varastoon(-666.0)")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")

def ota_mehusta(mehua):
    """Havainnollistaa mehuvarastosta ottamisen."""
    print(f"Mehuvarasto: {mehua}")
    print("mehua.otaVarastosta(-32.9)")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehua}")


def ottaminen(olutta, mehua):
    """Havainnollistaa varastosta ottamista."""
    print(f"Olutvarasto: {olutta}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    print(f"Olutvarasto: {olutta}")
    ota_mehusta(mehua)


def kasittele_varastot(mehua, olutta):
    """Antaa varastojen tiedot ja käsittelee niitä."""
    varastot(mehua, olutta)
    mehuvarasto(mehua)
    lisaaminen(olutta, mehua)
    ottaminen(olutta, mehua)

def main():
    """Suorittaa varasto-ohjelman annetut esimerkit."""
    mehua=Varasto(100.0)
    olutta=Varasto(100.0, 20.2)
    kasittele_varastot(mehua, olutta)
    virheet()

if __name__ == "__main__":
    main()
