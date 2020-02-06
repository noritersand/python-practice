def Necklace(self):
    return self

Jessica = Necklace('Jessica')
print(Jessica) # Jessica

Jessica = Necklace
print(Jessica('Jessica')) # Jessica

Jessica = "Necklace('Jessica')"
print(Jessica) # Necklace('Jessica')
