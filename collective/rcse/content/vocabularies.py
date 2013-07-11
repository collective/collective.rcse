from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm, TreeVocabulary

from collective.rcse.i18n import _t

gender = SimpleVocabulary([
    SimpleTerm(value=u"female", title=_t(u"Female")),
    SimpleTerm(value=u"male", title=_t(u"Male")),
    SimpleTerm(value=u"undefined", title=_t(u"Undefined")),
])

areas_of_expertise = SimpleVocabulary([
    SimpleTerm(value=u"area 1", title=_t(u"Area 1")),
    SimpleTerm(value=u"area 2", title=_t(u"Area 2")),
    SimpleTerm(value=u"area 3", title=_t(u"Area 3")),
])

languages = SimpleVocabulary([
    SimpleTerm(value=u"English", title=_t(u"English")),
    SimpleTerm(value=u"French", title=_t(u"French")),
    SimpleTerm(value=u"Italian", title=_t(u"Italian")),
    SimpleTerm(value=u"Spanish", title=_t(u"Spanish")),
])

interests = SimpleVocabulary([
    SimpleTerm(
        value=u"Emballages alimentaires",
        title=_t(u"Emballages alimentaires")
    ),
    SimpleTerm(
        value=u"Environnement",
        title=_t(u"Environnement")
    ),
    SimpleTerm(
        value=u"Evaluation sensorielle",
        title=_t(u"Evaluation sensorielle")
    ),
    SimpleTerm(
        value=u"Ingredients et formulation",
        title=_t(u"Ingredients et formulation")
    ),
    SimpleTerm(
        value=u"Innovation",
        title=_t(u"Innovation")
    ),
    SimpleTerm(
        value=u"Management",
        title=_t(u"Management")
    ),
    SimpleTerm(
        value=u"Management de la qualite",
        title=_t(u"Management de la qualite")
    ),
    SimpleTerm(
        value=u"Gestion de production",
        title=_t(u"Gestion de production")
    ),
    SimpleTerm(
        value=u"Marketing",
        title=_t(u"Marketing")
    ),
    SimpleTerm(
        value=u"Nutrition",
        title=_t(u"Nutrition")
    ),
    SimpleTerm(
        value=u"Reglementation",
        title=_t(u"Reglementation")
    ),
    SimpleTerm(
        value=u"Ressources humaines et developpement des competences",
        title=_t(u"Ressources humaines et developpement des competences")
    ),
    SimpleTerm(
        value=u"Securite des aliments",
        title=_t(u"Securite des aliments")
    ),
    SimpleTerm(
        value=u"Sante et Securite des personnes au travail",
        title=_t(u"Sante et Securite des personnes au travail")
    ),
    SimpleTerm(
        value=u"Techniques de laboratoire",
        title=_t(u"Techniques de laboratoire")
    ),
    SimpleTerm(
        value=u"Technologies et Process alimentaires",
        title=_t(u"Technologies et Process alimentaires")
    ),
])

functions = SimpleVocabulary([
    SimpleTerm(
        value=u"Achats",
        title=_t(u"Achats")
    ),
    SimpleTerm(
        value=u"Commercial - Ventes",
        title=_t(u"Commercial - Ventes")
    ),
    SimpleTerm(
        value=u"Direction",
        title=_t(u"Direction")
    ),
    SimpleTerm(
        value=u"Documentation - Reglementation",
        title=_t(u"Documentation - Reglementation")
    ),
    SimpleTerm(
        value=u"Emballage",
        title=_t(u"Emballage")
    ),
    SimpleTerm(
        value=u"Hygiene - Securite - Environnement",
        title=_t(u"Hygiene - Securite - Environnement")
    ),
    SimpleTerm(
        value=u"Ingenierie",
        title=_t(u"Ingenierie")
    ),
    SimpleTerm(
        value=u"Laboratoire - Analyses",
        title=_t(u"Laboratoire - Analyses")
    ),
    SimpleTerm(
        value=u"Logistique",
        title=_t(u"Logistique")
    ),
    SimpleTerm(
        value=u"Maintenance",
        title=_t(u"Maintenance")
    ),
    SimpleTerm(
        value=u"Marketing",
        title=_t(u"Marketing")
    ),
    SimpleTerm(
        value=u"Nutrition",
        title=_t(u"Nutrition")
    ),
    SimpleTerm(
        value=u"Production",
        title=_t(u"Production")
    ),
    SimpleTerm(
        value=u"Qualite - Securite des aliments",
        title=_t(u"Qualite - Securite des aliments")
    ),
    SimpleTerm(
        value=u"Recherche et Developpement - Innovation",
        title=_t(u"Recherche et Developpement - Innovation")
    ),
    SimpleTerm(
        value=u"Ressources humaines",
        title=_t(u"Ressources humaines")
    ),
    SimpleTerm(
        value=u"Services administratifs",
        title=_t(u"Services administratifs")
    ),
    SimpleTerm(
        value=u"Services techniques",
        title=_t(u"Services techniques")
    ),
    SimpleTerm(
        value=u"Autres",
        title=_t(u"Autres")
    ),
])

sector_terms = {
    (u'INDUSTRIES AGROALIMENTAIRES', _t(u'INDUSTRIES AGROALIMENTAIRES')): {
        (u'Viande et produits carnes', _t(u'Viande et produits carnes')): {},
        (u'Plats prepares et traiteur', _t(u'Plats prepares et traiteur')): {},
        (u'Produits laitiers et glaces', _t(u'Produits laitiers et glaces')): {},
        (u'Boulangerie - Viennoiserie - Patisserie', _t(u'Boulangerie - Viennoiserie - Patisserie')): {},
        (u'Sucre - Cacao - The - Cafe - Confiserie', _t(u'Sucre - Cacao - The - Cafe - Confiserie')): {},
        (u'Produits de la mer', _t(u'Produits de la mer')): {},
        (u'Boissons', _t(u'Boissons')): {},
        (u'Corps gras', _t(u'Corps gras')): {},
        (u'Pates - Riz - Produits cerealiers', _t(u'Pates - Riz - Produits cerealiers')): {},
        (u'Condiments - Assaisonnements', _t(u'Condiments - Assaisonnements')): {},
        (u'Fruits et legumes', _t(u'Fruits et legumes')): {},
        (u'Autres industries alimentaires', _t(u'Autres industries alimentaires')): {},
        (u'Aliments pour animaux', _t(u'Aliments pour animaux')): {},
        (u'Aliment homogeneise et dietetique', _t(u'Aliment homogeneise et dietetique')): {},
    },
    (u'FOURNISSEURS', _t(u'FOURNISSEURS')): {
        (u'Aromes', _t(u'Aromes')): {},
        (u'Additifs', _t(u'Additifs')): {},
        (u'Conseil - Ingenierie - Formation', _t(u'Conseil - Ingenierie - Formation')): {},
        (u'Emballages et materiaux au contact', _t(u'Emballages et materiaux au contact')): {},
        (u'Equipements - Procedes', _t(u'Equipements - Procedes')): {},
        (u'Hygiene et nettoyage', _t(u'Hygiene et nettoyage')): {},
        (u'Fournisseurs Autre', 'Fournisseurs Autre', _t(u"Autre")): {},
    },
    (u'AUTRES', _t(u'AUTRES')): {
        (u'Centre de recherche', _t(u'Centre de recherche')): {},
        (u'Institut technique agroalimentaire', _t(u'Institut technique agroalimentaire')): {},
        (u'Enseignement', _t(u'Enseignement')): {},
        (u'Autres Autre', 'Autres Autre', _t(u"Autre")): {},
    }
}
sector = TreeVocabulary.fromDict(sector_terms)
