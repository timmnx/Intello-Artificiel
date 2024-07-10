class Arbre:
  def __init__(self, grille :list, joueur :int, niveau_max :int, niveau :int) -> None:
    self.grille     :list   = grille
    self.joueur     :int    = joueur
    self.niveau_max :int    = niveau_max
    self.niveau     :int    = niveau
    #print(niveau, niveau_max)
    if self.niveau <= self.niveau_max-1:
      self.coups  :list   = self.grille.case(self.joueur)
      self.fils   :list   = []
      if len(self.coups) > 0:
        for coup in self.coups:
          grille :object  = self.grille.clone()
          grille.jouer(self.joueur, coup)
          self.fils   += [Arbre(grille, 1 if self.joueur==2 else 2, self.niveau_max, self.niveau+1)]

  def chercher(self) -> tuple:
    if self.niveau == self.niveau_max or len(self.coups) == 0:
      #print('fini', self.niveau)
      difference :int = self.grille.diff(1)
      return (difference, None)
    else:
      if self.joueur == 2:
        #print('mini', self.niveau)
        mini :tuple     = (float("inf"), None)
        for fils in self.fils:
          value :int  = fils.chercher()[0]
          if value < mini[0]:
            mini    = (value, self.coups[self.fils.index(fils)])
        return mini
      elif self.joueur == 1:
        #print('maxi', self.niveau)
        maxi :tuple     = (-float("inf"), None)
        for fils in self.fils:
          value :int  = fils.chercher()[0]
          if value > maxi[0]:
            maxi    = (value, self.coups[self.fils.index(fils)])
        return maxi
