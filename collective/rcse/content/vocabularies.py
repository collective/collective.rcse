from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm, TreeVocabulary

from collective.rcse.i18n import _


gender = SimpleVocabulary([
    SimpleTerm(value=u"female", title=_(u"Female")),
    SimpleTerm(value=u"male", title=_(u"Male")),
    SimpleTerm(value=u"undefined", title=_(u"Undefined")),
])

areas_of_expertise = SimpleVocabulary([
    SimpleTerm(value=u"area 1", title=_(u"Area 1")),
    SimpleTerm(value=u"area 2", title=_(u"Area 2")),
    SimpleTerm(value=u"area 3", title=_(u"Area 3")),
])

languages = SimpleVocabulary([
    SimpleTerm(value=u"English", title=_(u"English")),
    SimpleTerm(value=u"French", title=_(u"French")),
    SimpleTerm(value=u"Italian", title=_(u"Italian")),
    SimpleTerm(value=u"Spanish", title=_(u"Spanish")),
])

interests = SimpleVocabulary([
    SimpleTerm(
        value=u"Emballages alimentaires",
        title=_(u"Emballages alimentaires")
    ),
    SimpleTerm(
        value=u"Environnement",
        title=_(u"Environnement")
    ),
    SimpleTerm(
        value=u"Evaluation sensorielle",
        title=_(u"Evaluation sensorielle")
    ),
    SimpleTerm(
        value=u"Ingredients et formulation",
        title=_(u"Ingredients et formulation")
    ),
    SimpleTerm(
        value=u"Innovation",
        title=_(u"Innovation")
    ),
    SimpleTerm(
        value=u"Management",
        title=_(u"Management")
    ),
    SimpleTerm(
        value=u"Management de la qualite",
        title=_(u"Management de la qualite")
    ),
    SimpleTerm(
        value=u"Gestion de production",
        title=_(u"Gestion de production")
    ),
    SimpleTerm(
        value=u"Marketing",
        title=_(u"Marketing")
    ),
    SimpleTerm(
        value=u"Nutrition",
        title=_(u"Nutrition")
    ),
    SimpleTerm(
        value=u"Reglementation",
        title=_(u"Reglementation")
    ),
    SimpleTerm(
        value=u"Ressources humaines et developpement des competences",
        title=_(u"Ressources humaines et developpement des competences")
    ),
    SimpleTerm(
        value=u"Securite des aliments",
        title=_(u"Securite des aliments")
    ),
    SimpleTerm(
        value=u"Sante et Securite des personnes au travail",
        title=_(u"Sante et Securite des personnes au travail")
    ),
    SimpleTerm(
        value=u"Techniques de laboratoire",
        title=_(u"Techniques de laboratoire")
    ),
    SimpleTerm(
        value=u"Technologies et Process alimentaires",
        title=_(u"Technologies et Process alimentaires")
    ),
])

functions = SimpleVocabulary([
    SimpleTerm(
        value=u"Achats",
        title=_(u"Achats")
    ),
    SimpleTerm(
        value=u"Commercial - Ventes",
        title=_(u"Commercial - Ventes")
    ),
    SimpleTerm(
        value=u"Direction",
        title=_(u"Direction")
    ),
    SimpleTerm(
        value=u"Documentation - Reglementation",
        title=_(u"Documentation - Reglementation")
    ),
    SimpleTerm(
        value=u"Emballage",
        title=_(u"Emballage")
    ),
    SimpleTerm(
        value=u"Hygiene - Securite - Environnement",
        title=_(u"Hygiene - Securite - Environnement")
    ),
    SimpleTerm(
        value=u"Ingenierie",
        title=_(u"Ingenierie")
    ),
    SimpleTerm(
        value=u"Laboratoire - Analyses",
        title=_(u"Laboratoire - Analyses")
    ),
    SimpleTerm(
        value=u"Logistique",
        title=_(u"Logistique")
    ),
    SimpleTerm(
        value=u"Maintenance",
        title=_(u"Maintenance")
    ),
    SimpleTerm(
        value=u"Marketing",
        title=_(u"Marketing")
    ),
    SimpleTerm(
        value=u"Nutrition",
        title=_(u"Nutrition")
    ),
    SimpleTerm(
        value=u"Production",
        title=_(u"Production")
    ),
    SimpleTerm(
        value=u"Qualite - Securite des aliments",
        title=_(u"Qualite - Securite des aliments")
    ),
    SimpleTerm(
        value=u"Recherche et Developpement - Innovation",
        title=_(u"Recherche et Developpement - Innovation")
    ),
    SimpleTerm(
        value=u"Ressources humaines",
        title=_(u"Ressources humaines")
    ),
    SimpleTerm(
        value=u"Services administratifs",
        title=_(u"Services administratifs")
    ),
    SimpleTerm(
        value=u"Services techniques",
        title=_(u"Services techniques")
    ),
    SimpleTerm(
        value=u"Autres",
        title=_(u"Autres")
    ),
])

sector_terms = {
    (u'INDUSTRIES AGROALIMENTAIRES', _(u'INDUSTRIES AGROALIMENTAIRES')): {
        (u'Viande et produits carnes', _(u'Viande et produits carnes')): {},
        (u'Plats prepares et traiteur', _(u'Plats prepares et traiteur')): {},
        (u'Produits laitiers et glaces', _(u'Produits laitiers et glaces')): {},
        (u'Boulangerie - Viennoiserie - Patisserie', _(u'Boulangerie - Viennoiserie - Patisserie')): {},
        (u'Sucre - Cacao - The - Cafe - Confiserie', _(u'Sucre - Cacao - The - Cafe - Confiserie')): {},
        (u'Produits de la mer', _(u'Produits de la mer')): {},
        (u'Boissons', _(u'Boissons')): {},
        (u'Corps gras', _(u'Corps gras')): {},
        (u'Pates - Riz - Produits cerealiers', _(u'Pates - Riz - Produits cerealiers')): {},
        (u'Condiments - Assaisonnements', _(u'Condiments - Assaisonnements')): {},
        (u'Fruits et legumes', _(u'Fruits et legumes')): {},
        (u'Autres industries alimentaires', _(u'Autres industries alimentaires')): {},
        (u'Aliments pour animaux', _(u'Aliments pour animaux')): {},
        (u'Aliment homogeneise et dietetique', _(u'Aliment homogeneise et dietetique')): {},
    },
    (u'FOURNISSEURS', _(u'FOURNISSEURS')): {
        (u'Aromes', _(u'Aromes')): {},
        (u'Additifs', _(u'Additifs')): {},
        (u'Conseil - Ingenierie - Formation', _(u'Conseil - Ingenierie - Formation')): {},
        (u'Emballages et materiaux au contact', _(u'Emballages et materiaux au contact')): {},
        (u'Equipements - Procedes', _(u'Equipements - Procedes')): {},
        (u'Hygiene et nettoyage', _(u'Hygiene et nettoyage')): {},
        (u'Fournisseurs Autre', 'Fournisseurs Autre', _(u"Autre")): {},
    },
    (u'AUTRES', _(u'AUTRES')): {
        (u'Centre de recherche', _(u'Centre de recherche')): {},
        (u'Institut technique agroalimentaire', _(u'Institut technique agroalimentaire')): {},
        (u'Enseignement', _(u'Enseignement')): {},
        (u'Autres Autre', 'Autres Autre', _(u"Autre")): {},
    }
}
sector = TreeVocabulary.fromDict(sector_terms)
